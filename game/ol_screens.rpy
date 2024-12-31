# level up screen and player action creation

image menu_frame = "menu_frame_black.png" #can put your custom frame here for the menu. I just have some dark gradiant thingy as a place holder


screen level_up_UI: #a button to open the in-game menu
    frame:
        xpadding 50
        ypadding 30
        xalign 0.9
        yalign 0.1
        textbutton "Menu" action [ShowMenu("character_menu")] #the textbutton that shows the menu

screen character_menu(): #holds where the main menu is, can be filled with overview information like current quest and such

    $ tooltip = GetTooltip() #allows us to add tooltips if we want
    if tooltip:
        text "[tooltip]"

    frame: #adds our backdrop
        align (0.5, 0.5) #aligns it to center
        padding (0,0) #sets our padding to 0, instead of the default

        viewport: #wraps everything into the size we want for the full menu layout
            xsize 1344
            ysize 972

            viewport: # menu navigation buttons with scrollbar in case we ever need it - copied into each menu so we don't have to have multiple popups
                xsize 384
                align (0,0)
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox: #a vertical box containing navigation buttons, can be added to if need be
                    textbutton "Main" action [Hide(),ShowMenu("character_menu")] #hids current, shows the called menu
                    textbutton "Attributes" action [Hide(), ShowMenu("level_up_menu")]
                    textbutton "Banes & Boons" action [Hide(), ShowMenu("favored_actions_menu")]
                    textbutton "Equipment" action [Hide(), ShowMenu("equipment")]
                    textbutton "Feats" action [Hide(), ShowMenu("feats")]
                    textbutton "Perks" action [Hide(), ShowMenu("perks")]
                    textbutton "Flaws" action [Hide(), ShowMenu("flaws")]
                    textbutton "Quests" action [Hide(), ShowMenu("quests")]
                    textbutton "Test List" action [Hide(), ShowMenu("test_list")]
                    textbutton "Return" action [Return()] #closes the menu

            hbox: # basic character info, this is just filler for the main menu. You can put a lot here
                xsize 960
                ysize 216
                pos(0.3,0.01)
                vbox:
                    text "[mc.name]'s Character Sheet"
                    text "Hit Points = [mc.hitpoints]"
                    text "Attribute Pts = [mc.attribute_pts]"
                vbox:
                    text "Defenses:"
                    text "Toughness = [mc.toughness]"
                    text "Guard = [mc.guard]"
                    text "Resolve = [mc.resolve]"

