'''
http功能演示
将网页发送给浏览器展示
再查找一下老师的代码
'''

from socket import *

def handle(connfd):
    print('Request from:',connfd.getpeername())
    request = connfd.recv(4096)
    #为了防止客户端断开,客户端突然关闭，request为空的。
    #为什么每次运行链接了两次？
    if not request:
        return
    #将request按行分割
    request_line = request.splitlines()[0].decode()
    print(request_line)#打印请求
    #获取请求内容
    info = request_line.split(' ')[1]
    print(info)
    if info == '/':
        fd = open('index.html')
        response = "HTTP/1.1 200 OK\r\n"
        response+= "Content-Type:text/html\r\n"
        response+= "\r\n"
        response+= fd.read()
    else:
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        response += "<h1>Sorry...</h1>"
    connfd.send(response.encode())

#搭建tcp网络
def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(('0.0.0.0',8000))
    sockfd.listen(3)
    print('Listen the port8000...')
    while True:
        connfd,addr = sockfd.accept()
        handle(connfd)#处理浏览器请求
        connfd.close()

if __name__ == '__main__':
    main()
