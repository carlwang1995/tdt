import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
host = os.environ.get("host")
user = os.environ.get("user")
password = os.environ.get("password")

config = {
	"host":host,
    "user":user,
    "password":password,
    "database":"tdt"
}
db = mysql.connector.pooling.MySQLConnectionPool(
	pool_name = "mypool",
	pool_size = 5,
	**config
)