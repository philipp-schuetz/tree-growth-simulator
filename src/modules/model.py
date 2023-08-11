import random
import logging
from pathlib import Path
import os
import numpy as np
import matplotlib.pyplot as plt
from modules.config import config

class Model:
	"""Model holds the tree model and all utilities to generate it"""
	def __init__(self):
		# create variable for model dimensions and set them with config
		self.width = -1
		self.height = -1
		self.set_dimensions()

		# get material ids from config
		ids = config.get_material_id()
		self.id_air = ids['air']
		self.id_leaf = ids['leaf']
		self.id_wood = ids['wood']
		self.id_wall = ids['wall']

		colors = config.get_material_colors()
		self.color_leaf = colors['leaf']
		self.color_wood = colors['wood']

		# create array for tree model
		self.model = np.zeros((self.width, self.height, self.width))

		# modifiers
		self.light = -1
		self.water = -1
		self.temperature = -1
		self.nutrients = -1

		# minimum values
		self.minimum_light = -1
		self.minimum_water = -1
		self.minimum_temperature = -1
		self.minimum_nutrients = -1
		self.set_minimum_values()

		# base material and radius for tree generation
		self.material = self.id_wood
		self.radius = 0

		# set first positions
		self.start_position = [int(self.width/2+0.5), self.height-1, int(self.width/2+0.5)]
		self.current_direction = 0
		self.position = self.start_position.copy()

		self.saved_position = []
		self.saved_direction = []
		self.saved_radius = []

		self.radius_mode = 'trunk'

		self.activated_sides = ['front','back','left','right','top']

		self.leaf_generation = False

		# increases after model has finished generating to prevent generation of multiple models in one array
		self.model_generated = 0

		self.api_id = ''


	def set_minimum_values(self):
		"""set minimum values for modifiers"""
		minimum_values = config.get_minimum_values()

		self.minimum_light = minimum_values[0]
		self.minimum_water = minimum_values[1]
		self.minimum_temperature = minimum_values[2]
		self.minimum_nutrients = minimum_values[3]

	def set_light_sides(self, sides: list[bool]):
		"""format of sides: [front, back, left, right, top]"""
		self.activated_sides = ['front','back','left','right','top']
		to_remove = []
		for i in range(len(sides)):
			if not sides[i]:
				to_remove.append(self.activated_sides[i])
		for item in to_remove:
			self.activated_sides.remove(item)

	def set_leaf_generation(self, status:bool):
		"""set whether leaf generation is enabled"""
		self.leaf_generation = status

	def set_dimensions(self):
		'fetch and set model dimensions from config file'
		dimensions = config.get_model_dimensions()
		self.width = dimensions['width']
		self.height = dimensions['height']

	def set_modifiers(self, light:int, water:int, temperature:int, nutrients:int):
		"""set modifiers from ui"""
		self.light = light
		self.water = water
		self.temperature = temperature
		self.nutrients = nutrients

	def set_api_id(self, id:str):
		"""set the api call id"""
		self.api_id = id

	def save(self):
		"""save model in file"""
		np.save('../saves/lightarr.npy', self.model)


	# ---------------- model generation ----------------

	def place_voxel(self):
		"""set current voxel(s) to specified material"""
		try:
			if self.radius > 1:
				for layer in range(self.width):
					for voxel in range(self.width):
						distance = np.sqrt(
							(layer - self.position[0])**2 + (voxel - self.position[2])**2
							)
						if distance <= self.radius:
							self.model[layer,self.position[1],voxel] = self.material
			elif self.radius == 1:
				self.model[self.position[0],self.position[1],self.position[2]] = self.material
			else:
				raise ValueError("radius for voxel placement can't be negative")
		except IndexError:
			pass

	def is_next_to(self, material_id:int) -> bool: # TODO check if method is working properly
		"""return True if voxel has given material next to it"""
		coordinates = self.position
		out = False
		try:
			# back
			if self.model[coordinates[0]-1,coordinates[1],coordinates[2]] == material_id:
				out = True
			# front
			if self.model[coordinates[0]+1,coordinates[1],coordinates[2]] == material_id:
				out = True
			# bottom
			if self.model[coordinates[0],coordinates[1]-1,coordinates[2]] == material_id:
				out = True
			# top
			if self.model[coordinates[0],coordinates[1]+1,coordinates[2]] == material_id:
				out = True
			# left
			if self.model[coordinates[0],coordinates[1],coordinates[2]-1] == material_id:
				out = True
			# right
			if self.model[coordinates[0],coordinates[1],coordinates[2]+1] == material_id:
				out = True
			out = False
		except IndexError:
			out = False
		return out

	def forward(self):
		"""move one voxel in the current direction"""
		match self.current_direction:
			case 0:# positive layer - forward
				self.position[0] = self.position[0]+1
			case 1: # negative voxel - right
				self.position[2] = self.position[2]-1
			case 2:# negative layer - back
				self.position[0] = self.position[0]-1
			case 3: # positive voxel - left
				self.position[2] = self.position[2]+1

	def right(self):
		"""turn right 90°"""
		self.current_direction += 1
		if self.current_direction > 3:
			self.current_direction = 0

	def left(self):
		"""turn left 90°"""
		self.current_direction -= 1
		if self.current_direction  < 0:
			self.current_direction = 3

	def up(self):
		"""move up one voxel"""
		self.position[1] -= 1

	def down(self):
		"""move down one voxel"""
		self.position[1] += 1

	def set_radius(self, amount:int):
		"""change radius size by the set amount"""
		radius = self.radius
		radius += amount
		if radius >= 1:
			self.radius = radius
		else:
			return

	def save_position(self):
		"""save current position"""
		self.saved_position.append(self.position)

	def get_position(self):
		"""get the position last saved"""
		if len(self.saved_position) > 0:
			self.position = self.saved_position.pop(-1)

	def save_direction(self):
		"""save current direction"""
		self.saved_direction.append(self.current_direction)

	def get_direction(self):
		"""get the direction last saved"""
		if len(self.saved_direction) > 0:
			self.current_direction = self.saved_direction.pop(-1)

	def save_radius(self):
		"""save current radius"""
		self.saved_radius.append(self.radius)

	def get_radius(self):
		"""get the radius last saved"""
		if len(self.saved_radius) > 0:
			self.radius = self.saved_radius.pop(-1)

	def save_positioning(self):
		"""save current position, direction and radius"""
		self.save_position()
		self.save_direction()
		self.save_radius()

	def get_positioning(self):
		"""get saved position, direction and radius"""
		self.get_position()
		self.get_direction()
		self.get_radius()

	def is_within_bounds(self):
		"""Check if the current position is within the bounds of the model"""
		x, y, z = self.position
		return 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.width

	def light_minimum_reached(self) -> bool:
		"""calculate and check if light level is above minimum on current position"""
		directions = [(-1, 0, 0), (1, 0, 0), (0, 0, -1), (0, 0, 1), (0, -1, 0)]
		# front back left right top
		if 'front' not in self.activated_sides:
			directions[0] = 0
		if 'back' not in self.activated_sides:
			directions[1] = 0
		if 'left' not in self.activated_sides:
			directions[2] = 0
		if 'right' not in self.activated_sides:
			directions[3] = 0
		if 'top' not in self.activated_sides:
			directions[4] = 0

		total_light = 0

		for direction in directions:
			if direction == 0:
				continue
			object_count = 0
			for x in range(1, 250):
				dx, dy, dz = direction
				new_x = self.position[0] + dx*x
				new_y = self.position[1] + dy*x
				new_z = self.position[2] + dz*x

				try:
					if self.model[new_x,new_y,new_z] != 0:
						object_count += 1
				except IndexError:
					pass

			if object_count == 0:
				total_light += self.light

		return total_light/2 >= self.minimum_light


	def generate_model(self):
		"""main method for tree structure generation"""
		# reset contents of model when generation without restarting the app
		if self.model_generated > 0:
			self.model = np.zeros((self.width, self.height, self.width))
		logging.info('starting model generation')
		self.radius = 5 # start_radius
		branch_length = 20
		iterations = 6
		min_branching_height = 40 # height at which branches start appearing

		# ---- calculate and apply modifiers ----
		# abort when minimum values are not reached
		if self.water < self.minimum_water:
			return
		if self.temperature < self.minimum_temperature:
			return
		if self.nutrients < self.minimum_nutrients:
			return

		if self.temperature/100 > 1:
			self.water *= self.temperature/100

		if self.water/100 <= 1.5:
			branch_length *= self.water/100
			min_branching_height *= self.water/100
		elif self.water/100 > 1.5:
			branch_length *= 1-self.water/100
			min_branching_height *= 1-self.water/100

		if self.nutrients/100 <= 1.5:
			branch_length *= self.nutrients/100
			min_branching_height *= self.nutrients/100
		elif self.nutrients/100 > 1.5:
			branch_length *= 1-self.nutrients/100
			min_branching_height *= 1-self.water/100


		branching_position = []
		branching_radius = []
		branching_position_tmp = []
		branching_radius_tmp = []

		# generate main trunk
		for i in range(int(min_branching_height)):
			self.place_voxel()
			self.up()
			if i % 20 == 0:
				self.set_radius(-1)
		branching_position.append(self.position)
		branching_radius.append(self.radius)

		for i in range(iterations):
			random.shuffle(branching_position)
			for bp in range(len(branching_position)):
				start_pos = branching_position[bp]
				start_radius = branching_radius[bp]

				for d in range(4):
					# chance to skip branch
					if iterations < 2 and random.randrange(128) == 0:
						continue
					if 2 <= iterations < 4 and random.randrange(6) == 0:
						continue
					if iterations >= 4 and random.randrange(2) == 0:
						continue

					self.position = start_pos.copy()
					self.radius = start_radius
					self.current_direction = d
					# branch_length += random.randrange(-2,i)
					for m in range(int(branch_length)):
						self.forward()
						if not self.light_minimum_reached():
							break
						self.place_voxel()
						for du in range(random.randrange(8)):
							self.up()
						for dd in range(random.randrange(4)):
							self.down()
						self.set_radius(-1)
					# save branch end
					branching_position_tmp.append(self.position)
					branching_radius_tmp.append(self.radius)

			branching_position = branching_position_tmp.copy()
			branching_position_tmp = []
			branching_radius = branching_radius_tmp.copy()
			branching_radius_tmp = []

		if self.leaf_generation:
			logging.info('starting leaf generation')
			# ---- generate leaves ---- # check thickness of wood
			for layer in range(0, self.width):
				for row in range(0, int(self.height-min_branching_height)): # start leaf generation on branching height
					for voxel in range(0, self.width):
						# check if voxel is next to wood and minimum lightlevel is reached
						self.position = [layer,row,voxel]
						if self.is_next_to(self.id_wood) and self.light_minimum_reached():
							# add leaf
							self.model[layer,row,voxel] = self.id_leaf

		self.model_generated += 1
		logging.info('model generation has finished')

	# ---------------- display model ----------------
	def mathplotlib_plot(self, save:bool = False, filename:str = 'out', api:bool = False):
		"""generate a 3d plot to visualize the tree model"""
		# TODO make save option available through local ui
		if filename == 'out':
			filename = config.get_plot_filename()

		# create output directory if it doesnt exist
		if save and not os.path.exists('plots'):
			os.makedirs('plots')

		if not self.leaf_generation:
			x = 1
		else:
			x = 2

		for i in range(x):
			# Plot the resulting tree model
			fig = plt.figure(num=int(i+1))
			if i == 0:
				fig.suptitle('Tree Structure')
			else:
				fig.suptitle('Tree Structure + Leaves')
			ax = fig.add_subplot(111, projection='3d')

			# Get the coordinates of the wood voxels
			x, y, z = np.where(self.model == self.id_wood)
			if i == 1:
				x1, y1, z1 = np.where(self.model == self.id_leaf)

			# plot voxels with correct orientation
			ax.scatter(x, z, -y, color=self.color_wood, marker='s')
			if i == 1:
				ax.scatter(x1, z1, -y1, color=self.color_leaf, marker='s')

			# Set the limits for the axes
			ax.set_xlim(0, self.model.shape[0])
			ax.set_ylim(0, self.model.shape[2])
			ax.set_zlim(-self.model.shape[1], 0)

			# Set labels for the axes
			ax.set_xlabel('X')
			ax.set_ylabel('Z')
			ax.set_zlabel('Y')

			if save:
				file_path = Path(f'plots/{filename}_{i+1}.png')
				plt.savefig(file_path)
		if not api:
			plt.show()
