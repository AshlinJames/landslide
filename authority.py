from flask import *
from database import*
import os
import requests
from datetime import datetime,timedelta



authority=Blueprint('authority',__name__)

@authority.route("authority_home",methods=['get','post'])
def authority_home():
    data={}
    return render_template("authority_home.html",data=data)


@authority.route('/authority_view_update_profile', methods=['GET', 'POST'])
def authority_view_update_profile():
    if 'authority_id' not in session:
        flash("You must be logged in to view this page.", "danger")
        return redirect(url_for('public.login'))

    authority_id = session['authority_id']

    if request.method == 'POST' and 'update_profile' in request.form:
        authority_name = request.form['authority_name']
        district = request.form['district']
        place = request.form['place']
        phone = request.form['phone']

        # Update authority details
        update_query = """UPDATE authority SET authority_name='%s', district='%s', place='%s', phone='%s' WHERE authority_id='%s'""" % (authority_name, district, place, phone, authority_id)
        update(update_query)

        flash("Profile updated successfully!", "success")

    # Fetch authority details
    authority = select("SELECT * FROM authority WHERE authority_id='%s'"%(authority_id))

    return render_template("authority_view_update_profile.html", authority=authority[0])


@authority.route('/authority_send_complaints', methods=['GET', 'POST'])
def authority_send_complaints():
    if 'authority_id' not in session:
        flash("You must be logged in to send complaints.", "danger")
        return redirect(url_for('login'))

    authority_id = session['authority_id']

    if request.method == 'POST' and 'send_complaint' in request.form:
        title = request.form['title']
        description = request.form['description']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert complaint into the database
        insert_query = """INSERT INTO complaints (sender_id, title, description, reply, date) 
                          VALUES ('%s', '%s', '%s', 'NA', '%s')""" % (authority_id, title, description, date)
        insert(insert_query)

        flash("Complaint submitted successfully!", "success")

    # Fetch complaints made by the logged-in authority
    complaints = select("SELECT * FROM complaints WHERE sender_id='%s' ORDER BY complaints_id DESC"%(authority_id))

    return render_template("authority_send_complaints.html", complaints=complaints)



@authority.route('/authority_view_emergency_notifications', methods=['GET', 'POST'])
def authority_view_emergency_notifications():
    
    # Fetch all existing notifications
    notifications = select("SELECT * FROM emergency_notification ORDER BY emergency_notification_id DESC")

    # Format time difference for display
    for notification in notifications:
        notification["status"] = format_time_difference(notification["date"])
        print(notification["status"])

    return render_template("authority_view_emergency_notifications.html", notifications=notifications)

def update_notification_status():
    """Updates notifications that have expired to 'Inactive'."""
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    update_query = """UPDATE emergency_notification 
                      SET status='Inactive' 
                      WHERE date < '%s' AND status='Active'"""%(current_date)
    
    update(update_query)

def format_time_difference(notification_time):
    """Formats time difference into '1 hour ago', '1 day ago', etc."""
    current_time = datetime.now()
    notification_time = datetime.strptime(notification_time, "%Y-%m-%d %H:%M:%S")
    time_difference = current_time - notification_time

    if time_difference < timedelta(minutes=1):
        return "Now"
    elif time_difference < timedelta(hours=1):
        return f"{time_difference.seconds // 60} minutes ago"
    elif time_difference < timedelta(days=1):
        return f"{time_difference.seconds // 3600} hours ago"
    elif time_difference < timedelta(weeks=1):
        return f"{time_difference.days} days ago"
    elif time_difference < timedelta(days=30):
        return f"{time_difference.days // 7} weeks ago"
    elif time_difference < timedelta(days=365):
        return f"{time_difference.days // 30} months ago"
    else:
        return f"{time_difference.days // 365} years ago"




@authority.route('/authority_view_and_verify_landslide_reporting_from_user')
def authority_view_and_verify_landslide_reporting_from_user():
    # Fetch user-submitted landslide reports
    user_reports = select("SELECT * FROM user_land_slide_report ORDER BY user_report_id DESC")

    return render_template("authority_view_and_verify_landslide_reporting_from_user.html", user_reports=user_reports)

@authority.route('/verify_landslide/<int:report_id>/<string:status>')
def verify_landslide(report_id, status):
    """Updates the status of a landslide report."""
    update_query = "UPDATE user_land_slide_report SET status='%s' WHERE user_report_id='%s'" % (status, report_id)  
    update(update_query)

    flash(f"Landslide report {report_id} marked as {status}!", "success")
    return redirect(url_for('authority.authority_view_and_verify_landslide_reporting_from_user'))






