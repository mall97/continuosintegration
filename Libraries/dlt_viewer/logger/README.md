# **Logger**

Logger is a library that receives logs from different APIs and can redirect them to other locations, namely robot_shell.
Also, logs are shown in the console and can be written into a file containing all the logs associated with the run_server2.0.


## Contents
---

 * [Complementary Files](#complementary-files)
 * [Logger Server API Commands](#logger-server-api-commands)
 * [Start Logger Server](#start-logger-server)
 * [Logger Server Dependencies](#logger-server-dependencies)


## Complementary Files
---
To perform operation on the logger library it is required the following modules:

* ***logger_server.py -***  This is the Logger server where it will be executed the Robot Framework Remote Server.

* ***logger_api.py -***  This is the Logger API containing the classes to handle logs received across the network and write those logs in a file. This file will contain all logs sent to the logger by the APIs.  

* ***configuration.json -***  This is the Logger configuration file containing the information regarding hosts and ports relevant for the logger. It also contains information regarding storage of the logs (logs directory and file name).  

## Logger Server API Commands
---

This section will be used to explain the API operations.

This server, written in python, makes possible a wide range of operations that interacts with Logger module. It is composed of the following main functions/classes:

    > handleLogs

    > LogRecordSocketReceiver
        > serve_until_stopped

    > LogRecordStreamHandler
        > handle
        > handleLogRecord


---


**handleLogs**, this function is responsible for setting up the logging configuration.
    In this function two handlers are added: a streamHandler and a FileHandler.   
    The streamHandler sends logging output to streams, in our case, prints directly to the console.
    The FileHandler sends the logging output to the file specified in the handler.

    E.g. handleLogs()

**LogRecordSocketReceiver**, this class contains the TCP socket-based logging receiver. The TCP server will listen to the IP and Port specified along with the name of the request handler.

    E.g. LogRecordSocketReceiver(host='127.0.0.1',port=21000,handler=self.LogRecordStreamHandler)

**LogRecordStreamHandler**, is a handler for a streaming logging request.
    This class is composed by two functions: handle() and handleLogRecord(record).  
    The handle() function is responsible for receiving the data from the socket and create a new LogRecord instance.  
    The handleLogRecord(record) function handles a record by passing it to all handlers associated with this logger, in this case, to the logger configured in handleLogs() function.


## Start Logger Server
---

Logger Server takes three arguments:

* **--ip**, a string value with the IP of the Logger Robot Framework Remote Server (Default: '127.0.0.1')
* **--port**, represents the port of the Robot Framework Logger Remote Library Server (Default: 21000)
* **--logger**, path to the logger configuration file (Default: 'D:/Workspace/APPS/bmw-gen5-robot-ci/libraries/altran/logger/configuration.json')

To start the server, you simply execute it with python:

            python logger_server.py

**NOTE:** This server is also started by the main Robot Object (run_server2.0).

## Logger Server Dependencies

This server has no dependencies.