screen level_up_menu(): #holds where you can go to adjust Character Attributes

    $ tooltip = GetTooltip()

    if tooltip:
        text "[tooltip]"

        
    frame: #handles all the buttons and attributes such as agility
        align (0.5, 0.5)
        padding (0,0)
        
        viewport: #a grid that contains the textbuttons which control increasing or decreasting on of Open Legend's Attributes
            xsize 1344
            ysize 972

            viewport: # menu navigation buttons with scrollbar in case we ever need it - copied into each menu so we don't have to have multiple popups
                xsize 384
                align (0,0)
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox: #a vertical box containing navigation buttons, can be added to if need be
                    textbutton "Main" action [Hide(),ShowMenu("character_menu")] #hids current, shows the called menu
                    textbutton "Attributes" action [Hide(), ShowMenu("level_up_menu")]
                    textbutton "Banes & Boons" action [Hide(), ShowMenu("favored_actions_menu")]
                    textbutton "Equipment" action [Hide(), ShowMenu("equipment")]
                    textbutton "Feats" action [Hide(), ShowMenu("feats")]
                    textbutton "Perks" action [Hide(), ShowMenu("perks")]
                    textbutton "Flaws" action [Hide(), ShowMenu("flaws")]
                    textbutton "Quests" action [Hide(), ShowMenu("quests")]
                    textbutton "Return" action [Return()] #closes the menu
            
            hbox:
                xsize 960
                ysize 216
                pos(0.3,0.01)
                vbox:
                    text "[mc.name]'s Character Sheet"
                    text "Hit Points = [mc.hitpoints]"
                    text "Attribute Pts = [mc.attribute_pts]"
                vbox:
                    text "Defenses:"
                    text "Toughness = [mc.toughness]"
                    text "Guard = [mc.guard]"
                    text "Resolve = [mc.resolve]"

            vbox: #a container with all of our non-extrodinary character attributes
                xsize 480
                ysize 756
                align (0.5, 1.0)
                vbox: #Physical Attributes
                    text "Physical Attributes"
                    hbox:
                        vbox: #a vertical box containing each attribute textbutton that makes the attribute's value go up when clicked on
                            textbutton "Agility": 
                                text_size 30
                                action Function(mc.attribute_up, "agility")
                                tooltip "Dodge attacks, move with stealth, perform acrobatics, shoot a bow, pick a pocket"
                            textbutton "Fortitude":
                                text_size 30
                                action Function(mc.attribute_up, "fortitude")
                                tooltip "Resist poison, shrug off pain, survive in a desert, wear heavy armor"
                            textbutton "Might":
                                text_size 30
                                action Function(mc.attribute_up, "might")
                                tooltip "Swing a maul, jump over a chasm, break down a door, wrestle a foe to submission"
                        
                        vbox: #a vertical box containing each attribute's value as a textbutton that reduces the value when pressed
                            textbutton "[mc.agility]" text_size 30:
                                action Function(mc.attribute_down, "agility")
                            textbutton "[mc.fortitude]" text_size 30:
                                action Function(mc.attribute_down, "fortitude")
                            textbutton "[mc.might]" text_size 30:
                                action Function(mc.attribute_down, "might")
                vbox: #Mental Attributes
                    text "Mental Attributes"
                    hbox:
                        vbox: #a vertical box containing each attribute textbutton that makes the attribute's value go up when clicked on
                            textbutton "Learning":
                                text_size 30
                                action Function(mc.attribute_up, "learning")
                                tooltip "Recall facts about history, arcane magic, the natural world, or any information you picked up from an external source"
                            textbutton "Logic":
                                text_size 30
                                action Function(mc.attribute_up, "logic")
                                tooltip "Innovate a new crafting method, decipher a code, jury-rig a device, get the gist of a language you don't speak"
                            textbutton "Perception":
                                text_size 30
                                action Function(mc.attribute_up, "perception")
                                tooltip "Sense ulterior motives, track someone, catch a gut feeling, spot a hidden foe, find a secret door"
                            textbutton "Will":
                                text_size 30
                                action Function(mc.attribute_up, "will")
                                tooltip "Maintain your resolve, resist torture, study long hours, stay awake on watch, stave off insanity"
                        
                        vbox: #a vertical box containing each attribute's value as a textbutton that reduces the value when pressed
                            textbutton "[mc.learning]" text_size 30:
                                action Function(mc.attribute_down, "learning")
                            textbutton "[mc.logic]" text_size 30:
                                action Function(mc.attribute_down, "logic")
                            textbutton "[mc.perception]" text_size 30:
                                action Function(mc.attribute_down, "perception")
                            textbutton "[mc.will]" text_size 30:
                                action Function(mc.attribute_down, "will")
                vbox: #Social Attributes 
                    text "Social Attributes"
                    hbox:
                        vbox: #a vertical box containing each attribute textbutton that makes the attribute's value go up when clicked on
                            textbutton "Deception":
                                text_size 30
                                action Function(mc.attribute_up, "deception")
                                tooltip "Tell a lie, bluff at cards, disguise yourself, spread rumors, swindle a sucker"
                            textbutton "Persuasion":
                                text_size 30
                                action Function(mc.attribute_up, "persuasion")
                                tooltip "Negotiate a deal, convince someone, haggle a good price, pry information"
                            textbutton "Presence":
                                text_size 30
                                action Function(mc.attribute_up, "presence")
                                tooltip "Give a speech, sing a song, inspire an army, exert your force of personality, have luck smile upon you"
                            
                        vbox: #a vertical box containing each attribute's value as a textbutton that reduces the value when pressed
                            textbutton "[mc.deception]" text_size 30:
                                action Function(mc.attribute_down, "deception")
                            textbutton "[mc.persuasion]" text_size 30:
                                action Function(mc.attribute_down, "persuasion")
                            textbutton "[mc.presence]" text_size 30:
                                action Function(mc.attribute_down, "presence")
                    
            viewport: #a container with all of our extraordinary character attributes
                xsize 480
                ysize 756
                align (1.0, 1.0)
                vbox:
                    text "Extraordinary Attributes"
                    hbox:
                        vbox: #a vertical box containing each attribute textbutton that makes the attribute's value go up when clicked on
                            textbutton "Alteration":
                                text_size 30
                                action Function(mc.attribute_up, "alteration")
                                tooltip "Change shape, alter molecular structures, transmute one material into another"
                            textbutton "Creation":
                                text_size 30
                                action Function(mc.attribute_up, "creation")
                                tooltip "Channel higher powers, manifest something from nothing, regenerate, divinely bolster"
                            textbutton "Energy":
                                text_size 30
                                action Function(mc.attribute_up, "energy")
                                tooltip "Create and control the elements—fire, cold, electricity"
                            textbutton "Entropy":
                                text_size 30
                                action Function(mc.attribute_up, "entropy")
                                tooltip "Disintegrate matter, kill with a word, create undead, sicken others"
                            textbutton "Influence":
                                text_size 30
                                action Function(mc.attribute_up, "influence")
                                tooltip "Control the minds of others, speak telepathically, instill fear, create illusory figments, cloak with invisibility"
                            textbutton "Movement":
                                text_size 30
                                action Function(mc.attribute_up, "movement")
                                tooltip "Teleport, fly, hasten, telekinetically push"
                            textbutton "Prescience":
                                text_size 30
                                action Function(mc.attribute_up, "prescience")
                                tooltip "See the future, read minds or auras, view from afar, detect magic or evil, communicate with extraplanar entities"
                            textbutton "Protection":
                                text_size 30
                                action Function(mc.attribute_up, "protection")
                                tooltip "Protect from damage, break supernatural influence, dispel magic, exile extradimensional beings"

                        vbox: #a vertical box containing each attribute's value as a textbutton that reduces the value when pressed
                            textbutton "[mc.alteration]" text_size 30:
                                action Function(mc.attribute_down, "alteration")
                            textbutton "[mc.creation]" text_size 30:
                                action Function(mc.attribute_down, "creation")
                            textbutton "[mc.energy]" text_size 30:
                                action Function(mc.attribute_down, "energy")
                            textbutton "[mc.entropy]" text_size 30:
                                action Function(mc.attribute_down, "entropy")
                            textbutton "[mc.influence]" text_size 30:
                                action Function(mc.attribute_down, "influence")
                            textbutton "[mc.movement]" text_size 30:
                                action Function(mc.attribute_down, "movement")
                            textbutton "[mc.prescience]" text_size 30:
                                action Function(mc.attribute_down, "prescience")
                            textbutton "[mc.protection]" text_size 30:
                                action Function(mc.attribute_down, "protection")

