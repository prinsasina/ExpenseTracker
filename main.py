import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💸",
)

def initialize_table():
    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()

    cur.execute(""" CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item VARCHAR(50) NOT NULL,
                price INTEGER NOT NULL,
                category VARCHAR(50) NOT NULL,
                date DATE NOT NULL,
                description VARCHAR(100))
    """)
    conn.commit()
    conn.close()

def add(item, price, category, date, description):
    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO expenses (item, price, category, date, description)
                VALUES (?, ?, ?, ?, ?)
                """, (item, price, category, date, description))
    conn.commit()
    conn.close()

initialize_table()
st.title("Expense Tracker")

mode = st.radio("Select input method:", ["Input","File uploading"])

if (mode=="Input"):
    with st.form("expense_form"):
        item = st.text_input("Item: ")
        price = st.number_input("Price: ", min_value=0.0, format="%.2f")
        category = st.text_input("Category: ")
        date = st.date_input("Date: ")
        description = st.text_input("Description: ")

        submitted = st.form_submit_button("Add expense")
        if submitted:
            add(item, price, category, date, description)
            st.success("Expense added")

elif (mode=="File uploading"):
    uploaded_file = st.file_uploader("Upload your input file", type=["csv"])
    if uploaded_file:
        try:
            df_upload = pd.read_csv(uploaded_file)
            st.dataframe(df_upload)
            uploaded = st.button("Upload")
            if uploaded:
                required_columns = {"item", "price", "category", "date", "description"}
                if required_columns.issubset(df_upload.columns):
                    for _, row in df_upload.iterrows():
                        add(row["item"], row["price"], row["category"], row["date"], row["description"])
                    st.success("Expenses uploaded successfully")
        except:
            st.error("Error reading file")

st.subheader("Total expenses")
conn = sqlite3.connect('expenses.db')
df = pd.read_sql_query("""
                        SELECT date, item, price, category, description FROM expenses
                       """, conn)
st.dataframe(df)

sum = pd.read_sql_query("""
                        SELECT SUM(price) FROM expenses
                        """, conn)
st.write(sum)

conn.close()