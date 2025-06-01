import streamlit as st
import pandas as pd
import sqlite3
import matplotlib
import plotly.express as px

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

def delete_row(id):
    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()
    cur.execute("""
                DELETE FROM expenses WHERE id = ?
                """, (id,))
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
            st.dataframe(df_upload, hide_index=True)
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
                        SELECT * FROM expenses
                       """, conn)

headers_cols = st.columns((1, 1, 1, 1, 1, 1))
headers = [(0, "Date"), (1, "Item"), (2, "Price"), (3, "Category"), (4, "Description"), (5, "Delete")]
for (i, header) in headers:
    headers_cols[i].markdown(f"**{header}**")

for i, row in df.iterrows():
    cols = st.columns((1, 1, 1, 1, 1, 1))
    cols[0].markdown(row["date"])
    cols[1].markdown(row["item"])
    cols[2].markdown(row["price"])
    cols[3].markdown(row["category"])
    cols[4].markdown(row["description"])
    
    if cols[5].button("Delete", key=f"delete_{row['id']}"):
        delete_row(row['id'])
        st.rerun()

sum_data = pd.read_sql_query("""
                        SELECT SUM(price) FROM expenses
                        """, conn)
sum_df = pd.DataFrame(sum_data)
sum = sum_df.loc[0,"SUM(price)"]
st.markdown(f"**Total spent is {sum}**")

cur = conn.cursor()
cur.execute("""
            SELECT SUM(price), category FROM expenses GROUP BY category
            """)
pie_data = cur.fetchall()
price_data = []
category_data = []

for i in pie_data:
    price_data.append(i[0])
    category_data.append(i[1])

df = pd.DataFrame({"category": category_data, "amount": price_data})
fig = px.pie(df, values="amount", names="category", title="Expenses Breakdown")
st.plotly_chart(fig)

st.subheader("Montly Summary Report")

df = pd.read_sql_query("SELECT date, price FROM expenses", conn)
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M')

monthly_summary = df.groupby('month')['price'].sum().reset_index()
monthly_summary['month'] = monthly_summary['month'].astype(str)

st.dataframe(monthly_summary.rename(columns={"month":"Month", "price":"Total Spent"}))

fig = px.bar(monthly_summary, x='month', y='price')
conn.close()