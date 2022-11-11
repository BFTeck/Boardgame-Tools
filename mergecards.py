import os
from math import sqrt, ceil, floor
from PIL import Image #Pillow
import fitz   #Pymupdf
import platform
import io
import math

def calculduratio(width,height):
    if width <= height:
        x=width
        y=height
    else:
        x=height
        y=width
    ratio=y/x
    ratio = ratio * 100
    ratio = math.trunc(ratio)
    ratio = ratio / 100
    # 63x88mm [rapport 1,39] => Magic et autres jeux de cartes à collectionner.
    # 55,16x84,24mm [rapport 1,52] => cartes françaises traditionnelles
    # 85x85mm [rapport 1] => format utilisé entre autre par Cocktail Games
    # 54x85mm [rapport 1,57] => format francais
    # 58x89mm [rapport 1,53] => format bridge
    # 63x89mm [rapport 1,41] => format poker
    # 60x113mm [rapport 1,88] => format Tarot


    #print(ratio)
    return ratio


def AnalyseCardSize(fichierPdf):
    n = 1
    img = 1
    fileName = "Myth"
    wid = 0
    hei = 0
    differentsize = False
    firstcard = True
    othersize = []
    doc = fitz.open(fichierPdf)
    listofsize=[]
    print("Analyse du fichier: " + str(fichierPdf))

    for page in doc:

            zoom = 3  # zoom factor
            mat = fitz.Matrix(zoom, zoom)
            pix = page.getPixmap(matrix=mat)

            if wid == 0:
                wid = pix.width
                hei = pix.height
                format = calculduratio(wid,hei)
                listofsize.append(format)
                print("premier taille: "+str(wid)+"x"+str(hei))

            if wid != pix.width or hei != pix.height:
                differentsize = True
                print("autre taille: " + str(wid) + "x" + str(hei))
                wid = pix.width
                hei = pix.height
                format = calculduratio(wid, hei)
                listofsize.append(format)



def search(cardsdirectoryinside):
    listofpdfinside=[]
    chemincompletinside=""
    for path, dirs, files in os.walk(cardsdirectoryinside):

        for filefound in files:
            fileName, fileExtension = os.path.splitext(os.path.basename(filefound))
            if fileExtension == ".pdf":
                if platform.system() == 'Linux':
                    chemincompletinside = path + '/' + filefound
                elif platform.system() == 'Windows':
                    chemincompletinside = path + '\\' + filefound
                else:
                    chemincompletinside = path + '/' + filefound
                listofpdfinside.append(chemincompletinside)


    return  listofpdfinside

