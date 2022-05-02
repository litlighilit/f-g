from cnf import WIN_FIG_RATE_W,WIN_FIG_RATE_H,FIG_CAN_RATE_W,FIG_CAN_RATE_H
from tkapp import Application
from _func import get_mode

def main():
    get_mode()
    def locatewin():
        sc_w=root.winfo_screenwidth()
        sc_h=root.winfo_screenheight()
        w_w=WIN_FIG_RATE_W*sc_w
        w_h=WIN_FIG_RATE_H*sc_h
        s_w=(sc_w-w_w)/2
        s_h=(sc_h-w_h)/2
        return w_w,w_h,s_w,s_h
    def sizefig():
        width,height=winlocate[0:2]
        return FIG_CAN_RATE_W*width,FIG_CAN_RATE_H*height
    winlocate=locatewin()
    root.geometry('%dx%d+%d+%d'%(winlocate)) #root.geometry('600x800+400+0')
    root.configure(bg='#ababab')
    root.title('函数')
    figsize=sizefig()
    app = Application(master=root,size=figsize)
    app.df={}
    root.mainloop()
   
if __name__=="__main__":
    from tkinter import Tk
    root = Tk()
    main()