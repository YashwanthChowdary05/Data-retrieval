Project Document: Flask-Based Student Record Management System

1. Introduction
This project is a web-based application built using Flask that allows users to upload and manage student records from an Excel file (.xlsx or .xls). The uploaded data is securely stored in a MySQL database and displayed in a user-friendly interface.

2. Features
- File upload interface for Excel files
- Data validation before insertion into the database
- Secure storage of student records in MySQL
- Display of stored student records on a web page
- Error handling and user notifications using flash messages

. Technologies Used
- Backend: Flask (Python)
- Frontend: HTML, Bootstrap
- Database: MySQL
- Libraries: Pandas, MySQL Connector, OS, Time

4. System Workflow
1. The user uploads an Excel file containing student records.
2. The system validates the file format and checks for required columns.
3. The data is extracted using Pandas and inserted into the MySQL database.
4. The records are displayed on the web page.
5. Any errors encountered are displayed as flash messages.

5. Folder Structure
```
/Project_Root
│── /templates
│   └── index.html (Frontend UI)
│── /uploads (Stores uploaded files)
│── app.py (Main Flask application)
│── db_connection.py (Database connection logic)
│── requirements.txt (Project dependencies)
```

6. Key Files and Their Roles
- app.py: Contains Flask routes for file upload, data processing, and fetching records.
- db_connection.py: Handles database connection setup.
- index.html: User interface for uploading files and displaying student records.

7. Database Schema
Table: STUDENTS
```
CREATE TABLE STUDENTS (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Student_Name VARCHAR(255),
    Class VARCHAR(50),
    Father_Name VARCHAR(255),
    Mother_Name VARCHAR(255),
    Phone_Number VARCHAR(20),
    Email VARCHAR(255)
);
```

8. Error Handling
- Invalid File Type: Ensures only Excel files are uploaded.
- Database Connection Issues: Handles MySQL connection failures gracefully.
- Data Validation Errors: Ensures correct column names before insertion.
- Unexpected Errors: Displays flash messages for troubleshooting.

9. Conclusion
This Flask-based system provides a simple and efficient way to manage student records using Excel uploads. With its modular design and database-backed storage, it ensures reliability and ease of use for educational institutions or administrative teams.

