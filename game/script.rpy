# The script of the game goes in this file.


#here is our Main Character or mc for short
default mc = Character_Sheet(character = Character("Main_Character", color="FF0000"), name = "MC", armor=0, agility=0, fortitude=0, might=0, learning=0, logic=0, perception=0, will=0, deception=0, persuasion=0, presence=0, alteration=0, creation=0, energy=0, entropy=0, influence=0, movement=0, prescience=0, protection=0, attribute_pts=40, level=1, toughness=0, guard=0, resolve=0, max_hitpoints=0, hitpoints=0, feat_pts=6, wealth_score=2)
$ quick_menu = True

label start: # The game starts here.

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene zombie_fight
    show screen level_up_UI

    "Text for Test, Enter to start fight screen"

    menu:

        "Call Character Creation":
            jump character_creation
        "Battle Test":
            jump testBattle
        "Shop Test":
            jump shop
        "Call Start":
            jump start
        

    return

label character_creation:

    $ mc.name = renpy.input("Enter your name:")

    if mc.name == "":
        $ mc.name = "Luna"

    "Of course, you're name is [mc.name]. How could I forget?"

    "[mc.name], this game assumes you're familiar with the Open Legends Tabletop Roleplay Game."

    "If you click on the Stats UI, you can select your attributes and view your stats. Click the name of the attribute to add one, or click the number to reduce by one."

    "While on the Stats UI screen, you'll notice a button in the top left hand corner. This allows you to pick character abilities."

    "Go ahead and click on it now, set your starting attributes, and select an ability or two."

    "Currently, you can change these at any time."

    "[mc.name], have you set your attributes and select an ability or two?"

    menu:
        "Yes, I'm ready for my single player Open Legend Adventure!":
            jump start
        "Oh, that's the name I picked? Uhm, maybe I should start over...":
            jump character_creation

label testBattle:
    
    #battle test
    $ mc.update_favored_actions()
    $ mc.hitpoints = mc.max_hitpoints   #this resets MC HP back to max
    $ enemy.hitpoints = enemy.max_hitpoints #this resets enemy HP back to max
    $ print(mc.favored_actions_touple)
    scene dark_city

    "A monster appears in the streets!"

    show armanite

    default player_initiative = dice_roll(mc.agility)
    default enemy_initiative = dice_roll(enemy.agility)

    "You rolled [player_initiative] for initiative."

    "The enemy rolled [enemy_initiative] for initiative."

    if player_initiative >= enemy_initiative:
        "The enemy is attacking! You quickly get your footing, and attack first!"
        call player_attack
    else:
        "The enemy is attacking! You lose your footing, and your enemy attacks first!"
        call enemy_attack
   
label player_attack: #controls combat with player first

    while mc.hitpoints > 0 and enemy.hitpoints > 0:

        #TO DO: add multi targets and such
        #menu player_attack_choice:
        #    "Enemy 1" if enemy.hitpoints > 0:
        #        $ enemy_count = 1

        #player turn, will add banes and boons later
        menu:
            "Basic Attack":
                menu:
                    "Might [mc.might]" if mc.might >= 1:
                        $ mc.base_attack(mc.might, enemy, enemy.guard)
                    "Agility [mc.agility]" if mc.agility >= 1:
                        $ mc.base_attack(mc.agility, enemy, enemy.guard)
                    "Energy [mc.energy]" if mc.energy >= 1:
                        $ mc.base_attack(mc.energy, enemy, enemy.guard)
                    "Entropy [mc.entropy]" if mc.entropy >= 1:
                        $ mc.base_attack(mc.entropy, enemy, enemy.toughness)
            "Favored Actions":
                # Display the dynamic menu and get the player's choice
                $ favored_actions = renpy.display_menu(mc.favored_actions_touple)
                $ print(f"Debug: action_message = {repr(favored_actions)}")
                # Output the selected action's message
                "[favored_actions]"
            "Exit Test":
                jump start

        if enemy.hitpoints <= 0:
            "You win the combat encounter!"
            jump start

        #Enemy Turn

        $ randability = renpy.random.randint(1, 4) #rolls a dice to determine random ability used by the enemy
        if randability >= 3:
            "Your enemy comes at you slamming their fists!"
            $ enemy.base_attack(enemy.might, mc, mc.guard)
        else:
            "They do nothing."

        if mc.hitpoints <= 0:
            "You lose the combat encounter!"
            jump start

label enemy_attack: #controls combat with player first

    while mc.hitpoints > 0 and enemy.hitpoints > 0:

        #TO DO: add multi targets and such
        #menu player_attack_choice:
        #    "Enemy 1" if enemy.hitpoints > 0:
        #        $ enemy_count = 1

        #Enemy Turn

        $ randability = renpy.random.randint(1, 4) #rolls a dice to determine random ability used by the enemy
        if randability >= 3:
            "Your enemy comes at you slamming their fists!"
            $ enemy.base_attack(enemy.might, mc, mc.guard)
        else:
            "They do nothing."

        if mc.hitpoints <= 0:
            "You lose the combat encounter!"
            jump start

        #player turn, will add banes and boons later
        menu:
            "Attack":
                menu:
                    "Might [mc.might]" if mc.might >= 1:
                        $ mc.base_attack(mc.might, enemy, enemy.guard)
                    "Agility [mc.agility]" if mc.agility >= 1:
                        $ mc.base_attack(mc.agility, enemy, enemy.guard)
                    "Energy [mc.energy]" if mc.energy >= 1:
                        $ mc.base_attack(mc.energy, enemy, enemy.guard)
                    "Entropy [mc.entropy]" if mc.entropy >= 1:
                        $ mc.base_attack(mc.entropy, enemy, enemy.toughness)
            "Favored Actions":
                # Display the dynamic menu and get the player's choice
                $ favored_actions = renpy.display_menu(mc.favored_actions_touple)
                $ print(f"Debug: action_message = {repr(favored_actions)}")
                # Output the selected action's message
                "[favored_actions]"
            "Exit Test":
                jump start

        if enemy.hitpoints <= 0:
            "You win the combat encounter!"
            jump start

label shop:

    menu:
        "Call Start":
            jump start



        