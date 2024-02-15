import PyPDF2
import copy
import gc
from tqdm import tqdm

LETTER_SIZE = (612, 792)

def new_page(width, height):
    writer = PyPDF2.PdfWriter()
    page = writer.add_blank_page(width, height)
    return page

def add_bleed(page, width, height, bleed):
    new_width = width + 2 * bleed
    new_height = height + 2 * bleed
    new = new_page(new_width, new_height)
    new.merge_page(page)
    new.add_transformation((1, 0, 0, 1, bleed, bleed))
    return new

def add_mirror_bleed(page, width, height, bleed):
    new_width = width + 2 * bleed
    new_height = height + 2 * bleed
    new = add_bleed(page, width, height, bleed)
    
    transformations = [
        (-1, 0, 0, 1, bleed, bleed), # left
        (-1, 0, 0, -1, bleed, bleed), # bottom left 
        (1, 0, 0, -1, bleed, bleed), # bottom
        (-1, 0, 0, -1, 2 * width + bleed, bleed), # bottom right
        (-1, 0, 0, 1, 2 * width + bleed, bleed), # right
        (1, 0, 0, -1, bleed, 2 * height + bleed), # top
        (-1, 0, 0, -1, bleed, 2 * height + bleed), # top left
        (-1, 0, 0, -1, 2 * width + bleed, 2 * height + bleed), # top right
    ]

    bleed_template = new_page(new_width, new_height)
    bleed_template.merge_page(page)

    for transformation in transformations:
        new_bleed = copy.copy(bleed_template)
        new_bleed.add_transformation(transformation)
        new.merge_page(new_bleed)
    
    return new

def aggiungi_mirror_bleed(input_pdf, output_pdf, bleed):
    # Apri il file PDF originale
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        
        for pagenum in tqdm(range(len(reader.pages)), desc="Processing Pages"):
            page = reader.pages[pagenum]
            width = abs(page.cropbox.width)
            height = abs(page.cropbox.height)
            new_page = add_mirror_bleed(page, width, height, bleed)
            writer.add_page(new_page)
            gc.collect()

        # Scrivi il nuovo PDF
        with open(output_pdf, 'wb') as outfile:
            writer.write(outfile)

# Uso della funzione
aggiungi_mirror_bleed('data/red_ita.pdf', 'data/red_ita_mod.pdf', 9)