screen favored_actions_menu(): #here's where we can list out the player's favored actions (or character abilities or bane/boon choices)

    # creates a tooltip variable that we can have show later
    $ tooltip = GetTooltip()
    if tooltip:
        text "[tooltip]"

    #below defined variables allows us to pull from our various lists needed to make this screen work
    #lets us pull from the player's baneboon list by creating a mirror of it
    default baneboons_list = mc.baneboons
    #lets us pull from the player's attribute_used list by creating a mirror of it
    default attrubutes_used_list = mc.attribute_used
    #lets us pull from a copy of the Bane or Boon's attribute list that we can select from to add to the player's attribute_used list later
    default attribute_list_temp = att_list
    #lets us pull the baneboon dictionary by creating a mirror of it
    default descriptions = mc.descriptions
        
    frame: #a frame where we can provide a background picture
        align (0.5, 0.5) #align to center
        padding (0,0) #our padding, which is currently set to 0 so it doesn't default to something else
        
        viewport: #a grid that contains the textbuttons which control increasing or decreasting on of Open Legend's Attributes
            xsize 1344
            ysize 972

            viewport: # menu navigation buttons with scrollbar in case we ever need it - copied into each menu so we don't have to have multiple popups
                xsize 384
                align (0,0)
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox: #a vertical box containing navigation buttons, can be added to if need be
                    textbutton "Main" action [Hide(),ShowMenu("character_menu")] #hids current, shows the called menu
                    textbutton "Attributes" action [Hide(), ShowMenu("level_up_menu")]
                    textbutton "Banes & Boons" action [Hide(), ShowMenu("favored_actions_menu")]
                    textbutton "Equipment" action [Hide(), ShowMenu("equipment")]
                    textbutton "Feats" action [Hide(), ShowMenu("feats")]
                    textbutton "Perks" action [Hide(), ShowMenu("perks")]
                    textbutton "Flaws" action [Hide(), ShowMenu("flaws")]
                    textbutton "Quests" action [Hide(), ShowMenu("quests")]
                    textbutton "Return" action [Return()] #closes the menu
            
            viewport:
                pos(0.3,0.01)
                xsize 960
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox:
                    textbutton "Add a Bane or Boon":
                        action ShowMenu("baneboon_menu")
                    vbox:
                        spacing 10
                        for index, item in enumerate(baneboons_list):
                                frame:
                                    has fixed
                                    yfit True
                                    xsize 905
                                    vbox:
                                        text "[item]"
                                        text "Uses: [mc.list_attribute_used(index)]"
                                        text "Description:"
                                        textbutton "[mc.list_descriptions(index)]" action [SetVariable("descript_index", index), Show("text_input_screen")]

