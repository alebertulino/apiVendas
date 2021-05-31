from app import app
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth

app.config['BASIC_AUTH_USERNAME'] = 'ale'
app.config['BASIC_AUTH_PASSWORD'] = '25683394@Gu'

auth = BasicAuth(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'alesil'
app.config['MYSQL_DATABASE_PASSWORD'] = 'alesil2021'
app.config['MYSQL_DATABASE_DB'] = 'vendas' 
app.config['MYSQL_DATABASE_HOST'] = 'db-alesil.cxycaymkd24m.us-east-1.rds.amazonaws.com'
mysql.init_app(app)

