import tkinter as tk
from tkinter import messagebox
import CoinExtractor
from Machine import Machine
from Tickets import Tickets
import os


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
        button1 = tk.Button(self,
                            text="Przejdź do wyboru i zakupu biletu",
                            relief=tk.GROOVE,
                            command=lambda: controller.show_frame("Page2"))
        button1.pack()


class Page2(tk.Frame):
    opr = {"+": (lambda x, y: x + y),
           "-": (lambda x, y: x - y)}

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.ticket = Tickets()
        self.coinExtractor = CoinExtractor.CoinExtractor()
        self.parent = parent
        self.machine = Machine()
        label = tk.Label(self, text="Prosze wybrać bilet:")
        label.pack(side="top")
        lb = tk.Label(self, text='', justify=tk.LEFT)
        lb['text'] = '\n\n'.join('{}\t  cena:\t{}zl'.format(k, d) for k, d in Tickets.ticket.items())
        lb.pack(side="left")
        counter_labels = self.createCounterLabels()
        self.createButtons('+', 0.6, counter_labels)
        self.createButtons('-', 0.8, counter_labels)
        pay_button = tk.Button(self,
                               text="Przejdz do platnosci",
                               relief=tk.RAISED,
                               command=lambda: [self.takeValueFromLablesAndCalculate(counter_labels),
                                                self.openPayWindow()])
        pay_button.place(relx=0.6, rely=0.9)

    def takeValueFromLablesAndCalculate(self, counter_labels):
        i = 0
        for tic in Tickets.ticket:
            value = counter_labels[i].cget("text")
            if value != 0:
                counter_labels[i].configure(text="0")
                self.machine.calculateAllChosenTicketsPrice(tic, value)
            i += 1

    def createCounterLabels(self):
        # TODO: doprowadz do tego:
        # TODO: return  [tk.Label(self, text='0').place(relx=0.7, rely=0.22 + i / 9.3) for i in range(0,len(Tickets.ticket))]

        labels_list = []
        counter = 0
        for i in range(len(Tickets.ticket)):
            labels_list.append(tk.Label(self, text=counter))
            labels_list[i].place(relx=0.7, rely=0.22 + i / 9.3)
        return labels_list

    def changeValueOnLabel(self, i, value):  # uzyc do buttonow
        return lambda: i.configure(
            text=str(self.opr[value](int(i.cget("text")), 1)) if int(i.cget("text")) - 1 >= 0 else i.configure(text=1))

    def createButtons(self, value, relx, labels):
        return [tk.Button(self,
                          text=value,
                          command=self.changeValueOnLabel(labels[i], value)).place(relx=relx, rely=0.22 + i / 9.3)for i in range(0, len(Tickets.ticket))]

    def openPayWindow(self):
        pay_window = tk.Toplevel()
        pay_window.resizable(False, False)
        moneys_list = self.coinExtractor.getMoneyList()
        var = tk.IntVar()
        var.set(int(self.machine.getMoneySum()))
        leftToPay_label = tk.Label(pay_window)
        leftToPay_label.configure(text="Do zapłaty: " + str(self.machine.getMoneySum()))
        leftToPay_label.pack(side=tk.TOP)
        tk.Button(pay_window, text="Zakończ transakcje", command=self.endMessageBox).pack(side=tk.BOTTOM)
        tk.Label(pay_window, text="Ilość monet:").pack(side=tk.TOP)
        var = tk.IntVar()
        self.coinsAmount_spinbox = tk.Spinbox(pay_window, from_=1, to=1000, width=10, bd=6, textvariable=var)
        # TODO:::::
        spinboxValue = var.get()
        if not isinstance(spinboxValue, int):
            print(type(var.get()))  # TODO
        elif spinboxValue < 0:
            print('xxxx')
            pass
        for money in moneys_list:
            tk.Button(pay_window,
                      text=str(money),
                      command=lambda button_money = money: self.a(leftToPay_label, button_money)).pack(side=tk.LEFT)

        self.coinsAmount_spinbox.pack(
            side=tk.TOP)
        # TODO:Dynamicznie sprawdzac wartosc tego !!!! nie moze byc <0 i musi byc int

    # TODO: ogolnie to sie ladnie zmienia ale nie liczy do konca poprawnie
    def a(self, i, money):
        i.configure(text="Do zaplaty:" + str(self.machine.substraction(
            money * int(self.coinsAmount_spinbox.get()))))  # money jest zle!!!! caly czas 50!!!! jak to naprawic???

    def endMessageBox(self):
        res = messagebox.askquestion("exit", "Czy chcesz zakończyć?")
        if res == 'yes':
            self.quit()