screen text_input_screen(): #screen for input
    frame:
        align (0.5, 0.5)
        #below defined variables allows us to pull from our various lists needed to make this screen work
        #lets us pull from the player's baneboon list by creating a mirror of it
        default baneboons_list = mc.baneboons
        #lets us pull the baneboon dictionary by creating a mirror of it
        default descriptions = mc.descriptions
        default screenvar = False
        vbox:
            imagemap:
                ground "background.png"
                idle "idle.png"
                hover "hover.png"
                selected_idle "hover.png"

                hotspot (150,140,475,200) action SetScreenVariable("screenvar",True)
                if screenvar == True:
                    
                    input default ability_description pos(200,165) value VariableInputValue("ability_description")
            textbutton "Save":
                align (0.5, 0.5)
                action [Function(mc.add_descriptions, ability_description, descript_index), Hide("text_input_screen")]

screen baneboon_menu(): #menu for creating our banes and boons actions the player can use during the game

    $ tooltip = GetTooltip() #allows us to add tooltips if we want
    if tooltip:
        text "[tooltip]"

    #below defined variables allows us to pull from our various lists needed to make this screen work
    #lets us pull from the player's baneboon list
    default baneboons_list = mc.baneboons
    #lets us pull from the player's attribute_used list
    default attrubutes_used_list = mc.attribute_used
    #lets us pull from a copy of the Bane or Boon's attribute list that we can select from to add to the player's attribute_used list later
    default attribute_list_temp = att_list
    #lists our banes
    $ banes = Bane.instances
    $ boons = Boon.instances
        
    frame: #adds our backdrop
        align (0.5, 0.5) #aligns it to center

        vbox:
            textbutton "Return": #just a textbutton that lets us hide this screen
                action Hide()
                align (0.5, 0.5)
            grid 2 2:
                
                vbox: #Banes
                    text "Banes" xalign 0.5
                    viewport:
                        scrollbars "vertical" #adds a scroll bar
                        xmaximum 400
                        ymaximum 400
                        mousewheel True #lets us use the mousewheel
                        has vbox
                        vbox: #vertical box containing the banes
                            for item in banes: #lists out all banes
                                textbutton "[item]": #creates a textbutton for each bane
                                    action Function(mc.add_baneboons, item) #adds the bane to our favored actions (baneboons)
                vbox: #Attribute Used
                    text "Attribute Used" xalign 0.5
                    viewport:
                        scrollbars "vertical"
                        xmaximum 400
                        ymaximum 400
                        mousewheel True
                        has vbox
                        vbox: #vertical box containing the attributes a bane or boon uses
                            for item in attribute_list_temp: #lists them out for us
                                textbutton "[item]": #makes a textbutton for each
                                    action Function(mc.add_attribute_used,item) #adds the attribute used to our list of attributes used
                vbox: #Boons
                    text "Boons" xalign 0.5
                    viewport:
                        scrollbars "vertical"
                        xmaximum 400
                        ymaximum 400
                        mousewheel True
                        has vbox
                        vbox: #works just like the banes section, but for boons
                            for item in boons:
                                textbutton "[item]":
                                    action Function(mc.add_baneboons, item)
                vbox: #Our baneboons with attribute_used - AKA Favored Actions
                    text "Favored Actions" xalign 0.5
                    viewport:
                        scrollbars "vertical"
                        xmaximum 400
                        ymaximum 400
                        mousewheel True
                        has vbox
                        vbox: #similar to our previous iterated textbuttons, but now lists "Bane/Boon : Attribute_Used"
                            for index, item in enumerate(baneboons_list):
                                textbutton "[item] : [mc.list_attribute_used(index)]":
                                    action [Function(mc.remove_baneboons, item),SetVariable("attribute_added", True), Function(att_list.temp_list.clear)] #removes the item, and resets our attribute_used toggle

