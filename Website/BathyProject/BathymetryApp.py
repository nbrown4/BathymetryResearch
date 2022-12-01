
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
 
from Website import create_app

app = create_app()

 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
    