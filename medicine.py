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

# Function to insert data
def insert_medicine(id, name, date, time, compartment):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = "INSERT INTO MedicineRemider (id, Name, Date, Time, compartment) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (id, name, date, time, compartment))
        conn.commit()
        return "New record inserted successfully!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conn.close()

# Function to update data
def update_medicine(id, name, date, time, compartment):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = "UPDATE MedicineRemider SET Name = %s, Time = %s, compartment = %s WHERE id = %s AND Date = %s"
        cursor.execute(sql, (name, time, compartment, id, date))
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
    id = st.number_input("Enter ID", min_value=1, step=1)
    name = st.text_input("Medicine Name")
    date = st.date_input("Date", value=datetime.today())
    time = st.time_input("Time")
    compartment = st.text_input("Compartment")

    if st.button("Insert Data"):
        response = insert_medicine(id, name, date.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), compartment)
        st.success(response)

# **Tab 2: Update Data**
with tab2:
    st.header("Update Medicine Reminder")
    id_update = st.number_input("Enter ID to Update", min_value=1, step=1)
    name_update = st.text_input("New Medicine Name")
    date_update = st.date_input("Date to Update", value=datetime.today())
    time_update = st.time_input("New Time")
    compartment_update = st.text_input("New Compartment")

    if st.button("Update Data"):
        response = update_medicine(id_update, name_update, date_update.strftime("%Y-%m-%d"), time_update.strftime("%H:%M:%S"), compartment_update)
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
