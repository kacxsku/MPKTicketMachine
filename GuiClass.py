import tkinter as tk
import CoinExtractor
import os
from tkinter import messagebox
from Machine import Machine
from Tickets import Tickets
from decimal import *
from exceptions import *

getcontext().prec = 3


class Page(tk.Tk):
    """Parent Page for other Pages"""
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
    """Ticket Machine Home page"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Witaj W automacie biletowym")
        label.pack(side="top", fill="both", expand=True)
        tk.Frame(self)
        # printing image in frame
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
    """frame for chosing tickets and operations on it"""
    #when operator is string
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
                               command=lambda: [self.takeValueFromLabelsAndCalculate(counter_labels),
                                                self.openPayWindow()])
        pay_button.place(relx=0.6, rely=0.9)

    def takeValueFromLabelsAndCalculate(self, counter_labels):
        """take value from label and calculate moneys"""
        i = 0
        for tic in Tickets.ticket:
            value = counter_labels[i].cget("text")
            if value != 0:
                counter_labels[i].configure(text="0")
                self.machine.calculateAllChosenTicketsPrice(tic, value)
            i += 1

    def createCounterLabels(self):
        '''creating labels with tickets amount'''
        labels_list = []
        for i in range(len(Tickets.ticket)):
            labels_list.append(tk.Label(self, text="0"))
            labels_list[i].place(relx=0.7, rely=0.22 + i/9.3)
        return labels_list

    def changeValueOnLabel(self, i, value):
        '''change value on counter label'''
        return lambda: i.configure(
            text=str(self.opr[value](int(i.cget("text")), 1)) if int(
                i.cget("text")) - 1 >= 0 else i.configure(text=1))

    def createButtons(self, value, relx, labels):
        '''create buttons for changing tickets count'''
        return [tk.Button(self,
                          text=value,
                          command=self.changeValueOnLabel(labels[i], value)).place(relx=relx, rely=0.22 + i/9.3) for i in range(0, len(Tickets.ticket))]

    def openPayWindow(self):
        '''create pay window and operations on coins'''
        pay_window = tk.Toplevel()
        pay_window.resizable(False, False)
        moneys_list = self.coinExtractor.getMoneyList()
        var = tk.IntVar()
        var.set(int(self.machine.getMoneySum()))
        leftToPay_label = tk.Label(pay_window)
        leftToPay_label.configure(text="Do zapłaty: " + str(self.machine.getMoneySum()), font=("Arial", 20))
        leftToPay_label.grid(row=0, column=0, columnspan=4)
        tk.Button(pay_window, text="Zakończ transakcje", command=self.endMessageBox).grid(row=8, column=10,columnspan=2)
        tk.Label(pay_window, text="Ilość monet:", font=("Arial", 12)).grid(row=2, column=1,columnspan=4)
        var = tk.IntVar()
        self.coinsAmount_spinbox = tk.Spinbox(pay_window, from_=1, to=1000, width=20, bd=6, textvariable=var)
        for money in range(len(moneys_list)):
            tk.Button(pay_window,
                      text=str(moneys_list[money]),
                      width=5,
                      command=lambda button_money=moneys_list[money]: (
                          self.fromSpinboxMoney(button_money),
                          self.calculateMoney(leftToPay_label, Decimal(str(button_money)),pay_window))) \
                .grid(row=1, column=money, columnspan=1, sticky="NWES")
        self.coinsAmount_spinbox.grid(row=2, column=4, columnspan=3)
        self.machine.setRecenlty()


    def fromSpinboxMoney(self, button_money):
        '''checking if exception was thrown and printing proper messagebox, else adding moneys to machine'''
        spinboxValue = self.coinsAmount_spinbox.get()
        try:
            self.machine.checkValue(spinboxValue)
        except NegativeNumberValueError:
            messagebox.showerror("showerror", "Liczba pieniędzy musi być dodatnia")
            self.quit()
        except NotIntValueError:
            messagebox.showerror("showerror", "Liczba pieniędzy musi być całkowita")
            self.quit()
        else:
            for _ in range(int(spinboxValue)):
                self.machine.addMoneyToMachine(button_money)

    def calculateMoney(self, i, money,top):
        '''calculate moneys to pay, and printing propert messagebox'''
        moneysToPay = Decimal(money*int(self.coinsAmount_spinbox.get()))
        subtractedMoneys = Decimal(self.machine.substraction(moneysToPay))
        change_info = self.machine.returnChange(-subtractedMoneys)
        if subtractedMoneys == 0:
            self.correctChangeMessageBox(change_info,top,i)
        elif subtractedMoneys < 0:
            i.configure(text="Reszta:" + str(subtractedMoneys))
            self.correctChangeMessageBox(change_info,top,i)
        else:
            i.configure(text="Do zaplaty:" + str(Decimal(subtractedMoneys)))

    def endMessageBox(self):
        '''showing exit messagebox'''
        res = messagebox.askquestion("exit", "Czy chcesz zakończyć?")
        if res == 'yes':
            self.quit()

    def correctChangeMessageBox(self, info,top,i):
        '''showing change message box'''
        if messagebox.showinfo("showinfo", info) == "ok":
            top.destroy()
            top.update()
            self.machine.setTotalCost(0)



