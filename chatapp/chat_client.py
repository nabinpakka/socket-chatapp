import os.path
import pickle
import select
import socket
import errno
import sys
import threading
import time

from file_handler import FileHandler
from message_model import Message
from cyptographer import Cryptograher

HEADER_LENGTH = 10
CLIENT_DIR_PATH = "/Users/hubbleloo/PycharmProjects/pythonProject/chatapp/files/client"


IP = "127.0.0.1"
PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

PASSWORD = b'PASSWORD1234'
SALT = b'SALT1234'


def listen_for_message():
    while True:
        try:
            # looping over the messages
            while True:
                username_header = client_socket.recv(HEADER_LENGTH)

                # if no data is received, the server has gracefully closed a connection
                if not len(username_header):
                    print("Connection has been closed by the server.")
                    sys.exit()

                username_length = int(username_header.decode("utf-8").strip())
                username = client_socket.recv(username_length).decode("utf-8")

                # getting message
                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode("utf-8").strip())
                message = client_socket.recv(message_length).decode("utf-8")

                print(f"{username} > {message}\n")
        except IOError as e:
            # This is normal on non blocking connections - when there are no incoming data error is going to be raised
            # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
            # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
            # If we got different error code - something happened
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()

            # We just did not receive anything
            continue

        except Exception as e:
            # Any other exception - something happened, exit
            print('Reading error: '.format(str(e)))
            sys.exit()

def get_msg_type() -> int:
    print("What type of message do you want to send? Choose a number from followings.")
    print("1. Personal")
    print("2. Group")
    print("3. File transfer")
    print("4. Encrypted")
    msg_type = int(input())
    return msg_type

def handle_file_receive(message):
    filehandler = FileHandler(client_socket)
    filename = os.path.basename(message.filename)
    output_path = CLIENT_DIR_PATH + "/" + my_username + "/" + filename
    filehandler.receive_and_save_file(output_path, int(message.msg))
def start_messaging(msg_type = "personal", receiver = None):
    cryptographer = Cryptograher(PASSWORD, SALT)
    key = cryptographer.derive_key()
    while True:
        # Check if there is any input to read
        sockets_list = [sys.stdin, client_socket]
        read_sockets, _, _ = select.select(sockets_list, [], [], 0.1)

        for socket in read_sockets:
            if socket == sys.stdin:
                message = sys.stdin.readline().strip()
                encrypted_msg = cryptographer.encrypt(message, key)
                print(f"{my_username} > {message}")
                print(f"{my_username} > encrypted > {encrypted_msg}")

                msg = Message(my_username, receiver, encrypted_msg, msg_type)
                msg = pickle.dumps(msg)
                msg = bytes(f"{len(msg):<{HEADER_LENGTH}}", 'utf-8') + msg

                client_socket.send(msg)
            else:
                try:
                    # looping over the messages
                    while True:
                        # username_header = client_socket.recv(HEADER_LENGTH)
                        # # if no data is received, the server has gracefully closed a connection
                        # username_length = int(username_header.decode("utf-8").strip())
                        # username = client_socket.recv(username_length).decode("utf-8")
                        # getting message
                        message_header = client_socket.recv(HEADER_LENGTH)
                        if not len(message_header):
                            print("Connection has been closed by the server.")
                            sys.exit()
                        message_length = int(message_header.decode("utf-8").strip())
                        message = client_socket.recv(message_length)
                        message = pickle.loads(message)

                        if(message.type == "file_transfer"):
                            handle_file_receive(message)

                        decrypted_msg = cryptographer.decrypt(message.msg, key)
                        print(f"{message.sender} > encrypted > {message.msg}")
                        print(f"{message.sender} > {decrypted_msg}")

                except IOError as e:
                    # This is normal on non blocking connections - when there are no incoming data error is going to be raised
                    # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                    # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                    # If we got different error code - something happened
                    if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                        print('Reading error: {}'.format(str(e)))
                        sys.exit()

                    # We just did not receive anything
                    continue

                except Exception as e:
                    # Any other exception - something happened, exit
                    print('Reading error: '.format(str(e.__str__())))
                    sys.exit()


def send_file(filepath, receiver):
    filesize = os.path.getsize(filepath)
    filehandler = FileHandler(client_socket)

    # first send msg for file transfer
    msg = str(filesize)
    message = Message(my_username, receiver,msg, "file_transfer", filepath)
    message = pickle.dumps(message)
    message = bytes(f"{len(message):<{HEADER_LENGTH}}", 'utf-8') + message
    client_socket.send(message)

    filehandler.send_file(filepath)

if __name__ == '__main__':
    my_username = input("Enter a username: ")

    # setting the socket to non-blocking mode
    client_socket.setblocking(False)

    #encoding the username to send to the server instantly after making a connection
    username = my_username.encode("utf-8")
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)

    time.sleep(1)
    ack = client_socket.recv(1048)
    print("Acknowledgement received from the server: ", str(ack.decode("utf-8")))
    #
    # listener = threading.Thread(target=listen_for_message)
    # listener.start()

    # defines how a message is going to be sent
    msg_type = get_msg_type()

    if msg_type == 1:
        # this is personal message type
        receiver = input("Enter username of receiver: ")

        start_messaging("personal", receiver)
    elif msg_type ==2:
        start_messaging("group")
    elif msg_type == 3:
        receiver = input("Enter username of receiver: ")
        filepath = CLIENT_DIR_PATH + "/"+my_username+"/" + "test.txt"
        send_file(filepath, receiver)




