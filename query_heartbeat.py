import requests
from urllib.request import urlopen
#from urrlib2 import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from time import gmtime, strftime
from datetime import timedelta
import smtplib
from email.mime.text import MIMEText
import os

def creatURL(idN, t):
    Ntu=['7507', '3039', '3038', '3040', '2026']
    if idN in Ntu:
        string = "www.database.com".format(idN,t)
        return string
    else:
        string = "www.database.com".format(idN,t)
        return string   

def query_data(arg1):
    r = requests.get(arg1) # URL path
    soup = BeautifulSoup(r.text,'lxml')
    a = list(soup.find_all('p'))

    # Split the list through the regular expression
    d = re.split('\s+|,|<br/>|<p>|</p>',str(a))

    # Remove the '' element from the list
    d = list(filter(lambda zz: zz != '', d)) 

    # Remove the '=' element from the list
    d = list(filter(lambda zz: zz != '=', d))

    # Remove the '[' & ']' element from the list
    try:
        d.remove(']')
        d.remove('[')
    except:
        pass
    
    return d

def calculateOFFtime(d):
    
    if ("No" in d) & ("results" in d):
        outputStr = "離線狀態 ,超過一天無接收到資料!!"

    else:
    # Create a dataframe from the URL by data crawling
        colName=['id', 'time', 'weather', 'air','acceleration','cleavage','incline','field1','field2','field3']
        _Num = 0
        _df  = pd.DataFrame(columns=colName)
        df   = pd.DataFrame(columns=colName)

        for ii in range(0,len(d)):    
            while colName[_Num] in d[ii]:
                _lst = d[ii + 1]
                _lst = _lst.strip(',')

                if _lst == '' or (_lst in colName):
                    _lst = None       

                _df[colName[_Num]] = [_lst] # Put the list into the dataframe
                if _Num < (len(colName)-1):
                    _Num += 1
                else:
                    df = df.append(_df, ignore_index=True)
                    _Num = 0 

        # Convert argument to a numeric type(float64 or int64)
        #waterlevel = ['time', 'id','depth','field1','field2']
        #for ii in numericCol:
        #    df[ii] = pd.to_numeric(df[ii])

        # Convert the format of date
        dates = df.time
        df.index = pd.to_datetime(dates.astype(str), format='%Y%m%d%H%M%S')
        df.index.name = 'time'
        del df['time']

        # Check dataframe format
        # df.info()

        # Query the latest time stamp
        lastestTimeStr = df.index[-1]

        # Release the memory
        del df

        # Calculate the offline time
        localTimeStamp = pd.to_datetime(strftime("%Y%m%d%H%M%S"), format="%Y%m%d%H%M%S")
        deltaT = localTimeStamp - lastestTimeStr
        alrTimeIntv = timedelta(minutes = 30)

        if deltaT > alrTimeIntv:

            deltaDay = deltaT.days
            deltaHr  = deltaT.seconds // 3600
            deltaMin = (deltaT.seconds % 3600) // 60
            deltaSec = deltaT.seconds % 60

            outputStr = "離線狀態，距離上次接收到資料時間: {} day, {} hr, {} min, {} sec".format(deltaDay,deltaHr, deltaMin, deltaSec)
        else:
            outputStr = "Online"            
    return outputStr

