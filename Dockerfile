FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./requirements_api.txt /code/requirements_api.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements_api.txt

COPY ./src /code

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
