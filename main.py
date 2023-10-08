from flask import Flask, redirect


app = Flask(__name__, template_folder="templates/")


@app.route("/")
def hello():
    return


if __name__ == '__main__':
    app.run(debug=True)
