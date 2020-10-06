from PyPDF2 import PdfFileReader


def pdf2text(file_path, file_exten) -> str:
    """ Converts a given file to text content """

    _content = None

    # Identify file type and get its contents
    if file_exten == 'pdf':
        with open(file_path, 'rb') as pdf_file:
            _pdf_reader = PdfFileReader(pdf_file)
            _content = _pdf_reader
            print('PDF operation done!')

    elif file_exten == 'txt':
        with open(file_path, 'r') as txt_file:
            _content = txt_file.read()
            print('TXT operation done!')

    return _content
