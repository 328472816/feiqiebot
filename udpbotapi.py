# -*- coding: utf-8 -*-
#内网通机器人接口的帮助类
import socket
import random
import threading, sys, os, socket, time, struct, select
#1@shiyeline:5508:Administra:HW01:288:123
#1_lbt6_0#128#305A3A52C61C#0#0#0#4001#9:1546625341:Administrator:HW01:122:\x00
botheader = '1_lbt6_0#128#305A3A52C610#0#0#0#4001#9:'
sendheader = ':UDP机器人:bot:288:'
#1_lbt6_0#128#305A3A52C61C#0#0#0#4001#9:1546625354:Administrator:HW01:33:14524125\x00
reposheader = ':UDP机器人:bot:33:'

hellotext = '欢迎使用内网通机器人,详细说明见 http://112.74.50.225:5000/article-detials/2'
    # AF_INET 是ipv4 的类型
    # sock_dgram 是UDP传输协议的类型
def udpbotinit(sock):
    sock.bind(('0.0.0.0', 2425))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#def BotHelloToAll(sock):
#    sock.sendto((botheader + '%d'%int(time.time()) + sendheader + '你好').decode('utf-8').encode('gbk'), ('192.168.0.103', 2425))

def UserMsg(msg):
#    groupmsg = msg.split('#')
#    mac = groupmsg[2]
#    print 'mac ' + mac
    groupmsg = msg.split(':')
    time = groupmsg[1]
#    print 'time ' + time
    username = groupmsg[2]
#    print 'username ' + username
    pcname = groupmsg[3]
#    print 'pcname ' + pcname
    type = int(groupmsg[4])
#    print 'type %d'%type
#    groupmsg = msg.split(';')
    body = groupmsg[5][:]
#    print 'body ' + body
    return {'time':time,'username':username,'pcname':pcname,'type':type,'body':body}


class R():
    def __init__(self):
        pass
    @staticmethod
    def exit():
        os.system("kill -9 " + str(os.getpid())) #杀掉进程

def msgdefu(bot,msg):
    return 'not define func'

def udpdefu(bot,ip,username,msg):
    return 'not define func'

def userget(ip):
    print ip

class UdpBotServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.func_dict = {}
        self.func_dict['msg'] = msgdefu
        self.func_dict['getudp'] = udpdefu
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpbotinit(sock)
        self.sock = sock
        self.r = 1
    def rcmsg(self, func_type):
        def wrapper(func):
            if func_type == 'msg':
                self.func_dict[func_type] = func
            elif func_type == 'getudp':
                self.func_dict[func_type] = func
            elif func_type == 'getuser':
                self.func_dict[func_type] = func
            else:
                self.func_dict['other'] = func
            return func
        return wrapper
    def sayhello(self,ip):
        sock = self.sock
        sock.sendto((botheader + '%d'%int(time.time()) + sendheader + hellotext).decode('utf-8').encode('gbk'), (ip, 2425))
    def udpsend(self,ip,msg):
        sock = self.sock
        sock.sendto((botheader + '%d'%int(time.time()) + sendheader + msg).decode('utf-8').encode('gbk'), (ip, 2425))
    def hellotoall(self):
        sock = self.sock
        sock.sendto((botheader + '%d'%int(time.time()) + sendheader + '你好').decode('utf-8').encode('gbk'), ('192.168.0.103', 2425))
    def run(self):
        sock = self.sock
        while(self.r):
            try:
                recver, dst_ip = sock.recvfrom(1024)
                # 对二进制数据进行解码
                print(recver.decode('gbk', errors='ignore').encode('utf-8'), dst_ip)
                msg = UserMsg(recver.decode('gbk', errors='ignore').encode('utf-8'))
                if msg['type'] == 288:
                    t = time.time()
                    sock.sendto((botheader + '%d'%int(t) + reposheader + msg['time']).decode('utf-8').encode('gbk'), dst_ip)
                    self.func_dict['msg'](self,msg['body'])
                    self.func_dict['getudp'](self,dst_ip[0], msg['username'],msg['body'])
                    #print msg['body']
                    #print 'return flag'
                else :
                    self.func_dict['getuser'](self,dst_ip[0])
            except Exception as e:
                print e
                sock.close()
                break



# 判断是否是程序的入口
if __name__ == '__main__':
    test = UdpBotServer()
    @test.rcmsg('msg')
    def my_func(bot,msg):
        print 'get msg : ' + msg
    @test.rcmsg('getudp')
    def my_func(bot,ip,username,msg):
        print 'get msg : ' + msg 
        print ' from : ' + username 
        print ' ip :' + ip
    test.run()


