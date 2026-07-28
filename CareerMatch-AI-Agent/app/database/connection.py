"""SQL Server database connection utilities."""

from typing import Optional
from app.config import DB_SERVER, DB_NAME

try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False


def get_connection():
    """
    Get a SQL Server database connection.
    
    Returns:
        Database connection object or None if connection fails
    """
    if not PYODBC_AVAILABLE:
        print("Warning: pyodbc is not installed. Database features unavailable.")
        return None
    
    if not DB_SERVER or not DB_NAME:
        print("Warning: DB_SERVER and DB_NAME environment variables not configured.")
        return None
    
    try:
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={DB_SERVER};'
            f'DATABASE={DB_NAME};'
            f'Trusted_Connection=yes;'
        )
        print(f"✓ Connected to database: {DB_NAME}")
        return connection
    except pyodbc.Error as e:
        print(f"✗ Database connection error: {str(e)}")
        return None


def save_job_match_to_db(
    connection,
    candidate_id: int,
    job_id: int,
    match_score: int,
    match_analysis: str
) -> bool:
    """
    Save a job match result to the database.
    
    Args:
        connection: Database connection
        candidate_id: Candidate ID
        job_id: Job ID
        match_score: Match score (0-100)
        match_analysis: Analysis text
        
    Returns:
        True if saved successfully, False otherwise
    """
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        query = """
            INSERT INTO job_matches (candidate_id, job_id, match_score, analysis, created_at)
            VALUES (?, ?, ?, ?, GETDATE())
        """
        
        cursor.execute(query, (candidate_id, job_id, match_score, match_analysis))
        connection.commit()
        
        return True
    except Exception as e:
        print(f"✗ Error saving to database: {str(e)}")
        return False


def create_tables(connection) -> bool:
    """
    Create database tables for job matching.
    
    Args:
        connection: Database connection
        
    Returns:
        True if tables created successfully, False otherwise
    """
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Create candidates table
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='candidates' AND xtype='U')
            CREATE TABLE candidates (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name NVARCHAR(255),
                email NVARCHAR(255),
                skills NVARCHAR(MAX),
                created_at DATETIME
            )
        """)
        
        # Create jobs table
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='jobs' AND xtype='U')
            CREATE TABLE jobs (
                id INT IDENTITY(1,1) PRIMARY KEY,
                title NVARCHAR(255),
                company NVARCHAR(255),
                description NVARCHAR(MAX),
                requirements NVARCHAR(MAX),
                posted_at DATETIME
            )
        """)
        
        # Create job_matches table
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='job_matches' AND xtype='U')
            CREATE TABLE job_matches (
                id INT IDENTITY(1,1) PRIMARY KEY,
                candidate_id INT,
                job_id INT,
                match_score INT,
                analysis NVARCHAR(MAX),
                created_at DATETIME,
                FOREIGN KEY (candidate_id) REFERENCES candidates(id),
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        """)
        
        connection.commit()
        print("✓ Database tables created successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error creating tables: {str(e)}")
        return False
