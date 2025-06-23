import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    json_path_edu = os.path.join(app.root_path,"data", "education.json")
    json_path_exp = os.path.join(app.root_path,"data", "experience.json")
    with open(json_path_exp) as f:
        experience = json.load(f)
    with open(json_path_edu) as f:
        education = json.load(f)
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), education=education, experience=experience)

@app.route('/hobbies')
def hobbies():
    json_path = os.path.join(app.root_path, "data", "hobbies.json")
    with open(json_path) as f:
        hobbies_data = json.load(f)
    return render_template('hobbies.html', title="My Hobbies", url=os.getenv("URL"), hobbies=hobbies_data["hobbies"])

@app.route('/map')
def map():
    return render_template('map.html', title="Places I've been to", url=os.getenv("URL"))
