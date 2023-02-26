# Microservice_Group_Project
Microservice Project For Jonathan's Group Project

## Requesting Data
The user will edit the sample_data.csv file to fit their estimates, then send the arrays related to the csv file to the server as a message. The server will then process the message into a new array to be compared with it's own recorded efforts. The messages are sent over to the server using the RabbitMQ message broker AMQP.

## Recieving Data
After comparing the group efforts of both csv files, the server will return the result. If the server finds no errors when comparing the two efforts the server will return "correct". In the case the server finds a different group effort for the feature, the server will return "incorrect" along with the different feature ID's and group associated with the incident and the entered in effort, where it will let the client know if the effort was higher or lower than expected.

## UML Sequence Diagram
![Alt text](https://raw.githubusercontent.com/andrew-sabin/Microservice_Group_Project/main/UML%20Screenshot.PNG "UML for microservice")
