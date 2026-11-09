"""Build Code.gs from Code.template.gs by inlining the button images."""
import base64, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
enc = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
s = open('Code.template.gs').read()
for k, f in {'__BTN_ADD_SMALL__': 'btn_add_small.png', '__BTN_ATT_SMALL__': 'btn_att_small.png', '__BTN_WEEK_SMALL__': 'btn_week_small.png',
             '__BTN_ADD__': 'btn_add.png', '__BTN_ATT__': 'btn_att.png'}.items():
    s = s.replace(k, enc(f))
open('Code.gs', 'w').write(s)
