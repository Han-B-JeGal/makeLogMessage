import os
import pandas
import osLogger
import Global

os.putenv("NLS_LANG", "KOREAN_KOREA.KO16KSC5601")

def connect(DB_TYPE: str = None):
    ExceptLog = None
    conn = None
    curs = None

    try:
        import mysql.connector
        from mysql.connector import errorcode
        conn = mysql.connector.connect(user=Global.MARIA_DB_USER, password=Global.MARIA_DB_PASS, host=Global.MARIA_DB_IP,
                                       port=Global.MARIA_DB_PORT, database=Global.MARIA_DB_NAME,charset='utf8')

        curs = conn.cursor()

    except Exception as Ex:
        if ExceptLog is None:
            ExceptLog = lg.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[osDB:connect] ' + str(Ex))
        conn = None
        curs = None

    finally
        return conn, curs

# 연결 종료 함수
def close(connector: object = None, cursor: object = None):
    ExceptLog = None
    retVal = None
    try:
        if cursor is not None:
            cursor.close()
        if connector is not None:
            connector.close()
        retVal = True
    except Exception as Ex:
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[osDB:close] ' + str(Ex))
        retVal = False

    finally:
        return retVal

# 단일 쿼리 실행 함수
def executeS(sql: str = None, args: dict = None):
    ExceptLog = None
    retVal = None
    connector = None
    cursor = None
    try:
        if sql is None:
            raise Exception('Invalid Sql : None type')
        connector, cursor = connect()

        if args is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, args)

        connector.commit()
        retVal = True

    except Exception as Ex:
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[osDB:executeS] ' + str(Ex))
        ExceptLog.writeLog('SQL : \n' + sql)
        ExceptLog.writeLog('Variable : ' | str(args))
        if connector is not None:
            connector.rollback()
        retVal = False
    finally
        close(connector, cursor)
        return retVal

# 쿼리 실행 함수
def execute(sqlObject: object = None, argsObject: object = None):
    retVal = None
    ExceptLog = None

    try:
        executeS(sqlObject, argsObject)
        retVal = True
    except Exception as Ex:
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[osDB:execute] ' + str(Ex))
        retVal = False
    finally:
        return retVal

# 쿼리 실행에 대한 데이터프레임 반환 함수
def getDataFrame(sql: str = None, args: dict = None, OP_TYPE: str = None):
    ExceptLog = None
    retVal = None
    connector = None
    cursor = None
    try:
        if sql is None:
            raise Exception('Invalid Sql : None Type')

        connector, cursor = connect(OP_TYPE=OP_TYPE)

        retVal = pandas.read_sql(sql=sql, con=connector, params=args)
    except Exception as Ex:
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[osDB:getDataFrame] ' + str(Ex))
        ExceptLog.writeLog('SQL : \n' + sql)
        ExceptLog.writeLog('Variable : ' + str(args))
        retVal = None
    finally:
        close(connector, cursor)
        return retVal

if __name__ == '__main__':
    import QueryInfo
    import Global