from numpy import *
import matplotlib.pyplot as plt

#plt.figure(figsize=(6,6))
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

def gets():
    global s, ls, le,n,m
    #ss = input("函数表达式(回车画图):")
    s=s1.get() if not s1.get().isspace() else '(x ^ 2 + y ^ 2 - 1) ^ 3 - x ^ 2 y ^ 3=0'  
    if s == ('quit()' or 'exit()'): exec(s)
    ls = s.lower().split(',')
    on,om=True,True
    i = 0
    while i <=len(ls)-1:
        if 'n=' in ls[i]:
            n=eval(ls[i].replace('n=',''))
            del ls[i]
            on=False
            i-=1
        if ls[i] in m0:
            m=ls.pop(i)
            om=False
        i+=1
    if on:n=100
    if om:m='b-'
    le = len(ls)


def ref(res):
    global d1
    pos = res.find('|')
    lresl = list(res)
    o = True
    while pos != -1:
        lresl[pos] = 'abs(' if o else ')'
        o = not o
        pos = res.find('|', pos + 1)

    res = ''.join(lresl)
    d1 = '^', 'lg', 'ln(', 'log_{', '}('
    d2 = '**', 'log10', 'log(', 'flog(', ','
    d = dict(zip(d1, d2))
    for i in d:
        res = res.replace(i, d[i])

    l = list(res)
    for i in range(1, len(l) - 1):
        if (l[i] == " ") and ((l[i - 1].isnumeric()) or (97 <= ord(l[i - 1]) <= 122)) and (
                (l[i + 1].isnumeric()) or (97 <= ord(l[i + 1]) <= 122)):
            l[i] = "*"

    res = ""
    for a in l:
        res += a
    return res


def flog(base, x):
    y = log(x) / log(base)
    return y


def fp():
    res1 = ls[0]
    res1 = ref(res1)
    res2 = ls[1]
    res2 = ref(res2)
    a = ls[2].replace('=','')
    a=ref(a)
    lt = a.split('<')
    if len(lt)==3:
        tn,tm=eval(lt.pop(0)),eval(lt.pop(-1))
    else:
        tn,tm= (-2,2)
    t = linspace(tn, tm, n)
    for i in res1,res2:
        if 'x=' in i:
            i=i.replace('x=','')
            x=eval(i)
        elif 'y='in i:
            i=i.replace('y=','')
            y=eval(i)
    plt.plot(x, y, m, linewidth=1)



def fn():
    res0 = ls[0]
    res0 = ref(res0)
    rx = ls[1] if le >= 2 else '-2<x<2'
    rx=ref(rx)
    lx = rx.split('<')
    if res0.startswith('y='):
        try:
            x = linspace(eval(lx[0]), eval(lx[2]), n)
        except NameError:
            print('请检查表达式')
        y = eval(res0[2:])
        if 'tan'in res0:
            y[:-1][diff(y) < 0] = nan
        plt.plot(x, y, m, linewidth=1) 
    else:
        x = linspace(eval(lx[0]), eval(lx[-1]), n)
        ry = ls[2] if le >= 3 else '-2<y<2'
        ly = ry.split('<')
        y = linspace(eval(ly[0]), eval(ly[-1]), n)
        x, y = meshgrid(x, y)
        lres = res0.split('=')
        lres[-1] = '({})'.format(lres[-1])
        res0 = '-'.join(lres)
        if NameError:
            print('请检查表达式')
        z = eval(res0)
        plt.contour(x, y, z, 0)
    if RuntimeWarning:
        print('请检查定义域')

def fshow():
    plt.title('func')
    plt.axis('equal')
    plt.show()

'''def main():
    gets()
    if s!='':
        if (le >= 3): 
            if (ls[0].startswith('x=') and ls[1].startswith('y='))or(ls[1].startswith('x=') and ls[0].startswith('y=')):
                fp()
        else:
            fn()
    else:
        fshow()'''
def fmain():
    get_mode()
    gets()
    if (le >= 3): 
        if (ls[0].startswith('x=') and ls[1].startswith('y='))or(ls[1].startswith('x=') and ls[0].startswith('y=')):
            fp()
    else:
        fn()
    fshow()
    s1.set('')



from tkinter import *

class Application(Frame):
    '''经典GUI写法'''

    def __init__(self, master=None):
        super().__init__(master)
        self.master=master
        self.pack()
        self.creatWidget()

    def creatWidget(self):
        self.label1 = Label(self,text='表达式')
        global s1
        s1=StringVar()
        self.entry1 = Entry(self,textvariable=s1)
        self.btnd=Button(self,text='绘图',command=fmain)
        self.label1.pack()
        self.entry1.pack()
        #s1.set('(x ^ 2 + y ^ 2 - 1) ^ 3 - x ^ 2 y ^ 3=0')
        self.btnd.pack()

def main():
    root = Tk()
    root.geometry('400x300')
    root.title('函数')
    app = Application(master=root)

    root.mainloop()
    

main()