FROM python:3.13.12-slim

WORKDIR /myapp

COPY app.py /myapp/
COPY requirements.txt /myapp/

RUN pip install --no-cache-dir -r requirements.txt


CMD [ "python","app.py" ]