from src.server import Server

from config import IP_K

my_server = Server(IP_K, 1234)

my_server.start()