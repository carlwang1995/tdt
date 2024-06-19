from fastapi import *
from fastapi.responses import FileResponse,JSONResponse
from typing import Annotated
from fastapi.staticfiles import StaticFiles
import mysql.connector
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from datetime import *
import jwt
import re
from fastapi.security import OAuth2PasswordBearer

app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Token Key
SECRET_KEY = "4aa0178f6632ed4b6754932831f7ed59e3b2d9dc4c397ed14bf039309c47770a"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="useless_fornow_maybe")

dbconfig = {
	"host":"localhost",
    "user":"root",
    "password":"11111111",
    "database":"tdt"
}
pool = mysql.connector.pooling.MySQLConnectionPool(
	pool_name = "mypool",
	pool_size = 5,
	**dbconfig
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
		connection = pool.get_connection()
		mycursor = connection.cursor(dictionary=True)
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
		connection.close()
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
		connection = pool.get_connection()
		mycursor = connection.cursor(dictionary=True)
		idlist = []
		mycursor.execute("SELECT `id` FROM `rawdata`;")
		myresult = mycursor.fetchall()
		mycursor.close()
		connection.close()
		for i in range(0,len(myresult)):
			idlist.append(myresult[i]["id"])
		if attractionId not in idlist:
			error_res["error"] = True
			error_res["message"] = "景點編號不正確"
			return JSONResponse(status_code=400,content=error_res)
		else:
			connection = pool.get_connection()
			mycursor = connection.cursor(dictionary=True)
			val = [attractionId]
			sql = "SELECT * FROM `rawdata` WHERE `id` = %s"
			mycursor.execute(sql,val)
			myresult = mycursor.fetchall()
			myresult[0]["images"] = myresult[0]["images"].split(",")
			myresult[0]["lat"] = float(myresult[0]["lat"])
			myresult[0]["lng"] = float(myresult[0]["lng"])
			result["data"]=myresult[0]
			mycursor.close()
			connection.close()
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
		connection = pool.get_connection()
		mycursor = connection.cursor(dictionary=True)
		mycursor.execute("SELECT `mrt`,COUNT(`mrt`) AS NUMBER FROM `rawdata` GROUP BY `mrt` HAVING COUNT(`mrt`) > 0 ORDER BY `NUMBER`DESC;")
		myresult = mycursor.fetchall()
		alist = []
		for mrt in myresult:
			alist.append(mrt["mrt"])
		result["data"] = alist
		mycursor.close()
		connection.close()
		return JSONResponse(result)
	except:
		error_res["error"] = True
		error_res["message"] = "後台發生錯誤"
		return JSONResponse(status_code=500,content=error_res)

class UserSignUpInput(BaseModel):
	name: str
	email: str
	password: str
class UserSignInInput(BaseModel):
	email: str
	password: str

# 註冊一個新的會員
@app.post("/api/user",response_class=JSONResponse)
async def signup(signup_info:UserSignUpInput):
	try:
		data = jsonable_encoder(signup_info)
		good_res = {"ok":True}
		error_res = {"error":True,"message":""}
		re_pattern = r"[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
		# 檢查是否有未輸入的註冊資訊
		if data["name"] == "" or data["email"] == "" or data["password"] == "":
			error_res["message"] = "請輸入註冊姓名、電子郵件以及密碼。"
			return JSONResponse(status_code=400,content=error_res)
		# 檢查email格式
		elif len(re.findall(re_pattern,data["email"])) == 0:
			error_res["message"] = "請輸入正確的電子郵件格式。"
			return JSONResponse(status_code=400,content=error_res)
		# 檢查是否重複email
		connection = pool.get_connection()
		mycursor = connection.cursor(dictionary=True)
		val = [data["email"]]
		sql = "SELECT * FROM `user` WHERE `email` = %s;"
		mycursor.execute(sql,val)
		email_check = mycursor.fetchone()
		connection.close()
		if email_check != None:
			print(email_check)
			error_res["message"] = "此電子郵件已重複。"
			return JSONResponse(status_code=400,content=error_res)
		# 進行註冊
		connection = pool.get_connection()
		mycursor = connection.cursor(dictionary=True)
		sql = ("INSERT INTO `user`(`name`, `email`, `password`) VALUES(%s,%s,%s);")
		val = (data["name"], data["email"], data["password"])
		mycursor.execute(sql,val)
		connection.commit()
		connection.close()
		return JSONResponse(status_code=200,content=good_res)
	except:
		error_res["message"] = "後台發生錯誤"
		return JSONResponse(status_code=500,content=error_res)

# 登入會員帳戶
@app.put("/api/user/auth",response_class=JSONResponse)
async def signin(signin_info:UserSignInInput):
	token_res = {"token":""}
	bad_res = {"error":True,"message":""}
	try:
		connection = pool.get_connection()
		mycursor = connection.cursor(dictionary=True)
		data = jsonable_encoder(signin_info)
		val = (data["email"],data["password"])
		sql = "SELECT `id`,`name`,`email` FROM `user` WHERE `email` = %s AND `password` = %s;"
		mycursor.execute(sql,val)
		to_encode = mycursor.fetchone()
		connection.close()
		if to_encode == None:
			bad_res["message"] = "登入失敗，帳號或密碼有誤"
			return JSONResponse(status_code=400,content=bad_res)
		else:
			expire = datetime.now(timezone.utc)+timedelta(days=7)
			to_encode["exp"] = expire
			encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
			token_res["token"] = encoded_jwt
			return JSONResponse(status_code=200,content=token_res)
	except:
		bad_res["message"] = "後台發生錯誤"
		return JSONResponse(status_code=500,content=error_res)
	
# 取得當前登入的會員資訊
@app.get("/api/user/auth",response_class=JSONResponse)
async def get_user_info(token:Annotated[str,Depends(oauth2_scheme)]):
	result = {"data":{}}
	try:
		decoded_jwt = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
		result["data"]["id"] = decoded_jwt["id"]
		result["data"]["name"] = decoded_jwt["name"]
		result["data"]["email"] = decoded_jwt["email"]
		return JSONResponse(status_code=200,content=result)
	except:
		result["data"] = None
		return JSONResponse(status_code=200,content=result)
