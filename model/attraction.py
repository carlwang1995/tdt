from dbconfig import db

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