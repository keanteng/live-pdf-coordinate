import fitz  # PyMuPDF
import tkinter as tk
from PIL import Image, ImageTk


# Function to get mouse position on the canvas
def on_click(event):
    canvas_x, canvas_y = event.x, event.y
    print(f"Cursor position on canvas: ({canvas_x}, {canvas_y})")

    # Map canvas coordinates to PDF coordinates
    pdf_x = (canvas_x / canvas_width) * page_width
    pdf_y = (
        (canvas_height - canvas_y) / canvas_height * page_height
    )  # Adjust for inverted y-axis
    print(f"Mapped PDF coordinates: ({pdf_x}, {pdf_y})")


# Load the PDF and get the first page, prompt if error
try:
    pdf_path = "einvoicer_template1.pdf"
    document = fitz.open(pdf_path)
    page = document.load_page(0)
except Exception as e:
    print(f"Error loading PDF: {e}")
    
#pdf_path = input("Enter the path to the PDF file: ")

document = fitz.open(pdf_path)
page = document.load_page(0)

# Render the page to an image
pix = page.get_pixmap()
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

# Create a tkinter window
root = tk.Tk()
root.title("PDF Viewer")

# Convert the image to a format tkinter can use
tk_img = ImageTk.PhotoImage(img)

# Create a canvas and add the image to it
canvas = tk.Canvas(root, width=pix.width, height=pix.height)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)

# Bind the mouse click event to the on_click function
canvas.bind("<Button-1>", on_click)

# Get canvas dimensions (same as image dimensions)
canvas_width, canvas_height = pix.width, pix.height

# Get PDF page dimensions
page_width = page.rect.width
page_height = page.rect.height
print(f"PDF Page dimensions: {page_width}x{page_height}")

# Start the tkinter main loop
root.mainloop()