def fetch_weather(lat, lon):
    """Fetches real-time weather data from Open-Meteo API based on selected latitude and longitude."""
    endpoint = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,precipitation,dewpoint_2m,windspeed_10m",
        "timezone": "auto"
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raise an error if request fails
        data = response.json()

        # Extract weather details
        current_weather = data.get("current", {})
        weather_data = {
            "success": True,
            "temperature": current_weather.get("temperature_2m", "N/A"),
            "humidity": current_weather.get("relative_humidity_2m", "N/A"),
            "precipitation": current_weather.get("precipitation", "N/A"),
            "dewpoint": current_weather.get("dewpoint_2m", "N/A"),
            "windspeed": current_weather.get("windspeed_10m", "N/A"),
            "elevation": data.get("elevation", "N/A")
        }
        return weather_data
    except requests.exceptions.RequestException:
        return {"success": False}


@authority.route('/authority_view_weather_data')
def authority_view_weather_data():
    return render_template("authority_view_weather_data.html")



@authority.route('/get_weather')
def get_weather():
    lat = request.args.get('lat', 20.5937)
    lon = request.args.get('lon', 78.9629)
    return jsonify(fetch_weather(lat, lon))
    
@authority.route('/landslide_prediction',methods=['get','post'])
def landslide_prediction():
    data1={}
    

    if request.method == 'POST':
        # Prepare new data for prediction
        lat = request.form.get('lat', 10.880397570633699)
        lon = request.form.get('lon', 78.32548141479492)
        location = request.form.get('location', 'Kanakampatty, Mathipatty, Krishnarayapuram, Karur, Tamil Nadu, India')
        temp = request.form.get('temp', 29.5)
        humidity = request.form.get('humidity', 53)
        precipitation = request.form.get('precipitation', 0)
        dewpoint = request.form.get('dewpoint', 18.9)
        windspeed = request.form.get('windspeed', 11.9)
        elevation = request.form.get('elevation', 121)
        soilmoisture = request.form.get('soilmoisture', 0.2)
        print("Preparing new data for prediction...")

        import numpy as np
        import pandas as pd
        import tensorflow as tf
        from tensorflow.keras.models import load_model
        import joblib

        # 🔹 Step 1: Load Saved Model, Scaler & Label Encoder
        model = load_model("landslide_risk_model.h5")
        scaler = joblib.load("scaler.pkl")
        label_encoder = joblib.load("label_encoder.pkl")

        # 🔹 Step 2: Prepare New Data for Prediction
        # Example new data point: Temperature, Humidity, Precipitation, Soil Moisture, Elevation
        # new_data = np.array([[32,94,232,89,861]])  # Replace with actual values
        new_data = np.array([[temp,humidity,precipitation,soilmoisture,elevation]])  # Replace with actual values

        # Standardize the new data using the saved scaler
        new_data_scaled = scaler.transform(new_data)

        # 🔹 Step 3: Make Prediction
        prediction = model.predict(new_data_scaled)
        predicted_class = np.argmax(prediction)  # Get the class with the highest probability

        # 🔹 Step 4: Convert Predicted Class Back to Category
        predicted_label = label_encoder.inverse_transform([predicted_class])

        # 🔹 Step 5: Print the Prediction
        print(f"Predicted Landslide Risk Level: {predicted_label[0]}")
        data1['predicted_label'] = predicted_label[0]
        dtime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        qry="""INSERT INTO `predict_landslide`
        (`predict_landslide_id`, `authority_id`, `location_name`, `latitude`, `longitude`, 
        `temperature`, `humidity`, `precipitation`, `dew_point`, `wind_speed`, `elevation`,
          `soil_moisture`, `date_time`, `result`) 
          VALUES (NULL,'%s','%s', '%s', '%s','%s','%s','%s', '%s', '%s','%s','%s', '%s','%s')"""%(session['authority_id'],location,lat,lon,temp,humidity,precipitation,dewpoint,windspeed,elevation,soilmoisture,dtime,predicted_label[0])
        insert(qry)
        # return render_template("landslide_prediction.html", data1=data1,data=request.args)






    return render_template("landslide_prediction.html", data=request.args,data1=data1)