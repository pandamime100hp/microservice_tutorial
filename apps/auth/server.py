import os

from flask import Flask, request
from flask_mysqldb import MySQL

from jwt_token import jwt


app = Flask(__name__)
mysql = MySQL(app)

app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))


@app.route("/login", methods=["POST"])
def login() -> tuple[str, int]:
    authorization  = request.authorization

    if not authorization or not authorization.username or not authorization.password:
        return "missing credentials", 401
    
    cursor = mysql.connection.cursor()
    response = cursor.execute(f"SELECT email, password FROM user WHERE email='{authorization.username}';")

    if response:
        user_row = cursor.fetchone()
        email = user_row[0]
        password = user_row[1]

        if authorization.username == email and authorization.password == password:
            return jwt.create(authorization.username, os.environ.get("JWT_SECRET"), True), 200

    return "invalid credentials", 401


@app.route("/validate", methods=["POST"])
def validate() -> tuple[str, int]:
    authorization: str = request.headers.get("Authorization")

    if not authorization:
        return "missing credentials", 401
    
    encoded_jwt: str = authorization.split(" ")[1]

    try:
        return jwt.decode(
            token=encoded_jwt, 
            secret=os.environ.get("JWT_SECRET")
        ), 200
    except:
        return "not authorized", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)