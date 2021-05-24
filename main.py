from GuiClass import Page

if __name__ == "__main__":
    app = Page()
    app.wm_geometry("410x310")
    app.resizable(False, False)
    app.mainloop()
