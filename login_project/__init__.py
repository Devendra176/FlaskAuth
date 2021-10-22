from flask import Flask
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
# from flask_social import Social


# import MySQLdb.cursors
import re

mysql = MySQL()
oauth = OAuth()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.config['SECRET_KEY'] = '97260ed3d63beccb783bd896'
        app.config['UPLOAD_FOLDER'] = 'login_project/static/Video_converter/videos'
        app.config['DOWNLOAD_FOLDER'] = 'login_project/static/Video_converter/audios'
        app.config['WIFI_FOLDER'] = 'login_project/static/wifi_qr'
        app.config['EXTRACT_FOLDER_RAW'] = 'login_project/static/ExtractText/RawImages'
        app.config['EXTRACT_FOLDER_OUTPUT'] = 'login_project/static/ExtractText/OutImages'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/flasklogin'
        app.config['SQLALCHEMY_POOL_SIZE'] = 20
        app.config['SQLALCHEMY_MAX_OVERFLOW'] = 100
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # app.config['SOCIAL_GOOGLE'] = {
        #                                 'consumer_key': '978588645771-af3sl4u1n2cpmrg74gora4bjrid2180p.apps.googleusercontent.com',
        #                                 'consumer_secret': 'UDm4N3NPyQc6ipH25ZCmxoy1'
        #                                 }
        # Enter your database connection details below
        # app.config['MYSQL_HOST'] = 'localhost'
        # app.config['MYSQL_USER'] = 'root'
        # app.config['MYSQL_PASSWORD'] = 'root'
        # app.config['MYSQL_DB'] = 'flasklogin'
        # Intialize MySQL
        db = SQLAlchemy(app)
        db.init_app(app)
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.login_message = "User needs to be logged in to view this page"
        login_manager.login_message_category = "warning"
        login_manager.init_app(app)
        # mysql = MySQL(app)
        # mysql.init_app(app)
        # conn = mysql.connect
        # crsr = conn.cursor()
        oauth.register(
                name = 'google',
                client_id = '978588645771-af3sl4u1n2cpmrg74gora4bjrid2180p.apps.googleusercontent.com',
                client_secret = 'UDm4N3NPyQc6ipH25ZCmxoy1',
                access_token_url= 'https://accounts.google.com/o/oauth2/token',
                access_token_params=None,
                authorize_url ='https://accounts.google.com/o/oauth2/auth',
                authorize_params=None,
                api_base_url = 'https://www.googleapis.com/oauth2/v1/',
                server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
                client_kwargs={'scope': 'openid profile email'}
                        )
        oauth.init_app(app)
        
        from .auth_google import auth_google as auth_google_blueprint
        app.register_blueprint(auth_google_blueprint)

        # blueprint for auth routes in our app
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        # blueprint for non-auth parts of app
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)



        from .models import User
        @login_manager.user_loader
        def load_user(user_id):
            # since the user_id is just the primary key of our user table, use it in the query for the user
            return User.query.get(int(user_id))
        
        return app

