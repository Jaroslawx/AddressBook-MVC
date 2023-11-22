from utils.Log import logger
from Models.Trivia import trivia


def main():
    logger.log_info("Application started.")
    print(trivia.get_random_trivia())
    logger.log_info("Application ended.")


if __name__ == '__main__':
    main()
