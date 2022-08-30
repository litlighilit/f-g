from func import *
# class InterEntry:
#     def get(self)->str:...
class InterfaceApp:
    #s1=InterEntry
    def __init__(self,fig) -> None:
        self.fig=fig
        self.au=fig.add_subplot(111)
        self.df={}
    def plot(x,y,mode,linewidth=1,picker=True):
        pass
def fmain(app,inp):
    #app.s1.get()
    get_mode()
    inp=inp.replace('\r\n',';')
    lf=inp.split(';')
    if len(lf)!=0 and lf[0]!='':
        for i in lf:
            if i.strip():fmain0(i,app)
        #app.s1.set('')
        #fshow(app)
    return True
import matplotlib.pyplot as plt
import io
"""

    exec(fn+f"({app},{arg})")

"""
def imain(input):
    
    app=InterfaceApp(plt.figure(figsize=(6, 6), dpi=300))
    fmain(app,input)

    fig=eval("app.fig")
    f = io.BytesIO()
    plt.savefig(f, dpi=fig.dpi)
    plt.close() #释放内存，不然内存会一直增加
    return f.getvalue()