def WcalculateOFFtime(d):
    
    if ("No" in d) & ("results" in d):
        outputStr = "離線狀態 ,超過一天接收到資料!!"

    else:
    # Create a dataframe from the URL by data crawling
        colName=['id', 'time', 'depth', 'field1','field2']
        _Num = 0
        _df  = pd.DataFrame(columns=colName)
        df   = pd.DataFrame(columns=colName)

        for ii in range(0,len(d)):    
            while colName[_Num] in d[ii]:
                _lst = d[ii + 1]
                _lst = _lst.strip(',')

                if _lst == '' or (_lst in colName):
                    _lst = None       

                _df[colName[_Num]] = [_lst] # Put the list into the dataframe
                if _Num < (len(colName)-1):
                    _Num += 1
                else:
                    df = df.append(_df, ignore_index=True)
                    _Num = 0 

        # Convert argument to a numeric type(float64 or int64)
        #waterlevel = ['time', 'id','depth','field1','field2']
        #for ii in numericCol:
        #    df[ii] = pd.to_numeric(df[ii])

        # Convert the format of date
        dates = df.time
        df.index = pd.to_datetime(dates.astype(str), format='%Y%m%d%H%M%S')
        df.index.name = 'time'
        del df['time']

        # Check dataframe format
        # df.info()

        # Query the latest time stamp
        lastestTimeStr = df.index[-1]

        # Release the memory
        del df

        # Calculate the offline time
        localTimeStamp = pd.to_datetime(strftime("%Y%m%d%H%M%S"), format="%Y%m%d%H%M%S")
        deltaT = localTimeStamp - lastestTimeStr
        alrTimeIntv = timedelta(minutes = 60)

        if deltaT > alrTimeIntv:

            deltaDay = deltaT.days
            deltaHr  = deltaT.seconds // 3600
            deltaMin = (deltaT.seconds % 3600) // 60
            deltaSec = deltaT.seconds % 60

            outputStr = "離線狀態，距離上次接收到資料時間: {} day, {} hr, {} min, {} sec".format(deltaDay,deltaHr, deltaMin, deltaSec)
        else:
            outputStr = "Online"            
    return outputStr

# =============================================================================
# def calculateOFFtime_light(d):
#     
#     if ("No" in d) & ("results" in d):
#         outputStr = "離線狀態，無接收到資料"
# 
#     else:    
#     # Create a dataframe from the URL by data crawling
#         colName=['id', 'time', 'weather', 'air','acceleration','cleavage','incline','field1','field2','field3']
#         _Num = 0
#         _df  = pd.DataFrame(columns=colName)
#         df   = pd.DataFrame(columns=colName)
# 
#         for ii in range(0,len(d)):    
#             while colName[_Num] in d[ii]:
#                 _lst = d[ii + 1]
#                 _lst = _lst.strip(',')
# 
#                 if _lst == '' or (_lst in colName):
#                     _lst = None       
# 
#                 _df[colName[_Num]] = [_lst] # Put the list into the dataframe
#                 if _Num < (len(colName)-1):
#                     _Num += 1
#                 else:
#                     df = df.append(_df, ignore_index=True)
#                     _Num = 0 
# 
#         # Convert argument to a numeric type(float64 or int64)
#         #numericCol = ['roll', 'pitch', 'yaw','field1','field2','field3']
#         #for ii in numericCol:
#         #    df[ii] = pd.to_numeric(df[ii])
# 
#         # Convert the format of date
#         dates = df.time
#         df.index = pd.to_datetime(dates.astype(str), format='%Y%m%d%H%M%S')
#         df.index.name = 'time'
#         del df['time']
# 
#         # Check dataframe format
#         # df.info()
# 
#         # Query the latest time stamp
#         lastestTimeStr = df.index[-1]
# 
#         # Release the memory
#         del df
# 
#         # Calculate the offline time
#         localTimeStamp = pd.to_datetime(strftime("%Y%m%d%H%M%S"), format="%Y%m%d%H%M%S")
#         deltaT = localTimeStamp - lastestTimeStr
#         alrTimeIntv = timedelta(minutes = 40)
# 
#         if deltaT > alrTimeIntv:
# 
#             deltaDay = deltaT.days
#             deltaHr  = deltaT.seconds // 3600
#             deltaMin = (deltaT.seconds % 3600) // 60
#             deltaSec = deltaT.seconds % 60
# 
#             outputStr = "Offline time: {} day, {} hr".format(deltaDay,deltaHr)
#         else:
#             outputStr = "Online"            
#     return outputStr
# =============================================================================


