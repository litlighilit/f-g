# edited by litlighilit in 2022/1/17  21:57
print('''函数输入(无论大小写)包括(反)三角函数、幂函数(eg.y=3^x)、指数函数(eg.y=x^2)、对数函数(自然对数ln(x)、常用对数lg(x)及底数为base的对数(log_{base}(x)))
变量以x,y表示，函数格式:y=f(x);隐函数:eg.x^2+y^2=1;
参数方程(以t为参数):<x表达式>,<y表达式>,<t范围>
(x、y表达式顺序可调换,t范围:a<t<b"(a<=b,a,b为实数),可省略范围，仅写为:t,此时默认为-2到2)eg.y=1-cos(t),x=t-sin(t),t
区间:在(隐)函数定义后加",a<x<b"(a<=b,a,b为实数)，表示定义域由a到b，其后可再加",n<y<m"(n<=m,n,m为实数)表示值域由n到m
图像格式(参数方程/函数):<颜色><线型><点型> eg.b-.(同matplotlib格式)
若仅输入空格，则输出默认值:"(x ^ 2 + y ^ 2 - 1) ^ 3 - x ^ 2 y ^ 3=0,-2<x<2,-2<y<2",精度为100
回车画图''')

from numpy import *
import matplotlib.pyplot as plt

plt.figure(figsize=(6,6))
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
    ss = input("函数表达式(回车画图):")
    s=ss if not ss.isspace() else '(x ^ 2 + y ^ 2 - 1) ^ 3 - x ^ 2 y ^ 3=0'  # ,-2<x<2,-2<y<2' 'x=cos(a),y=sin(a),0<a<4'
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
        
        x = linspace(eval(lx[0]), eval(lx[2]), n)
        if NameError:
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


while True:
    gets()
    if s!='':
        if (le >= 3): 
            if (ls[0].startswith('x=') and ls[1].startswith('y='))or(ls[1].startswith('x=') and ls[0].startswith('y=')):
                fp()
        else:
            fn()
    else:
        plt.title('func')
        plt.axis('equal')
        plt.show()
