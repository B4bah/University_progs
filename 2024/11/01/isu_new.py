import sqlite3

cursor = sqlite3.connect('E:\\pythonProject_Tests/University_progs/2024/11/01/isu_database.sqlite3').cursor()

for line in cursor.execute('SELECT password FROM isu_list'):
    print(line[0])
cursor.close()