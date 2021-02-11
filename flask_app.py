import requests                                              #importing libraries for retreiving data
from datetimerange import DateTimeRange                      # to define a time range
import datetime                                              # to make datetime objects
import json                                                     #to make json files
from flask import Flask,jsonify, render_template,request
app=Flask(__name__)
@app.route("/")
def register():
    return render_template("form.html")
@app.route("/insert",methods=["POST"])
def insert():
     res=requests.get("https://gitlab.com/-/snippets/2067888/raw/master/sample_json_1.json")   #requesting for data
     data=res.json()
     if res.status_code !=200:
        print("WARNING:There was some error retreiving data ")
     start_time=request.form.get("starttime")     # taking all the information from the form entered by users
     end_time=request.form.get("endtime")
     start_time=datetime.datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%SZ")
     end_time=datetime.datetime.strptime(end_time,"%Y-%m-%dT%H:%M:%SZ")
     Count_A1=Count_B1=Count_A2=Count_B2=Count_A3=Count_B3=0
     for time in data:
        if time["time"] in DateTimeRange(start_time,end_time):                           #traversing in interval
            f_time=datetime.datetime.strptime(time["time"],"%Y-%m-%d %H:%M:%S")           #formatting the time
            if f_time.hour<8 or (f_time.hour==8 and f_time.minute<=30):               #checking for shift_A
                if time["production_A"]==True:
                    Count_A1+=1
                if time["production_B"]==True:
                    Count_B1+=1
            elif f_time.hour<14 or (f_time.hour==14 and f_time.minute<=30):           #checking for shift_B
                if time["production_A"]==True:
                    Count_A2+=1
                if time["production_B"]==True:
                    Count_B2+=1
            else:
                if time["production_A"]==True:                                         #else it will shift_C
                    Count_A3+=1
                if time["production_B"]==True:
                    Count_B3+=1
     shift_data=[{                                                                            #making json
      "shift_A":
          {
             "Production_A_count":Count_A1,
             "Production_B_count":Count_B1,
           },
       "shift_B":
           {
             "Production_A_count":Count_A2,
             "Production_B_count":Count_B2,
           },
       "shift_C":
          {
             "Production_A_count":Count_A3,
             "Production_B_count":Count_B3,
          }
          }
    ]
     return jsonify(data=shift_data)

if __name__=="__main__" :
     app.run
