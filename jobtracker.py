#This file is what the user will use to interact with the database and make changes or look at the jobs
import datetime
import database


#This function will add a job
def add_job_call():
    
    #Ask for all information
    company = input("Enter the company name: ")
    while not company:
        company = input("Company name cannot be empty. Please enter the company name: ")
    role = input("Enter job title: ")
    while not role:
        role = input("Job title cannot be empty. Please enter the job title: ")
    location = input("Enter the location of the buisness: ")
    status = input("Enter the status of the application (press Enter for 'Applied'): ") or "Applied"
    date_applied = input("Enter the date applied (YYYY-MM-DD) or press Enter for today: ") or str(datetime.date.today())
    notes = input("Enter notes you want to keep: ")
    url = input("Enter job URL: ")

    #Then pass everything to the database
    database.add_job(company,role,location,status,date_applied,notes,url)

    print("New job has been added successfully!")

    #Add a space
    print()


#This will bring up all jobs in the table
def view_jobs():
    #Get a list of tuples
    jobs = database.get_all_jobs()

    #Check if the list has jobs in it
    if not jobs:
        print("No jobs found")
        return
    
    #Print out every job in the list
    for i in jobs:
        print("-" * 40)
        print(f"ID: {i[0]}")
        print(f"Company: {i[1]}")
        print(f"Role: {i[2]}")
        print(f"Location: {i[3]}")
        print(f"Status: {i[4]}")
        print(f"Date applied: {i[5]}")
        print(f"Notes: {i[6]}")
        print(f"URL: {i[7]}")
    
    #Add a space
    print()


#Will update a section of a certain job
def update_job_call():
    print("Pick from the list which job you want to update")
    view_jobs()

    #Get the job ID and other information
    job_id = int(input("Enter the ID of the job you want to update: "))
    new_status = input("Enter the new status of the application (press Enter for 'Applied'): ") or "Applied"
    new_notes = input("Enter new notes (press Enter to keep current): ") or None

    #Call the database
    database.update_job(job_id, new_status, new_notes)
    print("Job has been successfully updated!")
    print()


#Will delete a job
def delete_job_call():
    print("Pick from the list which job you want to delete")
    view_jobs()

    #Get the job ID
    job_id = int(input("Enter the ID of the job you want to delete: "))

    #Call the database and ask for confrimation
    confirm = input("Are you sure you want to delete this job? (yes/no): ")
    if confirm == "yes":
        database.delete_job(job_id)
        print("Job has been successfully deleted!")
    else:
        print("Delete has been cancelled")
    print()


#Will be used to start and ask what the user wants to do
def main():

    #make sure the database is up and running
    database.setup_database()

    while True:
        print("1. Add a job")
        print("2. View all jobs")
        print("3. Update a job")
        print("4. Delete a job")
        print("5. Exit")

        #Ask the user to make a choice
        choice = input("Pick a number to continue: ")

        #This is where calls are made based on user decision
        if choice == "1":
            add_job_call()
        elif choice == "2":
            view_jobs()
        elif choice == "3":
            update_job_call()
        elif choice == "4":
            delete_job_call()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid please try again")


#Used so only when this file is ran it will work not if it is called in another file
if __name__ == "__main__":
    main()