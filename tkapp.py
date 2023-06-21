import matplotlib.collections
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib.backend_bases import key_press_handler # here hotkeys handlers are somehow useless
from functools import partial

from tkinter import Tk,Frame,StringVar,Menubutton,Label,Menu,Entry,Button
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askstring
from tkinter.ttk import Separator

from _func import fmain
#will later partial fmain


class Handler:
    def __init__(self,target,res={}):
        self.target=target
        self.res=res
    def color_cg(self,event):
        this=event.artist
        l0=list('bcgkmrwy')
        l1='blue cyan green black magenta red white yellow'.split()
        dc=dict(zip(l0,l1))
        c=this.get_color()
        if len(c)==1:
            if isinstance(c, str):
                c=dc[c]
            else:
                c=tuple(round(i*255) for i in c[0][:3])
        elif isinstance(c, tuple):
            c=tuple(round(i*255) for i in c[:3])
        nc=askcolor(color=c)[-1] or c # without 'or c', when askcolor returns `None`, there'll be an error
        this.set_color(nc)
        self.target.canvas.draw()

    def style_cg(self,event):
        # TODO:
        #  * for `sw` use a toplevel instead of Tk 
        #  * move some to a new `init_style_menu`to cache
        this=event.artist
        if isinstance(this,
            matplotlib.collections.PathCollection): return # PathCollection doesn't have `get_marker`...
        def l_cg(w):
            plt.setp(this,linestyle=w)
            self.target.canvas.draw()
            s1.set(w)
        def m_cg(w):
            plt.setp(this,marker=w)
            self.target.canvas.draw()
            s2.set(w)
        sw=Tk()
        sw.title(this)
        f1=Frame(sw)
        s1=StringVar(sw)
        s1.set(this.get_linestyle())
        b1=Menubutton(f1,text='change linestyle', relief="raised")
        Label(f1,textvariable=s1).pack(side='right')
        m="- -- -. : None".split()
        line_menu=Menu(b1,tearoff=False)
        def add_l(l):
            line_menu.add_command(label=l,command=lambda:l_cg(l))
        for i in m:
            add_l(i) # capture i
        b1.config(menu=line_menu)
        b1.pack(side='right')

        f2=Frame(sw)
        s2=StringVar(sw)
        s2.set(this.get_marker())
        b2=Menubutton(f2,text='change marker:', relief="raised")
        Label(f2,textvariable=s2).pack(side='right')
        mark_menu=Menu(b2,tearoff=False)
        mark=' .,ov^<>1234sp*hHDd|_+x'
        def add_m(m):
            mark_menu.add_command(label=m,command=lambda:m_cg(m))
        for i in mark:
            add_m(i) # capture i
        m2_menu=Menu(mark_menu)

        ext_marker_res = self.res.get('marker', None)
        if ext_marker_res:
            with open(ext_marker_res,encoding='utf-8') as f:
                mark2_d, mark2 = map(
                    lambda c: c.split(','), 
                    f.read().split('\n'))
                for i,c in enumerate(mark2_d):
                    m2_menu.add_command(label=c,command=lambda:m_cg(mark2[i]))
                mark_menu.add_cascade(label='ext',menu=m2_menu)
        
        def entk():
            s=askstring('','marker:')
            m_cg('$'+s+'$')

        mark_menu.add_command(label='exec',command=entk)

        b2.config(menu=mark_menu)
        b2.pack(side='right')
        '''
        else:
            Label(f2,text='no marker ').pack(side='left')'''
        
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

    def __init__(self, master,size, dpi=100, res={}):
        super().__init__(master)
        global fmain
        fmain=partial(fmain,self)
        self.size=size
        self.dpi=dpi
        self.handler=Handler(self,res)
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
        self.label1 = Label(self,text='expression ')
        self.s1=StringVar()
        self.entry1 = Entry(self,textvariable=self.s1)
        self.entry1.bind('<Key-Return>',lambda x:fmain())
        self.label1.pack()
        self.entry1.pack()
        Button(self,text='plot',command=fmain).pack()
    def creatmat(self):
        figsize=tuple(map(lambda x:x/self.dpi,self.size))
        self.fig =plt.Figure(figsize=figsize, dpi=self.dpi,
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
                pycmd=askstring('','pycmd:')
                exec(pycmd)
            menu.add_command(label='cmd>python',command=to_exec)
            menu.post(event.x_root, event.y_root+6)
        self.master.bind('<Control-1>',to_exec0)
