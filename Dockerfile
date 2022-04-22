FROM python:3.10
WORKDIR /app/backend
COPY ./src/backend/app ./app
COPY ./requirements.txt .
RUN python -m venv venv 
RUN . venv/bin/activate
RUN pip install -r requirements.txt
CMD flask run --host=0.0.0.0 --port 5000
