from UsbCanStruct import *
import time
import datetime
import sys

# 装饰器 6了6了
def issucceed(func_name):
    def deco(func):
        def wrapper(self, *args):
            if func(self, *args):
                print(func_name+"成功")
            else:
                print(func_name+"失败")
        return wrapper
    return deco


class ControlCAN:
    """DevType设备类型号。USBCANI选择3，USBCANII 选择4。
    DevIndex设备索引号。比如当只有一个设备时，索引号为0，有两个时可以为0或1。
    CANIndex第几路CAN。即对应卡的CAN通道号，CAN0为0，CAN1为1。
    baudrate波特率。
    AccCode验收码。SJA1000的帧过滤验收码。
    AccMask屏蔽码。SJA1000的帧过滤屏蔽码。屏蔽码推荐设置为0xFFFF FFFF，即全部接收。

    """
    def __init__(self, devtype=4, devindex=0, canindex=0, baudrate=500, acccode=0x00000000, accmask=0xFFFFFFFF):
        time0 = {100: 0x04, 125: 0x03, 250: 0x01, 500: 0x00, 1000: 0x00}
        time1 = {100: 0x1C, 125: 0x1C, 250: 0x1C, 500: 0x1C, 1000: 0x14}
        pData = {100: 0x160023, 125: 0x1C0011, 250: 0x1C0008, 500: 0x060007, 1000: 0x060003}
        self.CANdll = WinDLL("./resource/dlls/ECanVci64.dll")  # 也可以使用windll.LoadLibrary，stdcall调用约定的两种加载方式
        self.devtype = devtype
        self.devindex = devindex
        self.canindex = canindex
        self.baudrate = baudrate
        self.time0 = time0[self.baudrate]
        self.time1 = time1[self.baudrate]
        # self.time1 = 0x1c
        self.acccode = acccode
        self.accmask = accmask
        self.initconfig = INIT_CONFIG(self.acccode, self.accmask, 0, 0, self.time0, self.time1, 0)
        self.pData = DWORD(pData[self.baudrate])
        self.errinfo = ERR_INFO()
        self.boardinfo = BOARD_INFO()
        self.receivebuf = (CAN_OBJ * 50)()  # 什么意思？
        self.sendbuf = (CAN_OBJ * 50)()
        self.emptynum = 0

    # OpenDevice(设备类型号，设备索引号，参数无意义)
    @issucceed("打开CAN卡")
    def opendevice(self):
        return self.CANdll.OpenDevice(self.devtype, self.devindex, 0)

    # InitCAN(设备类型号，设备索引号，第几路CAN，初始化参数initConfig)，
    @issucceed("初始化CAN卡")
    def initcan(self):
        # if self.devtype == 21:
        #     self.CANdll.SetReference(self.devtype, self.devindex, self.canindex, 0, byref(self.pData))
        return self.CANdll.InitCAN(self.devtype, self.devindex, self.canindex, byref(self.initconfig))

    # StartCAN(设备类型号，设备索引号，第几路CAN)
    @issucceed("启动CAN卡")
    def startcan(self):
        return self.CANdll.StartCAN(self.devtype, self.devindex, self.canindex)

    # 复位CAN。如当USBCAN分析仪进入总线关闭状态时，可以调用这个函数。
    @issucceed("复位CAN卡")
    def resetcan(self):
        return self.CANdll.ResetCAN(self.devtype, self.devindex, self.canindex)

    # 获取设备信息，最后一个参数是BOARD_INFO结构指针
    @issucceed("获取设备信息")
    def readboardinfo(self):
        return self.CANdll.ReadBoardInfo(self.devtype, self.devindex, byref(self.boardinfo))

    # 以下两个函数不加修饰器因为要重复调用，减少不必要输出
    # 此函数用以获取指定接收缓冲区中接收到但尚未被读取的帧数量。
    def getreceivenum(self):
        return self.CANdll.GetReceiveNum(self.devtype, self.devindex, self.canindex)

    # 此函数从指定的设备CAN通道的缓冲区里读取数据。
    def receive(self):
        respond = self.CANdll.Receive(self.devtype, self.devindex, self.canindex, byref(self.receivebuf), 50, 10)
        if respond == 0xFFFFFFFF:
            print("读取数据失败")
            self.CANdll.ReadErrInfo(self.devtype, self.devindex, self.canindex, byref(self.errinfo))
        elif respond == 0:
            pass
            # print("无新数据")
            # if self.devtype == 3 or self.devtype == 4:
            #     self.emptynum = self.emptynum + 1
            #     temp = self.emptynum // 20
            #     sys.stdout.write('\r' + "无新数据" + "." * temp)
            #     sys.stdout.flush()
        elif respond > 0:
            pass
            # 写入自己的代码 处理接收到的CAN数据
        return respond

    # 返回实际发送成功的帧数量。
    @issucceed("发送CAN帧")
    def transmit(self,frame_num=1):
        return self.CANdll.Transmit(self.devtype, self.devindex, self.canindex, byref(self.sendbuf), frame_num)

    @issucceed("读取错误")
    def readerrinfo(self):
        return self.CANdll.ReadErrInfo(self.devtype, self.devindex, self.canindex, byref(self.errinfo))

    @issucceed("设定E-U波特率")
    def setreference(self):
        return self.CANdll.SetReference(self.devtype, self.devindex, self.canindex, 0, byref(self.pData))

    # __del__方法：销毁对象
    @issucceed("关闭CAN卡")
    def __del__(self):
        return self.CANdll.CloseDevice(self.devtype, self.devindex)



