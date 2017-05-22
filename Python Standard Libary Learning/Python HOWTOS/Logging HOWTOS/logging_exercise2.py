import logging

logging.basicConfig(filename='example2.log',format='%(asctime)s %(message)s',level=logging.DEBUG)
logging.warning('is when the event is logged.')