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
mariadb_connection = mariadb.connect(user='test', password='password', host = 'localhost', database = 'taskapp')
create_cursor = mariadb_connection.cursor()

#Function declarations
def addTask():
    taskID = int(input("Please input a 2 digit task id: "))
    taskName = str(input("Please input the name of the task: "))
    taskDesc = str(input("Please input description of the task: "))
    taskDeadline = str(input("Please input the deadline of the task (YYYY-MM-DD): "))

    the_command = "INSERT INTO task VALUES (" + str(taskID) + ", \"" + taskName + "\", \"" + taskDesc + "\" , CURDATE(), STR_TO_DATE(\"" + taskDeadline + "\" , \"%Y-%m-%d\"), \"Ongoing\", 999)"

    create_cursor.execute(the_command)
    mariadb_connection.commit()
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
        taskName = str(input("Please input the new name of the task: "))
        taskDesc = str(input("Please input the new description of the task: "))
        taskDeadline = str(input("Please input the new deadline of the task (YYYY-MM-DD): "))
        # UPDATE task SET Name=<Name>, Description=<Description>, Deadline=STR_TO_DATE(<Deadline>, “%Y-%m-%d”) WHERE Task_id = <Task_id>;

        the_command = "UPDATE task SET Name=\"" + taskName + "\", Description=\"" + taskDesc + "\", Deadline=STR_TO_DATE(\"" + taskDeadline + "\", \"%Y-%m-%d\") WHERE Task_id = " + str(taskID)
        create_cursor.execute(the_command)
        mariadb_connection.commit()
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
    
    create_cursor.execute("SELECT * FROM task")
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

def markTaskAsDone(id):
    late = "Accomplished Late"
    acc = "Accomplished"
    sql_statement = 'UPDATE task SET Status = CASE WHEN DATEDIFF(CURDATE(), Deadline)<0 THEN %s ELSE %s END WHERE Task_id=%s;'
    to_update = (late, acc, id)
    create_cursor.execute(sql_statement, to_update)
    mariadb_connection.commit()
    print("Task %s is Marked as DONE." % id)

def addCategory(id, name):
    defaultStatus = "Not Yet Done"
    sql_statement = 'INSERT INTO category VALUES (%s, %s, %s);'
    to_insert = (id, name, defaultStatus)
    create_cursor.execute(sql_statement, to_insert)
    mariadb_connection.commit()
    print("Category %s Added!\n" % name)

def editCategory(id,name):
    sql_statement = 'UPDATE category SET Name=%s WHERE Category_id=%s;'
    to_update = (newCategName, id)
    create_cursor.execute(sql_statement, to_update)
    mariadb_connection.commit()
    print("Category %s Edited!\n" % name)

def deleteCategory(id):
    sql_statement = 'DELETE FROM category WHERE Category_id=%s;'
    to_delete = (id)
    create_cursor.execute(sql_statement, (to_delete,))
    mariadb_connection.commit()
    sql_statement = 'UPDATE task SET Category_id=999 WHERE Category_id=%s;'
    to_update = (id)
    create_cursor.execute(sql_statement, (to_update,))
    mariadb_connection.commit()
    print("Goodbye Category %s.\n" % id)

def viewCategory():
    sql_statement = 'SELECT * FROM category;'
    create_cursor.execute(sql_statement)
    category = create_cursor.fetchall()
    print("=======C A T E G O R Y=======\n")
    for x in category:
        print("● Category id:\t\t" + str(x[0]))
        print("● Category name:\t" + x[1])
        print("● Status:\t\t" + x[2] + "\n")   

def viewCategoryTasks(id):
    sql_statement = 'SELECT * FROM task WHERE Category_id=%s;'
    to_view = (id)
    create_cursor.execute(sql_statement, (to_view,))
    task_rows = create_cursor.fetchall()
    print("=======T A S K S=======\n")
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

def addTaskCategory(id1, id2):
    sql_statement = 'UPDATE task SET Category_id=%s WHERE Task_id=%s;'
    to_add = (id1, id2)
    create_cursor.execute(sql_statement, to_add)
    mariadb_connection.commit()
    print("Task successfully added to Category %s !" % id1)

def viewTaskSpecificDate(month, day):
    sql_statement = 'SELECT * FROM task WHERE MONTH(Deadline)=%s AND DAY(Deadline)=%s;'
    month_date = (month, day)
    create_cursor.execute(sql_statement, month_date)
    #format
    specified_rows = create_cursor.fetchall()
    date = (month, day)
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

while True:
    menu = """============ M E N U ============
 [0] Add Task \t\t [6] Edit Category \n [1] Edit Task \t\t [7] Delete Category \n [2] Delete Task \t [8] View Category \n [3] View Task \t\t [9] View Tasks Under Category \n [4] Mark Task as Done \t [10] Insert Task to Category \n [5] Add Category \t [11] View Task per day, month  \n [12] Exit
================================="""
    # check when all tasks under category are accomplished then update category status
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
        idInput = input("Enter ID of task to mark as done: ")
        markTaskAsDone(idInput)
    elif(userInput == 5):
        genCategoryId = randint(100,999)
        categoryName = input("Enter name of new Category: ")
        addCategory(genCategoryId, categoryName)
    elif(userInput == 6):
        categoryChoice = input("Enter ID of category to be edited: ")
        newCategName = input("Enter New Name for Category %d: " % categoryChoice)  
        editCategory(categoryChoice, newCategName)
    elif(userInput == 7):
        categoryChoice = input("Enter ID of category to be deleted: ")
        deleteCategory(categoryChoice)
    elif(userInput == 8):
        viewCategory()
    elif(userInput == 9):
        categoryChoice = input("Enter ID of the category to view: ")
        viewCategoryTasks(categoryChoice)
    elif(userInput == 10):
        categoryChoice = input("Enter ID of category to be edited: ")
        taskChoice = input("Enter ID of task to be put in the category: ")
        addTaskCategory(categoryChoice, taskChoice)
    elif(userInput == 11):
        monthChoice = input("Enter the month you want to check: ")
        dayChoice = input("Enter the day you want to check: ")
        viewTaskSpecificDate(monthChoice, dayChoice)
    elif(userInput == 12):
        #exit program
        print("Goodbye")
        break
    else:
        print("Invalid Choice. Enter Again.")

#close the connection
mariadb_connection.close()
