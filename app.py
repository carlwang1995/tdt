from fastapi import *
from fastapi.responses import FileResponse,JSONResponse
from typing import Annotated
from fastapi.staticfiles import StaticFiles
import mysql.connector
app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

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
		"nextPage":None,
		"data":[]
	}
	error_res = {
		"error": False,
		"message": ""
	}
	try:
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
				result["nextPage"] = None
				break
			myresult[i]["images"] = myresult[i]["images"].split(",")
			myresult[i]["lat"] = float(myresult[i]["lat"])
			myresult[i]["lng"] = float(myresult[i]["lng"])
			result["nextPage"] = page+1
			result["data"].append(myresult[i])
		
		mycursor.close()
		return JSONResponse(result)
	except:
		error_res["error"] = True
		error_res["message"] = "後台發生錯誤"
		return JSONResponse(status_code=500,content=error_res)
	
@app.get("/api/attraction/{attractionId}",response_class=JSONResponse)
async def get_attraction_by_ID(attractionId:int):
	result = {
		"data":{}
	}
	error_res = {
		"error": False,
		"message": ""
	}
	try:
		idlist = []
		mycursor = mydb.cursor(dictionary=True)
		mycursor.execute("SELECT `id` FROM `rawdata`;")
		myresult = mycursor.fetchall()
		for i in range(0,len(myresult)):
			idlist.append(myresult[i]["id"])
		mycursor.close()

		if attractionId not in idlist:
			error_res["error"] = True
			error_res["message"] = "景點編號不正確"
			return JSONResponse(status_code=400,content=error_res)
		else:
			mycursor = mydb.cursor(dictionary=True)
			val = [attractionId]
			sql = "SELECT * FROM `rawdata` WHERE `id` = %s"
			mycursor.execute(sql,val)
			myresult = mycursor.fetchall()
			myresult[0]["images"] = myresult[0]["images"].split(",")
			myresult[0]["lat"] = float(myresult[0]["lat"])
			myresult[0]["lng"] = float(myresult[0]["lng"])
			result["data"]=myresult[0]
			
			mycursor.close()
			return JSONResponse(result)
	except:
		error_res["error"] = True
		error_res["message"] = "後台發生錯誤"
		return JSONResponse(status_code=500,content=error_res)

@app.get("/api/mrts",response_class=JSONResponse)
async def get_mrts():
	result = {
	    "data":[]
	}
	error_res = {
		"error": False,
		"message": ""
	}
	try:
		mycursor = mydb.cursor(dictionary=True)
		mycursor.execute("SELECT `mrt`,COUNT(`mrt`) AS NUMBER FROM `rawdata` GROUP BY `mrt` HAVING COUNT(`mrt`) > 0 ORDER BY `NUMBER`DESC;")
		myresult = mycursor.fetchall()
		alist = []
		for mrt in myresult:
			alist.append(mrt["mrt"])
		result["data"] = alist
		mycursor.close()
		return JSONResponse(result)
	except:
		error_res["error"] = True
		error_res["message"] = "後台發生錯誤"
		return JSONResponse(status_code=500,content=error_res)