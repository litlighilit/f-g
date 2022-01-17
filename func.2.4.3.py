# edited by litlighilit in 2022/1/15  21:57
print('''函数输入(无论大小写)包括(反)三角函数(除正切)、幂函数(eg.y=3^x)、指数函数(eg.y=x^2)、对数函数(自然对数ln(x)、常用对数lg(x)及底数为base的对数(log_{base}(x)))
变量以x,y表示，函数格式:y=f(x);隐函数:x,y需同处等号左侧eg.x^2+y^2=1
区间;在(隐)函数定义后加",a<x<b"(a<=b,a,b为实数)，表示定义域由a到b，其后可再加",n<y<m"(n<=m,n,m为实数)表示值域由n到m（开）
若参数缺省，则输出默认值："(x ^ 2 + y ^ 2 - 1) ^ 3 - x ^ 2 y ^ 3=0,-2<x<2,-2<y<2",精度为100''')

from numpy import *
import matplotlib.pyplot as plt

m1=list('bcgkmrwy')
m2='-- - -. :'.split()
m3=list('.,ov^<>1234sp*hHd|_+x')
for i in m1,m2,m3:
    i.append('')
m0=[]
for i in m1:
    for j in m2:
        for z in m3:
            m0.append(f'{i}{j}{z}')
def gets():
    global s, ls, le,n,m
    ss = input("函数表达式(回车画图):")
    s=ss if ss!=' ' else '(x ^ 2 + y ^ 2 - 1) ^ 3 - x ^ 2 y ^ 3=0'  # ,-2<x<2,-2<y<2' 'x=cos(a),y=sin(a),0<a<4'
    if s == 'quit()': exec(s)
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
            m=ls[i]
            del ls[i]
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
    # ll=[]
    while pos != -1:
        # ll.append(pos)
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
    # lx, ly = rx.split("<"), ry.split("<")
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
    a = ls[2]
    for i in res1, res2:
        i = i.replace(a, "t")
    lt = ls[2].split('<')
    tn,tm=(eval(lt[0]),eval(lt[-1])) if len(lt)>=3 else (-2,2)
    t = linspace(tn, tm, n)
    for i in res1,res2:
        if 'x=' in i:
            i=i.replace('x=','')
            x=eval(i)
        elif 'y='in i:
            i=i.replace('y=','')
            y=eval(i)

    # exec(res1)
    # exec(res2)
    plt.plot(x, y, m, linewidth=1)



def fn():
    res0 = ls[0]
    res0 = ref(res0)
    rx = ls[1] if le >= 2 else '-2<x<2'

    
    lx = rx.split('<')

    if res0.startswith('y='):
        
        x = linspace(eval(lx[0]), eval(lx[2]), n)
        if NameError:
            print('请检查表达式')
        y = eval(res0[2:])
        plt.plot(x, y, m, linewidth=1)  # label='$'+res+'$',
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
        # plt.contourf(x, y, z, levels=[-1, 0])
        # plt.gca().set_aspect('equal')
        plt.contour(x, y, z, 0)

    # plt.figure(figsize=(20,20))
    # plt.autoscale(enable=True or False)
    if RuntimeWarning:
        print('请检查定义域')
    # if res[0:2]=='y=':plt.legend()


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