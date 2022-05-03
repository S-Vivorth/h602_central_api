FROM python:3.8


COPY ./h602_central ./app/h602_central

COPY ./h602_central/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["python","./app/h602_central/main.py"]