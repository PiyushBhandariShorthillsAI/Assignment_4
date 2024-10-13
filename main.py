from loaders.pdf_loader import PDFLoader
from loaders.ppt_loader import PPTLoader
from loaders.docs_loader import DOCXLoader
from extractor.data_extractor import DataExtractor
from storage.file_storage import FileStorage
from storage.sql_storage import SQLStorage

if __name__ == "__main__":
    # Example usage with a PDF file
    file_loader = PDFLoader('/home/shtlp_0125/Desktop/Piyush_Assignment_4/sample_requirements_with_table_image.pdf')
    # file_loader = DOCXLoader('/home/shtlp_0125/Desktop/Piyush_Assignment_4/file-sample_100kB.docx')
    # file_loader = PPTLoader('/home/shtlp_0125/Desktop/Piyush_Assignment_4/DALL·E 2024-10-13 13.09.57 - A simple PowerPoint presentation (PPTX) slide containing text, an embedded image, a hyperlink, and a data table. The slide has a title at the top, a s.pptx')
    extractor = DataExtractor(file_loader)

    # File storage
    file_storage = FileStorage(extractor)
    file_storage.store()

    # SQL storage
    sql_storage = SQLStorage(extractor)
    sql_storage.store()
