from utils.Log import AppLogger, logger


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    logger.log_info("Application started.")
    print_hi('PyCharm')

