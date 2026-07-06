# This is the brain of Flask and with stgart the web server, define routes, and handle the logic of the web app

#Flask for the app, render templates for getting html in templates, redirect for auto taking to next page, url for so nothing breaks
# request for getting if it is a post or get request, Sessions for keeping track if a user is logged in on every page
from flask import Flask, render_template, redirect, url_for, request, session, make_response
import database_web
from datetime import timedelta, datetime
from dotenv import load_dotenv
import os

#Login required detector is needed
from functools import wraps
#Makes sure that the logged in user can not hit the back page button after logging out
#Wraps the route and makes sure it is not cached
def nocache(f):
    
    #Pretend to be f
    @wraps(f)

    #Lets it take any argument
    def decorated_function(*args, **kwargs):

        #Call the original function
        response = make_response(f(*args, **kwargs))

        #Says to not cache this page and get a new one
        response.headers['Cache-Control'] = 'no-store'


        return response
    
    return decorated_function





#This starts the web app. __name__ is the current file, app is what routes will attach to and Flask is the framework
app = Flask(__name__)

#Gives 30 minutes of session time before it logs out the user for being inactive
app.permanent_session_lifetime = timedelta(minutes = 30)

#Gets the key from .env
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')


#Make sure the database is set up before the website starts
database_web.setup_database()





#Connects the root url aka the homepage of the website
@app.route('/')
#This is the root page of the website
def home():
    #Go to login
    return redirect(url_for("login"))



#Because we have post on the html I need methods
@app.route('/login', methods = ['GET', 'POST'])
@nocache
def login():

    #Check if a POST way sent
    if request.method == 'POST':
        #Get the username and password
        username = request.form['username']
        password = request.form['password']

        #check if they match the database
        if database_web.login_user(username, password):

            #This starts the timer for the session so they will be logged out after 30 minutes of inactivity
            session.permanent = True

            #This keeps the username and proof they are logged in on every page.
            session['username'] = username

            #If a match is found send them to the dashboard
            return redirect(url_for('dashboard'))
        
        else:
            #If no match is found show an error message by loading the login page and giving it a variable called error with the message
            return render_template('login.html', error = "Invalid username or password")
        

    #Show the login page if it is a GET
    return render_template('login.html')

#Used for the Register page
@app.route('/register', methods = ['GET', 'POST'])
@nocache
def register():

    #Check if a POST way sent
    if request.method == 'POST':
        #Get the username and password
        username = request.form['username']
        password = request.form['password']

        #Register the user in the database
        if database_web.register_user(username, password):
            #Send them to login
            return redirect(url_for('login'))
        
        else:
            #Throw an error because username is taken
            return render_template('register.html', error = "Username is already taken")
        

    #Show the register page if it is a GET
    return render_template('register.html')





@app.route('/dashboard')
@nocache
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    #Get the users data from the database
    user = database_web.get_user(session['username'])
    
    #Get the user id number
    user_id = user[0]

    #Try and get the sort value if not there use 4
    sort_by = request.args.get('sort', '4')

    #Gets all the jobs of the user and also makes sure the parameter is done right
    jobs = database_web.get_all_jobs(sort_by = sort_by, user_id = user_id)

    #Send the data to the html and send the jobs and username with it
    return render_template('dashboard.html', username = session['username'], jobs = jobs)


@app.route('/logout')
@nocache
def logout():
    #Clear the session data to log out the user and return to the logout page
    session.clear()
    return redirect(url_for('login'))



@app.route('/add', methods = ['GET', 'POST'])
@nocache
def add():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':

        #Get user id
        user = database_web.get_user(session['username'])
        user_id = user[0]

        #Get the data from the form
        company = request.form['company']
        role = request.form['role']
        location = request.form['location']
        status = request.form['status'] or "Applied"
        date_applied = request.form['date_applied'] or str(datetime.now().date())
        notes = request.form['notes']
        url = request.form['url']

        #Add the job to the database
        database_web.add_job(company, role, location, status, date_applied, notes, url, user_id)

        #Go back to the dashboard
        return redirect(url_for('dashboard'))
    
    #Show the add page if it is a GET
    return render_template('add.html')


#Job id is sent when clicked look at the table in dashboard and you will see the values
@app.route('/update/<int:job_id>', methods = ['GET', 'POST'])
@nocache
def update(job_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':

        #Get the data from the user to update
        new_status = request.form['status']
        new_notes = request.form['notes']
        new_url = request.form['url']

        #update the database
        database_web.update_job(job_id, new_status, new_notes, new_url)

        #Go back to the dashboard
        return redirect(url_for('dashboard'))

    #Show the update page if it is a GET and pass the job id to a variable that can be used in update
    #Adding show information if they have it

    #Get user id
    user = database_web.get_user(session['username'])
    user_id = user[0]

    job = database_web.get_job(job_id, user_id)

    if job:

        return render_template('update.html', job_id = job_id, status = job[4], notes = job[6], url = job[7])

    return redirect(url_for('dashboard'))




@app.route('/delete/<int:job_id>')
@nocache
def delete(job_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    #Delete the job from the database
    database_web.delete_job(job_id)

    #Reload the dashboard
    return redirect(url_for('dashboard'))


#Used so only when this file is ran it will work not if it is called in another file
if __name__ == "__main__":
    #Debug helps with development but make sure it is off when it is live
    #Put in .env file so it is not showing and only I can change it and it is secure
    app.run(debug= os.getenv('DEBUG', 'False') == 'True')