def lastsaveimg(n,pixlist,outputdirectory,fileName):
    img = 1
    wid = 0
    hei = 0
    othersize=[]
    for pix in pixlist:



            if wid == 0:
                correctsize = True
                print("Last pix:")
                print(pix)
            elif wid == pix.width and hei == pix.height:
                correctsize = True
            else:
                correctsize = False
                othersize.append(pix)
                print("New Other pix:")
                print(pix)

            if correctsize == True:
                if img==1:
                    wid = pix.width
                    hei = pix.height
                    dpix=pix.xres
                    dpiy=pix.yres
                    imgsize=(wid*3+2,hei*3+2)
                    im = Image.new('RGB', imgsize, 'black')
                    immodele =  Image.new('RGB', imgsize, 'white')
                    im.paste(immodele, (0,0))
                    im.paste(immodele, (wid+1, 0))
                    im.paste(immodele, (wid*2+2, 0))
                    im.paste(immodele, (0,hei+1))
                    im.paste(immodele, (wid+1, hei+1))
                    im.paste(immodele, (wid*2+2, hei+1))
                    im.paste(immodele, (0,hei*2+2))
                    im.paste(immodele, (wid+1, hei*2+2))
                    im.paste(immodele, (wid*2+2, hei*2+2))

                    im2 = Image.new('RGB', imgsize, 'black')
                    im2.paste(immodele, (0,0))
                    im2.paste(immodele, (wid+1, 0))
                    im2.paste(immodele, (wid*2+2, 0))
                    im2.paste(immodele, (0,hei+1))
                    im2.paste(immodele, (wid+1, hei+1))
                    im2.paste(immodele, (wid*2+2, hei+1))
                    im2.paste(immodele, (0,hei*2+2))
                    im2.paste(immodele, (wid+1, hei*2+2))
                    im2.paste(immodele, (wid*2+2, hei*2+2))
                    immodele.close
                    coords=(0,0)
                elif img==2:
                    coords = (wid+1, 0)
                elif img==3:
                    coords = (wid*2+2, 0)
                elif img==4:
                    coords=(0,hei+1)
                elif img==5:
                    coords = (wid+1, hei+1)
                elif img==6:
                    coords = (wid*2+2, hei+1)
                elif img==7:
                    coords=(0,hei*2+2)
                elif img==8:
                    coords = (wid+1, hei*2+2)
                elif img==9:
                    coords = (wid*2+2, hei*2+2)


                pixheight=pix.height
                pixwith=pix.width
                pixsize=(pixwith,pixheight)

                #pixpil=Image.frombuffer('RGBA', pixsize, pix.getPNGData(), decoder_name="raw")
                #pixpil = Image.frombytes('RGBA', pixsize, pix.getPNGData(), decoder_name="raw")
                image_data = pix.getImageData()
                pixpil = Image.open(io.BytesIO(image_data))

                im.paste(pixpil, coords)

                if img==9:
                    if n<10:
                        number="00"+str(n)
                    elif n< 100:
                        number = "0" + str(n)
                    else:
                        number = str(n)

                    if platform.system() == 'Linux':
                        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"

                    elif platform.system() == 'Windows':
                        chemincomplet = outputdirectory + '\\' + fileName + number + ".png"
                    else:
                        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"
                    
                    im.save(chemincomplet,dpi=(dpix,dpiy))
                    img = 0
                    n = n + 1

                img = img+1

    if n<10:
        number="00"+str(n)
    elif n< 100:
        number = "0" + str(n)
    else:
        number = str(n)

    if platform.system() == 'Linux':
        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"
    elif platform.system() == 'Windows':
        chemincomplet = outputdirectory + '\\' + fileName + number + ".png"
    else:
        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"

    if img != 1:
        im.save(chemincomplet,dpi=(dpix,dpiy))

    if len(othersize) != 0:
        lastsaveimg(n,othersize,outputdirectory,fileName)

