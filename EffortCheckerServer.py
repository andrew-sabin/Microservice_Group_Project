from csv import reader
import pika

# Creates the group estimates from the server's csv file 'sample_test.csv'
def getGroupEstimates():
    with open('sample_test.csv') as file:
        csv_reader = reader(file)
        colAmt = len(next(csv_reader))
        rowAmt = sum(1 for row in csv_reader)
        groupAmt = colAmt-3
        server_efforts = []

        file.close()
    with open('sample_test.csv') as file:
        csv_reader = reader(file)
        next(csv_reader)
        for row in csv_reader:
            nextFeature = []
            nextFeature.append(row[0])
            for itr in range(3,groupAmt+2):
                nextFeature.append(float(row[itr]))
            server_efforts.append(nextFeature)
        file.close()
        return server_efforts


# Grabs the test values from the message and puts them into an array and then compares them
# with the server estimates.
def sendTestGroup():
    def on_message_recieved(ch, method, properties, body):
        # Publish results over to client
        print(f"recieved new array: {body}")
        compared = compareGroups(getBody(body), getGroupEstimates())
        ch.basic_publish('', routing_key=properties.reply_to, body=compared)


    # Set consuming parameters
    connection_parameters = pika.ConnectionParameters('localhost')

    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()

    channel.queue_declare(queue='arrRPC')

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue='arrRPC', auto_ack=True, on_message_callback=on_message_recieved)

    print("started consuming")

    channel.start_consuming()

# Creates an array of sub arrays from the data from the client to be tested
def getBody(body):
    featArr = str(body)
    featArr = featArr[2:]
    featArr = featArr[0:len(featArr)-2]
    feat_grab = featArr.split(';')
    allFeats = []
    for itr in range(len(feat_grab)):
        newArr = feat_grab[itr].split(',')
        getArr = []
        for group in range(len(newArr)):
            if group == 0:
                getArr.append(newArr[group])
            else:
                getArr.append(float(newArr[group]))
        allFeats.append(getArr)
    return allFeats

# Compares the user sent in array and the server's test array so that the
def compareGroups(usrArr,testArr):
    incorrectFeats = []
    incorrectAmt = 0
    for row in range(len(testArr)):
        wrongGrps = 0
        currFeat = []
        currFeat.append('ID: ' + testArr[row][0])
        for col in range(1,len(testArr[row])-1):
            if testArr[row][col] != usrArr[row][col]:
                wrongGrps += 1
                if testArr[row][col] > usrArr[row][col]:
                    currFeat.append("Group "+ str(col) + ": " + str(testArr[row][col]) +" Smaller than estimate")
                else:
                    currFeat.append("Group " + str(col) + ": " + str(testArr[row][col]) + " Larger than estimate")
        if wrongGrps > 0:
            incorrectFeats.append(currFeat)
            incorrectAmt += 1
    if incorrectAmt > 0:
        return "Incorrect" + str(incorrectFeats)
    else:
        return "Correct"

sendTestGroup()