import logging


class AppLogger:
    def __init__(self, log_file):
        logging.basicConfig(filename=log_file, level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    @staticmethod
    def log_info(message):
        logging.info(message)

    @staticmethod
    def log_warning(message):
        logging.warning(message)

    @staticmethod
    def log_error(message):
        logging.error(message)

    @staticmethod
    def log_critical(message):
        logging.critical(message)


logger = AppLogger('app.log')
