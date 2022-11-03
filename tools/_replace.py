from _replace2abs import replace2abs
_opchr=r'+-*/'
def replace2mul(s):
    l=s.split()
    ns=l[0]
    #") +"
    for i in range(1,len(l)):
        if nows:=l[i]: #if isn't Empty-String

            before_=l[i-1][-1]
            if nows=='|':
                if (before_.isalnum() and
                    i+1!=len(l) and
                 l[i+1][0].isalnum() #handle ones like "+ |"
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


            if all([before_ == ')' or before_.isalnum(),(
                _after == '(' or _after.isalnum()
            )]):
                ns+='*'+nows
            else:ns+=nows

    return ns


 
if __name__=="__main__":
    s="|x+1|+|x|+3 |2 x+1|+5 |x+2 |x+1||""\
    5 (x+1)+x |x (3+x)|"
    ws=' '.join(filter(lambda x:not x.isspace(),s)
    )
    ns=(replace2abs(
        replace2mul(s)
        )
    )
    nws=(replace2abs(
        replace2mul(ws)
        )
    )
    print(s.replace(" ",'')==ws.replace(" ",''))
    print(ns,nws,ns==nws,sep="\n")