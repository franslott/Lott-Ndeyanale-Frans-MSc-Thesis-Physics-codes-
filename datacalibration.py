#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 03:34:32 2019

@author: thecuriosvambo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 03:55:15 2019

@author: thecurioswambo
"""
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from itertools import islice
import glob
from pathlib import Path
import math
import matplotlib.cm as cm
import csv
import itertools
from astropy.stats import median_absolute_deviation
#import scipy

from scipy.optimize import curve_fit
import numpy.polynomial.polynomial as poly
from scipy.interpolate import *
from scipy.stats import pearsonr

#####################################################################
####################################################################


# Opening Aeronet data and processing

print("press 1 for Aeronet , Atmoscope calibration")
print("press 2 for Atmoscope , CT calibration")

select=int(input('select:'))  # Input of option 1 or 2 

if select == 1:
    
    # Opens Aeronet datafile for processing
    aeronet=open("20160101_20191231_HESS.lev20",'r')
        
    Aerodate=[]
    AeronetPWV=[]
    fullAerodate=[]
    
    AeronetPWVdata=open('AeronetPWV.csv','w') # opens new file to write Aeronet PWV to
    
    for line in islice(aeronet, 7, None):
        pass
        aeroPWV=float(line.split(",")[26])
        
        if aeroPWV <= -50.0:
            continue
        
        date=line.split(",")[0]
        day=int(date.strip("")[0:2])
        month=int(date.strip(":")[3:5])
        year=int(date.strip(':')[6:])
        
        time=line.split(",")[1]
        hour=int(time.strip("")[0:2])
        minute=int(time.strip(":")[3:5])
        sec=int(time.strip(':')[6:])
        
        datetim=datetime(year,month,day,hour,minute)
        fulldatetim=datetime(year,month,day,hour,minute,sec)
        Aerodate.append(datetim)
        fullAerodate.append(fulldatetim)
        PWV=aeroPWV
        AeronetPWV.append(PWV*10.00)   
    aeronet.close()

    Aeronetdata=[i for i in zip(Aerodate,AeronetPWV)]
    
    for i,j in zip(fullAerodate,AeronetPWV):
        AeronetPWVdata.write('%s,%5.2f\n' %(i,j)) #writes PWV onto file
    #######################################################################

    ## Plots PWV from the Aeronet
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(fullAerodate,AeronetPWV,s=1,color='blue')
    #ax.set_title('Aeronet PW vs Time at H.E.S.S')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('period')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("completeAeronet")
    fig.show()



    #=========== opens and reads in data from atmoscope ==================#

    AtmoscopePWVdata=open('AtmosPWV.csv','w')
    y=6.5*(10**-3)
    Atmoscopetime=[]
    skytemp_atmoscope=[]
    fullAtmoscopetime=[]
    for file in sorted(glob.glob('/home/thecuriosvambo/Documents/codes/hesspart/*.dat')):
        with open(file) as f:
            # skipping and passing the Header titles and not reading them
            for line in islice(f, 1, None):
                pass
            
                # Extracting the temperature and cloud height and converting it into a useful number
                temperature=float(line.split()[2]) 
                cloud_altitude=float(line.split()[7])
                
                # skipping and not reading inthe data when the instruments where at the inital point and not recording useful data
                if  temperature <= -50.0:
                    continue
                
                # extracts the date and time from the file
                Datetime=line.split()[0]
                # extract date and converst it to a float (useful number)
                date=Datetime.split('_')[0]
                year=int(date.split('-')[0])
                month=int(date.split('-')[1])
                day=int(date.split('-')[2])
                # extracts the time and converts it into a useful number
                time=Datetime.split('_')[1]
                hour=int(time.split(':')[0])
                minute=int(time.split(':')[1])
                sec=int(time.split(':')[2])
                
                # Conversion to julian dates
                dateHuman = datetime(year, month, day, hour, minute)
                Atmoscopetime.append(dateHuman)
                
                fullhumandate = datetime(year, month, day, hour, minute,sec)
                fullAtmoscopetime.append(fullhumandate)
                    
                # Calculating the PWV from the ambient temp,cloud altitude altitude and gradient temperature.
                T0=temperature  # ( degrees Celscius)
                h=cloud_altitude  #(m)
                
                # MWS 3 & 485-Sensors with Microprocessor without datalogger manual
                
                # Formula to calculate the cloud temperature, page 9 section 3.2.6 The clouds Sensor WKS 485
                T=T0-h*y    # (K)   T=cloud temperature temperature,T0=ambient temp, y=gradient temperature 
                #T= T - 273.15  # (Degrees celcius) 
                
                skytemp_atmoscope.append(T)
                
    f.close()

    Atmoscopedata=[i for i in zip(Atmoscopetime,skytemp_atmoscope)]
    
    ##### plotting Atmoscope sky temparture at H.E.S.S.
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(fullAtmoscopetime,skytemp_atmoscope,s=1,color='red')
    #ax.set_title('Atmoscope PW vs Time at H.E.S.S')
    ax.set_ylabel('Infrared sky temp ($^\circ$C)')
    ax.set_xlabel('time')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("Atmosrawdata")
    fig.show()
    
##############################################################################
############ CALIBRATION of Atmoscope vs Aeronet##############################

###############################################################################


    #Atmos=sorted(list(set(i for i,j in Atmoscopedata) & set(x for x,y in Aeronetdata)))
    AtmosAero=list(set(i for i,j in Atmoscopedata).intersection(x for x,y in Aeronetdata))
    
    
    Atmoscopemapping = dict((a, b) for a, b in Atmoscopedata)
    Atmoscoperesult = [Atmoscopemapping[x] for x in sorted(AtmosAero)]
        
    
    Aeronetmapping = dict((a, b) for a, b in Aeronetdata) 
    Aeronetresult = [Aeronetmapping[i] for i in sorted(AtmosAero)] 
    
    print("The number of points with same time is %i"  %(len(AtmosAero)))
    
    ### plotted Aeronet PWV vs Atmoscope sky temperature
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(Atmoscoperesult,Aeronetresult,s=1,color='red')
    #ax.set_title('Aeronet PWV vs Atmoscope IR sky temp')
    ax.set_ylabel('AERONET PWV (mm)')
    ax.set_xlabel('Atmoscope Infrared sky temp ($^\circ$C)')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("Aeronet-Atmos")
    fig.show()

    # converted the data into x and y numpy arrays
    
    x = np.array(Atmoscoperesult, dtype=float)
    y = np.array(Aeronetresult, dtype=float)
    

    # fitted the data and found the relationship between Aeronet PWV and Atmoscope IR temperature
    
    fitting=np.polyfit(x, np.log(y), 1, w=np.sqrt(y))
    xx = np.linspace(-20, 16, 500)
    yy=[np.exp(fitting[1])*np.exp(fitting[0]*i) for i in xx]
    
    #found PWV as given by model
    
    AtmoscopePWV=[ np.exp(fitting[1])*np.exp(fitting[0]*i)  for i in skytemp_atmoscope]
   
    for i,j in zip(fullAtmoscopetime,AtmoscopePWV):
        AtmoscopePWVdata.write('%s,%5.2f\n' %(i,j)) #writing Atmoscope data to file
    
    
    
    # plots the fit between Aeronet PWV vs Atmoscope sky temp
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x,y,color='red',s=1,zorder=1) 
    ax.plot(xx,yy,'blue',label='fitted line y=%f*e^%fx' %(np.exp(fitting[1]),fitting[0]))
    ax.set_title('Aeronet PWV vs Atmoscope IR')
    ax.set_ylabel('AERONET PWV (mm)')
    ax.set_xlabel('Atmoscope Infrared sky temp ($^\circ$C)')
    ax.grid(True)
    ax.legend()
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("Aeronet-Atmosfit")
    fig.show()
    
    ########## plots callibrated Atmoscope data as govern by fit 
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(fullAtmoscopetime,AtmoscopePWV,s=1,color='blue')
    ax.set_title('callibrated Atmoscope PW vs Time at H.E.S.S')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('period')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("Atmoscalibrateddata")
    fig.show()
    
    
    
######################################################################   
    print ("Callibration completed")
######################################################################

# Opening H.E.S.S data for caliberation
if select == 2 :    # Part TWO

     
    fin=open("radio.dat",'r') 
    
    def zero_to_nan(values):
            return [float('nan') if x >= 0 else x for x in values]
        
    def one_to_nan(values):
            return [float('nan') if x < -100 else x for x in values]    

    def delete_to_nan(values):
            return [float('nan') if x < -100 else x for x in values]
        
    def two_to_nan(values):
            return [float('nan') if x < -100  else x for x in values]    
        
    def remove3_to_nan(values):
            return [float('nan') if x < -100 else x for x in values]
        
    
    CT1skyt=[]
    CT2skyt=[]
    CT3skyt=[]
    CT4skyt=[]
    
    CTtime=[]
    CTUTC=[]
       
    
    P1=9.614
    P0=-62.46
    
    for line in fin:
        run_no=float(line.split()[0])
        
        
        skyt_ct1=float(line.split()[1])
        CT1_zenith=float(line.split()[2])
        CT1_azimuth=float(line.split()[3])
        
        
        
        #print(skyt_ct1,Tz1)
        
        skyt_ct2=float(line.split()[4])
        CT2_zenith=float(line.split()[5])
        CT2_azimuth=float(line.split()[6])
        
        
        
       # print(skyt_ct1,Tz2)
        
        skyt_ct3=float(line.split()[7])
        CT3_zenith=float(line.split()[8])
        CT3_azimuth=float(line.split()[9])
        
        
        
        
        
        
        
        skyt_ct4=float(line.split()[10])
        CT4_zenith=float(line.split()[11])
        CT4_azimuth=float(line.split()[12])
        unix=float(line.split()[13])
        
        
        
        
        
        amb_T=float(line.split()[8])
        humid=float(line.split()[9])
        
        
        
        UTC=datetime.fromtimestamp(unix)
        UTCtime=UTC.replace(microsecond=0)
        UTCdate=UTC.replace(second=0, microsecond=0)
        
        CTtime.append(UTCtime)
        CTUTC.append(UTCdate)   
        
        if CT1_zenith != 0.0:
            
            z_theta1=90-CT1_zenith
            x_z1=(1/np.cos(np.deg2rad(z_theta1)))
            Tz1=(P1*(1-x_z1)) + skyt_ct1
            CT1skyt.append(Tz1)
              
        
        if CT1_zenith == 0.0: 
            CT1skyt.append(0.0) 
          
            
        if CT2_zenith != 0.0:
            
            z_theta2=90.0-CT2_zenith
            x_z2=(1/np.cos(np.deg2rad(z_theta2)))  
            Tz2=(P1*(1-x_z2)) + skyt_ct2
            CT2skyt.append(Tz2)
            
        if CT2_zenith == 0.0:   
            CT2skyt.append(0.0)
            
        
        if CT3_zenith != 0.0:
            
            z_theta3=90.0-CT3_zenith
            x_z3=(1/np.cos(np.deg2rad(z_theta3)))
            Tz3=(P1*(1-x_z3)) + skyt_ct3    
            CT3skyt.append(Tz3)
           
            
        if CT3_zenith == 0.0:
            CT3skyt.append(0.0) 
        
        if CT4_zenith != 0.0:
        
            z_theta4=90.0-CT4_zenith
            x_z4=(1/np.cos(np.deg2rad(z_theta4)))
            Tz4=(P1*(1-x_z4)) + skyt_ct4
            CT4skyt.append(Tz4)
              
        if CT4_zenith == 0.0:
            CT4skyt.append(0.0) 
        
        
    fin.close()    
    
    ############################# plotting to data  ##########################
   
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CTtime,CT1skyt,s=3,color='blue')
    ax.set_title('CT1 infrared Sky temp')
    ax.set_ylabel('infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('time')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("rawskyCT1")
    fig.show()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CTtime,CT2skyt,s=3,color='red')
    ax.set_title('CT2 infrared Sky temp')
    ax.set_ylabel('infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('time')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("rawskyCT2")
    fig.show()
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CTtime,CT3skyt,s=3,color='green')
    ax.set_title('CT3 infrared Sky temp')
    ax.set_ylabel('infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('time')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("rawskyCT3")
    fig.show()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CTtime,CT4skyt,s=3,color='purple')
    ax.set_title('CT4 infrared Sky temp')
    ax.set_ylabel('infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('time')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("rawskyCT4")
    fig.show()
    
    
    
    ###################### inspection of data #################################
    
    ##### To see if the CT telescopes are recording the same temperature ######
    #### ploting against each other
    ###########################################################################

    
    

    print("--unflagged raw data--")
    
    # raw plot CT1 vs CT2 plot
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CT1skyt,CT2skyt,s=3,color='blue')
    ax.set_title('CT1 vs CT2')
    ax.set_ylabel('CT2 infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('CT1 infrared Sky temp ($^\circ$C)')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("unskytCT1CT2")
    fig.show()
    
    # raw plot CT1 vs CT4 plots
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CT1skyt,CT4skyt,s=3,color='red')
    ax.set_title('CT1 vs CT4')
    ax.set_ylabel('CT4 infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('CT1 infrared Sky temp ($^\circ$C)')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("unskytCT1CT4")
    fig.show()
    
    # raw plot CT2 vs CT4 plot
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CT2skyt,CT4skyt,s=3,color='green')
    ax.set_title('CT2 vs CT4')
    ax.set_ylabel('CT4 infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('CT2 infrared Sky temp ($^\circ$C)')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("unskytCT2CT4")
    fig.show()
    
    # raw plot CT1 vs CT3 plot
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CT1skyt,CT3skyt,s=3,color='purple')
    ax.set_title('CT1 vs CT3')
    ax.set_ylabel('CT3 infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('CT1 infrared Sky temp ($^\circ$C)')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("unskytCT1CT3")
    fig.show()
    
    # raw plot CT2 vs CT3 plot
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CT2skyt,CT3skyt,s=3,color='yellow')
    ax.set_title('CT2 vs CT3')
    ax.set_ylabel('CT3 infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('CT2 infrared Sky temp ($^\circ$C)')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("unskytCT2CT3")
    fig.show()
    
    # raw plot CT3 vs CT4 plot
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CT3skyt,CT4skyt,s=3,color='grey')
    ax.set_title('CT3 vs CT4')
    ax.set_ylabel('CT4 infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('CT3 infrared Sky temp ($^\circ$C)')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("unskytCT3CT4")
    fig.show()
    
    
    ############### removing outliers and flagging of data ###################
    print("------unwanted data flagged------")
     
    CT1sky=zero_to_nan(CT1skyt)
    CT1sky=one_to_nan(CT1sky)

    CT2sky=zero_to_nan(CT2skyt)
    CT2sky=two_to_nan(CT2sky)

    CT3sky=zero_to_nan(CT3skyt)
    CT3sky=remove3_to_nan(CT3sky)

    CT4sky=zero_to_nan(CT4skyt)
    CT4sky=delete_to_nan(CT4sky)
   
    # removing nan values from  CT 1 and CT 2 data 
    CTs12=[(i,j) for i,j in zip(CT1sky,CT2sky) if str(i) != 'nan' and str(j) != 'nan'] 
    # splitting CTs12 in CT1 AND CT2
    x11=[i[0] for i in CTs12]
    y11=[i[1] for i in CTs12]
    
    # calculating the Pearson Coefficient of CT1 and CT2
    corr12, p12 = pearsonr(x11, y11)
    print(corr12,p12)
    
    # plotting CT1 vs CT3
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CT1sky,CT2sky,s=3,color='blue')
    ax.set_title('CT1 vs CT2 after flagging')
    ax.set_ylabel('CT2 infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('CT1 infrared Sky temp ($^\circ$C)')
    ax.text(2, 6, r'$\rho$=%f' %(corr12), fontsize=12)
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("flagskyCT1CT2")
    fig.show()
    
    # removing nan values from CT1 and CT3 data
    CTs13=[(i,j) for i,j in zip(CT1sky,CT3sky) if str(i) != 'nan' and str(j) != 'nan']
    
    # splitting CTs13 to CT1 and CT3 clean list
    x13=[i[0] for i in CTs13]
    y13=[i[1] for i in CTs13]
    
    # calculating the Pearson Coefficient of CT1 and CT3
    corr13, p13 = pearsonr(x13, y13)
    print(corr13,p13)
    
    # Plotting CT1 VS CT3
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CT1sky,CT3sky,s=3,color='purple')
    ax.set_title('CT1 vs CT3 after flagging')
    ax.set_ylabel('CT3 infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('CT1 infrared Sky temp ($^\circ$C)')
    ax.text(2, 6, r'$\rho$=%f' %(corr13), fontsize=12)
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("flagskyCT1CT3")
    fig.show()
    
    # removing nan values from CT1 and CT4 data
    CTs14=[(i,j) for i,j in zip(CT1sky,CT4sky) if str(i) != 'nan' and str(j) != 'nan']
    # splitting CTs14 to CT1 and CT4 clean list
    x14=[i[0] for i in CTs14]
    y14=[i[1] for i in CTs14]
    # calculating the Pearson Coefficient of CT1 and CT3
    corr14, p14 = pearsonr(x14, y14)
    print(corr14,p14)
    
    # Plotting CT 1 vs CT 4
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CT1sky,CT4sky,s=3,color='red')
    ax.set_title('CT1 vs CT4 after flagging')
    ax.set_ylabel('CT4 infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('CT1 infrared Sky temp ($^\circ$C)')
    ax.text(2, 6, r'$\rho$=%f' %(corr14), fontsize=12)
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("flagskyCT1CT4")
    fig.show()
    
    
     # removing nan values from CT2 and CT4 data
    CTs24=[(i,j) for i,j in zip(CT2sky,CT4sky) if str(i) != 'nan' and str(j) != 'nan']
    # splitting CTs24 to CT2 and CT4 clean list
    x24=[i[0] for i in CTs24]
    y24=[i[1] for i in CTs24]
    # calculating the Pearson Coefficient of CT2 and CT4
    corr24, p24 = pearsonr(x24, y24)
    print(corr24,p24)
    
    # Plotting CT 2 vs CT 4
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CT2sky,CT4sky,s=3,color='green')
    ax.set_title('CT2 vs CT4 after flagging')
    ax.set_ylabel('CT4 infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('CT2 infrared Sky temp ($^\circ$C)')
    ax.text(2, 6, r'$\rho$=%f' %(corr24), fontsize=12)
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("flagskyCT2CT4")
    fig.show()
    
    
    # removing nan values from CT2 and CT3 data
    CTs23=[(i,j) for i,j in zip(CT2sky,CT3sky) if str(i) != 'nan' and str(j) != 'nan']
    # splitting CTs23 to CT2 and CT3 clean list
    x23=[i[0] for i in CTs23]
    y23=[i[1] for i in CTs23]
    # calculating the Pearson Coefficient of CT2 and CT3
    corr23, p23 = pearsonr(x23, y23)
    print(corr23,p23)
    
    # Plotting CT2 vs CT3
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CT2sky,CT3sky,s=3,color='yellow')
    ax.set_title('CT2 vs CT3 after flagging')
    ax.set_ylabel('CT3 infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('CT2 infrared Sky temp ($^\circ$C)')
    ax.text(2, 6, r'$\rho$=%f' %(corr23), fontsize=12)
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("flagskyCT2CT3")
    fig.show()
    
    # removing nan values from CT3 and CT4 data
    CTs34=[(i,j) for i,j in zip(CT3sky,CT4sky) if str(i) != 'nan' and str(j) != 'nan']
    # splitting CTs34 to CT3 and CT4 clean list
    x34=[i[0] for i in CTs34]
    y34=[i[1] for i in CTs34]
    # calculating the Pearson Coefficient of CT3 and CT4
    corr34, p34 = pearsonr(x34, y34)
    print(corr34,p34)
    
    # plottinfg CT3 vs CT4
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CT3sky,CT4sky,s=3,color='grey')
    ax.set_title('CT3 vs CT4 flagging')
    ax.set_ylabel('CT4 infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('CT3 infrared Sky temp ($^\circ$C)')
    ax.text(2, 6, r'$\rho$=%f' %(corr34), fontsize=12)
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("flagskyCT3CT4")
    fig.show()
    
    ############################ calibrated plots after flagging of data ##########################
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CTtime,CT1sky,s=3,color='blue')
    ax.set_title('CT1 infrared Sky temp after calibration')
    ax.set_ylabel('infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('time')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("calskyCT1")
    fig.show()
    
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CTtime,CT2sky,s=3,color='red')
    ax.set_title('CT2 infrared Sky temp after calibration')
    ax.set_ylabel('infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('time')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("calskyCT2")
    fig.show()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CTtime,CT3sky,s=3,color='green')
    ax.set_title('CT3 infrared Sky temp after calibration')
    ax.set_ylabel('infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('time')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("calskyCT3")
    fig.show()
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.scatter(CTtime,CT4sky,s=3,color='purple')
    ax.set_title('CT4 infrared Sky temp after calibration')
    ax.set_ylabel('infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('time')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("calskyCT4")
    fig.show()
    
    ##### finding the Average & standard deviation of all CT 1-4 radiometer data ######
    
    CTs14ave=[]
    CTs14std=[]
    
    for i,k,m,n in zip(CT1sky,CT2sky,CT3sky,CT4sky):
        CTs=[i,k,m,n]
        aveCTs=np.mean(CTs)
        sttdCTs=np.std(CTs)
        CTs14ave.append(aveCTs)
        CTs14std.append(sttdCTs)
        
        
    CTs14ave=zero_to_nan(CTs14ave)
    CTs14stde=zero_to_nan(CTs14std)
       
    
    ########====== Atmoscope PWV for CALIBRATION with CT's =====######
    
    # reading in and processing Atmoscope data
    
    y=6.5*(10**-3)
    Atmoscopetime=[]
    skytemp_atmoscope=[]

    for file in sorted(glob.glob('/home/thecuriosvambo/Documents/codes/hesspart/*.dat')):
        with open(file) as f:
            # skipping and passing the Header titles and not reading them
            for line in islice(f, 1, None):
                pass
            
                # Extracting the temperature and cloud height and converting it into a useful number
                temperature=float(line.split()[2]) 
                cloud_altitude=float(line.split()[7])
                
                # skipping and not reading inthe data when the instruments where at the inital point and not recording useful data
                if  temperature <= -50.0:
                    continue
                
                # extracts the date and time from the file
                Datetime=line.split()[0]
                # extract date and converst it to a float (useful number)
                date=Datetime.split('_')[0]
                year=int(date.split('-')[0])
                month=int(date.split('-')[1])
                day=int(date.split('-')[2])
                # extracts the time and converts it into a useful number
                time=Datetime.split('_')[1]
                hour=int(time.split(':')[0])
                minute=int(time.split(':')[1])
                sec=int(time.split(':')[2])
                
                # Conversion to julian dates
                dateHuman = datetime(year, month, day, hour, minute)
                Atmoscopetime.append(dateHuman)
                
                    
                # Calculating the PWV from the ambient temp,cloud altitude altitude and gradient temperature.
                T0=temperature  # ( degrees Celscius)
                h=cloud_altitude  #(m)
                
                # MWS 3 & 485-Sensors with Microprocessor without datalogger manual
                
                # Formula to calculate the cloud temperature, page 9 section 3.2.6 The clouds Sensor WKS 485
                T=T0-h*y    # (K)   T=cloud temperature temperature,T0=ambient temp, y=gradient temperature 
                #T= T - 273.15  # (Degrees celcius) 
                
                skytemp_atmoscope.append(T)
                
    f.close()
    
    
    
    
    #######################################################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    
    ################### CT AND ATMOSCOPE DATA CALIBRATION #####################
    
    ###########################################################################
    ###########################################################################
    
    # CT sky temp data
    allCTdata=[i for i in zip(CTUTC,CTs14ave,CTs14std) if i[1] > -90]
    
    CTdata=[(i[0],i[1]) for i in allCTdata]
    CTsttd=[(i[0],i[2]) for i in allCTdata]
    
    
    newCTdata=[i for i in zip(CTtime,CTs14ave,CTs14std) if i[1] > -90]
    
    CTtime=[i[0] for i in newCTdata]
    CTs14ave=[i[1] for i in newCTdata]
    CTs14std=[i[2] for i in newCTdata]
    
    # Atmoscope data sky temp and calibrated PWV
    AtmoscopePWV=[ np.exp(2.08874992)*np.exp(0.07109687*i)  for i in skytemp_atmoscope]  ### As gain from the first relationship,between the atmoscope and Aeronet 
    Atmoscopedata=[i for i in zip(Atmoscopetime,skytemp_atmoscope)]
    AtmoscopePWVdata=[i for i in zip(Atmoscopetime,AtmoscopePWV)]
    
    # finding data that overlap between Atmoscope and CT
    
    AtmosCT=list(set(i for i,j in AtmoscopePWVdata).intersection(x for x,y in CTdata))
    
    # Overlapping Atmoscope PWV
    
    Atmoscopemapping = dict((a, b) for a, b in AtmoscopePWVdata)
    Atmoscoperesult = [Atmoscopemapping[x] for x in sorted(AtmosCT)]
        
    # Overlap CT sky temp and Standard deviation
    CTmapping = dict((a, b) for a, b in CTdata) 
    CTresult = [CTmapping[i] for i in sorted(AtmosCT)] 
    
    CTsttdmapping = dict((a, b) for a, b in CTsttd) 
    CTsttdresult = [CTsttdmapping[i] for i in sorted(AtmosCT)] 
    
    print("The number of points with same time is %i"  %(len(AtmosCT)))
    
    # removing nan values from overlapping CT,Atmoscope and standard deviation results
    
    XY=[i for i in zip(CTresult,Atmoscoperesult,CTsttdresult) if str(i[0]) != 'nan' ]
    
    X=np.array([i[0] for i in XY])
    Y=np.array([i[1] for i in XY])
    S=np.array([i[2] for i in XY])
    
    print("The number of points without 'nan' with the same time is %i"  %(len(X)))
    
    #########Ploting averaged sky temp calibrated plot
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.errorbar(CTtime,CTs14ave,yerr=CTs14std,color='red',markersize=3,fmt='o',alpha=1)
    ax.set_title('CT mean IR sky temperature at H.E.S.S')
    ax.set_ylabel('infrared Sky temp ($^\circ$C)')
    ax.set_xlabel('time')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("CTrawdata")
    fig.show()
    
    
    ### Ploting overlapping results against each other to find relationship 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.errorbar(X,Y,xerr=S,color='red',markersize=3,fmt='o')
    ax.set_title('Atmoscope PWV vs CT mean IR sky temp')
    ax.set_ylabel('Atmoscope PWV (mm)')
    ax.set_xlabel('CT mean infrared Sky temp ($^\circ$C)')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("Atmos-CT")
    fig.show()

    X = np.array(X, dtype=float)
    Y = np.array(Y, dtype=float)
    S = np.array(S, dtype=float)
    
    lin=np.polyfit(X, np.log(Y), 1, w=np.sqrt(Y))
    XX = np.linspace(-100, -20, 500)
    YY=[np.exp(lin[1])*np.exp(lin[0]*i) for i in XX]
    
    
    # Finding the relationship between CT sky temp and Atmoscope PWV
    
    #lin=np.polyfit(X,Y,1)
    print("A=%f" %(np.exp(lin[1])))
    print("B=%f" %(lin[0]))
    print("the equation is given by y=Ae^(Bx)")
    print("y=%f*e^%fx" %(np.exp(lin[1]),lin[0]))
    
    
    #Ploting the fit onto the grapgh
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.errorbar(X,Y,xerr=S,color='red',fmt='o',markersize=3,alpha=0.3,zorder=1,label="fitted data")
    ax.set_title('Atmoscope PWV vs CT mean IR sky temperaturature')
    ax.plot(XX,YY,'blue',label='fitted line y=%f*e^%fx' %(np.exp(lin[1]),lin[0]))
    ax.set_ylabel('Atmoscope PWV (mm)')
    ax.set_xlabel('CT mean infrared Sky temp ($^\circ$C)')
    ax.grid(True)
    ax.legend()
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("Atmos-CTfitt")
    fig.show()

    
    
    CTPWVdata=open('CTPWV.csv','w')  # Opening new file to write CT PWV results as given by fit
    
    #CTPWV=[ float(lin[0])*i+float(lin[1])  for i in CTs14ave] # PWV as given by fit
    CTPWV=[ np.exp(lin[1])*np.exp(lin[0]*i)  for i in CTs14ave]
    
    #Error propagation from Sky temp to PWV
    CTPWVstd=[np.sqrt(((lin[1]*lin[0])*(np.exp(lin[0]*i)))*(p**2)) for i,p in zip(CTs14ave,CTs14std)]   
    
    for i,j,k in zip(CTtime,CTPWV,CTPWVstd):
        CTPWVdata.write('%s,%5.2f,%5.2f\n' %(i,j,k)) #wirting on to File
    
    
    
    # Plotting CT PWV results 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([],[])
    ax.errorbar(CTtime,CTPWV,yerr=CTPWVstd,markersize=3,color='blue',fmt='o',alpha=1)
    ax.set_title('mean callibrated CT PWV at H.E.S.S')
    ax.set_ylabel('PWV (mm)')
    ax.set_xlabel('time')
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("CTcallibrateddata")
    fig.show()

    print ("Calibration Completed")