#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import warnings 
warnings.filterwarnings('ignore')


# In[3]:


#View To The Existing Raw Data
data = pd.read_csv('playstore-analysis .csv')
data


# In[4]:


data.columns


# In[5]:


data.info()


# In[6]:


data.isnull().sum()


# In[7]:


### here  we are able to see null values in each column 


# In[8]:


data = data.dropna(subset=['Rating'], how  = 'all') # after looking a lot of value is null so we drops the null values record


# In[9]:


data["Rating"].isnull().sum()


# In[10]:


### i droped the record where  rating is missing since rating is our target/study variable


# ### Check the null values for the Android Ver column

# In[11]:


data.loc[data["Android Ver"].isnull()]


# In[12]:


### here i got the three record here  with NaN in the Android Ver column


# ### Are all 3 records having the same problem?

# In[13]:


### yes ,all the three column is having the same problem that is NaN values


# ### Drop the 3rd record i.e. record for “Life Made WIFI

# In[14]:


data.drop([10472] , inplace=True)


# In[15]:


data.loc[data["Android Ver"].isnull()]


# ###  Replace remaining missing values with the mode
# 

# In[16]:


data['Android Ver'].fillna(data['Android Ver'].mode()[0], inplace=True)


# In[17]:


data.loc[data["Android Ver"].isnull()]


# ### Current ver – replace with most common value

# In[18]:


data.loc[data["Current Ver"].isnull()]


# In[19]:


data['Current Ver'].fillna(data['Current Ver'].mode()[0], inplace=True)


# In[20]:


data.loc[data["Current Ver"].isnull()]


# ### TASK 2:  Data clean up – correcting the data types

# ###   Which all variables need to be brought to numeric types?
# 

# In[21]:


### there are few variable need be  bring /change the numerical variable if they are not in the Numerical type
#1. Size
#2.  Install
#3. Category _and Content Rating
#4. price


# ### Price variable  remove    doller sign and convert to float

# In[22]:


data["Price"].unique()


# In[23]:


### here we are able  to see that data type is object and  a  unwanted  symbol that is $ so i have to remove it  because it will creatye a  problem while  performing any operation.


# In[24]:


data['price']=data.Price.replace('Everyone',np.nan)
data['Price']=data.Price.str.replace('$',"").astype(float)
data['Price'].dtype


# ### Installs – remove ‘,’ and ‘+’ sign, convert to integer

# In[25]:


data["Installs"].unique()


# In[26]:


data['Installs'] = data.Installs.str.replace(",","")
data['Installs'] = data.Installs.str.replace("+","")
data['Installs'] = data.Installs.replace("Free",np.nan)
data['Installs'] = data['Installs'].astype(float)
data['Installs'].dtype


# ### Convert all other identified columns to numeric

# In[27]:


data["Reviews"]=data["Reviews"].astype(float)


# In[28]:


data["Reviews"]


# ### Sanity checks – check for the following and handle accordingly

# ####  Avg. rating should be between 1 and 5, as only these values are allowed on the play store.

# In[29]:


data.loc[data.Rating < 1] & data.loc[data.Rating > 5]


# ### Are there any such records? Drop if so.

# In[30]:


### here we get thet there is no vlaues  less than 1 and Greater than 5 so no need to drop anything


# ###  Reviews should not be more than installs as only those who installed can review the app.

# In[31]:


data.loc[data["Reviews"]>data["Installs"]]


# In[32]:


### here few values which is greater  reviews than installs 


# ### Are there any such records? Drop if so.

# In[33]:


temp = data[data['Reviews']>data['Installs']].index
data.drop(labels=temp, inplace=True)


# In[34]:


data.loc[data['Reviews'] > data['Installs']]


# ### 4: Identify and handle outliers 

# ###  Make suitable plot to identify outliers in price

# In[35]:


df=pd.DataFrame(data)


# In[36]:


sns.boxplot(df["Price"])


# In[37]:


data["Price"].describe()


# In[38]:


###  from the above visualization we are able to see that there  is a outerlier laying in the Price column


# ### Do you expect apps on the play store to cost 200Doller? Check out these cases

# In[39]:


data1=data.loc[data['Price'] > 200]
data1


# In[40]:


data1.count()


# In[41]:


# yes there  are 15 records in  the data  which cost more than 200 $ in the play store 


# In[42]:


data.drop(data[data['Price'] >200].index, inplace = True) 


# In[43]:


data1=data.loc[data['Price'] > 200]
data1


# In[44]:


sns.boxplot(data['Price'])


# ###  Limit data to records with price < $30
# 

# In[45]:


record_30 = data[data['Price'] > 30].index
data.drop(labels=record_30, inplace=True)


# In[46]:


plt.boxplot(data['Price'])
plt.show()


# ## b. Reviews column

# ### i. Make suitable plot 

# In[47]:


box =sns.boxplot(data["Reviews"])
plt.show(box)


# ### ii) Limit data to apps with < 1 Million reviews

# In[48]:


record_1m = data[data['Reviews'] > 1000000 ].index
data.drop(labels = record_1m, inplace=True)
print(record_1m.value_counts().sum(),'cols dropped')


