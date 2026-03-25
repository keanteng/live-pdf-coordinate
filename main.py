import pymupdf  # PyMuPDF
import tkinter as tk
from PIL import Image, ImageTk


# Function to get mouse position on the canvas
def on_click(event):
    canvas_x, canvas_y = event.x, event.y
    
    # Check if click is within canvas boundaries
    if 0 <= canvas_x <= canvas_width and 0 <= canvas_y <= canvas_height:
        print(f"Cursor position on canvas: ({canvas_x}, {canvas_y})")

        # Map canvas coordinates to PDF coordinates
        pdf_x = (canvas_x / canvas_width) * page_width
        pdf_y = (
            (canvas_height - canvas_y) / canvas_height * page_height
        )  # Adjust for inverted y-axis
        print(f"Mapped PDF coordinates: ({pdf_x}, {pdf_y})")
        
        # Update coordinate display
        coord_display.config(text=f"Canvas: ({canvas_x}, {canvas_y}) | PDF: ({pdf_x:.2f}, {pdf_y:.2f})")
    else:
        print("Click outside canvas boundaries")
        coord_display.config(text="Canvas: (out of bounds) | PDF: (-, -)")

# Add a new function to track mouse movement for live coordinate updates
def on_mouse_move(event):
    canvas_x, canvas_y = event.x, event.y
    
    # Check if cursor is within canvas boundaries
    if 0 <= canvas_x <= canvas_width and 0 <= canvas_y <= canvas_height:
        # Map canvas coordinates to PDF coordinates
        pdf_x = (canvas_x / canvas_width) * page_width
        pdf_y = (
            (canvas_height - canvas_y) / canvas_height * page_height
        )  # Adjust for inverted y-axis
        
        # Update coordinate display
        coord_display.config(text=f"Canvas: ({canvas_x}, {canvas_y}) | PDF: ({pdf_x:.2f}, {pdf_y:.2f})")
    else:
        # When cursor is outside the canvas
        coord_display.config(text="Canvas: (out of bounds) | PDF: (-, -)")

def load_page(page_num):
    global current_page, page, canvas_width, canvas_height, page_width, page_height, tk_img
    
    # Update current page number
    current_page = page_num
    
    # Load the page
    page = document.load_page(current_page)
    
    # Render the page to an image
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # Update the canvas with the new image
    tk_img = ImageTk.PhotoImage(img)
    canvas.config(width=pix.width, height=pix.height)
    canvas.itemconfig(canvas_image, image=tk_img)
    
    # Update dimensions
    canvas_width, canvas_height = pix.width, pix.height
    page_width = page.rect.width
    page_height = page.rect.height
    
    # Update page status label
    page_status.config(text=f"Page {current_page + 1} of {total_pages}")
    
    # Update button states
    prev_button.config(state=tk.NORMAL if current_page > 0 else tk.DISABLED)
    next_button.config(state=tk.NORMAL if current_page < total_pages - 1 else tk.DISABLED)
    
    # Reset coordinate display
    coord_display.config(text="Canvas: (-, -) | PDF: (-, -)")


def prev_page():
    if current_page > 0:
        load_page(current_page - 1)


def next_page():
    if current_page < total_pages - 1:
        load_page(current_page + 1)


def go_to_page():
    try:
        requested_page = int(page_entry.get()) - 1  # Convert from 1-based to 0-based
        if 0 <= requested_page < total_pages:
            load_page(requested_page)
        else:
            print(f"Page number must be between 1 and {total_pages}")
    except ValueError:
        print("Please enter a valid page number")


# Load the PDF and get the first page, prompt if error
try:
    pdf_path = "hcs_card.pdf"
    document = pymupdf.open(pdf_path)
    total_pages = document.page_count
    current_page = 0
    page = document.load_page(current_page)
except Exception as e:
    print(f"Error loading PDF: {e}")
    
#pdf_path = input("Enter the path to the PDF file: ")

# Create a tkinter window
root = tk.Tk()
root.title("PDF Viewer")

# Create a frame for the page navigation controls
control_frame = tk.Frame(root)
control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

# Create navigation buttons and page entry
prev_button = tk.Button(control_frame, text="Previous", command=prev_page)
prev_button.pack(side=tk.LEFT, padx=5)

page_status = tk.Label(control_frame, text=f"Page {current_page + 1} of {total_pages}")
page_status.pack(side=tk.LEFT, padx=5)

page_entry = tk.Entry(control_frame, width=5)
page_entry.pack(side=tk.LEFT, padx=5)

go_button = tk.Button(control_frame, text="Go to Page", command=go_to_page)
go_button.pack(side=tk.LEFT, padx=5)

next_button = tk.Button(control_frame, text="Next", command=next_page)
next_button.pack(side=tk.LEFT, padx=5)

# Create a status frame for coordinate display
status_frame = tk.Frame(root)
status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)

# Add coordinate display label
coord_display = tk.Label(status_frame, text="Canvas: (-, -) | PDF: (-, -)", anchor=tk.W, 
                        relief=tk.SUNKEN, bd=1, padx=5, pady=2)
coord_display.pack(fill=tk.X)

# Disable prev button on first page
prev_button.config(state=tk.DISABLED if current_page == 0 else tk.NORMAL)
# Disable next button if only one page
next_button.config(state=tk.DISABLED if total_pages <= 1 else tk.NORMAL)

# Render the first page
pix = page.get_pixmap()
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

# Convert the image to a format tkinter can use
tk_img = ImageTk.PhotoImage(img)

# Create a canvas and add the image to it
canvas = tk.Canvas(root, width=pix.width, height=pix.height)
canvas.pack(expand=True, fill=tk.BOTH)
canvas_image = canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)

# Bind the mouse events
canvas.bind("<Button-1>", on_click)
canvas.bind("<Motion>", on_mouse_move)  # Track mouse movement for live updates

# Get canvas dimensions (same as image dimensions)
canvas_width, canvas_height = pix.width, pix.height

# Get PDF page dimensions
page_width = page.rect.width
page_height = page.rect.height
print(f"PDF Page dimensions: {page_width}x{page_height}")
print(f"Total pages in document: {total_pages}")

# Start the tkinter main loop
root.mainloop()