from document_processing.document_service import process_document

# ============================================================
# Document Processing Test
# ============================================================

# Change ONLY this filename to the actual file
# inside backend/uploads/
#
# Examples:
# "55b9581a_sample_manufacturing_requirements.pdf"
# "test.xlsx"
# "test.docx"
# "test.csv"

filename = "6b65cb29_product_requirements.txt"

# Build the complete path
file_path = f"uploads/{filename}"

print("========================================")
print("   AI Manufacturing Document Processor")
print("========================================")
print(f"Processing file: {filename}")
print(f"File path: {file_path}")
print()

try:
    # Process the document
    results = process_document(file_path)

    # Display number of extracted evidence items
    print(f"Extracted {len(results)} evidence items.")
    print()

    # Display each evidence item
    for index, item in enumerate(results, start=1):
        print("----------------------------------------")
        print(f"Evidence Item {index}")
        print("----------------------------------------")
        print(item)
        print()

    print("========================================")
    print("Document processing completed successfully.")
    print("========================================")

except FileNotFoundError:
    print("========================================")
    print("ERROR: File not found.")
    print("========================================")
    print(f"Could not find:")
    print(file_path)
    print()
    print("Make sure the file exists inside:")
    print("backend/uploads/")
    print()
    print("Example:")
    print("backend/uploads/55b9581a_sample_manufacturing_requirements.pdf")

except Exception as e:
    print("========================================")
    print("ERROR: Document processing failed.")
    print("========================================")
    print(f"Error: {e}")