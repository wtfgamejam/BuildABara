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
                name = file.replace('images/','').replace('clothes/','').replace('pinup/','').replace('love/','').replace('body/','').replace('/', ' ').replace('_', ' ').replace('-', ' ').replace('.png','')
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
        
    def draw_pinup(st, at, newGary):
        return LiveComposite((1600,1200),
                (0,0),"bg pinup",
                (0,0),"pinup skin " + newGary['skin'].replace('prostheticleg',''),
                (0,0),"pinup tattoo " + newGary['tattoo'],
                (0,0),"pinup bodyhair " + newGary['bodyhair'],
                (0,0),"pinup lines"),None
        
    def draw_love(st, at, newGary):
        return LiveComposite((1600,1200),
                (0,0),"bg love",
                (0,0),"love skin " + newGary['skin'].replace('prostheticleg',''),
                (0,0),"love lines"),None

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
        'glasses':15,
        'head':16,
        'shirt':17,
        'chest':19,
        'neck':19,
        'wrist':20,
        'jacket':21,
        'scarf':22,
        'facialhair':23}
    
    currentGary['gary'] = ''
    
    clothesBlanks = ['jacket','shirt','head','pants','shoes','glasses','neck','scarf','chest','wrist','socks']
    bodyBlanks = ['facialhair','bodyhair','hair','tattoo','details']
    
    for key in clothesBlanks:
        clothes[key].append('blank')
    for key in bodyBlanks:
        body[key].append('blank') 

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
image details blank = Null()
image glasses blank = Null()
image neck blank = Null()
image chest blank = Null()
image wrist blank = Null()
image scarf blank = Null()
image pinup tattoo blank = Null()
image pinup tattoo tribal = Null()
image pinup bodyhair blank = Null()

image gary prostheticleg = AlphaMask("gary", "details prostheticleg mask")
image skin dark prostheticleg = AlphaMask("skin dark", "details prostheticleg mask")
image skin medium prostheticleg = AlphaMask("skin medium", "details prostheticleg mask")
image skin pale prostheticleg = AlphaMask("skin pale", "details prostheticleg mask")
image hair andrew black fedora = AlphaMask("hair andrew black", "head fedora mask")
image hair andrew blonde fedora = AlphaMask("hair andrew blonde", "head fedora mask")
image hair andrew brown fedora = AlphaMask("hair andrew brown", "head fedora mask")
image hair andrew red fedora = AlphaMask("hair andrew red", "head fedora mask")
image hair locks black fedora = AlphaMask("hair locks black", "head fedora mask")
image hair locks blonde fedora = AlphaMask("hair locks blonde", "head fedora mask")
image hair locks brown fedora = AlphaMask("hair locks brown", "head fedora mask")
image hair locks red fedora = AlphaMask("hair locks red", "head fedora mask")

image bg black = "#000"

init python:
    def bodymask(img,mask):
        return AlphaMask(img,mask)

image baseGary = DynamicDisplayable(draw_gary,currentGary)
image pinupGary = DynamicDisplayable(draw_pinup,currentGary)
image loveGary = DynamicDisplayable(draw_love,currentGary)

transform halfsize:
    zoom 0.5
transform bust:
    xalign 0.5
    yalign 0.1

transform dateright:
    xalign 0.8
    yalign 0.1
transform dateleft:
    xalign 0.2
    yalign 0.1

transform underpantsloc:
    pos(332, 260)
transform pantsloc:
    pos(320, 267)
        

# Declare characters used by this game.
define g = Character('Yousuke', color="#c8ffc8")
define t = Character('Taylor Swift', color="#cc5490")
# Hold at black for a bit.
define fadehold = Fade(0.5, 1.5, 0.5)

# The game starts here.
label start:
    play music "music/buildabara-build.mp3"
    scene bg at halfsize
    call RandomGary(newGary=True,newOutfit=True)
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
    elif result == "randomoutfit":
        call RandomGary(newOutfit=True)
        jump dressup
    elif result == "randomgary":
        call RandomGary(newGary=True)
        jump dressup
    else:
        if result[0] in currentGary:
            call DressGary(*result)
        jump dressup


label DressGary(slot="",item=''):
    python:
        if currentGary[slot] == item:
            #if Gary is already wearing this item, remove it instead
            item = "blank"
        imagename = (slot,) + tuple(item.split())

        # bug: renpy.has_image checks for valid tag but NOT properties
        if not renpy.has_image(imagename):
            #if item doesn't exist, do nothing
            renpy.jump("DoneDressing")
    
        # update Gary's appearance dictionary
        currentGary[slot] = item
    call Masking
    show baseGary at halfsize
    return
label DoneDressing:
    return

label RandomGary(newGary=False,newOutfit=False):
    if newGary:
        python:
            attributes = ['skin','eyes','mouth','nose','brows','hair','facialhair','bodyhair','details','tattoo']
            for att in attributes:
                item = body[att][renpy.random.randint(0,len(body[att])-1)]
                currentGary[att] = item
            currentGary['underwear'] =  clothes['underwear'][renpy.random.randint(0,len(clothes['underwear'])-1)]
    if newOutfit:
        python:
            attributes = ['jacket','shirt','head','pants','underwear','shoes','socks','scarf','glasses','neck','chest','wrist']
            for att in attributes:
                articles = clothes[att][:]
                max = len(articles)
                if max < 8 and att in clothesBlanks:
                    for i in range(max, 8):
                        articles.append('blank')
                    max = 8
                index = renpy.random.randint(0,max-1)
                item = articles[index]
                    
                currentGary[att] = item
        
    call Masking
    show baseGary at halfsize
    return

