import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import re

files = sorted(glob.glob("/home/brian/Documents/codes/NameData/yob*.txt"))

nYears =  len(files)

dfBible = pd.read_csv("/home/brian/Documents/codes/NameData/BibleData-Person.csv")
f = open("newTestament.txt",'r')
nt = f.read()
f.close()

#remove punctuation
nt = re.sub("[.,&:123456789?()^_]","",nt)

#split into words
nt = nt.split(' ')

#remove newlines
nt_clean = []
for word in nt:
    nt_clean.append(word.replace("\n", ""))

#remove  null characters   
nt_clean = list(filter(None,nt_clean))

nt_names = []
for word in nt_clean:
    if word[0].isupper():
        nt_names.append(word)

years = np.zeros(nYears)

percentbibM = np.zeros(nYears)
percentNTM = np.zeros(nYears)


percentbibF = np.zeros(nYears)
percentNTF = np.zeros(nYears)

percentbib = np.zeros(nYears)
percentNT = np.zeros(nYears)

j = 0
for filename in files:
    
    year = filename[-8:-4]
    print(year)
    df = pd.read_csv(filename, header = None)
    df[3] = df[0].str.len()
    
    df[4] = df[0].isin(dfBible['person_name']).astype(int)
    #column 4: 1 if in Hebrew Bible, 0 otherwise
    
    df[5] = df[2]*df[4]
    
    df[6] = df[0].isin(nt_names).astype(int) #column 6: 1 if in NT, 0 otherwise
    
    df[7] = df[2]*df[6]
    
    dfFemale = df[df[1] == 'F']
    dfMale   = df[df[1] == 'M']
    
    dfMale.reset_index()
    dfMale.reset_index(inplace=True)
    
    dfFemale.reset_index()
    dfFemale.reset_index(inplace=True)

    plt.figure(0)
    plt.clf()
    plt.suptitle(year)
    
    
    plt.subplot(221)
    plt.plot(np.arange(len(dfFemale[2])),np.array(dfFemale[2]),color='purple')
    plt.yscale('log')
    plt.xscale('log')
    plt.grid()
    
    plt.subplot(222)
    plt.hist(dfFemale[3],color='purple')
    plt.xlim(0,13)
    #plt.ylim(0,7000)
    
    plt.subplot(223)
    plt.plot(np.arange(len(dfMale[2])),np.array(dfMale[2]),color='green') 
    plt.xscale('log')
    plt.yscale('log')
    plt.grid()
    
    plt.subplot(224)
    plt.hist(dfMale[3],color='green')
    plt.xlim(0,13)
    plt.show()
    plt.pause(.01)

    
    plt.figure(1)
    plt.clf()
    topnum = 50
    plt.subplot(211)
    plt.suptitle(year,size=18)
    
    y = np.array(dfFemale[5])
    x = np.arange(len(y))+1
    n = np.array(dfFemale[0])
    
    Idx = np.where(y!=0)
    
    female_bn = n[Idx]
    female_by = y[Idx]
    female_bx = x[Idx]
    
    y = np.array(dfFemale[7])
    x = np.arange(len(y))+1
    n = np.array(dfFemale[0])
    
    female_ntIdx = dfFemale.index[dfFemale[6] > dfFemale[4]]   
    
    female_ntn = n[female_ntIdx]
    #print(female_ntn[:10])
    female_ntx = x[female_ntIdx]
    female_nty = y[female_ntIdx]
    
    plt.plot(np.arange(len(dfFemale[2][:topnum]))+1,np.array(dfFemale[2][:topnum]),color='green')
    
    #plt.plot(x,y,color='purple')
    #for i in range(topnum):
    #    plt.text(x[i],dfFemale[2][i],dfFemale[0][i],rotation=90,color='black',size=8)
    for i in range(50):
        plt.text(i+1,dfFemale[2][i],dfFemale[0][i],rotation=75,color='gray')
    for i in range(len(female_bn)):
        plt.text(female_bx[i],female_by[i],female_bn[i],rotation=75,color='purple')
        
    for i in range(len(female_ntn)):
        plt.text(female_ntx[i],female_nty[i],female_ntn[i],rotation=75,color='blue')
    plt.xlim(0,50)    
    plt.ylabel('# of Babies')
    
    
    plt.subplot(212)
    
    male_y = np.array(dfMale[5])
    male_x = np.arange(len(male_y))+1
    male_n = np.array(dfMale[0])
    
    male_Idx = np.where(male_y!=0)
    
    male_bn = male_n[male_Idx]
    male_bx = male_x[male_Idx]
    male_by = male_y[male_Idx]
    
    male_y = np.array(dfMale[7])
    male_x = np.arange(len(male_y))+1
    male_n = np.array(dfMale[0])
    
    male_ntIdx = dfMale.index[dfMale[6] > dfMale[4]]
    
    male_ntn = male_n[male_ntIdx]
    male_ntx = male_x[male_ntIdx]
    male_nty = male_y[male_ntIdx]
    
 
    plt.plot()
    plt.plot(np.arange(len(dfMale[2][:topnum]))+1,np.array(dfMale[2][:topnum]),color='green')
    #plt.plot(x,y,color='green')
    for i in range(50):
        plt.text(i+1,dfMale[2][i],dfMale[0][i],rotation=75,color='gray')
    for i in range(len(male_bn)):
        plt.text(male_bx[i],male_by[i],male_bn[i],rotation=75,color='purple')

    for i in range(len(male_ntn)):
        plt.text(male_ntx[i],male_nty[i],male_ntn[i],rotation=75,color='blue')
        
    #plt.texbt(1,dfMale[5][1],dfMale[0][1])
    plt.ylabel('# of Babies')
    plt.xlabel('Rank')
    plt.xlim(0,50)
    
    plt.savefig('name_vs_rank_'+year+'.png')
    plt.pause(.01)
    '''
    fig2 = plt.figure(2)
    fig2.clf()
    tn=20
    ax = fig2.add_subplot(111) 
    ax.cla()    
    ax.barh(male_x[:tn],male_y[:tn])
    #ax.set_ylim(0,nt)
    ax.set_yticks(male_x[:tn])
    ax.set_yticklabels(male_n[:tn], minor=False) 
    plt.gca().invert_yaxis()

    plt.pause(.01)
    '''
    
    years[j] = year
    percentbibM[j] = 100*sum(dfMale[5])/sum(dfMale[2])
    percentNTM[j]  = 100*sum(dfMale[7])/sum(dfMale[2])
    
    percentbibF[j] = 100*sum(dfFemale[5])/sum(dfFemale[2])
    percentNTF[j] = 100*sum(dfFemale[7])/sum(dfFemale[2])
      
    percentbib[j]  = 100*sum(df[5])/sum(df[2])
    percentNT[j]  = 100*sum(df[7])/sum(df[2])

    j+=1
    
plt.figure(4, figsize=(15,8))
plt.clf()
plt.subplot(311)
plt.plot(years,percentbib,'k',label='% OT names')
plt.plot(years,percentNT,'k--',label='% NT names')
plt.grid()
plt.ylabel("%")
plt.legend(loc='upper right')
plt.title('Biblical Baby Name Prevalence in the US 1880-2021')

plt.subplot(312)
plt.plot(years, percentbibM, 'g',label = '% OT male')
plt.plot(years, percentNTM, 'g--',label = '% NT male')
plt.grid()
plt.ylabel("%")
plt.legend(loc='upper right')

plt.subplot(313)
plt.plot(years,percentbibF, color='purple', label = '% OT female')
plt.plot(years,percentNTF, color='purple',ls='--', label = '% NT female')
plt.grid()
plt.ylabel("%")
plt.xlabel('Year')
plt.legend(loc='upper right')
plt.savefig('Name Prevalence By Year.png')
