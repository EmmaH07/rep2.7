"""
Author: Emma Harel
Program name: server2.7
Description: a server that has 4 functions - TIME, RAND, NAME, and EXIT. the server sends a response based on the
clients request. The response contains the length of the message, a dollar sign($) and the message itself.
Date: 18/11/23
"""


def proto_msg0(b_request):
    """
    :param b_request:
    :return: a msg containing the complete msg length, a dollar sign (to be used as a seperator), the function's name,
    and two "empty" slots divided by dollar signs. the new msg's type is bytes.
    """
    new_msg = b_request + b'$' + b' ' + b'$' + b' '
    new_msg = bytes(str(len(new_msg)), 'utf-8') + b'$' + new_msg
    return new_msg


def proto_msg1(b_func, b_par):
    """
    :param b_func:
    :param b_par:
    :return: a msg containing the complete msg length, a dollar sign (to be used as a seperator), the function's name,
    a dollar sign, the parameter for the function, another dollar sign and an "empty" slot in bytes.
    """
    new_msg = b_func + b'$' + b_par + b'$' + b' '
    len_msg = str(len(new_msg))
    new_msg = bytes(len_msg, 'utf-8') + b'$' + new_msg
    return new_msg


def proto_msg2(b_func, b_par1, b_par2):
    """
    :param b_func:
    :param b_par1:
    :param b_par2:
    :return: a msg containing the complete msg length, a dollar sign (to be used as a seperator), the function's name, a
    dollar sign, the parameter for the function, another dollar sign, and the second parameter for the function. the
    new msg is in bytes.
    """
    new_msg = b_func + b'$' + b_par1 + b'$' + b_par2
    len_msg = str(len(new_msg))
    new_msg = bytes(len_msg, 'utf-8') + b'$' + new_msg
    return new_msg


def func(p_msg):
    """
    :param p_msg:
    :return: a msg containing the function's name part of the protocol msg as bytes.
    """
    try:
        str_msg = p_msg.decode()
        msg_arr = str_msg.split('$')
        return msg_arr[1].encode()
    except Exception as err:
        return str(err).encode()


def par1(p_msg):
    """
    :param p_msg:
    :return: a msg containing the first parameter part of the protocol msg as bytes.
    """
    str_msg = p_msg.decode()
    msg_arr = str_msg.split('$')
    return msg_arr[2].encode()


def par2(p_msg):
    """
    :param p_msg:
    :return: a msg containing the second part of the protocol msg.
    """
    str_msg = p_msg.decode()
    msg_arr = str_msg.split('$')
    return msg_arr[3].encode()


def send_msg(b_msg):
    """
    :param b_msg:
    :return: a msg containing the length of the return msg, a dollar sign as a seperator and the return msg itself.
    the msg is in bytes.
    """
    new_msg = b_msg + b'$' + b' ' + b'$' + b' '
    new_msg = bytes(str(len(new_msg)), 'utf-8') + b'$' + new_msg
    return new_msg


def get_msg(p_msg):
    str_msg = p_msg.decode()
    msg_arr = str_msg.split('$')
    return bytes(msg_arr[1], 'utf-8')


def all_msg_passed(p_msg):
    str_msg = p_msg.decode()
    msg_arr = str_msg.split('$')
    byte_msg = bytes(msg_arr[1], 'utf-8') + b'$' + bytes(msg_arr[2], 'utf-8') + b'$' + bytes(msg_arr[3], 'utf-8')
    if msg_arr[0] == str(len(byte_msg)):
        return True
    else:
        return False
