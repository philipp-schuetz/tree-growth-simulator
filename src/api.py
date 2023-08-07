# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring

import random
import time
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, StreamingResponse

from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from modules.app import App

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def create_request_id():
	timestamp = int(time.time() * 1000)
	random_part = random.randint(0, 999999)
	unique_id = f'{timestamp:013d}{random_part:06d}'
	return unique_id

@app.get('/')
async def read_root():
	return {
		'info': """Welcome to the API of the tree-growth-simulator project.
		Please note that this API is rate limited to 2 generation requests per minute.
		For more information see: https://github.com/philipp-schuetz/tree-growth-simulator"""
		}

@app.get('/github')
async def redirect_to_github():
	return RedirectResponse('https://github.com/philipp-schuetz/tree-growth-simulator')

@app.put('/generate')
@limiter.limit('2/minute')
async def generate_model(
	request: Request,
	mod_light: int=100, mod_water:int=100, mod_temperature:int=100, mod_nutrients:int=100,
	light_sides_front:bool=True, light_sides_back:bool=True, light_sides_left:bool=True,
	light_sides_right:bool=True, light_sides_top:bool=True,
	leafes:bool=False
	):
	request_id = create_request_id()
	light_sides = [
		light_sides_front, light_sides_back, light_sides_left, light_sides_right, light_sides_top
		]
	App().api_run(
		request_id, mod_light, mod_water, mod_temperature, mod_nutrients, leafes, light_sides
		)

	zip_name = f'{request_id}.zip'

	file_path_1 = Path(f'plots/{request_id}_1.png')
	if leafes:
		file_path_2 = Path(f'plots/{request_id}_2.png')

	buffer = BytesIO()
	with ZipFile(buffer, "w") as zipf:
		zipf.write(file_path_1, f'{request_id}_1.png')
		if leafes:
			zipf.write(file_path_2, f'{request_id}_2.png')

	file_path_1.unlink()
	if leafes:
		file_path_2.unlink()

	response = StreamingResponse(iter([buffer.getvalue()]), media_type="application/x-zip-compressed")
	response.headers["Content-Disposition"] = f'attachment; filename={zip_name}'

	return response
