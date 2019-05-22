'''
ftp文件服务器
并发网络功能训练
'''

from socket import *
import os,sys
from threading import Thread
from time import sleep

# 全局变量
ADDR = ('176.47.4.27', 6666)
FTP = "/home/tarena/month2/FTP/"#文件库路径


# 将客户端请求功能封装成类
class FtpServer:
    def __init__(self, connfd, FTP_PATH):
        self.connfd = connfd
        self.path = FTP_PATH

    def do_list(self):
        #获取文件列表
        files = os.listdir(self.path)
        if not files:
            self.connfd.send("该文件类别为空".encode())
            sleep(0.1)
            return
        else:
            self.connfd.send(b"OK")
            sleep(0.1)
        #过滤隐藏文件,前面带点是隐藏文件，用函数判断是普通文件
        for file in files:
            if file[0] != '.' and os.path.isfile(self.path + file):
                self.connfd.send(file.encode())
                sleep(0.1)
        self.connfd.send(b"##")

    def do_get(self,filename):
        try:
            file_fd = open(self.path+filename,'rb')
        except Exception:
            self.connfd.send('文件不存在'.encode())
            return
        else:
            self.connfd.send(b"OK")
            sleep(0.1)
        #发送文件内容
        while True:
            data = file_fd.read(1024)
            if not data:
                sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)

    def do_put(self,filename):
        # 判断文件是否已经存在
        if os.path.exists(self.path + filename):
            self.connfd.send("该文件已存在".encode())
            return
        self.connfd.send(b"OK")
        # 下载文件内容
        fd = open(self.path+filename,'wb')
        while True:
            data = self.connfd.recv(1024)
            if data == b'##':
                break
            else:
                fd.write(data)
        fd.close()


# 客户端请求处理函数
def handle(connfd):
    cls = connfd.recv(1024).decode()
    FTP_PATH = FTP + cls + '/'
    ftp = FtpServer(connfd, FTP_PATH)
    while True:
        # 接受客户端请求
        data = connfd.recv(1024).decode()
        # 客户端断开时，data为空字串，[0]会越界
        if not data or data[0] == 'Q':
            print("有客户端退出")
            return
        elif data[0] == 'L':
            ftp.do_list()
        elif data[0] == 'G':
            ftp.do_get(data.split(' ')[-1])
        elif data[0] == 'P':
            ftp.do_put(data.split(' ')[-1])


# 网络搭建
def main():
    # 创建监听套接字
    s = socket(AF_INET, SOCK_STREAM, proto=0)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 设置套接字端口立即重用
    s.bind(ADDR)
    s.listen(5)
    print('Listen the port 8888...')
    # 循环等待客户端链接
    while True:
        try:
            connfd, addr = s.accept()
        except KeyboardInterrupt:
            print("服务器退出")  # 退出进程
            return
        except Exception as e:
            print(e)
            continue
        print("链接的客户端：",addr)
        # 创建新的线程处理客户端请求
        client = Thread(target=handle, args=(connfd,))
        client.setDaemon(True)  # 当主线程退出时，分支线程也跟着退出
        client.start()


if __name__ == '__main__':
    main()




