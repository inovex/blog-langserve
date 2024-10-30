FROM python:3.12

WORKDIR /app

COPY . /app/

# setuptoolsneed to be installed before the other packages from requirements.txt
RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
