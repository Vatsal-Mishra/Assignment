import requests                                              #importing libraries for retreiving data
from datetimerange import DateTimeRange                      # to define a time range
import datetime                                              # to make datetime objects
import json                                                  #to make json files
from flask import Flask,jsonify, render_template,request
app=Flask(__name__)
@app.route("/")
def register():
    return render_template("form.html")
@app.route("/insert",methods=["POST"])
def insert():
    res=requests.get("https://gitlab.com/-/snippets/2067888/raw/master/sample_json_3.json")   #requesting for data
    data=res.json()
    list_id=[]
    value_data_list=[]
    start_time=request.form.get("starttime")     # taking all the information from the form entered by users
    end_time=request.form.get("endtime")
    start_time=datetime.datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%SZ")
    end_time=datetime.datetime.strptime(end_time,"%Y-%m-%dT%H:%M:%SZ")
    for time in data:
     if time["time"] in DateTimeRange(start_time,end_time):
        list_id.append(time["id"])                                 #storing all the ids in list_id
     sort_list=set(list_id)                                             #making set to get the unique value
     list_id=list(sort_list)                                             #converting set to list
     list_id=sorted(list_id)                                             #sorting that list
     for id in list_id:
       belt1=belt2=count=0                                                         #counter variables
       for time in data:
         if time["time"] in DateTimeRange(start_time,end_time):             #traversing through interval
          if id==time["id"]:
             count+=1
             if time["state"]==True:                                    #checking for required conditions and performing operations
               belt1+=0
               belt2+=time["belt2"]
             else:
               belt1+=time["belt1"]
               belt2=0
       avg_belt1=int(belt1/count)                                             #calculating average values
       avg_belt2=int(belt2/count)
       f_id=int(id[4])                                                        #converting the type of id (String to integer)
       value_json=[                                                           #creating json
         {
       "id":f_id,
       "avg_belt1":avg_belt1,
       "avg_belt2":avg_belt2
         }
         ]
       value_data_list.append(value_json)                                    #storing all jsons in list
    with open("value.json","w") as f:                                         #writing json to file value.json
        json.dump(value_data_list,f,indent=2)
    return jsonify(data=value_data_list[len(value_data_list)-4:len(value_data_list)])
if __name__=="__main__" :
     app.run
