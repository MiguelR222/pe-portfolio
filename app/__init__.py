import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/about')
def about():
    json_path_edu = os.path.join(app.root_path,"data", "education.json")
    json_path_exp = os.path.join(app.root_path,"data", "experience.json")
    with open(json_path_exp) as f:
        experience = json.load(f)
    with open(json_path_edu) as f:
        education = json.load(f)
    return render_template('about.html', title="About", url=os.getenv("URL"), education=education, experience=experience)

@app.route('/map')
def map():
    return render_template('map.html', title="Places I've been to", url=os.getenv("URL"))
