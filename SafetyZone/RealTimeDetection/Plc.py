"""import snap7

PlcIp = '10.15.221.254'
PlcRack = 0
PlcSlot = 0
PlcCpu = 30
IstasyonDB = 'DB90'
IstasyonDB = int(IstasyonDB[2:])
OperasyonBasladiDB = 'DBX0.0'
OperasyonTamamlandiDB = 'DBX0.1'

plc = snap7.client.Client()
plc.connect(PlcIp, PlcRack, PlcSlot)
reading = plc.db_read(90, 0, 2)
name = reading[0:256].decode('UTF-8').strip('\x00')
print(reading)"""

import snap7
import time

class Plc(object):
    def __init__(self, PlcIP, PlcRack, PlcSlot):
        self.bit_value = True
        self.client = snap7.client.Client()
        self.client.connect(PlcIP, PlcRack, PlcSlot)

    def Read_Byte(self, DB, DBX):
        buffer = self.client.db_read(DB, DBX, 1)
        # buffer -> type= byte array -> ascii -> string
        buffer_value = ord(buffer[0:256].decode('UTF-8'))  # only client.db_read(X, X, count) count =1
        return buffer_value , buffer     # string list

        # def write_byte(db_num, start_byte, byte_value):  # Byte yazma
        #     data = bytearray(1)
        #     snap7.util.set_byte(data, 0, byte_value)
        #     plc.db_write(db_num, start_byte, data)

    def Set_Byte(self, DB, DBX, value):
        try:
            data = bytearray(1)
            snap7.util.set_byte(data, 0, value)
            self.client.db_write(DB, DBX, data)
            result = True
        except:
            result = False
        return result


    def Read_Bit(self, DB, DBX, DB_X,pause):
        while True:
            buffer = self.client.db_read(DB, DBX, 1)
            byte_value = snap7.util.get_bool(buffer, 0, DB_X)
            self.bit_value = byte_value   # bool
            time.sleep(pause)


    def Set_bit(self, DB, DBX, DB_X, value):
        try:
            _,data = self.Read_Byte(DB,DBX)
            snap7.util.set_bool(data, 0, DB_X, value)
            self.client.db_write(DB, DBX, data)
            result = True
        except:
            result = False
        return result

