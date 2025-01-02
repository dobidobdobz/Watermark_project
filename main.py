import re
import tkinter
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import ImageTk, Image, ImageDraw, ImageFont

# Constants
DARK_GREY = "#272727"
left_canvas_width = 480
left_canvas_height = 300
right_canvas_width = 800
right_canvas_height = 625
available_fonts = ["Arial", "Calibri", "Georgia", "Impact", "Verdana", "Tahoma", "Gabriola", "Jokerman", "Mistral", "Ebrima"]

# Initialize the main window
window = Tk()
window.title("Watermark App")
window.maxsize(1400, 1080)
window.config(bg="black")
window.iconbitmap('droplet-fill.ico')

# image variables
left_img_display = None
right_img_display = None
img = None
img_right = None


def save():
    """Save the modified image to a chosen location."""
    # Open a file dialog to choose the save location and file name
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",  # Default extension if the user doesn't specify one
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],  # File types to show in the dialog
        title="Save Image As"  # Title of the dialog window
    )

    if file_path:
        try:
            img_right.save(file_path)
            messagebox.showinfo("Success", f"Image saved successfully at {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the image: {e}")


def clear_watermark():
    """Apply the watermark on the image."""
    global img, img_right, file_path, original, right_label, right_img_display

    del right_img_display

    img = Image.open(file_path)
    img_right = img.copy()

    img_right_width, img_right_height = img_right.size
    aspect_ratio_right = img_right_width / img_right_height
    if img_right_width > right_canvas_width or img_right_height > right_canvas_height:
        if img_right_width / right_canvas_width > img_right_height / right_canvas_height:
            new_right_width = right_canvas_width
            new_right_height = int(right_canvas_width / aspect_ratio_right)
        else:
            new_right_height = right_canvas_height
            new_right_width = int(right_canvas_height * aspect_ratio_right)
    else:
        new_right_width, new_right_height = img_right_width, img_right_height

    # Resize to fit inside the canvas
    img_right = img_right.resize((new_right_width, new_right_height), Image.Resampling.LANCZOS)

    right_img_display = ImageTk.PhotoImage(img_right)

    # Replace the image in the right frame
    right_label.config(image=right_img_display)


