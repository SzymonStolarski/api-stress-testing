from abc import ABC, abstractmethod


class BaseChecker:
    MAX_RANGE = 9223372036854775807

    def __init__(self):
        pass

    @abstractmethod
    def check(self, number_to_check: int) -> bool:
        pass

    def _validation(self, number_to_validate: int):
        if (number_to_validate > BaseChecker.MAX_RANGE
                or number_to_validate < 0):

            raise ValueError(f"Range of input number should be positive and in"
                             f" max range of: {BaseChecker.MAX_RANGE}")
