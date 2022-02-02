from tkinter import StringVar
from numpy import *
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus']=False
def get_mode():
    global m0,m1,m2,m3
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
    global s, ls, le,n,om,mode
    #ss = input("函数表达式(回车画图):")
    s=st if not st.isspace() else '(x ^ 2 + y ^ 2 - 1) ^ 3 - x ^ 2 y ^ 3=0'  
    if s == ('quit()' or 'exit()'): exec(s)
    ls = s.lower().split(',')
    on,om=0,0
    i = 0
    while i <=len(ls)-1:
        if 'n=' in ls[i]:
            n=eval(ls.pop(i).replace('n=',''))
            on=1
            i-=1
        elif ls[i].startswith("#"):
            global hcolor
            hm=ls.pop(i)
            om=2
            if len(hm)==7:hcolor=hm
            else:
                if hm[8:] in m0:
                    hcolor,mode=hm[:8],hm[8:]
            i-=1
        elif ls[i] in m0:
            mode=ls.pop(i)
            om=1
            i-=1
        i+=1
    if not on:n=100
    if not om:mode='-'
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
    d1 = '^', 'lg',   'ln(', 'log_{', '}('
    d2 = '**','log10','log(','flog(', ','
    d = dict(zip(d1, d2))
    for i in d:
        res = res.replace(i, d[i])

    l = list(res)
    for i in range(1, len(l) - 1):
        if (l[i] == " ") and ((l[i - 1].isnumeric()) or 97 <= ord(l[i - 1]) <= 122 or l[i-1]=='(') and (
                (l[i + 1].isnumeric()) or 97 <= ord(l[i + 1]) <= 122 or l[i+1]=='('):
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
    global iname
    exec(f"global {chr(iname)}\n{chr(iname)},=plt.plot(eval('x'),eval('y'),mode,c=hcolor,lw=1) if om==2 else plt.plot(eval('x'),eval('y'), mode, linewidth=1)")
    dic[chr(iname)]=eval(chr(iname)).get_xydata()
    iname+=1
    # if om==2:plt.plot(eval('x'),eval('y'),mode,c=hcolor,lw=1)
    # #else:plt.plot(locals()[res1[0]], locals()[res2[0]], mode, linewidth=1)
    # else:plt.plot(eval('x'), eval('y'), mode, linewidth=1)


def fn():
    res0 = ls[0]
    res0 = ref(res0)
    rx = ls[1] if le >= 2 else '-2<x<2'
    rx=ref(rx)
    lx = rx.split('<')
    global iname
    if res0.startswith('y='):
        x = linspace(eval(lx[0]), eval(lx[2]), n)
        if NameError:
            print('请检查表达式')
        y = eval(res0[2:])
        if 'tan'in res0:
            y[:-1][diff(y) < 0] = nan
        exec(f"global {chr(iname)}\n{chr(iname)},=plt.plot(x,y,mode,c=hcolor,lw=1) if om==2 else plt.plot(x, y, mode, linewidth=1)")
        #get_name('plt.plot(x,y,mode,c=hcolor,lw=1) if om==2 else plt.plot(x, y, mode, linewidth=1)')
        #print(locals())
        #f.writelines(str(i) for i in [chr(iname),':',eval(chr(iname)).get_xydata(),"\n"])
        dic[chr(iname)]=eval(chr(iname)).get_xydata()
        iname+=1
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
        if om==2:icolor,*type=hcolor,mode
        elif om==1:
            if len(mode)==1:
                icolor,*type=mode,'-'
            else:    
                icolor,*type=list(mode)
        else: icolor,*type='b',mode
        exec(f"global {chr(iname)}\n{chr(iname)}=plt.contour(x,y,z,0,colors=icolor,linestyles=type[0]) if om==2 else plt.contour(x, y,z,0, colors=icolor,linestyles=type[0])")
        
        l=concatenate([i.vertices for  i in eval(chr(iname)).collections[1].get_paths()])
        dic[chr(iname)]=l
        '''for c in eval('a').collections:
            data = c.get_paths()#.vertices.get_paths()[0].vertices
            print(c)
        for i in eval('a').collections[1].get_paths():
            i.vertices
        #print(m,len(m))
        print(eval('a').collections[0].get_paths(),'\n\n',eval('a').collections[1].get_paths())'''
        '''m=plt.contour(x, y, z, 0,colors=icolor,linestyles=type[0])
        print(m._contour_args([0],[0]))'''
        iname+=1
    if RuntimeWarning:
        print('请检查定义域')

