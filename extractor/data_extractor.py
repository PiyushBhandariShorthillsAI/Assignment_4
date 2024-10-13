import camelot

class DataExtractor:
    def __init__(self, file_loader):
        self.document = file_loader.load_file()
        self.file_path = file_loader.file_path  # Store the file path

    def extract_text(self):
        """Extract text from different document types."""
        if hasattr(self.document, 'load_page'):  # PDF handling
            text = ''
            for page_num in range(self.document.page_count):
                page = self.document.load_page(page_num)
                text += page.get_text("text")
            return text
        elif hasattr(self.document, 'paragraphs'):  # DOCX handling
            return "\n".join([para.text for para in self.document.paragraphs])
        elif hasattr(self.document, 'slides'):  # PPTX handling
            text = ''
            for slide in self.document.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + '\n'
            return text
        else:
            raise TypeError("Unsupported file format")

    def extract_links(self):
        """Extract hyperlinks."""
        if hasattr(self.document, 'load_page'):  # PDF handling
            links = []
            for page_num in range(self.document.page_count):
                page = self.document.load_page(page_num)
                links += [link['uri'] for link in page.get_links() if 'uri' in link]
            return links
        
        elif hasattr(self.document, 'element'):  # DOCX handling
            links = []
            for rel in self.document.part.rels.values():
                if "hyperlink" in rel.reltype:
                    links.append(rel.target_ref)
            return links
        
        elif hasattr(self.document, 'slides'):  # PPTX handling
            links = []
            for slide in self.document.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text_frame") and shape.has_text_frame:
                        for paragraph in shape.text_frame.paragraphs:
                            for run in paragraph.runs:
                                if hasattr(run, "hyperlink") and run.hyperlink.address:
                                    links.append(run.hyperlink.address)
            return links
        else:
            raise TypeError("Unsupported file format")

    def extract_images(self):
        """Extract images from PDF, DOCX, and PPTX."""
        if hasattr(self.document, 'load_page'):  # PDF handling
            images = []
            for page_num in range(self.document.page_count):
                page = self.document.load_page(page_num)
                for img in page.get_images(full=True):
                    images.append(f"Image {img[0]} - Format: {img[1]} - Resolution: {img[2]}x{img[3]}")
            return images
        elif hasattr(self.document, 'inline_shapes'):  # DOCX handling
            return [inline_shape._inline.graphic.graphicData for inline_shape in self.document.inline_shapes]
        elif hasattr(self.document, 'slides'):  # PPTX handling
            images = []
            for slide in self.document.slides:
                for shape in slide.shapes:
                    if shape.shape_type == 13:  # picture type
                        images.append(f"Image found on slide")
            return images
        else:
            raise TypeError("Unsupported file format")

    def extract_tables(self):
        """Extract tables from PDF, DOCX, and PPTX."""
        if hasattr(self.document, 'load_page'):  # PDF handling using camelot
            # Use Camelot for table extraction from PDFs
            tables = camelot.read_pdf(self.file_path, pages='all')  # Use stored file_path
            extracted_tables = []
            for table in tables:
                extracted_tables.append(table.df.values.tolist())  # Convert to DataFrame or list format
            return extracted_tables

        elif hasattr(self.document, 'tables'):  # DOCX handling
            tables = []
            for table in self.document.tables:
                rows = []
                for row in table.rows:
                    cells = [cell.text for cell in row.cells]
                    rows.append(cells)
                tables.append(rows)
            return tables

        elif hasattr(self.document, 'slides'):  # PPTX handling
            tables = []
            for slide in self.document.slides:
                print(f"Processing slide {slide.slide_id}")
                for shape in slide.shapes:
                    print(f"Shape type: {shape.shape_type}")  
                    if shape.has_table:
                        print(f"Found table in slide {slide.slide_id}")
                        table = shape.table
                        rows = []
                        for row in table.rows:
                            cells = [cell.text for cell in row.cells]
                            rows.append(cells)
                        print(f"Extracted rows: {rows}") 
                        tables.append(rows)
            return tables

        else:
            raise TypeError("Unsupported file format")
