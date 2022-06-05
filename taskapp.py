###########################################################
# CMSC 127 S-4L FINAL PROJECT FOR S.Y '21-'22
# A simple task listing app using python and mysql(mariadb)
# Authors:
#    ඞbadines, Jhiedy Wynn
#    Cagara, Johann
#    Tuazon, Andre
###########################################################
#imports
import mysql.connector as mariadb
from random import randint

#Create mysql connection and define cursor
mariadb_connection = mariadb.connect(user='test', password='password', host = 'localhost', database = 'task_record')
create_cursor = mariadb_connection.cursor()

################################################ Define Function ################################################
def addTask():
    # check first if the task table is not full
    create_cursor.execute("SELECT Task_id FROM task")
    data = create_cursor.fetchall()
    taskID = randint(10, 99)
    taskIDs = []
    for x in data:
        taskIDs.append(x[0])
    
    if(len(taskIDs)==90):
        print("Database is full.")
        return

    # choose randomly generated 2-digit int that does not yet exist
    while(taskID in taskIDs):
        taskID = randint(10,99)

    # get user inputs then append to query
    taskName = str(input("Please input the name of the task: "))
    taskDesc = str(input("Please input description of the task: "))
    taskDeadline = str(input("Please input the deadline of the task (YYYY-MM-DD): "))
    the_command = "INSERT INTO task VALUES (" + str(taskID) + ", \"" + taskName + "\", \"" + taskDesc + "\" , CURDATE(), STR_TO_DATE(\"" + taskDeadline + "\" , \"%Y-%m-%d\"), \"Ongoing\", 999)"
    # execute the command and commit to the database
    create_cursor.execute(the_command)
    mariadb_connection.commit()
    print("Task added successfully.")

def viewSpecificTask(taskID):
    # prints task with specified task ID
    create_cursor.execute("SELECT * FROM task WHERE Task_id = %s" % str(taskID))
    data = create_cursor.fetchall()

    for x in data:
        print("Task id:\t\t" + str(x[0]))
        print("Task name:\t\t" + x[1])
        print("Task description:\t" + x[2])
        print("Date posted:\t\t" + str(x[3]))
        print("Deadline:\t\t" + str(x[4]))
        print("Status:\t\t\t" + x[5])
        print("Category:\t\t" + str(x[6]))
        print()
    

def editTask():
    # check first if task table is not empty
    create_cursor.execute("SELECT Task_id FROM task")
    data = create_cursor.fetchall()
    
    taskIDs = []
    for x in data:
        taskIDs.append(x[0])
    
    if(len(taskIDs)==0):
        print("There is no data in the database.")
        return
    
    # get user input
    taskID = int(input("Please input the task id to be edited: "))

    # check if task ID exists in database
    if(taskID in taskIDs):
        # while loop that allows the user to repeatedly edit the task 
        while(True):
            print("==============================")
            # prints the specified task to allow user to see the changes
            viewSpecificTask(taskID)
            print("==============================")
            print("[1] Change Name")
            print("[2] Change Description")
            print("[3] Change Deadline")
            print("[0] Exit Edit Menu")
            userInput = str(input("Choice: "))

            if(userInput == "1"):
                # query that edits the task name of specified task
                taskName = str(input("Please input the new name of the task: "))
                command = ("UPDATE task SET Name = \"%s\" WHERE Task_id = %s" % (taskName, str(taskID)))
                create_cursor.execute(command)
                mariadb_connection.commit()
            elif(userInput == "2"):
                # query that edits the task description of specified task
                taskDesc = str(input("Please input the new description of the task: "))
                command = ("UPDATE task SET Description = \"%s\" WHERE Task_id = %s" % (taskDesc, str(taskID)))
                create_cursor.execute(command)
                mariadb_connection.commit()
            elif(userInput == "3"):
                # query that edits the task deadline of specified task
                taskDeadline = str(input("Please input the new deadline of the task (YYYY-MM-DD): "))
                command = "UPDATE task SET Deadline = STR_TO_DATE(\"" + taskDeadline + "\", \"%Y-%m-%d\") WHERE Task_id = " + str(taskID)
                create_cursor.execute(command)
                mariadb_connection.commit()
            elif(userInput=="0"):
                break
            
            print("Data has been successfully edited.")
    else:
        print("The Task id you inputted is not in the database.")
    
