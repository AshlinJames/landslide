from flask import Flask
from public import public
from admin import admin
from authority import authority
from api import api
# from sms_app import sms_app


app=Flask(__name__)

# Set a maximum upload size of 2 GB
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2 GB


app.secret_key="secret_key"

app.register_blueprint(public)
app.register_blueprint(admin,url_prefix="/admin")
app.register_blueprint(authority,url_prefix="/authority")
app.register_blueprint(api,url_prefix="/api")
# app.register_blueprint(sms_app,url_prefix="/sms_app/")

app.run(debug=True,port=5023,host="0.0.0.0")
