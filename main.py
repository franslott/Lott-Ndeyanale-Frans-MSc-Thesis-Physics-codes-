#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 17:49:16 2019

@Author: Frans Lott N
@alias: thecurioswambo
contact: +264 81 3129813
email:franslott8@gmail.com 
"""

#importing packages

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.cm as cm
import csv

###############################

###### Plotting option ######

print("enter 1: for CT (night) results")
print("enter 2: for AERONET (day) results")
##############################

select=int(input('select:')) ########### recieve plotting input
bin_edges=[2.5,3,3.5,4,4.5,5]  ####list of bin adges
bin_edges1=[2.5,3,3.5,4,4.5,5]  ####list of bin adges
bin_edges3=[.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8]
bin_edges2=[.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6]
bin_edges4=[1.5,2,2.5,3,3.5,4,4.5,5]
#### plotting CT results #######

if select == 1:
    fin=open('CTPWV.csv','r')      # Opening CT PWV file
    
    
    CTPWV=[]               # empty list for storing CT PWV data
    CTPWVstd=[]            # empty list storing CT PWV standard deviation data
    CTtime=[]              # empty list for storing correspinding CT data time
    
    
    #proccessing data from file (loading data)
    for line in fin:
        
        # extracts date and time strings, and converting it into a number
        Datetime=line.split(',')[0]
        date=Datetime.split()[0]
        year=int(date.split('-')[0])
        month=int(date.split('-')[1])
        day=int(date.split('-')[2])
        time=Datetime.split()[1]
        hour=int(time.split(':')[0])
        minute=int(time.split(':')[1])
        sec=int(time.split(':')[2])
                    
        # creating a time from extracted data        
        dateHuman = datetime(year, month, day, hour, minute)
        
        # extracting PWV and Standard deviation and converting it into float
        
        PWV=float(line.split(',')[1])
        std=float(line.split(',')[2])
        
        # storing time,PWV and standard deviation data to empty list
        CTPWV.append(PWV)
        CTPWVstd.append(std)
        CTtime.append(dateHuman)
        
    # plotting data to visulize how the PWV looks like
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.errorbar(CTtime,CTPWV,yerr=CTPWVstd,color='blue',fmt='o',alpha=1)
    ax.set_title('mean callibrated CT PWV at H.E.S.S')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('period')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig('CTplots/CTdata')
    fig.show()
    
    # a function to convert all zeros to nan values incase of plotting
    def zero_to_nan(values):
        return [float('nan') if x==0 else x for x in values]
    
    # creating a list equivalent to number of CT years data called YCT 
    YCT=list(range(1,17))
    
    # Creating a list equivalent to number of months in a year
    M=list(range(1,13))
    # Gamsberg Measured PWV in 1994 and 1995
    Gamsberg_94=[0,0,0,0,0,0,3.20799,2.56114,5.46083,6.21921,7.51292,6.70993]
    Gamsberg_95=[5.90694,0,6.33074,6.46457,6.55379,4.34557,3.52027,0,0,0,0,0]
    
    # a list containing months
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    # analysing the PWV data,and standard deviation by year
    for j in YCT:
        CTyear=[i for i in zip(CTtime,CTPWV,CTPWVstd) if i[0].year ==2003+j ]
        CTdateyear=[i[0] for i in CTyear]
        CTaveyear=[i[1] for i in CTyear]
        CTstdyear=[i[2] for i in CTyear]
        
        # plotting by yearly PWV data 
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.errorbar(CTdateyear,CTaveyear,CTstdyear,color='yellow',fmt='o')
        ax.set_title('CT mean at H.E.S.S. %i' %(2003+j))
        ax.set_ylabel('Percipitable Water Vapour (mm)')
        ax.set_xlabel('time')
        ax.grid(True)
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()
        fig.savefig('CTplots/Plots/Yearly/CT1-4meanatH.E.S.S.%i.jpg' %(2003+j))
        fig.show()  
        
        # analysing data by month of year in YCT
        for m,t in zip(M,months):
    
            CTmonth=[i for i in CTyear if i[0].month== m ]
            CTdate=[i[0] for i in CTmonth]
            CTave=[i[1] for i in CTmonth]
            CTstd=[i[2] for i in CTmonth]
    
            # Plotting individual month data
            
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.errorbar(CTdate,CTave,CTstd,color='blue',fmt='o')
            ax.set_title('CT mean PWV at H.E.S.S. in %s %i' %(t,2003+j))
            ax.set_ylabel('Percipitable Water Vapour (mm)')
            ax.set_xlabel('time')
            ax.grid(True)
            fig.autofmt_xdate(rotation=45)
            fig.tight_layout()
            fig.savefig('CTplots/Plots/Monthly/CT1-4meanatH.E.S.S.%s%i.jpg' %(t,2003+j))
            fig.show()  
                 
    # scaling function for Mt Gamsberg
    h1=1800                 #  elevation of H.E.S.S. site in meters
    h2=2347                 #  elevation of Mt Gamsberg in meters   
    H=2000.                 # Water vapour scale height
    alpha=np.e**-((h2-h1)/H)    #  scaling function
    
    Gamsberg_94=zero_to_nan(Gamsberg_94)   # removing zero values for plotting
    Gamsberg_95=zero_to_nan(Gamsberg_95)   # removing zero values for plotting
    
    PWVzero = [0 if math.isnan(x) else x for x in CTPWV] # adding zero if "nan"
    stdzero=[0 if math.isnan(x) else x for x in CTPWVstd] # adding zero if "nan"
    
    scaPWV = [ alpha*x for x in CTPWV]
    # removing zeros from list to have clean PWV and standard deviation
    PWVclean = [i for i in zip(CTtime,PWVzero,stdzero) if i[1] != 0 ]
  
    # creating empty list for storing weighted mean PWV
    PWVweightedave=[]
    # creating empty list for storing corresponding standard deviation 
    yerr=[]
    # creating empty list for storing corresponding time
    month=[]
    
    # analysing data by year
    for j in YCT:
        CTyear=[i for i in PWVclean if i[0].year ==2003+j ]
        CTdateyear=[i[0] for i in CTyear]
        CTaveyear=[i[1] for i in CTyear]
        CTstdyear=[i[2] for i in CTyear]
        
    
        monthlist=[]
        allmonthdata=[]
        
        maxcount=[]
        maxtime=[]
        
        mincount=[]
        mintime=[]
        
        # Analysing data by month
        for m,t in zip(M,months):
            CTmonth=[i for i in CTyear if i[0].month== m ]
            CTdate=[i[0] for i in CTmonth]
            CTave=[i[1] for i in CTmonth]
            CTstd=[i[2] for i in CTmonth]
            CTstd=[1 if np.mean(CTstd)==0 else i for i in CTstd]
            allmonthdata.append(len(CTmonth))
            monthlist.append(t)
            
            # proccesing data as 0 if number of data points is less than 50
            
            if len(CTmonth) < 50.0 :
                month.append(t)
                yerr.append(0.0)
                PWVweightedave.append(0.0)
                mincount.append(len(CTmonth))
                maxcount.append(0.0)
                maxtime.append(t)
                mintime.append(t)
                
            # processing data if number of data points is 50 or more    
            if len(CTmonth) >= 50.0 :
                weightedave=np.average(CTave,weights=CTstd)
                PWVweightedave.append(weightedave)
                CTweightedstd=np.std(CTave)
                yerr.append(CTweightedstd)
                month.append(t)
                mincount.append(0.0)
                maxcount.append(len(CTmonth))
                maxtime.append(t)
                mintime.append(t)
                
                # Plotting monthly histogram
                
                plt.figure("Monthly Histogram of PWV")
                plt.hist(CTave, color = 'purple', edgecolor = 'black',bins = bin_edges,alpha=1,cumulative=1,normed=True)
                plt.title("PWV Histogram for %s in %i at H.E.S.S." %(t,2003+j))
                plt.xlabel(" Percipitable Water Vapour (mm)")
                plt.ylabel("fraction [%]")
                plt.savefig('CTplots/Hist/Monthly/PWV histograms of month %s year %i.jpeg' %(t,2003+j))
                #plt.show()
     
    
        # getting number of data taken for each month with records and writting them to a file 
        alldatafile=[i for i in zip(monthlist,allmonthdata)]  
        with open('CTplots/datacount/csvfile/alldatafile_{0}.csv'.format(j+2003),'w',newline='') as f:
            w = csv.writer(f)
            w.writerow(['month of year','data points taken'])
            w.writerows(alldatafile)
            
        # plotting number of monthly data points    
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(monthlist,allmonthdata,color='purple')
        #ax.set_title('number of monthly recordings at H.E.S.S. in %i' %(2003+j))
        ax.set_ylabel('number of recordings')
        ax.set_xlabel('Month')
        ax.grid(True)
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()
        fig.savefig('CTplots/datacount/plots/recordcount%i.jpg' %(2003+j))
        fig.show()
        
       
        # convering all zero data points to nan for plotting
        maxcount=zero_to_nan(maxcount)
        mincount=zero_to_nan(mincount)
        
        # plotting considered 50 or more points for visualization
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(maxtime,maxcount,color='purple',label='considered value')
        ax.scatter(mintime,mincount,color='grey',label='Unconsidered value')
        ax.set_title('number of considered monthly recordings at H.E.S.S. in %i' %(2003+j))
        ax.set_ylabel('number of recordings')
        ax.set_xlabel('Month')
        ax.grid(True)
        ax.legend()
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()
        fig.savefig('CTplots/datacount/plots/greyrecordcount%i.jpg' %(2003+j))
        fig.show()     
     
        
    # converting zero to nan    
    yerr=zero_to_nan(yerr)
    PWVweightedave=zero_to_nan(PWVweightedave)
    # removing nana values
    PWVstdtime=[i for i in zip(month,PWVweightedave,yerr) if str(i[1]) != 'nan']
    
    
    # scaling H.E.S.S. site PWV for Mt Gamsberg
    scPWVweighted=[i*alpha for i in PWVweightedave]
    # removing nan values
    scPWVstdtime=[i for i in zip(month,scPWVweighted,yerr) if str(i[1]) != 'nan']
    
    
    avePWV=[]   # empty list to store mean PWV of H.E.S.S.
    aveSTD=[]   #  empty lsit for storing corresponding Standard deviation
    
    scavePWV=[]  # empty list for storing scaled mean PWV for Mt Gamsberg
    scaveSTD=[]  # empty list storing corresponding standard deviation for scaled vales
    
    
    # processing non scaled PWV of H.E.S.S. and scaled PWV for Mt Gamsberg
    for i in months:
        avestd=[(k[0],k[1],k[2]) for k in PWVstdtime if k[0]==i]
        allPWV=[i[1] for i in avestd ]
        allstd=[i[2] for i in avestd ]
        avePWVave=np.average(allPWV,weights=allstd)
        stdallstd=np.std(allPWV)
        avePWV.append(avePWVave)
        aveSTD.append(stdallstd)
        
        scavestd=[(k[0],k[1],k[2]) for k in scPWVstdtime if k[0]==i]
        scallPWV=[i[1] for i in scavestd ]
        scallstd=[i[2] for i in scavestd ]
        scavePWVave=np.average(scallPWV,weights=scallstd)
        scstdallstd=np.std(scallPWV)
        scavePWV.append(scavePWVave)
        scaveSTD.append(scstdallstd)
        
        
    # Plotting H.E.S.S. site single monthly  PWV values
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(month,PWVweightedave,color='grey',label='monthly weighted value')
    ax.errorbar(months,avePWV,yerr=aveSTD,color='blue',fmt='o',label='specific month weighted averages')
    ax.set_title('H.E.S.S Weighted monthly averages')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('Month')
    ax.grid(True)
    ax.legend()
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig('CTplots/AveragedpointHESS.jpg')
    fig.show()        
    
    # Plotting Mt Gasmberg site single monthly weighted mean PWV values
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(month,scPWVweighted,color='grey',label='monthly weighted value')
    ax.errorbar(months,scavePWV,yerr=aveSTD,color='green',fmt='o',label='specific month weighted averages')
    ax.set_title('Mt Gamsberg Weighted monthly averages')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('Month')
    ax.grid(True)
    ax.legend()
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig('CTplots/AveragedpointGams.jpg')
    fig.show()    
    
 
        
    Gamsberg_94=zero_to_nan(Gamsberg_94)
    Gamsberg_95=zero_to_nan(Gamsberg_95)
    yerr=zero_to_nan(yerr)
    PWVweighted=zero_to_nan(PWVweightedave)
    
    
    # Plotting H.E.S.S. weighted mean PWV (seasonal variations)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    n=12    
    q=[PWVweighted[i:i+n] for i in range(0, len(PWVweighted), n)]    
    x = np.arange(1,13)
    markers=['x','*','o','v','^','<','>','1','D','H','s','8','_','|','+','.']
    colors = cm.rainbow(np.linspace(0, 1, len(q)))
    
    for j,y, c,m in zip(YCT,q, colors,markers):
        ax.plot(months, y, color=c,linestyle='-',marker=m,label="%i "%(2003+j))    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.5, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_title('H.E.S.S. weighted Means')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('Month of the year')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig('CTplots/H.E.S.S.monthlyave.png')
    fig.show()
    
    # plotting weighted mean scaled values for Mt Gamsberg (Seasonal variations)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    n=12    
    q=[scPWVweighted[i:i+n] for i in range(0, len(scPWVweighted), n)]    
    x = np.arange(1,13)
    markers=['x','*','o','v','^','<','>','1','D','H','s','8','_','|','+','.']
    colors = cm.rainbow(np.linspace(0, 1, len(q)))
    
    for j,y, c,m in zip(YCT,q, colors,markers):
        ax.plot(months, y, color=c,linestyle='-',marker=m,label="%i "%(2003+j))    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.5, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_title('Mt Gamsberg weighted Means')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('Month of the year')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig('CTplots/MountGamsaveCT.png')
    fig.show()
    
    
    # plotting weighted means of Mt Gamsberg along with 1994-1995 PWV values
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(months,Gamsberg_94,color='grey',linestyle='-',marker='+',label="1994" )
    ax.plot(months,Gamsberg_95,color='purple',linestyle='-',marker='s',label="1995" )
    n=12    
    q=[scPWVweighted[i:i+n] for i in range(0, len(scPWVweighted), n)]    
    x = np.arange(1,13)
    markers=['x','*','o','v','^','<','>','1','D','H','s','8','_','|','+','.']
    colors = cm.rainbow(np.linspace(0, 1, len(q)))
    
    for j,y, c,m in zip(YCT,q, colors,markers):
        ax.plot(months, y, color=c,linestyle='-',marker=m,label="%i "%(2003+j))    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.5, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_title('Mt Gamsberg weighted Means')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('Month of the year')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig('CTplots/MountGamsave.png')
    fig.show()
    
    
    
    
    
    heights, bins = np.histogram(CTPWV, bins = bin_edges3)
    percent = [i/sum(heights)*100 for i in heights]
    
    
    plt.figure()
    plt.bar(bins[:-1], percent, width = 0.5, linewidth=1,align="edge", edgecolor='black',color='blue',alpha=1)
    plt.xlim(min(bins), max(bins))
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Percipitable Water Vapour (mm)')
    plt.ylabel('Fraction  [%]')
    plt.xticks()
    plt.yticks()
    plt.savefig('CTplots/Hist/Monthly/allHESSPWV.jpeg')
    plt.title('relative frequencyDistribution Histogram H.E.S.S.',fontsize=15)
    plt.show()
    
    
    heights1, bins2 = np.histogram(scaPWV, bins = bin_edges2)
    percent1 = [i/sum(heights1)*100 for i in heights1]
    print(percent1)
    
    plt.figure()
    plt.bar(bins2[:-1], percent1, width = 0.5, linewidth=1,align="edge", edgecolor='black',color='green',alpha=1)
    plt.xlim(min(bins2), max(bins2))
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Percipitable Water Vapour (mm)')
    plt.ylabel('Fraction  [%]')
    plt.xticks()
    plt.yticks()
    plt.savefig('CTplots/Hist/Monthly/allgamsPWV.jpeg')
    plt.title('Relative frequency Distribution Histogram for Gamsberg',fontsize=15)
    plt.show
    
    plt.figure()
    plt.hist(scaPWV, color = 'purple', edgecolor = 'black',bins = bin_edges4,alpha=1,cumulative=1,normed=True)
    plt.title('Relative frequency Distribution Histogram for Gamsberg 1',fontsize=15)
    plt.xlabel(" Percipitable Water Vapour (mm)")
    plt.ylabel("fraction [%]")
    #plt.savefig('CTplots/Hist/Monthly/PWV histograms of month %s year %i.jpeg')

    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.errorbar(CTtime,scaPWV,yerr=CTPWVstd,markersize=3,color='green',fmt='o',alpha=1)
    #ax.set_title('mean callibrated CT PWV at H.E.S.S')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('period')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig('CTplots/gamsCTdata.jpeg')
    fig.show()
    
    
    
    
# proccesing areonet values (daily values)    
    
if select == 2:
        
    fin=open('AeronetPWV.csv','r') # opening Aeronet data file
    
    
    def zero_to_nan(values):
        return [float('nan') if x==0 else x for x in values]
    
    CTPWV=[]   # empty list for storing PWV
    CTtime=[]  # empty list for storing corresponding time
    
    # reading and loading data from file
    for line in fin:
        
        # reading in date and time, converting it to a number
        Datetime=line.split(',')[0]
        date=Datetime.split()[0]
        year=int(date.split('-')[0])
        month=int(date.split('-')[1])
        day=int(date.split('-')[2])
        time=Datetime.split()[1]
        hour=int(time.split(':')[0])
        minute=int(time.split(':')[1])
        sec=int(time.split(':')[2])
                    
        # converting it to useful date         
        dateHuman = datetime(year, month, day, hour, minute,sec)
        PWV=float(line.split(',')[1])
        
        # storing PWV data and time to empty list
        CTPWV.append(PWV)
        CTtime.append(dateHuman)
        
    #plotting data to visualize
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CTtime,CTPWV,color='blue',alpha=1)
    ax.set_title('mean callibrated CT PWV at H.E.S.S')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('time')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig('Aeronetplots/Aeronetcallibrateddata')
    fig.show()
    
     # a function to convert all zeros to nan values incase of plotting
    def zero_to_nan(values):
        return [float('nan') if x==0 else x for x in values]
    
    # a list containing number of years data taken (3)
    YCT=list(range(1,4))
    # list containing number of months in year (12)
    M=list(range(1,13))
    # list contaning listof month
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    # processing data by yeear
    for j in YCT:
        CTyear=[i for i in zip(CTtime,CTPWV) if i[0].year ==2015+j ]
        CTdateyear=[i[0] for i in CTyear]
        CTaveyear=[i[1] for i in CTyear]
        
        # plotting year data
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(CTdateyear,CTaveyear,color='yellow')
        ax.set_title('Aeronet PWV at H.E.S.S. %i' %(2015+j))
        ax.set_ylabel('Percipitable Water Vapour (mm)')
        ax.set_xlabel('time')
        ax.grid(True)
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()
        fig.savefig('Aeronetplots/Plots/yearly/meanatH.E.S.S.%i.jpg' %(2015+j))
        fig.show()  
        
        # processing data by month
        for m in M:
    
            CTmonth=[i for i in CTyear if i[0].month== m ]
            CTdate=[i[0] for i in CTmonth]
            CTave=[i[1] for i in CTmonth]
            
            # plotting monthly plots
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.scatter(CTdate,CTave,color='blue')
            ax.set_title('Aeronet PWV at H.E.S.S. %i %i' %(m,2015+j))
            ax.set_ylabel('Percipitable Water Vapour (mm)')
            ax.set_xlabel('time')
            ax.grid(True)
            fig.autofmt_xdate(rotation=45)
            fig.tight_layout()
            fig.savefig('Aeronetplots/Plots/monthly/H.E.S.S.%i%i.jpg' %(m,2015+j))
            fig.show()  
                 
    
    
    h1=1800  # H.E.S.S elevation in meters
    h2=2347  # Mt Gamsberg elevation in meters
    H=2000.  # water vapour scale heiht  
    alpha=np.e**-((h2-h1)/H)
    
    # adding zero if vale is equall to nan
    PWVzero = [0 if math.isnan(x) else x for x in CTPWV]
    # removing zero PWV with its time
    PWVclean = [i for i in zip(CTtime,PWVzero) if i[1] != 0 ]
    
  
    # empty list for weighted PWV and erro,and time
    PWVweightedave=[]
    yerr=[]
    month=[]
    
    # processing data by year
    for j in YCT:
        CTyear=[i for i in PWVclean if i[0].year ==2015+j ]
        CTdateyear=[i[0] for i in CTyear]
        CTaveyear=[i[1] for i in CTyear]
        
    
        monthlist=[]
        allmonthdata=[]
        
        maxcount=[]
        maxtime=[]
        
        mincount=[]
        mintime=[]
        
        # processing data by month
        for m,t in zip(M,months):
            CTmonth=[i for i in CTyear if i[0].month== m ]
            CTdate=[i[0] for i in CTmonth]
            CTave=[i[1] for i in CTmonth]
            
            allmonthdata.append(len(CTmonth))
            monthlist.append(t)
            
            # discarding data of month if its less then 1500
            if len(CTmonth) < 00.0 :
                month.append(t)
                yerr.append(0.0)
                PWVweightedave.append(0.0)
                mincount.append(len(CTmonth))
                maxcount.append(0.0)
                maxtime.append(t)
                mintime.append(t)
                
            # proccesing data of month if its equall to 1500 or more    
            if len(CTmonth) >= 0.0 :
                weightedave=np.mean(CTave)
                PWVweightedave.append(weightedave)
                CTweightedstd=np.std(CTave)
                yerr.append(CTweightedstd)
                month.append(t)
                mincount.append(0.0)
                maxcount.append(len(CTmonth))
                maxtime.append(t)
                mintime.append(t)
                
                # plotting histo plot of data
                plt.figure("Monthly Histogram of PWV")
                plt.hist(CTave, color = 'purple', edgecolor = 'black',bins = bin_edges,alpha=1,cumulative=1,normed=True)
                plt.title("PWV Histogram for %s in %i at H.E.S.S." %(t,2015+j))
                plt.xlabel(" Percipitable Water Vapour (mm)")
                plt.ylabel("fraction [%]")
                plt.savefig('CTplots/Hist/Monthly/PWV histograms of month %s year %i.jpeg' %(t,2003+j))
                plt.show()
     
    
        # getting number of data taken for each month with records and writting them to a file 
        alldatafile=[i for i in zip(monthlist,allmonthdata)]  
        with open('Aeronetplots/datacount/csvfile/alldatafile_{0}.csv'.format(j+2015),'w',newline='') as f:
            w = csv.writer(f)
            w.writerow(['month of year','data points taken'])
            w.writerows(alldatafile)
            
         # plotting number of data recorded per month of year   
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(monthlist,allmonthdata,color='purple')
        ax.set_title('number of monthly recordings at H.E.S.S. in %i' %(2015+j))
        ax.set_ylabel('number of recordings')
        ax.set_xlabel('Month')
        ax.grid(True)
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()
        fig.savefig('Aeronetplots/datacount/plots/recordcount%i.jpg' %(2015+j))
        fig.show()
        
        maxcount=zero_to_nan(maxcount)
        mincount=zero_to_nan(mincount)
        # plotting considered number of points
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(maxtime,maxcount,color='purple',label='considered value')
        ax.scatter(mintime,mincount,color='grey',label='Unconsidered value')
        ax.set_title('number of considered monthly recordings at H.E.S.S. in %i' %(2015+j))
        ax.set_ylabel('number of recordings')
        ax.set_xlabel('Month')
        ax.grid(True)
        ax.legend()
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()
        fig.savefig('Aeronetplots/datacount/plots/greyrecordcount%i.jpg' %(2015+j))
        fig.show()     
     
    yerr=zero_to_nan(yerr)
    PWVweightedave=zero_to_nan(PWVweightedave)   
    PWVstdtime=[i for i in zip(month,PWVweightedave,yerr) if str(i[1]) != 'nan']
    
    scPWVweighted=[i*alpha for i in PWVweightedave]
    scPWVstdtime=[i for i in zip(month,scPWVweighted,yerr) if str(i[1]) != 'nan']
    
    
    avePWV=[]
    aveSTD=[]
    
    scavePWV=[]
    scaveSTD=[]
    
    for i in months:
        avestd=[(k[0],k[1],k[2]) for k in PWVstdtime if k[0]==i]
        allPWV=[i[1] for i in avestd ]
        allstd=[i[2] for i in avestd ]
        avePWVave=np.average(allPWV,weights=allstd)
        stdallstd=np.std(allPWV)
        avePWV.append(avePWVave)
        aveSTD.append(stdallstd)
        
        scavestd=[(k[0],k[1],k[2]) for k in scPWVstdtime if k[0]==i]
        scallPWV=[i[1] for i in scavestd ]
        scallstd=[i[2] for i in scavestd ]
        scavePWVave=np.average(scallPWV,weights=scallstd)
        scstdallstd=np.std(scallPWV)
        scavePWV.append(scavePWVave)
        scaveSTD.append(scstdallstd)
        
        
    # plotting monthly mean PWV at h.e.s.s. site
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(month,PWVweightedave,color='grey',label='monthly weighted value')
    ax.errorbar(months,avePWV,yerr=aveSTD,color='blue',fmt='o',label='specific month weighted averages')
    ax.set_title('H.E.S.S Weighted monthly averages')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('Month')
    ax.grid(True)
    ax.legend()
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig('Aeronetplots/AveragedpointHESS.jpg')
    fig.show()        
     
    # plotting weighted mean PWV scaled for Mt Gamsberg
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(month,scPWVweighted,color='grey',label='monthly weighted value')
    ax.errorbar(months,scavePWV,yerr=aveSTD,color='red',fmt='o',label='specific month weighted averages')
    ax.set_title('Mt Gamsberg Weighted monthly averages')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('Month')
    ax.grid(True)
    ax.legend()
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig('Aeronetplots/AveragedpointGams.jpg')
    fig.show()    
        
        
    yerr=zero_to_nan(yerr)
    PWVweighted=zero_to_nan(PWVweightedave)
    
    
    
    # plotting seasonal variations plot at H.E.S.S. site
    fig = plt.figure()
    ax = fig.add_subplot(111)
    n=12    
    q=[PWVweighted[i:i+n] for i in range(0, len(PWVweighted), n)]    
    x = np.arange(1,13)
    markers=['x','*','o']
    colors = cm.rainbow(np.linspace(0, 1, len(q)))
    
    for j,y, c,m in zip(YCT,q, colors,markers):
        ax.plot(months, y, color=c,linestyle='-',marker=m,label="%i "%(2015+j))    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.5, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_title('H.E.S.S. weighted Means')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('Month of the year')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig('Aeronetplots/H.E.S.S.monthlyave.png')
    fig.show()
    
    Gamsberg_94=[0,0,0,0,0,0,3.20799,2.56114,5.46083,6.21921,7.51292,6.70993]
    Gamsberg_95=[5.90694,0,6.33074,6.46457,6.55379,4.34557,3.52027,0,0,0,0,0]
    
    Gamsberg_94=zero_to_nan(Gamsberg_94)
    Gamsberg_95=zero_to_nan(Gamsberg_95)
    
    # plotting scaled values for Mt Gamsberg (seasonal variations)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    n=12    
    q=[scPWVweighted[i:i+n] for i in range(0, len(scPWVweighted), n)]    
    x = np.arange(1,13)
    markers=['x','*','o']
    colors = cm.rainbow(np.linspace(0, 1, len(q)))
    
    for j,y, c,m in zip(YCT,q, colors,markers):
        ax.plot(months, y, color=c,linestyle='-',marker=m,label="%i "%(2015+j))    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.5, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_title('Mt Gamsberg AERONET mean PWV')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('Month of the year')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig('Aeronetplots/MountGamsaveCT.png')
    fig.show() 
    
    
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    n=12    
    q=[scPWVweighted[i:i+n] for i in range(0, len(scPWVweighted), n)]    
    x = np.arange(1,13)
    ax.plot(months,Gamsberg_94,color='grey',linestyle='-',marker='+',label="1994" )
    ax.plot(months,Gamsberg_95,color='purple',linestyle='-',marker='s',label="1995")
    markers=['x','*','o']
    colors = cm.rainbow(np.linspace(0, 1, len(q)))
    
    for j,y, c,m in zip(YCT,q, colors,markers):
        ax.plot(months, y, color=c,linestyle='-',marker=m,label="%i-AERONET"%(2015+j))    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.5, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_title('Mt Gamsberg mean PWV')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('Month of the year')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig('Aeronetplots/MountGamsaveall.png')
    fig.show()
    
    
