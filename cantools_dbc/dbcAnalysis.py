import cantools
import os
from pprint import pprint

dirs = os.listdir('./')
for i in dirs:
    if os.path.splitext(i)[1] == '.dbc':
        # [0]是文件名，[1]对应是扩展名，这个函数是显示文件名
        print(i)
    break

'''-----打印消息-----'''
db = cantools.database.load_file(i)
print(db.messages[0])

# print(type(db.messages[0]))

# for i in db.messages:
#     message_str = str(i)
#
#     message_str = message_str.replace('message(', '').replace(')', '')
#     print(message_str)
#     message_list = message_str.split(',')
#     print(message_list)

'''-----打印消息里的信号-----'''
BCM_111_message = db.get_message_by_name('BCM_111')
# 消息的16进制ID
print(hex(BCM_111_message.frame_id))
# 消息名称
print(BCM_111_message.name)

print("测试信号是：{}".format(BCM_111_message.senders))
# 返回了信号树列表
print(BCM_111_message.length)
# 返回了信号树的字符串
# print(BCM_111_message.signal_tree_string())
# 信号的选项有哪些
# print(BCM_111_message.signal_choices_string())
#
# print(BCM_111_message.layout_string())


'''
输出格式如下
class cantools.database.can.Signal(name, start, length, byte_order='little_endian', 
is_signed=False, initial=None, scale=1, offset=0, minimum=None, maximum=None, 
unit=None, choices=None, dbc_specifics=None, comment=None, receivers=None, 
is_multiplexer=False, multiplexer_ids=None, multiplexer_signal=None, is_float=False, decimal=None)
'''
pprint(BCM_111_message.signals)
print(BCM_111_message.signals[0].scale)

# print(type(BCM_111_message.signals[0]))




# 编码成16进制报文 要注意把信号参数写全了
# s = db.encode_message('BCM_111', {'BCM_RcBaffleCtrl': 1,
#                                   'BCM_RcWateringCtrl': 1,
#                                   'BCM_RcVibratedustCtrl': 1,
#                                   'BCM_RcCleanCtrl': 1
#                                   })
# print(s)
#
# f = db.decode_message('BCM_111', b'\x00\x00\x00\x08\x00\x00\x00\x00')  # 解码16进制报文
# print(f)




