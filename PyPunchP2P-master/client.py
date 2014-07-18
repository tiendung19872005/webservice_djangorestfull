#!/usr/bin/env python
# coding:utf-8

import optparse
import sys
import struct
import socket
from threading import Thread, Event
import getpass 
import stun
from fabric.api import *

FullCone = "Full Cone"  # 0
RestrictNAT = "Restrict NAT"  # 1
RestrictPortNAT = "Restrict Port NAT"  # 2
SymmetricNAT = "Symmetric NAT"  # 3
UnknownNAT = "Unknown NAT" # 4
NATTYPE = (FullCone, RestrictNAT, RestrictPortNAT, SymmetricNAT, UnknownNAT)


def bytes2addr(bytes):
    """Convert a hash to an address pair."""
    if len(bytes) != 8:
        raise ValueError("invalid bytes")
    host = socket.inet_ntoa(bytes[:4])
    port = struct.unpack("H", bytes[-4:-2])[0]  # unpack returns a tuple even if it contains exactly one item
    nat_type_id = struct.unpack("H", bytes[-2:])[0]
    target = (host, port)
    return target, nat_type_id


class Client():

    def __init__(self):
        try:
            master_ip = '127.0.0.1' if sys.argv[1] == 'localhost' else sys.argv[1]
            self.master = (master_ip, int(sys.argv[2]))
            self.pool = sys.argv[3].strip()
            self.sockfd = self.target = None
            self.periodic_running = False
            self.peer_nat_type = None
            
            self.ssh_started = False
            self.ssh_server = False
#             self.user = None
            
            
        except (IndexError, ValueError):
            print sys.stderr, "usage: %s <host> <port> <pool>" % sys.argv[0]
            sys.exit(65)

    def request_for_connection(self, nat_type_id=0):
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.sockfd.sendto(self.pool + ' {0}'.format(nat_type_id), self.master)
        data, addr = self.sockfd.recvfrom(len(self.pool) + 3)
        if data != "ok " + self.pool:
            print sys.stderr, "unable to request!"
            sys.exit(1)
        self.sockfd.sendto("ok", self.master)
        sys.stderr = sys.stdout
        print sys.stderr, "request sent, waiting for partner in pool '%s'..." % self.pool
        data, addr = self.sockfd.recvfrom(8)

        self.target, peer_nat_type_id = bytes2addr(data)
        print(self.target, peer_nat_type_id)
        self.peer_nat_type = NATTYPE[peer_nat_type_id]
        print sys.stderr, "connected to {1}:{2}, its NAT type is {0}".format(self.peer_nat_type, *self.target)
          
    def clean_Buffer(self,sock):
        sock.sendto("++++++++ Begin SSH +++++++++",self.target)
        clean, addr = sock.recvfrom(1024)
        print clean
        while not clean == "++++++++ Begin SSH +++++++++":
            print clean
            clean, addr = sock.recvfrom(1024)
      
#     def ssh_Server(self,sock):  
#         import re
#         self.clean_Buffer(sock)
#         print "------------begin ssh server-------------"
#         user = getpass.getuser()
#         buffer = []
#         getpass_word = "Pass word for user %s :" % user
#         sock.sendto(getpass_word,self.target)
#         password, addr = sock.recvfrom(1024)
#         
#         def run_command(user_, password_,command):
#             with settings(hide('warnings', 'running', 'stdout', 'stderr'),user=user_, password=password_, host_string="localhost"):
#                 data =  run(command)
#                 return data
#         while True:
#             sock.sendto("your command: ",self.target)
#             
#             command, addr = sock.recvfrom(1024)
#             print command
#             if command == "exit":
#                 break
#             ####################################
#             if re.match("cd*", command):
#                 tem = str(command).split(" ")[1]
#                 print tem
#                 buffer.append(tem)
#                 #########################################
#             data = run_command(user, password, command)
#             sock.sendto(data,self.target)
    def ssh_Server(self,sock):  
        
        self.clean_Buffer(sock)
        print "------------begin ssh server-------------"
        request, addr = sock.recvfrom(1024)
        if request == "your_user:":
            
            user_ = getpass.getuser()
            sock.sendto("your_user:%s"%user_, addr)
            
            while True:
                request, addr = sock.recvfrom(1024)
                print request
                if request == "exit":
                    break
            
