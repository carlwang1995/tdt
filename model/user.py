from dbconfig import db
from fastapi.encoders import jsonable_encoder
from datetime import *
import jwt,re,os
from dotenv import load_dotenv

load_dotenv()

# Token Key
SECRET_KEY = os.environ.get("secret_key")
ALGORITHM = os.environ.get("algorithm")

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