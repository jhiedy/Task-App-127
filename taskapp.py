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
    # taskID = int(input("Please input a 2 digit task id: "))
    create_cursor.execute("SELECT Task_id FROM task")
    data = create_cursor.fetchall()
    
    taskID = randint(10, 99)
    taskIDs = []
    for x in data:
        taskIDs.append(x[0])
    
    if(len(taskIDs)==90):
        print("Database is full.")
        return

    while(taskID in taskIDs):
        taskID = randint(10,99)

    taskName = str(input("Please input the name of the task: "))
    taskDesc = str(input("Please input description of the task: "))
    taskDeadline = str(input("Please input the deadline of the task (YYYY-MM-DD): "))

    the_command = "INSERT INTO task VALUES (" + str(taskID) + ", \"" + taskName + "\", \"" + taskDesc + "\" , CURDATE(), STR_TO_DATE(\"" + taskDeadline + "\" , \"%Y-%m-%d\"), \"Ongoing\", 999)"

    create_cursor.execute(the_command)
    mariadb_connection.commit()
    print("Task added successfully.")

def viewSpecificTask(taskID):
    create_cursor.execute("SELECT * FROM task WHERE Task_id = %s" % str(taskID))
    data = create_cursor.fetchall()

    for x in data:
        print("Task id:\t\t" + str(x[0]))
        print("Task name:\t\t" + x[1])
        print("Task description:\t" + x[2])
        print("Date posted:\t\t" + str(x[3]))
        print("Deadline:\t\t" + str(x[4]))
        print("Status:\t\t\t" + x[5])
        #Category id for now
        print("Category:\t\t" + str(x[6]))
        print()
    

def editTask():
    create_cursor.execute("SELECT Task_id FROM task")
    data = create_cursor.fetchall()
    
    taskIDs = []
    for x in data:
        taskIDs.append(x[0])
    
    if(len(taskIDs)==0):
        print("There is no data in the database.")
        return
    
    taskID = int(input("Please input the task id to be edited: "))

    if(taskID in taskIDs):
        while(True):
            print("==============================")
            viewSpecificTask(taskID)
            print("==============================")
            print("[1] Change Name")
            print("[2] Change Description")
            print("[3] Change Deadline")
            print("[0] Exit Edit Menu")
            
            userInput = str(input("Choice: "))

            if(userInput == "1"):
                taskName = str(input("Please input the new name of the task: "))
                command = ("UPDATE task SET Name = \"%s\" WHERE Task_id = %s" % (taskName, str(taskID)))
                create_cursor.execute(command)
                mariadb_connection.commit()
            elif(userInput == "2"):
                taskDesc = str(input("Please input the new description of the task: "))
                command = ("UPDATE task SET Description = \"%s\" WHERE Task_id = %s" % (taskDesc, str(taskID)))
                create_cursor.execute(command)
                mariadb_connection.commit()
            elif(userInput == "3"):
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
    create_cursor.execute("SELECT Task_id FROM task")
    data = create_cursor.fetchall()
    
    taskIDs = []
    for x in data:
        taskIDs.append(x[0])

    if(len(taskIDs)==0):
        print("There is no data in the database.")
        return

    taskID = int(input("Please input the task id to be deleted: "))

    if(taskID in taskIDs):
        #DELETE FROM task WHERE Task_id = <Task_id>;

        the_command = "DELETE FROM task WHERE Task_id = " + str(taskID)
    
        create_cursor.execute(the_command)
        mariadb_connection.commit()
    else:
        print("The Task id you inputted is not in the database.")
