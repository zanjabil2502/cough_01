# -*- coding: utf-8 -*-
"""text_model_public.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RaitRVjdZ0XpBmJV44uDERng6kac2VlN

# Text Model

Importing libraries and train data from google drive
"""

import pandas as pd
import pickle
import numpy as np
import urllib.request

from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report,confusion_matrix, plot_confusion_matrix
from imblearn.over_sampling import *

urllib.request.urlretrieve("https://raw.githubusercontent.com/virufy/covid/master/data/labels.csv", "labels.csv")
urllib.request.urlretrieve("https://raw.githubusercontent.com/virufy/covid/master/data/crowdsource.csv", "crowdsource.csv")

"""## **Main class**"""

class Text():
  """
  This is a class for training , preprcoessing data and testing the text model data using testData provided
  """

  def __init__(self, model_file = None):
    if model_file:
      self.model = pickle.load(open(model_file, 'rb'))


  def preprocess(csv_file, mode=None):
    if mode=="crowdsource":
      return Text.preprocess_crowdsource(csv_file)

    elif mode=="clinical":
      return Text.preprocess_clinical(csv_file)

    else:
      return Text.preprocess_none(csv_file)

  def preprocess_none(csv_file):
      df = pd.read_csv(csv_file)
      y = df["corona_test"] 
      x = df.drop(columns = ["corona_test"])
      return x,y

  def preprocess_crowdsource(in_file):
    labels_df = pd.read_csv(in_file)
    
    try:
      labels_df = labels_df.drop(columns=["cough_audio", "breath_audio", "consent", "test", "id", "email", "userid", "medical_history9", "reported_symptoms12", "country", "dt", "count_audio"])
    except:
      pass

    symptom_list = list(filter(lambda column : "symptoms" in column, list(labels_df.columns)))
    medical_history = list(filter(lambda column : "history" in column, list(labels_df.columns)))


    labels_df[symptom_list] = labels_df[symptom_list].fillna(0)
    labels_df[medical_history] = labels_df[medical_history].fillna(0)

    for column in medical_history:
      labels_df[column] = pd.to_numeric(labels_df[column], errors='coerce').fillna(1, downcast='infer')

    for column in symptom_list:
      labels_df[column] = pd.to_numeric(labels_df[column], errors='coerce').fillna(1, downcast='infer')

    labels_df["age"] = pd.to_numeric(labels_df["age"], errors='coerce').dropna()


    labels_df = labels_df[labels_df.condition != "pending"]


    labels_df.dropna(subset = ["condition","gender", "age"] , inplace=True)


    labels_df['condition'] = LabelEncoder().fit_transform(labels_df['condition'])
    labels_df['gender'] = LabelEncoder().fit_transform(labels_df['gender'])
    labels_df['smoker'] = LabelEncoder().fit_transform(labels_df['gender'])
    

    target_labels = labels_df["condition"] 
    newdf = labels_df.drop(columns = ["condition"])
    newdf = labels_df.drop(columns = ["reported_symptoms11"], errors="ignore")

    newdf['medical_history1'] = 0
    newdf['reported_symptoms6'] = 0

    newdf.sort_index(axis=1, inplace=True)

    newdf.to_csv("crowdsource.csv")

    return newdf, target_labels


  def preprocess_clinical(in_file):
    labels_f = in_file
    labels_df = pd.read_csv(labels_f)
    #dropping the columns unrealted to the text model
    try:
      labels_df = labels_df.drop(columns=["date", "cough_filename"])
    except:
      pass

    #removing the columns which does not contain the information on covid tests
    labels_df["corona_test"].fillna("None", inplace = True) 
    labels_df = labels_df.drop(labels_df[labels_df.corona_test == "None"].index)

    #replacing the empty values with None
    labels_df ["smoker"].fillna("None", inplace = True) 
    labels_df ["patient_reported_symptoms"].fillna("None", inplace = True)
    labels_df ['age'].fillna("None", inplace = True)
    labels_df ['gender'].fillna("None", inplace = True)
    labels_df ['medical_history'].fillna("None", inplace = True)
    labels_df.dropna()

    #CORONA_TEST
    newdf= labels_df.replace(to_replace ="negative", 
                    value =0)
    newdf = newdf.replace(to_replace ="positive", 
                    value =1)
    newdf= newdf.replace(to_replace ="FALSE", 
                    value =0)
    newdf = newdf.replace(to_replace ="TRUE", 
                    value =1)

    #AGE
    newdf['age'] = LabelEncoder().fit_transform(newdf['age'])

    #Gender
    newdf['gender'] = newdf['gender'].str.lower()
    newdf['gender'] = LabelEncoder().fit_transform(newdf['gender'])

    #medical_history
    newdf["medical_history"] = newdf["medical_history"].str.lower()
    med_history = ['None,', 'congestive heart failure,','disease or conditions that make it harder to cough,', \
                        'asthma or chronic lung disease,','pregnancy,', 'diabetes with complications,']
        
    for mh in med_history:
        newdf[mh] = newdf.medical_history.str.contains(mh).astype(int)
        newdf["medical_history"] = newdf.medical_history.str.replace(mh+ ",", "")

    newdf = newdf.drop(columns = ["medical_history"])

    #smoker
    newdf['smoker'] = LabelEncoder().fit_transform(newdf['smoker'])

    #symptoms
    newdf['patient_reported_symptoms'] = newdf['patient_reported_symptoms'].str.lower()

    symptoms = ['fever, chills, or sweating,', 'shortness of breath,', \
                      'new or worsening cough,','sore throat,', 'body aches,', \
                      'loss of taste,', 'loss of smell,', 'none,']
    for ps in symptoms:
        newdf[ps] = newdf.patient_reported_symptoms.str.contains(ps).astype(int)
        newdf["patient_reported_symptoms"] = newdf.patient_reported_symptoms.str.replace(ps+ ",", "")

    newdf = newdf.drop(columns = ["patient_reported_symptoms"])

    target_labels = newdf["corona_test"] 
    newdf = newdf.drop(columns = ["corona_test"])

    newdf.drop(newdf.columns[newdf.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

    newdf.rename(columns={"congestive heart failure,": "medical_history5",
                          "disease or conditions that make it harder to cough," : "medical_history4",
                          "asthma or chronic lung disease,": "medical_history1", 
                          'pregnancy,': "medical_history2",
                          'diabetes with complications,': "medical_history3",
                          'fever, chills, or sweating,': "reported_symptoms3",
                          'shortness of breath,': "reported_symptoms2",
                          'new or worsening cough,': "reported_symptoms1",
                          'sore throat,': "reported_symptoms4",
                          'body aches,': "reported_symptoms5",
                          'loss of taste,': "reported_symptoms6",
                          'loss of smell,': "reported_symptoms7"}, inplace=True)
    
    newdf['medical_history7'] = 0
    newdf['medical_history8'] = 0
    newdf['reported_symptoms8'] = 0
    newdf['reported_symptoms9'] = 0
    newdf['reported_symptoms10'] = 0

    newdf.drop(columns=["None,","none,"], inplace=True) 

    newdf.sort_index(axis=1, inplace=True)
    
    newdf.to_csv("clinical_preprocessed.csv")
    
    return newdf, target_labels

  def split(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=True)

    return x_train, y_train, x_test, y_test


  def train(self, x_train_orig, y_train_orig, save_path='model.sav'):

    """
    Trains the text model using the trainData 
    Returns:
      a string containing saved model of form .sav
    """
    try:
      x_train, y_train = SMOTE(sampling_strategy='minority').fit_resample(x_train_orig, y_train_orig)
    except:
      x_train, y_train = RandomOverSampler(sampling_strategy='minority').fit_resample(x_train_orig, y_train_orig)

    clf = SVC(kernel = "linear",C=1, degree = 2, gamma=0.001,random_state=0)
    clf.fit(x_train,y_train)

    print("\nTraining:")
    print("Accuracy: ",end="")
    pred = clf.predict(x_train_orig)
    accuracy = accuracy_score(y_train_orig, pred)
    print(accuracy)
    conf_mat = confusion_matrix(y_train_orig, pred)
    print(conf_mat)

    self.model = clf
    pickle.dump(clf, open(save_path, 'wb'))
  

  def predict(self, x_test, y_test):
    """
    Predict for covid positive or negative using the saved model 
    Returns: 
      bool value depecting positive and negative covid results 
    """
    
    pred = self.model.predict(x_test)
    print(pred)
    accuracy = accuracy_score(y_test,pred)
    print("Accuracy on test dataset : ", accuracy)
    conf_mat = confusion_matrix(y_test,pred)
    print("Confusion matrix :\n", conf_mat)
    print("Classification report \n", classification_report(y_test, pred))
    
    return pred

"""## Run the Model

### Clinical Data
"""

filename = "labels.csv"
if __name__ == "__main__":
  text = Text()
  x, y = Text.preprocess(csv_file=filename, mode="clinical")
  x_train, y_train, x_test, y_test = Text.split(x, y)

  text.train(x_train, y_train, "text-model.sav")
  prediction = text.predict(x_test, y_test)



"""### Crowdsourced Data"""

filename = "crowdsource.csv"
if __name__ == "__main__":
  text = Text()
  x, y = Text.preprocess(csv_file=filename, mode="crowdsource")
  x_train, y_train, x_test, y_test = Text.split(x, y)

  text.train(x_train, y_train, "text-model.sav")
  prediction = text.predict(x_test, y_test)