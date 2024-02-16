import PyPDF2
import copy
import gc
from tqdm import tqdm

# Dimensioni standard delle pagine in punti
PAGE_SIZES = {
	'Letter': (612, 792),
	'Legal': (612, 1008),
	'Ledger': (792, 1224),
	'Tabloid': (1224, 792),
	'A0': (2384, 3370),
	'A1': (1684, 2384),
	'A2': (1190, 1684),
	'A3': (842, 1190),
	'A4': (595, 842),
	'A5': (420, 595),
	'A6': (298, 420),
	'A7': (210, 298),
	'A8': (148, 210),
}

def new_page(width, height):
	writer = PyPDF2.PdfWriter()
	page = writer.add_blank_page(width, height)
	return page


def resize(page, width, height, size, bleed):
	target_width, target_height = PAGE_SIZES[size]
	new_width = target_width + 2 * bleed
	new_height = target_height + 2 * bleed
	ratio = min(target_width/width, target_height/height)
	new = new_page(new_width,new_height)
	new.merge_page(page)
	dx = abs(ratio*width-target_width)
	dy = abs(ratio*height-target_height)
	new.add_transformation((ratio, 0, 0, ratio, bleed+(dx/2), bleed+(dy/2)))
	return new, ratio

def add_mirror_bleed(page, width, height, size, bleed):
	target_width, target_height = PAGE_SIZES[size]
	new_width = target_width + 2 * bleed
	new_height = target_height + 2 * bleed

	new, ratio = resize(page, width, height, size, bleed)
	dx = abs(ratio*width-target_width)
	dy = abs(ratio*height-target_height)

	actual_width = ratio*width
	actual_height = ratio*height

	wbleed = bleed + dx/2
	hbleed = bleed + dy/2

	transformations = [
		(-ratio, 0, 0, ratio, wbleed, hbleed), # left
		(-ratio, 0, 0, -ratio, wbleed, hbleed), # bottom left 
		(ratio, 0, 0, -ratio, wbleed, hbleed), # bottom
		(-ratio, 0, 0, -ratio, 2 * actual_width + wbleed, hbleed), # bottom right
		(-ratio, 0, 0, ratio, 2 * actual_width + wbleed, hbleed), # right
		(ratio, 0, 0, -ratio, wbleed, 2 * actual_height + hbleed), # top
		(-ratio, 0, 0, -ratio, wbleed, 2 * actual_height + hbleed), # top left
		(-ratio, 0, 0, -ratio, 2 * actual_width + wbleed, 2 * actual_height + hbleed), # top right
	]

	bleed_template = new_page(new_width, new_height)
	bleed_template.merge_page(page)

	for transformation in transformations:
		new_bleed = copy.copy(bleed_template)
		new_bleed.add_transformation(transformation)
		new.merge_page(new_bleed)
	
	return new

def modify_pdf(input_pdf_path, output_pdf_path, size, bleed):
	with open(input_pdf_path, 'rb') as file:
		reader = PyPDF2.PdfReader(file)
		writer = PyPDF2.PdfWriter()
		
		page_count = 0
		for page in tqdm((reader.pages), desc="Processing Pages"):
			width = page.mediabox.width
			height = page.mediabox.height
			new = add_mirror_bleed(page, width, height, size, bleed)
			writer.add_page(new)
			
			if page_count % 10 == 0:
				gc.collect()

			page_count += 1
			# Ogni 50 pagine, scrivi l'output temporaneo
			if page_count % 50 == 0:
				temp_output_path = f"data/left_temp_output_{page_count}.pdf"
				with open(temp_output_path, 'wb') as temp_outfile:
					writer.write(temp_outfile)
				writer = PyPDF2.PdfWriter()

		with open(output_pdf_path, 'wb') as outfile:
			writer.write(outfile)

# Utilizzo dello script
input_pdf_path = 'data/dark_left.pdf'  # Inserire il percorso del PDF di input
output_pdf_path = 'data/dark_left_mod.pdf'  # Inserire il percorso per il PDF di output
modify_pdf(input_pdf_path, output_pdf_path, 'A5', 9)