screen equipment():

    default equipment = mc.equipment

    frame: #a frame where we can provide a background picture
        align (0.5, 0.5) #align to center
        padding (0,0) #our padding, which is currently set to 0 so it doesn't default to something else
        
        viewport: #a grid that contains the textbuttons which control increasing or decreasting on of Open Legend's Attributes
            xsize 1344
            ysize 972

            viewport: # menu navigation buttons with scrollbar in case we ever need it - copied into each menu so we don't have to have multiple popups
                xsize 384
                align (0,0)
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox: #a vertical box containing navigation buttons, can be added to if need be
                    textbutton "Main" action [Hide(),ShowMenu("character_menu")] #hids current, shows the called menu
                    textbutton "Attributes" action [Hide(), ShowMenu("level_up_menu")]
                    textbutton "Banes & Boons" action [Hide(), ShowMenu("favored_actions_menu")]
                    textbutton "Equipment" action [Hide(), ShowMenu("equipment")]
                    textbutton "Feats" action [Hide(), ShowMenu("feats")]
                    textbutton "Perks" action [Hide(), ShowMenu("perks")]
                    textbutton "Flaws" action [Hide(), ShowMenu("flaws")]
                    textbutton "Quests" action [Hide(), ShowMenu("quests")]
                    textbutton "Return" action [Return()] #closes the menu
            
            viewport:
                xsize 960
                pos(0.3,0.01)
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox:
                    xsize 905
                    spacing 10
                    text "Equipment"
                    vbox:
                        spacing 10
                        for item in equipment:
                                frame:
                                    has fixed
                                    yfit True
                                    xsize 905
                                    vbox:
                                        text "[item.name]"
                                        text "[item.description]"

screen feats():
    frame: #a frame where we can provide a background picture
        align (0.5, 0.5) #align to center
        padding (0,0) #our padding, which is currently set to 0 so it doesn't default to something else
        
        viewport: #a grid that contains the textbuttons which control increasing or decreasting on of Open Legend's Attributes
            xsize 1344
            ysize 972

            viewport: # menu navigation buttons with scrollbar in case we ever need it - copied into each menu so we don't have to have multiple popups
                xsize 384
                align (0,0)
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox: #a vertical box containing navigation buttons, can be added to if need be
                    textbutton "Main" action [Hide(),ShowMenu("character_menu")] #hids current, shows the called menu
                    textbutton "Attributes" action [Hide(), ShowMenu("level_up_menu")]
                    textbutton "Banes & Boons" action [Hide(), ShowMenu("favored_actions_menu")]
                    textbutton "Equipment" action [Hide(), ShowMenu("equipment")]
                    textbutton "Feats" action [Hide(), ShowMenu("feats")]
                    textbutton "Perks" action [Hide(), ShowMenu("perks")]
                    textbutton "Flaws" action [Hide(), ShowMenu("flaws")]
                    textbutton "Quests" action [Hide(), ShowMenu("quests")]
                    textbutton "Return" action [Return()] #closes the menu
            
            viewport:
                pos(0.3,0.01)
                xsize 960

