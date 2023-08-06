from urlextract import URLExtract
from wordcloud import WordCloud
extract=URLExtract()
def help(selected_user,df):
    if selected_user=='Overall':
        num_msg=df.shape[0]
        words=[]
        for message in df['messages']:
            words.extend(message)
        total_media=df[df['messages']=='<Media omitted>\n'].shape[0]  
        links=[]
        for link in df['messages']:
            links.extend(extract.find_urls(link))
        return num_msg,len(words),total_media,len(links)
    else:
        new_df=df[df['user']==selected_user]
        words=[]
        for message in new_df['messages']:
            words.extend(message)
        total_media=new_df[new_df['messages']=='<Media omitted>\n'].shape[0]    
        links=[]
        for link in df['messages']:
            links.extend(extract.find_urls(link))
        return new_df.shape[0],len(words),total_media,len(links)
def busyuser(df):
    most_user=df['user'].value_counts().head()
    all_user=(df['user'].value_counts()/df.shape[0])*100    
    return most_user,all_user 
def wordcloud_fun(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_word=f.read()
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    temp=df[df['user']!='group_notification']   
    temp=temp[temp['messages']!='<Media omitted>\n'] 
    def remove_stop_word(message):
        y=[]
        for word in message.lower().split():
            if word!=stop_word:
                y.append(word)
        return " ".join(y)
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['messages']=temp['messages'].apply(remove_stop_word)
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline=df.groupby(['year','month']).count()['messages'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"_"+ str(timeline['year'][i]))
    timeline['time'] = time     
    return timeline
def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('messagedate').count()['messages'].reset_index()

    return daily_timeline       
   
      

