import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from utils import OCR
from Translator import Translator
import threading

root = tk.Tk()
root.title("OCR and Translator")
root.geometry("1200x800")
root.configure(bg='#145da0')

img_label = ttk.Label(root, borderwidth=2, relief="solid", background='#FFDAB9')  
image_path = ""

def load_image(image_path, max_width=600, max_height=600):
    try:
        image = Image.open(image_path)
        width_ratio = max_width / image.width
        height_ratio = max_height / image.height
        ratio = min(width_ratio, height_ratio)
        new_width = int(image.width * ratio)
        new_height = int(image.height * ratio)
        image = image.resize((new_width, new_height))
        return image
    except FileNotFoundError:
        print("Error: Image file not found.")
        return None
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def perform_ocr(image):
    global root

    if image is None:
        print("Error: No image provided.")
        return

    ocr = OCR(image)
    ocr_text = ocr.detection()

    def update_ui():
        ocr_text_box.delete(1.0, tk.END)
        ocr_text_box.insert(tk.END, ocr_text)

        translated_text = translate_text(ocr_text)
        translated_text_box.delete(1.0, tk.END)
        translated_text_box.insert(tk.END, translated_text)

        loading_label.config(text="")

    root.after(0, update_ui)

def translate_text(text):
    translator = Translator()
    translated_text = translator.Translate(text)
    return translated_text

def browse_image():
    global img_label
    global image_path

    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        image_path = file_path
        image = load_image(image_path)
        if image is not None:
            img_label.image = ImageTk.PhotoImage(image)
            img_label.configure(image=img_label.image)
            file_label.config(text="Selected Image: " + image_path)

            ocr_text_box.delete(1.0, tk.END)
            translated_text_box.delete(1.0, tk.END)

def update_text():
    global image_path

    if not image_path:
        print("Error: No image selected.")
        return

    image = load_image(image_path)
    if image is None:
        print("Error: Failed to load image.")
        return

    loading_label.config(text="Loading...")

    print("Performing OCR...")
    threading.Thread(target=perform_ocr, args=(image,)).start()

# Load placeholder image
image_path = "ig.png"
image = load_image(image_path)
if image is not None:
    img_label.image = ImageTk.PhotoImage(image)
    img_label.configure(image=img_label.image)
    img_label.place(relx=0.5, rely=0.3, anchor="center")

file_label = ttk.Label(root, text="Selected Image: None", background='#263D42', foreground='#FFFFFF')
file_label.place(relx=0.5, rely=0.1, anchor="center")

ocr_text_box = tk.Text(root, height=10, width=50, bg='#ffffff', fg='#000000', font=('Arial', 12))
ocr_text_box.insert(tk.END, "OCR Text Placeholder")
ocr_text_box.place(relx=0.1, rely=0.6)

translated_text_box = tk.Text(root, height=10, width=50, bg='#ffffff', fg='#000000', font=('Arial', 12))
translated_text_box.insert(tk.END, "Translated Text Placeholder")
translated_text_box.place(relx=0.5, rely=0.6)

loading_label = ttk.Label(root, text="", background='#263D42', foreground='#FFFFFF')
loading_label.place(relx=0.5, rely=0.8, anchor="center")

btn = ttk.Button(root, text="Perform OCR & Translate", command=update_text, style='LightOrange.TButton')
btn.place(relx=0.5, rely=0.8, anchor="center")

browse_btn = ttk.Button(root, text="Browse Image", command=browse_image, style='LightOrange.TButton')
browse_btn.place(relx=0.5, rely=0.9, anchor="center")

style = ttk.Style()
style.configure('LightOrange.TButton', background='#FFDAB9')  

root.mainloop()
