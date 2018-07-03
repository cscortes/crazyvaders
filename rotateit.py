from PIL import Image

im = Image.open("stardust.png")
im.thumbnail( (96,96) )
for idx, angle in enumerate(range(0,180,9*2)):
    print(idx,angle)
    t = im.rotate(angle)
    t.save("images/explosion/stardust_sm_%02d.png"%idx,"png")

