import PyPDF2
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window(title="PDF decrypter", themename="superhero", size=(300,250))
root.position_center()

# Open the PDF file in read-binary mode
def remove_password(dir_path, filename, password, output_path, output):
    output_path = output_path + "/"
    with open(dir_path + filename, 'rb') as input_file:

        # Create a PdfFileReader object
        pdf_reader = PyPDF2.PdfReader(input_file)
        pdf_reader.decrypt(password)

        # Get the number of pages in the PDF file
        num_pages = len(pdf_reader.pages)

        # Create a new PDF file in write-binary mode
        with open(output_path + output, 'wb') as output_file:

            # Create a PdfFileWriter object
            pdf_writer = PyPDF2.PdfWriter()

            # Loop through each page in the PDF file
            for page_num in range(num_pages):

                # Get the current page
                page = pdf_reader.pages[page_num]

                # Add the current page to the PdfFileWriter object
                pdf_writer.add_page(page)

            # Write the PdfFileWriter object to the output file
            pdf_writer.write(output_file)

def execute(dir_path, output_path, password):

    files = []
    dir_path = dir_path + "/"
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            files.append(path)

    for file in files:
        remove_password(dir_path, file, password, output_path, "Unlocked_" + file)

dir_path_label = ttk.Label(root, text="Path of the files directory")
dir_path_label.place(relx = 0.5, rely = 0.1, anchor = "center")
dir_path_entry = ttk.Entry(root)
dir_path_entry.place(relx = 0.5, rely = 0.2, anchor = "center")

output_path_label = ttk.Label(root, text="Path for pdfs to be outputed")
output_path_label.place(relx = 0.5, rely = 0.3, anchor = "center")
output_path_entry = ttk.Entry(root)
output_path_entry.place(relx = 0.5, rely = 0.4, anchor = "center")

password_label = ttk.Label(root, text="Password")
password_label.place(relx = 0.5, rely = 0.5, anchor = "center")
password_entry = ttk.Entry(root)
password_entry.place(relx = 0.5, rely = 0.6, anchor = "center")

execute_button = ttk.Button(root, text="EXECUTE", bootstyle="SUCCESS", command = lambda: execute(dir_path_entry.get(), output_path_entry.get(), password_entry.get()))
execute_button.place(relx = 0.5, rely = 0.8, anchor = "center")

"""
# folder path
dir_path = "D:/Programs/VisualCode/Projects/PDFs/Proizvodno/"
output_path = "D:/School/3.letnik/2.semester/PI/"

# list to store files
files = []

# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        files.append(path)
"""

#for file in files:
    #remove_password(file, "4b9P9eyA", "Unlocked_" + file)

root.mainloop()