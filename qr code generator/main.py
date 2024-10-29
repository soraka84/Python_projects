import qrcode

img = qrcode.make("https://www.instagram.com/miroosweets/")
img.save("qrcode.png")