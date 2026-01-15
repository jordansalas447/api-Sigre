import pyodbc

# class Config:
#     cnxn = pyodbc.connect(
#      r"Driver={ODBC Driver 18 for SQL Server};"
#      r"Server=serversigre.database.windows.net,1433;"
#      r"Database=sigre;"
#      r"UID=usersigre;"
#      r"PWD=Sigrebt#2025;"
#      r"Encrypt=yes;"
#      r"TrustServerCertificate=no;"
#      r"Connection Timeout=30"
#      r"MARS_Connection=Yes;"
# )
    
CONNECTION_STRING = (
     r"Driver={ODBC Driver 18 for SQL Server};"
     r"Server=serversigre.database.windows.net,1433;"
     r"Database=sigre;"
     r"UID=usersigre;"
     r"PWD=Sigrebt#2025;"
     r"Encrypt=yes;"
     r"TrustServerCertificate=no;"
     r"Connection Timeout=30"
     r"MARS_Connection=Yes;"
)

CONNECTION_STRING2 = (
   r"Driver={ODBC Driver 18 for SQL Server};"
   r"Server=.\SQLEXPRESS;"
   r"Database=Sigre3;"
   r"Trusted_Connection=yes;"
   r"TrustServerCertificate=yes;"
)

CONNECTION_STRING3 = (
    r"DRIVER={ODBC Driver 18 for SQL Server};"
    r"SERVER=host.docker.internal,1433;"
    r"DATABASE=Sigre;"
    r"UID=sa;"
    r"PWD=123456789;"
    r"Encrypt=yes;"
    r"TrustServerCertificate=yes;"
    r"Connection Timeout=30;"
)

def get_connection():
    return pyodbc.connect(CONNECTION_STRING2)

#     r"Driver={ODBC Driver 18 for SQL Server};"
#     r"Server=serversigre.database.windows.net,1433;"
#     r"Database=sigre;"
#     r"UID=usersigre;"
#     r"PWD=Sigrebt#2025;"
#     r"Encrypt=yes;"
#     r"TrustServerCertificate=no;"
#     r"Connection Timeout=30"


#    "DRIVER={ODBC Driver 18 for SQL Server};"
#    "SERVER=host.docker.internal\\SQLEXPRESS;"
#    "DATABASE=sigre;"
#    "UID=sa;"
#    "PWD=123456789;"
#    "Encrypt=yes;"
#    "TrustServerCertificate=yes;"
#    "Connection Timeout=30;"


#   r"Driver={ODBC Driver 18 for SQL Server};"
#   r"Server=.\SQLEXPRESS;"
#   r"Database=sigre;"
#   r"Trusted_Connection=yes;"
#   r"TrustServerCertificate=yes;"