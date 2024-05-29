"""
Module for handling subjects.
"""

from typing import Union

class Subject:
    """
    A class to represent a subject.

    Attributes:
        area (str): The area of study the subject belongs to.
        short (str): Short code for the subject.
        name (str): Full name of the subject.
        lp (int): Credit points (Leistungspunkte) for the subject.
        lp_evaluate (int): Credit points to be evaluated.
        grade (Union[float, None]): Grade for the subject, None if not graded.
    """
    def __init__(self, area: str, short: str, name: str, lp: int, lp_evaluate: int, grade: Union[float, None]):
        """
        Initialize a subject with its attributes.

        :param area: The area of study the subject belongs to.
        :param short: Short code for the subject.
        :param name: Full name of the subject.
        :param lp: Credit points (Leistungspunkte) for the subject.
        :param lp_evaluate: Credit points to be evaluated.
        :param grade: Grade for the subject, None if not graded.
        """
        self.area = area
        self.short = short
        self.name = name
        self.lp = lp
        self.lp_evaluate = lp_evaluate
        self.grade = grade

    def __str__(self) -> str:
        """
        Return a string representation of the subject.

        :return: A string describing the subject.
        """
        return f"{self.short} {self.name}, LP: {self.lp_evaluate}/{self.lp}, Grade: {self.grade}"