#     def ssh_Client(self,sock):
#         import re
#         self.clean_Buffer(sock)
#         print "------------begin ssh client---------------"
#         while True:
#             request, addr = sock.recvfrom(1024)
#             if request == "your command: " or re.match("Pass word for user*", request):
#                 reponse = raw_input(request)
#                 while reponse == "":
#                     reponse = raw_input(request)
#                 if reponse == "exit":
#                     sock.sendto(reponse, self.target)
#                     break
#                
#                 sock.sendto(reponse, self.target)
#             else:
#                 print request
#                 print "\n"
# #             data, addr = sock.recvfrom(1024)
# #             print "%s\n" data
#             
    def ssh_Client(self,sock):
#         from fabric.api import *
        import re
        self.clean_Buffer(sock)
        print "------------begin ssh client---------------"
        
        def run_command(user_, target_, sock):
            remote_p = target_[1]
            remote_bind_addr = target_[0]
#             with remote_tunnel():
            with settings(hide('warnings', 'running', 'stdout', 'stderr'), user=user_):
                run("")
                while True:
                    command = raw_input("\n\nyour command :\t")
                    if command == "exit":
                        sock.sendto(command, target_)
                        break
                    try:
                        data = run(command)
                        print data
                    except:
                        print "error"
        sock.sendto("your_user:", self.target)
        request, addr = sock.recvfrom(1024)
        if re.match("your_user:", str(request)):
            user_ = str(request).split(":")[1]
            run_command(user_,self.target,sock)
        
    def ssh_Start(self,sock):
        print "Are you ssh server ?"
        check = raw_input("server ? : y\t")
        if check == "y":
            self.ssh_server = True
        if self.ssh_server:
            print "You are Ssh Server"
