import pandas as pd
import nltk
from nltk.corpus import stopwords
from pyresparser import ResumeParser
from pickle import load
import re
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer


def concatenate_list_data(list):
          result= ''
          for element in list:
              result += str(element) + ','
          return result

def get_prediction(filename,details):
      
      name = 'Sample DE'
      data = ResumeParser(filename,skills_file='skills.csv').get_extracted_data()
      df = pd.DataFrame({'Skills':data.get("skills")})
      df['Email']=data.get("email")
      df['Contact_Number']=data.get("mobile_number")
      df['Name'] = name
      try:
        df['Experience']=data.get("total_experience")
      except:
        df['Experience'] = 0

      try:
        df['Education']=data.get("education")[0]
      except:
        df['Education'] = 'Did not catch that!'
      a=[]
      a = df["Skills"].tolist() 
      b=concatenate_list_data(a)
      df['Skills']=b
      df = df[["Name","Email","Contact_Number","Education","Experience","Skills"]]
      df = df.drop_duplicates()
      model=load(open('MB.pkl','rb'))
      wn = WordNetLemmatizer()
      corpus1 = []
      for i in range(len(df)):
          review=re.sub('[^a-zA-Z]',' ',str(df['Skills'][i]))
          review=review.lower()
          review=review.split()
          
          review=[wn.lemmatize(word) for word in review if not word in stopwords.words('english')]
          review=' '.join(review)
          corpus1.append(review)

      tf_fit=load(open('TF_FIT.pkl','rb'))
      X=tf_fit.transform(corpus1)
      pred = model.predict(X)
      df['Best_Suited_Role'] = pred
      df['Name']=details['name']
      df['Email']=details['email']
      df['Education']=details['edu']
      df['Contact_Number']=details['mobno']
      df['Experience']=details['expe']
      df=df.to_dict()
      return df
  
  
  