locationList = ["Demo", "FD01_RMO"]
#locationList = ["Taipei"]
saveFid  =[]

for location in locationList:
    idNumList = []
    DBName =""
    DBname1 =""
    queryDate = strftime("%Y%m%d")
    quertMonth = strftime("%Y%m")
    now = strftime("%Y%m%d%H%M")

    if (location.lower() == "demo"):
        idNumDict  = [{'name':'介壽村','id':'3040'}, # 0
                      {'name':'復興村','id':'3038'}, # 1
                      {'name':'珠螺村','id':'3039'}, # 2
                      {'name':'港口','id':'2026'}]
        DBName = "雨量計"
        DB1 = "rain"
    elif (location.lower() == "fd01_rmo"):
        idNumDict  = [{'name':'介壽村','id':'7504'},
                      {'name':'復興村','id':'7505'},
                      {'name':'珠螺村','id':'7506'},
                      {'name':'港口','id':'7507'}]
        DBName = "水位計"
        DB1 = "waterlevel"
    else:
        print("No such name.")


    flag = 0
    for ii in range(0, len(idNumDict)):
        
        URLstr = creatURL(str(idNumDict[ii]["id"]),queryDate) # Format in (id_Num, yyyymm)
        # print("Look at here:" + URLstr)
        qD = query_data(URLstr)
        #print(qD)
        if ("No" in qD) & ("results" in qD):
            #print("{} 離線超過一天！".format(idNumDict[ii]["id"]))
            URLstr = creatURL(str(idNumDict[ii]["id"]),quertMonth)
            qD = query_data(URLstr)    
        if idNumDict[ii]["id"] in ['3039', '3038', '3040', '2026']:
            writingStr = calculateOFFtime(qD)
        else:
            writingStr = WcalculateOFFtime(qD)

        if (ii == 0):
            queryFid = "{}_hearbeatList.txt".format(DB1)
            saveFid  += [queryFid]

        if (flag == 0):
            with open(queryFid, "a") as file:
                file.write("---------------儀器目前狀況---------------")
                file.write("\n")
                file.write("儀器類別: " + DBName)
                file.write("\n")
                file.write("上次收到資料時間: {}".format(strftime("%Y/%m/%d %H:%M")))
                file.write("\n")
                flag = 1   
        with open(queryFid, "a") as file:
            writing = "{}    {}    {}".format(idNumDict[ii]["name"],idNumDict[ii]["id"],writingStr)
            file.write(writing)
            file.write("\n")
        #print(str(idNumDict[ii]["id"]) + "  Done.")


# Send a e-mail
smtpssl=smtplib.SMTP_SSL("smtp.gmail.com", 465)
smtpssl.ehlo()
smtpssl.login("icebergtek.mail@gmail.com", "odiedag8")

msg = ""
for ii in range(0, len(saveFid)):    
    with open(saveFid[ii],'r') as file:
        msg += file.read()       
        
mime = MIMEText(msg, "plain", "utf-8")
mime["Subject"] = "連江縣淹水感知器狀態\n"
msgEmail        = mime.as_string()  

#to_addr  = ["jim@icebergtek.com", "white@icebergtek.com", "ian@icebergtek.com",
#            "yujiachiu@ntu.edu.tw", "yolandadeschanel@gmail.com", "milk920120@gmail.com"]

to_addr  = ["jim@icebergtek.com","zmingwu2011@gmail.com"]          

status = smtpssl.sendmail("icebergtek.mail@gmail.com", 
                          to_addr, 
                          msgEmail)
if status == {}:
    print("Sending e-mail is done.")
    smtpssl.quit()
    
    try:
        #os.remove("/home/pi/query_heartbeat/"+saveFid[0])
        #os.remove("/home/pi/query_heartbeat/"+saveFid[1])
        os.remove(saveFid[0])
        os.remove(saveFid[1])         
    except OSError as e:
        print(e)
    else:
        print("The file is deleted successfully")

else:
    print("Failed to transmit.")
    smtpssl.quit()
