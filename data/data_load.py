import mysql.connector
import json
import re

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "11111111",
    database = "tdt"
)
mycursor = mydb.cursor()

with open("taipei-attractions.json", mode="r",encoding="utf-8") as file:
    data = json.load(file)

attractionList = data["result"]["results"]

pattern = r"https://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\.(?:jpg|JPG|png|PNG)"

for i in range(0,len(attractionList)):
    attractionList[i]['file'] = re.findall(pattern, attractionList[i]['file'])
    attractionfile = ""
    for j in range(0,len(attractionList[i]['file'])):
        if j < len(attractionList[i]['file'])-1:
            attractionfile += attractionList[i]['file'][j] + ","
        else:
            attractionfile += attractionList[i]['file'][j]

    val = (attractionList[i]['name'],
           attractionList[i]['CAT'],
           attractionList[i]['description'],
           attractionList[i]['address'],
           attractionList[i]['direction'],
           attractionList[i]['MRT'],
           attractionList[i]['latitude'],
           attractionList[i]['longitude'],
           attractionfile
           )
    sql =("INSERT INTO `rawdata`(`name`,`category`,`description`,`address`,`transport`,`mrt`,`lat`,`lng`,`images`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s);")
    mycursor.execute(sql,val)
    mydb.commit()