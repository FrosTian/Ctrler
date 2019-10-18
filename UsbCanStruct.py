from ctypes import *
from ctypes.wintypes import DWORD
# import time

"""每一个子类必须定义"_fields_"属性，"_fields_"是一个二维的tuples列表
创建结构与联合体时，可以包含位域字段。只有整型域才可以使用位字段，位宽可以在_fields_元组的第三个选项中指定

"""
# dll = windll.LoadLibrary('./resource/dlls/ECanVci64.dll')
#  板卡信息结构体，结构体将在ReadBoardInfo函数中被填充。
class BOARD_INFO(Structure):
    _fields_ = [('hw_Version', c_ushort),
                ('fw_Version', c_ushort),
                ('dr_Version', c_ushort),
                ('in_Version', c_ushort),
                ("irq_Num", c_ushort),
                ('can_Num', c_byte),
                ('str_Serial_Num', c_char * 20),
                ('str_hw_Type', c_char * 40),
                ('Reserved', c_ushort * 4)]  # 保留字段

    def __str__(self):
        return '硬件版本号：%s,固件版本号：%s,驱动程序版本号：%s,接口库版本号：%s,中断号：%s,共有%s路CAN，序列号：%s,硬件类型：%s' % (
            self.hw_Version, self.fw_Version, self.dr_Version, self.in_Version, self.irq_Num, self.can_Num,
            self.str_Serial_Num, self.str_hw_Type)

# a = BOARD_INFO(1, 2, 3, 4, 5, 6, b'asdf', b'USB', (1,2,3,4))  结构体内容格式举例
# print(a)


class CAN_OBJ(Structure):
    _fields_ = [('ID', c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_byte),
                ('SendType', c_byte),
                ('RemoteFlag', c_byte),
                ('ExternFlag', c_byte),
                ('DataLen', c_byte),
                ('Data', c_ubyte * 8),
                ('Reserved', c_byte * 3)]

    def __str__(self):
        datastr = ''
        for i in range(self.DataLen):
            datastr += format(self.Data[i], '02X') + " "  # 用两位的16进制字符串表示
        return 'ID:%08X,时间戳:%X,长度:%X,数据:%s' % (self.ID, self.TimeStamp, self.DataLen, datastr)

    # 获取数据，返回一个列表
    def getdata(self):
        return [self.Data[i] for i in range(self.DataLen)]

    # 设置报文数据，参数需要是一个8位列表或元组，这里使用args，表示传进来的就是元组了
    def setdata(self, *args):
        self.DataLen = len(args)
        for i in range(self.DataLen):
            self.Data[i] = args[i]


# vco = CAN_OBJ(ID = 0x55, SendType = 1, RemoteFlag = 0, ExternFlag = 0, DataLen = 8,
#               Data = (1, 2, 3, 4, 5, 6, 0xf, 0), Reserved = (0, 0, 0))
# print(vco)  # 测试这个结构体的功能
# print(vco.getdata())
# vco.setdata(0, 7, 6, 5, 4, 0xa, 2, 1)
# print(vco.getdata())


# 控制器状态信息。中断记录和各种寄存器：模式，状态，仲裁丢失，错误，错误警告限制，接收错误，发送错误
class CAN_STATUS(Structure):
    _fields_ = [('ErrInterrupt', c_ubyte),
                ('regMode', c_ubyte),
                ('regStatus', c_ubyte),
                ('regALCapture', c_ubyte),
                ('regECCapture', c_ubyte),
                ('regEWLimit', c_ubyte),
                ('regRECounter', c_ubyte),
                ('regTRCounter', c_ubyte),
                ('Reserved', c_ulong)]


#  装载VCI库运行时产生的错误信息。结构体在readErrInfo函数中被填充。
class ERR_INFO(Structure):
    _fields_ = [('ErrCode', c_uint),
                ('Passive_ErrData', c_byte * 3),
                ('ArLost_ErrData', c_byte)]


#  定义了初始化CAN的配置。结构体将在InitCan函数中被填充。在初始化之前，要先填好这个结构体变量。
class INIT_CONFIG(Structure):
    _fields_ = [('AccCode', DWORD),  # 验收码，后面是数据类型c_ulong，也可以用c_ulong
                ('AccMask', DWORD),  # 屏蔽码
                ('Reserved', DWORD),  # 保留
                ('Filter', c_ubyte),  # 滤波使能。0=不使能，1=使能使能时。
                ('Timing0', c_ubyte),  # 波特率定时器0（BTR0）
                ('Timing1', c_ubyte),  # 波特率定时器1（BTR1)
                ('Mode', c_ubyte)]  # 模式。=0为正常模式，=1为只听模式， =2为自发自收模式


# 定义了CAN滤波器的滤波范围。 结构体将在SetReference函数中被填充。
class FILTER_RECORD(Structure):
    _fields_ = [('ExtFrame', DWORD),
                ('Start', DWORD),
                ('End', DWORD)]

'''
# 用于装载更改CANET_UDP与CANET_TCP 的目标IP和端口的必要信息。此结构体在CANETE_UDP与CANET_TCP中使用。广成科技无此功能，后面的结构体也都没有
class CHGDESIPANDPORT(Structure):
    _fields_ = [('szpwd', c_char * 10),
                ('szdesip', c_char * 20),
                ('desport', c_int),
                ('blisten', c_byte)]


class AUTO_SEND_OBJ(Structure):
    _fields_ = [('Enable', c_byte),
                ('Index', c_byte),
                ('Interval', DWORD),
                ('Obj', CAN_OBJ)]


class INDICATE_LIGHT(Structure):
    _fields_ = [('Indicate', c_byte),
                ('AttribRedMode', c_byte, 2),
                ('AttribGreenMode', c_byte, 2),
                ('AttribReserved', c_byte, 4),
                ('FrequenceRed', c_byte, 2),
                ('FrequenceGreen', c_byte, 2),
                ('FrequenceReserved', c_byte, 4)]


class CAN_OJB_REDIRECT(Structure):
    _fields_ = [('Action', c_byte),
                ('DestCanIndex', c_byte)]


class DTUCOMCONFIG(Structure):
    _fields_ = [('dwLen', DWORD),
                ('pData', POINTER(c_byte))]
'''


