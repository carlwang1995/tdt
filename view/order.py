from fastapi.responses import JSONResponse

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
    def get_orders(data):
        error_mes = {"error":True,"message":""}
        if data == "error_not_login":
            error_mes["message"] = "未登入系統，拒絕存取"
            return JSONResponse(status_code=403,content=error_mes)
        elif data == "error":
            error_mes["message"] = "後台發生錯誤"
            return JSONResponse(status_code=500,content=error_mes)   
        else:
            return JSONResponse(status_code=200,content=data)