def lastsaveimgFold(n,pixlist,outputdirectory,fileName):
    img = 1
    wid = 0
    hei = 0
    othersize=[]
    for pix in pixlist:



            if wid == 0:
                correctsize = True
                print("Last pix:")
                print(pix)
            elif wid == pix.width and hei == pix.height:
                correctsize = True
            else:
                correctsize = False
                othersize.append(pix)
                print("New Other pix:")
                print(pix)

            if correctsize == True:
                pixheight=pix.height
                pixwith=pix.width
                pixsize=(pixwith,pixheight)

                #pixpil=Image.frombuffer('RGBA', pixsize, pix.getPNGData(), decoder_name="raw")
                #pixpil = Image.frombytes('RGBA', pixsize, pix.getPNGData(), decoder_name="raw")
                image_data = pix.getImageData()
                pixpil = Image.open(io.BytesIO(image_data))

                if img==1:
                    wid = pix.width
                    hei = pix.height
                    dpix=pix.xres
                    dpiy=pix.yres
                    imgsize=(wid*3+2,hei*3+2)
                    im = Image.new('RGB', imgsize, 'black')
                    immodele =  Image.new('RGB', imgsize, 'white')
                    im.paste(immodele, (0,0))
                    im.paste(immodele, (wid+1, 0))
                    im.paste(immodele, (wid*2+2, 0))
                    im.paste(immodele, (0,hei+1))
                    im.paste(immodele, (wid+1, hei+1))
                    im.paste(immodele, (wid*2+2, hei+1))
                    im.paste(immodele, (0,hei*2+2))
                    im.paste(immodele, (wid+1, hei*2+2))
                    im.paste(immodele, (wid*2+2, hei*2+2))

                    im2 = Image.new('RGB', imgsize, 'black')
                    im2.paste(immodele, (0,0))
                    im2.paste(immodele, (wid+1, 0))
                    im2.paste(immodele, (wid*2+2, 0))
                    im2.paste(immodele, (0,hei+1))
                    im2.paste(immodele, (wid+1, hei+1))
                    im2.paste(immodele, (wid*2+2, hei+1))
                    im2.paste(immodele, (0,hei*2+2))
                    im2.paste(immodele, (wid+1, hei*2+2))
                    im2.paste(immodele, (wid*2+2, hei*2+2))
                    immodele.close
                    coords=(0,0)
                    im.paste(pixpil, coords)
                elif img==2:
                    coords = (wid+1, 0)
                    im.paste(pixpil, coords)
                elif img==3:
                    coords=(0,hei+1)
                    im.paste(pixpil, coords)
                elif img==4:
                    coords = (wid+1, hei+1)
                    im.paste(pixpil, coords)

                elif img==5:
                    coords=(0,hei*2+2)
                    im.paste(pixpil, coords)
                elif img==6:
                    coords = (wid+1, hei*2+2)
                    im.paste(pixpil, coords)

                elif img==7:
                    coords = (wid*2+2, 0)
                    im.paste(pixpil, coords)
                elif img==8:
                    coords = (wid*2+2, hei+1)
                    rotated     = pixpil.rotate(180)
                    im.paste(rotated, coords)





                if img==8:
                    if n<10:
                        number="00"+str(n)
                    elif n< 100:
                        number = "0" + str(n)
                    else:
                        number = str(n)

                    if platform.system() == 'Linux':
                        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"

                    elif platform.system() == 'Windows':
                        chemincomplet = outputdirectory + '\\' + fileName + number + ".png"
                    else:
                        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"
                    
                    im.save(chemincomplet,dpi=(dpix,dpiy))
                    img = 0
                    n = n + 1

                img = img+1

    if n<10:
        number="00"+str(n)
    elif n< 100:
        number = "0" + str(n)
    else:
        number = str(n)

    if platform.system() == 'Linux':
        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"
    elif platform.system() == 'Windows':
        chemincomplet = outputdirectory + '\\' + fileName + number + ".png"
    else:
        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"

    if img != 1:
        im.save(chemincomplet,dpi=(dpix,dpiy))

    if len(othersize) != 0:
        lastsaveimg(n,othersize,outputdirectory,fileName)

