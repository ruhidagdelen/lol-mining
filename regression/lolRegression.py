import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.model_selection import train_test_split
import seaborn as sns
from imblearn.over_sampling import SMOTE
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

data = pd.read_json('data/matches.json')

for i in range(9):
    daTemp = pd.read_json('data/matches%s.json'%str(i+2))
    data = data.append(daTemp)

# data = data['matches']
indices = ['assists','visionScore','timeCCingOthers','deaths','kills','longestTimeSpentLiving',
    'champLevel','totalHeal','totalDamageDealtToChampions','win']
df = pd.DataFrame(columns=indices)

for row in data['matches']:
    for participant in row['participants']:
        nero = {prop: participant['stats'][prop] for prop in indices}

        df=df.append(nero,ignore_index=True)

df = df.replace(True,1)
df = df.replace(False,0)

X = df.loc[:, df.columns != 'win']
y = df.loc[:, df.columns == 'win']

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_sample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns )
os_data_y= pd.DataFrame(data=os_data_y,columns=['win'])

print("length of oversampled data is ",len(os_data_X))
print("Number of no subscription in oversampled data",len(os_data_y[os_data_y['win']==0]))
print("Number of subscription",len(os_data_y[os_data_y['win']==1]))
print("Proportion of no subscription data in oversampled data is ",len(os_data_y[os_data_y['win']==0])/len(os_data_X))
print("Proportion of subscription data in oversampled data is ",len(os_data_y[os_data_y['win']==1])/len(os_data_X))

# data_final_vars=df.columns.values.tolist()
# y=['win']
# X=[i for i in data_final_vars if i not in y]
# from sklearn.feature_selection import RFE
# from sklearn.linear_model import LogisticRegression
# logreg = LogisticRegression()
# rfe = RFE(logreg, 20)
# rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
# print(rfe.support_)
# print(rfe.ranking_)

cols = ['assists','visionScore','timeCCingOthers','deaths','kills','longestTimeSpentLiving',
    'champLevel','totalHeal','totalDamageDealtToChampions']
X=os_data_X[cols]
y=os_data_y['win']

import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())

cols = ['assists','visionScore','timeCCingOthers','deaths','kills',
    'totalDamageDealtToChampions']

X=os_data_X[cols]
y=os_data_y['win']

logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())