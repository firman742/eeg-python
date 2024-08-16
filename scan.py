import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.title("Real-Time / Live Data EEG Dashboard")

# Connect to MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='eeg',
)

cursor = connection.cursor()

# Fetch data from 'klasifikasi' table
cursor.execute("""
    SELECT k.nis, k.kode_test, k.tanggal_test, k.level,
           s.nama, s.gender, s.tanggal_lahir, s.tempat_lahir, 
           l.kode_level, l.kesiapan, l.deskripsi
    FROM klasifikasi k
    JOIN siswa s ON k.nis = s.nis
    JOIN level l ON k.level = l.kode_level
""")
data = cursor.fetchall()

# Create DataFrame
columns = [
    'NIS', 'Kode Test', 'Tanggal Test', 'Level', 'Nama', 'Gender', 
    'Tanggal Lahir', 'Tempat Lahir', 'Kode Level', 'Kesiapan', 'Deskripsi'
]
df = pd.DataFrame(data, columns=columns)

# Ensure 'Tanggal Test' is in datetime format
df['Tanggal Test'] = pd.to_datetime(df['Tanggal Test'])

# Create a bar chart from 'klasifikasi' data
fig_bar = px.bar(df, x='Tanggal Test', y='Level', title='Test Level Over Time', 
                 labels={'Level': 'Level', 'Tanggal Test': 'Tanggal Test'})

# Show the chart
st.plotly_chart(fig_bar)

# Display detailed information in a card
selected_row = st.selectbox('Select NIS for Details:', df['NIS'])

# Filter the DataFrame for the selected NIS
filtered_df = df[df['NIS'] == selected_row]

if not filtered_df.empty:
    details = filtered_df.iloc[0]

    # Card-like display using markdown with custom HTML/CSS
    st.markdown(f"""
    <div style="background-color:#f9f9f9; padding:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); color: black;">
        <h3 style="text-align:center; color: black;">Detailed Information</h3>
        <div style="display: flex; justify-content: space-between;">
            <div style="width: 45%;">
                <p><strong>Kode Test:</strong> {details['Kode Test']}</p>
                <p><strong>Tanggal Test:</strong> {details['Tanggal Test']}</p>
                <p><strong>Nama:</strong> {details['Nama']}</p>
                <p><strong>Gender:</strong> {details['Gender']}</p>
            </div>
            <div style="width: 45%;">
                <p><strong>Tanggal Lahir:</strong> {details['Tanggal Lahir']}</p>
                <p><strong>Tempat Lahir:</strong> {details['Tempat Lahir']}</p>
                <p><strong>Kode Level:</strong> {details['Kode Level']}</p>
                <p><strong>Kesiapan:</strong> {details['Kesiapan']}</p>
                <p><strong>Deskripsi:</strong> {details['Deskripsi']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("No details found for the selected NIS.")
