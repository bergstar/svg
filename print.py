import sys
import cups
from PyPDF2 import PdfFileReader

def print_pdf(file_path):
    # Connect to CUPS
    conn = cups.Connection()

    # Find the Zebra printer
    printers = conn.getPrinters()
    zebra_printer = None
    for printer in printers:
        if "Zebra_GK420D" in printer:
            zebra_printer = printer
            break

    if not zebra_printer:
        print("Zebra GK420D printer not found. Please check the configuration.")
        sys.exit(1)

    # Check if the input file is a PDF
    try:
        with open(file_path, 'rb') as f:
            pdf = PdfFileReader(f)
            if not pdf.isEncrypted:
                pdf.getNumPages()
            else:
                print("Encrypted PDFs are not supported.")
                sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Configure printer settings
    options = {
        "media": "Custom.102x192mm",  # Set the paper size to 102 x 192 mm
        "printer-resolution": "203dpi",  # Set the print resolution
        "ZebraDarkness": "20",  # Set the darkness to 20
        "ZebraSpeed": "slow",  # Set the speed to slow
    }

    # Print the PDF on the Zebra printer
    conn.printFile(zebra_printer, file_path, "PDF Printing", options)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python print_pdf_on_zebra.py <pdf_file_path>")
        sys.exit(1)

    pdf_file_path = sys.argv[1]
    print_pdf(pdf_file_path)

