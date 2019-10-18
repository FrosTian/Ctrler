def text_create(name, msg):
    desktop_path = "d:\\"  # 新创建的txt文件的存放路径
    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path, 'w')
    file.write(msg)  # msg也就是下面的Hello world!
    file.close()

    import time

    l=[]
    for i in range(10):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        time.sleep(1)
        print(l)
        l.append(t+'\n')







# import time
#
# # i = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#
# while 1:
#     i = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     time.sleep(1)
#     print(i)




