#Database will handle everything related to storing and retrieving data. This will never talk to the user
#Used for Web version
#Uses psycopg2 so I can keep data even if the server goes to sleep

import psycopg2

#Will let me load the .env file
from dotenv import load_dotenv

#Lets me access environment variables
import os

import datetime
import bcrypt

#Read the .env file
load_dotenv()


#____________________________________________________________________________________________________________________________________

#This will be a users table
def users_table():

    #Open/Create the data base file / os.getenv asks for what is in Database url 
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))

    #Creates a cursor so that you can run SQL commands
    cursor = connection.cursor()

    #This section will create the database that will be used and set up the columns for the data
    #SERIAL is and integer and autoincrments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            account_type TEXT DEFAULT 'regular'
        )
    """)

    #Saves the changes to the database file
    connection.commit()

    #Closes the file
    connection.close()


#Register a new user
def register_user(username, password):
    
    #Open/Create the data base file
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))

    #Creates a cursor so that you can run SQL commands
    cursor = connection.cursor()

    #Hash the password using bcrypt and salt is so that identical passwords get hashed to different values
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt().decode('utf-8'))

    #Insert the new user into the users table and see if the username is taken
    try:

        cursor.execute("""
            INSERT INTO users (username, password_hash) VALUES (%s, %s)
        """, (username, password_hash))
        connection.commit()
        connection.close()
        print("User registered successfully.")
        return True
    except:
        connection.close()
        print("Username already taken. Please choose a different username.")
        return False
    


#Where login will be handled and the password will be checked
def login_user(username, password):

    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = connection.cursor()

    #Get all usernames and make sure the one they type is real
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    connection.close()

    #If no user is found end the function and ask they to register
    if not user:
        print("Username not found. Please register first.")
        return False    
    
    #Check the password
    #user[2] because password is in the 2nd column of the table
    #Since PostgreSQL stores as text you need to make it to bytes
    stored_hash = user[2].encode('utf-8')
    #hashes the password they entered and checks it with the stored hash to see if it maches
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)


#Gets all the users data from the table and returns it
def get_user(username):

    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = connection.cursor()

    #Get all the data for the user and return it
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    connection.close()
    return user




#____________________________________________________________________________________________________________________________________

#Function to setup the database table
def setup_database():

    #Open/Create the data base file
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))

    #Creates a cursor so that you can run SQL commands
    cursor = connection.cursor()

    #Try and create the table so you don't have to call it somewhere else
    users_table()

    #This section will create the database that will be used and set up the columns for the data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            status TEXT DEFAULT 'Applied',
            date_applied TEXT,
            notes TEXT,
            url TEXT,
            user_id INTEGER REFERENCES users(id)
        )
    """)

    #Saves the changes to the database file
    connection.commit()

    #Closes the file
    connection.close()


#This will be used to add all the data to the table by the user
def add_job(company,role,location,status,date_applied,notes,url, user_id = None):
    
    #Open/Create the data base file
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))

    #Creates a cursor so that you can run SQL commands
    cursor = connection.cursor()

    #This is where you define the columns used and the values
    #Uses ? for no SQL injection
    cursor.execute("""
    
        INSERT INTO jobs(company,role,location,status,date_applied,notes,url, user_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """, (company,role,location,status,date_applied,notes,url, user_id))

    #Saves the changes to the database file
    connection.commit()

    #Closes the file
    connection.close()


#This function will return all jobs in the table
def get_all_jobs(sort_by = "4", user_id = None):

    #Open/Create the data base file
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))

    #Creates a cursor so that you can run SQL commands
    cursor = connection.cursor()

    #Get all the information from the table based on the Sort_By
    if sort_by == "1":
        cursor.execute("SELECT * FROM jobs WHERE user_id = %s ORDER BY date_applied ASC", (user_id,))
    elif sort_by == "2":
        cursor.execute("SELECT * FROM jobs WHERE user_id = %s ORDER BY company ASC", (user_id,))
    elif sort_by == "3":
        cursor.execute("SELECT * FROM jobs WHERE user_id = %s ORDER BY status ASC", (user_id,))
    elif sort_by == "4":
        cursor.execute("SELECT * FROM jobs WHERE user_id = %s ORDER BY id ASC", (user_id,))
    else:
        print("Invalid sort option. Defaulting to sorting by ID.")
        cursor.execute("SELECT * FROM jobs WHERE user_id = %s ORDER BY id ASC", (user_id,))


    #Now get the table from jobs
    table = cursor.fetchall()

    #Closes the file
    connection.close()

    #Return the table to the user
    return table



#Will update the columns in the database
def update_job(job_id, new_status = None, new_notes = None, new_url = None):

    #Open/Create the data base file
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))

    #Creates a cursor so that you can run SQL commands
    cursor = connection.cursor()

    #Arrays for the data that is needed
    updates = []
    values = []

    #If statments for if a field was left blank and if so do not overwrite it
    if new_status not in (None, ""):
        updates.append("status = %s")
        values.append(new_status)
    
    if new_notes not in (None, ""):
        updates.append("notes = %s")
        values.append(new_notes)

    if new_url not in (None, ""):
        updates.append("url = %s")
        values.append(new_url)

    #If empty do nothing
    if not updates:
        connection.close()
        return


    #Because it is dynamic you have to build the sql outside the execute
    sql = "UPDATE jobs SET " + ", ".join(updates) + " WHERE id = %s" 
    #Add job id to the end for the WHERE
    values.append(job_id)

    #Run the code
    cursor.execute(sql, values)

    #Saves the changes to the database file
    connection.commit()

    #Closes the file
    connection.close()


#Used to delete any jobs
def delete_job(job_id):

    #Open/Create the data base file
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))

    #Creates a cursor so that you can run SQL commands
    cursor = connection.cursor()

    #Deletes a whole job from the table
    cursor.execute("DELETE FROM jobs WHERE id = %s", (job_id,))

    #Saves the changes to the database file
    connection.commit()

    #Closes the file
    connection.close()

#____________________________________________________________________________________________________________________________________

#Used so only when this file is ran it will work not if it is called in another file
if __name__ == "__main__":
    setup_database()