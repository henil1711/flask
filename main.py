from flask import Flask, jsonify, render_template, request, make_response
import pymysql


app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "flask"
db = pymysql.connect(
    host=app.config["MYSQL_HOST"],
    user=app.config["MYSQL_USER"],
    password=app.config["MYSQL_PASSWORD"],
    db=app.config["MYSQL_DB"],
)


@app.route("/", methods=["GET"])
def get_word():
    cursor = db.cursor()
    cursor.execute("SELECT name FROM task")
    result = cursor.fetchone()
    word = result[0] if result else "Word"
    return make_response(word)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        word = request.form["word"]
        cursor = db.cursor()
        cursor.execute("TRUNCATE TABLE task")
        cursor.execute("INSERT INTO task (name) VALUES (%s)", word)
        db.commit()
    return render_template("admin.html")




if __name__ == "__main__":
    app.run()
