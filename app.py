import streamlit as st
import datareader,helper
import matplotlib.pyplot as plt
st.title("WhatsApp-Chat-Analyzer")
uploaded_file=st.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=datareader.dataread(data)
    st.dataframe(df)
    user=df['user'].unique().tolist()
    user.sort()
    user.insert(0,"Overall")
    selected_user=st.selectbox("select a single user",user)
    if st.button("Analysis"):
        number_of_msg,words,total_media,links=helper.help(selected_user,df)
        col1, col2, col3,col4= st.columns(4)
        with col1:
            st.header("Total messages")
            st.text(number_of_msg)
        with col2:
            st.header("Total words")
            st.text(words)
        with col3:
            st.header("Media files")
            st.text(total_media) 
        with col4:
            st.header("No of links")
            st.text(links) 
        if selected_user=='Overall':
            col1,col2=st.columns(2)
            x,y=helper.busyuser(df)
            flg,ax=plt.subplots()
         
            with col1:
                st.header('busy users')
                ax.bar(x.index,x.values) 
                plt.xticks(rotation='vertical')
                st.pyplot(flg) 
            with col2:
                st.header("All user's chatt")
                ax.bar(y.index,y.values)
                plt.xticks(rotation='vertical')
                st.pyplot(flg)  
        st.title('wordcloud')
        df_wc=helper.wordcloud_fun(selected_user,df)
        flg,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(flg)
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig) 
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['messagedate'], daily_timeline['messages'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)       
           
