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
        cursor.close()
        conn.close()

# Function to fetch medicine records by date
def get_medicine_by_date(date):
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM MedicineRemider WHERE Date = %s"
        cursor.execute(sql, (date,))
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        return []
    finally:
        cursor.close()
        conn.close()

# Streamlit App
st.title("Medicine Reminder Management")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Insert Data", "Update Data", "Check Data"])

# **Tab 1: Insert Data**
with tab1:
    st.header("Insert Medicine Reminder")
    name = st.text_input("Medicine Name")
    date = st.date_input("Date", value=datetime.today())

    # Time Selection with Spinner (HH:MM format)
    col1, col2 = st.columns(2)
    with col1:
        hour = st.number_input("Hour", min_value=0, max_value=23, step=1, format="%02d")
    with col2:
        minute = st.number_input("Minute", min_value=0, max_value=59, step=1, format="%02d")
    time = f"{hour:02d}:{minute:02d}"  # Formatting time in HH:MM format

    # Dropdown for Compartment Selection (1 to 5)
    compartment = st.selectbox("Select Compartment", [1, 2, 3, 4, 5])

    if st.button("Insert Data"):
        response = insert_medicine(name, date.strftime("%Y-%m-%d"), time, compartment)
        st.success(response)

# **Tab 2: Update Data**
with tab2:
    st.header("Update Medicine Reminder")
    name_update = st.text_input("New Medicine Name")
    date_update = st.date_input("Date to Update", value=datetime.today())

    # Time Selection with Spinner (HH:MM format)
    col1, col2 = st.columns(2)
    with col1:
        hour_update = st.number_input("New Hour", min_value=0, max_value=23, step=1, format="%02d")
    with col2:
        minute_update = st.number_input("New Minute", min_value=0, max_value=59, step=1, format="%02d")
    time_update = f"{hour_update:02d}:{minute_update:02d}"

    # Dropdown for Compartment Selection (1 to 5)
    compartment_update = st.selectbox("Select New Compartment", [1, 2, 3, 4, 5])

    if st.button("Update Data"):
        response = update_medicine(name_update, date_update.strftime("%Y-%m-%d"), time_update, compartment_update)
        st.success(response)

# **Tab 3: Check Data**
with tab3:
    st.header("Check Medicine Reminders by Date")
    date_check = st.date_input("Select Date to View Records", value=datetime.today())

    if st.button("Fetch Data"):
        records = get_medicine_by_date(date_check.strftime("%Y-%m-%d"))
        if records:
            df = pd.DataFrame(records)
            df["Day"] = pd.to_datetime(df["Date"]).dt.day_name()
            st.write(df)
        else:
            st.warning("No records found for the selected date.")
