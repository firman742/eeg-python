import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_calendar import calendar
from datetime import datetime

# --------- Custom CSS Style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title('Hi, User')

# Connect to MySQL
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='eeg',
    )

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM eeg_table")
    data = cursor.fetchall()

    # Create DataFrame
    df = pd.DataFrame(data, columns=cursor.column_names)

    # Ensure created_at is in datetime format
    df['created_at'] = pd.to_datetime(df['created_at'])

except mysql.connector.Error as err:
    st.error(f"Error: {err}")
    st.stop()

finally:
    cursor.close()
    connection.close()

# Get today's date
today_date = datetime.today().strftime('%Y-%m-%d')

# Set up calendar options
calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridDay,dayGridWeek,dayGridMonth",
    },
    "initialDate": today_date,  # Start the calendar on today's date
    "initialView": "dayGridMonth",
}

# Sample calendar events (You should populate this from your data)
calendar_events = [
    {
        "title": "Event 1",
        "start": "2023-07-31T08:30:00",
        "end": "2023-07-31T10:30:00",
        "resourceId": "a",
    },
    {
        "title": "Event 2",
        "start": "2023-07-31T07:30:00",
        "end": "2023-07-31T10:30:00",
        "resourceId": "b",
    },
    {
        "title": "Event 3",
        "start": "2023-07-31T10:40:00",
        "end": "2023-07-31T12:30:00",
        "resourceId": "a",
    }
]

# Custom CSS to highlight today
custom_css = f"""
        .fc.fc-media-screen {{
                padding: 20px;
                background-color: #fff;
        }}
        .fc-view-harness, h2.fc-toolbar-title {{
                color: #666;
        }}
        .fc-event-past {{
                opacity: 0.8;
        }}
        .fc-event-time {{
                font-style: italic;
        }}
        .fc-event-title {{
                font-weight: 700;
        }}
        .fc-toolbar-title {{
                font-size: 2rem;
        }}
        .fc-daygrid-day.fc-day-today {{
                background-color: #ffeb3b !important;  /* Highlight today's date */
                font-weight: bold !important;          /* Bold today's date */
        }}
        
        @media (max-width: 768px) {{
                .fc-toolbar-title {{
                        font-size: 1.2rem; /* Further reduce font size for smaller screens */
                }}
                
                .fc-button-group .fc-button {{
                        padding: 5px 8px; /* Smaller button size */
                        font-size: 0.9rem; /* Smaller font size in buttons */
                }}

                .fc .fc-daygrid-day-frame {{
                        padding: 5px; /* Reduce padding around day numbers */
                }}

                .fc .fc-daygrid-day-number {{
                        font-size: 0.9rem; /* Smaller day number font size */
                }}
                
                .fc-daygrid-day-events {{
                        margin-top: 2px; /* Reduce margin for events */
                }}
        }}

        @media (max-width: 480px) {{
                .fc-toolbar-title {{
                        font-size: 1rem; /* Even smaller font size for very small screens */
                }}
                
                .fc .fc-daygrid-day-frame {{
                        padding: 3px; /* Further reduce padding for smaller screens */
                }}

                .fc .fc-daygrid-day-number {{
                        font-size: 0.8rem; /* Smaller day number font size */
                }}
                
                .fc-button-group .fc-button {{
                        padding: 3px 5px; /* Further reduce button size */
                        font-size: 0.8rem; /* Further reduce font size in buttons */
                }}
                
                .fc-daygrid-day-events {{
                        margin-top: 1px; /* Reduce margin for events */
                }}
        }}
        @media (max-width: 320px) {{
                .fc-toolbar-title {{
                        font-size: 0.8rem; /* Even smaller font size for very small screens */
                }}
                
                .fc-today-button {{
                        font-size:0.6rem
                }}
                
                .fc .fc-daygrid-day-frame {{
                        # padding: 3px; /* Further reduce padding for smaller screens */
                }}

                .fc .fc-daygrid-day-number {{
                        font-size: 0.8rem; /* Smaller day number font size */
                }}
                
                .fc-button-group .fc-button {{
                        font-size: 0.4rem; /* Further reduce font size in buttons */
                }}
                
                .fc-col-header {{
                        font-size: 0.6rem;
                }}
                
                .fc-daygrid-day-events {{
                        margin-top: 1px; /* Reduce margin for events */
                }}
        }}
        """

# Display the calendar
st_calendar = calendar(events=calendar_events, options=calendar_options, custom_css=custom_css)
st.write(st_calendar)

st.button("Scan Now!")

# Display scan history with links
st.subheader("Scan History")

# Adjust this to the correct column name
for index, row in df.iterrows():
    link = f"[{row['created_at']}: {row['status']}](/SingleItem?item_id={row['id']})"
    st.markdown(link, unsafe_allow_html=True)
