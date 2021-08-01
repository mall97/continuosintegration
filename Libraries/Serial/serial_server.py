#!/usr/bin/env python3
####################################################################################################################
###-                            {DLT Viewer Remote Server}                                                      ##-#
###-Connect Robot framework with remote DLT Viewer                                                              ##-#
###-Author: Rafael Santos Costa                                                                                 ##-#
###-Comment by:                                                                                                 ##-#
####################################################################################################################

####################################################################################################################
# -----------------------------------------------------------------------------
# imports
# -----------------------------------------------------------------------------
####################################################################################################################
from robotremoteserver import RobotRemoteServer
from serial_api    import serial_api as Serial
####################################################################################################################
# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
####################################################################################################################
def main(params):
    try:
        # -----------------------------------------------------------------------------
        # Start server
        # -----------------------------------------------------------------------------
        api = Serial(params)
        RobotRemoteServer(api, host=str(params['ip']), port=int(params['port']))
    except Exception as e:
        print(str(e))
####################################################################################################################
# -----------------------------------------------------------------------------
# run
# -----------------------------------------------------------------------------
####################################################################################################################
from argparse import ArgumentParser
#
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--ip',           type=str,   default = "127.0.0.1",    help='DLT Viewer Server Host')
    parser.add_argument('--port',         type=int,   default = 20014,  help='DLT Viewer Server Port')
    # It is missing the logger
    args = parser.parse_args()
    # main 
    main(vars(args))
####################################################################################################################
# -----------------------------------------------------------------------------
# end
# -----------------------------------------------------------------------------
####################################################################################################################