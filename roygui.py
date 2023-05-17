# -*- coding: cp1251 -*-
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageTk, Image


def delete():
    output_text1.delete("0.0", tk.END)
    plt.cla()

#def update_image():
#    # Загружаем новое изображение
#    new_image = Image.open("graph.png")
#    new_photo = ImageTk.PhotoImage(new_image)
#
#    # Устанавливаем новое изображение в объект Label
#    label.config(image=new_photo)
#
#    # Обновляем ссылку на объект PhotoImage, чтобы изображение не было удалено сборщиком мусора
#    label.image = new_photo
def create():   # Инициализация
    global swarm
    global velocity
    global pbest_pos
    global pbest_value
    global gbest_pos
    global gbest_value
    global k
    global bounds
    global dim
    global mystat
    mystat = []
    #np.random.seed(int(seed_entry.get()))
    dim = int(mutant_entry.get())
    k_entry.delete(0, tk.END)
    k_entry.insert(0, 0)
    k = 0
    bounds = np.array([int(minn_entry.get()) * dim, int(maxx_entry.get()) * dim])
    swarm = np.random.uniform(bounds[0], bounds[1], (int(chromoval_entry.get()), dim))
    velocity = np.zeros((int(chromoval_entry.get()), dim))
    pbest_pos = swarm.copy()
    pbest_value = np.array([np.inf] * int(chromoval_entry.get()))
    gbest_pos = np.zeros(dim)
    gbest_value = np.inf

