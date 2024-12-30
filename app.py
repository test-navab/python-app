from flask import Flask, render_template, request
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

app = Flask(__name__)

# Create a connection to the MySQL database
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    port=DB_PORT
)

# Create the users table if it doesn't exist
with conn.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usersdata (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255),
            email VARCHAR(255),
            age INT,
            gender VARCHAR(10)
        )
    """)
    conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']

        with conn.cursor() as cursor:
            # Check if a record with the same email already exists in the table
            cursor.execute("SELECT * FROM usersdata WHERE email=%s", (email,))
            result = cursor.fetchone()

            if result:
                # If a record with the same email already exists, return a message
                return f"<p style='font-size: 30px; color: red;'>Details for {name} ({email}) already exist in the database!</p>"
            else:
                # If a record with the same email doesn't exist, execute the INSERT query
                sql = "INSERT INTO usersdata (name, email, age, gender) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, email, age, gender))
                conn.commit()

                return f"<p style='font-size: 30px; color: green;'>Thank you for submitting your details, {name} ({email})!</p>"

    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

