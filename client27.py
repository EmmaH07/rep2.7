"""
Author: Emma Harel
Program name: client2.6
Description: A client that requests 4 things from the server: TIME, RAND, NAME, and EXIT.
The client receives a message from the server that contains the length of the message, a dollar sign($) and the message
itself.
Date: 18/11/23
"""

import socket
import logging
import protocol27
from PIL import Image
from io import BytesIO
import base64
import server_func

MAX_PACKET = 1024
REQ_LIST = ["DIR", "DELETE", "COPY", "EXECUTE", "TAKE_SCREENSHOT", "SEND_PHOTO", "EXIT"]
logging.basicConfig(filename='client27.log', level=logging.DEBUG)


def is_valid_req(request):
    for item in REQ_LIST:
        if request == item:
            return True
    return False


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        my_socket.connect(('127.0.0.1', 1729))
        logging.debug("Client connected to: 127.0.0.1:1729")
        print('Try one of the following requests: ')
        print(REQ_LIST)
        request = input("Enter request: ")

        while not is_valid_req(request):
            logging.debug("Client sent: " + request)
            print("Illegal request, try again.")
            request = input("Enter request: ")

        logging.debug("Client sent: " + request)

        while request != "EXIT":
            if request == "DIR":
                path = bytes(str(input("Please enter the files path: ")), 'utf-8')
                path = protocol27.proto_msg1(bytes(request, 'utf-8'), path)
                my_socket.send(path)
                response = my_socket.recv(MAX_PACKET)
                while not protocol27.all_msg_passed(response):
                    response += my_socket.recv(MAX_PACKET)
                print(protocol27.get_msg(response).decode())

            elif request == "DELETE":
                path = bytes(str(input("Please enter the path of the file you'd like to delete: ")), 'utf-8')
                path = protocol27.proto_msg1(bytes(request, 'utf-8'), path)
                my_socket.send(path)
                response = my_socket.recv(MAX_PACKET)
                while not protocol27.all_msg_passed(response):
                    response += my_socket.recv(MAX_PACKET)
                print(protocol27.get_msg(response).decode())

            elif request == "COPY":
                path1 = str(input("Please enter the path of the file you'd like to copy: "))
                path1 = bytes(path1, 'utf-8')
                path2 = str(input("Please enter the path of the new file: "))
                path2 = bytes(path2, 'utf-8')
                path = protocol27.proto_msg2(bytes(request, 'utf-8'), path1, path2)
                my_socket.send(path)
                response = my_socket.recv(MAX_PACKET)
                while not protocol27.all_msg_passed(response):
                    response += my_socket.recv(MAX_PACKET)
                print(protocol27.get_msg(response).decode())

            elif request == "EXECUTE":
                path = str(input("Please enter the path of the app you'd like to open: "))
                path = bytes(path, 'utf-8')
                path = protocol27.proto_msg1(bytes(request, 'utf-8'), path)
                print(path)
                my_socket.send(path)
                response = my_socket.recv(MAX_PACKET)
                while not protocol27.all_msg_passed(response):
                    response += my_socket.recv(MAX_PACKET)
                print(protocol27.get_msg(response).decode())

            elif request == "TAKE_SCREENSHOT":
                send = protocol27.proto_msg0(bytes(request, 'utf-8'))
                my_socket.send(send)
                response = my_socket.recv(MAX_PACKET)
                while not protocol27.all_msg_passed(response):
                    response += my_socket.recv(MAX_PACKET)
                print(protocol27.get_msg(response).decode())

            elif request == "SEND_PHOTO":
                send = protocol27.proto_msg0(bytes(request, 'utf-8'))
                my_socket.send(send)
                response = my_socket.recv(1).decode()
                length = response
                while response != '$':
                    length += response
                    response = my_socket.recv(1).decode()

                response = my_socket.recv(1).decode()
                msg = response
                while response != '$':
                    msg += response
                    response = my_socket.recv(1).decode()

                print(msg)
                server_func.decode_image(msg.encode())

            print('Try one of the following requests: ')
            print(REQ_LIST)
            request = input("Enter request: ")

            while not is_valid_req(request):
                logging.debug("Client sent: " + request)
                print("Illegal request, try again.")
                request = input("Enter request: ")

            logging.debug("Client sent: " + request)

        my_socket.send(protocol27.proto_msg0(b'EXIT'))
        my_socket.close()

    except socket.error as err:
        print('received socket error ' + str(err))
        logging.error(err)

    finally:
        my_socket.close()


if __name__ == "__main__":
    assert is_valid_req("EXIT")
    main()
