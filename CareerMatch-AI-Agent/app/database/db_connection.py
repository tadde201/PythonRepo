import pyodbc


def get_connection():
    connection = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=CareerMatch;"
        "Trusted_Connection=yes;"
    )
    return connection
