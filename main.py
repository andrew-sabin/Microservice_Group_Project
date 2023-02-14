import time, os
from csv import reader,writer
def enterGroupEstimates():
    group_amt = 4
    # finished = False
    groups = []
    efforts = []
    curr_group = 1
    while curr_group <= group_amt:
        group_effort = input("Please enter the group amount estimate")
        group_effort = int(group_effort)
        groups.append("Group "+str(curr_group))
        efforts.append(group_effort)
        curr_group += 1
    service_file = open('microservice-test', 'r')
    read_file = service_file.read()
    service_file.close()
    while read_file != 'standby':
        time.sleep(5.0)
        service_file = open('microservice-test', 'r')
        read_file = service_file.read()
        service_file.close()
    time.sleep(5.0)
    service_file = open('microservice-test', 'w', encoding="utf-8")
    for itr in range(0,len(efforts)):
        service_file.write(str(efforts[itr])+',')
    service_file.close()
    time.sleep(5.0)
    service_file2 = open('microservice-test','r')
    file_read = service_file2.read()
    service_file2.close()
    while file_read != 'correct' and file_read != 'incorrect':
        time.sleep(5.0)
        service_file2 = open('microservice-test', 'r')
        file_read = service_file2.read()
        service_file2.close()
    return file_read


print(enterGroupEstimates())


