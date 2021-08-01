##############################################################################
###-           {Simple API to gather logs from other APIs}                ##-#
###-Logger API                                                            ##-#
###-Authors:  Raquel Ribeiro                                              ##-#
##############################################################################

##############################################################################
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
##############################################################################
import os
import json
import pickle
import logging
import logging.handlers
import socketserver
import struct
import select

##############################################################################
# ----------------------------------------------------------------------------
# Logger Api
# ----------------------------------------------------------------------------
##############################################################################
class Api(object):
    """
        :description:           Api for logger
        :params:                None
        :return:                Object LoggerApi
    """

    ####################################################################################################################
    # -----------------------------------------------------------------------------
    #   Global Variables
    # -----------------------------------------------------------------------------

    global logger_name
    logger_name            = 'logger_server'

    # --------------------------------------------------------------------------
    #   Information, warning and Error messages
    # --------------------------------------------------------------------------
    __FILE_ERROR          = 'Failed to open file %s\nMake sure the path is correct.'

    ####################################################################################################################
    # ------------------------------------------------------------------------
    #   Constructor
    # ------------------------------------------------------------------------
    def __init__(self, params):
        """
            :description:          Initialize constructors
            :param params:         Parameters passed to the Api
            :return:               void
        """

        self.__ip               = params['ip']
        self.__port             = params['port']

        self.__logger           = self.__load_json(params['logger'] )
        self.__logs_file_path   = os.path.join(self.__logger['log_to_api']['log_folder'], self.__logger['log_to_api']['log_file'])

        self.__shell_ip         = self.__logger['log_to_shell']['host']
        self.__shell_port       = int(self.__logger['log_to_shell']['port'])

        self.handleLogs()
        self.socketLogger()

    ##########################################################################
    # ------------------------------------------------------------------------
    #  Destructor
    # ------------------------------------------------------------------------
    def __del__(self):
        """
            :description:           Destructor. Destroys all objects.
            :return:                void
        """
        logging.info('__del__()')

    ##########################################################################
    # ------------------------------------------------------------------------
    #  Logs configuration
    # ------------------------------------------------------------------------
    def handleLogs(self):
        """
            :description:          Set up logging configuration
            :return:               void
        """

        # create logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # define type of handler
        ch = logging.StreamHandler()
        fh = logging.FileHandler(self.__logs_file_path)
        socketHandler = logging.handlers.SocketHandler(self.__shell_ip, self.__shell_port)

        # create formatter
        self.formatLogMessage = '[%(asctime)s] [%(module)s] [%(levelname)-2s] %(message)s'
        formatter = logging.Formatter(fmt=self.formatLogMessage, datefmt='%Y/%m/%d %H:%M:%S')

        # add formatter
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        socketHandler.setFormatter(formatter)

        # add handlers to logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.addHandler(socketHandler)



    ##########################################################################
    # ------------------------------------------------------------------------
    #  Handle logs
    # ------------------------------------------------------------------------
    def socketLogger(self):
        """
            :description:          Function to initialize the socket receiver
            :return:               void
        """

        self.tcpserver = self.LogRecordSocketReceiver(host=self.__ip,port=self.__port,handler=self.LogRecordStreamHandler)
        print('About to start Logger server...')
        self.tcpserver.serve_until_stopped()

   ####################################################################################################################
    # -----------------------------------------------------------------------------
    # Classes
    # -----------------------------------------------------------------------------
    ####################################################################################################################

    class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
        """
        Simple TCP socket-based logging receiver.
        """

        def __init__(self, host, port, handler):
            """
            :description:          Initialize socket server
            :param host:           ServerAddress IP
            :param port:           ServerAddress Port
            :param handler:        TCPClientHandler
            :return:               void
            """

            socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
            self.abort = 0
            self.timeout = 1

        def serve_until_stopped(self):
            """
            :description:          Monitor sockets
            :return:               void
            """
            abort = 0
            while not abort:
                rd, wr, ex = select.select([self.socket.fileno()], [], [], self.timeout)
                if rd:
                    # Process request
                    self.handle_request()
                abort = self.abort


    class LogRecordStreamHandler(socketserver.StreamRequestHandler):
        """
        Handler for a streaming logging request.
        """

        def handle(self):
            """
            :description:          Handle multiple socket requests
            :return:               void
            """

            while True:
                # Receive data from the socket in chunks of 4 bytes
                chunk = self.connection.recv(4)
                if len(chunk) < 4:
                    break
                # Handle binary data from network connection
                slen = struct.unpack('>L', chunk)[0]
                # Receive full message in bytes
                # slen represents the buffersize of the message received
                chunk = self.connection.recv(slen)
                while len(chunk) < slen:
                    chunk = chunk + self.connection.recv(slen - len(chunk))
                # Reconstituted object hierarchy of the pickled representation bytes_object of an object
                obj =  pickle.loads(chunk)
                # Creates new LogRecord instance
                record = logging.makeLogRecord(obj)
                self.handleLogRecord(record)

        def handleLogRecord(self, record):
            """
            :description:          Log records received
            :return:               void
            """

            logger = logging.getLogger(logger_name)
            logger.handle(record)


    ####################################################################################################################
    # -----------------------------------------------------------------------------
    # helpers
    # -----------------------------------------------------------------------------
    ####################################################################################################################

    # -----------------------------------------------------------------------------
    # Help docstring
    # -----------------------------------------------------------------------------
    def help(self):
        return str(help(self ))

    # -----------------------------------------------------------------------------
    # Load json
    # -----------------------------------------------------------------------------
    def __load_json(self, file_to_load):
        """
            :description:           Function to load json 
            :param file_to_load:    Path for the json file to be loaded
            :return:                void
        """
        try:
            with open(file_to_load) as json_file:
                return json.load(json_file)

        except FileNotFoundError as e:
            print(str(self.__FILE_ERROR) %(file_to_load))

        return None
