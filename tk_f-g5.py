from numpy import *
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus']=False
NOTE='''
from replace2mul:
!!!Note:
due to the lack of time,
replace2mul can't handle ones like "| x" , temporarily
'''
print(NOTE)

_opchr=r'+-*/'
def replace2mul(s):

    l=s.split()
    ns=l[0]
    for i in range(1,len(l)):
        if nows:=l[i]: #if isn't Empty-String
            before_=l[i-1][-1]
            if nows=='|':
                if (before_.isalnum() and #handle ones like "+ |"
                    i+1!=len(l) and
                 l[i+1][0].isalnum()
                ):
                    ns+='*'+nows
                else: #handle ones like "x | )"
                    ns+=nows
                continue
            if nows=='(': #handle ones like "x | ( x"
                ns+='*'+nows
                continue
            

            
            _after=nows[0]
            if before_=='|':
                try:before_=l[i-1][-2]
                except IndexError:pass
            if _after=='|':
                _after=nows[1]

            if (          #handle ones like ") +"
                (before_ == ')' or before_.isalnum()
                ) and (
                (_after == '(' or _after.isalnum())
                )
            ):
            # if all([before_ == ')' or before_.isalnum(),(  # handle ones like ") +"
            #     _after == '(' or _after.isalnum()
            # )]):
                ns+='*'+nows
            else:ns+=nows

    return ns


def replace2abs(s):

    ns='abs(' if s[0]=='|' else s[0]
    for i in range(1,len(s)-1):
        ss,es=s[i-1],s[i+1]
        if s[i]=='|':
            if (es==')' or es in '|)'+_opchr
            ) and ss.isalnum():
                ns+=')'
            elif ss in '=)'+_opchr and (
                es in '(|' or es.isalnum()
            ):
                ns+='abs('
        else:ns+=s[i]
    ns+=')' if s[-1]=='|' else s[-1]
    return ns

def rmtan90(exp,y,x,*,rel_tol=0.1,abs_tol=0.0):
    ntan=exp.find('tan(')
    if ntan!=-1:
        intan=set()
        def findintan(s,n):
            n0=n=n+4
            nn=1
            while all([n<len(s),nn!=0]):
                ss=s[n]
                if ss=='(':nn+=1
                elif ss==')':nn-=1
                n+=1
            nns=s[n0:n-1]
            intan.add(nns)
            n1=nns.find('tan(')
            if n1!=-1:findintan(nns,n1)
        findintan(exp,ntan)
        from math import isclose,cos,nan
        for i in range(len(x)):
            for e in intan:
                if isclose(cos(eval(e,{'x':x[i]})),0.0,rel_tol=rel_tol,abs_tol=abs_tol):
                    y[i]=nan
                    break
        del intan

DPI=100

WIN_FIG_RATE_W=0.6
WIN_FIG_RATE_H=0.9

FIG_CAN_RATE_W=0.8
FIG_CAN_RATE_H=0.75

def get_mode():
    global m0
    m1=list('bcgkmrwy')
    m2='-- - -. :'.split()
    m3=list('.,ov^<>1234sp*hHd|_+x')
    for i in m1,m2,m3:
        i.append('')
    m0=[]
    for i in m1:
        for j in m2:
            for z in m3:
                m0.append(i+j+z)

def gets(st):
    global s, ls, le,n,mode,sf
    #ss = input("函数表达式(回车画图):")
    s=st if not st.isspace() else '(x ^ 2 + y ^ 2 - 1) ^ 3 - x ^ 2 y ^ 3=0' 
    if s == ('quit()' or 'exit()'): exec(s)
    ls = s.lower().split(',')
    on,om=True,True
    i = 0
    while i <=len(ls)-1:
        if 'n=' in ls[i]:
            n=eval(ls.pop(i).replace('n=',''))
            on=False
            i-=1
        if ls[i] in m0:
            mode=ls.pop(i)
            om=False
            i-=1
        i+=1
    if on:n=100
    if om:mode='b-'
    sf=','.join(ls)
    le = len(ls)


def ref(res):
    global d1
    d1 = '^', 'lg', 'ln(', 'log_{', '}('
    d2 = '**', 'log10', 'log(', 'flog(', ','
    dic = dict(zip(d1, d2))
    for i in dic:
        res = res.replace(i, dic[i])

    res = replace2mul(res)
    res = replace2abs(res)
    return res


def flog(base, x):
    y = log(x) / log(base)
    return y


def fp():
    res1 = ls[0]
    res1 = ref(res1)
    res2 = ls[1]
    res2 = ref(res2)
    ar = ls[2].replace('=','')
    ar=ref(ar)
    lt = ar.split('<')
    if len(lt)==3:
        tn,tm=eval(lt.pop(0)),eval(lt.pop(-1))
    else:
        tn,tm= (-2,2)
    exec(f'{lt[0]} = linspace(tn, tm, n)')
    exec(res1)
    exec(res2)
    f,=app.au.plot(eval('x'), eval('y'), mode, linewidth=1,picker=1)
    app.df[str(f)]=sf



