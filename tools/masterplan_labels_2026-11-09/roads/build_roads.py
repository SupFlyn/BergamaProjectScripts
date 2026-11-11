# Layer 8 (roads + paths) and layer 9 (corrections) for Aras's 9 Nov 09:00 masterplan (B19_setB_layers2_0600.svg).
# Coordinates = that file's own units (viewBox 0 0 8372.233 10968.204), so Paste in Place lands on it.
import json,copy,html,sys,os
from lxml import etree
D=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,D)
from tfm import to_plan
P=etree.XMLParser(huge_tree=True);NS='http://www.w3.org/2000/svg';E_=html.escape
SRC=D+'/../../inputs/B19_setB_layers2_0600.svg'
OLD='/mnt/project-files/library/examples/liked_2026-11-05/previews/v13_1/illustrator/B19_setB_layers.svg'
OUT=D+'/../../roads_v1/'
S=2.64119;OLDTF='matrix(%g 0 0 %g %g %g)'%(S,S,1.0575+236.734,14.956+5688.012)   # v13.1 sheet mm -> today's file
HEAD='<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="295.354cm" height="386.934cm" viewBox="0 0 8372.233 10968.204">\n'
FT='font-family="Arial, ArialMT"'
F={i:(k,t,p) for k,i,t,p in json.load(open(D+'/feat.json'))}
def pl(i): return [to_plan(*q) for q in F[i][2]]
def pts(P): return ' '.join('%.1f,%.1f'%q for q in P)
def gid(s): return ''.join(c if c.isalnum() or c in '-_' else '_' for c in s.replace(' ','_'))
# ---------- layer 8: roads + paths ----------
his=etree.parse(SRC,P);roads=his.xpath('//*[@id="roads_streets"]')[0]
els=[e for e in roads.iter() if isinstance(e.tag,str) and e.tag.split('}')[1] in('path','polygon','polyline','line','rect')]
CL={c['i']:c for c in json.load(open(D+'/his_cls.json'))}
STY={'main_roads':('#C9C3B8','#8F887D'),'streets':('#DCD7CE','#A39C91'),'paths_steps':('#EADFCC','#B49F7E')}
groups={k:{} for k in STY}
for n,e in enumerate(els):
    c=CL[n];e=copy.deepcopy(e)
    for a in ('clip-path','class','opacity'): e.attrib.pop(a,None)
    fill,stk=STY[c['cls']]
    if e.get('fill')=='none': e.set('stroke',stk); e.set('stroke-width',e.get('stroke-width') or '.5')
    else:
        e.set('fill',fill)
        if e.get('stroke') not in(None,'none'): e.set('stroke',stk)
    nm=c['name'] or 'unnamed'
    groups[c['cls']].setdefault(nm,[]).append(etree.tostring(e,encoding='unicode').replace(' xmlns="%s"'%NS,''))
o=[HEAD,'<g id="ROADS_PATHS_around_the_site">\n<g id="roads_and_paths_in_your_plan">\n']
for k in ('main_roads','streets','paths_steps'):
    o.append('<g id="%s">'%k)
    for nm,lst in sorted(groups[k].items()): o.append('<g id="%s_%s">%s</g>'%(k[:4],gid(nm),''.join(lst)))
    o.append('</g>\n')
o.append('</g>\n')
# OSM roads/paths that are not in his plan (checked by overlap: <50 % of the OSM line within ~3 m of a drawn road, inside his drawn street net)
R=json.load(open(D+'/osm_res.json'))
PATH={'footway','steps','pedestrian','path','track','cycleway'};MAIN={'trunk','primary','secondary'}
LOW=['371130187','1350426789','371130159']   # Bergama - Kozak Yolu (2 parts) + Cami Kebir Caddesi: the lower-edge road
miss=[r for r in R if r['cov']<0.5 and r['near']>0.7 and r['i'] not in LOW and r['i']!='50470038']
CK='#C0392B'
def dline(r):
    h=r['h'];w=1.2 if h in PATH else 3.0 if h in MAIN else 2.0;da='3 3' if h in PATH else '10 6'
    s='<polyline points="%s" fill="none" stroke="%s" stroke-width="%g" stroke-dasharray="%s" stroke-linecap="round"/>'%(pts(pl(r['i'])),CK if h not in PATH else '#8A5A2B',w,da)
    return '<g id="osm_%s_%s_%s">%s</g>'%(r['i'],h,gid(r['name'] or 'unnamed'),s)
