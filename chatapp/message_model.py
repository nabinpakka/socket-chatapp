
class Message:
    def __init__(self, sender, receiver, msg, msg_type, filename = None) -> None:
        self.sender = sender
        self.msg = msg
        self.receiver = receiver
        self.type = msg_type
        self.filename = filename

    def from_dict(self, dict):
        self.sender = dict["sender"]
        self.msg = dict["msg"]
        self.receiver = dict["receiver"]
        self.type = dict["msg_type"]
        self.filename = dict.get("filename", None)
        return self

    def __str__(self) -> str:
        return str({
            "sender" : self.sender,
            "receiver" : self.receiver,
            "type" : self.type,
            "msg" : self.msg,
            "filename" : self.filename
        })