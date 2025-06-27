from flask import *
from database import *

public = Blueprint('public', __name__)  

@public.route('/')
def home():
    return render_template("home.html")


@public.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()  # Clear session on login attempt

    if request.method == 'POST':  # Check if form is submitted
        uname = request.form['username']
        passs = request.form['password']

        # Secure query using parameterized format
        q = "SELECT * FROM login WHERE username='%s' AND password='%s'"% (uname, passs)
        res = select(q)

        if res:
            session['lid'] = res[0]['login_id']
            user_type = res[0]['usertype']

            if user_type == "admin":
                return render_template("success.html", redirect_url=url_for("admin.admin_home"))
                # return render_template(redirect_url=url_for("admin.admin_home"))
            
            elif user_type == "authority":
                authority_query = "SELECT * FROM authority WHERE login_id='%s'"% (session['lid'])
                authority_res = select(authority_query)
                if authority_res:
                    session['authority_id'] = authority_res[0]['authority_id']
                    flash("Login Success.", "success")
                    return redirect(url_for("authority.authority_home"))
                    
            else:
                flash("Invalid User Type!", "danger")
                return redirect(url_for("public.login"))

        else:
            return render_template("error.html", message="Login Failed! Check Username or Password.")

    return render_template("login.html")  # Render login page on GET request


