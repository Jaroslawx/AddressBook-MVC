from utils.Log import logger
import random
import os


class Trivia:
    def __init__(self, trivia_file="assets/files/trivia.txt"):
        self.trivia_file = trivia_file
        self.list_of_trivia = self.load_trivia()

    def load_trivia(self):
        try:
            if os.path.exists(self.trivia_file):
                with open(self.trivia_file, "r", encoding="utf-8") as file:
                    trivia_list = [line.strip() for line in file.readlines()]

                logger.log_info(f"Loaded {len(trivia_list)} trivia.")
                return trivia_list
            else:
                raise FileNotFoundError(f"File not found: {self.trivia_file}")
        except Exception as e:
            logger.log_error(f"Error loading trivia: {e}")
            return ["Error! Can't find any trivia."]

    def get_random_trivia(self):
        return random.choice(self.list_of_trivia)


trivia = Trivia()

