import serial
import simplejson
import logging
import argparse
import MatrixDriver
import threading
import TESmartMatrix
from web import flaskTread
import driver

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-v", "--verbose", action="count",
                    help="increase output verbosity")
  parser.add_argument("-t", "--virtual", action="store_true",
                    help="use test or virtual matrix")
  args = parser.parse_args()
  loglevel = logging.ERROR
  if( args.verbose == 1 ): 
    loglevel = logging.WARNING
  elif( args.verbose == 2 ): 
    loglevel = logging.INFO
  elif( args.verbose == 3 ): 
    loglevel = logging.DEBUG
    
  logging.basicConfig(level=loglevel,
                    format='(%(threadName)-13s)[%(levelname)-8s] %(message)s',
                    )
  if( args.virtual ):
    serial_port=""
    driver.driver = MatrixDriver.MatrixDriver(serial_port)
  else:
    serial_port = serial.Serial('/dev/ttyUSB0')  # open serial port
    logging.debug(serial_port.name)
    driver.driver = TESmartMatrix.TESmartMatrix(serial_port) 
  driver.driver.start()
  logging.debug("This is a debug.")
  logging.info("This is a info.")
  logging.warning("This is a warning.")
  logging.error("This is an error.")
  logging.critical("This is a critical.")

  t1 = threading.Thread(target=flaskTread,name="webThread")    
  t1.start()
  t1.join()
  driver.driver.join()

  serial_port.close()

