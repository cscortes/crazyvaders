from PIL import Image

fname = "stardust_missile"

im = Image.open(fname + ".png")

# im.thumbnail( (96,96) )
for idx, angle in enumerate(range(0,180,9*2)):
    print(idx,angle)
    t = im.rotate(angle)
    t.save("../images/explosion/{}_{:02d}.png".format(fname,idx),"png")

