import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

mysql = MySQL(app)


def createJWT(username, secret, admin):
    return jwt.encode(
        {
            "username": username,
            "expire_at": datetime.datetime.now(tz=datetime.datetime.utc) + datetime.timedelta(days=1),
            "issued_at": datetime.datetime.now(tz=datetime.datetime.utc),
            "admin": admin
        }, 
        secret, 
        algorithm="HS256"
    )


@app.route("/login", methods=["POST"])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return "missing credentials", 401
    
    cur = mysql.connection.cursor()
    res = cur.execute("SELECT email, password FROM user WHERE email=%s;", (auth.username))

    if res:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username == email and auth.password == password:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)

    return "invalid credentials", 401


@app.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401
    
    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(encoded_jwt, os.environ.get("JWT_SECRET"), algorithms="HS256")
        return decoded, 200
    except:
        return "not authorized", 403



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)