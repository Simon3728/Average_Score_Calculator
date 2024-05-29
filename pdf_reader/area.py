"""
Module for calculating areas.
"""

from typing import List
from .subject import Subject

class Area:
    """
    A class to represent an area of study.

    Attributes:
        name (str): The name of the area.
        lp (int): Total credit points (Leistungspunkte) required for the area.
        subjects (List[Subject]): A list of subjects in the area.
    """
    def __init__(self, name: str, lp: int):
        """
        Initialize an area of study with its attributes.

        :param name: Name of the area.
        :param lp: Total credit points (Leistungspunkte) required for the area.
        """
        self.name = name
        self.lp = lp
        self.subjects: List[Subject] = []

    def __str__(self) -> str:
        """
        Return a string representation of the area.

        :return: A string describing the area.
        """
        return f"{self.name}, {self.lp} LP"

    def add_subject(self, subject: Subject) -> None:
        """
        Add a subject to the area.

        :param subject: Subject to be added.
        """
        self.subjects.append(subject)

    def modify_lp(self) -> None:
        """
        Adjust the credit points to match the area's required points.
        """
        area_lp = self.lp
        total_lp = self.calculate_total_lp()
        if area_lp < total_lp:
            sorted_subjects = sorted(self.subjects, key=lambda sub: sub.grade if sub.grade is not None else float('inf'), reverse=True)
            for s in sorted_subjects:
                if s.lp < (total_lp - area_lp):
                    total_lp -= s.lp
                    s.lp_evaluate = 0
                else:
                    s.lp_evaluate -= (total_lp - area_lp)
                    break

    def missing_lp(self) -> int:
        """
        Calculate missing credit points to reach the area's required points.

        :return: Missing credit points.
        """
        return max(0, self.lp - self.calculate_total_lp())

    def calculate_total_lp(self) -> int:
        """
        Calculate the total LP for this area.

        :return: Total LP for the area.
        """
        return sum(subject.lp_evaluate for subject in self.subjects if subject.grade is not None)

    def calculate_total_weighted_sum(self) -> float:
        """
        Calculate the total weighted sum for this area.

        :return: Total weighted sum for the area.
        """
        return sum((subject.lp_evaluate * subject.grade) for subject in self.subjects if subject.grade is not None)

    def set_all_subjects_lp_to_zero(self) -> None:
        """
        Set the LP of all subjects in this area to 0.
        """
        for subject in self.subjects:
            subject.lp_evaluate = 0
