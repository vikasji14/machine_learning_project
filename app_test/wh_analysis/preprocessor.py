import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:AM|PM)\s-\s'


    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data) 

    df = pd.DataFrame({'user_message': messages, 'message_date':dates})   

    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ') 
    df.rename(columns={'message_date':'date'}, inplace=True) 

    

    users = []
    messages = []

    # Regex pattern for extracting the user and message
    pattern = r'([\w\W]+?):\s'

    # Loop through the 'user_message' and apply regex split
    for message in df['user_message']:
        entry = re.split(pattern, message)
        if len(entry) > 2:
            users.append(entry[1].strip())  # Extract user
            messages.append(entry[2].strip())  # Extract message
        else:
            # For messages without a user (group notifications, etc.)
            users.append('group_notification')
            messages.append(entry[0].strip())  # Keep the entire message as it's a group notification

    # Add the 'user' and 'message' columns to the DataFrame
    df['user'] = users
    df['message'] = messages

    # Drop the original 'user_message' column
    df.drop(columns=['user_message'], inplace=True)

    df['year']=df['date'].dt.year 
    df['month']=df['date'].dt.month_name() 
    df['day']=df['date'].dt.day  
    df['hour']=df['date'].dt.hour 
    df['minute']=df['date'].dt.minute 

    # period = []
    # for hour in df[['day_name', 'hour']]['hour']:
    #     if hour == 23:
    #         period.append(str(hour) + "-" + str('00'))
    #     elif hour == 0:
    #         period.append(str('00') + "-" + str(hour + 1))
    #     else:
    #         period.append(str(hour) + "-" + str(hour + 1))

    # df['period'] = period

    return df