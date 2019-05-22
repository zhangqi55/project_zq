from socket import *
import os,sys

#服务器地址
ADDR = ('0.0.0.0',8888)

list_users = {}

#　进入聊天室
def do_login(s,name,addr):
    if name in list_users or "Manager" in name:
        #不允许字符串中包含管理员
        s.sendto("Already exists.".encode(),addr)
        return
    else:
        s.sendto(b'OK',addr)
        #通知其他人
        msg = "Welcome %s enter chatroom"%name
        for i in list_users:
            s.sendto(msg.encode(),list_users[i])
        #将用户加入
        list_users[name] = addr

#聊天
def do_chat(s,name,text):
    msg = '%s:%s'%(name,text)
    for item in list_users:
        if item != name:
            s.sendto(msg.encode(), list_users[item])

#退出聊天室
def do_quit(s,name):
    msg = "%s leave the room."%name
    for item in list_users:
        if item == name:
            s.sendto('EXIT'.encode(), list_users[item])
        else:
            s.sendto(msg.encode(), list_users[item])
    del list_users[name]

#接收各种客户端请求
def do_request(s):
    while True:
        data,addr = s.recvfrom(1024)
        #解析请求
        list_tem = data.decode().split(' ')
        if list_tem[0] == 'L':
            do_login(s, list_tem[1], addr)
        elif list_tem[0] == 'C':
            msg = ' '.join(list_tem[2:])
            do_chat(s,list_tem[1],msg)
        elif list_tem[0] == 'Q':
            do_quit(s,list_tem[1])



#创建网络链接
def main():
    #套接字
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)
    pid = os.fork()
    if pid<0:
        return
    elif pid == 0:
        while True:
            msg = input("Manager information:")
            msg = "C Manager information:" +msg
            s.sendto(msg.encode(),ADDR)
            #发给自己了
    else:
    #请求处理
        do_request(s)#处理客户端请求

if __name__ == '__main__':
    main()
    for item in list_users:
        print(item)

