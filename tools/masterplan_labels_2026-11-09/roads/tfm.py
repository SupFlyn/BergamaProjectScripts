import json
T=json.load(open('/tmp/claude-0/w/osm2old.json'))
z=complex(*T['z']);S=2.64119;TX=1.0575;TY=14.956;DX,DY=236.734,5688.012
def to_plan(lon,lat):  # -> coordinates of today's 06:00 file
    x=(lon-T['lon0'])*T['kx'];y=-(lat-T['lat0'])*T['ky']
    c=complex(x-T['mp'][0],y-T['mp'][1])*z
    return (S*(c.real+T['mq'][0])+TX+DX,S*(c.imag+T['mq'][1])+TY+DY)
