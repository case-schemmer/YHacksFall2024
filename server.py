from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import os

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app)


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'



@app.route('/add', methods=['GET'])
def handle_get():
    tmp = os.popen("wolframscript -file rolldice.wls").read()
    print(tmp)
    return tmp



# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()