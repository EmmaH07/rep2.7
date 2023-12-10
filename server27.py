"""
Author: Emma Harel
Program name: server2.7
Description: a server that has 4 functions - TIME, RAND, NAME, and EXIT. the server sends a response based on the
clients request. The response contains the length of the message, a dollar sign($) and the message itself.
Date: 18/11/23
"""

import socket
import logging
import server_func
import protocol27

QUEUE_LEN = 1
MAX_PACKET = 1024

logging.basicConfig(filename='server27.log', level=logging.DEBUG)


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.bind(('0.0.0.0', 1729))
        my_socket.listen(QUEUE_LEN)
        logging.debug("server is waiting for a new client")

        while True:
            client_socket, client_address = my_socket.accept()
            logging.debug("server connected to: " + client_address[0] + ":" + str(client_address[1]))

            try:
                request = client_socket.recv(MAX_PACKET)

                while not protocol27.all_msg_passed(request):
                    request += client_socket.recv(MAX_PACKET)

                logging.debug("Server received: " + request.decode())
                while protocol27.func(request).decode() != "EXIT":
                    if protocol27.func(request).decode() == "DIR":
                        d = server_func.dir_cmd(protocol27.par1(request).decode())
                        d = protocol27.send_msg(d)
                        client_socket.send(d)

                    elif protocol27.func(request).decode() == "DELETE":
                        de = server_func.delete(protocol27.par1(request).decode())
                        de = protocol27.send_msg(de)
                        client_socket.send(de)

                    elif protocol27.func(request).decode() == "COPY":
                        c = server_func.copy(protocol27.par1(request).decode(), protocol27.par2(request).decode())
                        c = protocol27.send_msg(c)
                        client_socket.send(c)

                    elif protocol27.func(request).decode() == "EXECUTE":
                        exe = server_func.exe(protocol27.par1(request).decode())
                        exe = protocol27.send_msg(exe)
                        client_socket.send(exe)

                    elif protocol27.func(request).decode() == "TAKE_SCREENSHOT":
                        scr = server_func.take_screenshot()
                        scr = protocol27.send_msg(scr)
                        print(scr)
                        client_socket.send(scr)

                    elif protocol27.func(request).decode() == "SEND_PHOTO":
                        send = server_func.send_screenshot()
                        send = protocol27.send_msg(send)
                        print(send)
                        client_socket.send(send)

                    else:
                        send = protocol27.send_msg(b'Illegal request')
                        client_socket.send(send)

                    request = client_socket.recv(MAX_PACKET)
                    logging.debug("Server received: " + request.decode())

                logging.debug("server disconnected from: " + client_address[0] + ":" + str(client_address[1]))
                logging.debug("server is waiting for a new client")

            except socket.error as err:
                print('received socket error on client socket' + str(err))
                logging.error("received socket error on client socket: " + str(err))

            finally:
                client_socket.close()

    except socket.error as err:
        print('received socket error on server socket' + str(err))
        logging.error("received socket error on server socket")

    finally:
        my_socket.close()


if __name__ == "__main__":
    assert server_func.dir_cmd("hi") == b''
    assert server_func.delete("cyber") == b"An error accrued"
    assert server_func.copy("i_Love", "Hapoel") == b"An error accrued"
    assert server_func.exe("cyber") == b"An error accrued"
    assert server_func.take_screenshot() == b"Executed successfully" or server_func.take_screenshot() == (b"An error "
                                                                                                          b"accrued")
    assert server_func.is_valid_req("DIR")
    main()
