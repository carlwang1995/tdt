from fastapi import *
from fastapi.responses import FileResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated,Dict
from pydantic import BaseModel
from model.attraction import AttractionModel
from model.booking import BookingModel
from model.order import OrderModel
from model.user import UserModel
from view.attraction import AttractionView
from view.booking import BookingView
from view.order import OrderView
from view.user import UserView

app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="useless_fornow_maybe")

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
@app.get("/member", include_in_schema=False)
async def member(request: Request):
	return FileResponse("./static/member.html", media_type="text/html")

# API
# 取得景點資料列表
@app.get("/api/attractions",response_class=JSONResponse)
async def get_attractions(page:Annotated[int,Query(ge=0)]=None,keyword:str=None):
	data = AttractionModel.get_attraction(page,keyword)
	result = AttractionView.get_attraction(data)
	return result
	
# 根據景點編號取得景點資料	
@app.get("/api/attraction/{attractionId}",response_class=JSONResponse)
async def get_attraction_by_ID(attractionId:int):
	data = AttractionModel.get_attraction_by_ID(attractionId)
	result = AttractionView.get_attraction_by_ID(data)
	return result

# 取得捷運站名稱列表
@app.get("/api/mrts",response_class=JSONResponse)
async def get_mrts():
	data = AttractionModel.get_mrts()
	result = AttractionView.get_mrts(data)
	return result

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
	data = UserModel.sign_up(signup_info)
	result = UserView.sign_up(data)
	return result

# 登入會員帳戶
@app.put("/api/user/auth",response_class=JSONResponse)
async def signin(signin_info:UserSignInInput):
	data = UserModel.sign_in(signin_info)
	result = UserView.sign_in(data)
	return result
	
# 取得當前登入的會員資訊
@app.get("/api/user/auth",response_class=JSONResponse)
async def get_user_info(token:Annotated[str,Depends(oauth2_scheme)]):
	data = UserModel.user_auth(token)
	result = UserView.user_auth(data)
	return result

# 取得尚未下單的預定行程
@app.get("/api/booking",response_class=JSONResponse)
async def get_booking(token:Annotated[str,Depends(oauth2_scheme)]):
	data = BookingModel.get_booking(token)
	result = BookingView.get_booking(data)
	return result

# 建立新的預定行程
class BookingInput(BaseModel):
	id : int
	date : str
	time : str
	price : int
@app.post("/api/booking",response_class=JSONResponse)
async def booking_input(token:Annotated[str,Depends(oauth2_scheme)],data:BookingInput):
	data_ = BookingModel.booking_input(token, data)
	result = BookingView.booking_input(data_)
	return result

# 刪除目前的預定行程
@app.delete("/api/booking",response_class=JSONResponse)
async def delete_booking(token:Annotated[str,Depends(oauth2_scheme)]):
	data = BookingModel.delete_booking(token)
	result = BookingView.delete_booking(data)
	return result

# 建立新的訂單，並完成付款程序
class Attraction(BaseModel):
	id:int
	name:str
	address:str
	image:str
class Contact(BaseModel):
	name:str
	email:str
	phone:str
class Order(BaseModel):
	price:int
	trip: Dict[str, Attraction]
	date:str
	time:str
class OrderInput(BaseModel):
	prime:str
	order:Order
	contact:Contact
@app.post("/api/orders", response_class=JSONResponse)
async def send_order(token:Annotated[str,Depends(oauth2_scheme)], order_input:OrderInput):
	data = OrderModel.order_input(token,order_input)
	result = OrderView.order_input(data)
	return result

# 根據訂單編號取得訂單資訊
@app.get("/api/order/{orderNumber}")
async def get_order(token:Annotated[str,Depends(oauth2_scheme)],orderNumber:str):
	data = OrderModel.get_order(token, orderNumber)
	result = OrderView.get_order(data)
	return result

# 根據電子郵件取得所有訂單資訊
@app.get("/api/orders/{email}")
async def get_orders_by_email(token:Annotated[str, Depends(oauth2_scheme)], email:str):
	data = OrderModel.get_orders(token, email)
	result = OrderView.get_orders(data)
	return result

# 編輯會員資料(姓名、電子郵件)
class MemberInfo(BaseModel):
	old_name:str
	old_email:str
	new_name:str
	new_email:str
@app.patch("/api/edit_member")
async def edit_member(token:Annotated[str, Depends(oauth2_scheme)],member_info:MemberInfo):
	data = UserModel.user_edit(token, member_info)
	result = UserView.user_edit(data)
	return result

# 上傳會員照片
@app.post("/api/upload")
async def upload_image(token:Annotated[str, Depends(oauth2_scheme)],file:UploadFile = File(...)):
	data = UserModel.upload_image(token, file)
	result = UserView.upload_image(data)
	return result

# 取得會員上傳照片
@app.get("/api/upload/{email}")
async def get_image(token:Annotated[str, Depends(oauth2_scheme)], email:str):
	data = UserModel.get_image(token, email)
	result = UserView.get_image(data)
	return result