screen perks():

    default char_perks = mc.perks
    default char_flaws = mc.flaws
    $ perks = Perk.instances
    $ flaws = Flaw.instances

    frame: #a frame where we can provide a background picture
        align (0.5, 0.5) #align to center
        padding (0,0) #our padding, which is currently set to 0 so it doesn't default to something else
        
        viewport:
            xsize 1344
            ysize 972

            viewport: # menu navigation buttons with scrollbar in case we ever need it - copied into each menu so we don't have to have multiple popups
                xsize 384
                align (0,0)
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox: #a vertical box containing navigation buttons, can be added to if need be
                    textbutton "Main" action [Hide(),ShowMenu("character_menu")] #hids current, shows the called menu
                    textbutton "Attributes" action [Hide(), ShowMenu("level_up_menu")]
                    textbutton "Banes & Boons" action [Hide(), ShowMenu("favored_actions_menu")]
                    textbutton "Equipment" action [Hide(), ShowMenu("equipment")]
                    textbutton "Feats" action [Hide(), ShowMenu("feats")]
                    textbutton "Perks" action [Hide(), ShowMenu("perks")]
                    textbutton "Flaws" action [Hide(), ShowMenu("flaws")]
                    textbutton "Quests" action [Hide(), ShowMenu("quests")]
                    textbutton "Return" action [Return()] #closes the menu
            
            viewport:
                xsize 960
                pos(0.3,0.01)
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox:
                    vbox:
                        xsize 905
                        spacing 10
                        text "Current Perks"
                        vbox:
                            spacing 10
                            for item in char_perks:
                                    frame:
                                        has fixed
                                        yfit True
                                        xsize 905
                                        vbox:
                                            text "[item.name]"
                                            text "[item.description]"
                    vbox:
                        text "Perks List"
                        viewport:
                            has vbox
                            vbox:
                                spacing 10
                                if len(char_perks) < 2:
                                    for index, item in enumerate(perks):
                                            frame:
                                                has fixed
                                                yfit True
                                                xsize 905
                                                vbox:
                                                    text "[item.name]"
                                                    text "[item.description]"
                                                    textbutton "Add Perk" action Function(mc.add_perk,item)
                                else:
                                    text "You've selected all of your Perks"

screen flaws():

    default char_perks = mc.perks
    default char_flaws = mc.flaws
    $ perks = Perk.instances
    $ flaws = Flaw.instances

    frame: #a frame where we can provide a background picture
        align (0.5, 0.5) #align to center
        padding (0,0) #our padding, which is currently set to 0 so it doesn't default to something else
        
        viewport:
            xsize 1344
            ysize 972

            viewport: # menu navigation buttons with scrollbar in case we ever need it - copied into each menu so we don't have to have multiple popups
                xsize 384
                align (0,0)
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox: #a vertical box containing navigation buttons, can be added to if need be
                    textbutton "Main" action [Hide(),ShowMenu("character_menu")] #hids current, shows the called menu
                    textbutton "Attributes" action [Hide(), ShowMenu("level_up_menu")]
                    textbutton "Banes & Boons" action [Hide(), ShowMenu("favored_actions_menu")]
                    textbutton "Equipment" action [Hide(), ShowMenu("equipment")]
                    textbutton "Feats" action [Hide(), ShowMenu("feats")]
                    textbutton "Perks" action [Hide(), ShowMenu("perks")]
                    textbutton "Flaws" action [Hide(), ShowMenu("flaws")]
                    textbutton "Quests" action [Hide(), ShowMenu("quests")]
                    textbutton "Return" action [Return()] #closes the menu
            
            viewport:
                xsize 960
                pos(0.3,0.01)
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox:
                    vbox:
                        xsize 905
                        spacing 10
                        text "Current Flaws"
                        vbox:
                            spacing 10
                            for item in char_flaws:
                                    frame:
                                        has fixed
                                        yfit True
                                        xsize 905
                                        vbox:
                                            text "[item.name]"
                                            text "[item.description]"
                    vbox:
                        text "Flaws List"
                        viewport:
                            has vbox
                            vbox:
                                spacing 10
                                if len(char_flaws) < 2:
                                    for index, item in enumerate(flaws):
                                            frame:
                                                has fixed
                                                yfit True
                                                xsize 905
                                                vbox:
                                                    text "[item.name]"
                                                    text "[item.description]"
                                                    textbutton "Add Flaw" action Function(mc.add_flaw,item)
                                else:
                                    text "You've selected all of your Flaws"

