import socket
clientSocket = socket.socket()
host = socket.gethostname()
port = 8093
print("Waiting for connection")
try:
    clientSocket.connect((host,port))
except socket.error as error:
    print(str(error))
welcome = 'WELCOME TO RAILWAY HELPDESK'
print(welcome)
print(clientSocket.recv(2048).decode('utf-8'))

while True:
    sel = input()
    selected = sel.encode('utf-8')
    clientSocket.send(selected)
    msg = clientSocket.recv(2048).decode('utf-8')
    #Complaint Registration
    if (msg and sel == '1'): 
        print(msg)
        pas_id = input("Enter the Passenger id: ")
        username = input("Enter the username: ")
        issue = input("Enter the complaint briefly: ")
        reg_complaint = [pas_id, username, issue]
        reg_complaint = str(reg_complaint)
        clientSocket.send(reg_complaint.encode('utf-8'))
        choice = clientSocket.recv(1024)
        print(choice.decode('utf-8'))
    
    #Train Tracking
    elif (msg and sel == '2'): 
        print(msg)
        inp = clientSocket.recv(2048).decode('utf-8')
        print(inp)
        trainNo = input()
        clientSocket.send(trainNo.encode('utf-8'))
        info = clientSocket.recv(2048).decode('utf-8')
        print(info)
    
    #Password Reset
    elif(msg and sel == '3'):
        print(msg)
        inp = clientSocket.recv(2048).decode('utf-8')
        print(inp)
        pas_id = input()
        clientSocket.send(pas_id.encode('utf-8'))
        inp = clientSocket.recv(2048).decode('utf-8')
        print(inp)
        pswd = input()
        clientSocket.send(pswd.encode('utf-8'))
        info = clientSocket.recv(2048).decode('utf-8')
        print(info)
clientSocket.close()

