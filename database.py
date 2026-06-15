#Database will handle everything related to storing and retrieving data. This will never talk to the user

import sqlite3
import datetime

#Function to setup the database table
def setup_database():

    #Open/Create the data base file
    connection = sqlite3.connect("jobs.db")

    #Creates a cursor so that you can run SQL commands
    cursor = connection.cursor()

    #This section will create the database that will be used and set up the columns for the data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            status TEXT DEFAULT 'Applied',
            date_applied TEXT,
            notes TEXT,
            url TEXT
        )
    """)

    #Saves the changes to the database file
    connection.commit()

    #Closes the file
    connection.close()


#This will be used to add all the data to the table by the user
def add_job(company,role,location,status,date_applied,notes,url):
    
    #Open/Create the data base file
    connection = sqlite3.connect("jobs.db")

    #Creates a cursor so that you can run SQL commands
    cursor = connection.cursor()

    #This is where you define the columns used and the values
    #Uses ? for no SQL injection
    cursor.execute("""
    
        INSERT INTO jobs(company,role,location,status,date_applied,notes,url) VALUES(?,?,?,?,?,?,?)
    """, (company,role,location,status,date_applied,notes,url))

    #Saves the changes to the database file
    connection.commit()

    #Closes the file
    connection.close()


#This function will return all jobs in the table
def get_all_jobs():

    #Open/Create the data base file
    connection = sqlite3.connect("jobs.db")

    #Creates a cursor so that you can run SQL commands
    cursor = connection.cursor()

    #Get all the information from the table
    cursor.execute("SELECT * FROM jobs")

    #Now get the table from jobs
    table = cursor.fetchall()

    #Closes the file
    connection.close()

    #Return the table to the user
    return table



#Will update the columns in the database
def update_job(job_id, new_status, new_notes):

    #Open/Create the data base file
    connection = sqlite3.connect("jobs.db")

    #Creates a cursor so that you can run SQL commands
    cursor = connection.cursor()

    cursor.execute("UPDATE jobs SET status = ?, notes = ? WHERE id = ?",(new_status, new_notes, job_id))

    #Saves the changes to the database file
    connection.commit()

    #Closes the file
    connection.close()


#Used to delete any jobs
def delete_job(job_id):

    #Open/Create the data base file
    connection = sqlite3.connect("jobs.db")

    #Creates a cursor so that you can run SQL commands
    cursor = connection.cursor()

    #Deletes a whole job from the table
    cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))

    #Saves the changes to the database file
    connection.commit()

    #Closes the file
    connection.close()


#Used so only when this file is ran it will work not if it is called in another file
if __name__ == "__main__":
    setup_database()