label Masking:
    python:
        currentGary['gary'] = currentGary['gary'].replace('prostheticleg','')
        currentGary['skin'] = currentGary['skin'].replace('prostheticleg','')
        currentGary['hair'] = currentGary['hair'].replace('fedora','')
        
        if currentGary['details'] == 'prostheticleg':
            currentGary['gary'] = currentGary['gary'] + ' prostheticleg'
            currentGary['skin'] = currentGary['skin'] + ' prostheticleg'
        if currentGary['head'] == 'fedora':
            if 'andrew' in currentGary['hair']:
                currentGary['hair'] = currentGary['hair'] + ' fedora'
            if 'locks' in currentGary['hair']:
                currentGary['hair'] = currentGary['hair'] + ' fedora'
    return

label date:
    python:
        boring = False
        if 'fedora' in currentGary['head']:
            boring = True
            if 'redpill' in currentGary['shirt']:
                renpy.jump("mra")
    play music "music/buildabara-date.mp3"
    scene bg date at halfsize
    show baseGary at bust
    g "Hey! Wow, you look just like your Tinder picture."
    g "...that's a good thing by the way."
    g "Where do you want to go today?"
    menu:
        "Let's cut right to the chase. Your place or mine?":
            g "Woah, tiger! Maybe let's get to know each other first."
            g "Like..."
            jump doforfun
        "There's a great dog park nearby.":
            g "Oh, do you have a dog?"
            menu:
                "Yeah! Do you mind?":
                    g "Not at all!"
                    jump doforfun
                "Nope! I just like watching them play":
                    g "Haha! Okay. Sounds fun."
                    jump doforfun
        "I didn't really plan anything.":
            $ boring = True
            g "Oh. Hmm."
            g "Okay..."
            g "So..."
            jump doforfun

label doforfun:
    g "What do you like to do for fun?"
    menu fun_menu:
        "Photography":
            g "Oh yeah?! What kind?"
            menu:
                "People, mostly.":
                    g "Oh yeah?"
                    menu:
                        "Yeah... You know, you have great bone structure.":
                            jump bonestructure
                "Oh, this and that":
                    g "Cool. What else do you do?"
                    jump fun_menu
        "Oh you know. Reading, playing video games, watching Netflix.":
            jump Netflix
        "Stuff, I guess" if boring:
            g "...you're not giving me a lot to work with."
            menu:
                "Yeah, this was a mistake":
                    jump sadending
        
label Netflix:
    g "Me too! What are you watching right now?"
    menu:
        "House of Cards":
            pass
        "Unbreakable":
            pass
        "Orange is the New Black":
            pass
    g "Wow, me too! What did you think of the last episode?"
    
    show bg date at halfsize with fadehold
    jump goodtime

label goodtime:
    g "Wow... I had a really great time tonight. You're incredible."
    menu:
        "Yeah... You know, you have great bone structure.":
            jump bonestructure
        "Yeah. I feel that way too.":
            jump kiss
            
label bonestructure:
    g "Oh really..."
    "Yeah, you should 'model' for me sometime"
    g "Haha! Maybe let's see where the night takes us..."
    jump pinupending
    
label kiss:
    g "Maybe this is a little forward but..."
    g "...is it alright if I kiss you?"
    menu:
        "I was just about to ask you the same thing...":
            show bg date with fadehold
            jump taylor
        "I really like you, but...":
            g "I get it...that's okay."
            jump taylor
        "I think we should just be friends.":
            jump friends
label friends:
    g "Oh... okay."
    g "That's okay."
    g "See you around, I guess."
    jump sadending

label taylor:
    show baseGary:
        xalign 0.25
    with move

    g "Wait a minute..."
    show taylor:
        xalign 0.0 
        yalign 1.0
        zoom 0.7
    with moveinleft
    g "...is that Taylor Swift?"
    t "Hey guys! I couldn't help but overhear your conversation. I can't believe you just met!"
    t "I go on too many dates, myself."
    t "Can't seem to make them stay."
    t "But I can tell you two are gonna be forever!"
    t "Here, I want you guys to have these cookies I just made."
    t "You guys have mad love!"
    jump happyending

label happyending:
    scene bg black with fade
    show loveGary at halfsize with fade
    pause
    return
label sadending:
    scene bg netflix at halfsize with fade
    pause
    return

label pinupending:
    scene bg black with fade
    show pinupGary at halfsize with fade
    pause
    return

label mra:
    play music "music/buildabara-dateawful.mp3"
    scene bg mra at halfsize
    show baseGary at bust
    g "Hey. Huh..."
    g "Someone's been using old pictures on their Tinder profile, and it's not me."
    menu:
        "Are you sure about that?":
            g "Hey, it's just a joke! Lighten up."
            g "I think you look better now. Too bad your pretty face doesn't match that nasty attitude."
        "Well, this is off to a good start.":
            pass
    menu:
        "Are you seriously trying to neg me?":
            pass
    g "Oh... uh... um. Never mind."
    menu:
        "This was a mistake":
            pass
    g "Wait, wait! I'm just really insecure! I don't know how to talk to people!"
    menu:
        "Okay. One more shot.":
            g "Thanks!"
        "Yeah, we're done here.":
            jump sadending
    menu:
        "What do you think about Mad Max?":
            g "You know, I would have liked Max to be more of a prominent character, you know?"
        "What do you think about Gamergate?":
            g "I really do think it's become more about ethics in game journalism..."
    menu donehere_menu:
        "Yeah, we're done here.":
            jump sadending

    