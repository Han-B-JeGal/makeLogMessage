import os
import platform
import osLogger
from datetime import datetime

os.putenv("NLS_LANG", "KOREAN_KOREA.KO16KSC5601")

# DB 접속용 변수
MARIA_DB_USER = 'root'
MARIA_DB_PASS = 'P@s$w0rd'
MARIA_DB_IP = '127.0.0.1'
MARIA_DB_PORT = '3306'
MARIA_DB_NAME = 'EMS_DCS'

def readConfiguration(FileName: str = './Service.json'):