for zone,lab in ((True,'inside_the_site_zone_under_your_design'),(False,'around_the_site')):
    sel=[r for r in miss if (r['inz']>0.5)==zone]
    o.append('<g id="CHECK_in_OpenStreetMap_not_in_your_plan_%s">'%lab)
    o.append('<g id="roads">%s</g>'%''.join(dline(r) for r in sel if r['h'] not in PATH))
    o.append('<g id="paths_steps">%s</g></g>\n'%''.join(dline(r) for r in sel if r['h'] in PATH))
# his lower-edge road: OSM + 2023 satellite centre line where it is ~14 m off
o.append('<g id="CHECK_lower_edge_road_true_centre_Bergama_Kozak_Yolu_Cami_Kebir_Caddesi">')
for w in LOW:
    o.append('<polyline points="%s" fill="none" stroke="#C2306E" stroke-width="3" stroke-dasharray="10 6"/>'%pts(pl(w)))
o.append('<text x="1240" y="6805" %s font-size="11" fill="#C2306E" font-weight="bold">real road centre (OSM + 2023 satellite)</text></g>\n'%FT)
o.append('</g>\n</svg>\n')
import re as _re
_seen={}
def _u(m):
    v=m.group(1);n=_seen.get(v,0);_seen[v]=n+1
    return 'id="%s"'%(v if n==0 else '%s_%d'%(v,n+1))
open(OUT+'layer_8_roads_paths.svg','w').write(_re.sub(r'id="([^"]+)"',_u,''.join(o)))
print('layer 8:',{k:sum(len(v) for v in g.values()) for k,g in groups.items()},'missing osm',len(miss))
# ---------- layer 9: corrections ----------
old=etree.parse(OLD,P)
def oldpieces(gidn,idx,fill,stroke,sw='0.35'):
    g=old.xpath('//*[@id=$i]',i=gidn)[0]
    E=[e for e in g.iter() if isinstance(e.tag,str) and e.tag.split('}')[1] in('path','polygon','rect','polyline')]
    out=[]
    for n in idx:
        e=copy.deepcopy(E[n])
        for a in ('clip-path','class','opacity'): e.attrib.pop(a,None)
        if e.get('fill')!='none': e.set('fill',fill)
        e.set('stroke',stroke);e.set('stroke-width',sw)
        out.append(etree.tostring(e,encoding='unicode').replace(' xmlns="%s"'%NS,''))
    return '<g transform="%s">%s</g>'%(OLDTF,''.join(out))
C=dict(her='#8E2B36',ex='#5A6670')
def callout(num,name,sub,col,ax,ay,bx,by,idn):
    T=13.0;U=8.4;w=max(len(name)*T*0.6,len(sub)*U*0.53)+30;h=34;x0,y0=bx,by-h
    ex=min(max(ax,x0),x0+w);ey=min(max(ay,y0),y0+h)
    g='<g id="%s">'%idn
    g+='<path d="M%.1f %.1fL%.1f %.1f" fill="none" stroke="%s" stroke-width="0.9"/>'%(ax,ay,ex,ey,col)
    g+='<circle cx="%.1f" cy="%.1f" r="4" fill="%s" stroke="#FFFFFF" stroke-width="1"/>'%(ax,ay,col)
    g+='<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#FFFFFF" stroke="%s" stroke-width="1"/>'%(x0,y0,w,h,col)
    g+='<circle cx="%.1f" cy="%.1f" r="8" fill="%s"/>'%(x0+12,y0+12,col)
    g+='<text x="%.1f" y="%.1f" %s font-size="%s" font-weight="bold" text-anchor="middle" fill="#FFFFFF">%s</text>'%(x0+12,y0+15.5,FT,'9' if len(num)>1 else '10',E_(num))
    g+='<text transform="translate(%.1f %.1f)" %s><tspan x="0" y="0" font-size="13" font-weight="bold" fill="%s">%s</tspan><tspan x="0" y="12" font-size="8.4" font-weight="normal" fill="#1E1E1E">%s</tspan></text>'%(x0+24,y0+16,FT,col,E_(name),E_(sub))
    return g+'</g>',(x0,y0,w,h)
