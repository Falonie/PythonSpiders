import logging

logging.basicConfig(filename='example2.log',format='%(asctime)s %(levelname)s %(levelno)s %(message)s',level=logging.DEBUG)
logging.warning('is when the event is logged.')