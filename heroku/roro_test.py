
# coding: utf-8

# In[ ]:


#this is for Recognize a sound is previous exist 

import warnings
import json
warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer


# In[ ]:


config = {
     "database": {
         "host": "127.0.0.1",
         "user": "root",
         "passwd": "",
         "db": "dejavu"
     },
     "fingerprint_limit" : 35
 }


# In[ ]:


djv = Dejavu(config)


# In[ ]:


# Recognize audio from a file
song = djv.recognize(FileRecognizer,
      "C:\\Users\\ranop\\Desktop\\5thyear\\roro-dejavu-master_2\\roro-dejavu-master\\mp3\\211528.wav")
print ("From file we recognized: %s\n" % song)


# In[ ]:


#this is for Recognize a new sound and add it to database 
import os
import sys
import json
import warnings
import argparse


# In[ ]:


djv.fingerprint_directory("C:\\Users\\ranop\\Desktop\\5thyear\\roro-dejavu-master_2\\roro-dejavu-master\\mp3", [".mp3"], 3)


# In[ ]:


print (djv.db.get_num_fingerprints())

