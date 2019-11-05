import psycopg2


con = psycopg2.connect(database="postgres", user="postgres", password="rohtakhr", host="localhost", port="5432")
print("Database opened successfully")

db = con.cursor()
db.execute("CREATE TABLE books (bookid SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL,title VARCHAR NOT NULL,author VARCHAR NOT NULL,year VARCHAR NOT NULL)")
print("Table created successfully")


con.commit()
con.close()
