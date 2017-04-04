import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re,csv

data=pd.read_csv('lagou_update.csv')
# a=[re.split(r'[-,以上]',line)[0] for line in data.Salary]
# b=[re.split(r'[-,以上]',line)[1] for line in data.Salary]
# for line in data['Salary']:
#     b=re.split(r'[-,以上]',line)[1]
    #print(b)
data['Salary2']=data['Salary2'].fillna(data['Salary2'].mean()) #fill the missing data with mean of Salary2.用Salary2的平均值填充缺失数据
# a=[int(m) for m in a]
# b=[int(n) for n in b]

fig=plt.figure()
plt.subplot()
plt.xlabel('Company',fontsize=20)
plt.ylabel('Salary',fontsize=20)
plt.plot(data['Salary1'][:80],'r-',label='Lowest Salary')
plt.plot(data['Salary2'][:80],label='Highest Salary')
#plt.fill_between(data['Salary1'][:80],data['Salary2'][:80],facecolor='blue',alpha=.5)
#plt.xticks([0,50,100,150,200,250,300,350,400,450])
plt.ylim(0,30000)
plt.title('Data Analyst Salary',fontsize=30)
plt.grid(False)
plt.legend(loc='best')

fig2=plt.figure()
#ax1=fig2.add_subplot(211)
len1=len(data.Salary1)
colors=np.random.rand(len1)
size=np.pi*np.random.rand(len1)*50
plt.title('Data Analyst Salary1',fontsize=30)
plt.xticks([0,50,100,150,200,250,300,350,400,450])
plt.scatter(range(len1),data['Salary1'],c='b',s=80,alpha=.5)
# lowest_salary_data=[(182,1000,'Lowest Salary'),(189,1000,'Lowest Salary')]
# for x,y,label in lowest_salary_data:
#     plt.annotate(label,xy=(x,y),
#                  xytext=(x,y),
#                  arrowprops=dict(facecolor='black'))
plt.annotate('Lowest Salary',xy=(182,1000),xytext=(125,2500),arrowprops=dict(facecolor='black',shrink=.05))
plt.annotate('Lowest Salary',xy=(189,1000),xytext=(225,2500),arrowprops=dict(facecolor='black',shrink=.05))
#plt.colorbar()
print(data['Salary1'].asof(182)+50)

fig3=plt.figure()
ax2=fig2.add_subplot(111)
len2=len(data.Salary2)
colors=np.random.rand(len2)
size2=np.pi*np.random.rand(len2)*60
plt.title('Data Analyst Salary2',fontsize=25)
plt.xticks([0,50,100,150,200,250,300,350,400,450])
plt.xlabel('Company',fontsize=20)
plt.ylabel('Salary',fontsize=20)
#plt.scatter(range(len2),data.Salary2,c=colors,s=size2)
plt.scatter(range(len2),data.Salary2,s=80,c=range(len(data.Salary2)))
plt.scatter(range(len2),data.Salary2,s=80,c='r')
plt.scatter(446,60000,c='b',s=200)
plt.annotate('Highest Salary',xy=(446,60000),fontsize=15,xytext=(330,55000),arrowprops=dict(facecolor='black',shrink=.05))
#plt.colorbar()
print(range(len(data.Salary2)))

fig4=plt.figure()
plt.hist(data.Salary1,50)

plt.show()