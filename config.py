from app import app
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth

app.config['BASIC_AUTH_USERNAME'] = 'ale'
app.config['BASIC_AUTH_PASSWORD'] = '25683394@Gu'

auth = BasicAuth(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '25683394@Gu'
app.config['MYSQL_DATABASE_DB'] = 'cadastro' 
app.config['MYSQL_DATABASE_DB'] = 'produtos'
app.config['MYSQL_DATABASE_DB'] = 'vendas'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

