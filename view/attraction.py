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