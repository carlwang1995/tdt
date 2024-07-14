from dbconfig import db
from fastapi.encoders import jsonable_encoder
from datetime import *
import requests,random,os
from dotenv import load_dotenv

load_dotenv()

class OrderModel:
    def order_input(token, input_data):
        result = {"data":""}
        partner_key = os.environ.get("partner_key")
        merchant_id = os.environ.get("merchant_id")
        try:
            if token == "null":
                return "error_not_login"
            data = jsonable_encoder(input_data)
            prime = data["prime"]
            # 首次創建訂單，存入訂單資料庫
            number = datetime.now().strftime("%Y%m%d%H%M%S%f") + "-" + str(random.randrange(0,99))
            order_price = data["order"]["price"]
            order_date = data["order"]["date"]
            order_time = data["order"]["time"]
            trip_attraction_id = data["order"]["trip"]["attraction"]["id"]
            trip_attraction_name = data["order"]["trip"]["attraction"]["name"]
            trip_attraction_address = data["order"]["trip"]["attraction"]["address"]
            trip_attraction_image = data["order"]["trip"]["attraction"]["image"]
            contact_name = data["contact"]["name"]
            contact_email = data["contact"]["email"]
            contact_phone = data["contact"]["phone"]
            try:
                connection = db.get_connection()
                mycursor = connection.cursor(dictionary=True)
                val = (number, order_price, order_date, order_time, trip_attraction_id, trip_attraction_name, trip_attraction_address, trip_attraction_image,contact_name ,contact_email, contact_phone)
                sql = ("INSERT INTO `order`(`number`, `order_price`, `order_date`, `order_time`, `attraction_id`, `attraction_name`, `attraction_address`, `attraction_image`, `contact_name` ,`contact_email`, `contact_phone`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);")
                mycursor.execute(sql,val)
                connection.commit()
                connection.close()
            except:
                return "error_data"
            # 取得prime後，向tappay api發送資料，取得付款狀態
            pay_data = {
                "prime":prime,
                "partner_key": partner_key,
                "merchant_id":merchant_id,
                "order_number":number,
                "details":"TapPay Test",
                "amount":order_price,
                "cardholder":{"phone_number": contact_phone, "name": contact_name, "email": contact_email}
            }
            url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
            headers = {"Content-Type": "application/json","x-api-key": partner_key}
            response = requests.post(url, json=pay_data, headers=headers)
            pay_result = response.json()

            # 記錄付款(payment)結果(不論成功失敗)
            connection = db.get_connection()
            mycursor = connection.cursor()
            val = (number, pay_result["status"], pay_result["msg"])
            sql = ("INSERT INTO `payment`(`number`,`status`,`message`) VALUES(%s,%s,%s);")
            mycursor.execute(sql,val)
            connection.commit()
            connection.close()

            message = ""
            status = 1
            # 如果付款成功，更新訂單表單的付款狀態(status)
            if pay_result["status"] == 0 and pay_result["msg"] == "Success":
                message = "付款成功"
                status = 0
                connection = db.get_connection()
                mycursor = connection.cursor()
                mycursor.execute(f"UPDATE `order` SET `status` = 0 WHERE `number` = '{pay_result["order_number"]}';")
                connection.commit()
                connection.close()
            else:
                message = "付款失敗"

            # 回傳訂購結果到前端
            result["data"] = {"number":number,"payment":{"status":status,"message":message}}
            return result
        except:
            return "error"
    def get_order(token,orderNumber):
        result ={"data":{
            "number":"",
            "price":0,
            "trip":{
                "attraction":{
                    "id":0,
                    "name":"",
                    "address":"",
                    "image":""
                },
                "date":"",
                "time":""
            },
            "contact":{
                "name":"",
                "email":"",
                "phone":""
            },
            "status":2
        }}
        try:
            if token == "null":
                return "error_not_login"
            connection =db.get_connection()
            mycursor = connection.cursor(dictionary=True)
            mycursor.execute(f"SELECT * FROM `order` WHERE `number` = '{orderNumber}'")
            myresult = mycursor.fetchone()
            connection.close()
            result["data"]["number"] = myresult["number"]
            result["data"]["price"] = myresult["order_price"]
            result["data"]["trip"]["attraction"]["id"] = myresult["attraction_id"]
            result["data"]["trip"]["attraction"]["name"] = myresult["attraction_name"]
            result["data"]["trip"]["attraction"]["address"] = myresult["attraction_address"]
            result["data"]["trip"]["attraction"]["image"] = myresult["attraction_image"]
            result["data"]["trip"]["date"] = str(myresult["order_date"])
            result["data"]["trip"]["time"] = myresult["order_time"]
            result["data"]["contact"]["name"] = myresult["contact_name"]
            result["data"]["contact"]["email"] = myresult["contact_email"]
            result["data"]["contact"]["phone"] = myresult["contact_phone"]
            result["data"]["status"] = myresult["status"]
            return result
        except:
            return "error"
    def get_orders(token, email):
        result = {"data":None}
        try:
            if token == "null":
                return "error_not_login"
            connection = db.get_connection()
            mycursor = connection.cursor(dictionary=True)
            mycursor.execute(f"SELECT `number`,`order_price`,`status` FROM `order` WHERE `contact_email` = '{email}';")
            myresult = mycursor.fetchall()
            result["data"] = myresult
            return result
        except:
            return "error"
        finally:
            connection.close()