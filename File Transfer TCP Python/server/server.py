import socket
import hashlib

# Filename and format definition
filename = 'Package.txt' 

# Hashing with MD5 algorithm 
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Create socket
def create_socket():
    try:
        global host
        global port
        global s
        host = "192.168.100.20"
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
        print("Now listening for connection...")

    except socket.error as msg:
        print ("Socket binding error: "+ str(msg) +"\n" + "Retrying...")
        bind_socket()

# Establish connection with a client (socket must be listening)
def socket_accept():
    global conn
    conn, address = s.accept() #return object of conversation and list of IP addresses and port
    print("Connection has been established!\n" + "IP: " + address[0] +"\n"+ "Port: " +str(address[1]))

# Sending commands to client shell
def socket_communicate(conn):
    try:
        # Sending filename and format
        conn.send(str.encode(filename))

        # Getting hash value of sent file
        hash_value = md5(filename)

        # Sending hash value
        conn.send(str.encode(hash_value))

        # Preparing file
        f = open(filename,'rb')
        buffer = f.read(1024)

        # Sending file content
        while (buffer):
            conn.send(buffer)
            buffer = f.read(1024)
        f.close()
        print("File succesfully sent")
        
    except:
        print("Sending file error")
    
    print(hash_value)
    conn.close()
            
def main():
    create_socket()
    bind_socket()
    socket_accept()
    socket_communicate(conn)
    s.close()

main()