o=[HEAD,'<g id="CORRECTIONS_9_Nov_kisla_bridges_askerlik">\n']
# existing bridges as surveyed (v13.1 survey-made decks): Adnan Menderes 0-3, Ilica 4-7, Sube Sokak 8-11 ; Tabak = context piece 1 ; Ulucami = pedestrian bridge 0-16
o.append('<g id="existing_bridges_as_surveyed">')
o.append('<g id="bridge_Adnan_Menderes_Bulvari">%s</g>'%oldpieces('road_bridge_carriageway_pavements',[0],'none','#3A3A3A','0.5'))
o.append('<g id="bridge_Ilica_Deresi_Koprusu">%s</g>'%oldpieces('road_bridge_carriageway_pavements',[4],'none','#3A3A3A','0.5'))
o.append('<g id="bridge_Sube_Sokak_road_bridge">%s</g>'%oldpieces('road_bridge_carriageway_pavements',[8],'none','#3A3A3A','0.5'))
o.append('<g id="bridge_Tabak_Koprusu">%s</g>'%oldpieces('bridge_outside_the_zone_context_v13_1',[1],'none','#3A3A3A','0.5'))
o.append('<g id="bridge_Ulucami_Koprusu">%s</g>'%oldpieces('pedestrian_bridge_no_car_road_beyond_it',[0],'none','#3A3A3A','0.5'))
uk=pl('370936583')
o.append('<g id="bridge_Uc_Kemer_Koprusu_OSM_centre_line_width_not_surveyed"><polyline points="%s" fill="none" stroke="#3A3A3A" stroke-width="2.2" stroke-dasharray="6 3"/></g>'%pts(uk))
o.append('</g>\n')
# buildings
o.append('<g id="existing_buildings_corrected">')
o.append('<g id="Eski_Kisla_Binasi_OSM_footprint"><polygon points="%s" fill="#E4877A" stroke="#8E918A" stroke-width="0.8"/></g>'%pts(pl('1085996474')[:-1]))
o.append('<g id="Harap_Camii_as_surveyed">%s</g>'%oldpieces('heritage_buildings_kept',[10],'#E4877A','#8E918A','0.3'))
o.append('<g id="Askerlik_Subesi_building_as_surveyed">%s</g>'%oldpieces('context_buildings',[9],'#B9BDC2','#5A6670','0.3'))
o.append('<g id="Askerlik_Subesi_compound_wall_OSM"><polyline points="%s" fill="none" stroke="#5A6670" stroke-width="1" stroke-dasharray="4 3"/></g>'%pts(pl('387226210')))
o.append('</g>\n')
# labels (positions: OSM / survey; boxes placed by hand, checked on a render)
L=[]
k=pl('1085996474');kx=sum(a for a,b in k[:-1])/len(k[:-1]);ky=sum(b for a,b in k[:-1])/len(k[:-1])
L.append(callout('28','Old Kışla','Eski Kışla Binası, historic',C['her'],kx,ky,kx-185,ky-38,'28_Old_Kisla'))
L.append(callout('13','Üç Kemer Bridge','historic bridge, kept (K5)',C['her'],(uk[0][0]+uk[-1][0])/2,(uk[0][1]+uk[-1][1])/2,3360,6625,'13_Uc_Kemer_Bridge'))
L.append(callout('12','Harap Camii','ruined mosque, kept',C['her'],3966,6633,3990,6610,'12_Harap_Camii'))
L.append(callout('29','Road Bridge','Şube Sokak, kept',C['her'],3927,6735,3955,6790,'29_Road_Bridge_Sube_Sokak'))
L.append(callout('30','Askerlik Şubesi','army office, existing',C['ex'],3871,6522,3700,6470,'30_Askerlik_Subesi'))
L.append(callout('9','Tabak Bridge','road bridge, kept',C['her'],2232,6541,2250,6500,'09_Tabak_Bridge'))
o.append('<g id="labels_corrected">%s</g>\n'%''.join(g for g,b in L))
o.append('</g>\n</svg>\n')
open(OUT+'layer_9_corrections.svg','w').write(''.join(o))
json.dump([b for g,b in L],open(D+'/label_boxes.json','w'))
print('layer 9 written')
