from application import app

if __name__ == '__main__': #this piece of code let us run with calling out "python xxx.py" in the terminal, instead of running with "flask run"
    #db.create_all() #database
    app.run( debug = True)
   #debug true help us refresh the code everytime we save changes.
    
