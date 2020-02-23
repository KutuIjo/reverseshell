import socket
import sys
import hashlib

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
    s.connect((host,port))
    print("Connected to " + host +":"+ str(port))
    
# Establish communication
def socket_communicate():
    # Receiving filename and format
    filename = str(s.recv(1024),"utf-8")

    # Receiving hash value from the server
    hash_value_rcv = str(s.recv(1024),"utf-8")
    print (hash_value_rcv)

    # Preparing file
    f = open(filename,'wb')
    # Receiving file content
    while True:
        data = s.recv(1024)
        if not data:
            break
        # write data to a file
        f.write(data)
    f.close()

    # Calculating hash value of received file 
    hash_value_ccl = md5(filename)
    print(hash_value_ccl)

    # Comparing hash value
    if  hash_value_ccl == hash_value_rcv:
        print ("File received successfully")
    else:
        print ("File corrupted")

def main():
    create_socket()
    socket_communicate()

main()