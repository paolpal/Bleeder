import fitz  # PyMuPDF
from PyPDF2 import PdfWriter, PdfReader, Transformation

def add_mirror_bleed(input_path, output_path, bleed_width):
    pdf_document = fitz.open(input_path)
    out = fitz.Document()
    a = fitz.Matrix(-1,0,0,1,0,0)
    lr = fitz.Matrix(1,0,0,-1,0,0)
    
    for page_num in range(pdf_document.page_count):
        print(page_num,'/',pdf_document.page_count)
        page = pdf_document[page_num]

        # Estensione esterna (bleed esterno)
        page_media_box = page.rect
        #page.rect = page.rect*a
        old_width = page_media_box.width 
        old_height = page_media_box.height
        new_width = page_media_box.width + 2 * bleed_width
        new_height = page_media_box.height + 2 * bleed_width
        
		# Applicare una trasformazione di specchio orizzontale
        #mirrored_page.transform([(-1, 0, 0, 1, page_width, 0)])

        # Creazione di una nuova pagina con il bleed esterno
        new_page = out.new_page(width=new_width, height=new_height)

        # Posizionamento del contenuto originale sulla nuova pagina con il bleed esterno
        new_page.show_pdf_page(fitz.Rect(bleed_width, bleed_width, new_width-bleed_width, new_height-bleed_width), pdf_document, page_num)

        # Riflessione del bleed esterno sul lato sinistro
        new_page.show_pdf_page(fitz.Rect(0, bleed_width, bleed_width, new_height-bleed_width), pdf_document, page_num, keep_proportion=False, clip=fitz.Rect(0, 0, bleed_width, new_height))

        # Riflessione del bleed esterno sul lato destro
        new_page.show_pdf_page(fitz.Rect(new_width - bleed_width, bleed_width, new_width, new_height-bleed_width), pdf_document, page_num, keep_proportion=False, clip=fitz.Rect(old_width - bleed_width, 0, new_width, new_height))
        
		# Riflessione del bleed esterno in alto
        #new_page.show_pdf_page(fitz.Rect(bleed_width, 0, bleed_width, new_height-bleed_width), pdf_document, page_num, keep_proportion=False, clip=fitz.Rect(0, 0, bleed_width, new_height))

        # Salvataggio della nuova pagina con il bleed
        #out.insert_page(page_num, new_page)
        if page_num >= 20:
            break

    # Salvataggio del documento PDF risultante
    out.save(output_path)
    pdf_document.close()
    out.close()

if __name__ == "__main__":
    input_path = "dark.pdf"
    output_path = "dark_out.pdf"
    bleed_width = 9  # Larghezza del bleed desiderata in punti

    add_mirror_bleed(input_path, output_path, bleed_width)