def deleteTask():
    # check first if task table is not empty
    create_cursor.execute("SELECT Task_id FROM task")
    data = create_cursor.fetchall()
    
    taskIDs = []
    for x in data:
        taskIDs.append(x[0])

    if(len(taskIDs)==0):
        print("There is no data in the database.")
        return

    # get user input
    taskID = int(input("Please input the task id to be deleted: "))

    # check if task is in the database
    if(taskID in taskIDs):
        # query that deletes the task with the specified id
        the_command = "DELETE FROM task WHERE Task_id = " + str(taskID)
    
        create_cursor.execute(the_command)
        mariadb_connection.commit()
    else:
        print("The Task id you inputted is not in the database.")

def viewTask():
    # checks first if task table is not empty
    create_cursor.execute("SELECT Task_id FROM task")
    data = create_cursor.fetchall()
    
    taskIDs = []
    for x in data:
        taskIDs.append(x[0])

    if(len(taskIDs)==0):
        print("There is no data in the database.")
        return
    
    # gets all tasks and prints them
    create_cursor.execute("SELECT * FROM task ORDER BY Deadline ASC")
    data = create_cursor.fetchall()
    print("============== T A S K S ==============")
    for x in data:
        print("● Task id:\t\t" + str(x[0]))
        print("● Task name:\t\t" + x[1])
        print("● Task description:\t" + x[2])
        print("● Date posted:\t\t" + str(x[3]))
        print("● Deadline:\t\t" + str(x[4]))
        print("● Status:\t\t" + x[5])
        print("● Category:\t\t" + str(x[6]))
        print()

def markTaskAsDone():
    # check first if task table is not empty
    create_cursor.execute("SELECT Task_id FROM task")
    data = create_cursor.fetchall()
    taskIDs = []
    for x in data:
        taskIDs.append(x[0])
    
    if(len(taskIDs)==0):
        print("There is no data in the database.")
        return
    
    late = "Accomplished Late"
    acc = "Accomplished"
    # gets user input
    id = int(input("Enter ID of task to mark as done: "))
    # checks if task exists in database 
    if(id in taskIDs):
        # query that updates the status of the task with specified id to either Accomplished or Accomplished Late
        sql_statement = 'UPDATE task SET Status = CASE WHEN DATEDIFF(CURDATE(), Deadline)>0 THEN %s ELSE %s END WHERE Task_id=%s;'
        to_update = (late, acc, id)
        create_cursor.execute(sql_statement, to_update)
        mariadb_connection.commit()
        print("Task %s is Marked as DONE." % id)
    else:
        print("Task not found in the database.")

def addCategory():
    # check first if the category table is not full
    create_cursor.execute("SELECT Category_id FROM category")
    data = create_cursor.fetchall()
    categoryIDS = []
    for x in data:
        categoryIDS.append(x[0])
    
    if(len(categoryIDS)==899):
        print("Database is full.")
        return

    id = randint(100,999)
    # choose a randomly generated categoryId that does not yet exist
    while(id in categoryIDS):
        id = randint(10,99)
    # get user input
    name = input("Enter name of new Category: ")
    defaultStatus = "Not Yet Done"

    # query that inserts new vlaue to category table
    sql_statement = 'INSERT INTO category VALUES (%s, %s, %s);'
    to_insert = (id, name, defaultStatus)
    create_cursor.execute(sql_statement, to_insert)
    mariadb_connection.commit()
    print("Category %s Added!\n" % name)

def editCategory():
    # check first if category table is not empty
    create_cursor.execute("SELECT Category_id FROM category WHERE Category_id != 999")
    data = create_cursor.fetchall()
    categoryIDs = []
    for x in data:
        categoryIDs.append(x[0])
    if(len(categoryIDs)==0):
        print("There is no data in the database.")
        return

    # get user input
    id = int(input("Enter ID of category to be edited: ") )
    # print first category with specified category 
    sql_statement = 'SELECT * FROM category WHERE Category_id = %s;' % id
    create_cursor.execute(sql_statement)
    category = create_cursor.fetchall()
    print("======= C A T E G O R Y =======")
    for x in category:
        print("● Category id:\t\t" + str(x[0]))
        print("● Category name:\t" + x[1])
        print("● Status:\t\t" + x[2] + "\n")
    # check if categoryID exists in database
    if(id in categoryIDs):
        #query that edits the name of the category with the specified id
        newCategName = input("Enter New Name for Category %s: " % str(id)) 
        sql_statement = 'UPDATE category SET Name=%s WHERE Category_id=%s;'
        to_update = (newCategName, id)
        create_cursor.execute(sql_statement, to_update)
        mariadb_connection.commit()
        print("Category %s Edited!\n" % id)
    else:
        print("Category not found in database.")

