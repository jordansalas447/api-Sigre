import pyodbc

class Config:
    cnxn = pyodbc.connect(
     r"Driver={ODBC Driver 18 for SQL Server};"
     r"Server=serversigre.database.windows.net,1433;"
     r"Database=sigre;"
     r"UID=usersigre;"
     r"PWD=Sigrebt#2025;"
     r"Encrypt=yes;"
     r"TrustServerCertificate=no;"
     r"Connection Timeout=30"
)
    
    
#     r"Driver={ODBC Driver 18 for SQL Server};"
#     r"Server=serversigre.database.windows.net,1433;"
#     r"Database=sigre;"
#     r"UID=usersigre;"
#     r"PWD=Sigrebt#2025;"
#     r"Encrypt=yes;"
#     r"TrustServerCertificate=no;"
#     r"Connection Timeout=30"


#   r"Driver={ODBC Driver 18 for SQL Server};"
#   r"Server=.\SQLEXPRESS;"
#   r"Database=sigre;"
#   r"Trusted_Connection=yes;"
#   r"TrustServerCertificate=yes;"