from flask import *
from flask_mysqldb import *
import netifaces as ni

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'Direccion MySQL'
app.config['MYSQL_USER'] = 'User'
app.config['MYSQL_PASSWORD'] = 'Pass'
app.config['MYSQL_DB'] = 'DB'
app.secret_key = 'Key'
mysql = MySQL(app)

@app.route('/')
def main():
    return render_template('/separadas/rick.html')

if __name__ == '__main__':
    ip_page = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['addr']
    app.run(host=ip_page, port=80, debug = True)
