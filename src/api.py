from typing import Union
import random
import time
from modules.app import App

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse

app = FastAPI()

def create_id():
	timestamp = int(time.time() * 1000)
	random_part = random.randint(0, 999999)
	unique_id = f'{timestamp:013d}{random_part:06d}'
	return unique_id

@app.get('/')
async def read_root():
	return {'info': 'Welcome to the API of the tree-growth-simulator project. Please note that this API is rate limited to 2 generation requests per minute. For more information see: https://github.com/philipp-schuetz/tree-growth-simulator'}

@app.get('/github')
async def redirect_typer():
    return RedirectResponse('https://github.com/philipp-schuetz/tree-growth-simulator')

@app.put('/generate')
async def update_item(mod_light: int, mod_water:int, mod_temperature:int, mod_nutrients:int, light_sides_front:bool, light_sides_back:bool, light_sides_left:bool, light_sides_right:bool, light_sides_top:bool,leafes:bool):
	id = create_id()
	light_sides = [light_sides_front, light_sides_back, light_sides_left, light_sides_right, light_sides_top]
	App().api_run(id, mod_light, mod_water, mod_temperature, mod_nutrients, leafes, light_sides)

	# script that deletes generated files after 5 minutes (cron)
	return FileResponse(f'folder/{id}')
