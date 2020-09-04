import logging

class logger(object):
    @staticmethod 
    def __console(level, message):
        LOG_LEVEL = logging.INFO
        LOGFORMAT = logging.Formatter("%(asctime)s  --  %(message)s")
        stream = logging.StreamHandler()
        stream.setFormatter(LOGFORMAT)
        logfile = logging.FileHandler('./log.txt')
        logfile.setLevel(LOG_LEVEL)
        logfile.setFormatter(LOGFORMAT)
        log = logging.getLogger('mariolog')
        log.setLevel(LOG_LEVEL)
        log.addHandler(stream)
        log.addHandler(logfile)
        if level == "error":
            log.error(message)
        elif level == 'info':
            log.info(message)
        elif level == 'warning':
            log.warning(message)
        log.removeHandler(stream)
        log.removeHandler(logfile)
    @staticmethod 
    def error (message):
        logger.__console('error',message)
    @staticmethod 
    def info (message):
        logger.__console('info',message)
    @staticmethod
    def warning (message):
        logger.__console('warning',message)
