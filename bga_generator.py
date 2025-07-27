from KicadModTree import *
from math import ceil


width = 12.6
height = 12.6
clearance = 0.4
pad_width = 0.25

footprint_name = "VFBGA-641_12.6x12.6mm"

kicad_mod = Footprint(footprint_name)
kicad_mod.setDescription(footprint_name)
kicad_mod.setTags("")


cols = int(width/clearance)
rows = int(height/clearance)

#example, can be empty.
pad_ignore_list = {
    "A" : [4, 7, 10, 13, 16, 19, 22, 25, 28],
    "C" : [1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25],
    "D" : [13, 16, 19, 22, 24, 31],
    "E" : [4, 5, 6, 7, 8, 10, 11, 13, 14, 16, 18, 19, 21, 22, 26, 29]
}

offset_x = width/2
offset_y = height/2

kicad_mod.append(RectLine(start=[-offset_x, -offset_y], end=[offset_x, offset_y], layer='F.SilkS'))

kicad_mod.append(RectLine(start=[-(offset_x+0.25), -(offset_y+0.25)], end=[(offset_x+0.25), (offset_y+0.25)], layer='F.CrtYd'))

for pad_x in range(rows):
    for pad_y in range(cols):
        pad_name = ''
        tmp = pad_x
        while True:
            pad_name = chr(ord('A') + (tmp % 26)) + pad_name
            tmp = tmp // 26 - 1
            if tmp < 0:
                break
            
        if pad_name in pad_ignore_list:
            if (pad_y + 1) in pad_ignore_list[pad_name]:
                continue
        
        pad_name += str(pad_y + 1)

        x = round(-int(offset_x) + (clearance * pad_x), 1)
        y = round(-int(offset_y) + (clearance * pad_y), 1)
        
        
        print(pad_name + ' ' + str(x) + ' ' + str(y) + ' ')
        
        kicad_mod.append(Pad(number=pad_name, type=Pad.TYPE_SMT, shape=Pad.SHAPE_CIRCLE,
                     at=[y, x], size=[pad_width, pad_width], layers=Pad.LAYERS_SMT))
    print('\n')

file_handler = KicadFileHandler(kicad_mod)
file_handler.writeFile(footprint_name + '.kicad_mod')
