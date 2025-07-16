import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import json
from peewee import *
from playhouse.shortcuts import model_to_dict
import datetime

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri = True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

# print(mydb)

class TimelinePost(Model):
    name= CharField()
    email= CharField()
    content= TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost], safe=True)

@app.route('/')
def index():
    json_path_edu = os.path.join(app.root_path,"data", "education.json")
    json_path_exp = os.path.join(app.root_path,"data", "experience.json")
    with open(json_path_exp) as f:
        experience = json.load(f)
    with open(json_path_edu) as f:
        education = json.load(f)
    return render_template('index.html', title="Miguel's Portfolio", url=os.getenv("URL"), education=education, experience=experience)

@app.route('/hobbies')
def hobbies():
    json_path = os.path.join(app.root_path, "data", "hobbies.json")
    with open(json_path) as f:
        hobbies_data = json.load(f)
    return render_template('hobbies.html', title="My Hobbies", url=os.getenv("URL"), hobbies=hobbies_data["hobbies"])

@app.route('/map')
def map():
    return render_template('map.html', title="Places I've been to", url=os.getenv("URL"))

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if not name or not name.strip():
        return jsonify({'error': 'Invalid name'}), 400
    if not content or not content.strip():
        return jsonify({'error': 'Invalid content'}), 400

    if not email or not email.strip():
        return jsonify({'error': 'Invalid email'}), 400

    email_s = email.strip()
    if '@' not in email_s or '.' not in email_s:
        return jsonify({'error': 'Invalid email'}), 400

    timeline_post = TimelinePost.create(name=name.strip(), email=email.strip(), content=content.strip())
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in 
TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
@app.route('/api/timeline_post/<id>', methods=['DELETE'])
def timeline_post_delete(id):
    timeline_post = TimelinePost.get(id)
    if timeline_post:
        timeline_post.delete_instance()
        return {'message': 'Timeline post deleted successfully'}, 200
    else: 
        return {'message': 'Timeline post not found'}, 404
    
@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline", url=os.getenv("URL"))
