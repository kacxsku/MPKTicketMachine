from GuiClass import Page

if __name__ == "__main__":
    '''starting main loop and setting frame dimensions'''
    app = Page()
    app.wm_geometry("410x310")
    app.resizable(False, False)
    app.mainloop()