# ## Install

# ### i. What is the 95th percentile of the installs?

# In[49]:


percentile = data.Installs.quantile(0.95) 
print(percentile,"is 95th percentile of Installs")


# ### Drop records having a value more than the 95th percentile

# In[50]:


temp=data[data["Installs"]>percentile].index
data.drop(labels=temp,inplace=True)
print(temp.value_counts().sum())


# # Data analysis to answer business questions

# ### What is the distribution of ratings like? (use Seaborn) More skewed towards higher/lowervalues?

# In[51]:


#how do you explain this 
sns.distplot(data['Rating'])
plt.show()
print('The skewness of this distribution is',data['Rating'].skew())
print('The Median of this distribution {} is greater than mean {} of this distribution'.format(data.Rating.median(),data.Rating.mean()))


# In[52]:


#The skewness of this distribution is -1.7434270330647985
#The Median of this distribution 4.3 is greater than mean 4.170800237107298 of this distribution


# In[53]:


##What is the implication of this on your analysis?
'''
Since mode >= median > mean, the distribution of Rating is Negatively Skewed.
Thereforethe  distribution of Rating is more Skewed towards lower values.

'''
data['Rating'].mode()


# ## What are the top Content Rating values?

# In[54]:


# Are there any values with very few records?


# In[55]:


data['Content Rating'].value_counts()


# In[ ]:





# # Effect of size on rating

# In[56]:


## Make a joinplot to understand the effect of size on rating 


# In[57]:


sns.jointplot(y='Size',x='Rating',data=data,kind='hex')
plt.show()


# In[58]:


# b) Do you see any patterns?
'''Yes, Patterns can be observed between Size and Rating which proves their is correlation between Size and Rating.'''


# In[59]:


# c) How do you explain the pattern?
'''There is positive correlation between Size and Rating since usually on increased Rating, Size of App also increases, but this is not always the case ie.for higher Rating, their is constant Size maintained'''


# # Effect of price on rating

# In[64]:


# a) Make a jointplot (with regression line)

sns.jointplot(x='Price', y='Rating', data=data, kind='reg')
plt.show()


# In[65]:


sns.jointplot(y='Price',x='Rating',data=data,kind='hex')
plt.show()


# 

# In[ ]:





# In[ ]:





# In[ ]:


### Which metric would you use? Mean? Median? Some other quantile?


# In[ ]:





# In[ ]:





# In[ ]:





# ### Look at all the numeric interactions together 

# In[66]:


# a) Make a pairplort with the colulmns - 'Reviews', 'Size', 'Rating', 'Price'

sns.pairplot(data, vars=['Reviews', 'Size', 'Rating', 'Price'], kind='reg')
plt.show()


# ## 10. Rating vs. content rating

# In[ ]:


## Make a bar plot displaying the rating for each content rating


# In[ ]:


data.groupby(['Content Rating'])['Rating'].count().plot.bar(color="lightblue")
plt.show()


# In[ ]:


data1=data.groupby(['Content Rating'])
print(data1)


# In[ ]:


# b) Which metric would you use? Mean? Median? Some other quantile?
'''We use Median in this case as we are having Outliers in Rating. Because in case of Outliers, median is the best measure of central tendency.'''


# In[ ]:


plt.boxplot(data['Rating'])
plt.show()


# In[ ]:


# c) Choose the right metric and plot
data.groupby(['Content Rating'])['Rating'].median().plot.barh(color="darkgreen")
plt.show()


# ## 11. Content rating vs. size vs. rating – 3 variables at a time
# 

# In[ ]:


### a. Create 5 buckets (20% records in each) based on Size


# In[ ]:


#data[('Size')].count()


# In[ ]:


#bins=[0-1687,3374,5061,6748,8435]


# In[ ]:


#data["Size"]=pd.cut(data['Size'],bins)


# In[ ]:


#data["Size"]


# In[ ]:


## By Content Rating vs. Size buckets, get the rating (20th percentile) for each combination


# In[ ]:





# In[ ]:


temp3= pd.pivot_table(data, values='Rating', index='Bucket Size', columns='Content Rating',
aggfunc= lambda x:np.quantile(x,0.2))
temp3


# In[ ]:


# c) Make a Heatmap of this
# i) Annoted

f,ax = plt.subplots(figsize=(5, 5))
sns.heatmap(temp3, annot=True, linewidths=.5, fmt='.1f',ax=ax)
plt.show()


# In[ ]:


# ii) Greens color map

f,ax = plt.subplots(figsize=(5, 5))
sns.heatmap(temp3, annot=True, linewidths=.5, cmap='Greens',fmt='.1f',ax=ax)
plt.show()


# In[61]:


# d)  What’s your inference? Are lighter apps preferred in all categories? Heavier? Some?

'''After The Analysis, it is visible that its not solely that lighter apps are preferred in all categories,
as apps with 60K-100K have got the Highest Rating in almost every category. Hence we can conclude as there is no such
preference of lighter weighing apps over heavier apps. '''


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




