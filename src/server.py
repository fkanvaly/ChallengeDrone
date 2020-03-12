import sys
import socket
import selectors
import types


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sel = selectors.DefaultSelector()
        self.Received_messages = []
        self.imgcounter = 1
        self.basename = "image%s.png"

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
       # print("accepted connection from", addr)
        conn.setblocking(True)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)

    def receive_img(self, key, mask, size, filename):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ: 
            BUFF_SIZE = 4096 # 4 KiB
            recv_data = b''
            while len(recv_data)<size:
                part = sock.recv(BUFF_SIZE)
                recv_data += part 
            myfile = open(filename, 'wb')
            myfile.write(recv_data)
            self.Received_messages += [self.basename % self.imgcounter]
            print(self.Received_messages)
            self.imgcounter += 1
            repr("GOT IMAGE")
           # print("echoing", repr("GOT IMAGE"), "to", data.addr)
            sent = sock.send(bytes("GOT IMAGE",'utf-8'))  # Should be ready to write
           # print("closing connection to", data.addr)
            self.sel.unregister(sock)
            myfile.close()
            sock.close()

    def receive_msg(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
                self.Received_messages += [recv_data.decode("utf-8")]
                print(self.Received_messages)
            else:
               # print("closing connection to", data.addr)
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                repr(data.outb)
               # print("echoing", repr(data.outb), "to", data.addr)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]
                
    def service_connection(self, key, mask):
        if len(self.Received_messages) !=0 and self.Received_messages[-1].split()[0] == "sending_image" :
            size = int(self.Received_messages[-1].split()[1])
            filename = self.Received_messages[-1].split()[2]
            self.receive_img(key, mask, size, filename)
        else:
            self.receive_msg(key, mask)

    def start(self):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((self.host, self.port))
        lsock.listen()
        print("listening on", (self.host, self.port))
        lsock.setblocking(False)
        self.sel.register(lsock, selectors.EVENT_READ, data=None)
        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()

#yahya = '192.168.1.153'
#my_server = Server(yahya,1234)
#my_server.start()