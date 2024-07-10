from fastapi.responses import JSONResponse

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