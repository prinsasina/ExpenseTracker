# Expense Tracker 

[![Live Demo](https://img.shields.io/badge/demo-live-blue)](https://expensetracker-01.streamlit.app/)  

A simple web-based expense tracker built with **Streamlit**, **SQLite**, and **Plotly** that allows users to input, view, delete, and analyze their personal expenses in a clean interface.

## Features

- **Manual/File Upload Input**  
  Add expenses individually or upload a CSV file with multiple records.

- **Display of Expense Records**  
  See all added expenses.

- **Delete Button**  
  Remove unwanted entries.

- **Pie Chart Visualization**  
  See a breakdown of your spending by category using interactive Plotly charts.

- **Total Spending Summary**  
  Automatically calculates and displays the total money spent.

## Tech Stack

- **Frontend/UI**: Streamlit
- **Database**: SQLite
- **Visualization**: Plotly
- **Data Handling**: Pandas

## Setup Instructions

### Clone the repository

```bash
git clone https://https://github.com/prinsasina/ExpenseTracker
cd expense-tracker-streamlit
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the Streamlit app

```bash
streamlit run main.py
```
The app will open in your browser at http://localhost:8501
