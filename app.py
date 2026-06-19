# This is the brain of Flask and with stgart the web server, define routes, and handle the logic of the web app

#Flask for the app, render templates for getting html in templates, redirect for auto taking to next page, url for so nothing breaks
# request for getting if it is a post or get request, Sessions for keeping track if a user is logged in on every page
from flask import Flask, render_template, redirect, url_for, request, session
import database
from datetime import timedelta

#This starts the web app. __name__ is the current file, app is what routes will attach to and Flask is the framework
app = Flask(__name__)

#Gives 30 minutes of session time before it logs out the user for being inactive
app.permanent_session_lifetime = timedelta(minutes = 30)

app.secret_key = "change_this_to_something_random_before_going_live"


#Make sure the database is set up before the website starts
database.setup_database()





#Connects the root url aka the homepage of the website
@app.route('/')
#This is the root page of the website
def home():
    return redirect(url_for("login"))



#Because we have post on the html I need methods
@app.route('/login', methods = ['GET', 'POST'])
def login():

    #Check if a POST way sent
    if request.method == 'POST':
        #Get the username and password
        username = request.form['username']
        password = request.form['password']

        #check if they match the database
        if database.login_user(username, password):

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
def register():

    #Check if a POST way sent
    if request.method == 'POST':
        #Get the username and password
        username = request.form['username']
        password = request.form['password']

        #Register the user in the database
        if database.register_user(username, password):
            #Send them to login
            return redirect(url_for('login'))
        
        else:
            #Throw an error because username is taken
            return render_template('register.html', error = "Username is already taken")
        

    #Show the register page if it is a GET
    return render_template('register.html')





@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    #Get the users data from the database
    user = database.get_user(session['username'])
    
    #Get the user id number
    user_id = user[0]

    #Gets all the jobs of the user and also makes sure the parameter is done right
    jobs = database.get_all_jobs(user_id = user_id)

    #Send the data to the html and send the jobs and username with it
    return render_template('dashboard.html', username = session['username'], jobs = jobs)


@app.route('/logout')
def logout():
    #Clear the session data to log out the user and return to the logout page
    session.clear()
    return redirect(url_for('login'))


#Used so only when this file is ran it will work not if it is called in another file
if __name__ == "__main__":
    #Debug helps with development but make sure it is off when it is live
    app.run(debug=True)