def lastsaveimgRV(n,pixlist,outputdirectory,fileName):
    img = 1
    wid = 0
    hei = 0
    othersize=[]
    for pix in pixlist:



            if wid == 0:
                correctsize = True
                print("Last pix:")
                print(pix)
            elif wid == pix.width and hei == pix.height:
                correctsize = True
            else:
                correctsize = False
                othersize.append(pix)
                print("New Other pix:")
                print(pix)

            if correctsize == True:
                image_data = pix.getImageData()
                pixpil = Image.open(io.BytesIO(image_data))

                if img==1:
                    wid = pix.width
                    hei = pix.height
                    imgsize=(wid*3+2,hei*3+2)
                    im = Image.new('RGB', imgsize, 'black')
                    immodele =  Image.new('RGB', imgsize, 'white')
                    im.paste(immodele, (0,0))
                    im.paste(immodele, (wid+1, 0))
                    im.paste(immodele, (wid*2+2, 0))
                    im.paste(immodele, (0,hei+1))
                    im.paste(immodele, (wid+1, hei+1))
                    im.paste(immodele, (wid*2+2, hei+1))
                    im.paste(immodele, (0,hei*2+2))
                    im.paste(immodele, (wid+1, hei*2+2))
                    im.paste(immodele, (wid*2+2, hei*2+2))

                    im2 = Image.new('RGB', imgsize, 'black')
                    im2.paste(immodele, (0,0))
                    im2.paste(immodele, (wid+1, 0))
                    im2.paste(immodele, (wid*2+2, 0))
                    im2.paste(immodele, (0,hei+1))
                    im2.paste(immodele, (wid+1, hei+1))
                    im2.paste(immodele, (wid*2+2, hei+1))
                    im2.paste(immodele, (0,hei*2+2))
                    im2.paste(immodele, (wid+1, hei*2+2))
                    im2.paste(immodele, (wid*2+2, hei*2+2))
                    immodele.close
                    dpix=pix.xres
                    dpiy=pix.yres
                    coords=(0,0)

                    im.paste(pixpil, coords)
                elif img==3:
                    coords = (wid+1, 0)
                    im.paste(pixpil, coords)
                elif img==5:
                    coords = (wid*2+2, 0)
                    im.paste(pixpil, coords)
                elif img==7:
                    coords=(0,hei+1)
                    im.paste(pixpil, coords)
                elif img==9:
                    coords = (wid+1, hei+1)
                    im.paste(pixpil, coords)
                elif img==11:
                    coords = (wid*2+2, hei+1)
                    im.paste(pixpil, coords)
                elif img==13:
                    coords=(0,hei*2+2)
                    im.paste(pixpil, coords)
                elif img==15:
                    coords = (wid+1, hei*2+2)
                    im.paste(pixpil, coords)
                elif img==17:
                    coords = (wid*2+2, hei*2+2)
                    im.paste(pixpil, coords)
                elif img==6:
                    coords=(0,0)
                    im2.paste(pixpil, coords)
                elif img==4:
                    coords = (wid+1, 0)
                    im2.paste(pixpil, coords)
                elif img==2:
                    coords = (wid*2+2, 0)
                    im2.paste(pixpil, coords)
                elif img==12:
                    coords=(0,hei+1)
                    im2.paste(pixpil, coords)
                elif img==10:
                    coords = (wid+1, hei+1)
                    im2.paste(pixpil, coords)
                elif img==18:
                    coords = (wid+1, hei*2+2)
                    im2.paste(pixpil, coords)

                    if n<10:
                        number="00"+str(n)
                    elif n< 100:
                        number = "0" + str(n)
                    else:
                        number = str(n)

                    if platform.system() == 'Linux':
                        chemincomplet = outputdirectory + '/' + fileName +  number + "_Recto.jpg"
                        chemincomplet2 = outputdirectory + '/' + fileName +  number + "_Verso.jpg"

                    elif platform.system() == 'Windows':
                        chemincomplet = outputdirectory + '\\' + fileName + number + "_Recto.jpg"
                        chemincomplet2 = outputdirectory + '\\' + fileName + number + "_Verso.jpg"
                    else:
                        chemincomplet = outputdirectory + '/' + fileName + number + "_Recto.jpg"
                        chemincomplet2 = outputdirectory + '/' + fileName + number + "_Verso.jpg"

                    im.save(chemincomplet,dpi=(dpix,dpiy))
                    im2.save(chemincomplet2,dpi=(dpix,dpiy))
                    img = 0
                    n = n + 1
                elif img==16:
                    coords = (wid+1, hei*2+2)
                    im2.paste(pixpil, coords)
                elif img==14:
                    coords = (wid*2+2, hei*2+2)
                    im2.paste(pixpil, coords)
                img = img +1

    if n<10:
        number="00"+str(n)
    elif n< 100:
        number = "0" + str(n)
    else:
        number = str(n)

    if platform.system() == 'Linux':
        chemincomplet = outputdirectory + '/' + fileName +  number + "_Recto.jpg"
        chemincomplet2 = outputdirectory + '/' + fileName +  number + "_Verso.jpg"

    elif platform.system() == 'Windows':
        chemincomplet = outputdirectory + '\\' + fileName + number + "_Recto.jpg"
        chemincomplet2 = outputdirectory + '\\' + fileName + number + "_Verso.jpg"
    else:
        chemincomplet = outputdirectory + '/' + fileName + number + "_Recto.jpg"
        chemincomplet2 = outputdirectory + '/' + fileName + number + "_Verso.jpg"

    if img != 1:
        im.save(chemincomplet,dpi=(dpix,dpiy))
        im2.save(chemincomplet2,dpi=(dpix,dpiy))

    if len(othersize) != 0:
        lastsaveimgRV(n,othersize,outputdirectory,fileName)