screen quests():
    frame: #a frame where we can provide a background picture
        align (0.5, 0.5) #align to center
        padding (0,0) #our padding, which is currently set to 0 so it doesn't default to something else
        
        viewport: #a grid that contains the textbuttons which control increasing or decreasting on of Open Legend's Attributes
            xsize 1344
            ysize 972

            viewport: # menu navigation buttons with scrollbar in case we ever need it - copied into each menu so we don't have to have multiple popups
                xsize 384
                align (0,0)
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox: #a vertical box containing navigation buttons, can be added to if need be
                    textbutton "Main" action [Hide(),ShowMenu("character_menu")] #hids current, shows the called menu
                    textbutton "Attributes" action [Hide(), ShowMenu("level_up_menu")]
                    textbutton "Banes & Boons" action [Hide(), ShowMenu("favored_actions_menu")]
                    textbutton "Equipment" action [Hide(), ShowMenu("equipment")]
                    textbutton "Feats" action [Hide(), ShowMenu("feats")]
                    textbutton "Perks" action [Hide(), ShowMenu("perks")]
                    textbutton "Flaws" action [Hide(), ShowMenu("flaws")]
                    textbutton "Quests" action [Hide(), ShowMenu("quests")]
                    textbutton "Return" action [Return()] #closes the menu
            
            viewport:
                pos(0.3,0.01)
                xsize 960

screen test_list():

    $ mc.update_favored_actions()
    default test_list = mc.favored_actions_touple

    frame: #a frame where we can provide a background picture
        align (0.5, 0.5) #align to center
        padding (0,0) #our padding, which is currently set to 0 so it doesn't default to something else
        
        viewport: #a grid that contains the textbuttons which control increasing or decreasting on of Open Legend's Attributes
            xsize 1344
            ysize 972

            viewport: # menu navigation buttons with scrollbar in case we ever need it - copied into each menu so we don't have to have multiple popups
                xsize 384
                align (0,0)
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox: #a vertical box containing navigation buttons, can be added to if need be
                    textbutton "Main" action [Hide(),ShowMenu("character_menu")] #hids current, shows the called menu
                    textbutton "Attributes" action [Hide(), ShowMenu("level_up_menu")]
                    textbutton "Banes & Boons" action [Hide(), ShowMenu("favored_actions_menu")]
                    textbutton "Equipment" action [Hide(), ShowMenu("equipment")]
                    textbutton "Feats" action [Hide(), ShowMenu("feats")]
                    textbutton "Perks" action [Hide(), ShowMenu("perks")]
                    textbutton "Flaws" action [Hide(), ShowMenu("flaws")]
                    textbutton "Quests" action [Hide(), ShowMenu("quests")]
                    textbutton "Test List" action [Hide(), ShowMenu("test_list")]
                    textbutton "Return" action [Return()] #closes the menu
            
            viewport:
                pos(0.3,0.01)
                xsize 960
                scrollbars "vertical" #adds a scroll bar
                mousewheel True #lets us use the mousewheel
                has vbox
                vbox:
                    spacing 10
                    for index, item in enumerate(test_list):
                            frame:
                                has fixed
                                yfit True
                                xsize 905
                                vbox:
                                    text "[item[0]]"
                                    text "[item[1]]"
