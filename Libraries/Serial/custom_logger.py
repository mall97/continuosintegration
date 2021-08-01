import logging

logging.basicConfig(format      = '[%(asctime)s] [%(levelname)s] [%(name)s::%(funcName)s] %(message)s',
                    level   	= logging.DEBUG,
                    handlers    = [logging.FileHandler("log.txt", mode='w'),
                                   logging.StreamHandler()])
