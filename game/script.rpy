# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"
init python hide:

    for file in renpy.list_files():
        if file.startswith('images/'):
            if file.endswith('.png'):
                name = file.replace('images/','').replace('/', ' ').replace('_', ' ').replace('-', ' ').replace('.png','')
                renpy.image(name, Image(file))
                continue
            continue
            
init python:
    currentGary = {'facialhair':'',
    'jacket':'',
    'accessory':'',
    'shirt':'',
    'hat':'',
    'pants':'',
    'shoes':'',
    'underthings':'',
    'bodyhair':'',
    'hair':'',
    'lines':'',
    'tattoos':'',
    'eyebrows':'',
    'eyes':'',
    'nose':'',
    'mouth':'',
    'bodydetail':'',
    'skin':''}
            

image facialhair blank = Null()
image jacket blank = Null()
image accessory blank = Null()
image shirt blank = Null()
image hat blank = Null()
image pants blank = Null()
image shoes blank = Null()
image underthings blank = Null()
image bodyhair blank = Null()
image hair blank = Null()
image lines blank = Null()
image tattoos blank = Null()
image eyebrows blank = Null()
image eyes blank = Null()
image nose blank = Null()
image mouth blank = Null()
image bodydetail blank = Null()
image skin blank = Null()
image pants black clothes = "images/pants-suit.png"

transform halfsize:
    zoom 0.5
transform bust:
    xalign 0.5
    yalign 0.1
    
transform underpantsloc:
    pos(332, 260)
transform pantsloc:
    pos(320, 267)
        

# Declare characters used by this game.
define b = Character('Bara', color="#c8ffc8")


# The game starts here.
label start:
    scene bg gary at halfsize
    call DressGary("pants",("black",))
    jump dressup

    return

# Enter the dressup game interface
label dressup:
    show screen dressup
    # wait for value returned from dressup interface
    $ result = ui.interact()
    
    # if it's date time, move on to date interface
    if result == "date":
        hide screen dressup
        jump date
    else:
        call DressGary(*result)
        jump dressup


label DressGary(slot="",item=()):
    python:
        if currentGary[slot] == item:
            #if Gary is already wearing this item, remove it instead
            item = "blank",
        imagename = (slot,) + tuple(item)
        if not renpy.has_image(imagename):
            #if item doesn't exist, do nothing
            renpy.notify(str(imagename) + " does not exist!")
            renpy.jump("DoneDressing")
    
        # update Gary's appearance dictionary
        currentGary[slot] = item
        
        renpy.show((imagename), (halfsize,))
label DoneDressing:
    return
    
label date:
    scene bg gary at bust
    "Hello"
    return