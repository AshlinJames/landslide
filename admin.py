from flask import *
from database import*
import os
from datetime import datetime, timedelta



admin=Blueprint('admin',__name__)


@admin.route("admin_home")
def admin_home():
	data={}
	if not session.get("lid") is None:
		
		return render_template("admin_home.html",data=data)
	else:
		return redirect(url_for("public.login"))



@admin.route('/admin_manage_authority', methods=['GET', 'POST'])
def admin_manage_authority():
    if request.method == 'POST' and 'add_authority' in request.form:
        authority_name = request.form['authority_name']
        district = request.form['district']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists
        check_query = "SELECT * FROM login WHERE username='%s'"%(email)
        existing_user = select(check_query)
        
        if existing_user:
            flash("Email already exists!", "danger")
        else:
            # Insert into login table
            login_query = "INSERT INTO login (username, password, usertype) VALUES ('%s', '%s', 'authority')"%(email, password)
            login_id = insert(login_query)

            # Insert into authority table
            authority_query = """INSERT INTO authority (login_id, authority_name, district, place, phone, email, status) 
                                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 'Active')"""%(login_id, authority_name, district, place, phone, email)
            insert(authority_query)

            flash("Authority added successfully!", "success")

    # Fetch existing authorities
    authorities = select("SELECT * FROM authority ORDER BY authority_id DESC")

    return render_template("admin_manage_authority.html", authorities=authorities)


@admin.route('/update_authority_status/<int:authority_id>/<string:status>')
def update_authority_status(authority_id, status):
    update_query = "UPDATE authority SET status='%s' WHERE authority_id='%s'"%(status, authority_id)
    update(update_query)

    flash("Authority status updated successfully!", "success")
    return redirect(url_for('admin.admin_manage_authority'))


@admin.route('/admin_send_emergency_notifications', methods=['GET', 'POST'])
def admin_send_emergency_notifications():
    if request.method == 'POST' and 'send_notification' in request.form:
        title = request.form['title']
        description = request.form['description']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
        status = "Active"  # Default status

        # Insert notification into the database
        insert_query = """INSERT INTO emergency_notification (title, description, date, status) 
                          VALUES ('%s', '%s', '%s', '%s')"""%(title, description, date, status)
        insert(insert_query)

        flash("Emergency notification sent successfully!", "success")

    # Update expired notifications
    update_notification_status()

    # Fetch all existing notifications
    notifications = select("SELECT * FROM emergency_notification ORDER BY emergency_notification_id DESC")

    # Format time difference for display
    for notification in notifications:
        notification["status"] = format_time_difference(notification["date"])
        print(notification["status"])

    return render_template("admin_send_emergency_notifications.html", notifications=notifications)

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





@admin.route('/admin_manage_help_line_number', methods=['GET', 'POST'])
def admin_manage_help_line_number():
    if request.method == 'POST' and 'add_update_helpline' in request.form:
        helpline_number_id = request.form.get('helpline_number_id')  # Get ID (if updating)
        name = request.form['name']
        number = request.form['number']

        if helpline_number_id:  # If ID exists, update the record
            update_query = "UPDATE helpline_number SET name='%s', number='%s' WHERE helpline_number_id='%s'"%(name, number, helpline_number_id)
            update(update_query)
            flash("Helpline number updated successfully!", "success")
        else:  # Otherwise, insert a new record
            insert_query = "INSERT INTO helpline_number (name, number) VALUES ('%s', '%s')"%(name, number)
            insert(insert_query)
            flash("Helpline number added successfully!", "success")

    # Fetch existing helpline numbers
    helplines = select("SELECT * FROM helpline_number ORDER BY helpline_number_id DESC")

    return render_template("admin_manage_help_line_number.html", helplines=helplines)

@admin.route('/delete_helpline/<int:helpline_number_id>')
def delete_helpline(helpline_number_id):
    """Delete a helpline number from the database."""
    delete_query = "DELETE FROM helpline_number WHERE helpline_number_id='%s'"%(helpline_number_id)
    delete(delete_query)
    flash("Helpline number deleted successfully!", "success")
    return redirect(url_for('admin.admin_manage_help_line_number'))


@admin.route('/admin_view_complaints_send_reply', methods=['GET', 'POST'])
def admin_view_complaints_send_reply():
    if request.method == 'POST' and 'send_reply' in request.form:
        complaints_id = request.form['complaints_id']
        reply = request.form['reply']
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Update complaint with reply
        update_query = "UPDATE complaints SET reply='%s', date='%s' WHERE complaints_id='%s' AND reply='NA'"%(reply, current_date, complaints_id)
        update(update_query)

        flash("Reply sent successfully!", "success")

    # Fetch all complaints
    complaints = select("SELECT * FROM complaints ORDER BY complaints_id DESC")

    return render_template("admin_view_complaints_send_reply.html", complaints=complaints)



@admin.route('/admin_view_landslide_reporting')
def admin_view_landslide_reporting():
    # Fetch user landslide reports
    user_reports = select("SELECT * FROM user_land_slide_report ORDER BY user_report_id DESC")

    # Fetch authority landslide reports
    authority_reports = select("SELECT * FROM authority_land_slide_report ORDER BY authority_report_id DESC")

    return render_template("admin_view_landslide_reporting.html", user_reports=user_reports, authority_reports=authority_reports)



@admin.route('/admin_view_landslide_prediction')
def admin_view_landslide_prediction():
    # Fetch landslide prediction records
    predictions = select("SELECT * FROM predict_landslide ORDER BY predict_landslide_id DESC")

    return render_template("admin_view_landslide_prediction.html", predictions=predictions)
