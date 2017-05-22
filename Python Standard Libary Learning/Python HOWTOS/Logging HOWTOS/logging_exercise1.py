import logging

#logging.warning('Watch out!')
def main():
    logging.basicConfig(filename='example.log',level=logging.INFO)
    logging.debug('message1')
    logging.info('message2')
    logging.warning('{} is running...'.format('warning'))
    logging.error('message4')
    logging.critical('message5')

if __name__=='__main__':
    main()