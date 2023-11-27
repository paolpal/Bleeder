import fitz  # PyMuPDF
from PyPDF2 import PdfWriter, PdfReader, Transformation
from PyPDF2.generic import RectangleObject
from PyPDF2._page import PageObject
import copy

def create_blank_page(width, height):
    # Crea un oggetto PdfFileWriter
    pdf_writer = PdfWriter()

    # Aggiungi una pagina vuota al writer con le dimensioni specificate
    page = pdf_writer.add_blank_page(width, height)

    return page

def add_bleed_margin(input_path, output_path, bleed_width):
    # Apri il file PDF con PyMuPDF per ottenere le informazioni sulla dimensione del documento
    pdf_document = fitz.open(input_path)
    page = pdf_document[0]  # Assumiamo che il bleed sia applicato solo alla prima pagina

    # Ottieni le dimensioni originali della pagina
    original_width = page.rect.width
    original_height = page.rect.height

    # Calcola le nuove dimensioni della pagina con il bleed
    new_width = original_width + 2*bleed_width
    new_height = original_height + 2*bleed_width

    # Creare un nuovo oggetto PDFWriter
    pdf_writer = PdfWriter()

    # Apri il file PDF con PyPDF2
    pdf_reader = PdfReader(input_path)


        # Per ogni pagina nel documento 
    for page_num in range(len(pdf_reader.pages)):
            # Estrai la pagina
        print(page_num,'/',len(pdf_reader.pages))
        pdf_page = pdf_reader.pages[page_num]
        translate = Transformation().translate(bleed_width,bleed_width)

        # creo la pagina
        new_pdf_page = create_blank_page(new_width, new_height)
        # posiziono il contenuto principale
        new_pdf_page.merge_page(pdf_page)
        new_pdf_page.add_transformation(translate)

        # mirror destra - sinistra
        mirror = Transformation((-1,0,0,1,pdf_page.mediabox[2],0))
        lr = copy.deepcopy(pdf_page)
        lr.add_transformation(mirror)
        translate_r = Transformation().translate(original_width+bleed_width,bleed_width)
        translate_l = Transformation().translate(-(original_width-bleed_width),bleed_width)
        new_pdf_page.mergeTransformedPage(lr,translate_r)
        new_pdf_page.mergeTransformedPage(lr,translate_l)

        # mirror sopra - sotto
        mirror = Transformation((1,0,0,-1,0,pdf_page.mediabox[3]))
        td = copy.deepcopy(pdf_page)
        td.add_transformation(mirror)
        translate_t = Transformation().translate(bleed_width,original_height+bleed_width)
        translate_d = Transformation().translate(bleed_width,-original_height+bleed_width)
        new_pdf_page.mergeTransformedPage(td,translate_t)
        new_pdf_page.mergeTransformedPage(td,translate_d)

        pdf_writer.add_page(new_pdf_page)
        if page_num >= 20:
            break

        

    # Salva il nuovo documento con il margine di bleed aggiunto
    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

if __name__ == "__main__":
    input_path = "dark.pdf"
    output_path = "dark_out.pdf"
    bleed_width = 9  # Sostituisci con la larghezza del bleed desiderata in punti

    add_bleed_margin(input_path, output_path, bleed_width)