def fitness(x):
    return (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2

def PSO():
    # func - целевая функция
    # dim - размерность пространства решений
    # swarm_size - количество частиц в рое
    # max_iter - максимальное число итераций
    # bounds - границы пространства поиска
    create()
    global swarm
    global velocity
    global pbest_pos
    global pbest_value
    global gbest_pos
    global gbest_value
    global k
    global bounds
    global mystat
    gener_val = int(generations_var.get())
    chromo_val = int(chromoval_entry.get())
    k += gener_val
    k_entry.delete(0, tk.END)
    k_entry.insert(0, k)
    # Цикл по итерациям
    w = float(inercia_entry.get())
    c1 = c2 = float(speed_entry.get())
    for i in range(gener_val):
        # Вычисление значения функции для каждой частицы
        f = np.array([fitness(x) for x in swarm])

        # Обновление лучшей позиции для каждой частицы
        mask = f < pbest_value
        pbest_value[mask] = f[mask]
        pbest_pos[mask] = swarm[mask]

        # Обновление лучшей позиции для всего роя
        mask = pbest_value < gbest_value
        if np.any(mask):
            gbest_value = np.min(pbest_value)
            gbest_pos = pbest_pos[np.argmin(pbest_value)]
        if gbest_value <80 :
            mystat.append(gbest_value)
        # Обновление скорости и позиции каждой частицы
        #w = 0.7  # инерционный вес
        #c1 = c2 = 1.4  # коэффициенты ускорения
        r1 = np.random.rand(chromo_val, dim)
        r2 = np.random.rand(chromo_val, dim)
        velocity = w * velocity + c1 * r1 * (pbest_pos - swarm) + c2 * r2 * (gbest_pos - swarm)
        swarm = swarm + velocity

         # Обрезаем значения позиций частиц до границ пространства поиска
        swarm = np.clip(swarm, bounds[0], bounds[1])

        # Заменяем значения, находящиеся за границами, на соответствующие граничные значения
        swarm = np.where(swarm < bounds[0], bounds[0], swarm)
        swarm = np.where(swarm > bounds[1], bounds[1], swarm)

    #plt.plot(range(1, len(mystat) + 1), mystat)
    #plt.title("График зависимости точности от кол-ва поколений")
    #plt.xlabel("Номер поколения")
    #plt.ylabel("Минимальное значение для поколения")
    #plt.savefig("graph.png")
    #update_image()
    output_text2.delete(1.0, tk.END)
    output_text2.insert(tk.END, "Номер, Результат, Вектор расположения \n")
    for i in range(chromo_val):
        line = "{} , {}, {}".format(i,pbest_value[i].round(4), pbest_pos[i].round(4)) + "\n"
        output_text2.insert(tk.END, line)

    resx = "Minimum found: {}".format(gbest_pos.round(6))
    resy = "Minimum value: {}".format(gbest_value.round(6))
    output_text1.insert("1.0", resx + "\n")
    output_text1.insert("1.0", resy + "\n")
    output_text1.insert("1.0", "************************\n")
    print(gbest_pos.round(6), gbest_value.round(6))
    #return gbest_pos.round(6), gbest_value.round(6)

# Create the main window
root = tk.Tk()
root.title("Роевой алгоритм")

# Set the size of the window
root.geometry("1200x720")

# Create the left and right frames
left_frame = ttk.Frame(root, padding=10)
right_frame = ttk.LabelFrame(root, padding=10, text="Особь")

# Divide the main window into two equal parts
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Pack the left and right frames into the main window
left_frame.grid(row=0, column=0, sticky="nsew")
right_frame.grid(row=0, column=1, sticky="nsew")

# Create the child frames in the left frame
frame1 = ttk.LabelFrame(left_frame, padding=10, text="Параметры")
frame11 = ttk.LabelFrame(left_frame, padding=10, text="Количество шагов")
frame2 = ttk.LabelFrame(left_frame, padding=10, text="Управление")
frame3 = ttk.LabelFrame(left_frame, padding=10, text="Результаты")

# Pack the child frames into the left frame
frame1.pack(side="top", fill="x", padx=5, pady=5)
frame11.pack(side="top", fill="x", padx=5, pady=5)
frame2.pack(side="top", fill="x", padx=5, pady=5)
frame3.pack(side="top", fill="both", expand=True, padx=5, pady=5)

# Create the input widgets with captions in frame1
combo_label = ttk.Label(frame1, text="Функция")
combo = ttk.Combobox(frame1, width="40")
combo['value'] = ("(x[1] - x[0]**2)**2 + (1 - x[0])**2",)
combo.current(0)  # установите вариант по умолчанию

mutant_label = ttk.Label(frame1, text="Размерность")
mutant_entry = ttk.Spinbox(frame1, from_=0, to=10)
mutant_entry.insert(0, "2")
chromoval_label = ttk.Label(frame1, text="Кол-во Особей")
chromoval_entry = ttk.Spinbox(frame1, from_=0, to=10000)
chromoval_entry.insert(0, "50")
minn_label = ttk.Label(frame1, text="Левая граница области поиска")
minn_entry = ttk.Spinbox(frame1, from_=-10000, to=10000)
minn_entry.insert(0, "-50")
maxx_label = ttk.Label(frame1, text="Правая граница области поиска")
maxx_entry = ttk.Spinbox(frame1, from_=-10000, to=10000)
maxx_entry.insert(0, "50")
inercia_label = ttk.Label(frame1, text="Инерционный вес")
inercia_entry = ttk.Spinbox(frame1, from_=-100, to=100)
inercia_entry.insert(0, "0.7")
speed_label = ttk.Label(frame1, text="Коэффициент ускорения")
speed_entry = ttk.Spinbox(frame1, from_=-100, to=100)
speed_entry.insert(0, "1.4")
seed_label = ttk.Label(frame1, text="Seed")
seed_entry = ttk.Spinbox(frame1, from_=-100000, to=100000)
seed_entry.insert(0, "24567")

# Pack the input widgets with captions into frame1
combo_label.grid(row=0, column=0)
combo.grid(row=1, column=0)
mutant_label.grid(row=2, column=0, padx=0, pady=5)
mutant_entry.grid(row=2, column=1, padx=5, pady=5)

chromoval_label.grid(row=3, column=0, padx=0, pady=5)
chromoval_entry.grid(row=3, column=1, padx=5, pady=5)

minn_label.grid(row=4, column=0, padx=0, pady=5)
minn_entry.grid(row=4, column=1, padx=5, pady=5)

maxx_label.grid(row=5, column=0, padx=0, pady=5)
maxx_entry.grid(row=5, column=1, padx=5, pady=5)

inercia_label.grid(row=6, column=0, padx=0, pady=5)
inercia_entry.grid(row=6, column=1, padx=5, pady=5)

speed_label.grid(row=7, column=0, padx=0, pady=5)
speed_entry.grid(row=7, column=1, padx=5, pady=5)

seed_label.grid(row=8, column=0, padx=0, pady=5)
seed_entry.grid(row=8, column=1, padx=5, pady=5)
# Create the Radio buttons and the calculate button in frame11
generations_var = tk.IntVar()
spin = ttk.Spinbox(frame11, from_=10, to=1000, width=10, textvariable=generations_var)
radio_button0 = ttk.Radiobutton(frame11, text="1", variable=generations_var, value=1)
radio_button1 = ttk.Radiobutton(frame11, text="10", variable=generations_var, value=10)
radio_button2 = ttk.Radiobutton(frame11, text="100", variable=generations_var, value=100)
radio_button3 = ttk.Radiobutton(frame11, text="500", variable=generations_var, value=500)
# Pack the Radio buttons and the calculate button into frame11
radio_button0.grid(row=0, column=0, padx=1, pady=5)
radio_button1.grid(row=0, column=1, padx=1, pady=5)
radio_button2.grid(row=0, column=2, padx=1, pady=5)
radio_button3.grid(row=0, column=3, padx=1, pady=5)
spin.grid(row=0, column=4, padx=5, pady=5)

# frame2
k = 0
create_button = ttk.Button(frame2, text="Создать особей с начальными данными", command=create)
calculate_button = ttk.Button(frame2, text="Посчитать все шаги", command=PSO)
k_label = ttk.Label(frame2, text="Шагов прошло:")
k_entry = ttk.Entry(frame2)
create_button.grid(row=2, column=0, padx=5, pady=5)
calculate_button.grid(row=2, column=1, padx=5, pady=5)
k_label.grid(row=3, column=0, padx=5, pady=5)
k_entry.grid(row=3, column=1, padx=5, pady=5)
output_text1 = ScrolledText(frame3, width=20, height=8)
output_text1.pack(side="top", fill="both", expand=True)
delbutton = ttk.Button(frame3, text="Очистить", command=delete)
delbutton.pack(side="bottom", fill="x")
# Create the text output widget in frame3
output_text2 = ScrolledText(right_frame, width=50, height=40)
output_text2.pack()

#image = Image.open("graph.png")
#photo = ImageTk.PhotoImage(image)
#label = tk.Label(right_frame, image=photo)
#label.pack()
#
################
dim = 2
bounds = np.array([int(minn_entry.get()) * dim, int(maxx_entry.get()) * dim])
swarm = np.empty((int(chromoval_entry.get()), dim))
velocity = np.empty((int(chromoval_entry.get()), dim))
pbest_pos = swarm.copy()
pbest_value = np.array([np.inf] * int(chromoval_entry.get()))
gbest_pos = np.zeros(dim)
gbest_value = np.inf
generations_var.set(1)
mystat = []
################


root.mainloop()
