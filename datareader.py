import re
import pandas as pd
def dataread(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP][M]\s-\s'
    messages=re.split(pattern,data)[2:]
    dates=re.findall(pattern,data)[1:]
    dataframe=pd.DataFrame({'usermessages':messages,'messagedate':dates})
    dataframe['messagedate']=pd.to_datetime(dataframe['messagedate'],format='%m/%d/%y, %H:%M %p - ')
    user=[]
    messages=[]
    for message in dataframe['usermessages']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            user.append(entry[1])
            messages.append(entry[2])
        else:
            user.append("group notification")
            messages.append(entry[0])
    dataframe['user']=user
    dataframe['messages']=messages
    dataframe.drop(columns=['usermessages'],inplace=True)
    dataframe['year']=dataframe['messagedate'].dt.year
    dataframe['month']=dataframe['messagedate'].dt.month_name()
    dataframe['days']=dataframe['messagedate'].dt.day_name()
    dataframe['hour']=dataframe['messagedate'].dt.hour
    dataframe['minute']=dataframe['messagedate'].dt.minute
    return dataframe