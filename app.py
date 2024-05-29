from fastapi import *
from fastapi.responses import FileResponse,JSONResponse
from typing import Annotated
import mysql.connector
app=FastAPI()

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "11111111",
    database = "tdt"
)

# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")

# API
@app.get("/api/attractions",response_class=JSONResponse)
async def get_attractions(request:Request,page:Annotated[int,Query(ge=0)]=None,keyword:str=None):
	if page == None:
		page = 0

	result = {
		"nextpage":None,
		"data":[]
	}
	mycursor = mydb.cursor(dictionary=True)
	if keyword != None:
		val = f"WHERE `name` LIKE '%{keyword}%' OR `mrt` = '{keyword}';"
		sql = "SELECT * FROM `rawdata` " + val
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
	else:
		mycursor.execute("SELECT * FROM `rawdata`")
		myresult = mycursor.fetchall()
	
	for i in range(page*12,page*12+12):
		if page * 12 > len(myresult):
			return JSONResponse(result)
		elif i == len(myresult):
			result["nextpage"] = None
			break
		myresult[i]["images"] = myresult[i]["images"].split(",")
		myresult[i]["lat"] = float(myresult[i]["lat"])
		myresult[i]["lng"] = float(myresult[i]["lng"])
		result["nextpage"] = page+1
		result["data"].append(myresult[i])
	
	mycursor.close()
	return JSONResponse(result)
	
@app.get("/api/attraction/{attractionId}",response_class=JSONResponse)
async def get_attraction_by_ID(attractionId:int):
	result = {
		"data":{}
	}
	mycursor = mydb.cursor(dictionary=True)
	val = [attractionId]
	sql = "SELECT * FROM `rawdata` WHERE `id` = %s"
	mycursor.execute(sql,val)
	myresult = mycursor.fetchall()
	myresult[0]["images"] = myresult[0]["images"].split(",")
	result["data"]=myresult[0]
	
	mycursor.close()
	return JSONResponse(result)

@app.get("/api/mrts",response_class=JSONResponse)
async def get_mrts():
	mycursor = mydb.cursor(dictionary=True)
	mycursor.execute("SELECT `mrt` FROM `rawdata`")
	myresult = mycursor.fetchall()

	result = {
	    "data":[]
	}
	alist = []
	for i in range(0,len(myresult)):
		if myresult[i]["mrt"] != None:
			alist.append(myresult[i]["mrt"])
	adict = {}
	for i in range(0,len(alist)):
		count = 0
		for j in range(0,len(alist)):
			if alist[i] == alist[j]:
				count += 1
		adict[alist[i]] = count
	sorted_keys = sorted(adict, key=adict.get, reverse=True)
	result["data"] = sorted_keys
	
	mycursor.close()
	return JSONResponse(result)