def regroupRecto(listofpdf, outputdirectory):
    n=1
    img = 1
    fileName="Myth"
    wid = 0
    hei = 0

    othersize=[]
    for pdffile in listofpdf:
        doc = fitz.open(pdffile)
        #listofpix=[]

        for page in doc:

            zoom = 3   # zoom factor
            mat = fitz.Matrix(zoom, zoom)
            pix = page.getPixmap(matrix = mat)


            if wid == 0:
                correctsize = True

            elif wid == pix.width and hei == pix.height:
                correctsize = True
            else:
                correctsize = False
                othersize.append(pix)


            if correctsize == True:
                if img==1:
                    wid = pix.width
                    hei = pix.height
                    dpix=pix.xres
                    dpiy=pix.yres
                    imgsize=(wid*3+2,hei*3+2)
                    #im = Image.new('RGBA', imgsize, None)
                    im = Image.new('RGB', imgsize, 'black')
                    immodele =  Image.new('RGB', imgsize, 'white')
                    im.paste(immodele, (0,0))
                    im.paste(immodele, (wid+1, 0))
                    im.paste(immodele, (wid*2+2, 0))
                    im.paste(immodele, (0,hei+1))
                    im.paste(immodele, (wid+1, hei+1))
                    im.paste(immodele, (wid*2+2, hei+1))
                    im.paste(immodele, (0,hei*2+2))
                    im.paste(immodele, (wid+1, hei*2+2))
                    im.paste(immodele, (wid*2+2, hei*2+2))
                    immodele.close


                    coords=(0,0)
                elif img==2:
                    coords = (wid+1, 0)
                elif img==3:
                    coords = (wid*2+2, 0)
                elif img==4:
                    coords=(0,hei+1)
                elif img==5:
                    coords = (wid+1, hei+1)
                elif img==6:
                    coords = (wid*2+2, hei+1)
                elif img==7:
                    coords=(0,hei*2+2)
                elif img==8:
                    coords = (wid+1, hei*2+2)
                elif img==9:
                    coords = (wid*2+2, hei*2+2)


                pixheight=pix.height
                pixwith=pix.width
                pixsize=(pixwith,pixheight)

                #pixpil=Image.frombuffer('RGBA', pixsize, pix.getPNGData(), decoder_name="raw")
                #pixpil = Image.frombytes('RGBA', pixsize, pix.getPNGData(), decoder_name="raw")
                image_data = pix.getImageData()
                pixpil = Image.open(io.BytesIO(image_data))

                im.paste(pixpil, coords)

                if img==9:
                    if n<10:
                        number="00"+str(n)
                    elif n< 100:
                        number = "0" + str(n)
                    else:
                        number = str(n)

                    if platform.system() == 'Linux':
                        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"

                    elif platform.system() == 'Windows':
                        chemincomplet = outputdirectory + '\\' + fileName + number + ".png"
                    else:
                        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"
                    
                    im.save(chemincomplet, dpi=(dpix, dpiy))
                    img = 0
                    n = n + 1

                img = img+1

    if n<10:
        number="00"+str(n)
    elif n< 100:
        number = "0" + str(n)
    else:
        number = str(n)

    if platform.system() == 'Linux':
        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"
    elif platform.system() == 'Windows':
        chemincomplet = outputdirectory + '\\' + fileName + number + ".png"
    else:
        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"

    if img != 1:
        im.save(chemincomplet,dpi=(dpix,dpiy))

    if len(othersize) != 0:
        print("Appel de la fonction pour les images de taille différente")
        #lastsaveimg(n,othersize,outputdirectory,fileName)

