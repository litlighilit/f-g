NOTE='''
from tools._replace:
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

def test(s):
    ws=' '.join(
        filter(lambda x:not x.isspace(),s)
    )
    ns=(replace2abs(
        replace2mul(s)
        )
    )
    nws=(replace2abs(
        replace2mul(ws)
        )
    )
    print(s)
    print(s.replace(" ",'')==ws.replace(" ",''))
    print(ns,nws,ns==nws,sep="\n")
if __name__=="__main__":
    s="|x+1|+|x|+3 |2 x+1|+5 |x+2 |x+1||""\
 5 (x+1)+x |x (3+x)|"
    s="x+2 |x+1| 5 (x+1)"
    test(s)
