import fitz  # PyMuPDF
import os
import subprocess

import fitz  # PyMuPDF
from ebooklib import epub

def pdf_to_epub(pdf_path, epub_path):
    # Open the PDF file
    document = fitz.open(pdf_path)
    epub_book = epub.EpubBook()

    # Add metadata (modify as needed)
    epub_book.set_identifier('id123456')
    epub_book.set_title('Sample Book')
    epub_book.set_language('en')

    # Loop through each page of the PDF
    for page_num in range(document.page_count):
        page = document[page_num]
        text = page.get_text("text")
        
        # Create a new chapter for each page
        chapter = epub.EpubHtml(title=f'Page {page_num+1}', file_name=f'chap_{page_num+1}.xhtml', lang='en')
        chapter.content = f'<h1>Page {page_num+1}</h1><p>{text}</p>'
        
        # Add chapter to the book
        epub_book.add_item(chapter)

    # Define the Table Of Contents and the book order
    epub_book.toc = tuple(epub_book.items)
    epub_book.add_item(epub.EpubNcx())
    epub_book.add_item(epub.EpubNav())

    # Write the EPUB file
    epub.write_epub(epub_path, epub_book, {})


def convert_all_pdfs_in_folder(pdf_folder, epub_folder):
    if not os.path.exists(epub_folder):
        os.makedirs(epub_folder)

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            epub_folder = os.path.join(epub_folder, f'{os.path.splitext(pdf_file)[0]}.epub')
            pdf_to_epub(pdf_path, epub_folder)
            
## Example usage
pdf_folder = os.path.join(os.getcwd(),'pdfs')
epub_folder = os.path.join(os.getcwd(),'epub')

convert_all_pdfs_in_folder(pdf_folder, epub_folder)