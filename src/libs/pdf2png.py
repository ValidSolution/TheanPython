# coding:utf-8

# dependencies:
# pip install pdf2image
# brew install poppler
from pdf2image import convert_from_path
import os


def disassemble_pdf_to_png(pdf_path, output_path):
    images = convert_from_path(pdf_path)
    file_path, file_name = os.path.split(pdf_path)
    fn, ext = os.path.splitext(file_name)
    for index, img in enumerate(images):
        img.save(os.path.join(output_path, "%s_%s.png" % (fn, index)))
        img.close()


# run this script in a system Terminal or pyCharm!!! iterm and terminal in pyCharm won't work!!!
if __name__ == "__main__":
    inputs = "/Users/thean/Desktop/test.pdf"
    output = "/Users/thean/Desktop/tmp"
    disassemble_pdf_to_png(inputs, output)
