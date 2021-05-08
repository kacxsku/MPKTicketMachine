import tkinter as tk
import CoinExtractor
from Tickets import Tickets
import os
from PIL import Image, ImageTk


class Page(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Page1, Page2):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Page1")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Witaj W automacie biletowym")
        label.pack(side="top", fill="both", expand=True)
        tk.Frame(self)
        dir_path = os.path.dirname(__file__)

        canvas = tk.Canvas(self, width=340, height=250)
        canvas.pack()
        self.img = tk.PhotoImage(file=dir_path + r"/assets/ticket.gif")
        canvas.create_image(10, 10, anchor=tk.NW, image=self.img)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("Page2"))

        button1.pack()


class Page2(tk.Frame):
    opr = {"+": (lambda x, y: x + y),
           "-": (lambda x, y: x - y)}

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Prosze wybrać bilet:")
        label.pack(side="top")
        lb = tk.Label(self, text='', justify=tk.LEFT)
        lb['text'] = '\n\n'.join('{}\t  cena:\t{}zl'.format(k, d) for k, d in Tickets.ticket.items())
        lb.pack(side="left")

        counter_labels = self.createCounterLabels()
        self.createButtons('+', 0.6, counter_labels)
        self.createButtons('-', 0.7, counter_labels)

        pay_button = tk.Button(self, text="Przejdz do platnosci", command=self.openPayWindow)
        pay_button.place(relx=0.6, rely=0.9)

    def openPayWindow(self):
        payWindow = tk.Toplevel()
        moneys_list = CoinExtractor.CoinExtractor.getMoneyList()
        tk.Label(payWindow, text="reszta:").pack(side=tk.TOP)
        tk.Button(payWindow, text="zakoncz transakcje").pack(side=tk.BOTTOM)
        for money in moneys_list:
            tk.Button(payWindow, text=str(money)).pack(side=tk.LEFT)

    def createCounterLabels(self):
        labels_list = []
        counter = 0
        for i in range(len(Tickets.ticket)):
            labels_list.append(tk.Label(self, text=counter))
            labels_list[i].place(relx=0.8, rely=0.22 + i / 9.3)
        return labels_list

    def changeValueOnLabel(self, i, value):
        return lambda: i.configure(
            text=str(self.opr[value](int(i.cget("text")), 1)) if int(i.cget("text")) - 1 >= 0 else i.configure(text=1))

    def calculateMoney(self):
        # suma pieniedzy
        valueLabel = tk.Label(self, text="do zaplaty: ")
        valueLabel.place(relx=0.4, rely=0.9)

    def createButtons(self, value, relx, labels):
        buttons_list = []
        for i in range(0, len(Tickets.ticket)):  # TODO:
            button = tk.Button(self, text=value)
            button.configure(command=self.changeValueOnLabel(labels[i], value))
            button.place(relx=relx, rely=0.22 + i / 9.3)
            buttons_list.append(button)
        return buttons_list


class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is page 3")
        label.pack(side="top", fill="both", expand=True)
        # ticket = Tickets()
        # var_material = tk.StringVar()
        # tickets_combobox = ttk.Combobox(self,text="bilet" ,
        #                                 values=list(ticket.twenty_minutes_ticket.keys()),
        #                                 justify="center",
        #                                 textvariable=var_material,
        #                                 state='readonly')
        # tickets_combobox.set('wybierz bilet')
        # label_selected = tk.Label(self, text="Not Selected")
        # tickets_combobox.bind('<<ComboboxSelected>>', lambda event: label_selected.config(text=ticket.twenty_minutes_ticket[var_material.get()]))
        # tickets_combobox.place(relx=0.3, rely=0.12, anchor='n')


if __name__ == "__main__":
    # root = tk.Tk()
    # main = Page(root)
    # main.pack(side="top", fill="both", expand=True)
    # root.wm_geometry("350x300")
    # root.mainloop()
    app = Page()
    app.wm_geometry("410x310")
    app.resizable(False,False)
    app.mainloop()
