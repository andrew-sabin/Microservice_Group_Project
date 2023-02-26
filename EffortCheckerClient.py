import time, os
from csv import reader,writer
import pika
import uuid

class GroupEstimates(object):
    def enterGroupEstimates(self):

        # Creates the message to be sent over to the EffortCheckerServer
        message = ""
        self.full_result = ""
        with open('sample_data.csv') as file:
            csv_reader = reader(file)
            groupAmt = len(next(csv_reader))-4
            for row in csv_reader:
                if row[1] != 'Title':
                    message += str(row[0]) + ','
                    for col in range(3,groupAmt+3):
                        message += str(row[col]+',')
                    message += str(row[groupAmt+3] +';')

        def on_message_recieved(ch, method, properties, body):
            print(f"recieved message: {body}")
            result = str(body)
            result = result[2:]
            result = result[:len(result)-1]
            channel.connection.close()
            self.full_result = result



        # Sending Array Over to Server

        connection_parameters = pika.ConnectionParameters('localhost')

        connection = pika.BlockingConnection(connection_parameters)

        channel = connection.channel()

        reply_queue = channel.queue_declare(queue='', exclusive=True)

        cor_id = str(uuid.uuid4())

        channel.queue_declare(queue='arrRPC')

        channel.basic_publish(exchange='', routing_key='arrRPC',
                              properties=pika.BasicProperties(reply_to=reply_queue.method.queue, correlation_id=cor_id),
                              body=message)

        print(f'Sent Array: {message}')

        # sets consume for grabbing the result from the server

        channel.basic_consume(queue=reply_queue.method.queue, auto_ack=True, on_message_callback=on_message_recieved)

        print("started consuming")

        channel.start_consuming()

        return self.full_result

# Sets the full_estimates object as a GroupEstimates object
full_estimates = GroupEstimates()

# Grabs the full estimates and then prints the result
print("Requesting Estimate Check")
response = full_estimates.enterGroupEstimates()
print(response)