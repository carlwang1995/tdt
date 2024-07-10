from fastapi.responses import JSONResponse

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