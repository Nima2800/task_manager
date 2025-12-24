from flask import Flask,render_template,redirect,request,url_for,Response
import uuid
import pandas as pd
from datetime import datetime
import json


app = Flask(__name__)

tasks = [

]

@app.route("/")
def main_page():
    if tasks :
        try:
            tasks.sort(key=lambda x: datetime.strptime(x["start_time"], "%H:%M"))
        except:
            pass
    return render_template("index.html",tasks = tasks)


@app.post("/add_task")
def add_task():
    title = request.form.get('title')
    des = request.form.get('description')
    status = request.form.get('status')
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    
    tasks.append({"id":uuid.uuid4().int , "title" : title , "description":des , "status":status , "start_time":start_time,"end_time":end_time})
    return redirect("/")

@app.route("/update_task/<int:task_id>",methods=['POST'])
def update_task(task_id):
    title = request.form.get('title')
    des = request.form.get('description')
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    
    for task in tasks:
        if task["id"] == task_id:
            task["title"]=title
            task["description"] =des
            task["start_time"]=start_time
            task["end_time"] =end_time
    
    return redirect(url_for("main_page"))

@app.route("/delete/<int:task_id>",methods=["GET"])
def delete(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
    
    return redirect(url_for("main_page"))


@app.route("/toggle_status/<int:task_id>",methods = ["POST"])
def toggle_status(task_id):
    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "Completed":
                task["status"] = "Pending"
            else:
                task["status"] = "Completed"
    
    return redirect(url_for("main_page"))

@app.route("/import_excel",methods = ["POST"])
def import_excel():
    excel = request.files.get('excel')
    
    file = pd.read_excel(excel)

    for row in file.itertuples():
        title = row[1]
        des =  row[2]
        status =  row[3]
        if status == "انجام شده" or status == "Completed":
            status = "Completed"
        else:
            status = "Pending"
            
        start_time =  row[4]
        end_time =  row[5]
        
        tasks.append({"id":uuid.uuid4().int , "title" : title , "description":des , "status":status , "start_time":start_time,"end_time":end_time})
        
    return redirect("/")
    
    
@app.route("/export_json", methods=["GET"])
def export_json():
    json_output = json.dumps(tasks, ensure_ascii=False, indent=2)
    return Response(
        json_output,
        mimetype="application/json",
        headers={
            "Content-Disposition": "attachment; filename=tasks.json"
        }
    )