import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

# Database Configuration
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students",
    "password": "testStudents@123",
    "database": "u263681140_students",
}

# Function to connect to MySQL
def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

# Function to insert data (ID default to 1)
def insert_medicine(name, date, time, compartment):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = "INSERT INTO MedicineRemider (id, Name, Date, Time, compartment) VALUES (1, %s, %s, %s, %s)"
        cursor.execute(sql, (name, date, time, compartment))
        conn.commit()
        return "New record inserted successfully!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Function to update data
def update_medicine(name, date, time, compartment):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = "UPDATE MedicineRemider SET Name = %s, Time = %s, compartment = %s WHERE id = 1 AND Date = %s"
        cursor.execute(sql, (name, time, compartment, date))
        conn.commit()
        return "Record updated successfully!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Function to fetch all medicine records for history
def get_all_history():
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM MedicineRemider ORDER BY Date DESC, Time DESC"
        cursor.execute(sql)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        return []
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Function to fetch medicine records by date
def get_medicine_by_date(date):
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM MedicineRemider WHERE Date = %s"
        cursor.execute(sql, (date,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        return []
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Streamlit App
st.set_page_config(page_title="Medicine Reminder", layout="wide")
st.title("💊 Medicine Reminder Management")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["➕ Insert Data", "📝 Update Data", "🔍 Check by Date", "📜 History"])

# **Tab 1: Insert Data**
with tab1:
    st.header("Insert Medicine Reminder")
    name = st.text_input("Medicine Name", key="ins_name")
    date = st.date_input("Date", value=datetime.today(), key="ins_date")

    col1, col2 = st.columns(2)
    with col1:
        hour = st.number_input("Hour", min_value=0, max_value=23, step=1, format="%02d", key="ins_hour")
    with col2:
        minute = st.number_input("Minute", min_value=0, max_value=59, step=1, key="ins_min")
    
    # Custom Time Formatting: No leading zero for minutes 0-9
    formatted_time = f"{hour:02d}:{minute}" 

    compartment = st.selectbox("Select Compartment", [1, 2, 3, 4, 5, 6], key="ins_comp")

    if st.button("Insert Data", type="primary"):
        if name:
            response = insert_medicine(name, date.strftime("%Y-%m-%d"), formatted_time, compartment)
            st.success(response)
        else:
            st.error("Please enter a medicine name.")

# **Tab 2: Update Data**
with tab2:
    st.header("Update Medicine Reminder")
    name_update = st.text_input("New Medicine Name", key="upd_name")
    date_update = st.date_input("Date to Update", value=datetime.today(), key="upd_date")

    col1, col2 = st.columns(2)
    with col1:
        hour_update = st.number_input("New Hour", min_value=0, max_value=23, step=1, format="%02d", key="upd_hour")
    with col2:
        minute_update = st.number_input("New Minute", min_value=0, max_value=59, step=1, key="upd_min")
    
    formatted_time_update = f"{hour_update:02d}:{minute_update}"
    compartment_update = st.selectbox("Select New Compartment", [1, 2, 3, 4, 5, 6], key="upd_comp")

    if st.button("Update Data"):
        response = update_medicine(name_update, date_update.strftime("%Y-%m-%d"), formatted_time_update, compartment_update)
        st.success(response)

# **Tab 3: Check Data**
with tab3:
    st.header("Check Medicine Reminders by Date")
    date_check = st.date_input("Select Date", value=datetime.today(), key="chk_date")

    if st.button("Fetch Data"):
        records = get_medicine_by_date(date_check.strftime("%Y-%m-%d"))
        if records:
            df = pd.DataFrame(records)
            df["Day"] = pd.to_datetime(df["Date"]).dt.day_name()
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No records found for this date.")

# **Tab 4: History (Past Records)**
with tab4:
    st.header("Past Reminders (History)")
    st.write("Showing all medicines scheduled before current date and time.")
    
    if st.button("Refresh History"):
        all_records = get_all_history()
        
        if all_records:
            now = datetime.now()
            past_data = []

            for row in all_records:
                # Reconstruct time string to handle the missing leading zero in minutes for parsing
                # If time is "10:5", we need to make it "10:05" just for comparison logic
                t_parts = row['Time'].split(':')
                h = int(t_parts[0])
                m = int(t_parts[1])
                
                # Create a datetime object for the record
                # Use .date() to ensure the first argument is a Python date object
                #record_dt = datetime.combine(row['Date'].date(), datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M").time())
                #record_dt = datetime.combine(row['Date'], datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M").time())
                # Add .date() to row['Date']
                record_dt = datetime.combine(pd.to_datetime(row['Date']).date(), datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M").time())
                
                # Check if record is in the past
                if record_dt < now:
                    row['Day'] = record_dt.strftime('%A')
                    past_data.append(row)

            if past_data:
                history_df = pd.DataFrame(past_data)
                st.dataframe(history_df, use_container_width=True)
            else:
                st.info("No past records found.")
        else:
            st.warning("Database is empty.")
