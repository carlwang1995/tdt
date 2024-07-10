from dbconfig import db
from fastapi.encoders import jsonable_encoder
import jwt,os
from dotenv import load_dotenv

load_dotenv()

# Token Key
SECRET_KEY = os.environ.get("secret_key")
ALGORITHM = os.environ.get("algorithm")

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