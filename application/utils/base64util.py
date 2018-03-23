import base64


def encode64(string):
    return base64.encodestring(string.encode())


def decode64(string):
    return base64.decodestring(string).decode()
