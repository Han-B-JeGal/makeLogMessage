import socket
import Global
import osLogger


def getChecksum(Data: str = None):
    ExceptLog = None
    RetVal = None
    try:
        if Data is None:
            raise Exception('Invalid Input Data : None')

        iLen = len(str(Data))
        CharSum = 0
        for i in range(0, iLen):
            CharSum = CharSum + ord(Data[i])
        CheckSum1 = ((CharSum & 0xF0) >> 4) + 0x30
        CheckSum2 = ((CharSum & 0x0F) >> 0) + 0x30

        RetVal = chr(CheckSum1) + chr(CheckSum2)
    except Exception as Ex:
        if ExceptLog is None:
            ExceptLog = osLogger.cOSLogger(_pPrefix='Exception', _pLevel='ERROR')
        ExceptLog.writeLog('[sendData:getChecksum] ' + str(Ex))
    finally:
        return RetVal


if __name__ == '__main__':
    Pkt1 = 'ABCD'

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 6363))

    client.send(Pkt1.encode())
    print('SEND : ' + Pkt1)

    client.close()
