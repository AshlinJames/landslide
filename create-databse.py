

from docx import Document

def extract_table_details(file_path):
    doc = Document(file_path)
    paragraphs = doc.paragraphs
    table_details = []
    current_table_name = None
    current_table_columns = []

    for paragraph in paragraphs:
        text = paragraph.text.strip()
        if text.startswith("Table:"):
            # New table found
            if current_table_name is not None:
                table_details.append((current_table_name, current_table_columns))
            current_table_name = text.replace("Table:", "").strip().lower()
            current_table_columns = []
        elif text:
            # Column found
            if text.endswith("_id"):
                column_definition = f"{text.lower()} INT"
            else:
                column_definition = f"{text.lower()} VARCHAR(255)"
            current_table_columns.append(column_definition)

    # Append the last table
    if current_table_name is not None and len(current_table_columns) > 0:
        table_details.append((current_table_name, current_table_columns))

    return table_details

def generate_sql_script(table_details):
    sql_script = ""

    for table_data in table_details:
        table_name, columns = table_data

        create_table_statement = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
        column_definitions = ",\n".join([f"    {column}" for column in columns])

        # Set the first column as INT, PRIMARY KEY, and remove "_id" suffix
        first_column = columns[0].split(" ")[0].replace("_id", "")
        column_definitions = column_definitions.replace(columns[0], f"{first_column}_id INT PRIMARY KEY AUTO_INCREMENT")

        create_table_statement += column_definitions
        create_table_statement += "\n);\n\n"

        sql_script += create_table_statement

    return sql_script

# Specify the file path of the Word document
file_path = "/Users/shijojohn/Riss/2024-2025 Modules and Tables/2024-25 Projects/Nehru MCA/Land Slide/Land Slide Modules Synopsis.docx"

# Extract table details from the Word file
table_details = extract_table_details(file_path)

# Generate SQL script from table details
sql_script = generate_sql_script(table_details)

# Save SQL script to a file
output_file_path = "LandSlide.sql"
with open(output_file_path, "w") as f:
    f.write(sql_script)

print(f"SQL script saved to {output_file_path}")
