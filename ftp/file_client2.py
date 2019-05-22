from socket import *

#服务器地址
ADDR = ('176.47.4.27',6666)

#具体功能
class FtpClient:
    pass

#网络链接
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

if __name__ == '__main__':
    main()