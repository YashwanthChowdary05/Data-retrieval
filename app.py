from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
import os
import time
import mysql.connector
import db_connection

app = Flask(__name__, template_folder='templates')

# Configure file upload folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET'])
def index():
    """Render the index page with student data."""
    data = fetch_data()  # Fetch data on initial load
    return render_template('index.html', data = data)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle Excel file upload and insert data into the database."""
    if 'fileToUpload' not in request.files:
        flash("No file uploaded.", "error")
        return redirect(url_for('index'))

    file = request.files['fileToUpload']
    if file.filename == '':
        flash("No file selected.", "error")
        return redirect(url_for('index'))

    if not file.filename.endswith(('.xlsx', '.xls')):
        flash("Invalid file type. Please upload an Excel file (.xlsx or .xls).", "error")
        return redirect(url_for('index'))

    try:
        filename = f"students_{int(time.time())}.xlsx"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        print(f"File saved successfully at: {filepath}")

        # Establish database connection
        connection, cursor = db_connection.get_db_connection()
        if not connection or not cursor:
            flash("Database connection failed.", "error")
            return redirect(url_for('index'))

        # Read Excel file into DataFrame
        df = pd.read_excel(filepath)

        # Ensure correct columns exist
        expected_columns = ["Student_Name", "Class", "Father_Name", "Mother_Name", "Phone_Number", "Email"]
        actual_columns = list(df.columns)
        
        print(f"Excel Columns: {actual_columns}")
        
        if actual_columns != expected_columns:
            raise ValueError(f"Excel file columns mismatch. Expected: {expected_columns}, Found: {actual_columns}")

        # Insert data into MySQL
        for _, row in df.iterrows():
            sql = """
                INSERT INTO STUDENTS (Student_Name, Class, Father_Name, Mother_Name, Phone_Number, Email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (row['Student_Name'], row['Class'], row['Father_Name'], row['Mother_Name'], row['Phone_Number'], row['Email'])
            cursor.execute(sql, values)

        connection.commit()

        flash("Data uploaded successfully!", "success")

        # Fetch updated data from the database after the commit
        data = fetch_data()
        #print(data)
        return render_template('index.html', data = data)

    except mysql.connector.Error as mysql_error:
        connection.rollback()
        flash(f"MySQL Error: {mysql_error}", "error")
        data = []
    except pd.errors.ParserError as panda_error:
        connection.rollback()
        flash(f"Pandas Error: {panda_error}", "error")
        data = []
    except ValueError as value_err:
        connection.rollback()
        flash(f"Value Error: {value_err}", "error")
        data = []
    except Exception as err:
        connection.rollback()
        flash(f"Unexpected Error: {err}", "error")
        data = []
    finally:
        # Close the cursor and connection after the entire operation is done
        if cursor: cursor.close()
        if connection: connection.close()

def fetch_data():
    """Fetch all students' data from the database, returning a list of dictionaries."""
    connection, cursor = db_connection.get_db_connection()
    if not connection or not cursor:
        return []

    try:
        cursor.execute("SELECT ID, Student_Name, Class, Father_Name, Mother_Name, Phone_Number, Email FROM STUDENTS")
        data = cursor.fetchall()
        # print('Fetch Data')
        print(data)
        return data
    except mysql.connector.Error as mysql_error:
        print(f"Database Error: {mysql_error}")
        return []
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

if __name__ == '__main__':
    app.run(debug=True)