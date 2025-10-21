from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB connection (use atlas)
MONGO_URI=os.getenv("mongodb+srv://task_managmeny_system:<db_password>@cluster0.kk06hhq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client= MongoClient("MONGO_URI")
db = client["task_management"]
tasks = db["tasks"]

@app.route('/')
def index():
    all_tasks = list(tasks.find())
    return render_template('index.html', tasks=all_tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        tasks.insert_one({"title": title, "desc": desc, "status": "Pending"})
        return redirect('/')
    return render_template('add_task.html')

@app.route('/complete/<id>')
def complete_task(id):
    tasks.update_one({'_id': ObjectId(id)}, {'$set': {'status': 'Completed'}})
    return redirect('/')

@app.route('/delete/<id>')
def delete_task(id):
    tasks.delete_one({'_id': ObjectId(id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)