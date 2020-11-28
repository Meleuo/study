import socket

sr = socket.socket()
sr.bind(('0.0.0.0', 12138))
sr.listen()

while 1:
    conn, addr = sr.accept()
    text = conn.recv(1024)
    print(text.decode('utf-8'))
    msg = 'HTTP/1.1 200 ok\n request OK!'
    conn.send(msg.encode('utf-8'))
    # conn.send(text)
    conn.close()