def deleteCategory():
    # check first if category table is not empty
    create_cursor.execute("SELECT Category_id FROM category WHERE Category_id != 999")
    data = create_cursor.fetchall()
    categoryIDs = []
    for x in data:
        categoryIDs.append(x[0])
    if(len(categoryIDs)==0):
        print("There is no data in the database.")
        return

    # get user input
    id = int(input("Enter ID of category to be deleted: "))
    # check if category id exists in the database
    if(id in categoryIDs):
        # query that updates the category_id of tasks under category that was deleted to the default category 
        sql_statement = 'UPDATE task SET Category_id=999 WHERE Category_id=%s;'
        to_update = (id)
        create_cursor.execute(sql_statement, (to_update,))
        mariadb_connection.commit()
        # query that deletes category with specified id
        sql_statement = 'DELETE FROM category WHERE Category_id=%s;'
        to_delete = (id)
        create_cursor.execute(sql_statement, (to_delete,))
        mariadb_connection.commit()
        print("Successfully deleted category %s.\n" % id)
    else:
        print("Category not found in database")

def viewCategory():
    # check first if category table is not empty
    create_cursor.execute("SELECT Category_id FROM category WHERE Category_id != 999")
    data = create_cursor.fetchall()
    categoryIDs = []
    for x in data:
        categoryIDs.append(x[0])
    if(len(categoryIDs)==0):
        print("There is no data in the database.")
        return
    
    # query that selects all on category table
    sql_statement = 'SELECT * FROM category;'
    create_cursor.execute(sql_statement)
    category = create_cursor.fetchall()
    # print all values in category
    print("======= C A T E G O R Y =======")
    for x in category:
        print("● Category id:\t\t" + str(x[0]))
        print("● Category name:\t" + x[1])
        print("● Status:\t\t" + x[2] + "\n")   

def viewCategoryTasks():
    # check first if category table is not empty
    create_cursor.execute("SELECT Category_id FROM category WHERE Category_id != 999")
    data = create_cursor.fetchall()
    categoryIDs = []

    for x in data:
        categoryIDs.append(x[0])

    if(len(categoryIDs)==0):
        print("There are no categories in the database.")
        return
    
    # get user input
    id = int(input("Enter ID of the category to view: "))
    # user input cannot be the default category
    if(id==999):
        print("You cannot edit the default category.")
        return
    # check if id is in database
    if(id not in categoryIDs):
        print("The Category ID does not exist.")
        return
    # if category exists, select all tasks under with that category id
    sql_statement = 'SELECT * FROM task WHERE Category_id=%s;'
    to_view = (id)
    create_cursor.execute(sql_statement, (to_view,))
    task_rows = create_cursor.fetchall()
    
    if(len(task_rows)==0):
        print("There are no tasks in this category.")
        return
    # print all values in task_rows
    print("======= T A S K S =======")
    for x in task_rows:
        print("■ Task id:\t\t" + str(x[0]))
        print("■ Task name:\t\t" + x[1])
        print("■ Task description:\t" + x[2])
        print("■ Date posted:\t\t" + str(x[3]))
        print("■ Deadline:\t\t" + str(x[4]))
        print("■ Status:\t\t" + x[5])
        print("■ Category:\t\t" + str(x[6]))
        print()

def addTaskCategory():
    #Checking if there is any tasks
    create_cursor.execute("SELECT Task_id FROM task")
    data = create_cursor.fetchall()
    
    taskIDs = []
    for x in data:
        taskIDs.append(x[0])

    if(len(taskIDs)==0):
        print("There is no data in the database.")
        return
    
    #Checking if there is any categories
    create_cursor.execute("SELECT Category_id FROM category WHERE Category_id != 999")
    data = create_cursor.fetchall()
    categoryIDs = []

    for x in data:
        categoryIDs.append(x[0])

    if(len(categoryIDs)==0):
        print("There are no categories in the database.")
        return

    # get user input
    id1 = int(input("Enter ID of category: "))
    id2 = int(input("Enter ID of task to be put in the category: "))
    # check if task and category inputs exists in database
    if((id2 in taskIDs) and (id1 in categoryIDs)):
        # query that updates the category_id of task to the specified category id
        sql_statement = 'UPDATE task SET Category_id=%s WHERE Task_id=%s;'
        to_add = (id1, id2)
        create_cursor.execute(sql_statement, to_add)
        mariadb_connection.commit()
        print("Task successfully added to Category %s!" % id1)
    else:
        print("Task/Category ID not found.")