def regroupRectoVerso(listofpdf, outputdirectory):
    n=1
    img = 1
    fileName="Myth_RV_"
    wid = 0
    hei = 0
    othersize=[]
    for pdffile in listofpdf:
        doc = fitz.open(pdffile)

        for page in doc:
            #page = doc.loadPage(0) #number of page

            zoom = 3   # zoom factor
            mat = fitz.Matrix(zoom, zoom)
            pix = page.getPixmap(matrix = mat)

            #fileName, fileExtension = os.path.splitext(os.path.basename(pdffile))

            #pix.writePNG(chemincomplet)

            pixheight=pix.height
            pixwith=pix.width
            pixsize=(pixwith,pixheight)

            #pixpil=Image.frombuffer('RGBA', pixsize, pix.getPNGData(), decoder_name="raw")
            #pixpil = Image.frombytes('RGBA', pixsize, pix.getPNGData(), decoder_name="raw")


            image_data = pix.getImageData()
            pixpil = Image.open(io.BytesIO(image_data))

            if wid == 0:
                correctsize = True

            elif wid == pix.width and hei == pix.height:
                correctsize = True
            else:
                correctsize = False
                othersize.append(pix)


            if correctsize == True:

                if img==1:
                    wid = pix.width
                    hei = pix.height
                    dpix=pix.xres
                    dpiy=pix.yres
                    imgsize=(wid*3+2,hei*3+2)
                    im = Image.new('RGB', imgsize, 'black')
                    immodele =  Image.new('RGB', imgsize, 'white')
                    im.paste(immodele, (0,0))
                    im.paste(immodele, (wid+1, 0))
                    im.paste(immodele, (wid*2+2, 0))
                    im.paste(immodele, (0,hei+1))
                    im.paste(immodele, (wid+1, hei+1))
                    im.paste(immodele, (wid*2+2, hei+1))
                    im.paste(immodele, (0,hei*2+2))
                    im.paste(immodele, (wid+1, hei*2+2))
                    im.paste(immodele, (wid*2+2, hei*2+2))

                    im2 = Image.new('RGB', imgsize, 'black')
                    im2.paste(immodele, (0,0))
                    im2.paste(immodele, (wid+1, 0))
                    im2.paste(immodele, (wid*2+2, 0))
                    im2.paste(immodele, (0,hei+1))
                    im2.paste(immodele, (wid+1, hei+1))
                    im2.paste(immodele, (wid*2+2, hei+1))
                    im2.paste(immodele, (0,hei*2+2))
                    im2.paste(immodele, (wid+1, hei*2+2))
                    im2.paste(immodele, (wid*2+2, hei*2+2))
                    immodele.close
                    coords=(0,0)
                    im.paste(pixpil, coords)
                elif img==3:
                    coords = (wid+1, 0)
                    im.paste(pixpil, coords)
                elif img==5:
                    coords = (wid*2+2, 0)
                    im.paste(pixpil, coords)
                elif img==7:
                    coords=(0,hei+1)
                    im.paste(pixpil, coords)
                elif img==9:
                    coords = (wid+1, hei+1)
                    im.paste(pixpil, coords)
                elif img==11:
                    coords = (wid*2+2, hei+1)
                    im.paste(pixpil, coords)
                elif img==13:
                    coords=(0,hei*2+2)
                    im.paste(pixpil, coords)
                elif img==15:
                    coords = (wid+1, hei*2+2)
                    im.paste(pixpil, coords)
                elif img==17:
                    coords = (wid*2+2, hei*2+2)
                    im.paste(pixpil, coords)
                elif img==6:
                    coords=(0,0)
                    im2.paste(pixpil, coords)
                elif img==4:
                    coords = (wid+1, 0)
                    im2.paste(pixpil, coords)
                elif img==2:
                    coords = (wid*2+2, 0)
                    im2.paste(pixpil, coords)
                elif img==12:
                    coords=(0,hei+1)
                    im2.paste(pixpil, coords)
                elif img==10:
                    coords = (wid+1, hei+1)
                    im2.paste(pixpil, coords)
                elif img==8:
                    coords = (wid*2+2, hei+1)
                    im2.paste(pixpil, coords)
                elif img==18:
                    coords = (0, hei*2+22)
                    im2.paste(pixpil, coords)

                    if n<10:
                        number="00"+str(n)
                    elif n< 100:
                        number = "0" + str(n)
                    else:
                        number = str(n)

                    if platform.system() == 'Linux':
                        chemincomplet = outputdirectory + '/' + fileName +  number + "_Recto.jpg"
                        chemincomplet2 = outputdirectory + '/' + fileName +  number + "_Verso.jpg"

                    elif platform.system() == 'Windows':
                        chemincomplet = outputdirectory + '\\' + fileName + number + "_Recto.jpg"
                        chemincomplet2 = outputdirectory + '\\' + fileName + number + "_Verso.jpg"
                    else:
                        chemincomplet = outputdirectory + '/' + fileName + number + "_Recto.jpg"
                        chemincomplet2 = outputdirectory + '/' + fileName + number + "_Verso.jpg"

                    im.save(chemincomplet,dpi=(dpix,dpiy))
                    im2.save(chemincomplet2,dpi=(dpix,dpiy))
                    img = 0
                    n = n + 1
                elif img==16:
                    coords = (wid+1, hei*2+2)
                    im2.paste(pixpil, coords)
                elif img==14:
                    coords = (wid*2+2, hei*2+2)
                    im2.paste(pixpil, coords)


                img = img+1

    if n<10:
        number="00"+str(n)
    elif n< 100:
        number = "0" + str(n)
    else:
        number = str(n)

    if platform.system() == 'Linux':
        chemincomplet = outputdirectory + '/' + fileName +  number + "_Recto.jpg"
        chemincomplet2 = outputdirectory + '/' + fileName +  number + "_Verso.jpg"

    elif platform.system() == 'Windows':
        chemincomplet = outputdirectory + '\\' + fileName + number + "_Recto.jpg"
        chemincomplet2 = outputdirectory + '\\' + fileName + number + "_Verso.jpg"
    else:
        chemincomplet = outputdirectory + '/' + fileName + number + "_Recto.jpg"
        chemincomplet2 = outputdirectory + '/' + fileName + number + "_Verso.jpg"

    if img != 1:
        im.save(chemincomplet,dpi=(dpix,dpiy))
        im2.save(chemincomplet2,dpi=(dpix,dpiy))

    if len(othersize) != 0:
        lastsaveimgRV(n,othersize,outputdirectory,fileName)

