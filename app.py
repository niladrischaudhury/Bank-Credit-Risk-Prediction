from distutils.log import debug
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Bank Credit Risk Prediction App in Progress"

if __name__ == "__main__":
    app.run(debug=True)