"""
Main module to run the application.
"""

from pdf_reader.pdf_parser import read_pdf_line_by_line, parse_subjects, calculate_average, calculate_average_ba, check_vertiefungsbereich
from export_excel.export_to_excel import export_to_excel
import os

def main() -> None:
    """
    Main function to read the PDF, parse the subjects, and calculate the average grades.
    """
    relative_filepath = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(relative_filepath, 'Noten_Uni.pdf')

    # Read the pdf File 
    text = read_pdf_line_by_line(pdf_path)

    # Create a Dictonary with all possible Areas and its neseccary LPs
    lp_dict = {
        "Informatik-Grundlagen": 46,
        "Ingenieurtechnische Grundlagen": 35,
        "Mathematische Grundlagen": 30,
        "Physikalische Grundlagen": 13,
        "1. Vertiefungsbereich Software and Systems Engineering": 16,
        "2. Vertiefungsbereich Ressourceneffizienz und Materialwissenschaften": 12,
        "3. Vertiefungsbereich Mechatronik und Robotik (12 LP)": 12,
        "4. Vertiefungsbereich Technische Informatik, Adaptive Systeme": 12,
        "Bachelorarbeit": 12
    }

    # All Valid Kürzel for the Subjects
    kuerzel = ['INF', 'MTH', 'PHM']

    # Creat Areas and Subject Objects from the input text
    areas = parse_subjects(text, lp_dict, kuerzel)

    try:
        # Calculate the Average Grade
        weighted_grade, total_lp = calculate_average(areas)
        print(f"Average: {(weighted_grade / total_lp):.5f}")
        
        # Calculate, what influence the Grade Thesis would have
        ba_note = 2.3
        avg_ba = calculate_average_ba(weighted_grade, total_lp, ba_note)
        print(f"Average mit {ba_note} in BA: {avg_ba:.5f}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Export All Data into an Excel File
    export_to_excel(areas, "Notenübersicht.xlsx")

if __name__ == "__main__":
    main()