def regroupRectoVersoFold(listofpdf, outputdirectory):
    n=1
    img = 1
    fileName="Myth_Fold_"
    wid = 0
    hei = 0
    othersize=[]
    for pdffile in listofpdf:
        doc = fitz.open(pdffile)

        for page in doc:
            #page = doc.loadPage(0) #number of page

            zoom = 3   # zoom factor
            mat = fitz.Matrix(zoom, zoom)
            pix = page.getPixmap(matrix = mat)

            #fileName, fileExtension = os.path.splitext(os.path.basename(pdffile))

            #pix.writePNG(chemincomplet)

            pixheight=pix.height
            pixwith=pix.width
            pixsize=(pixwith,pixheight)

            #pixpil=Image.frombuffer('RGBA', pixsize, pix.getPNGData(), decoder_name="raw")
            #pixpil = Image.frombytes('RGBA', pixsize, pix.getPNGData(), decoder_name="raw")
            image_data = pix.getImageData()
            pixpil = Image.open(io.BytesIO(image_data))

            if wid == 0:
                correctsize = True

            elif wid == pix.width and hei == pix.height:
                correctsize = True
            else:
                correctsize = False
                othersize.append(pix)


            if correctsize == True:

                if img==1:
                    wid = pix.width
                    hei = pix.height
                    dpix=pix.xres
                    dpiy=pix.yres
                    imgsize=(wid*3+2,hei*3+2)
                    im = Image.new('RGB', imgsize, 'black')
                    immodele =  Image.new('RGB', imgsize, 'white')
                    im.paste(immodele, (0,0))
                    im.paste(immodele, (wid+1, 0))
                    im.paste(immodele, (wid*2+2, 0))
                    im.paste(immodele, (0,hei+1))
                    im.paste(immodele, (wid+1, hei+1))
                    im.paste(immodele, (wid*2+2, hei+1))
                    im.paste(immodele, (0,hei*2+2))
                    im.paste(immodele, (wid+1, hei*2+2))
                    im.paste(immodele, (wid*2+2, hei*2+2))
                    immodele.close
                    coords=(0,0)
                    im.paste(pixpil, coords)
                elif img==2:
                    coords = (wid+1, 0)
                    im.paste(pixpil, coords)
                elif img==3:
                    coords=(0,hei+1)
                    im.paste(pixpil, coords)
                elif img==4:
                    coords = (wid+1, hei+1)
                    im.paste(pixpil, coords)
                elif img==5:
                    coords=(0,hei*2+2)
                    im.paste(pixpil, coords)
                elif img==6:
                    coords = (wid+1, hei*2+2)
                    im.paste(pixpil, coords)
                elif img==7:
                    coords = (wid*2+2, 0)
                    im.paste(pixpil, coords)
                elif img==8:
                    coords = (wid*2+2, hei+1)
                    rotated     = pixpil.rotate(180)
                    im.paste(rotated, coords)

                    if n<10:
                        number="00"+str(n)
                    elif n< 100:
                        number = "0" + str(n)
                    else:
                        number = str(n)

                    if platform.system() == 'Linux':
                        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"

                    elif platform.system() == 'Windows':
                        chemincomplet = outputdirectory + '\\' + fileName + number + ".png"
                    else:
                        chemincomplet = outputdirectory + '/' + fileName + number + ".png"


                    im.save(chemincomplet,dpi=(dpix,dpiy))
                    img = 0
                    n = n + 1



                img = img+1

    if n<10:
        number="00"+str(n)
    elif n< 100:
        number = "0" + str(n)
    else:
        number = str(n)

    if platform.system() == 'Linux':
        chemincomplet = outputdirectory + '/' + fileName +  number + ".png"
    elif platform.system() == 'Windows':
        chemincomplet = outputdirectory + '\\' + fileName + number + ".png"
    else:
        chemincomplet = outputdirectory + '/' + fileName + number + ".png"


    if img != 1:
        im.save(chemincomplet,dpi=(dpix,dpiy))


    if len(othersize) != 0:
        lastsaveimgFold(n,othersize,outputdirectory,fileName)

