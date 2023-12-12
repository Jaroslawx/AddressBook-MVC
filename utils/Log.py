import logging
import os


class AppLogger:
    def __init__(self, log_file, log_to_file=True):
        self.logger = logging.getLogger(__name__)
        self.log_to_file = log_to_file

        # Prevent adding handlers multiple times
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            if self.log_to_file:
                # Handler for file
                log_folder = "files"
                os.makedirs(log_folder, exist_ok=True)
                log_path = os.path.join(log_folder, log_file)
                file_handler = logging.FileHandler(log_path)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_critical(self, message):
        self.logger.critical(message)


logger = AppLogger("app.log", log_to_file=False)
