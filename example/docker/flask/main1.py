from flask import Flask, render_template
import os

wd = os.getcwd()
app = Flask(__name__, template_folder=wd)

@app.route("/")
def index():    
    return render_template("1.html")


@app.route("/sheet2/") 
def sheet2():
    return render_template("2.html")

app.run(host="0.0.0.0")