import serial

class TesterlyzerIBox4():
    # documentation see: http://wiki-id.conti.de/display/CIPS/sw.tool.robot-gen-library.git#sw.tool.robot-gen-library.git-PowerSupply
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    ####################################################################################################################
    def __init__(self, port):
        self.device = "PowerSupply"
        self.deviceName = "Testerlyzer"
        #self.DebugLevel = 2     # 0->no debug output | 1->short debug output | 2->full debug output
        self.connection = serial.Serial()
        self.connection.baudrate = 115200
        self.connection.port = str(port)
        self.connection.bytesize = 8
        self.connection.parity = str("N")
        self.connection.stopbits = int(1)
        self.connection.xonxoff = False
        self.connection.timeout = 0.5

    ####################################################################################################################
    def powersupply_begin(self):
        if (self.connection.isOpen() == False):
            self.connection.open()

        return(self.powersupply_get_current())

    ####################################################################################################################
    def powersupply_end(self):
        self.powersupply_set_voltage(0)
        if (self.connection.isOpen() == True):
            self.connection.close()

    ####################################################################################################################
    def powersupply_set_voltage(self, voltage):
        if (self.connection.isOpen() == False):
            self.connection.open()

        log_file = open("serialoutput.txt", "a")
        log_file.truncate(0)
        log_file.write(
        str(self.connection.readlines()))
        text = ("\n" + "HFBSR" + "\n")
        self.connection.write(text.encode('ascii'))
        log_file.write(str(self.connection.readlines()))

        if float(voltage) == float(0):
            text = ("\n" + "HFBC0" + "\n")
            self.connection.write(text.encode('ascii'))
            log_file.write(str(self.connection.readlines()))
            text = ("\n" + "HFBCf" + "\n")
            self.connection.write(text.encode('ascii'))
            log_file.write(str(self.connection.readlines()))
            text = ("\n" + "HFBCb" + "\n")
            self.connection.write(text.encode('ascii'))
            log_file.write(str(self.connection.readlines()))
        else:
            text = ("\n" + "HFBS0" + "\n")
            self.connection.write(text.encode('ascii'))
            log_file.write(str(self.connection.readlines()))
            text = ("\n" + "HFBSf" + "\n")
            self.connection.write(text.encode('ascii'))
            log_file.write(str(self.connection.readlines()))
            text = ("\n" + "HFBSb" + "\n")
            self.connection.write(text.encode('ascii'))
            log_file.write(str(self.connection.readlines()))

        log_file.close()
        self.connection.close()

    ####################################################################################################################
    def powersupply_set_current(self, current):
        pass

    ####################################################################################################################
    def powersupply_get_current(self):
        if (self.connection.isOpen() == False):
            self.connection.open()

        log_file = open("serialoutput.txt", "a")
        log_file.truncate(0)  # delete content of file
        text = str(self.connection.readlines())
        print(text)
        log_file.write(text)  # waiting for timeout of readlines function (boot process finished)
        text = ("\n" + "HFBSR" + "\n")
        self.connection.write(text.encode('ascii'))
        text = str(self.connection.readlines())
        log_file.write(text)
        text = ("\n" + "HMGC" + "\n")
        self.connection.write(text.encode('ascii'))
        text = str(self.connection.readlines())
        log_file.write(text)
        log_file.close()
        log_file = open("serialoutput.txt", "r")
        logtext = log_file.read()
        current = logtext.split("MCmA:")[1].split("\\n")[0]
        log_file.close()
        self.connection.close()

        current = float(current) / 1000.00
        return current