def fshow():
    plt.title('func')
    plt.axis('equal')
    #plt.show()

def fmain(w):
    #print(type(s1.text()))
    gets(w#s1.text_disp.get_text()
         )
    if ls!=[] and not ls[0].isspace():
        if (le >= 3): 
            if (ls[0].startswith('x=') and ls[1].startswith('y='))or(ls[1].startswith('x=') and ls[0].startswith('y=')):
                fp()
        else:
            fn()
        fshow()
        # l=plt.ginput()
        # print(l)
        
        s1.set_val('')

iname=97
dic={}
'''def get_name(ob):
    global iname
    while iname<10:
        try:
            print("e")
            exec(f"nonlocal {eval(chr(iname))}")
            print('0')
            exec(f"[{eval(chr(iname))},off]={eval(ob)}")
            exec(f"nonlocals()[{chr(iname)}]={eval(ob)}")
            print('y')
            break
        except: 
            iname+=1
    print(iname)'''

import tkinter as tk
#f=open('varies.txt','w')
get_mode()
def ctk(ob):
    try:
        obj=eval(ob).collections
    except:
        obj=eval(ob)
    def fp_cgc(c):
        try:
            for  i in obj:
                i.set_color(c)
        except:
            obj.set_color(c)
        fig.canvas.draw()
        root.destroy()
    def fp_cgl(c):
        try:
            for  i in obj:
                i.set_linestyle(c)
        except:
            obj.set_linestyle(c)
        fig.canvas.draw()
        root.destroy()
    def fp_cgm(c):
        try:
            for  i in obj:
                i.set_marker(c) #inp func can't be changed
        except:
            obj.set_marker(c)
        fig.canvas.draw()
        root.destroy()
    root=tk.Tk()
    cs=StringVar(root)
    #cs.set(obj[0].get_color()[:-1])
    f1=tk.Frame(root)
    tk.Label(f1,text='change color').pack(side='left')
    tk.OptionMenu(f1,cs,*m1,command=fp_cgc).pack(side='right')
    f1.pack()
    f2=tk.Frame(root)
    tk.Label(f2,text='change linestyle').pack(side='left')
    tk.OptionMenu(f2,cs,*m2,command=fp_cgl).pack(side='right')
    f2.pack()
    f3=tk.Frame(root)
    tk.Label(f3,text='change marker').pack(side='left')
    tk.OptionMenu(f3,cs,*m3,command=fp_cgm).pack(side='right')
    f3.pack()
    root.mainloop()

from matplotlib.widgets import TextBox
from time import sleep
#color = "cornflowerblue"
fig=plt.figure(2,(9,7)
,facecolor='gray')
ax1=fig.add_axes([0.1,0,0.8,0.06])
s1=TextBox(ax1,'input')
fig.add_axes([0.10, 0.15, 0.75, 0.85])
s1.on_submit(fmain)

#s1.set_val('x^2-y^2=1')

# def on_mouse_move(event):
#     print('Event received:',event.xdate,event.ydate)
def onclick(event):
    # print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
    #       (event.button, event.x, event.y, event.xdata, event.ydata))
    #print('e',event.ind,event.artist.get_data)
    arr=array([event.xdata,event.ydata]) #in array([[-1,-1],[0,0]])
    test=0
    for i in dic:
        for j in dic[i]:
            if allclose(arr,j,1.e-1):
                if not test:
                    #print('here is',i)
                    ctk(i)
                test+=1
    sleep(0.2)
    text=0
    #plt.plot(event.xdata, event.ydata, ',')
    #fig.canvas.draw()

fig.canvas.mpl_connect('button_release_event', onclick)
#plt.connect('buttom_press_event',on_mouse_move)'button_release_event'
#plt.connect('motion_notify_event',on_mouse_move)
#plt.axis('equal')

plt.show()