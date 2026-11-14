import sys
def linea_c(v,t):
 x=(v+' '+t).upper()
 ar=('LATTAFA','ARMAF','AFNAN','AL HARAMAIN','RASASI','SWISS ARABIAN','ORIENTICA','MAISON ALHAMBRA','FRAGRANCE WORLD','PARIS CORNER','GULF ORCHID','REYANE TRADITION','ARD AL ZAAFARAN','ZIMAYA','KAAF','BHARARA','DUMONT','KHADLAJ')
 if any(a in x for a in ar):return 'ARABE'
 ni=('CREED','PARFUMS DE MARLY','MANCERA','MONTALE','XERJOFF','NISHANE','BYREDO','LE LABO','MAISON FRANCIS KURKDJIAN','TOM FORD','AMOUAGE','INITIO','TIZIANA TERENZI','KILIAN','ROJA','BOND NO 9','MEMO PARIS','SOSPIRO')
 if any(n in x for n in ni):return 'NICHO'
 return 'DISENADOR'
def calc(k,lin,ven,plf):
 k,v=int(round(k)),ven.upper()
 if lin=='ARABE':m,p=m5c(k+100),m5c(k+395)
 elif lin=='NICHO':m=m5c(k+200);ps=m5c(k+495);p=m5c(plf-10) if plf>ps else ps
 else:
  m=m5c(k+50) if(k<700 and('ADIDAS'in v or 'CUBA'in v))else(m5c(k+75) if(k<700 and any(z in v for z in('ANTONIO BANDERAS','NAUTICA','BENETTON','PERRY ELLIS','GUESS','PARIS HILTON')))else m5c(k+150))
  ps=m5c(k+395);p=m5c(plf-10) if plf>ps else ps
 return p,m5a(k+((p-k)*0.5)),m