'''
# 定义一个用于初始化的实例对象vic
vic = VciInitConfig()
vic.AccCode = 0x00000000
vic.AccMask = 0xffffffff
vic.reserved = 0
vic.Filter = 0
vic.Timing0 = 0x00  # 500Kbps
vic.Timing1 = 0x1C  # 500Kbps
vic.Mode = 0

# 定义报文实例对象，用于发送
vco = VciCanObj()
vco.ID = 0x00000055  # 帧的ID
vco.SendType = 1  # 发送帧类型，0是正常发送，1为单次发送，这里要选1！要不发不去！
vco.RemoteFlag = 0
vco.ExternFlag = 0
vco.DataLen = 8
vco.Data = (1, 2, 3, 4, 5, 6, 7, 0)
vco.Reserved = (0, 0, 0)
# 也可以用下面的定义方式，其中报文可以用0x的表达选择是16进制还是10进制
'''

'''ubyte_array = c_ubyte * 8
a = ubyte_array(1, 2, 3, 4, 5, 6, 7, 0x64)
ubyte_3array = c_ubyte * 3
b = ubyte_3array(0, 0, 0)
vco = VciCanObj(0x01, 0, 0, 1, 0, 0, 8, a)'''


'''
# 定义报文实例对象，用于接收
vco2 = VciCanObj()
vco2.ID = 0x00000001  # 帧的ID 后面会变成真实发送的ID
vco2.SendType = 0  # 这里0就可以收到
vco2.RemoteFlag = 0
vco2.ExternFlag = 0
vco2.DataLen = 8
vco2.Data = (0, 0, 0, 0, 0, 0, 0, 0)


# 设备的打开如果是双通道的设备的话，可以再用initcan函数初始化



print("opendevice:", ret)

print("initcan0:", ret)

ret = dll.StartCAN(nDeviceType, nDeviceInd, 0)
print("startcan0:", ret)

i = 1
while i:
    art = dll.Transmit(nDeviceType, nDeviceInd, 0, byref(vco), 1)  # 发送vco
    ret = dll.Receive(nDeviceType, nDeviceInd, 0, byref(vco2), 1, 0)  # 以vco2的形式接收报文
    time.sleep(1)  # 设置一个循环发送的时间
    if ret > 0:
        print(i)
        print(list(vco2.Data))  # 打印接收到的报文
    i += 1

ret = dll.CloseDevice(nDeviceType, nDeviceInd)
print("closedevice:", ret)
'''