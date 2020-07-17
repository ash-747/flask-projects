from flask import Flask

app = Flask(__name__)

@app.route ("/")
def home():
    return 'Open a new tab and enter /Welcome/name for URL'

@app.route ("/welcome/<name>")
def welcome(name):
    return 'Welcome ' + name + '!'

if __name__ == "__main__":
    app.run(debug = True, host = "localhost", port = 3000)