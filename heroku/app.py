
# coding: utf-8

# In[2]:


from flask import Flask, request, jsonify
from flask_cors import CORS
from serve import get_model_api  # see part 1.
import os
from werkzeug import secure_filename
import sys
import json
import warnings
import argparse
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
from argparse import RawTextHelpFormatter
from os.path import join, dirname, realpath

# In[3]:


import numpy as np
import scipy.io.wavfile as wav
import json
#configuration of connecting to database
config = {
     "database": {
         "host": "127.0.0.1",
         "user": "root",
         "passwd": "",
         "db": "dejavu"
     },
     "fingerprint_limit" : 35
 }
#conecting to database 
djv = Dejavu(config)


# In[8]:


class NumPyArangeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist() # or map(int, obj)
        return json.JSONEncoder.default(self, obj)


# In[6]:


#UPLOAD_FOLDER='C:/Users/acer/Desktop/app/'
UPLOAD_FOLDER='uploads/'
ALLOWED_EXTENSIONS = set(['wav'])
print("end of import")
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app) # needed for cross-domain requests, allow everything by default
model_api = get_model_api()
# default route
@app.route('/')
def index():
    return "Index API"

# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404

@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

@app.route('/add', methods=['POST','GET'])
def add():
    
    if request.method == 'POST':
        upload_file = request.files['file']
        filename = secure_filename(upload_file.filename)
        print("print fiile name ")
        new_file = UPLOAD_FOLDER+filename
        print(new_file)
        upload_file.save(join(dirname(realpath(__file__)),new_file))
        djv.fingerprint_directory((join(dirname(realpath(__file__)),UPLOAD_FOLDER)), [".wav"], 3)
    return "Done"
print("end of define default route ")

# API route
@app.route('/api', methods=['POST','GET'])
def api():
    
    if request.method == 'POST':
        #upload_file = request.files['file']
        #filename = secure_filename(upload_file.filename)
        #print(filename)
        #upload_file.save(os.path.join(UPLOAD_FOLDER, filename))

        upload_file = request.files['file']
        filename = secure_filename(upload_file.filename)
        print("print fiile name ")
        new_file = UPLOAD_FOLDER+filename
        print(new_file)
        upload_file.save(join(dirname(realpath(__file__)),new_file))
        #input_data = request.json
        #print(input_data)
        #app.logger.info("api_input: " + str(filename))
        output_data = model_api(join(dirname(realpath(__file__)),os.path.join(UPLOAD_FOLDER, filename)))
        song = djv.recognize(FileRecognizer,(join(dirname(realpath(__file__)),os.path.join(UPLOAD_FOLDER, filename) )))
        print(song)
        print("the out")
        print(output_data)
        app.logger.info("api_output: " + str(output_data))
        response = jsonify(str(output_data))
        out={
            "classification": json.dumps(output_data, cls=NumPyArangeEncoder),
            "fingerprint": json.dumps(song, cls=NumPyArangeEncoder)
        }
        return jsonify(out)
    return  '''
    <!doctype html>
    <html lang="en">
    <head>
      <title>Running my first AI Demo</title>
    </head>
    <body>
    <div class="site-wrapper">
        <div class="cover-container">
            <nav id="main">
                <a href="http://localhost:5000/demo" >HOME</a>
            </nav>
          <div class="inner cover">
          </div>
          <div class="mastfoot">
          <hr />
            <div class="container">
              <div style="margin-top:5%">
                    <h1 style="color:black">Sound Classification Demo</h1>
                    <h4 style="color:black">Upload new Sound </h4>
                    <form method=post enctype=multipart/form-data>
                     <p><input type=file name=file>
                    <input type=submit style="color:black;" value=Record>
                    </form>
                </div>
            </div>
            </div>
     </div>
   </div>
</body>
</html>
    '''

print("end of define main route ")

if __name__ == '__main__':
    app.run(host='192.168.1.170')
    #app.run( )

print("end")

