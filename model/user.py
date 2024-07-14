from dbconfig import db
from fastapi.encoders import jsonable_encoder
from datetime import *
import jwt,re,os,shutil
from dotenv import load_dotenv

load_dotenv()

# Token Key
SECRET_KEY = os.environ.get("secret_key")
ALGORITHM = os.environ.get("algorithm")

re_pattern = r"[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"

class UserModel:
    def sign_up(info):
        result = {"ok":True}
        try:
            data = jsonable_encoder(info)
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
    
    def user_edit(token, info):
        try:
            if token == "null":
                return "error_not_login"
            data = jsonable_encoder(info)
            old_name = data["old_name"]
            new_name = data["new_name"]
            old_email = data["old_email"]
            new_email = data["new_email"]

            if new_name == "" or new_email == "":
                return "error_no_data"
            elif len(re.findall(re_pattern,new_email)) == 0:
                return "error_email_input"
            
            def check_repeat_email():
                connection = db.get_connection()
                mycursor = connection.cursor(dictionary=True)
                sql = f"SELECT * FROM `user` WHERE `email` = '{new_email}';"
                mycursor.execute(sql)
                email_check = mycursor.fetchone()
                connection.close() 
                return email_check
            
            if new_name == old_name and new_email != old_email:
                if check_repeat_email() != None:
                    return "error_email_repeat" 
                connection = db.get_connection()
                mycursor = connection.cursor()
                mycursor.execute(f"UPDATE `user` SET `email` = '{new_email}' WHERE `name` = '{old_name}' AND `email` = '{old_email}';")            
                connection.commit()
                connection.close()
            elif new_name != old_name and new_email == old_email:
                connection = db.get_connection()
                mycursor = connection.cursor()
                mycursor.execute(f"UPDATE `user` SET `name` = '{new_name}' WHERE `name` = '{old_name}' AND `email` = '{old_email}';")
                connection.commit()
                mycursor = connection.cursor()
                mycursor.execute(f"UPDATE `order` SET `contact_name` = '{new_name}' WHERE `contact_name` = '{old_name}' AND `contact_email` = '{old_email}';")
                connection.commit()
                connection.close()
            elif new_name != old_name and new_email != old_email:
                if check_repeat_email() != None:
                    return "error_email_repeat" 
                connection = db.get_connection()
                mycursor = connection.cursor()
                mycursor.execute(f"UPDATE `user` SET `email` = '{new_email}' WHERE `name` = '{old_name}' AND `email` = '{old_email}';")            
                connection.commit()
                mycursor = connection.cursor()
                mycursor.execute(f"UPDATE `user` SET `name` = '{new_name}' WHERE `name` = '{old_name}' AND `email` = '{new_email}';")
                connection.commit()
                mycursor = connection.cursor()
                mycursor.execute(f"UPDATE `order` SET `contact_name` = '{new_name}' WHERE `contact_name` = '{old_name}' AND `contact_email` = '{new_email}';")
                connection.commit()
                connection.close()
            result = {"ok":True}
            return result
        except:
            return "error"
    def upload_image(token,file):
        result = {"ok":True}
        try:
            if token == "null":
                return "error_not_login"
            decoded_jwt = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
            email = decoded_jwt["email"]
            # 檢查是否有既有圖片，如果有就刪除
            connection = db.get_connection()
            mycursor = connection.cursor(dictionary=True)
            mycursor.execute(f"SELECT * FROM `user` WHERE `email` = '{email}'")
            myresult = mycursor.fetchone()
            connection.close()
            if myresult["imgurl"] != None:
                path = myresult["imgurl"]
                os.remove(path)
            # 上傳圖片，路徑存至資料庫，圖片檔名加上使用者ID以獨立識別
            user_id = myresult["id"]
            save_path = os.path.join("static/images/uploads/", str(user_id) + "-" + file.filename)
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            connection = db.get_connection()
            mycursor = connection.cursor()
            mycursor.execute(f"UPDATE `user` SET `imgurl` = '{save_path}' WHERE `email` = '{email}';")
            connection.commit()
            connection.close()
            return result
        except:
            return "error"
    def get_image(token, email):
        result = {"data":None}
        try:
            if token == "null":
                return "error_not_login"
            connection = db.get_connection()
            mycursor = connection.cursor(dictionary=True)
            mycursor.execute(f"SELECT `imgurl` FROM `user` WHERE `email` = '{email}';")
            myresult = mycursor.fetchone()
            result["data"] = myresult["imgurl"]
            return result
        except:
            return "error"
        finally:
            connection.close()