import sys, zlib, struct
def png(path):
    d=open(path,'rb').read(); p=8; idat=b''; plte=None; trns=None
    while p<len(d):
        n=struct.unpack('>I',d[p:p+4])[0]; t=d[p+4:p+8]; c=d[p+8:p+8+n]; p+=12+n
        if t==b'IHDR': w,h,bd,ct=struct.unpack('>IIBB',c[:10])
        elif t==b'PLTE': plte=c
        elif t==b'tRNS': trns=c
        elif t==b'IDAT': idat+=c
    raw=zlib.decompress(idat); ch={0:1,2:3,3:1,4:2,6:4}[ct]; bpp=max(1,ch*bd//8); stride=(w*ch*bd+7)//8
    prev=bytearray(stride); i=0; px=[]
    for y in range(h):
        f=raw[i]; line=bytearray(raw[i+1:i+1+stride]); i+=1+stride
        for x in range(stride):
            a=line[x-bpp] if x>=bpp else 0; b=prev[x]; c=prev[x-bpp] if x>=bpp else 0
            if f==1: line[x]=(line[x]+a)&255
            elif f==2: line[x]=(line[x]+b)&255
            elif f==3: line[x]=(line[x]+(a+b)//2)&255
            elif f==4:
                pa,pb,pc=abs(b-c),abs(a-c),abs(a+b-2*c); pr=a if pa<=pb and pa<=pc else (b if pb<=pc else c); line[x]=(line[x]+pr)&255
        prev=line
        for x in range(w):
            if ct==3:
                k=line[x] if bd==8 else (line[x*bd//8]>>(8-bd-(x*bd)%8))&((1<<bd)-1)
                if trns is not None and k<len(trns) and trns[k]==0: continue
                px.append(tuple(plte[k*3:k*3+3]))
            elif ct in (2,6):
                if ct==6 and line[x*ch+3]==0: continue
                px.append(tuple(line[x*ch:x*ch+3]))
            else: px.append((line[x*ch],)*3)
    return px
for f in sys.argv[1:]:
    px=png(f); n=len(px); print(f.split('/')[-1], '#%02x%02x%02x'%tuple(round(sum(p[i] for p in px)/n) for i in range(3)))
