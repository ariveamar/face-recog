FROM python:3.10.6
WORKDIR /usr/src/app
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y iputils-ping
COPY requirements.txt ./
RUN pip install -U pip wheel cmake
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]
