import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

class BackgammonCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contadora de Fichas - Grupo 4")
        self.root.state('zoomed')
        self.root.geometry("{}x{}".format(root.winfo_screenwidth(), root.winfo_screenheight()))

        self.result_tarea1 = tk.StringVar()
        self.result_tarea2 = tk.StringVar()
        self.result_tarea3 = tk.StringVar()

        self.image_original = None
        self.lbl_imagen = None

        self.init_gui()

    def init_gui(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Cargar Imagen", command=self.cargar_imagen)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.salir)

        main_frame = ttk.Frame(self.root, padding=(20, 20, 20, 20), style="Main.TFrame")
        main_frame.pack(pady=10, fill=tk.X)

        style = ttk.Style()
        style.configure("Main.TFrame", background="#f0f0f0")
        style.configure("Main.TButton", padding=10, font=("Segoe UI", 12))
        style.map("Main.TButton",
                  background=[("active", "#3498db"), ("disabled", "#95a5a6")],
                  foreground=[("active", "blue"), ("disabled", "gray")])

        btn_cargar_imagen = ttk.Button(main_frame, text="Cargar Imagen", command=self.cargar_imagen, style="Main.TButton")
        btn_cargar_imagen.grid(row=0, column=0, pady=10, padx=10)

        btn_realizar_tareas = ttk.Button(main_frame, text="Ejecutar", command=self.realizar_tareas, style="Main.TButton")
        btn_realizar_tareas.grid(row=0, column=1, pady=10, padx=10)

        btn_limpiar_imagen = ttk.Button(main_frame, text="Limpiar Imagen", command=self.limpiar_imagen, style="Main.TButton")
        btn_limpiar_imagen.grid(row=0, column=2, pady=10, padx=10)

        btn_salir = ttk.Button(main_frame, text="Salir", command=self.salir, style="Main.TButton")
        btn_salir.grid(row=0, column=3, pady=10, padx=10)

        lbl_result_tarea1 = ttk.Label(main_frame, textvariable=self.result_tarea1, font=("Segoe UI", 12), style="Main.TLabel")
        lbl_result_tarea1.grid(row=1, column=0, padx=10, pady=5, columnspan=4, sticky=tk.W)

        lbl_result_tarea2 = ttk.Label(main_frame, textvariable=self.result_tarea2, font=("Segoe UI", 12), style="Main.TLabel")
        lbl_result_tarea2.grid(row=2, column=0, padx=10, pady=5, columnspan=4, sticky=tk.W)

        lbl_result_tarea3 = ttk.Label(main_frame, textvariable=self.result_tarea3, font=("Segoe UI", 12), style="Main.TLabel")
        lbl_result_tarea3.grid(row=3, column=0, padx=10, pady=5, columnspan=4, sticky=tk.W)

        self.lbl_imagen = ttk.Label(main_frame, style="Main.TLabel")
        self.lbl_imagen.grid(row=4, column=0, columnspan=4, pady=10)

        style.configure("Main.TLabel", background="#f0f0f0")

    def cargar_imagen(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp")])

        if file_path:
            self.image_original = Image.open(file_path)
            image = ImageTk.PhotoImage(self.image_original)

            if self.lbl_imagen:
                self.lbl_imagen.config(image=image)
                self.lbl_imagen.image = image
            else:
                self.lbl_imagen = ttk.Label(self.root, image=image, style="Main.TLabel")
                self.lbl_imagen.image = image
                self.lbl_imagen.grid(row=4, column=0, columnspan=4, pady=10)

            self.image_path = file_path

    def realizar_tareas(self):
        if hasattr(self, 'image_path'):
            image = cv2.imread(self.image_path)

            _, _, _ = self.contar_fichas_por_color(image)

            image_circles, num_circles = self.encerrar_fichas_circulares(image)
            image_circles = cv2.cvtColor(image_circles, cv2.COLOR_BGR2RGB)
            image_circles = Image.fromarray(image_circles)
            image_circles = ImageTk.PhotoImage(image_circles)

            self.lbl_imagen.config(image=image_circles)
            self.lbl_imagen.image = image_circles

            self.result_tarea3.set(f"Fichas circulares encontradas: {num_circles}")

    def salir(self):
        self.root.destroy()

    def limpiar_imagen(self):
        self.image_original = None
        self.lbl_imagen.config(image=None)
        self.lbl_imagen.image = None
        delattr(self, 'image_path')
        self.result_tarea1.set("")
        self.result_tarea2.set("")
        self.result_tarea3.set("")

    def contar_fichas_por_color(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_color1 = np.array([H_MIN1, S_MIN1, V_MIN1])
        upper_color1 = np.array([H_MAX1, S_MAX1, V_MAX1])

        lower_color2 = np.array([H_MIN2, S_MIN2, V_MIN2])
        upper_color2 = np.array([H_MAX2, S_MAX2, V_MAX2])

        mask_color1 = cv2.inRange(hsv, lower_color1, upper_color1)
        mask_color2 = cv2.inRange(hsv, lower_color2, upper_color2)

        contours_color1, _ = cv2.findContours(mask_color1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_color2, _ = cv2.findContours(mask_color2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        count_color1 = len(contours_color1)
        count_color2 = len(contours_color2)

        return None, count_color1, count_color2

    def contar_fichas_por_grupo(self, image):
        # Eliminar la lógica y el texto "Implementa la lógica aquí"
        pass

    def contar_fichas_por_fila(self, image):
        # Eliminar la lógica y el texto "Implementa la lógica aquí"
        pass

    def encerrar_fichas_circulares(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 30, 100)
        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                                   param1=50, param2=30, minRadius=5, maxRadius=35)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for circle in circles:
                cv2.circle(image, (circle[0], circle[1]), circle[2], (0, 0, 255), 2)

        return image, len(circles) if circles is not None else 0

if __name__ == "__main__":
    H_MIN1, S_MIN1, V_MIN1 = 0, 0, 0
    H_MAX1, S_MAX1, V_MAX1 = 180, 255, 255

    H_MIN2, S_MIN2, V_MIN2 = 0, 0, 0
    H_MAX2, S_MAX2, V_MAX2 = 180, 255, 255

    root = tk.Tk()
    app = BackgammonCounterApp(root)
    root.mainloop()
