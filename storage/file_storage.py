import csv
from .storage import Storage

class FileStorage(Storage):
    def store(self):
        # Save text to a file
        with open('extracted_text.txt', 'w') as text_file:
            text_file.write(self.extractor.extract_text())

        # Save tables to a CSV file
        with open('extracted_tables.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            tables = self.extractor.extract_tables()
            for table in tables:
                for row in table:
                    if isinstance(row, (list, tuple)):
                        cleaned_row = [cell.strip() for cell in row if isinstance(cell, str) and cell.strip()]  # Remove empty strings
                        writer.writerow(cleaned_row)
                    else:
                        print(f"Unexpected row format: {row}")  # Log unexpected row format

        # Save images as filenames (simulate saving)
        images = self.extractor.extract_images()
        print(f"Images saved: {images}")
