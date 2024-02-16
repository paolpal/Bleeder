from PyPDF2 import PdfWriter

merger = PdfWriter()

for pdf in ["data/dark0-280.pdf", "data/dark280-end.pdf"]:
    merger.append(pdf)

merger.write("data/dark_fine.pdf")
merger.close()