def viewTaskSpecificDate():
    #Checking if there is any tasks
    create_cursor.execute("SELECT Task_id FROM task")
    data = create_cursor.fetchall()
    
    taskIDs = []
    for x in data:
        taskIDs.append(x[0])

    if(len(taskIDs)==0):
        print("There is no data in the database.")
        return

    # get user input
    month = input("Enter the month you want to check (MM): ")
    day = input("Enter the day you want to check (DD): ")

    # query that selects tasks where deadline is on the specified day and month
    sql_statement = 'SELECT * FROM task WHERE MONTH(Deadline)=%s AND DAY(Deadline)=%s;'
    month_date = (month, day)
    create_cursor.execute(sql_statement, month_date)
    #format
    specified_rows = create_cursor.fetchall()

    if(len(specified_rows)==0):
        print("There are no tasks for that date.")
        return
    # prints values in specified_rows
    date = (month, day)
    print("===============================")
    print("TASKS DUE ON %s / %s:" % date)
    print("===============================")

    for x in specified_rows:
        print("ඞ Task id:\t\t" + str(x[0]))
        print("ඞ Task name:\t\t" + x[1])
        print("ඞ Task description:\t" + x[2])
        print("ඞ Date posted:\t\t" + str(x[3]))
        print("ඞ Deadline:\t\t" + str(x[4]))
        print("ඞ Status:\t\t" + x[5])
        print("ඞ Category:\t\t" + str(x[6]))
        print()

def checkCategoryStatus():
    # function that updates the status of categories whose tasks under it have Accomplished or Accomplished late as status to Done
    create_cursor.execute("SELECT Category_id FROM category")
    data = create_cursor.fetchall()
    for x in data:
        categoryID = x[0]
        # if(categoryID!=999):
        create_cursor.execute("SELECT Task_id FROM task WHERE Status NOT IN (\"Accomplished\", \"Accomplished Late\") AND Category_id = %s;" % str(categoryID))
        numTask = create_cursor.fetchall()
        # if the number of tasks under the category in specified index is equal to zero, then update the status to Done else, Not Yet Done
        if(len(numTask)==0):
            create_cursor.execute("UPDATE category SET Status=\"Done\" WHERE Category_id=%s;" % str(categoryID))    
            mariadb_connection.commit()
        else:
            create_cursor.execute("UPDATE category SET Status=\"Not Yet Done\" WHERE Category_id=%s;" % str(categoryID))    
            mariadb_connection.commit()

def markLateTasks():
    # query that updates the status of tasks that has exceeded deadline and not yet marked as done to Missing
    create_cursor.execute("UPDATE task SET Status = \"Missing\" WHERE DATEDIFF(CURDATE(), Deadline) > 0 AND Status NOT IN (\"Accomplished\", \"Accomplished Late\");")    
    mariadb_connection.commit()

############################################### Main Menu ################################################
markLateTasks()
while True:
    checkCategoryStatus()
    menu = """======================== M E N U =======================
 [0] Add Task \t\t [6] Edit Category
 [1] Edit Task \t\t [7] Delete Category
 [2] Delete Task \t [8] View Category
 [3] View Task \t\t [9] View Tasks Under Category
 [4] Mark Task as Done \t [10] Insert Task to Category
 [5] Add Category \t [11] View Task per day, month
 [12] Exit
========================================================"""
    print(menu)
    userInput = int(input("Choice: "))
    if(userInput == 0):
        addTask()
    elif(userInput == 1):
        editTask()
    elif(userInput == 2):
        deleteTask()
    elif(userInput == 3):
        viewTask()
    elif(userInput == 4):
        markTaskAsDone()
    elif(userInput == 5):
        addCategory()
    elif(userInput == 6):
        editCategory()
    elif(userInput == 7):
        deleteCategory()
    elif(userInput == 8):
        viewCategory()
    elif(userInput == 9):
        viewCategoryTasks()
    elif(userInput == 10):
        addTaskCategory()
    elif(userInput == 11):
        viewTaskSpecificDate()
    elif(userInput == 12):
        #exit program
        print("Goodbye")
        break
    else:
        print("Invalid Choice. Enter Again.")

#close the connection
mariadb_connection.close()
