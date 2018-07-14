
# coding: utf-8

# In[1]:


import os
import sys
import json
import warnings
import argparse

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
from dejavu.recognize import MicrophoneRecognizer
from argparse import RawTextHelpFormatter


# In[2]:


config = {
     "database": {
         "host": "127.0.0.1",
         "user": "root",
         "passwd": "",
         "db": "dejavu"
     }
 }


# In[3]:


djv = Dejavu(config)


# In[4]:


djv.fingerprint_directory("C:/Users/rano4/Desktop/dejavu-master/dejavu-master/mp3/", [".mp3"], 3)