def main():
 modo=sys.argv.pop(1) if len(sys.argv)>1 else 'escanear'
 a,d=open('datos.js',encoding='utf-8').read().split('=',1)
 items=json.loads(d.strip().rstrip(';'))
 if modo=='aplicar':
  if not(os.path.exists('aprobados.json') and os.path.exists('pendientes.json')):return
  apr=json.load(open('aprobados.json',encoding='utf-8'))
  pend=json.load(open('pendientes.json',encoding='utf-8'))
  sids,ped=set(str(x) for x in apr.get('ids',list())),apr.get('precios',dict())
  mp=dict((str(i.get('id','')),i) for i in items)
  mx=max((int(i.get('id',0)) for i in items if str(i.get('id','')).isdigit()),default=0)
  for c in pend.get('cambios',list()):
   cid=str(c.get('id',''))
   if cid not in sids:continue
   tp=c.get('tipo','')
   if tp=='NUEVO':
    mx+=1;pf=int(ped.get(cid,c.get('p_sug',0)));kf=int(c.get('k_nuevo',0))
    items.append({'id':mx,'n':c.get('n',''),'c':c.get('c',''),'l':c.get('l','DISENADOR'),'i':c.get('i',''),'k':kf,'p':pf,'s':m5a(kf+((pf-kf)*0.5)),'m':int(c.get('m_sug',0)),'a':0,'w':1,'o':0})
   elif cid in mp:
    it=mp.get(cid)
    if tp=='DISP':it.update({'a':int(c.get('a_nuevo',0))})
    elif tp in('SUBIO','BAJO','OFERTA'):
     kf=int(c.get('k_nuevo',it.get('k',0)));pf=int(ped.get(cid,c.get('p_sug',it.get('p',0))));sf=m5a(kf+((pf-kf)*0.5));mf=int(c.get('m_sug',it.get('m',0)))
     it.update({'k':kf,'p':pf,'s':sf,'m':mf,'av':0})
     if tp=='OFERTA':it.update({'o':1,'d':max(0,int(c.get('p_ant',pf))-pf),'ds':max(0,int(c.get('s_ant',sf))-sf),'dm':max(0,int(c.get('m_ant',mf))-mf),'df':int(c.get('rebaja_lafe',0))})
  open('datos.js','w',encoding='utf-8').write(a+'='+json.dumps(items,ensure_ascii=False,separators=(',',':'))+';\n')
  pend.update({'cambios':list(c for c in pend.get('cambios',list()) if str(c.get('id','')) not in sids)})
  json.dump(pend,open('pendientes.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
  return
 vivo=dict()
 for pr in lafe():
  tit,ven,ptp=pr.get('title',''),pr.get('vendor',''),pr.get('product_type','')
  tg=','.join(pr.get('tags',list())) if isinstance(pr.get('tags'),list) else str(pr.get('tags',''))
  if relleno(tit,ptp,tg):continue
  imgs=pr.get('images',list());imu=imgs.pop(0).get('src','') if imgs else ''
  for v in pr.get('variants',list()):
   vt=v.get('title','');fn=tit if(not vt or vt=='Default Title')else(tit+' - '+vt)
   if relleno(fn,ptp,tg):continue
   pc,cp=float(v.get('price') or 0),float(v.get('compare_at_price') or 0)
   if pc<=100:continue
   of=cp>pc;vivo.update({norm(fn):{'n':fn.upper(),'c':ven.upper(),'i':imu,'k':int(round(pc if of else pc/1.25)),'p_lafe':int(round(cp if of else pc)),'oferta':of,'a':0 if v.get('available',True) else 1}})
 cmb,ex=list(),set()
 for it in items:
  cl=norm(it.get('n',''));ex.add(cl)
  if cl not in vivo:continue
  lv=vivo.get(cl);iid,ka,kn=str(it.get('id','')),int(it.get('k',0)),int(lv.get('k',0));lin=it.get('l',linea_c(it.get('c',''),it.get('n','')))
  if int(it.get('a',0))!=int(lv.get('a',0)):cmb.append({'id':iid,'tipo':'DISP','n':it.get('n',''),'c':it.get('c',''),'l':lin,'i':it.get('i',''),'a_nuevo':int(lv.get('a',0)),'detalle':'Agotado en La Fe' if lv.get('a')==1 else 'Disponible de nuevo'})
  if ka>0 and kn>0:
   df=kn-ka
   if abs(df)/float(ka)>0.40:continue
   if df>=20:
    ps,ss,ms=calc(kn,lin,it.get('c',''),lv.get('p_lafe',0))
    cmb.append({'id':iid,'tipo':'SUBIO','n':it.get('n',''),'c':it.get('c',''),'l':lin,'i':it.get('i',''),'k_ant':ka,'k_nuevo':kn,'diff':df,'p_ant':it.get('p',0),'p_sug':ps,'s_sug':ss,'m_sug':ms})
   elif df<=-20:
    pa,rb=int(it.get('p',0)),abs(df);pof=150 if pa>=1600 else 100
    if lv.get('oferta') and rb>=pof:
     d50=m5c(rb*0.5)
     cmb.append({'id':iid,'tipo':'OFERTA','n':it.get('n',''),'c':it.get('c',''),'l':lin,'i':it.get('i',''),'k_ant':ka,'k_nuevo':kn,'diff':df,'rebaja_lafe':rb,'p_ant':pa,'s_ant':it.get('s',0),'m_ant':it.get('m',0),'p_sug':max(kn+100,pa-d50),'s_sug':max(kn+50,int(it.get('s',0))-d50),'m_sug':max(kn+25,int(it.get('m',0))-d50)})
    else:
     ps,ss,ms=calc(kn,lin,it.get('c',''),lv.get('p_lafe',0))
     cmb.append({'id':iid,'tipo':'BAJO','n':it.get('n',''),'c':it.get('c',''),'l':lin,'i':it.get('i',''),'k_ant':ka,'k_nuevo':kn,'diff':df,'p_ant':pa,'p_sug':ps,'s_sug':ss,'m_sug':ms})
 ix=1
 for cl,lv in vivo.items():
  if cl in ex or lv.get('a')==1:continue
  lin=linea_c(lv.get('c',''),lv.get('n',''));ps,ss,ms=calc(lv.get('k',0),lin,lv.get('c',''),lv.get('p_lafe',0))
  cmb.append({'id':'NEW_'+str(ix),'tipo':'NUEVO','n':lv.get('n',''),'c':lv.get('c',''),'l':lin,'i':lv.get('i',''),'k_nuevo':lv.get('k',0),'p_lafe':lv.get('p_lafe',0),'p_sug':ps,'s_sug':ss,'m_sug':ms});ix+=1
 json.dump({'fecha':os.popen('date -u +%Y-%m-%dT%H:%M:%SZ').read().strip(),'cambios':cmb},open('pendientes.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
if __name__=='__main__':main()
