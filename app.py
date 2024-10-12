import streamlit as st
import preprocessor
import helper
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")


    df=preprocessor.preprocess(data)
    
    # Fetch uniques user

    user_list=df["user"].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

      # Create a selectbox for user selection
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # Show analysis button
    if st.sidebar.button("Show Analysis"):
        # Stats Area
        num_message,word,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_message)
        with col2:
            st.header("Total Words")
            st.title(word)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
            
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        
        #Monthly Timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.rcParams['font.family'] = 'DejaVu Sans'
        ax.plot(timeline["time"],timeline["message"],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #Daily timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.rcParams['font.family'] = 'DejaVu Sans'
        ax.plot(daily_timeline["only_date"],daily_timeline["message"],color="orange")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)


        # Activity map
        st.title("Acitvity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most Busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color="Red")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="blue")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        
        st.title("Weekly Activity Map")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)

        


        # Finding the busiest user in Group (Group Level)
        if selected_user == "Overall":
            st.title("Most Busy User")
            
            # Fetch the most busy user data
            x ,new_df= helper.most_busy_user(df)
            
            # Create a figure and axis
            fig, ax = plt.subplots()  # Set figure size here

            
            # Create two columns
            col1, col2 = st.columns(2)

            with col1:
                # Plot the bar chart on the ax
                ax.bar(x.index, x.values, color='skyblue')
            
                # Set labels and title
                ax.set_xlabel('Users')
                ax.set_ylabel('Message Count')
                ax.set_title('Top 5 Active Users')
                
                # Rotate x-axis labels for readability
                plt.xticks(rotation=45)
                # Display the figure in Streamlit
                st.pyplot(fig)
            with col2:
    
                st.dataframe(new_df)
        
        #WordCloud
        st.title("Word Cloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        #Most Common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        # Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)  # Display the dataframe

        with col2:
            fig, ax = plt.subplots()
            
            # Assuming emoji_df[0] contains emojis and emoji_df[1] contains their counts
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            
            # Make sure to display the pie chart
            st.pyplot(fig)


