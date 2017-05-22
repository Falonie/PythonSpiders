import logging

def main():
    logger=logging.getLogger('simple_example')
    logger.setLevel(logging.DEBUG)

    ch=logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter=logging.Formatter('%(filename)s %(funcName)s %(asctime)s %(name)s %(levelname)s %(levelno)s %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')

if __name__=='__main__':
    main()