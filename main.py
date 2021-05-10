import tkinter as tk
from tkinter import messagebox
import CoinExtractor
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
        button1 = tk.Button(self, text="Przejdź do wyboru i zakupu biletu", relief=tk.GROOVE,
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
        label = tk.Label(self, text="Prosze wybrać bilet:")
        label.pack(side="top")
        lb = tk.Label(self, text='', justify=tk.LEFT)
        lb['text'] = '\n\n'.join('{}\t  cena:\t{}zl'.format(k, d) for k, d in Tickets.ticket.items())
        lb.pack(side="left")
        counter_labels = self.createCounterLabels()
        self.createButtons('+', 0.6, counter_labels)
        self.createButtons('-', 0.8, counter_labels)
        pay_button = tk.Button(self, text="Przejdz do platnosci", relief=tk.RAISED, command=self.openPayWindow)#TODO: tutaj sume jakos licz i przekazuj do payWindow
        pay_button.place(relx=0.6, rely=0.9)

    # sciagac value z labela i jakos przekazywac do funkcji liczacej sume pewnie petla jakas

    def endMessageBox(self):
        res = messagebox.askquestion("exit", "Czy chcesz zakończyć?")
        if res == 'yes':
            self.quit()

    def openPayWindow(self):
        pay_window = tk.Toplevel()
        pay_window.resizable(False, False)
        moneys_list = CoinExtractor.CoinExtractor.getMoneyList()
        tk.Label(pay_window, text="Do zapłaty:"+str(0)).pack(side=tk.TOP)#self.coinExtractor.moneys_sum()#self.calculatePriceForAllTickets()
        tk.Button(pay_window, text="Zakończ transakcje", command=self.endMessageBox).pack(side=tk.BOTTOM)
        tk.Label(pay_window, text="Ilość monet:").pack(side=tk.TOP)
        var = tk.IntVar()
        #https://stackoverflow.com/questions/44563549/tkinter-how-to-prevent-users-entering-strings-into-spin-box
        #https://stackoverflow.com/questions/42729317/python-tkinter-spinbox-validate-fail
        #vcmd = (self.register(self.validate_spinbox), '%P')  validatecommand=vcmd
        moneys_count = tk.Spinbox(pay_window, from_=1, to=1000, width=10, bd=6, textvariable=var).pack(side=tk.TOP)###TODO:Dynamicznie sprawdzac wartosc tego !!!! nie moze byc <0 i musi byc int
        spinboxValue= var.get()
        if not isinstance(spinboxValue,int):
            print(type(var.get()))#TODO
        elif spinboxValue<0:
            print('xxxx')
            pass
        for money in moneys_list:
            tk.Button(pay_window, text=str(money), command=lambda m=money: self.addToCoinExtractor(m)).pack(side=tk.LEFT)


    def validate_spinbox(self, new_value):
        # Returning True allows the edit to happen, False prevents it.
        return new_value.isdigit()
##TODO:
    def calculatePriceForAllTickets(self,buttons,labels):
        price = 0
        for b,l in zip(buttons,labels):
            price+= self.ticket.getTicketPrice()
        return  price#self.ticket.getTicketPrice()#zbierz wartosc z przyciskow*cena biletu


    def addToCoinExtractor(self,money):#TODO: tak zeby dodawalo spinbox.get *moneta razy monete
        newMoney = CoinExtractor.Moneta(money)
        self.coinExtractor.add_coin(newMoney)

    def createCounterLabels(self):
        labels_list = []
        counter = 0
        for i in range(len(Tickets.ticket)):
            labels_list.append(tk.Label(self, text=counter))
            labels_list[i].place(relx=0.7, rely=0.22 + i / 9.3)
        return labels_list

    def changeValueOnLabel(self, i, value):
        return lambda: i.configure(
            text=str(self.opr[value](int(i.cget("text")), 1)) if int(i.cget("text")) - 1 >= 0 else i.configure(text=1))

    def createButtons(self, value, relx, labels):
        buttons_list = []
        for i in range(0, len(Tickets.ticket)):
            button = tk.Button(self, text=value)
            button.configure(command=self.changeValueOnLabel(labels[i], value))
            button.place(relx=relx, rely=0.22 + i / 9.3)
            buttons_list.append(button)
        return buttons_list


if __name__ == "__main__":
    app = Page()
    app.wm_geometry("410x310")
    app.resizable(False, False)
    app.mainloop()

# Dodaj message boxy
#pomysl o wrzucaniu pieniedzy jak to ma wygladac
# dodaj funkcjonalnosci
# podziel na moduly
# podziel na pakiety
