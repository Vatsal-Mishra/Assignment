import requests                                              #importing libraries for retreiving data
from datetimerange import DateTimeRange                      # to define a time range
import datetime                                              # to make datetime objects
import json
import time                                                    #to make json files
from flask import Flask,jsonify, render_template,request
app=Flask(__name__)
@app.route("/")
def register():
    return render_template("form.html")
@app.route("/insert",methods=["POST"])
def insert():
    res=requests.get(" https://gitlab.com/-/snippets/2067888/raw/master/sample_json_2.json")   #requesting for data
    data=res.json()
    if res.status_code !=200:
       print("WARNING:There was some error retreiving data ")                                #error warning if something goes wrong
    start_time=request.form.get("starttime")     # taking all the information from the form entered by users
    end_time=request.form.get("endtime")
    start_time=datetime.datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%SZ")
    end_time=datetime.datetime.strptime(end_time,"%Y-%m-%dT%H:%M:%SZ")
    total_runtime=total_downtime=0
    for item in data:
        if item["time"] in DateTimeRange(start_time,end_time):              #traversing in interval
          if item["runtime"]<1021:                                         #checking for runtime and downtime
            total_runtime+=item["runtime"]
          else:
            total_runtime+=1021
            f_runtime=item["runtime"]-1021
            total_downtime+=f_runtime
    machine_utilization=(total_runtime/(total_runtime+total_downtime))*100     #calculating utilization
    machine_utilization=round(machine_utilization,2)
    total_runtime=time.strftime("%H:%M:%S", time.gmtime(total_runtime))         #formatting in %h%m%s
    total_downtime=time.strftime("%H:%M:%S", time.gmtime(total_downtime))
    machine_data=[
       {                                                                #making json
       "runtime":total_runtime,
       "downtime":total_downtime,
       "utilization":machine_utilization
       }
       ]
    return jsonify(data=machine_data)
if __name__=="__main__" :
     app.run
