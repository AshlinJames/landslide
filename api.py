from flask import *
from database import *
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import datetime

api=Blueprint('api', __name__)


@api.route('/login', methods=['POST'])
def login():
	data = {}

	username = request.form['username']
	password = request.form['password']  # Make sure to hash this before storing in DB

	q = """SELECT * FROM `login` INNER JOIN user USING(login_id)
			WHERE username='%s' AND password='%s'""" % (username, password)
	res = select(q)

	if res:
		data['status'] = "success"
	
		data['data'] = res
	
	else:
		data['status'] = "failed"

	return str(data)


@api.route('/userregister', methods=['POST','GET'])
def userregister():
    data = {}

    fname = request.form['fname']
    lname = request.form['lname']
    place = request.form['place']
    phone = request.form['phone']
    email = request.form['email']
    uname = request.form['uname']
    passw = request.form['passw']
    district = request.form['district']

    # ✅ **Hash the password for security**
    # hashed_pass = hashlib.sha256(passw.encode()).hexdigest()

    # ✅ **Check if username already exists**
    q = "SELECT * FROM login WHERE username='%s'" % (uname)
    res = select(q)

    if res:
        data['status'] = "exist"
    else:
        # ✅ **Insert into login table**
        q = "INSERT INTO login (username, password, usertype) VALUES ('%s', '%s', 'user')" % (uname, passw)
        login_id = insert(q)

        # ✅ **Insert into patient table**
        q = """INSERT INTO user (login_id, fname, lname, place, phone, email, district) 
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (login_id, fname, lname, place, phone, email, district)
        insert(q)

        data['status'] = "success"

    return str(data)


@api.route('/get_reports', methods=['GET'])
def get_reports():
    q="""SELECT predict_landslide_id, authority_id, location_name, latitude, longitude, 
               temperature, humidity, precipitation, dew_point, wind_speed, elevation, 
               soil_moisture, date_time, result 
        FROM predict_landslide where result!='Low'
        ORDER BY date_time DESC"""
    result = select(q)

    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "No landslide reports found with result other than 'Low'."}), 404  # 404 Not Found




# Insert a new complaint
@api.route('/send_complaint', methods=['POST'])
def send_complaint():
    data = request.json
    sender_id = data.get("sender_id")
    title = data.get("title")
    description = data.get("description")

    if not sender_id or not title or not description:
        return jsonify({"message": "Missing required fields"}), 400

    query = "INSERT INTO complaints (sender_id, title, description,date,reply) VALUES ('%s', '%s', '%s',curdate(),'NA')"%(sender_id, title, description)
    insert(query)

    return jsonify({"message": "Complaint submitted successfully"}), 201

# Retrieve complaints and replies for a specific sender
@api.route('/get_complaints/<int:sender_id>', methods=['GET'])
def get_complaints(sender_id):
    query = "SELECT complaints_id, title, description, reply, date FROM complaints WHERE sender_id = '%s' ORDER BY date DESC"%(sender_id)
    print(query)
    result=select(query)
    
    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "No complaints found"}), 404  # No Data Found


@api.route('/get_emergency_notifications', methods=['GET'])
def get_emergency_notifications():
    query = """SELECT emergency_notification_id, title, description, date, status 
               FROM emergency_notification 
               ORDER BY date DESC"""
    result = select(query)
    
    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "No emergency notifications found"}), 404  # No Data Found



@api.route('/get_helpline_numbers', methods=['GET'])
def get_helpline_numbers():
    
    query = """SELECT helpline_number_id, name, number 
               FROM helpline_number 
               ORDER BY name ASC"""
    result = select(query)
    

    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "No helpline numbers found"}), 404



@api.route('/get_family_friends/<int:user_id>', methods=['GET'])
def get_family_friends(user_id):
    query = """SELECT family_friend_id, name, number 
               FROM family_friends_number 
               WHERE user_id = '%s'"""%(user_id)
    result = select(query)

    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "No contacts found"}), 404

@api.route('/add_family_friend', methods=['POST'])
def add_family_friend():
    data = request.json
    user_id = data.get("user_id")
    name = data.get("name")
    number = data.get("number")

    if not user_id or not name or not number:
        return jsonify({"message": "Missing required fields"}), 400


    query = "INSERT INTO family_friends_number (user_id, name, number) VALUES ('%s', '%s', '%s')"%(user_id, name, number)
    insert(query)
   

    return jsonify({"message": "Contact added successfully"}), 201



# ✅ Submit a Landslide Report
@api.route('/report_landslide', methods=['POST'])
def report_landslide():
    data = request.json
    user_id = data.get("user_id")
    place = data.get("place")
    place = place.replace("'", "")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    date = datetime.date.today().strftime("%Y-%m-%d")
    time = datetime.datetime.now().strftime("%H:%M:%S")

    if not user_id or not place or not latitude or not longitude:
        return jsonify({"message": "Missing required fields"}), 400

    query = """INSERT INTO user_land_slide_report (user_id, place, latitude, longitude, date, time, status) 
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 'Pending')"""%(user_id, place, latitude, longitude, date, time)
    insert(query)
   
    return jsonify({"message": "Landslide reported successfully"}), 201


# ✅ Fetch Landslide Reports for Logged-in User
@api.route('/get_user_reports/<int:user_id>', methods=['GET'])
def get_user_reports(user_id):
    query = """SELECT user_report_id, place, latitude, longitude, date, time, status 
               FROM user_land_slide_report 
               WHERE user_id = '%s' ORDER BY date DESC"""%(user_id)
    result = select(query)
    print(result)
  
    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "No reports found"}), 404




# ✅ Fetch Today's Landslide Predictions (Exclude 'Low' Risk)
@api.route('/get_landslides', methods=['GET'])
def get_landslides():
    today_date = datetime.date.today().strftime("%Y-%m-%d")
    print("today_date : ",today_date)
 
    query = """SELECT predict_landslide_id, authority_id, location_name, latitude, longitude, 
                      temperature, humidity, precipitation, dew_point, wind_speed, elevation, 
                      soil_moisture, date_time, result 
               FROM predict_landslide 
               WHERE DATE(date_time) ='%s' AND result != 'Low'
               ORDER BY date_time DESC"""%(today_date)
    result_data = select(query)
    print("@"*100)
    print(result_data)

    

    if result_data:
        print("..............."*100)
        return jsonify(result_data)
    else:
        return jsonify({"message": "No landslide predictions for today"}), 404
