import sys
import socket
import selectors
import types
import time
from time import sleep


class Client:

    def __init__(self,host,port,num):
        self.host = host
        self.port = port
        self.sel = selectors.DefaultSelector()
        self.client_num = num
        self.Received_messages = []

    def start_connections(self, messages):
        server_addr = (self.host, self.port)
        connid = self.client_num
        print("starting connection", connid, "to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=list(messages),
            outb=b"",
        )
        self.sel.register(sock, events, data=data)


    def service_connection(self, key, mask, messages):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                print("received", repr(recv_data), "from connection", data.connid)
                data.recv_total += len(recv_data)
                self.Received_messages += [recv_data.decode("utf-8")]
            if not recv_data or data.recv_total == data.msg_total:
                print("closing connection", data.connid)
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if not data.outb and data.messages:
                data.outb = data.messages.pop(0)
            if data.outb:
                # repr(data.outb)
                sleep(0.001)
                # print("sending", repr(data.outb), "to connection", data.connid)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]


    def send_message(self,message):
        messages = [bytes(message, 'utf-8')]
        self.start_connections(messages)
        try:
            while True:
                events = self.sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        self.service_connection(key, mask, messages)
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")

    def send_img(self,filename):
        myfile = open(filename, 'rb')
        image_bytes = myfile.read()
        size = len(image_bytes)
        notif = "sending_image %s" %size
        messages = [bytes(notif, 'utf-8'), image_bytes]
        self.start_connections(messages)
        try:
            while True:
                events = self.sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        self.service_connection(key, mask, messages)
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        myfile.close()

#tom = '192.168.1.112'
