import mysql.connector

config = {
	"host":"localhost",
    "user":"root",
    "password":"11111111",
    "database":"tdt"
}
db = mysql.connector.pooling.MySQLConnectionPool(
	pool_name = "mypool",
	pool_size = 5,
	**config
)