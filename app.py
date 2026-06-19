# This is the brain of Flask and with stgart the web server, define routes, and handle the logic of the web app

#Flask for the app, render templates for getting html in templates, redirect for auto taking to next page, url for so nothing breaks
# request for getting if it is a post or get request 
from flask import Flask, render_template, redirect, url_for, request
import database

#This starts the web app. __name__ is the current file, app is what routes will attach to and Flask is the framework
app = Flask(__name__)

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
    return "Dash coming soon"




#Used so only when this file is ran it will work not if it is called in another file
if __name__ == "__main__":
    #Debug helps with development but make sure it is off when it is live
    app.run(debug=True)