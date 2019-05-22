from socket import *
import sys
from time import sleep

# 服务器地址
ADDR = ('176.47.4.27',6666)

# 具体功能
class FtpClient:
    def __init__(self,sockfd):
        self.sockfd = sockfd
    def do_list(self):
        self.sockfd.send(b'L')
        #等待回复
        data = self.sockfd.recv(128).decode()
        #OK表示请求成功
        if data == 'OK':
            while True:
                data = self.sockfd.recv(128)
                if data == b'##':
                    print(data.decode())
                    return
                else:
                    print(data.decode())

    def do_get(self,filename):
        #发送请求
        self.sockfd.send(('G '+filename).encode())
        # 等待回复
        data = self.sockfd.recv(128).decode()
        # OK表示请求成功
        if data == 'OK':
            fd = open(filename,'wb')
            #接收内容，写入文件
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                else:
                    fd.write(data)
            fd.close()
        else:
            print(data)

    def do_put(self,filename):
        try:
            fd = open(filename, 'rb')
        except Exception:
            print("没有该文件")
            return
        # 发送请求
        filename = filename.split('/')[-1]#对文件路径进行切割解析
        self.sockfd.send(('P ' + filename).encode())
        sleep(0.1)
        # 等待回复
        data = self.sockfd.recv(128).decode()
        # OK表示请求成功
        if data == 'OK':
            # 读取文件并且发送
            while True:
                data = fd.read(1024)
                if not data:
                    sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)
            fd.close()
        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit("谢谢使用")


# 发起请求
def request(sockfd):
    ftp = FtpClient(sockfd)
    while True:
        print("\n==========命令选项==========")
        print("************list************")
        print("**********get file**********")
        print("**********put file**********")
        print("************quit************")
        print("============================")

        cmd = input("输入命令：")
        if cmd == 'list':
            ftp.do_list()
        elif cmd[:3] == 'get':
            filename = cmd.split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.split(' ')[-1]
            ftp.do_put(filename)
        elif cmd == 'quit':
            ftp.do_quit()


# 网络链接
def main():
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print("链接服务器失败")
        return
    else:
        print('''
                 ********************
                  Data  File  Image
                 ********************
        ''')
        cls = input("请输入想要的文件种类：")
        if cls not in ['Data','File','Image']:
            print("Sorry input Irror!!")
            return
        else:
            sockfd.send(cls.encode())
            request(sockfd)

if __name__ == '__main__':
    main()







