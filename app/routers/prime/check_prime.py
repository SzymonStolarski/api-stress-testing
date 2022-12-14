from abc import ABC, abstractmethod

from fastapi import APIRouter, HTTPException
import sympy


MAX_RANGE = 9223372036854775807

router = APIRouter()


class Checker(ABC):

    def __init__(self) -> None:
        """Empty constructor"""
        pass

    @abstractmethod
    def check(self, number_to_check: int) -> bool:
        pass

    def _validation(self, number_to_validate: int):
        if (number_to_validate > MAX_RANGE
                or number_to_validate < 0):

            raise ValueError(f"Range of input number should be positive and in"
                             f" max range of: {MAX_RANGE}")


class DefaultChecker(Checker):

    def __init__(self) -> None:
        super().__init__()

    def check(self, number_to_check: int) -> bool:
        self._validation(number_to_validate=number_to_check)

        return self.__prime_checker(number_to_check)

    def __prime_checker(self, number_to_check: int) -> bool:
        """
        Assumes that n is a positive natural number
        """
        # We know 1 is not a prime number
        if number_to_check == 1:
            return False

        i = 2
        # This will loop from 2 to int(sqrt(x))
        while i*i <= number_to_check:
            # Check if i divides x without leaving a remainder
            if number_to_check % i == 0:
                # This means that n has a factor in between 2 and sqrt(n)
                # So it is not a prime number
                return False
            i += 1
        # If we did not find any factor in the above loop,
        # then n is a prime number
        return True


class SympyChecker(Checker):

    def __init__(self) -> None:
        super().__init__()

    def check(self, number_to_check: int) -> bool:
        self._validation(number_to_validate=number_to_check)

        return sympy.isprime(number_to_check)


prime_checker = SympyChecker()


@router.get("/prime/{number}")
def check_prime(number: int):

    try:
        return {'result': prime_checker.check(number)}
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Wrong number passed!"
        )
