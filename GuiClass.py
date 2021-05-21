import tkinter as tk
import CoinExtractor
import os
from tkinter import messagebox
from Machine import Machine
from Tickets import Tickets
from decimal import *

getcontext().prec = 3


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
                               #  state=tk.DISABLED, #TODO:MOZNA TAK ZROBIC!!!!!
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
        # TODO:
        #return [tk.Label(self, text='0').place(relx=0.7, rely=0.22 + i / 9.3) for i in range(0, len(Tickets.ticket))]

        labels_list = []
        for i in range(len(Tickets.ticket)):
            labels_list.append(tk.Label(self, text="0"))
            labels_list[i].place(relx=0.7, rely=0.22 + i/9.3)
        return labels_list

    def changeValueOnLabel(self, i, value):
        return lambda: i.configure(
            text=str(self.opr[value](int(i.cget("text")), 1)) if int(
                i.cget("text")) - 1 >= 0 else i.configure(text=1))

    def createButtons(self, value, relx, labels):
        return [tk.Button(self,
                          text=value,
                          command=self.changeValueOnLabel(labels[i], value)).place(relx=relx,rely=0.22 + i/9.3) for i in range(0, len(Tickets.ticket))]

    def openPayWindow(self):
        pay_window = tk.Toplevel()
        pay_window.resizable(False, False)
        moneys_list = self.coinExtractor.getMoneyList()
        var = tk.IntVar()
        var.set(int(self.machine.getMoneySum()))
        leftToPay_label = tk.Label(pay_window)
        leftToPay_label.configure(text="Do zapłaty: " + str(self.machine.getMoneySum()), font=("Arial", 20))
        leftToPay_label.grid(row=0, column=0)
        tk.Button(pay_window, text="Zakończ transakcje", command=self.endMessageBox).grid(row=8, column=8)
        tk.Label(pay_window, text="Ilość monet:", font=("Arial", 20)).grid(row=2, column=0)
        var = tk.IntVar()
        self.coinsAmount_spinbox = tk.Spinbox(pay_window, from_=1, to=1000, width=25, bd=6, textvariable=var)
        # TODO:::::
        spinboxValue = var.get()
        if not isinstance(spinboxValue, int):
            print(type(var.get()))  # TODO: obluzyc toooo
        elif spinboxValue < 0:
            print('xxxx')
        for money in range(len(moneys_list)):
            tk.Button(pay_window,
                      text=str(moneys_list[money]),
                      width=5,  ###ogolnie jest problem po zmianie na grid buttony nie sa rowne !!!!
                      command=lambda button_money=moneys_list[money]: (
                          self.calculateMoney(leftToPay_label, Decimal(str(button_money))),
                          self.machine.addMoneyToMachine(button_money))) \
                .grid(row=1, column=money, sticky="NWES")
        self.coinsAmount_spinbox.grid(row=2, column=4)
        # TODO:Dynamicznie sprawdzac wartosc tego !!!! nie moze byc <0 i musi byc int

    def calculateMoney(self, i, money):
        moneysToPay = Decimal(money*int(self.coinsAmount_spinbox.get()))
        subtractedMoneys = Decimal(self.machine.substraction(moneysToPay))
        if subtractedMoneys == 0:
            self.correctChangeMessageBox("Kupiłeś bilet za odliczoną kwotę")
        elif subtractedMoneys < 0:
            i.configure(text="Reszta:" + str(subtractedMoneys))
            change = self.machine.returnChange(-subtractedMoneys)
            if not change:
                self.cantGiveChangeMessageBox()
            else:
                print("Twoja reszta :" + str(change))
                self.correctChangeMessageBox("Twoja reszta :" + str(change))#TODO: dodac ladne wypisywanie reszty
        else:
            i.configure(text="Do zaplaty:" + str(Decimal(subtractedMoneys)))

    def endMessageBox(self):
        res = messagebox.askquestion("exit", "Czy chcesz zakończyć?")
        if res == 'yes':
            self.quit()

    def cantGiveChangeMessageBox(self):
        if messagebox.showwarning("showwarning", "Nie mogę wydać ci reszty\n Nie kupiłeś biletu") == "ok":
            self.quit()

#*args moze ????
    def correctChangeMessageBox(self, info):
        if messagebox.showinfo("showinfo", info ) == "ok":
            self.quit()
