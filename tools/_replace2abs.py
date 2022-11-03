import re


preabs = re.compile(
        r"\|(?=[\w\(])"
        )
nexabs = re.compile(
        r"(?<=[\w\)])\|"
        )


#called after _replacemul
def replace2abs(s):
    assert re.search(r"[\w\(]\|[\w\(]",s)==None
    return preabs.sub('abs(',
                      nexabs.sub(')',
                                 s
                                 )
                      )


if __name__=="__main__":
    teststr="""
|3*x+1|*|5+x|+8
    """.strip()
    out=replace2abs(teststr)
    print(teststr,"->",out)