#             self.ssh_Server(sock)
            Thread(target=self.ssh_Server, args=(self.sockfd,)).start()
        else:
            Thread(target=self.ssh_Client, args=(self.sockfd,)).start()
        

    def recv_msg(self, sock, is_restrict=False, event=None):
        print "master %s"% str(self.master)
        print "target %s"%str(self.target)
        print "sock %s" % str(sock)
        if is_restrict:
            while True:
                data, addr = sock.recvfrom(1024)
                sys.stdout.write(data)
                print "------------------------"
                if self.periodic_running:
                    print "periodic_send is alive"
                    self.periodic_running = False
                    event.set()
                    print "received msg from target, periodic send cancelled, chat start."
                if addr == self.target or addr == self.master:
                    
                    if self.ssh_started:
                        print "star ssh server"
                        break
                    else:
                        sys.stdout.write(data)


                    if data == "punching...\n":
                        self.ssh_started = True
                        sock.sendto("end punching\n", addr)
                        #######################################
                    else:
                        self.ssh_started = True

        else:
            while True:
                data, addr = sock.recvfrom(1024)
                sys.stdout.write(data)
                print "------------------------"
                if addr == self.target or addr == self.master:
                    sys.stdout.write(data)


                    if self.ssh_started:
                        print "star ssh client"
                        break
                    else:
                        sys.stdout.write(data)
                        
                    if data == "punching...\n":  # peer是restrict
                        sock.sendto("end punching", addr)
                        
                        self.ssh_started = True
                        #######################################
                    else:
                        self.ssh_started = True

    def send_msg(self, sock):
        import time
        sock.sendto("punching...\n",self.target)
        while not self.ssh_started:
            time.sleep(1)
        self.ssh_Start(sock)#### begin ssh

    def chat_fullcone(self):
        Thread(target=self.send_msg, args=(self.sockfd,)).start()
        Thread(target=self.recv_msg, args=(self.sockfd,)).start()

    def chat_restrict(self):
        from threading import Timer
        cancel_event = Event()

        def send(count):
            self.sockfd.sendto('punching...\n', self.target)
            print("UDP punching package {0} sent".format(count))
            if self.periodic_running:
                Timer(0.5, send, args=(count + 1,)).start()

        self.periodic_running = True
        send(0)
        kwargs = {'is_restrict': True, 'event': cancel_event}
        Thread(target=self.recv_msg, args=(self.sockfd,), kwargs=kwargs).start()
        cancel_event.wait()
        Thread(target=self.send_msg, args=(self.sockfd,)).start()

    def chat_symmetric(self):
        """
        Completely rely on relay server(TURN)
        """
        def send_msg_symm(sock):
            while True:
                data = 'msg ' + sys.stdin.readline()
                sock.sendto(data, self.master)

        def recv_msg_symm(sock):
            while True:
                data, addr = sock.recvfrom(1024)
                if addr == self.master:
                    sys.stdout.write(data)
        Thread(target=send_msg_symm, args=(self.sockfd,)).start()
        Thread(target=recv_msg_symm, args=(self.sockfd,)).start()

    def main(self, test_nat_type=None):
        """
        nat_type是自己的nat类型
        peer_nat_type是从服务器获取的对方的nat类型
        选择哪种chat模式是根据nat_type来选择, 例如我这边的NAT设备是restrict, 那么我必须得一直向对方发包,
        我的NAT设备才能识别对方为"我已经发过包的地址". 直到收到对方的包, periodic发送停止
        """
        if not test_nat_type:
            nat_type, _, _ = self.get_nat_type()
        else:
            nat_type = test_nat_type  # 假装正在测试某种类型的NAT
        try:
            self.request_for_connection(nat_type_id=NATTYPE.index(nat_type))
        except ValueError:
            print("NAT type is %s" % nat_type)
            self.request_for_connection(nat_type_id=4)  # Unknown NAT

        if nat_type == UnknownNAT or self.peer_nat_type == UnknownNAT:
            print("Symmetric chat mode")
            self.chat_symmetric()
        if nat_type == SymmetricNAT or self.peer_nat_type == SymmetricNAT:
            print("Symmetric chat mode")
            self.chat_symmetric()
        elif nat_type == FullCone:
            print("FullCone chat mode")
            self.chat_fullcone()
        elif nat_type in (RestrictNAT, RestrictPortNAT):
            print("Restrict chat mode")
            self.chat_restrict()
        else:
            print("NAT type wrong!")

    @staticmethod
    def get_nat_type():
        parser = optparse.OptionParser(version=stun.__version__)
        parser.add_option("-d", "--debug", dest="DEBUG", action="store_true",
                          default=False, help="Enable debug logging")
        parser.add_option("-H", "--host", dest="stun_host", default=None,
                          help="STUN host to use")
        parser.add_option("-P", "--host-port", dest="stun_port", type="int",
                          default=3478, help="STUN host port to use (default: "
                          "3478)")
        parser.add_option("-i", "--interface", dest="source_ip", default="0.0.0.0",
                          help="network interface for client (default: 0.0.0.0)")
        parser.add_option("-p", "--port", dest="source_port", type="int",
                          default=54320, help="port to listen on for client "
                          "(default: 54320)")
        (options, args) = parser.parse_args()
        if options.DEBUG:
            stun.enable_logging()
        kwargs = dict(source_ip=options.source_ip,
                      source_port=int(options.source_port),
                      stun_host=options.stun_host,
                      stun_port=options.stun_port)
        nat_type, external_ip, external_port = stun.get_ip_info(**kwargs)
        print "NAT Type:", nat_type
        print "External IP:", external_ip
        print "External Port:", external_port
        return nat_type, external_ip, external_port
        
        
        
if __name__ == "__main__":
    c = Client()
    try:
        test_nat_type = NATTYPE[int(sys.argv[4])]  # 输入数字0,1,2,3
    except IndexError:
        test_nat_type = None
#################################
#     c.user = getpass.getuser()
    c.main(test_nat_type)
    


# 
# Host *.kd.io
#     User tiendungyahoo
#     ProxyCommand ssh %r@ssh.koding.com nc %h %p
