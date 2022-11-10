# Data Streaming API Layer between QRadar and MongoBD

## Description
QRadar is a SIEM tool. QRadar stores historical data on event processors in its Ariel Database. Each Event Processor (EP) has its forwarding service that queries the database using AQL and forwards the data to a specified destination IP and port. In this case, multiple EPs are forwarding data to the same "forwarding destination".
QRadar forwards the log data as JSON strings, where each log corresponds to 1 JSON string. This script acts as an API by listening to the data coming onto the socket. We only move ahead in the script if the connection originates from a known source.

Every newline is inserted into a Queue. A separate task is started to read the data from this Queue. The data is processed asynchronously, where each JSON string is converted into a dictionary. A timestamp and the client IP address are appended to this dictionary.
Since customer data needs to be segregated into individual databases, the customer name is extracted from this dictionary and used as the database name. A different thread is used to insert the data into MongoDB.