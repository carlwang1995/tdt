from dbconfig import db
from fastapi.encoders import jsonable_encoder
from datetime import *
import jwt,re

# Token Key
SECRET_KEY = "4aa0178f6632ed4b6754932831f7ed59e3b2d9dc4c397ed14bf039309c47770a"
ALGORITHM = "HS256"

class AttractionModel:
    def get_attraction(page,keyword):
        if page == None:
            page = 0

        result = {
            "nextPage":None,
            "data":[]
        }
        try:
            connection = db.get_connection()
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
                    return result
                elif i == len(myresult):
                    result["nextPage"] = None
                    break
                myresult[i]["images"] = myresult[i]["images"].split(",")
                myresult[i]["lat"] = float(myresult[i]["lat"])
                myresult[i]["lng"] = float(myresult[i]["lng"])
                result["nextPage"] = page+1
                result["data"].append(myresult[i])
            return result
        except:
            return "error"
        finally:
            mycursor.close()
            connection.close()
    def get_attraction_by_ID(id):
        result = {
        "data":{}
    }
        try:
            connection = db.get_connection()
            mycursor = connection.cursor(dictionary=True)
            idlist = []
            mycursor.execute("SELECT `id` FROM `rawdata`;")
            myresult = mycursor.fetchall()
            mycursor.close()
            connection.close()
            for i in range(0,len(myresult)):
                idlist.append(myresult[i]["id"])
            if id not in idlist:
                return "error_id"
            else:
                connection = db.get_connection()
                mycursor = connection.cursor(dictionary=True)
                val = [id]
                sql = "SELECT * FROM `rawdata` WHERE `id` = %s"
                mycursor.execute(sql,val)
                myresult = mycursor.fetchall()
                myresult[0]["images"] = myresult[0]["images"].split(",")
                myresult[0]["lat"] = float(myresult[0]["lat"])
                myresult[0]["lng"] = float(myresult[0]["lng"])
                result["data"]=myresult[0]
                mycursor.close()
                connection.close()
                return result
        except:
            return "error"
    def get_mrts():
        result = {
	        "data":[]
	    }
        try:
            connection = db.get_connection()
            mycursor = connection.cursor(dictionary=True)
            mycursor.execute("SELECT `mrt`,COUNT(`mrt`) AS NUMBER FROM `rawdata` GROUP BY `mrt` HAVING COUNT(`mrt`) > 0 ORDER BY `NUMBER`DESC;")
            myresult = mycursor.fetchall()
            alist = []
            for mrt in myresult:
                alist.append(mrt["mrt"])
            result["data"] = alist
            mycursor.close()
            connection.close()
            return result
        except:
            return "error"

class UserModel:
    def sign_up(info):
        result = {"ok":True}
        try:
            data = jsonable_encoder(info)
            re_pattern = r"[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
            # 檢查是否有未輸入的註冊資訊
            if data["name"] == "" or data["email"] == "" or data["password"] == "":
                return "error_empty_input"
            # 檢查email格式
            elif len(re.findall(re_pattern,data["email"])) == 0:
                return "error_email_input"
            # 檢查是否重複email
            connection = db.get_connection()
            mycursor = connection.cursor(dictionary=True)
            val = [data["email"]]
            sql = "SELECT * FROM `user` WHERE `email` = %s;"
            mycursor.execute(sql,val)
            email_check = mycursor.fetchone()
            connection.close()
            if email_check != None:
                return "error_email_repeat"
            # 進行註冊
            connection = db.get_connection()
            mycursor = connection.cursor(dictionary=True)
            sql = ("INSERT INTO `user`(`name`, `email`, `password`) VALUES(%s,%s,%s);")
            val = (data["name"], data["email"], data["password"])
            mycursor.execute(sql,val)
            connection.commit()
            connection.close()
            return result
        except:
            return "error"
    def sign_in(info):
        result = {"token":""}
        try:
            connection = db.get_connection()
            mycursor = connection.cursor(dictionary=True)
            data = jsonable_encoder(info)
            val = (data["email"],data["password"])
            sql = "SELECT `id`,`name`,`email` FROM `user` WHERE `email` = %s AND `password` = %s;"
            mycursor.execute(sql,val)
            to_encode = mycursor.fetchone()
            connection.close()
            if to_encode == None:
                return "user_error"
            else:
                expire = datetime.now(timezone.utc)+timedelta(days=7)
                to_encode["exp"] = expire
                encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
                result["token"] = encoded_jwt
                return result
        except:
            return "error"
    def user_auth(token):
        result = {"data":{}}
        try:
            decoded_jwt = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
            result["data"]["id"] = decoded_jwt["id"]
            result["data"]["name"] = decoded_jwt["name"]
            result["data"]["email"] = decoded_jwt["email"]
            return result
        except:
            result["data"] = None
            return result

