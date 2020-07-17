from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") 
def hello():
    return "Hello World!"

@app.route("/home")
def homepage():
    return "Welcome to my Homepage!"

@app.route("/education")
def education():
    return "Happy learning from our education unit!"

if __name__ == "__main__":
    app.run(debug= True, host= "localhost", port = 3000)








