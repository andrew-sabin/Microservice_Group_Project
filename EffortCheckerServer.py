import time,os
from csv import reader
server_efforts = []
server_groups = []
def getGroupEstimates():
    with open('Group_Estimate_Example.csv') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if row[1] != 'Effort':
                server_groups.append(row[0])
                server_efforts.append(row[1])



def sendTestGroup():
    service_file = open('microservice-test','w',encoding="utf-8")
    service_file.write('standby')
    service_file.close()
    time.sleep(5.0)
    getGroupEstimates()
    service_file = open('microservice-test','r')
    file_read = service_file.read()
    service_file.close()
    while file_read == 'standby' or file_read == 'incorrect' or file_read =='correct':
        time.sleep(5.0)
        service_file = open('microservice-test', 'r')
        file_read = service_file.read()
        service_file.close()
    time.sleep(5.0)
    with open('microservice-test') as read_file:
        text = read_file.read()
    read_file.close()
    request = text.split(',')
    for itr in range(0, len(server_efforts)):
        if server_efforts[itr] != request[itr]:
            service_file = open('microservice-test', 'w', encoding="utf-8")
            service_file.write('incorrect')
            service_file.close()
            break
    service_file = open('microservice-test','r')
    file_read = service_file.read()
    service_file.close()
    if file_read != 'incorrect':
        service_file = open('microservice-test', 'w', encoding="utf-8")
        service_file.write('correct')
        service_file.close()

sendTestGroup()