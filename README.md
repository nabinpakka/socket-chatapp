# A chat app using socket programming

This project is for the requirement of CSCE513 Computer Networks course. The project supports personal chat, group chat, file transfer,
and encrypted chat.

To run the project, use following commands inside `chatapp` directory.

```
python chat_server.py
python chat_client.py
```

A username is required to start connection with the server. Then the console will show options for the chat. Choose a 
number from the options.

## Personal message

A receiver username will be asked for chatting. If the receiver is not connected to the server, then a error msg is returned from the server.
The personal message is encrypted using AES algorithm.

## Group chat

You can discuss in a group as well. Currently, only one group is available. All the connected users will receive the group message. 
The messages are encrypted. 

## File transfer

You can transfer file to a specified user using socket. A receiver username will be asked before the initiation of file transfer. 
The files will be saved under `chatapp/files/client/<username>`. The files to be transferred should be under `chatapp/files/client/<username>`.

