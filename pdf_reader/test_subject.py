import pytest
from subject import Subject

def test_subject_initialization():
    subject = Subject("Mathematics", "MATH101", "Calculus I", 6, 6, 1.7)
    assert subject.area == "Mathematics"
    assert subject.short == "MATH101"
    assert subject.name == "Calculus I"
    assert subject.lp == 6
    assert subject.lp_evaluate == 6
    assert subject.grade == 1.7

def test_subject_initialization_without_grade():
    subject = Subject("Physics", "PHYS101", "Mechanics", 6, 6, None)
    assert subject.area == "Physics"
    assert subject.short == "PHYS101"
    assert subject.name == "Mechanics"
    assert subject.lp == 6
    assert subject.lp_evaluate == 6
    assert subject.grade is None

def test_subject_str():
    subject = Subject("Mathematics", "MATH101", "Calculus I", 6, 6, 1.7)
    assert str(subject) == "MATH101 Calculus I, LP: 6/6, Grade: 1.7"

def test_subject_str_without_grade():
    subject = Subject("Physics", "PHYS101", "Mechanics", 6, 6, None)
    assert str(subject) == "PHYS101 Mechanics, LP: 6/6, Grade: None"

if __name__ == "__main__":
    pytest.main()