class BookingModel:
    def get_booking(token):
        result = {"data":""}
        try:
            if token == "null":
                return "error_not_login"
            decoded_jwt = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
            user_id = decoded_jwt["id"]
            connection = db.get_connection()
            mycursor = connection.cursor(dictionary=True)
            mycursor.execute(f"SELECT * FROM `booking` WHERE `user_id` = {user_id}")
            myresult = mycursor.fetchone()
            connection.close()
            if myresult != None:
                booking_attraction_id = myresult["attraction_id"]
                booking_date = str(myresult["date"])
                booking_time = myresult["time"]
                booking_price = myresult["price"]
                connection = db.get_connection()
                mycursor = connection.cursor(dictionary=True)
                mycursor.execute(f"SELECT `name`,`address`,`images` FROM `rawdata` WHERE `id` = {booking_attraction_id}")
                myresult = mycursor.fetchone()
                connection.close()
                myresult["images"] = myresult["images"].split(",")[0]
                attraction_dict = {"id":booking_attraction_id,"name":myresult["name"],"address":myresult["address"],"image":myresult["images"]}
                data = {"attraction":attraction_dict,"date":booking_date,"time":booking_time,"price":booking_price}
                result["data"] = data
            else:
                result["data"] = None
            return result
        except:
            return "error"
    def booking_input(token, data):
        result = {"ok":True}
        try:
            if token == "null":
                return "error_not_login"                       
            decode_jwt = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
            user_id = decode_jwt["id"]
            data = jsonable_encoder(data)
            attraction_id = data["id"]
            date = data["date"]
            time = data["time"]
            price = data["price"]
            #檢查Input
            if date == "" or time == "" or price == "":
                return "error_data"
            connection = db.get_connection()
            mycursor = connection.cursor(dictionary=True)
            #檢查是否有既有預定資料，有則更新，沒有則新建
            mycursor.execute(f"SELECT * FROM `booking` WHERE `user_id` = {user_id}")
            myresult = mycursor.fetchone()
            if myresult != None:
                mycursor.execute(f"UPDATE `booking` SET `attraction_id`={attraction_id},`date`='{date}',`time`='{time}', `price`={price} WHERE `user_id`={user_id}")
                connection.commit()
                connection.close()
            else:
                val = (user_id, attraction_id, date, time, price)
                sql = ("INSERT INTO `booking`(`user_id`,`attraction_id`,`date`,`time`,`price`) VALUES(%s,%s,%s,%s,%s);")
                mycursor.execute(sql,val)
                connection.commit()
                connection.close()
            return result
        except:
            return "error"
    def delete_booking(token):
        result = {"ok":True}
        try:
            if token == "null":
                return "error_not_login"   
            decoded_jwt = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
            user_id = decoded_jwt["id"]
            connection = db.get_connection()
            mycursor = connection.cursor()
            mycursor.execute(f"DELETE FROM `booking` WHERE `user_id` = {user_id}")
            connection.commit()
            connection.close()
            return result
        except:
            return "error"