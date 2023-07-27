from typing import Union
import random

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
	return {'info': 'Welcome to the API of the tree-growth-simulator project. Please note that this API is rate limited to 2 generation requests per minute. For more information see: https://github.com/philipp-schuetz/tree-growth-simulator'}


@app.put('/generate/')
def update_item(mod_light: int, mod_water:int, mod_temperature:int, mod_nutrients:int, light_sides_front:bool, light_sides_back:bool, light_sides_left:bool, light_sides_right:bool, light_sides_top:bool,leafes:bool):
	id = random.randint(10000000, 99999999)
	# check in database if id is being used, if so regenerate
	# script that deletes generated files after 5 minutes (cron)
	return {'result': 'https://127.0.0.1/results/{id}'}
