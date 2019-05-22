from socket import *
import os,sys

#服务器地址
ADDR = ('0.0.0.0',8888)

def send_msg(s,name):
    while True:
        try:
            text = input('')
        except KeyboardInterrupt:
            text = 'quit'
        #退出聊天室
        if text == 'quit':
            msg = "Q "+name
            s.sendto(msg.encode(),ADDR)
            sys.exit('Quit')
        else:
            msg = "C %s %s"%(name,text)
            s.sendto(msg.encode(),ADDR)

def recv_msg(s):
    while True:
        data, addr = s.recvfrom(1024)
        if data.decode() == 'EXIT':
            sys.exit()
        print(data.decode())


#创建网络链接
def main():
    #套接字
    s = socket(AF_INET,SOCK_DGRAM)
    while True:
        name = input('Input your name:')
        msg = "L " + name  # 有空格，便于解析
        s.sendto(msg.encode(), ADDR)
        # 等待回应
        data, addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print('Welcome to the chat room.')
            break
        else:
            print(data.decode())
    pid = os.fork()
    if pid < 0:
        print('Error')
    # 子进程－发消息
    elif pid == 0:
        send_msg(s, name)
    # 父进程－收消息
    else:
        recv_msg(s)

if __name__ == '__main__':
    main()

