import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog

class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Image Viewer")

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(expand="true", fill="both", side="left")  # Используйте side="left" для выравнивания слева

        self.page_scale = tk.Scale(self.root, from_=1, to=1, orient=tk.VERTICAL, label="", command=self.show_page)
        self.page_scale.pack(fill="y", side="right")  # Используйте side="right" для выравнивания справа

        self.photo_image = None  # Сохраняем ссылку на объект PhotoImage

        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_pdf)

    def open_pdf(self):
        file_path = filedialog.askopenfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            self.pdf_document = fitz.open(file_path)

            num_pages = len(self.pdf_document)
            self.page_scale.config(to=num_pages, label=f"Page ({num_pages})")
            self.page_scale.set(1)

            self.show_page(1)

            self.root.mainloop()

    def show_page(self, page_number):
        page_number = int(page_number)
        page = self.pdf_document[page_number - 1]
        image = page.get_pixmap()
        self.photo_image = tk.PhotoImage(data=image.tobytes(), width=image.width, height=image.height)

        self.canvas.config(width=image.width, height=image.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

if __name__ == "__main__":
    root = tk.Tk()
    pdf_viewer = PDFViewer(root)
    root.mainloop()
