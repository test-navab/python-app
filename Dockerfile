FROM python:alpine3.18

WORKDIR /app

COPY . .

RUN pip install cryptography && \
    pip install pymysql && \
    pip install flask   && \
    pip install python-dotenv && \
    pip install mysql-connector-python

EXPOSE 5000

CMD ["python3", "app.py"]