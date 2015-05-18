# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"
init python:
    
    clothes = {}
    body = {}
    currentGary = {}
    thumbs = {}
    
    # Automatically import all images
    for file in renpy.list_files():
        (slot, item) = ('','')
        if file.startswith('images/'):
            if file.endswith('.png'):
                name = file.replace('images/','').replace('clothes/','').replace('body/','').replace('/', ' ').replace('_', ' ').replace('-', ' ').replace('.png','')
                renpy.image(name, Image(file))
                thumbfile = file.replace('images/','thumbs/').replace('.png',' thumb.png')
                
                if renpy.loadable(thumbfile):
                    renpy.image(name + " thumbs", im.Scale(Image(thumbfile),100,100))
                
                #create a list of image name elements - first item is item category, rest is description
                nameSections = name.split(' ',1)
                if len(nameSections) > 0:
                    slot = nameSections[0]
                if len(nameSections) > 1:
                    item = nameSections[1]
                
                if file.find('clothes/') >= 0:
                    if slot in clothes:
                        clothes[slot].append(item)
                    else:
                        clothes[slot] = [item]
                        currentGary[slot] = 'blank'
                elif file.find('body/') >= 0:
                    if slot in body:
                        body[slot].append(item)
                    else:
                        body[slot] = [item]
                        currentGary[slot] = 'blank'
                        
                continue
            continue
    
    def composite_attributes(size,rawDict):
        list = [size]
        midDict = {}
        for key in rawDict:
            if rawDict[key] != 'blank':
                midDict[key] = rawDict[key]
        for key in sorted(midDict, key=garyZorder.__getitem__):
            list.append((0,0))
            list.append(" ".join((key,) + tuple(midDict[key].split())))
        #renpy.notify(str(list))
        return(list)
        
    def draw_gary(st, at, newGary):
        return LiveComposite(*composite_attributes((1600,1200),newGary)),1

    garyZorder = {'skin':0,
        'details':1,
        'mouth':2,
        'nose':3,
        'eyes':4,
        'brows':5,
        'tattoo':6,
        'gary':7,
        'hair':8,
        'mask':9,
        'bodyhair':10,
        'underwear':11,
        'socks':12,
        'shoes':13,
        'pants':14,
        'head':15,
        'shirt':16,
        'glasses':17,
        'chest':19,
        'neck':19,
        'wrist':20,
        'jacket':21,
        'facialhair':22}
    
    currentGary['gary'] = ''

image facialhair blank = Null()
image jacket blank = Null()
image shirt blank = Null()
image head blank = Null()
image pants blank = Null()
image shoes blank = Null()
image underwear blank = Null()
image socks blank = Null()
image bodyhair blank = Null()
image hair blank = Null()
image tattoo blank = Null()
image bodydetail blank = Null()
image glasses blank = Null()
image neck blank = Null()
image chest blank = Null()
image wrist blank = Null()

image gary prostheticleg = AlphaMask("gary", "details prostheticleg mask")
image skin dark prostheticleg = AlphaMask("skin dark", "details prostheticleg mask")
image skin medium prostheticleg = AlphaMask("skin medium", "details prostheticleg mask")
image skin pale prostheticleg = AlphaMask("skin pale", "details prostheticleg mask")

init python:
    def bodymask(img,mask):
        return AlphaMask(img,mask)

image baseGary = DynamicDisplayable(draw_gary,currentGary)

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
    scene bg at halfsize
    call RandomGary
    #show gary at halfsize
    #show details prostheticleg masked zorder 20
    #show baseGary
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
        call RandomGary
        jump dressup
        #jump date
    else:
        call DressGary(*result)
        call RandomGary
        jump dressup


label DressGary(slot="",item=''):
    python:
        if currentGary[slot] == item:
            #if Gary is already wearing this item, remove it instead
            item = "blank",
        imagename = (slot,) + tuple(item.split())
        renpy.notify(str(imagename))
        if not renpy.has_image(imagename):
            #if item doesn't exist, do nothing
            #renpy.notify(str(imagename) + " does not exist!")
            renpy.jump("DoneDressing")
    
        # update Gary's appearance dictionary
        currentGary[slot] = item
       
        renpy.show((imagename), (halfsize,))
    return
label DoneDressing:
    return

label RandomGary:
    python:
        attributes = ['skin','eyes','mouth','nose','brows','hair','facialhair','bodyhair','details']
        for att in attributes:
            item = body[att][renpy.random.randint(0,len(body[att])-1)]
            currentGary[att] = item
            imagename = (att,) + tuple(item.split())
            #renpy.show(baseGary, (halfsize,))
            #renpy.show((imagename), (halfsize,))
        #renpy.notify(currentGary)
        currentGary['gary'].replace(' prostheticleg','')
        if currentGary['details'] == 'prostheticleg':
            if not 'prostheticleg' in currentGary['gary']:
                currentGary['gary'] = currentGary['gary'] + ' prostheticleg'
                currentGary['skin'] = currentGary['skin'] + ' prostheticleg'
        if currentGary['head'] == 'fedora':
            currentGary['hair'] = currentGary['hair'] + ' fedora'
    show baseGary at halfsize
    return

label date:
    scene bg gary at bust
    "Hello"
    return