def apply():
    """Apply the watermark on the image."""
    global draw_on_blank_image, right_img_display, right_label, font_color, font_size, Rotate, Tile

    if watermark_textfield.get() == '':
        watermark_text = "example text"
    else:
        watermark_text = watermark_textfield.get()

    font_choice = font_combobox.get()

    if font_color.get() == '':
        font_color_value = (255, 255, 255, 255)
    else:
        color = tuple(map(int, re.findall(r'\d+', font_color.get())))
        font_color_value = color

    try:
        font_size_value = int(font_size.get())
    except:
        font_size_value = 20

    Tile_value = Tile.get()

    try:
        Rotate_value = int(Rotate.get())
    except:
        Rotate_value = 0

    # try user font choice, else fallback on default font
    try:
        font = ImageFont.truetype(f"C:/Windows/Fonts/{font_choice}.ttf", size=font_size_value)  # Specify font and size
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font if not found

    # create blank image
    blank_image = Image.new('RGBA', img_right.size, (0, 0, 0, 0))

    if Tile_value == "" or Tile_value == "1":
        # draw on the blank image
        draw_on_blank_image = ImageDraw.Draw(blank_image)

        # Get text size (width, height) for the watermark text
        text_width, text_height = draw_on_blank_image.textbbox((0, 0), watermark_text, font=font)[2:4]

        # Calculate the position to center the text
        image_width, image_height = img_right.size
        x_position = (image_width - text_width) // 2  # Center the text horizontally
        y_position = (image_height - text_height) // 2  # Center the text vertically

        # Draw the text on the blank_image
        draw_on_blank_image.text((x_position, y_position), f"{watermark_text}", font=font, fill=font_color_value)

        # Rotate the text blank_image
        rotate_blank_image = blank_image.rotate(Rotate_value)

        # paste the rotated blank image
        img_right.paste(rotate_blank_image, (0, 0), rotate_blank_image.convert("RGBA"))

        # Update the display on the right frame
        right_img_display = ImageTk.PhotoImage(img_right)
        right_label.config(image=right_img_display)

    elif Tile_value == "2":

        # Draw on the blank image
        draw_on_blank_image = ImageDraw.Draw(blank_image)

        # Get text size (width, height) for the watermark text
        text_width, text_height = draw_on_blank_image.textbbox((0, 0), watermark_text, font=font)[2:4]

        # Calculate the position to center the text
        image_width, image_height = img_right.size
        x_position = (image_width - text_width) // 2  # Center the text horizontally
        y_position = (image_height - text_height) // 2  # Center the text vertically

        # Draw center text
        draw_on_blank_image.text((x_position, y_position), text=watermark_text, font=font, fill=font_color_value)

        # Calculate quadrant centers (based on image size)
        quadrants = {
            "Q1": ((image_width // 4), (image_height // 4)),  # Top-left
            "Q2": ((3 * image_width // 4), (image_height // 4)),  # Top-right
            "Q3": ((3 * image_width // 4), (3 * image_height // 4)),  # Bottom-right
            "Q4": ((image_width // 4), (3 * image_height // 4)),  # Bottom-left
        }

        # Draw text in the center of each quadrant
        for quadrant, (x, y) in quadrants.items():
            # Adjust text position so it's centered in the quadrant
            x_position = x - (text_width // 2)
            y_position = y - (text_height // 2)

            # Draw the text on the blank image at the calculated position
            draw_on_blank_image.text((x_position, y_position), text=watermark_text, font=font, fill=font_color_value)

            rotate_blank_image = blank_image.rotate(Rotate_value)
            img_right.paste(rotate_blank_image, (0, 0), rotate_blank_image.convert("RGBA"))
            right_img_display = ImageTk.PhotoImage(img_right)
            right_label.config(image=right_img_display)

    elif Tile_value == "3":

        # Draw on the blank image
        draw_on_blank_image = ImageDraw.Draw(blank_image)

        # Get image dimensions
        image_width, image_height = img_right.size

        # Define number of rows and columns for the grid
        rows = 3  # You can change this based on your preference
        cols = 3

        # Calculate the spacing between watermarks
        x_spacing = image_width // cols
        y_spacing = image_height // rows

        # Define padding from the edges to ensure watermark isn't too close to the border
        padding = 60

        # Loop through each grid cell and place a watermark
        for row in range(rows):
            for col in range(cols):
                # Calculate position for the watermark
                x_position = col * x_spacing + padding
                y_position = row * y_spacing + padding

                # Draw the watermark at the calculated position
                draw_on_blank_image.text((x_position, y_position), watermark_text, font=font, fill=font_color_value)

        rotate_blank_image = blank_image.rotate(Rotate_value)
        img_right.paste(rotate_blank_image, (0, 0), rotate_blank_image.convert("RGBA"))
        right_img_display = ImageTk.PhotoImage(img_right)
        right_label.config(image=right_img_display)


# Function to handle image upload
def upload_image():
    global img, img_right, left_img_display, right_img_display, file_path, original

    # Open file dialog to select an image
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

    if file_path:
        try:
            # Load the selected image
            img = Image.open(file_path)
            img_right = img.copy()
            original = img.copy()

            # Resize image to fit in left frame
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height
            if img_width > left_canvas_width or img_height > left_canvas_height:
                if img_width / left_canvas_width > img_height / left_canvas_height:
                    new_width = left_canvas_width
                    new_height = int(left_canvas_width / aspect_ratio)
                else:
                    new_height = left_canvas_height
                    new_width = int(left_canvas_height * aspect_ratio)
            else:
                new_width, new_height = img_width, img_height

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Resize to fit inside the canvas
            left_img_display = ImageTk.PhotoImage(img)

            # Replace the image in the left frame
            left_label.config(image=left_img_display)

            # Resize image to fit in right frame
            img_right_width, img_right_height = img_right.size
            print(img_right.size)
            aspect_ratio_right = img_right_width / img_right_height
            if img_right_width > right_canvas_width or img_right_height > right_canvas_height:
                if img_right_width / right_canvas_width > img_right_height / right_canvas_height:
                    new_right_width = right_canvas_width
                    new_right_height = int(right_canvas_width / aspect_ratio_right)
                else:
                    new_right_height = right_canvas_height
                    new_right_width = int(right_canvas_height * aspect_ratio_right)
            else:
                new_right_width, new_right_height = img_right_width, img_right_height

            print(new_right_width, new_right_height)
            img_right = img_right.resize((new_right_width, new_right_height), Image.Resampling.LANCZOS)  # Resize to fit inside the canvas
            right_img_display = ImageTk.PhotoImage(img_right)

            # Replace the image in the right frame
            right_label.config(image=right_img_display)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open the image: {e}")


# Create left and right frames
left_frame = Frame(window, bg=DARK_GREY)
right_frame = Frame(window, bg=DARK_GREY)
left_frame.grid(row=0, column=0, padx=10, pady=5)
right_frame.grid(row=0, column=1, padx=10, pady=5)

# Labels for left frame
Label(left_frame, text="Original Image", font=("Arial", 12, "bold"), fg="white", bg=DARK_GREY).grid(row=0, column=0, padx=5, pady=5)

# Labels to display image in left and right frame
left_label = Label(left_frame, bg=DARK_GREY)
left_label.grid(row=1, column=0, padx=5, pady=5)
right_label = Label(right_frame, bg=DARK_GREY)
right_label.grid(row=0, column=0, padx=5, pady=5)

# all buttons
save_button = tkinter.Button(left_frame, text="Save", command=save, bg="green", fg="white", font=("Arial", 10))
save_button.grid(row=2, column=0, sticky="ew")  # Center horizontally (east-west)

clear_watermark_button = tkinter.Button(left_frame, text="Clear Watermark", command=clear_watermark, bg="green", fg="white", font=("Arial", 10))
clear_watermark_button.grid(row=3, column=0, sticky="ew")  # Center horizontally (east-west)

upload_button = tkinter.Button(left_frame, text="Upload Image", command=upload_image, bg="green", fg="white", font=("Arial", 10))
upload_button.grid(row=4, column=0, sticky="ew")  # Center horizontally (east-west)

apply_button = tkinter.Button(left_frame, text="Apply", command=apply, bg="green", fg="white", font=("Arial", 10))
apply_button.grid(row=5, column=0, sticky="ew")

# Watermark properties frame
watermark_properties = Frame(left_frame)
watermark_properties.grid(row=6, column=0, padx=0, pady=0)

# Watermark properties widgets
watermark_text_label = Label(watermark_properties, text="Watermark text:")
watermark_text_label.grid(row=1, column=0, padx=2, pady=1)
watermark_textfield = Entry(watermark_properties, width=54, justify='center')
watermark_textfield.grid(row=1, column=1)

font_label = Label(watermark_properties, text="Font")
font_label.grid(row=2, column=0, padx=2, pady=1)
font_combobox = ttk.Combobox(watermark_properties, values=available_fonts, width=50)
font_combobox.grid(row=2, column=1, padx=0, pady=0)
font_combobox.set("Arial")

font_color_label = Label(watermark_properties, text="Font-color rgba(255, 255, 255, 255)")
font_color_label.grid(row=3, column=0, padx=2, pady=1)
font_color = Entry(watermark_properties, width=54, justify='center')
font_color.grid(row=3, column=1)

font_size_label = Label(watermark_properties, text="Font-size")
font_size_label.grid(row=4, column=0, padx=2, pady=1)
font_size = Entry(watermark_properties, width=54, justify='center')
font_size.grid(row=4, column=1)

Rotate_label = Label(watermark_properties, text="Rotate(degree's)")
Rotate_label.grid(row=5, column=0, padx=2, pady=1)
Rotate = Entry(watermark_properties, width=54, justify='center')
Rotate.grid(row=5, column=1)

Tile_label = Label(watermark_properties, text="Tile (1/2/3)")
Tile_label.grid(row=6, column=0, padx=5, pady=1)
Tile = Entry(watermark_properties, width=54, justify="center")
Tile.grid(row=6, column=1)

window.mainloop()
