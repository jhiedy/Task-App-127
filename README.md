# Task-App-127
Final Project for CMSC 127

MODULES TO BE INSTALLED BEFORE USING THE APPLICATION

1. PIP for python
2. mysql-connector-python
3. python
4. mariadb

HOW TO RUN THE APPLICATION

1. Start the database (If you are using a wsl terminal) by using the code

    sudo service mysql start

2. Log in to mariadb as root, then source the task_record.sql dump file provided by using the code

    source task_record.sql

3. Create a new username "test" with password "password" by using the code

    CREATE USER test IDENTIFIED BY "password";

4. Grant all privileges for the user test in the task_record database by using the code

    GRANT ALL PRIVILEGES ON task_record.* TO test;

5. Then run the application by using the code

    python3 taskapp.py
