from PIL import Image

def negative_filter(img):
    negative_list = [(255-p[0], 255-p[1], 255-p[2])
                           for p in img.getdata()]

    img.putdata(negative_list)
    img.save('static/uploads/new.jpg')

def grayscale_filter(img):
    new_list = [((a[0]*299 + a[1]*587 + a[2]*114 )//1000,) * 3
                                      for a in img.getdata()]
                                    
    img.putdata(new_list)
    img.save('static/uploads/new.jpg')

def sepia(p):
   # tint shadows
   if p[0] < 63:
       r,g,b = int(p[0] * 1.1), p[1], int(p[2] * 0.9)

   # tint midtones
   elif p[0] > 62 and p[0] < 192:
       r,g,b = int(p[0] * 1.15), p[1], int(p[2] * 0.85)

   # tint highlights
   else:
       r = int(p[0] * 1.08)
       g,b = p[1], int(p[2] * 0.5)

   return r, g, b


def sepia_filter(img):
    img_list = [(p[0], p[1], p[2])
                           for p in img.getdata()]
    
    new_list = []
    for pixels in img_list:
        new_list.append(sepia(pixels))

    img.putdata(new_list)
    img.save('static/uploads/new.jpg')

def thumbnail_filter(my_src):
    #my_src = Image.open(img)
    w,h = my_src.width, my_src.height
    my_trgt = Image.new('RGB', (w,h))

    target_x = 0
    for source_x in range(0, w, 2):
        target_y = 0
        for source_y in range(0, h, 2):
            p = my_src.getpixel((source_x, source_y))
            my_trgt.putpixel((target_x, target_y), p)
            target_y += 1
        target_x += 1

    my_trgt.save('static/uploads/new.jpg')