def fn():
    res0 = ls[0]
    res0 = ref(res0)
    rx = ls[1] if le >= 2 else '-2<x<2'
    rx=ref(rx)
    lx = rx.split('<')
    if res0.startswith('y='):
        x = linspace(eval(lx[0]), eval(lx[2]), n)
        '''if NameError:
            app.text.insert(0.0,'请检查表达式')'''
        y = eval(res0[2:])
        # if 'tan'in res0:
        #     y[:-1][diff(y) < 0] = nan
        f,=app.au.plot(x, y, mode, linewidth=1,picker=True) 
        app.df[str(f)]=sf
    else:
        x = linspace(eval(lx[0]), eval(lx[-1]), n)
        ry = ls[2] if le >= 3 else '-2<y<2'
        ly = ry.split('<')
        y = linspace(eval(ly[0]), eval(ly[-1]), n)
        x, y = meshgrid(x, y)
        lres = res0.split('=')
        lres[-1] = '({})'.format(lres[-1])
        res0 = '-'.join(lres)
        '''if NameError:
            app.text.insert(0.0,'请检查表达式')'''
        z = eval(res0)
        for i in app.au.contour(x, y, z, 0).collections:
            print(i)
            i.set_picker(2)
            app.df[str(i)]=sf
            
        
    '''if RuntimeWarning:
        app.text.insert(0.0,'请检查定义域')'''

def fshow():
    #app.canvas.title('func')
    app.au.axis('equal')
    app.canvas.draw() 

def fmain0(ao):
    gets(ao)
    if (le >= 3): 
        if (ls[0].startswith('x=') and ls[1].startswith('y='))or(ls[1].startswith('x=') and ls[0].startswith('y=')):
            fp()
    else:
        fn()

def fmain():
    lf=app.s1.get().split(';')
    if len(lf)!=0 and lf[0]!='':
        for i in lf:
            fmain0(i)
        app.s1.set('')
        fshow()


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib.backend_bases import key_press_handler #由于输入框占据了按键，快捷键无效


from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askstring
from tkinter.ttk import Separator


def color_cg(event):
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
    app.canvas.draw()

def style_cg(event):
    this=event.artist
    def l_cg(w):
        plt.setp(this,linestyle=w)
        app.canvas.draw()
        s1.set(this.get_linestyle())
    def m_cg(w):
        plt.setp(this,marker=w)
        app.canvas.draw()
        s2.set(this.get_marker())
    sw=Tk()
    sw.title(this)
    f1=Frame(sw)
    s1=StringVar(sw)
    s1.set(this.get_linestyle())
    b1=Menubutton(f1,text='change linestyle', relief=RAISED)
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
        b2=Menubutton(f2,text='change marker:', relief=RAISED)
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

def rmf(event):
    this=event.artist
    sf=app.df[str(this)]
    for key in list(app.df.keys()):
        if app.df[key]==sf:
            del app.df[key]
    this.remove()
    #del app.df[str(this)]
    app.canvas.draw()
    app.menu.destroy()
    
    
class Application(Frame):

    def __init__(self, master,size):
        super().__init__(master)
        self.size=size
        self.pack()
        self.creatmat()
        self.creatWidget()
        
    def rightmenu(self,a=None):
        self.menu = Menu(self.master,tearoff=0)
        #for i in vars(a.artist):print(i)           
        if a:
            exp=app.df[str(a.artist)]
            g=lambda:(self.master.clipboard_clear(),self.master.clipboard_append(exp))
            self.menu.add_command(label=exp,foreground="grey",command=g)
            self.menu.add_command(label="set color",command=lambda:color_cg(a))
            self.menu.add_command(label="set style",command=lambda:style_cg(a))
            self.menu.add_separator()
            self.menu.add_command(label="remove",command=lambda:rmf(a))

        def do_popup(event):
            try:
                self.menu.post(event.x_root, event.y_root+6)
            except:pass # avoid error after "remove"
        root.bind("<Button-3>", do_popup)       
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
        self.canvas._tkcanvas.pack(side=TOP,fill=BOTH,expand=YES)
        self.canvas.mpl_connect('pick_event',self.rightmenu)
        NavigationToolbar2Tk(self.canvas, self) #self.canvas.toolbar
        def to_exec0(event):
            menu=Menu(root)
            def to_exec():
                s=askstring('指令','输入')
                exec(s)
            menu.add_command(label='cmd>python',command=to_exec)
            menu.post(event.x_root, event.y_root+6)
        root.bind('<Control-1>',to_exec0)




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
    global app
    figsize=sizefig()
    app = Application(master=root,size=figsize)
    app.df={}
    root.mainloop()
   
if __name__=="__main__":
    root = Tk()
    main()