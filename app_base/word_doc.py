import os
import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF
from pathlib import Path

class PDF(FPDF):
    def header(self):
        if hasattr(self, 'document_title'):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, self.document_title, 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title, font='Arial', size=12):
        self.set_font(font, 'B', size)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body, font='Arial', size=12):
        self.set_font(font, '', size)
        self.multi_cell(0, 10, body)
        self.ln()

def create_pdf(filename, document_title, author, chapters, image_path=None):
    pdf = PDF()
    pdf.document_title = document_title
    pdf.add_page()
    if author:
        pdf.set_author(author)
    if image_path:
        pdf.image(image_path, x=10, y=25, w=pdf.w - 20)
        pdf.ln(120)

    for chapter in chapters:
        title, body, font, size = chapter
        pdf.chapter_title(title, font, size)
        pdf.chapter_body(body, font, size)

    pdf.output(filename)

def generate_pdf():
    document_title = title_entry.get()
    author = author_entry.get()

    chapters = []
    for i in range(int(chapter_count_entry.get())):
        chapter_title = chapter_title_entries[i].get()
        chapter_body = chapter_body_texts[i].get("1.0", tk.END)
        chapters.append((chapter_title, chapter_body, 'Arial', 12))

    # Set the download path to the user's Downloads directory
    download_path = os.path.join(Path.home(), "Downloads", "Generated_Document.pdf")

    create_pdf(download_path, document_title, author, chapters)
    status_label.config(text=f"PDF saved to {download_path}")

def select_image():
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
    image_label.config(text=image_path)

def update_chapter_fields():
    # Clear existing chapter fields if any
    for widget in chapter_frame.winfo_children():
        widget.destroy()

    # Create the chapter title and body fields based on the number of chapters specified
    num_chapters = int(chapter_count_entry.get())
    for i in range(num_chapters):
        tk.Label(chapter_frame, text=f"Page {i + 1} Title:").pack()
        chapter_title_entry = tk.Entry(chapter_frame, width=50)
        chapter_title_entry.pack()
        chapter_title_entries.append(chapter_title_entry)

        tk.Label(chapter_frame, text=f"Page {i + 1} Body:").pack()
        chapter_body_text = tk.Text(chapter_frame, width=60, height=5)
        chapter_body_text.pack()
        chapter_body_texts.append(chapter_body_text)

# Create the main application window
root = tk.Tk()
root.title("PDF Document Creator")

# Document title input
tk.Label(root, text="Document Title:").pack()
title_entry = tk.Entry(root, width=50)
title_entry.pack()

# Author input
tk.Label(root, text="Author:").pack()
author_entry = tk.Entry(root, width=50)
author_entry.pack()

# Chapter count input
tk.Label(root, text="Number of pages:").pack()
chapter_count_entry = tk.Entry(root, width=10)
chapter_count_entry.pack()

# Add a button to create the chapter fields based on the number specified
chapter_button = tk.Button(root, text="Add pages", command=lambda: update_chapter_fields())
chapter_button.pack()

# Frame to contain chapter fields dynamically
chapter_frame = tk.Frame(root)
chapter_frame.pack()

# Lists to hold chapter title and body fields
chapter_title_entries = []
chapter_body_texts = []

# Image selection button
image_label = tk.Label(root, text="No image selected")
image_label.pack()
select_image_button = tk.Button(root, text="Select Image", command=select_image)
select_image_button.pack()

# Generate PDF button
generate_button = tk.Button(root, text="Generate PDF", command=generate_pdf)
generate_button.pack()

# Status label to display the save status of the PDF
status_label = tk.Label(root, text="")
status_label.pack()

# Start the main loop
root.mainloop()
