from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import os, subprocess, shutil, glob, time
from PIL import Image, ImageTk
from threading import Thread

class SRGUI():
    def __init__(self):
        self.root = Tk()

        self.input_img_path = StringVar()

        self.canvas = {}
        self.image = {}
        self.imagetk = {}
        self.id_canvas = {}
        self.label = {}

        self.default_diff = 20
        self.diff = self.default_diff

        ##### ENTREE
        self.frame_input = Frame(self.root)
        self.frame_input.grid(row=1, column=1, rowspan=2)

        Label(self.frame_input, text="Entrée", font=("Purisa", 18)).grid(row=1, column=1, columnspan=2)
        self.canvas["input"] = Canvas(self.frame_input, relief=SOLID, borderwidth=2, width=400, height=400)
        self.canvas["input"].grid(row=2, column=1, columnspan=2)
        Entry(self.frame_input, textvariable=self.input_img_path, width=60).grid(row=3, column=1, sticky="NEWS")

        Button(self.frame_input, text="...", relief=RIDGE, command=self.select_img).grid(row=3, column=2, sticky="NEWS")
        Button(self.frame_input, text="Calculer", relief=RIDGE, command=self.calcul).grid(row=4, column=1, columnspan=2, sticky="NEWS")

        def zoom(event):
            for type in ["input", "bil", "bic", "SRCNN", "SRGAN", "original"]:
                if type in self.id_canvas:
                    x1 = ((event.x - self.diff) * self.image[type].width) // 400
                    x2 = ((event.x + self.diff) * self.image[type].width) // 400
                    y1 = ((event.y - self.diff) * self.image[type].height) // 400
                    y2 = ((event.y + self.diff) * self.image[type].height) // 400

                    _img = self.image[type].crop((x1, y1, x2, y2))
                    self.imagetk[type] = ImageTk.PhotoImage(_img.resize((400, 400)))
                    self.canvas[type].itemconfig(self.id_canvas[type], image = self.imagetk[type])

        def change_diff(event):
            if event.delta > 0: self.diff -= 5
            else: self.diff += 5
            zoom(event)

        def reset(event):
            for type in ["input", "bil", "bic", "SRCNN", "SRGAN", "original"]:
                if type in self.id_canvas:
                    self.imagetk[type] = ImageTk.PhotoImage(self.image[type].resize((400, 400)))
                    self.canvas[type].itemconfig(self.id_canvas[type], image = self.imagetk[type])

        def activate_zoom(event):
            self.canvas["input"].bind("<Motion>", zoom)
        def desactivate_zoom(event):
            self.canvas["input"].unbind("<Motion>")

        self.canvas["input"].bind("<ButtonPress-1>", activate_zoom)
        self.canvas["input"].bind("<ButtonRelease-1>", desactivate_zoom)

        self.canvas["input"].bind("<Button-3>", reset)
        self.canvas["input"].bind("<MouseWheel>", change_diff)

        ##### BILINEAIRE
        self.frame_bil = Frame(self.root)
        self.frame_bil.grid(row=1, column=3)

        Label(self.frame_bil, text="Bilinéaire", font=("Purisa", 18)).grid(row=1, column=1)
        self.canvas["bil"] = Canvas(self.frame_bil, relief=SOLID, borderwidth=2, width=400, height=400)
        self.canvas["bil"].grid(row=2, column=1)

        self.label["bil"] = Label(self.frame_bil, fg="gray")
        self.label["bil"].grid(row=3, column=1)

        ##### BICUBIQUE
        self.frame_bic = Frame(self.root)
        self.frame_bic.grid(row=2, column=3)

        Label(self.frame_bic, text="Bicubique", font=("Purisa", 18)).grid(row=1, column=1)
        self.canvas["bic"] = Canvas(self.frame_bic, relief=SOLID, borderwidth=2, width=400, height=400)
        self.canvas["bic"].grid(row=2, column=1)

        self.label["bic"] = Label(self.frame_bic, fg="gray")
        self.label["bic"].grid(row=3, column=1)

        ##### SRCNN
        self.frame_SRCNN = Frame(self.root)
        self.frame_SRCNN.grid(row=1, column=4)

        Label(self.frame_SRCNN, text="SRCNN", font=("Purisa", 18)).grid(row=1, column=1)
        self.canvas["SRCNN"] = Canvas(self.frame_SRCNN, relief=SOLID, borderwidth=2, width=400, height=400)
        self.canvas["SRCNN"].grid(row=2, column=1)

        self.label["SRCNN"] = Label(self.frame_SRCNN, fg="gray")
        self.label["SRCNN"].grid(row=3, column=1)

        ##### SRGAN
        self.frame_SRGAN = Frame(self.root)
        self.frame_SRGAN.grid(row=2, column=4)

        Label(self.frame_SRGAN, text="SRGAN", font=("Purisa", 18)).grid(row=1, column=1)
        self.canvas["SRGAN"] = Canvas(self.frame_SRGAN, relief=SOLID, borderwidth=2, width=400, height=400)
        self.canvas["SRGAN"].grid(row=2, column=1)

        self.label["SRGAN"] = Label(self.frame_SRGAN, fg="gray")
        self.label["SRGAN"].grid(row=3, column=1)

        ##### ORIGINAL
        self.frame_original = Frame(self.root)

        Label(self.frame_original, text="Original", font=("Purisa", 18)).grid(row=1, column=1)
        self.canvas["original"] = Canvas(self.frame_original, relief=SOLID, borderwidth=2, width=400, height=400)
        self.canvas["original"].grid(row=2, column=1)


    def select_img(self):
        self.input_img_path.set(askopenfilename(filetypes = [('Images', '*.png *.jpg *.jpeg *.bmp *.gif')]))
        if os.path.exists(self.input_img_path.get()):
            self.image["input"] = Image.open(self.input_img_path.get())
            self.imagetk["input"] = ImageTk.PhotoImage(self.image["input"].resize((400, 400)))
            self.id_canvas["input"] = self.canvas["input"].create_image(204, 204, image = self.imagetk["input"])

            _l = self.input_img_path.get().split(".")
            _l[-2] += "_original"
            original_img_path = ".".join(_l)
            if os.path.exists(original_img_path):
                self.image["original"] = Image.open(original_img_path)
                self.imagetk["original"] = ImageTk.PhotoImage(self.image["original"].resize((400, 400)))
                self.id_canvas["original"] = self.canvas["original"].create_image(204, 204, image=self.imagetk["original"])

                self.frame_original.grid(row=1, column=5, rowspan=2)
            else: self.frame_original.grid_forget()


        else: showerror("Erreur", "Ce fichier n'existe pas.")

    def calcul(self):
        def thread_func():
            type2func = {"bil": self.Bilinear, "bic": self.Bicubic, "SRCNN": self.SRCNN, "SRGAN": self.SRGAN}
            for type in type2func:
                try:
                    t1 = time.time()
                    type2func[type]()
                    t2 = time.time()
                except: self.label["bil"].config(text="Erreur", fg="red")
                else: self.label["bil"].config(text="Temps de calcul : %0.2fs" % (t2 - t1), fg="gray")

        thfunc = Thread(target=thread_func)
        thfunc.setDaemon(True)
        thfunc.start()

    def Bilinear(self):
        self.image["bil"] = Image.open(self.input_img_path.get()).resize((400 * 4, 400 * 4), Image.BILINEAR)
        self.imagetk["bil"] = ImageTk.PhotoImage(self.image["bil"].resize((400, 400)))
        self.id_canvas["bil"] = self.canvas["bil"].create_image(204, 204, image=self.imagetk["bil"])

    def Bicubic(self):
        self.image["bic"] = Image.open(self.input_img_path.get()).resize((400 * 4, 400 * 4), Image.BICUBIC)
        self.imagetk["bic"] = ImageTk.PhotoImage(self.image["bic"].resize((400, 400)))
        self.id_canvas["bic"] = self.canvas["bic"].create_image(204, 204, image=self.imagetk["bic"])

    def SRCNN(self):
        SRCNN_img_path = "./SRCNN-pytorch-master/data/" + os.path.basename(self.input_img_path.get())
        self.image["input"].resize((self.image["input"].width * 4, self.image["input"].height * 4), Image.BICUBIC).save(SRCNN_img_path)

        subprocess.call(
        '"D:/ProgramData/Anaconda3/python.exe" \
        "./SRCNN-pytorch-master/test.py" \
        --weights-file "./SRCNN-pytorch-master/weights/srcnn_x4.pth" \
        --image-file "%s" \
        --scale 4' % SRCNN_img_path)

        l = SRCNN_img_path.split(".")
        l[-2] += "_srcnn_x4"
        self.SRCNN_img_path = ".".join(l)

        self.image["SRCNN"] = Image.open(self.SRCNN_img_path)
        self.imagetk["SRCNN"] = ImageTk.PhotoImage(self.image["SRCNN"].resize((400, 400)))
        self.id_canvas["SRCNN"] = self.canvas["SRCNN"].create_image(204, 204, image=self.imagetk["SRCNN"])

    def SRGAN(self):
        SRGAN_img_path = "./SRGAN-PyTorch-master/LR_imgs_dir/" + os.path.basename(self.input_img_path.get())
        shutil.copy(self.input_img_path.get(), SRGAN_img_path)

        workingdir = os.getcwd()
        os.chdir("./SRGAN-PyTorch-master/")

        subprocess.call(
        '"D:/ProgramData/Anaconda3/python.exe" \
        main.py \
        --mode test_only \
        --LR_path LR_imgs_dir/ \
        --generator_path model/SRGAN.pt"')

        os.chdir(workingdir)

        os.remove(SRGAN_img_path)

        self.SRGAN_img_path = glob.glob("./SRGAN-PyTorch-master/result/res_*.png")[-1]

        self.image["SRGAN"] = Image.open(self.SRGAN_img_path)
        self.imagetk["SRGAN"] = ImageTk.PhotoImage(self.image["SRGAN"].resize((400, 400)))
        self.id_canvas["SRGAN"] = self.canvas["SRGAN"].create_image(204, 204, image=self.imagetk["SRGAN"])

App = SRGUI()
mainloop()