def viewTask():
    create_cursor.execute("SELECT Task_id FROM task")
    data = create_cursor.fetchall()
    
    taskIDs = []
    for x in data:
        taskIDs.append(x[0])

    if(len(taskIDs)==0):
        print("There is no data in the database.")
        return
    
    create_cursor.execute("SELECT * FROM task ORDER BY Deadline ASC")
    data = create_cursor.fetchall()

    for x in data:
        print("Task id:\t\t" + str(x[0]))
        print("Task name:\t\t" + x[1])
        print("Task description:\t" + x[2])
        print("Date posted:\t\t" + str(x[3]))
        print("Deadline:\t\t" + str(x[4]))
        print("Status:\t\t\t" + x[5])
        #Category id for now
        print("Category:\t\t" + str(x[6]))
        print()

def markTaskAsDone():
    id = int(input("Enter ID of task to mark as done: "))
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
    
    if(id in taskIDs):
        sql_statement = 'UPDATE task SET Status = CASE WHEN DATEDIFF(CURDATE(), Deadline)>0 THEN %s ELSE %s END WHERE Task_id=%s;'
        to_update = (late, acc, id)
        create_cursor.execute(sql_statement, to_update)
        mariadb_connection.commit()
        print("Task %s is Marked as DONE." % id)
    else:
        print("Task not found in the database.")

def addCategory():
    id = randint(100,999)
    name = input("Enter name of new Category: ")
    defaultStatus = "Not Yet Done"
    sql_statement = 'INSERT INTO category VALUES (%s, %s, %s);'
    to_insert = (id, name, defaultStatus)
    create_cursor.execute(sql_statement, to_insert)
    mariadb_connection.commit()
    print("Category %s Added!\n" % name)

def editCategory():
    create_cursor.execute("SELECT Category_id FROM category")
    data = create_cursor.fetchall()
    categoryIDs = []
    for x in data:
        categoryIDs.append(x[0])
    if(len(categoryIDs)==0):
        print("There is no data in the database.")
        return

    id = int(input("Enter ID of category to be edited: ") )
    
    if(id in categoryIDs):
        newCategName = input("Enter New Name for Category %s: " % str(id)) 
        sql_statement = 'UPDATE category SET Name=%s WHERE Category_id=%s;'
        to_update = (newCategName, id)
        create_cursor.execute(sql_statement, to_update)
        mariadb_connection.commit()
        print("Category %s Edited!\n" % id)
    else:
        print("Category not found in database.")

def deleteCategory():
    create_cursor.execute("SELECT Category_id FROM category")
    data = create_cursor.fetchall()
    categoryIDs = []
    for x in data:
        categoryIDs.append(x[0])
    if(len(categoryIDs)==0):
        print("There is no data in the database.")
        return
    
    id = int(input("Enter ID of category to be deleted: "))
    
    if(id in categoryIDs):
        sql_statement = 'DELETE FROM category WHERE Category_id=%s;'
        to_delete = (id)
        create_cursor.execute(sql_statement, (to_delete,))
        mariadb_connection.commit()
        sql_statement = 'UPDATE task SET Category_id=999 WHERE Category_id=%s;'
        to_update = (id)
        create_cursor.execute(sql_statement, (to_update,))
        mariadb_connection.commit()
        print("Successfully deleted category %s.\n" % id)
    else:
        print("Category not found in database")

def viewCategory():
    sql_statement = 'SELECT * FROM category;'
    create_cursor.execute(sql_statement)
    category = create_cursor.fetchall()

    print("======= C A T E G O R Y =======")
    for x in category:
        print("● Category id:\t\t" + str(x[0]))
        print("● Category name:\t" + x[1])
        print("● Status:\t\t" + x[2] + "\n")   

