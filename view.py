from fastapi.responses import JSONResponse
class AttractionView:
    def get_attraction(data):
        error_mes = {"error":True,"message":""}
        if data == "error":
            error_mes["message"] = "後台發生錯誤"
            return JSONResponse(status_code=500,content=error_mes)
        else:
            return JSONResponse(status_code=200,content=data)      
    def get_attraction_by_ID(data):
        error_mes = {"error":True,"message":""}
        if data == "error_id":
            error_mes["message"] = "景點編號不正確"
            return JSONResponse(status_code=400,content=error_mes)
        elif data == "error":
            error_mes["message"] = "後台發生錯誤"
            return JSONResponse(status_code=500,content=error_mes)
        else:
            return JSONResponse(status_code=200,content=data)  
    def get_mrts(data):
        error_mes = {"error":True,"message":""}
        if data == "error":
            error_mes["message"] = "後台發生錯誤"
            return JSONResponse(status_code=500,content=error_mes)
        else:
            return JSONResponse(status_code=200,content=data)
        
class UserView:
    def sign_up(data):
        error_mes = {"error":True,"message":""}
        if data == "error_empty_input":
            error_mes["message"] = "請輸入註冊姓名、電子郵件以及密碼。"
            return JSONResponse(status_code=400, content=error_mes)
        elif data == "error_email_input":
            error_mes["message"] = "請輸入正確的電子郵件格式。"
            return JSONResponse(status_code=400, content=error_mes)
        elif data == "error_email_repeat":
            error_mes["message"] = "此電子郵件已重複。"
            return JSONResponse(status_code=400, content=error_mes)
        elif data == "error":
            error_mes["message"] = "後台發生錯誤"
            return JSONResponse(status_code=500, content=error_mes)
        else:
            return JSONResponse(status_code=200, content=data)
    def sign_in(data):
        error_mes = {"error":True,"message":""}
        if data == "user_error":
            error_mes["message"] = "登入失敗，帳號或密碼有誤"
            return JSONResponse(status_code=400, content=error_mes)
        elif data == "error":
            error_mes["message"] = "後台發生錯誤"
            return JSONResponse(status_code=500, content=error_mes)
        else:
            return JSONResponse(status_code=200, content= data)
    def user_auth(data):
        return JSONResponse(status_code=200, content=data)
    
class BookingView:
    def get_booking(data):
        error_mes = {"error":True,"message":""}
        if data == "error_not_login":
            error_mes["message"] = "未登入系統，拒絕存取"
            return JSONResponse(status_code=403,content=error_mes)
        elif data == "error":
            error_mes["message"] = "後台發生錯誤"
            return JSONResponse(status_code=500,content=error_mes)
        else:
            return JSONResponse(status_code=200, content=data)
    def booking_input(data):
        error_mes = {"error":True,"message":""}
        if data == "error_not_login":
            error_mes["message"] = "未登入系統，拒絕存取"
            return JSONResponse(status_code=403,content=error_mes)
        elif data == "error_data":
            error_mes["message"] = "資料有缺漏"
            return JSONResponse(status_code=400,content=error_mes)
        elif data == "error":
            error_mes["message"] = "後台發生錯誤"
            return JSONResponse(status_code=500,content=error_mes)
        else:
            return JSONResponse(status_code=200, content=data)
    def delete_booking(data):
        error_mes = {"error":True,"message":""}
        if data == "error_not_login":
            error_mes["message"] = "未登入系統，拒絕存取"
            return JSONResponse(status_code=403,content=error_mes)
        elif data == "error":
            error_mes["message"] = "後台發生錯誤"
            return JSONResponse(status_code=500,content=error_mes)
        else:
            return JSONResponse(status_code=200, content=data)

class OrderView:
    def order_input(data):
        error_mes = {"error":True,"message":""}
        if data == "error_not_login":
            error_mes["message"] = "未登入系統，拒絕存取"
            return JSONResponse(status_code=403,content=error_mes)
        elif data == "error_data":
            error_mes["message"] = "訂單建立失敗，請檢查資料是否正確"
            return JSONResponse(status_code=400,content=error_mes)
        elif data == "error":
            error_mes["message"] = "後台發生錯誤"
            return JSONResponse(status_code=500,content=error_mes)  
        else: 
            return JSONResponse(status_code=200,content=data)
    def get_order(data):
        error_mes = {"error":True,"message":""}
        if data == "error_not_login":
            error_mes["message"] = "未登入系統，拒絕存取"
            return JSONResponse(status_code=403,content=error_mes)
        elif data == "error":
            error_mes["message"] = "後台發生錯誤"
            return JSONResponse(status_code=500,content=error_mes)   
        else:
            return JSONResponse(status_code=200,content=data)