pathofscript = os.getcwd()
if platform.system() == 'Linux':
    pathtrecto = pathofscript + '/inputPdfR'
    pathtverso = pathofscript + '/inputPdfV'
    pathtrectoverso = pathofscript + '/inputPdfRV'
    pathtoutput = pathofscript + '/cropped'

    if os.path.exists(pathtrecto) is False:
        os.mkdir(pathtrecto)
    if os.path.exists(pathtverso) is False:
        os.mkdir(pathtverso)
    if os.path.exists(pathtrectoverso) is False:
        os.mkdir(pathtrectoverso)

    if os.path.exists(pathtoutput) is False:
        os.mkdir(pathtoutput)

if platform.system() == 'Windows':
    pathtrecto = pathofscript + '\\inputPdfR'
    pathtverso = pathofscript + '\\inputPdfV'
    pathtrectoverso = pathofscript + '\\inputPdfRV'
    pathtoutput = pathofscript + '/cropped'

    if os.path.exists(pathtrecto) is False:
        os.mkdir(pathtrecto)
    if os.path.exists(pathtverso) is False:
        os.mkdir(pathtverso)
    if os.path.exists(pathtrectoverso) is False:
        os.mkdir(pathtrectoverso)

    if os.path.exists(pathtoutput) is False:
        os.mkdir(pathtoutput)

listePdfR = search(pathtrecto)
listePdfV = search(pathtverso)
listeRPdfV = search(pathtrectoverso)

for fichierpdf in listePdfR:
    AnalyseCardSize(fichierpdf)

for fichierpdf in listePdfV:
    AnalyseCardSize(fichierpdf)

for fichierpdf in listeRPdfV:
    AnalyseCardSize(fichierpdf)

#regroupRecto(listeR, outputdirectory)
#regroupRectoVerso(liste2, outputdirectory)
#regroupRectoVersoFold(liste2, outputdirectory)

