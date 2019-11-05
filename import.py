import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker # inroder to run scoped_session
# create in current folder where you project lies as .pylintrc and add 
#ignored-classes=SQLObject, Registrant, scoped_session
# this is VS code issue

if not os.getenv("DATABASE_URL"): # databaseurl is an environment variable
    #therefore, for now it is needed to be defined into the terminal window using the command
    # export DATABASE_URL=postgresql://postgres:rohtakhr@localhost:5432/postgres or 
    # any other url, above is ubuntu/bash command, for cmd replace export with set
    raise RuntimeError("DATABASE_URL is not set")

engine= create_engine(os.getenv("DATABASE_URL"))
db =scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader =csv.reader(f)
    for isbn,title,author,year in reader:
        if year == "year":
            print('skipped first line')
        else:    
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:a,:b,:c,:d)",{"a":isbn,"b":title,"c":author,"d":year})
        
    print("done")            
    db.commit()    







if __name__ == "__main__":
    main()
