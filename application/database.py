#intento: https://www.youtube.com/watch?v=byHcYRpMgI4
import sqlite3

conn = sqlite3.connect('customer.db')

#create a cursor
c = conn.cursor()

#create a table, this code is run only one time
#c.execute("""CREATE TABLE customers (
         #first_name text,
        # last_name text,
        # email text


 #   )""")

#insert data into the table
c.execute("INSERT INTO customers VALUES ('lilli','lee','lee@gmail.com')")



print ("executed succesfully")
#Commit the command
conn.commit()

#close the connection
conn.close()
