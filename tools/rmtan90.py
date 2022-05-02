
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
        
if __name__=='__main__':
    from numpy import linspace,tan,pi
    
    x=linspace(0,pi,3)
    print(x)
    s='tan(1+x)'
    y=eval(s)
    print(y)
    rmtan90(s,x,y)
    print(y)
