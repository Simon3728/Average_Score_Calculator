"""
Module for parsing PDF files and exctracting the Data
"""

import pdfplumber
from typing import List, Dict
from .subject import Subject
from .area import Area

def read_pdf_line_by_line(pdf_path: str) -> str:
    """
    Read the content of a PDF file line by line.
    
    :param pdf_path: Path to the PDF file.
    :return: Full text extracted from the PDF.
    """
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return full_text

def parse_subjects(text: str, lp_dict: Dict[str, int], kuerzel: List[str]) -> Dict[str, Area]:
    """
    Parse the subjects from the text extracted from the PDF.
    
    :param text: Extracted text from the PDF.
    :param lp_dict: Dictionary of area names and their required credit points.
    :param kuerzel: List of subject codes.
    :return: Dictionary of areas with their subjects.
    """
    lines = text.strip().split('\n')
    areas: Dict[str, Area] = {}
    current_area = None

    for line in lines:
        if line in lp_dict:
            current_area = Area(line.strip(), lp_dict[line.strip()])
            areas[line.strip()] = current_area
        elif is_subject(line, kuerzel):
            if current_area:
                subject = parse_subject(line, current_area.name)
                current_area.add_subject(subject)
            
    return areas

def is_subject(line: str, kuerzel: List[str]) -> bool:
    """
    Determine if a line represents a subject based on known subject codes.
    
    :param line: Line of text to be checked.
    :param kuerzel: List of known subject codes.
    :return: True if the line represents a subject, otherwise False.
    """
    return any(line.startswith(code) for code in kuerzel)

def parse_subject(line: str, area_name: str) -> Subject:
    """
    Parse a subject's details from a line of text.
    
    :param line: Line of text containing the subject details.
    :param area_name: The area to which the subject belongs.
    :return: Parsed Subject object.
    """
    parts = line.split()
    lp = int(parts[-2])
    lp_evaluate = lp
    try:
        grade = float(parts[-1].replace(",", ".")) if parts[-1] != "--" else None
    except ValueError:
        print(f"Grade can not convert to float number")
        raise

    short = parts[0]
    name = " ".join(parts[1:-2])
    return Subject(area_name, short, name, lp, lp_evaluate, grade)

def calculate_average(areas: Dict[str, Area]) -> float:
    """
    Calculate the weighted average grade across all areas.
    
    :param areas: Dictionary of areas with their subjects.
    :return: Weighted average grade.
    """
    total_lp = 0
    weighted_grade = 0.0

    for area in areas.values():
        area.modify_lp()
        for subject in area.subjects:
            if subject.grade is not None:
                total_lp += subject.lp_evaluate
                weighted_grade += subject.lp_evaluate * subject.grade
        
    if total_lp == 0:
        raise ValueError("Total credit points is zero, cannot calculate average.")
    weighted_grade / total_lp
    return weighted_grade, total_lp

def calculate_average_ba(weighted_grade: float, total_lp: int, ba_note: float) -> float:
    """
    Calculate the new average including the Bachelor's thesis grade.
    
    :param weighted_grade: Current weighted grade sum.
    :param total_lp: Current total credit points.
    :param ba_note: Grade for the Bachelor's thesis.
    :return: New weighted average grade.
    """
    try:
        total_lp += 12
        weighted_grade += 12 * ba_note
    except ValueError as e:
        print(f"Error calculating average with BA grade: {e}")
        raise

    return weighted_grade / total_lp

def check_vertiefungsbereich(areas: Dict[str, Area]) -> None:
    """
    Check and handle the Vertiefungsbereiche, allowing the user to exclude one if there are three present.
    
    :param areas: Dictionary of areas with their subjects.
    """
    # Filter out "Vertiefungsbereich" areas
    area_names = list(areas.keys())
    vertiefungsbereiche = [a for a in area_names if '2.' in a or '3.' in a or '4.' in a]

    if len(vertiefungsbereiche) == 3:
        print("You can choose one of these Areas to not count into your Average Calculation, since you only need 2 of the 3 Vertiefungsbereiche")
        print()
        for i, area_name in enumerate(vertiefungsbereiche):
            total_lp = areas[area_name].calculate_total_lp()
            total_weighted_sum = sum(subject.lp * subject.grade for subject in areas[area_name].subjects if subject.grade is not None)
            print(f"Enter {i+2}: {area_name}: Total_LP: {total_lp} (of {areas[area_name].lp} LP), Average_Grade of Area: {(total_weighted_sum/total_lp):.2f}")
        print("Or E for Exit")

        try:
            inp = input("Which area would you like not to count: ")
            if inp == 'E':
                print("No Vertiefungsbereich deleted")
                return
            else:
                try:
                    idx = int(inp) - 2
                    if 0 <= idx < len(vertiefungsbereiche):
                        selected_area = vertiefungsbereiche[idx]
                        areas[selected_area].set_all_subjects_lp_to_zero()
                        print(f"Set all subjects' LP to zero for area: {selected_area}")
                        return
                except ValueError:
                    pass

            print("Invalid input. No Vertiefungsbereich deleted")
        except (EOFError, KeyboardInterrupt):
            print("\nInput interrupted. No Vertiefungsbereich deleted")

    return