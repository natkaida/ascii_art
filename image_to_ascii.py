import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import os

# ASCII символы, используемые для построения ASCII-арта
ASCII_CHAR = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

class ImageToASCIIConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Вычисляем координаты для размещения окна по центру
        x = (screen_width // 2) - (700 // 2)  # Ширина окна - 700 пикселей
        y = (screen_height // 2) - (600 // 2)  # Высота окна - 600 пикселей
        self.geometry(f"700x600+{x}+{y}")
        self.title("Конвертация изображения в ASCII-арт")
        self.original_image = None
        self.ascii_image = None
        self.images = {}
        self.create_widgets()

    def create_widgets(self):
        # Создание фрейма и элементов интерфейса
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Исходное изображение
        original_image_frame = tk.Frame(main_frame)
        original_image_frame.pack(side="left", padx=10)

        # Плейсхолдер
        self.canvas = tk.Canvas(original_image_frame, width=300, height=300)
        self.canvas.pack()
        self.canvas.create_rectangle(0, 0, 300, 300, fill="light blue", outline="")
        self.canvas.create_text(150, 150, text="Выберите изображение", font=("Verdana", 16))

        # Текстовое поле для вывода ASCII-арта
        ascii_text_frame = tk.Frame(main_frame)
        ascii_text_frame.pack(side="right", padx=10)
        self.ascii_text = tk.Text(ascii_text_frame, width=100, height=50, font=("Courier", 4), state="disabled")
        self.ascii_text.pack(side="top", pady=10)

        # Кнопки
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        choose_image_button = tk.Button(button_frame, text="Выбрать изображение", command=self.choose_image)
        choose_image_button.pack(side="left", padx=5)
        self.convert_button = tk.Button(button_frame, text="Конвертировать", command=self.display_ascii_art, state="disabled")
        self.convert_button.pack(side="left", padx=5)
        self.save_button = tk.Button(button_frame, text="Сохранить", command=self.save_ascii_art, state="disabled")
        self.save_button.pack(side="left", padx=5)

    def choose_image(self): #Типы файлов, видимые в диалоговом окне
        image_exts = r"*.jpg *.jpeg *.png *.bmp"
        image_filetypes = [
            ("Изображения", image_exts),
            ("JPEG", "*.jpg;*.jpeg"),
            ("PNG", "*.png"),
            ("BMP", "*.bmp"),
            ("Все файлы", "*.*")
        ]
        file_path = filedialog.askopenfilename(filetypes=image_filetypes)
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.display_original_image()  # Отображаем изображение на холсте
                self.convert_button.config(state="normal")
            except Exception as e:
                print(f"Ошибка при открытии файла: {e}")

    def display_original_image(self):
        # Очищаем холст
        self.canvas.delete("all")
        if "original" in self.images: #Удаляем ссылку на изображение
            del self.images["original"] #если было выбрано другое
 

        # Показываем изображение на холсте
        if self.original_image is not None:
            resized_image = self.original_image.resize((300, 300), Image.Resampling.LANCZOS)
            original_image_tk = ImageTk.PhotoImage(resized_image)
            self.images["original"] = original_image_tk  # Сохраняем ссылку на изображение в словаре
            self.canvas.create_image(0, 0, anchor="nw", image=original_image_tk)
    
    def resize_img(self, image, new_width=100):
        # Вычисляем высоту и ширину уменьшенного изображения, сохраняя соотношение сторон
        width, height = image.size
        ratio = height / width 
        new_height = int(new_width * ratio)
        resized_img = image.resize((new_width, new_height))
        return resized_img

    def pixel_to_grayscale(self, image):
        # Преобразование изображения в оттенки серого
        grayscale_img = image.convert("L")
        return grayscale_img

    def pixel_to_ascii(self, image):
        # Преобразованиe пикселей изображения в ASCII символы
        pixels = image.getdata()
        characters = "".join(ASCII_CHAR[pixel // 25] for pixel in pixels)
        return characters

    def convert_to_ascii(self, image, new_width=100):
        grayscale_image = self.pixel_to_grayscale(self.resize_img(image))
        new_image_data = self.pixel_to_ascii(grayscale_image)
        pixel_nb = len(new_image_data)
        ascii_img = "\n".join(new_image_data[i : i + new_width] for i in range(0, pixel_nb, new_width))
        return ascii_img


    def display_ascii_art(self):
        ascii_art = self.convert_to_ascii(self.original_image)
        self.ascii_text.config(state="normal")
        self.ascii_text.delete("1.0", tk.END)
        self.ascii_text.insert(tk.END, ascii_art)
        self.ascii_text.config(state="disabled")
        self.save_button.config(state="normal")  # Включаем кнопку "Сохранить" после конвертации

    def save_ascii_art(self):
    # Проверяем, было ли выбрано изображение
        if self.original_image is None:
            print("Не выбрано изображение для конвертации.")
            return

        # Получаем путь к исходному изображению
        original_image_path = self.original_image.filename
        # Извлекаем имя файла без расширения
        original_filename = os.path.splitext(os.path.basename(original_image_path))[0]
        # Создаем путь для сохранения ASCII-арта, используя имя исходного файла
        ascii_art_path = os.path.join(os.path.dirname(original_image_path), f"{original_filename}_ascii.txt")

        # Сохраняем ASCII-арт в файл
        with open(ascii_art_path, "w") as file:
            ascii_art = self.ascii_text.get("1.0", tk.END)
            file.write(ascii_art)
            print(f"ASCII-арт сохранен в файл: {ascii_art_path}")
     

if __name__ == "__main__":
    app = ImageToASCIIConverter()
    app.mainloop()