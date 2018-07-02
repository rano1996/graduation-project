
# coding: utf-8

# In[6]:


import librosa
import numpy as np
import pickle
import os
import glob


# In[7]:



def extract_features(file_name):
    print("hello")
    features, labels, name = np.empty((0,161)), np.empty(0), np.empty(0)
    X, sample_rate = librosa.load(file_name)
    #X=np.float(np.array(file_name))
    sample_rate=44100
    stft = np.abs(librosa.stft(X))
    mfccs = np.array(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=8).T)
    mfccs = np.array(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=8).T)
    chroma = np.array(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T)
    mel = np.array(librosa.feature.melspectrogram(X, sr=sample_rate).T)
    contrast = np.array(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T)
    tonnetz = np.array(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T)
    ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
    features = np.vstack([features,ext_features])
    return features


# In[4]:


def get_model_api():
    """Returns lambda function for api"""
    # 1. initialize model once and for all and reload weights
    print("load model")  
    with open('res_model.pkl', 'rb') as fin:
        sc, clf = pickle.load(fin)


    def model_api(input_data):
        print("hello from model_api")
        # 2. process input with simple tokenization and no punctuation
        new_samples = extract_features(input_data)
        #print(new_samples.shape)
        X_new = sc.transform(new_samples)
        # 3. call model predict function
        X_new_preds = clf.predict(X_new)
        # 4. process the output
        # 5. return the output for the api
    
        return X_new_preds
    return model_api


# In[8]:


print("load model")  
with open('res_model.pkl', 'rb') as fin:
    sc, clf = pickle.load(fin)


# In[10]:


def model_api(input_data):
    print("hello from model_api")
    # 2. process input with simple tokenization and no punctuation
    new_samples = extract_features(input_data)
    #print(new_samples.shape)
    X_new = sc.transform(new_samples)
    # 3. call model predict function
    X_new_preds = clf.predict(X_new)
    # 4. process the output
    # 5. return the output for the api
    
    return X_new_preds

