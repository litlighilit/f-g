import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib.backend_bases import key_press_handler #由于输入框占据了按键，快捷键无效
from functools import partial

from tkinter import Tk,Frame,StringVar,Menubutton,Label,Menu,Entry,Button
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askstring
from tkinter.ttk import Separator

from cnf import DPI
from _func import fmain
#partial fmain


class Handler:
    def __init__(self,target):
        self.target=target
    def color_cg(self,event):
        this=event.artist
        l0=list('bcgkmrwy')
        l1='blue cyan green black magenta red white yellow'.split()
        dc=dict(zip(l0,l1))
        c=this.get_color()
        if len(c)==1:
            if type(c)==str:
                c=dc[c]
            else:
                c=tuple(round(i*255) for i in c[0][:3])
        elif type(c) is tuple:
            c=tuple(round(i*255) for i in c[:3])
        nc=askcolor(color=c)[-1] or c #'or c'防止askcolor->None时报错
        this.set_color(nc)
        self.target.canvas.draw()

    def style_cg(self,event):
        this=event.artist
        def l_cg(w):
            plt.setp(this,linestyle=w)
            self.target.canvas.draw()
            s1.set(this.get_linestyle())
        def m_cg(w):
            plt.setp(this,marker=w)
            self.target.canvas.draw()
            s2.set(this.get_marker())
        sw=Tk()
        sw.title(this)
        f1=Frame(sw)
        s1=StringVar(sw)
        s1.set(this.get_linestyle())
        b1=Menubutton(f1,text='change linestyle', relief="raised")
        Label(f1,textvariable=s1).pack(side='right')
        m="- -- -. : None".split()
        line_menu=Menu(b1,tearoff=False)
        def addl(o):
            line_menu.add_command(label=o,command=lambda:l_cg(o))
        for i in m:
            addl(i)
        b1.config(menu=line_menu)
        b1.pack(side='right')

        f2=Frame(sw)
        try:
            s2=StringVar(sw)
            s2.set(this.get_marker())
            b2=Menubutton(f2,text='change marker:', relief="raised")
            Label(f2,textvariable=s2).pack(side='right')
            mark_menu=Menu(b2,tearoff=False)
            mark=list(' .,ov^<>1234sp*hHDd|_+x')
            def addm(o):
                mark_menu.add_command(label=o,command=lambda:m_cg(o))
            for i in mark:
                addm(i)

            mark2_l=open('./src/c.txt',encoding='utf-8').read().split('\n')
            mark2_d,mark2=mark2_l[0].split(','),mark2_l[1].split(',')
            m2_menu=Menu(mark_menu)
            def addm2(o):
                m2_menu.add_command(label=mark2_d[o],command=lambda:m_cg(mark2[o]))
            for i in range(len(mark2_d)):
                addm2(i)
            mark_menu.add_cascade(label='Greek',menu=m2_menu)
            def entk():
                s=askstring('符号','输入')
                m_cg('$'+s+'$')

            mark_menu.add_command(label='exec',command=entk)

            b2.config(menu=mark_menu)
            b2.pack(side='right')
        except:
            Label(f2,text='no marker ').pack(side='left')
        f1.pack()
        Separator(sw,orient='horizontal').pack(fill='x')
        f2.pack()

    def rmf(self,event):
        this=event.artist
        sf=self.target.df[str(this)]
        for key in list(self.target.df.keys()):
            if self.target.df[key]==sf:
                del self.target.df[key]
        this.remove()
        #del app.df[str(this)]
        self.target.canvas.draw()
        self.target.menu.destroy()
    
    
class Application(Frame):

    def __init__(self, master,size):
        super().__init__(master)
        global fmain
        fmain=partial(fmain,self)
        self.size=size
        self.handler=Handler(self)
        self.pack()
        self.creatmat()
        self.creatWidget()
        
    def rightmenu(self,a=None):
        self.menu = Menu(self.master,tearoff=0)
        #for i in vars(a.artist):print(i)           
        if a:
            exp=self.df[str(a.artist)]
            g=lambda:(self.master.clipboard_clear(),self.master.clipboard_append(exp))
            self.menu.add_command(label=exp,foreground="grey",command=g)
            self.menu.add_command(label="set color",command=lambda:self.handler.color_cg(a))
            self.menu.add_command(label="set style",command=lambda:self.handler.style_cg(a))
            self.menu.add_separator()
            self.menu.add_command(label="remove",command=lambda:self.handler.rmf(a))

        def do_popup(event):
            try:
                self.menu.post(event.x_root, event.y_root+6)
            except:pass # avoid error after "remove"
        self.master.bind("<Button-3>", do_popup)       
    def creatWidget(self):
        self.label1 = Label(self,text='表达式')
        self.s1=StringVar()
        self.entry1 = Entry(self,textvariable=self.s1)
        self.entry1.bind('<Key-Return>',lambda x:fmain())
        self.label1.pack()
        self.entry1.pack()
        Button(self,text='绘图',command=fmain).pack()
    def creatmat(self):
        figsize=tuple(map(lambda x:x/DPI,self.size))
        self.fig =plt.Figure(figsize=figsize, dpi=DPI,
           facecolor='#0000006f'
           ,edgecolor='#99e5ff0f',linewidth=3)
        self.au = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas._tkcanvas.pack(side="top",fill="both",expand=True)
        self.canvas.mpl_connect('pick_event',self.rightmenu)
        NavigationToolbar2Tk(self.canvas, self) #self.canvas.toolbar
        def to_exec0(event):
            menu=Menu(self.master)
            def to_exec():
                s=askstring('指令','输入')
                exec(s)
            menu.add_command(label='cmd>python',command=to_exec)
            menu.post(event.x_root, event.y_root+6)
        self.master.bind('<Control-1>',to_exec0)
