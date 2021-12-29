import socket
import pandas as pd
from _thread import *
import csv
serverSocket = socket.socket()
host = socket.gethostname()
port = 8093
thread_count = 0
try:
    serverSocket.bind((host,port))
except socket.error as error:
    print(str(error))
print("Waiting for Connections")
serverSocket.listen(5)

def client_thread(connection):
    df = pd.read_csv('passengers.csv')
    df1 = pd.read_csv('train_tracking.csv')
    while True:
        select = """ \n Please Enter \n 1 for General Complaints \n 2 for Tracking the Train Status \n 3 for Payment Related Enquiry """
        connection.send(select.encode('utf-8'))
        choice = connection.recv(2048)
        choice = choice.decode('utf-8')
        ch = int(choice)
        if ch == 1:
            connection.send("Enter the required information".encode('utf-8'))
            complaint = connection.recv(2048).decode('utf-8')
            complaint = eval(complaint)
            with open('passengers.csv', 'a', newline='') as f_object:
                writer_object = csv.writer(f_object)
                writer_object.writerow(complaint)
                f_object.close()
            connection.send("Complaint Registered".encode('utf-8'))
            
        elif ch == 2:
            connection.send("Passenger may view the location of the train with the train number".encode('utf-8'))
            train_num = "\n Enter the train number"
            connection.send(train_num.encode('utf-8'))
            choice = connection.recv(2048).decode('utf-8')
            details = df1.loc[df1['Train_No'] == int(choice)]
            details = details.to_string(index=False)
            fields = details.encode('utf-8')
            connection.send(fields)
            
        elif ch==3:
            connection.send("If the passenger couldn't complete the payment due to incorrect bank account password issue, then it can be reset \n Reset password will be updated".encode('utf-8'))
            pid = "\n Enter the passenger id"
            connection.send(pid.encode('utf-8'))
            choice = connection.recv(2048).decode('utf-8')
            new_password = "Enter the new password"
            connection.send(new_password.encode('utf-8'))
            password_new = connection.recv(2048).decode('utf-8')
            details = df.loc[df['P_ID'] == int(choice), 'PASSWORD'] = password_new
            df.to_csv('passengers.csv', index=False)
            details = df.loc[df['P_ID'] == int(choice)]
            details = details.to_string(index=False)
            fields = details.encode('utf-8')
            connection.send(fields)
    connection.close()
    
while True:
    client, address = serverSocket.accept()
    print("Connected to "+address[0]+str(address[1]))
    start_new_thread(client_thread, (client,))
    thread_count += 1
    print("Thread Number: "+str(thread_count))
