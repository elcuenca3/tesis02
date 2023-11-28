import csv
import MySQLdb

mydb = MySQLdb.connect(host="127.0.0.1", user="root", password="", database="all db")

with open("cars.csv") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    all_value = []
    for row in csvreader:
        all_value.append((row[0], row[1], row[2]))

    query = "insert into tbl_cars (name, company, launch_year) values (%s, %s, %s)"

    mycursor = mydb.cursor()
    mycursor.executemany(query, all_value)

    mydb.commit()