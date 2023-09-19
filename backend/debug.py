import boto3
from datetime import datetime

session = boto3.Session(profile_name='CP_team16')

scheduler_client = session.client(
    'scheduler'
)

if __name__ == "__main__":
    a = "與大慈討論"
    
    print(a == '與大慈討論')