def viewCategoryTasks():
    create_cursor.execute("SELECT Category_id FROM category WHERE Category_id != 999")
    data = create_cursor.fetchall()
    categoryIDs = []

    for x in data:
        categoryIDs.append(x[0])

    if(len(categoryIDs)==0):
        print("There are no categories in the database.")
        return
    
    id = input("Enter ID of the category to view: ")

    if(id=="999"):
        print("You cannot edit the default category.")
        return

    if(id not in categoryIDs):
        print("The Category ID does not exist.")
        return

    sql_statement = 'SELECT * FROM task WHERE Category_id=%s;'
    to_view = (id)
    create_cursor.execute(sql_statement, (to_view,))
    task_rows = create_cursor.fetchall()
    
    if(len(task_rows)==0):
        print("There are no tasks in this category.")
        return

    print("======= T A S K S =======")
    for x in task_rows:
        print("■ Task id:\t\t" + str(x[0]))
        print("■ Task name:\t\t" + x[1])
        print("■ Task description:\t" + x[2])
        print("■ Date posted:\t\t" + str(x[3]))
        print("■ Deadline:\t\t" + str(x[4]))
        print("■ Status:\t\t" + x[5])
        #Category id for now
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

    id1 = int(input("Enter ID of category: "))
    id2 = int(input("Enter ID of task to be put in the category: "))
    if((id2 in taskIDs) and (id1 in categoryIDs)):
        sql_statement = 'UPDATE task SET Category_id=%s WHERE Task_id=%s;'
        to_add = (id1, id2)
        create_cursor.execute(sql_statement, to_add)
        mariadb_connection.commit()
        print("Task successfully added to Category %s!" % id1)
    else:
        print("Task/Category ID not found.")

def viewTaskSpecificDate():
    month = input("Enter the month you want to check (MM): ")
    day = input("Enter the day you want to check (DD): ")

    sql_statement = 'SELECT * FROM task WHERE MONTH(Deadline)=%s AND DAY(Deadline)=%s;'
    month_date = (month, day)
    create_cursor.execute(sql_statement, month_date)
    #format
    specified_rows = create_cursor.fetchall()

    if(len(specified_rows)==0):
        print("There are no tasks for that date.")
        return

    date = (month, day)
    print("===============================")
    print("TASKS DUE ON %s / %s:" % date)
    print("===============================")

    for x in specified_rows:
        print("Task id:\t\t" + str(x[0]))
        print("Task name:\t\t" + x[1])
        print("Task description:\t" + x[2])
        print("Date posted:\t\t" + str(x[3]))
        print("Deadline:\t\t" + str(x[4]))
        print("Status:\t\t\t" + x[5])
        #Category id for now
        print("Category:\t\t" + str(x[6]))
        print()

def checkCategoryStatus():
    create_cursor.execute("SELECT Category_id FROM category WHERE Status = \"Not Yet Done\"")
    data = create_cursor.fetchall()

    for x in data:
        categoryID = x[0]
        # if(categoryID!=999):
        create_cursor.execute("SELECT Task_id FROM task WHERE Status NOT IN (\"Accomplished\", \"Accomplished Late\") AND Category_id = %s;" % str(categoryID))
        numTask = create_cursor.fetchall()
        if(len(numTask)==0):
            create_cursor.execute("UPDATE category SET Status=\"Done\" WHERE Category_id=%s;" % str(categoryID))    
            mariadb_connection.commit()
        else:
            create_cursor.execute("UPDATE category SET Status=\"Not Yet Done\" WHERE Category_id=%s;" % str(categoryID))    
            mariadb_connection.commit()


    
def markLateTasks():
    create_cursor.execute("UPDATE task SET Status = \"Missing\" WHERE DATEDIFF(CURDATE(), Deadline) > 0 AND Status NOT IN (\"Accomplished\", \"Accomplished Late\");")    
    mariadb_connection.commit()
    print("Update status of tasks that exceeded deadline")

############################################### Main Menu ################################################
markLateTasks()
while True:
    menu = """======================== M E N U =======================
 [0] Add Task \t\t [6] Edit Category
 [1] Edit Task \t\t [7] Delete Category
 [2] Delete Task \t [8] View Category
 [3] View Task \t\t [9] View Tasks Under Category
 [4] Mark Task as Done \t [10] Insert Task to Category
 [5] Add Category \t [11] View Task per day, month
 [12] Exit
========================================================"""
    checkCategoryStatus()
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
