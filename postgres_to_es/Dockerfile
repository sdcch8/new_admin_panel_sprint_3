FROM python:3.10

WORKDIR /opt/postgres_to_es

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .

CMD python main.py