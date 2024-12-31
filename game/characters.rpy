#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# For ease, I will be documenting things as though you are somewhat familiar with Tabletop RPGs, and Open Legends.
# I will try and stick to language used by the Open Legends core rules for certain things such as "Attributes"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

init python:
    class Character_Sheet: # Plays the roll of a blank character sheet in Open Legend
        def __init__(self, character, name, agility, fortitude, might, learning, logic, perception, will, deception, persuasion, presence, alteration, creation, energy, entropy, influence, movement, prescience, protection, attribute_pts, level, feat_pts, wealth_score, armor, toughness, guard, resolve, max_hitpoints, hitpoints): 
            
            # Basic Character Information
            self.c = character # Used for calling the character, will need to type out luna.c for example
            self.name = name # Name used for the character
            self.perks = [] # A list of the player's chosen perks
            self.flaws = [] # A list of the player's chosen flaws

            # Character Attributes
            self.agility = agility 
            self.fortitude = fortitude
            self.might = might
            self.learning = learning
            self.logic = logic
            self.perception = perception
            self.will = will
            self.deception = deception
            self.persuasion = persuasion
            self.presence = presence
            self.alteration = alteration
            self.creation = creation
            self.energy = energy
            self.entropy = entropy
            self.influence = influence
            self.movement = movement
            self.prescience = prescience
            self.protection = protection

            # Levels and Points
            self.attribute_pts = attribute_pts # Holds an amount of points used in increasing an attribute on the level up screen
            self.level = level # The character level
            self.feat_pts = feat_pts # Feat Points used to buy feats in the level up screen
            self.wealth_score = wealth_score # The character's wealth score, used with purchasing items in a shop or such

            # Defensive Stats
            self.armor = armor # Adds an Armor Bonus to Guard
            self.toughness = 10 + self.fortitude + self.will
            self.guard = 10 + self.agility + self.might + self.armor
            self.resolve = 10 + self.presence + self.will
            self.max_hitpoints = 2 * (self.fortitude + self.presence + self.will) + 10 # Holds the max amount of HP a character has so we can reset to this number after combat
            self.hitpoints = self.max_hitpoints # Holds the current amount of HP a character has during combat

            # Favored Actions
            self.baneboons = [] # A list of the character's banes and boons
            self.attribute_used = [] # A list of the attributes used with the banes and boons in the baneboons list
            self.baneboon_dict = dict(zip(self.baneboons, self.attribute_used)) # Creates a dictionary of the Banes/Boons and the Attributes the player wants to use for them
            self.descriptions = [] # A list of the player's descriptions of their banes and boons
            self.equipment = [] #holds a list of the player's equipment
            self.equipment_descriptions = [] #holds a list of descriptions of using equipment
            self.favored_actions_touple = list(zip(self.baneboons, self.descriptions)) # A touple with all of our Favored Actions - Banes, Boons, and Equipment actions (Work in progress)

            # Other information to keep track of
            self.conditions = {} # A dictionary of conditions effecting the Actor during combat

        def __iter__(self): # Make the self.baneboons iterable
            return iter(self.baneboons)

        def __iter__(self): # Make the self.attribute_used iterable
            return iter(self.attribute_used)

        def __iter__(self): # Make the self.equipment iterable
            return iter(self.equipment)

        # Functions for our Character Attributes on the Character_Sheet

        def attribute_up(self, att_name_str): # Handles when a player increases their Character Attribute Score in the level-up menu, and 
            # att_name_str should be the Character Attribute that you wish to increase
            att_name_up = getattr(self, att_name_str)  # Get the current value of the attribute
            if (att_name_up == 5) and (self.level == 1): # Checks if the attribute score is 5, and if the level is 1. So a level one character doesn't have a 6 in any one attribute.
                renpy.notify("Need to be higher than level 1!") # Notify the player
            elif (att_name_up == 9): # Caps the attribute score at 9 via this method. 10 is still achievable via other methods.
                renpy.notify("Can't purchase a 10 in your attributes with points!") # Notify the player
            elif (self.attribute_pts < sum_up_to(att_name_up + 1)): # Checks to make sure we have enough attribute points to purchase the attribute score increase
                renpy.notify("Not enough Attribute Points!") # Notify the player
            else: # Now that we've confirmed we have enough attribute points, and we haven't hit our limits
                self.attribute_pts -= sum_up_to(att_name_up + 1) # The amount of attribute points used to purchase the level is the sum of every number up to the level we're purchasing
                att_name_up += 1 # Adds one to the attribute score
                setattr(self, att_name_str, att_name_up) # Dynamically set the updated attribute value
                att_name_up = sum_up_to(att_name_up + 1) # Handles some math in the background in case the player is spamming the button
            self.update_derived_attributes() # Calls for the function that updates our defensive stats
                  
        def attribute_down(self, att_name_str): # Handles when a player reduces a Character Attribute Score in the level-up menu
            # att_name_str should be the Character Attribute that you wish to decrease
            att_name_up = getattr(self, att_name_str)  # Get the current value of the attribute
            self.attribute_pts += sum_up_to(att_name_up) # Handles the math to give back the attribute points used
            if att_name_up > 0: #makes sure we don't reduce an attribute to a negative number
                att_name_up -= 1 #decrement the attribute
                setattr(self, att_name_str, att_name_up) # Dynamically set the updated attribute value
            self.update_derived_attributes() #updates the defensive stats
     
        def update_derived_attributes(self): #used to help recalulate toughness, guard, resolve, max hp, and hp in the attribute_up and down functions
            self.toughness = 10 + self.fortitude + self.will
            self.guard = 10 + self.agility + self.might + self.armor
            self.resolve = 10 + self.presence + self.will
            self.max_hitpoints = 2 * (self.fortitude + self.presence + self.will) + 10
            self.hitpoints = self.max_hitpoints

        # Functions for our various lists on the Character_Sheet

        def add_baneboons(self, baneboons): # Adds a Bane or Boon to our list of Banes and Boons (self.baneboons) on Character_Sheet
            global attribute_added # Access a bool variable we will use as a toggle when a Character Attribute is selected to use the Bane or Boon with. See add_attribute_used.
            if not attribute_added and baneboons: # If our bool variable is not toggled, then doesn't allow a new Bane or Boon to be added. If not, then we need to pick an attribute
                renpy.notify("You need to select an attribute to use before adding more Banes or Boons.")
            else:
                if len(self.baneboons) < 12: # Caps the amount of banes/boons a player. You can set the number to something else if you think 12 is too few, but you'll need to update other functions below.
                    self.baneboons.append(baneboons.name) # Append the function's input (the Bane or Boon) into the baneboons list.
                    self.descriptions.append(baneboons.description) # Append the Bane or Boon's default description to the self.description list. 
                    renpy.notify("Select an attribute used for the Bane or Boon.")
                    att_list.attribute_list(baneboons) # Calls for an Attribute List to created using the Bane or Boon's required Character Attributes
                    self.update_favored_actions() # Runs the function to update our Favored Actions touple
                    attribute_added = False #this is our toggle saying "okay we selected our bane/boon, now we need an attribute to go with it"
        
        def remove_baneboons(self, baneboons): # Removes Banes/Boons and their corresponding attributes_used and descriptions from the self.baneboons list
            if baneboons in self.baneboons: # Checks if the bane/boon is on our list to avoid errors
                index = self.baneboons.index(baneboons) # Looks for the index of the bane/boon to use later
                if index >= len(self.attribute_used): # Checks if there's anything at that index
                    pass #if nothing, pass
                else:
                    self.attribute_used.pop(index) #if something, removes the attribute_used at the index of the bane/boon
                    self.descriptions.pop(index)
                self.baneboons.remove(baneboons) #removes the bane/boon
                mc.update_favored_actions()        

        def list_baneboons(self, index): # Call the Bane or Boon at the index number
            if 0 <= index < len(self.baneboons): # Checks to make sure there's something at the index number
                return self.baneboons[index] # If so, provides what's at that index number
            else:
                return None

        def add_descriptions(self, descriptions, index): # Adds or Replaces a Description in the self.descriptions list
            if len(self.descriptions) < 12: # Caps the amount of descriptions.
                if 0 <= index <= len(self.descriptions):  # Check if index is valid
                    self.descriptions[index] = descriptions # Replace description at index
                else:
                    self.descriptions.insert(index, descriptions) # Insert description at index if nothing is there
            else:
                renpy.notify("Error: Description not saved")
            self.update_favored_actions() # Function to update our Favored Actions Touple

        def list_descriptions(self, index): # Allows listing a Description using the index number
            if 0 <= index < len(self.descriptions): #checks to make sure there's something at the index number
                return self.descriptions[index] #if so, provides what's at that index number
            else:
                return None

        def add_attribute_used(self, attribute_used): # Adds the attribute_used for a Bane or Boon to a list
            global attribute_added # Calls the bool variable
            if len(self.attribute_used) < 12: # Caps the amount of attribute_used a player can have to match the cap of Banes/Boons
                self.attribute_used.append(attribute_used) # Appends to the attribute_used list
                attribute_added = True # This is our toggle to say "we added an attribute for the Bane/Boon we chose"
                att_list.temp_list.clear() # Clears the temporary list of Character Attributes so a player can't accidentally add another.
        
        def list_attribute_used(self, index): # Calls a specific Attribute Used at the index provided
            if 0 <= index < len(self.attribute_used): # Checks the index number we provide
                return self.attribute_used[index] # If something is there, provide it
            else:
                return None

        def update_favored_actions(self): # Updates our favored_actions_touple AND baneboon_dict when we call it
            self.favored_actions_touple = list(zip(self.baneboons, self.descriptions))
            self.baneboon_dict = dict(zip(self.baneboons, self.attribute_used))

        # Functions for combat actions

        def base_attack(self, attribute, target, target_defense): # Handles the base attack to deal damage, not used for Banes or Boons      
            attack_roll = dice_roll(attribute) # Assigns the variable, which is made by the dice_roll function, passing in the attribute we feed the base_attack function
            renpy.say(narrator, f"{self.name} rolled a {attack_roll}!") # Tells the player what the roll was
            damage = attack_roll - target_defense # Maths out the damage dealt according to the Open Legend's rules
            # See: Open Legend's Core Mechanic in Combat - in this instance, there is no option, as Deal 3 Damage is pre-selected for the player. I intend to update this.
            if damage <= 3: # If less than or equal to three, we'll update the damage variable
                damage = 3
                target.take_damage(3) # Calls the damage function
                renpy.say(narrator,"And only deals 3 damage...") # Tells the player how much damage was dealt
            else:
                target.take_damage(damage) # Calls the damage function
                renpy.say(narrator,"And attacks for %i damage!" % (damage)) # Tells the player how much damage was dealt

        def adv_attack(self, attribute, target, target_defense, advantage=0, disadvantage=0): # FOR TEST PURPOSES
            attack_roll = dice_roll(attribute, advantage, disadvantage) # Assigns the variable, which is made by the dice_roll function, passing in the attribute we feed the base_attack function
            renpy.say(narrator, f"{self.name} rolled a {attack_roll}!") # Tells the player what the roll was
            damage = attack_roll - target_defense # Maths out the damage dealt according to Open Legend's rules
            if damage <= 3: # If less than or equal to three, we'll update the damage variable
                damage = 3
                target.take_damage(3) # Handles the damage
                renpy.say(narrator,"And only deals 3 damage...") # Tells the player how much damage was dealt
            else:
                target.take_damage(damage) # Handles the damage
                renpy.say(narrator,"And attacks for %i damage!" % (damage)) # Tells the player how much damage was dealt

        def take_damage(self, damage): # Handles the damage math in attacks
            self.hitpoints -= damage # Simple math, but by having a function for the math, we can implement this in the Renpy Script with other uses. Ex: Self damage during a ritual, Traps, etc.

        # Perks and Flaws

        def add_perk(self, perk):
            if len(self.perks) < 2: # Caps the amount a player can have
                    self.perks.append(perk) # Appends to the list

        def add_flaw(self, flaw):
            if len(self.flaws) < 2: # Caps the amount a player can have
                    self.flaws.append(flaw) # Appends to the list

        # Banes and Boons - Work In Progress

        def bane_attack (self, bane, target): # Rolls the dice to see if a Bane works
            attribute = self.baneboon_dict.get(bane) # Finds the attribute used for the Bane in the player's baneboon dictionary
            defense = bane.attribute_dict.get(attribute) # Finds the attribute used to defend against the bane, should search the Bane's dictionary for the corresponding defense
            attack_roll = dice_roll(attribute) # Rolls the dice
            renpy.say("%s rolled a %i!" % (self.name, attack_roll))
            if attack_roll > target.defense:
                apply_baneboon(bane) # Calls for the function to find the bane to apply, which will then apply the bane
            else:
                renpy.say("But misses...")

        def boon_use(self, boon, target): # Similar to bane_attack, but Boons (WIP)
            attribute = self.baneboon_dict.get(boon) # Finds the attribute used for the Boon in the player's baneboon dictionary
            ability_roll = dice_roll(attribute) # Rolls the dice
            renpy.say("%s rolled a %i!" % (self.name, attack_roll))
            power_level_list = boon.power_level.copy()

        def use_ability (self, name, target): # Call this first when using a bane or boon (WIP)
            if name in Bane.instances: # Checks to see if what we're feeding it is a Bane 
                bane_attack(name, target) # Calls for the function used to attack with a Bane, passing through the name and the target we already used
            elif name in Boon.instances: # checks to see if what we're feeding it is a Boon
                boon_use(name, target) # calls for the function used for using a Boon, passing through the name and the target we already used
            else: # and if for some reason this doesn't work...
                renpy.say("Bane or Boon Not Found?! Someone call the Devs!")

        def apply_condition(self, condition): #Apply a condition from a Bane or Boon
            self.conditions.append(condition)
            renpy.say(self.name, "[self.name] is now [condition.name]!")

        def remove_condition(self, condition): #Remove a condition from a Bane or Boon
            if condition in self.conditions:
                self.conditions.remove(condition)
                renpy.say(self.name, "[self.name] is no longer [condition.name]!")

        # Equipment - Work In Progress

        def add_equipment(self, equipment): # called when adding equipment
            # Does not handle purchasing math
            # Please see Carrying Capacity rules for Open Legend
            if not attribute_added and baneboons: 
                renpy.notify("You need to select an attribute to use before adding more Banes or Boons.")
            else:
                if len(self.baneboons) < 20: #caps equipment at 20 items
                    self.baneboons.append(baneboons.name) #append the function's input into the baneboons list
                    self.descriptions.append(baneboons.description)
                    renpy.notify("Select an attribute used for the Bane or Boon.")
                    att_list.attribute_list(baneboons) #calls for our attribute list to be created that we will choose from on the levelup screen
                    self.update_favored_actions()
                    attribute_added = False #this is our toggle saying "okay we selected our bane/boon, now we need an attribute to go with it"

    # Functions for Dice!

    def sum_up_to(n): # Used to determine math for attribute_up, mainly for how many attribute_pts needed for each increase
        x = sum(range(1, n + 1)) # Creates a range from 1 to one above the number we provide. Then adds the range together
        return x

    def generate_exploded_dice(min_value, max_value, rerolls=0): # Rolls dice with explosion mechanic, rerolling dice that explode.
        total = 0
        count = 0
        rolls = []
        
        def roll_die():
            roll = renpy.random.randint(min_value, max_value) # Random num gen for die rolls
            rolls.append(roll)  # Track the individual rolls
            return roll
        
        # Perform initial roll
        for _ in range(1 + rerolls):  # Initial roll plus any rerolls
            roll = roll_die()
            
            # If the die explodes (max value), we keep rerolling
            while roll == max_value:
                count += 1  # Count explosions
                roll = roll_die()  # Reroll the exploded die
            total += roll  # Add the final roll to the total

        return rolls, count

    def get_rerolls(advantage, disadvantage): # Returns how many extra dice to roll based on advantage/disadvantage.
        return max(advantage, disadvantage) 

    def dice_roll(power_level, advantage=0, disadvantage=0): # Roll dice based on power level and apply Advantage/Disadvantage logic
        dice_total = 0 #sum of dice

        rerolls = get_rerolls(advantage, disadvantage) # Determine the number of rerolls based on advantage and disadvantage

        # Base roll (d20 is always rolled once)
        d20, count_exploded_d20 = generate_exploded_dice(1, 20, rerolls=0)  # d20 rolls once, can explode
        d20_total = sum(d20)

        # For the other dice (d4, d6, d8, etc.), we'll roll them based on power level
        attribute_rolls = [] # A list of all of our rolls
        total_explosions = count_exploded_d20 #Starts our explosion count with how many times the d20 exploded first

        if power_level == 1:  # d20 + 1d4
            attribute_rolls, count_exploded_attribute = generate_exploded_dice(1, 4, rerolls=0 + rerolls)  # 1 base + rerolls
            total_explosions += count_exploded_attribute

        elif power_level == 2:  # d20 + 1d6
            attribute_rolls, count_exploded_attribute = generate_exploded_dice(1, 6, rerolls=0 + rerolls)  # 1 base + rerolls
            total_explosions += count_exploded_attribute

        elif power_level == 3:  # d20 + 1d8
            attribute_rolls, count_exploded_attribute = generate_exploded_dice(1, 8, rerolls=0 + rerolls)  # 1 base + rerolls
            total_explosions += count_exploded_attribute

        elif power_level == 4:  # d20 + 1d10
            attribute_rolls, count_exploded_attribute = generate_exploded_dice(1, 10, rerolls=0 + rerolls)  # 1 base + rerolls
            total_explosions += count_exploded_attribute

        elif power_level == 5:  # d20 + 2d6
            attribute_rolls, count_exploded_attribute = generate_exploded_dice(1, 6, rerolls=1 + rerolls)  # 2 base + rerolls
            total_explosions += count_exploded_attribute

        elif power_level == 6:  # d20 + 2d8
            attribute_rolls, count_exploded_attribute = generate_exploded_dice(1, 8, rerolls=1 + rerolls)  # 2 base + rerolls
            total_explosions += count_exploded_attribute

        elif power_level == 7:  # d20 + 2d10
            attribute_rolls, count_exploded_attribute = generate_exploded_dice(1, 10, rerolls=1 + rerolls)  # 2 base + rerolls
            total_explosions += count_exploded_attribute

        elif power_level == 8:  # d20 + 3d8
            attribute_rolls, count_exploded_attribute = generate_exploded_dice(1, 8, rerolls=2 + rerolls)  # 3 base + rerolls
            total_explosions += count_exploded_attribute

        elif power_level == 9:  # d20 + 3d10
            attribute_rolls, count_exploded_attribute = generate_exploded_dice(1, 10, rerolls=2 + rerolls)  # 3 base + rerolls
            total_explosions += count_exploded_attribute

        elif power_level == 10:  # d20 + 4d8
            attribute_rolls, count_exploded_attribute = generate_exploded_dice(1, 8, rerolls=3 + rerolls)  # 4 base + rerolls
            total_explosions += count_exploded_attribute

        # Apply Advantage or Disadvantage
        if advantage > 0:
            # Remove the lowest `advantage` number of rolls
            attribute_rolls.sort()  # Sort the rolls in ascending order
            print(f"Sorted Rolls: {attribute_rolls}") # For debugging
            attribute_rolls = attribute_rolls[advantage:]  # Keep the highest rolls after removing the lowest `advantage` rolls

        elif disadvantage > 0:
            # Remove the highest `disadvantage` number of rolls
            attribute_rolls.sort(reverse=True)  # Sort the rolls in descending order
            print(f"Sorted Rolls: {attribute_rolls}") # For debugging
            attribute_rolls = attribute_rolls[disadvantage:]  # Keep the lowest rolls after removing the highest `disadvantage` rolls

        # Sum the remaining rolls
        dice_total = d20_total + sum(attribute_rolls)

        # Notify player about the explosion count
        renpy.notify(f"The dice exploded {total_explosions} times!")

        print(f"Base roll (d20): {d20}") # For debugging
        print(f"Additional rolls: {attribute_rolls}") # For debugging

        return dice_total

    # Other classes

    class Bane: #allows us to make the different Banes from Open Legend, and holds their functions
        instances = []

        def __init__ (self, name, power_level, attack_attributes, attack_vs, invocation, duration, description, effect):
            self.name = name
            self.power_level = power_level
            self.attack_attributes = attack_attributes
            self.attack_vs = attack_vs
            self.invocation = invocation
            self.duration = duration
            self.description = description
            self.effect = effect
            self.attribute_dict = dict(zip(self.attack_attributes, self.attack_vs))
            self.original_values = {} #Store original attribute values for easy restoration
            
            Bane.instances.append(self) # Append this instance to the class-level 'instances' list

        def __repr__(self):
            return f"{self.name}"
        
        def __iter__(self): # Make the class iterable
            # Return an iterator over the list
            return iter(Bane.instances)

        def apply_blinded(self, character): #applys the effects of the bane Blinded
                self.original_values['guard'] = character.guard #stores the original value
                character.guard -= 3  
                return f"{character.name} is blinded! Guard is reduced by 3."



        def apply_charmed(target):
            # Apply the Charmed status effect.
            # Add logic to apply the Charmed effect (e.g., target is friendly towards the caster)
            pass

        def apply_deafened(target):
            # Apply the Deafened status effect.
            # Add logic to apply the Deafened effect (e.g., target can't hear, can be immune to sound-based effects)
            pass

        def apply_death(target):
            # Apply the Death status effect.
            # Add logic to apply the Death effect (e.g., target is dead, remove from game)
            pass

        def apply_demoralized(target):
            # Apply the Demoralized status effect.
            # Add logic to apply the Demoralized effect (e.g., target suffers penalties to attacks or morale)
            pass

        def apply_disarmed(target):
            # Apply the Disarmed status effect.
            # Add logic to apply the Disarmed effect (e.g., target drops their weapon, can't use it)
            pass

        def apply_dominated(target):
            # Apply the Dominated status effect.
            # Add logic to apply the Dominated effect (e.g., target is controlled by another entity)
            pass

        def apply_fatigued(target):
            # Apply the Fatigued status effect.
            # Add logic to apply the Fatigued effect (e.g., target suffers penalties to physical actions)
            pass

        def apply_fear(target):
            # Apply the Fear status effect.
            # Add logic to apply the Fear effect (e.g., target is frightened, must flee)
            pass

        def apply_forced_move(target):
            # Apply the Forced Move status effect.
            # Add logic to apply the Forced Move effect (e.g., target is moved against their will)
            pass

        def apply_immobile(target):
            # Apply the Immobile status effect.
            # Add logic to apply the Immobile effect (e.g., target can't move)
            pass

        def apply_incapacitated(target):
            # Apply the Incapacitated status effect.
            # Add logic to apply the Incapacitated effect (e.g., target is unable to take actions or reactions)
            pass

        def apply_knockdown(target):
            # Apply the Knockdown status effect.
            # Add logic to apply the Knockdown effect (e.g., target falls prone)
            pass

        def apply_memory_alteration(target):
            # Apply the Memory Alteration status effect.
            # Add logic to apply the Memory Alteration effect (e.g., target's memories are altered or erased)
            pass

        def apply_mind_dredge(target):
            # Apply the Mind Dredge status effect.
            # Add logic to apply the Mind Dredge effect (e.g., target suffers memory loss or mental debuffs)
            pass

        def apply_nullify(target):
            # Apply the Nullify status effect.
            # Add logic to apply the Nullify effect (e.g., target's magical abilities are nullified)
            pass

        def apply_persistent_damage(target):
            # Apply the Persistent Damage status effect.
            # Add logic to apply the Persistent Damage effect (e.g., target suffers ongoing damage over time)
            pass

        def apply_phantasm(target):
            # Apply the Phantasm status effect.
            # Add logic to apply the Phantasm effect (e.g., target is hallucinating, seeing illusions)
            pass

        def apply_polymorph(target):
            # Apply the Polymorph status effect.
            # Add logic to apply the Polymorph effect (e.g., target is transformed into another form)
            pass

        def apply_provoked(target):
            # Apply the Provoked status effect.
            # Add logic to apply the Provoked effect (e.g., target is forced to act aggressively)
            pass

        def apply_spying(target):
            # Apply the Spying status effect.
            # Add logic to apply the Spying effect (e.g., target is being observed or tracked)
            pass

        def apply_sickened(target):
            # Apply the Sickened status effect.
            # Add logic to apply the Sickened effect (e.g., target suffers penalties due to illness)
            pass

        def apply_silenced(target):
            # Apply the Silenced status effect.
            # Add logic to apply the Silenced effect (e.g., target can't speak or cast verbal spells)
            pass

        def apply_slowed(target):
            # Apply the Slowed status effect.
            # Add logic to apply the Slowed effect (e.g., target moves slower, takes longer actions)
            pass

        def apply_stunned(target):
            # Apply the Stunned status effect.
            # Add logic to apply the Stunned effect (e.g., target can't act or react for a turn)
            pass

        def apply_stupefied(target):
            # Apply the Stupefied status effect.
            # Add logic to apply the Stupefied effect (e.g., target is mentally overwhelmed and disoriented)
            pass

        def apply_truthfulness(target):
            # Apply the Truthfulness status effect.
            # Add logic to apply the Truthfulness effect (e.g., target is compelled to tell the truth)
            pass

        def update_banes():
            for condition in self.conditions:
                condition.reduce_duration()
                if condition.duration <= 0:
                    condition.restore(player)
                    player.remove_condition(condition)
    
        def apply_bane(self, bane, character):
        #Apply the effect of the Bane to a character. TO DO: remove from being a part of Bane, add the Boons, have a pass through for the Bane/Boon in the function
            if self.name == "Blinded":
                self.apply_blinded(character)
            elif self.name == "Charmed":
                self.apply_charmed(character)
            elif self.name == "Deafened":
                self.apply_deafened(character)
            elif self.name == "Demoralized":
                self.apply_demoralized(character)
            elif self.name == "Death":
                self.apply_death(character)
            elif self.name == "Disarmed":
                self.apply_disarmed(character)
            elif self.name == "Dominated":
                self.apply_dominated(character)
            elif self.name == "Fatigued":
                self.apply_fatigued(character)
            elif self.name == "Fear":
                self.apply_fear(character)
            elif self.name == "Forced Move":
                self.apply_forced_move(character)
            elif self.name == "Incapacitated":
                self.apply_incapacitated(character)
            elif self.name == "Knockdown":
                self.apply_knockdown(character)
            elif self.name == "Memory Alteration":
                self.apply_memory_alteration(character)
            elif self.name == "Mind Dredge":
                self.apply_mind_dredge(character)
            elif self.name == "Nullify":
                self.apply_nullify(character)
            elif self.name == "Persistent Damage":
                self.apply_persistent_damage(character)
            elif self.name == "Phantasm":
                self.apply_phantasm(character)
            elif self.name == "Polymorph":
                self.apply_polymorph(character)
            elif self.name == "Provoked":
                self.apply_provoked(character)
            elif self.name == "Spying":
                self.apply_spying(character)
            elif self.name == "Sickened":
                self.apply_sickened(character)
            elif self.name == "Silenced":
                self.apply_silenced(character)
            elif self.name == "Slowed":
                self.apply_slowed(character)
            elif self.name == "Stunned":
                self.apply_stunned(character)
            elif self.name == "Stupefied":
                self.apply_stupefied(character)
            elif self.name == "Truthfulness":
                self.apply_truthfulness(character)

    class Boon: #allows us to make the different Boons from Open Legend
        instances = []

        def __init__ (self, name, power_level, attack_attributes, invocation, duration, description, effect):
            self.name = name
            self.power_level = power_level
            self.attack_attributes = attack_attributes
            self.invocation = invocation
            self.duration = duration
            self.description = description
            self.effect = effect

            Boon.instances.append(self) # Append this instance to the class-level 'instances' list

        def __repr__(self):
            return f"{self.name}"

        def __iter__(self): # Make the class iterable
            # Return an iterator over the list
            return iter(Boon.instances)

    class AttributeList: # Will be used to keep a list of attributes used to cast a specific bane or boon that we can then select from in the levelup/actions screen
        def __init__ (self):
            self.temp_list = []

        def __iter__(self): # Make the class iterable
        # Return an iterator over the list
            return iter(self.temp_list)

        def attribute_list(self, baneboon): #clears our attribute list and copies from the selected bane/boon
            self.temp_list.clear()
            self.temp_list = baneboon.attack_attributes.copy()

        def getIdx(self, idx): #checks to see if there is anything at the index on the list, helps avoid "IndexError"
            if idx >= len(self.temp_list):
                return None
            return self.temp_list[idx]

    class Perk:
        instances = []

        def __init__ (self, name, description):
            self.name = name
            self.description = description

            Perk.instances.append(self) # Append this instance to the class-level 'instances' list

        def __repr__(self):
            return f"{self.name}"
        
        def __iter__(self): # Make the class iterable
            return iter(Perk.instances) # Return an iterator over the list

    class Flaw:
        instances = []

        def __init__ (self, name, description):
            self.name = name
            self.description = description

            Flaw.instances.append(self) # Append this instance to the class-level 'instances' list

        def __repr__(self):
            return f"{self.name}"
        
        def __iter__(self): # Make the class iterable
            return iter(Flaw.instances) # Return an iterator over the list

    class Weapon:
        instances = []

        def __init__ (self, name, category, wealth_level, properties, banes, description): # TO DO: consider adding attribute that has how many hands required, having Melee or Ranged be category, short or long being range
            self.name = name
            self.category = category
            self.wealth_level = wealth_level
            self.properties = properties
            self.banes = banes
            self.description = description

            Equipment.instances.append(self) # Append this instance to the class-level 'instances' list

        def __repr__(self):
            return f"{self.name}"
        
        def __iter__(self): # Make the class iterable
            return iter(Equipment.instances) # Return an iterator over the list

# Variables
define attribute_added = True # this variable is used to toggle if a player can add a Bane or Boon with add_baneboons
define att_list = AttributeList() # this is a list that we call on in the levelup screens
default ability_description = "None" # holds a temporary input where a player describes what their bane or boon does, which is passed on
default descript_index = 0 # holds a temporary index to help place a bane or boon description

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define possible Non-player Characters below:

#define initials/name = Character_Sheet(self, character, name, agility, fortitude, might, learning, logic, perception, will, deception, persuasion, presence, alteration, creation, energy, entropy, influence, movement, prescience, protection, attribute_pts, level, feat_pts, wealth_score, armor, toughness, guard, resolve, max_hitpoints, hitpoints)

define enemy = Character_Sheet("Enemy", "Enemy", armor=1, agility=1, fortitude=1, might=3, learning=0, logic=0, perception=0, will=0, deception=0, persuasion=0, presence=0, alteration=0, creation=0, energy=0, entropy=0, influence=0, movement=0, prescience=0, protection=0, attribute_pts=0, level=0, toughness=0, guard=0, resolve=0, max_hitpoints=0, hitpoints=0, feat_pts=0, wealth_score=0)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define possible Weapons here, I've already provided some from the Open Legends website

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Banes = Bane("Bane_name", power_level = [], attack_attributes = [], attack_vs = [], invocation = "Major Action", duration = 1, description ="description", effect ="effect")
define Blinded = Bane("Blinded", power_level = [5], attack_attributes = ["Agility", "Creation", "Energy", "Entropy"], attack_vs = ["Guard","Guard","Guard","Toughness"], invocation = "Major Action", duration = 10, description = "You blind your foe with anything from a massive explosion, to a handful of sand, to an arctic blast, to a dazzling flash of light.", effect = "The target cannot see as long as the effect persists. The target automatically fails any Perception rolls based solely on normal sight. Attack rolls and Perception rolls based partially on sight that can be supplemented by another sense suffer disadvantage 5. The target's Guard defense is reduced by 3.")
define Charmed = Bane("Charmed", power_level = [3, 4, 6], attack_attributes = ["Influence"], attack_vs = ["Resolve"], invocation = "Major Action", duration = 10, description = "Charms are one of the great banes of legend, wielded by powerful enchantresses like Circe (of Homer's The Odyssey), nymphs, psychics, and other characters who control the will of others, not through total domination, but through a magical spell of love or friendship.", effect ="The charmed bane manifests at two levels: minor and major. Minor Charm - The target is mentally compelled to become more friendly, only changing their attitude toward you moderately. If they are about to strike you, they will restrain themselves - still angry and hostile, but no longer violent. If they want to help you and are leaning toward trusting you, but have some hesitation because you've just met, then that hesitation goes away. Major Charm - The attacker chooses whether the major charm is platonic or romantic. If platonic, the bane causes the target to consider the attacker their best friend and one of the most trustworthy and noble people they have met in all their lives. Alternatively, the attacker can choose for this trust and admiration to manifest as romantic love. The target is unable to do anything to plot against the one who afflicted them, and will (at the earliest possible opportunity) tell their charmer of any rumored harm or danger coming their way. The afflicted character becomes immediately suspicious of anyone who speaks ill of their attacker. The target is mentally compelled to like and trust you more, depending on the power level of the bane when invoked.")
define Deafened = Bane("Deafened", power_level = [4], attack_attributes = ["Agility", "Energy", "Entropy"], attack_vs = ["Guard", "Toughness", "Toughness"], invocation = "Major Action", duration = 10, description = "You deafen your foe with a crash of thunder, a deft strike to their ears, or a dark energy that disables their hearing.", effect ="The target cannot hear as long as the effect persists. The target automatically fails any Perception rolls based solely on hearing. Perception rolls based partially on hearing that can be supplemented by another sense suffer disadvantage 3.")
define Death = Bane("Death", power_level = [9], attack_attributes = ["Agility", "Entropy"], attack_vs = ["Toughness", "Toughness"], invocation = "Major Action", duration = 1, description = "Utilizing either incredible precision or the power of entropy, you snuff out the target's life force completely.", effect ="Upon a successful invocation, the target is immediately rendered immobile, unconscious, and unable to take actions. They have disadvantage 5 on all Perception rolls, and any damaging attacks against them count as finishing blows. If the target fails three resist rolls to shake off this bane, they die. The death is permanent.")
define Demoralized = Bane("Demoralized", power_level = [3, 6, 8], attack_attributes = ["Agility", "Energy", "Entropy", "Influence", "Might", "Persuasion", "Presence"], attack_vs = ["Resolve", "Resolve", "Resolve", "Resolve", "Resolve", "Resolve", "Resolve"], invocation = "Major Action", duration = 10, description = "Using your quick wit, intimidating presence, or even a strong display of magical power, you cause your enemies to doubt themselves.", effect ="The affected target has disadvantage on all action rolls.")
define Disarmed = Bane("Disarmed", power_level = [3, 6], attack_attributes = ["Agility", "Alteration", "Energy", "Entropy", "Influence", "Might", "Movement"], attack_vs = ["Guard", "Guard", "Guard", "Toughness", "Resolve", "Guard", "Guard"], invocation = "Major Action", duration = 1, description = "You force an opponent to lose control of an object they are holding, whether through brute force, mental compulsion, a skillful parry, heating the item to unbearable temperatures, shooting it from their hands, or some other means.", effect ="The target drops an object they are holding within 15' of the target.")
define Dominated = Bane("Dominated", power_level = [3, 5, 9], attack_attributes = ["Influence"], attack_vs = ["Resolve"], invocation = "Major Action", duration = 1,  description = "Though rare, domination is seen from time to time in legendary tales, often wielded by vampires, and sometimes by the most powerful of sorcerers or mad scientists who command legions of mindless zombies, completely enslaved to their will.", effect ="The dominated bane manifests at two levels: lesser and greater. Lesser Domination - The target obeys a one word command until the end of their next turn, at which time the bane immediately ends. Greater Domination - The target's every action and move is under your control.")
define Fatigued = Bane("Fatigued", power_level = [5], attack_attributes = ["Entropy"], attack_vs = ["Toughness"], invocation = "Major Action", duration = 1,  description = "You cause the target's body to wither and weaken, gradually losing its ability to function until the victim finally succumbs to death. Fatigue may be the result of a necromancer's curse, an assassin's poison, a radiation ray, or similar life sapping effects.", effect ="This bane has multiple tiers which are applied in succession. Each time this bane is inflicted, if it is already in effect on the target, the severity escalates by one level.")
define Fear = Bane("Fear", power_level = [5], attack_attributes = ["Creation", "Entropy", "Influence", "Might"], attack_vs = ["Resolve", "Resolve", "Resolve", "Resolve"], invocation = "Major Action", duration = 1, description = "Through an overwhelming force of physical might or extraordinary power, you strike terror into the hearts of enemies, causing them to flee from your presence.", effect ="On its turn, the afflicted target must use its entire turn to get as far away as possible from you. It cannot use its actions to do anything other than retreat, and it cannot willingly move closer to you while the bane persists.")
define Forced_Move = Bane("Forced Move", power_level = [2, 4, 6, 8], attack_attributes = ["Agility", "Energy", "Might", "Movement"], attack_vs = ["Guard", "Guard", "Guard", "Guard"], invocation = "Major Action", duration = 1, description = "With a forceful blow, magical gust of wind, or telekinetic push, you move your target against its will.", effect ="The target is moved a distance against their will, as determined by the bane's power level. Five feet per power level.")
define Immobile = Bane("Immobile", power_level = [1], attack_attributes = ["Agility", "Alteration", "Creation", "Energy", "Entropy", "Influence", "Might", "Movement"], attack_vs = ["Guard", "Guard", "Toughness", "Toughness", "Toughness", "Resolve", "Guard", "Guard"], invocation = "Major Action", duration = 10, description = "Whether through grappling, a precise nerve strike, entangling vines, mental compulsion, or a bone-numbing blast of cold, you render your foe incapable of movement.", effect ="Your target cannot move from its current space. If you invoked the bane with a Might roll and are within 5' of the target, then both you and the target are immobile in your current space for the duration of the bane (locked in a grapple).")
define Incapacitated = Bane("Incapacitated", power_level = [5, 7, 9], attack_attributes = ["Agility", "Entropy", "Influence"], attack_vs = ["Toughness", "Toughness", "Resolve"], invocation = "Major Action", duration = 1, description = "Incapacitation is a catch-all bane for a variety of effects, including total paralysis, sleep, petrification, poison, being knocked out, fainting, or similar conditions that render a character completely helpless.", effect ="The target is immobile (can't move from their current space) and unconscious. They have disadvantage 5 on all perception rolls and are incapable of moving. As a result of being completely incapable of movement, an incapacitated character can be the victim of a finishing blow.")
define Knockdown = Bane("Knockdown", power_level = [1], attack_attributes = ["Agility", "Energy", "Might", "Movement"], attack_vs = ["Guard", "Guard", "Guard", "Guard"], invocation = "Major Action", duration = 1, description = "Whether via a thunderous blow from a great axe, an earth shattering bolt of supernatural energy, or a well aimed shove in a direction where the enemy's balance is weak, you knock the target off their feet.", effect ="The target falls prone. Prone targets have disadvantage 1 on all attacks they make. Characters that are prone due to the knockdown bane (or any other reason) get +2 to Guard versus Ranged attacks and -2 Guard versus Melee attacks. Standing up from prone requires a move action and costs a character half (round down) of their speed for the round.")
define Memory_Alteration = Bane("Memory Alteration", power_level = [5, 6, 8], attack_attributes = ["Influence"], attack_vs = ["Resolve"], invocation = "Major Action", duration = 1, description = "Warping or controlling the mind is one of the most dreaded powers of enchanters, causing powerful heroes to forget their homes, families, and quests.", effect ="You alter the target's memories to an extent based on the power level of the bane. (Situational)")
define Mind_Dredge = Bane("Mind Dredge", power_level = [2, 4, 6, 8, 9], attack_attributes = ["Prescience"], attack_vs = ["Resolve"], invocation = "Major Action", duration = 10, description = "You gaze into the mind of another creature and read their thoughts. The most powerful wielders of this bane can even pry into the distant memories of their subjects.", effect ="You gaze into the mind of another creature and read their thoughts. The most powerful wielders of this bane can even pry into the distant memories of their subjects.")
define Nullify = Bane("Nullify", power_level = [1, 2, 3, 4, 5, 6, 7, 8, 9], attack_attributes = ["Protection"], attack_vs = ["Resolve"], invocation = "Major Action", duration = 1, description = "Through magical power, technological hacking, or similar means, you are able to nullify your enemy's boons.", effect ="You cancel a single boon currently in effect if it is of this bane's power level or lower.")
define Persistent_Damage = Bane("Persistent Damage", power_level = [2, 4, 6, 8, 9], attack_attributes = ["Agility", "Energy", "Entropy"], attack_vs = ["Guard", "Guard", "Toughness"], invocation = "Major Action", duration = 10, description = "Whether by setting the target ablaze, covering them in acid, slicing an artery, or cursing them with a wasting disease, you inflict your foe with a lasting and recurring source of damage.", effect ="At the beginning of the target's turn, before they take any actions, they suffer damage determined by the power level of the bane.")
define Phantasm = Bane("Phantasm", power_level = [1, 2, 3, 4, 5, 6, 7, 8, 9], attack_attributes = ["Influence"], attack_vs = ["Resolve"], invocation = "Major Action", duration = 1, description = "You create an illusory manifestation to deceive the senses.", effect ="You create a phantasm of your choosing. The power level at which you invoke the bane determines which senses you can deceive as well as the maximum size of your illusion.")
define Polymorph = Bane("Polymorph", power_level = [5, 6, 7, 8, 9], attack_attributes = ["Alteration"], attack_vs = ["Toughness"], invocation = "1 Minute", duration = 10, description = "You alter the size, shape, and composition of the target by causing them to grow, shrink, or assume a completely new form, like that of a sheep or a newt.", effect ="Your power level determines the extent to which you can transform your target.")
define Provoked = Bane("Provoked", power_level = [4, 5, 6, 7, 8, 9], attack_attributes = ["Agility", "Creation", "Deception", "Energy", "Influence", "Might", "Persuasion", "Presence"], attack_vs = ["Resolve", "Resolve", "Resolve", "Resolve", "Resolve", "Resolve", "Resolve", "Resolve"], invocation = "Minor Action", duration = 10, description = "Through a display of awe-inspiring force, intimidation, or leadership, you command attention as the greatest threat, causing others to fear attacking your allies.", effect ="Any attacks made by the target that do not include you as a target suffer disadvantage. Disadvantage 1 per power level.")
define Spying = Bane("Spying", power_level = [5, 6, 7, 8, 9], attack_attributes = ["Prescience"], attack_vs = ["Resolve"], invocation = "10 Minutes", duration = 1, description = "Either through innate extrasensory perception or a special conduit such as a computer terminal, bubbling cauldron, or a crystal ball, you can view the target from a distance.", effect ="You can spy on a person or area that you are familiar with. The power level of this bane determines the maximum distance between you and the target. If successfully invoked, you can see and hear everything that goes on within a 60' radius of your target. Anyone within the targeted area who has a Resolve defense score higher than your Prescience action roll to invoke this bane becomes aware of an unseen presence in the area (regardless of whether or not you succeed at the roll).")
define Sickened = Bane("Sickened", power_level = [5], attack_attributes = ["Entropy"], attack_vs = ["Toughness"], invocation = "Major Action", duration = 10, description = "Entropic energy overcomes the target, bombarding their system and inducing nausea that makes self-defense and any kind of action difficult.", effect ="The target has disadvantage 1 on all action rolls and -1 to all defenses.")
define Silenced = Bane("Silenced", power_level = [2], attack_attributes = ["Agility", "Alteration", "Entropy", "Might"], attack_vs = ["Toughness", "Toughness", "Toughness", "Toughness"], invocation = "Major Action", duration = 10, description = "Silence overcomes the target, whether from the warping of sound around the target, or from a physical effect like strangulation or suffocation.", effect ="If Might, Agility, or Entropy is used to inflict this bane, then the character is suffering strangulation and unable to speak. If the bane is inflicted using Alteration, then all sound within 5' of the target is suppressed through extraordinary means, making their footsteps and the usual clank of belongings they are carrying inaudible.")
define Slowed = Bane("Slowed", power_level = [1], attack_attributes = ["Agility", "Energy", "Entropy", "Might", "Movement"], attack_vs = ["Guard","Guard","Toughness","Guard","Guard"], invocation = "Major Action", duration = 1, description = "The target's movement is impaired, either by extreme cold, prolonged heat, poison, or injury to one or both legs.", effect ="The afflicted target's speed is reduced to half its current speed, rounded down to the nearest 5' increment. This applies to all movement that is physical (flight, walking, climbing, etc.). If the target is currently under a magical effect that increases speed, the two effects are canceled.")
define Stunned = Bane("Stunned", power_level = [4], attack_attributes = ["Agility", "Energy", "Entropy", "Might"], attack_vs = ["Toughness", "Toughness", "Toughness", "Toughness"], invocation = "Major Action", duration = 10, description = "You disorient the target's senses, causing them to act much less efficiently.", effect ="During the target's turn, they are limited to either a single major action, a single move action, or a single minor action.")
define Stupefied = Bane("Stupefied", power_level = [7], attack_attributes = ["Influence"], attack_vs = ["Resolve"], invocation = "Major Action", duration = 1, description = "The stupefied bane has examples in many stories and legends: a vampire's eyes, a siren's song, and a nymph's beauty are all known to cast a stupor upon weak-willed mortals. Being stupefied causes the target to be lulled into a false sense of security, tranquility, and pacifism.", effect ="The target is in a state of mental fog, lowering their mental defenses. While stupefied, the target's Resolve defense is reduced to 10.")
define Truthfulness = Bane("Truthfulness", power_level = [5], attack_attributes = ["Influence"], attack_vs = ["Resolve"], invocation = "10 Minutes", duration = 1, description = "By controlling the target's mind through compulsion magic, chemical injection, neural probes, or similar means, you render them incapable of lying deliberately.", effect ="The target answers any question asked with honesty, to the best of their knowledge.")

#Boons = Boon("Boon_name", power_level = [], attack_attributes = [], invocation = "Major Action", duration = 1, description ="description", effect ="effect")
define Absorb_Object = Boon("Absorb Object", power_level = [4], attack_attributes = ["Alteration", "Movement"], invocation = "Major Action", duration = 1, description = "description", effect ="The object remains in place, completely hidden from the perception of others, until the target summons or recalls it (automatically) as a minor action. If anything happens to cancel this boon (such as the nullify bane), the object is immediately shunted out of the target's body as if the object had been withdrawn.")
define Animation = Boon("Animation", power_level = [6,8], attack_attributes = ["Creation", "Entropy", "Logic"], invocation = 1, duration = 1, description = "description", effect ="You are able to create an autonomous being from inanimate material components")
define Aura = Boon("Aura", power_level = [4,6,8], attack_attributes = ["Alteration", "Creation", "Energy", "Entropy", "Influence", "Movement", "Presence", "Prescience", "Protection"], invocation = "Major Action", duration = 1, description ="description", effect ="effect")
define Barrier = Boon("Barrier", power_level = [3,5,7,9], attack_attributes = ["Creation", "Energy", "Entropy", "Protection"], invocation = "Major Action", duration = 1, description ="description", effect ="effect")
define Blindsight = Boon("Blindsight", power_level = [5], attack_attributes = ["Alteration", "Entropy", "Perception", "Prescience"], invocation = "Major Action", duration = 1, description ="description", effect ="The target is immune to the blinded bane and they are able to see normally even in conditions of little or no light.")
define Bolster = Boon("Bolster", power_level = [3,6,8], attack_attributes = ["Alteration", "Creation", "Prescience", "Presence"], invocation = "Major Action", duration = 1, description ="description", effect ="Choose a single attribute. The target gains advantage on their action rolls with that attribute according to the power level of the boon.")
define Concealment = Boon("Concealment", power_level = [3,4,5,6,7,8], attack_attributes = ["Alteration", "Influence"], invocation = "Major Action", duration = 1, description ="description", effect ="effect")
define Darkness = Boon("Darkness", power_level = [1, 2, 3, 4, 5, 6, 7, 8, 9], attack_attributes = ["Entropy", "Influence"], invocation = "Major Action", duration = 1, description ="description", effect ="Choose a space or object within range. Darkness emanates from the target to a radius equal to five feet per power level of the boon.")
define Detection = Boon("Detection", power_level = [1], attack_attributes = ["Prescience"], invocation = "Major Action", duration = 1, description ="description", effect ="When calling on this boon, you must choose the type of aura you are detecting: holy, unholy, life, death, or magic. You can perceive invisible auras pertaining to the chosen type of force and have an approximate sense of their strength.")
define Flight = Boon("Flight", power_level = [5,6,8], attack_attributes = ["Alteration", "Movement"], invocation = "Major Action", duration = 1, description ="description", effect ="You gain a flight speed. 10' for power level 5, 30' for power level 6, 60' for power level 8.")
define Genesis = Boon("Genesis", power_level = [1,3,5,7,9], attack_attributes = ["Creation"], invocation = "Major Action", duration = 1, description ="description", effect ="You create something from nothing. Depending on the power of your invocation, you are able to manifest a wide array of materials, from temporary vegetable matter to permanent crafted goods of remarkable complexity.")
define Haste = Boon("Haste", power_level = [2,4,6,8], attack_attributes = ["Alteration", "Movement"], invocation = "Major Action", duration = 1, description ="description", effect ="The target moves with extraordinary speed")
define Heal = Boon("Heal", power_level = [1, 2, 3, 4, 5, 6, 7, 8, 9], attack_attributes = ["Creation", "Learning", "Logic", "Presence"], invocation = "Major Action", duration = 1, description ="description", effect ="Heal a target. Higher power levels heal for more.")
define Insubstantial = Boon("Insubstantial", power_level = [7], attack_attributes = ["Alteration", "Entropy"], invocation = "Major Action", duration = 1, description ="description", effect ="The target gains the ability to pass freely through all physical barriers as if they were unoccupied spaces.")
#define Invisible <REPLACED BY CONCEALMENT, JUST HERE FOR DOCUMENTATION PURPOSES>  = Boon("Invisible", power_level = [5,6], attack_attributes = ["Alteration", "Influence"], invocation = "Major Action", duration = 1, description ="description", effect ="effect")
define Life_Drain = Boon("Life Drain", power_level = [5], attack_attributes = ["Entropy"], invocation = "Major Action", duration = 1, description ="description", effect ="While this boon persists, the target heals half (round up) of the damage they inflict with each attack. If an attack damages multiple foes, the target of this boon heals based on the total damage inflicted against all foes.")
define Light = Boon("Light", power_level = [1, 2, 3, 4, 5, 6, 7, 8, 9], attack_attributes = ["Creation", "Energy"], invocation = "Major Action", duration = 1, description ="description", effect ="Choose a space or object within range. Extraordinary light emanates from the target to a radius equal five feet per power level of the boon. If the light area overlaps an area affected by the darkness boon, then the one of greater power level supersedes the other. If the power level of both is equal, then they cancel each other out.")
define Precognition = Boon("Precognition", power_level = [1,3,5,7], attack_attributes = ["Prescience"], invocation = "1 Minute", duration = 1, description ="description", effect ="effect")
define Reading = Boon("Reading", power_level = [5,6,7,8,9], attack_attributes = ["Prescience"], invocation = "Major Action", duration = 1, description ="description", effect ="When you successfully invoke this boon, you gain information from an object or place within range")
define Regeneration = Boon("Regeneration", power_level = [1,3,5,7,9], attack_attributes = ["Alteration", "Creation"], invocation = "Major Action", duration = 1, description ="description", effect ="While the regeneration boon is sustained, the target heals hit points at the beginning of each of the boon invoker's turns. The amount of healing is determined by the power level of the boon.")
define Resistance = Boon("Resistance", power_level = [3,5,7,9], attack_attributes = ["Alteration", "Energy", "Movement", "Protection"], invocation = "Major Action", duration = 1, description ="description", effect ="When the boon is invoked, the invoker chooses one type of attack and the target gains resistance to that type.")
define Restoration = Boon("Restoration", power_level = [1, 2, 3, 4, 5, 6, 7, 8, 9], attack_attributes = ["Creation", "Protection"], invocation = "Major Action", duration = 1, description ="description", effect ="You can dispel all banes affecting your target of a power level less than or equal to the level at which you invoke this boon.")
define Seeing = Boon("Seeing", power_level = [4,5,6], attack_attributes = ["Prescience"], invocation = "Major Action", duration = 1, description ="description", effect ="For as long as you concentrate, you can see through the eyes of the target, a willing ally.")
define Shapeshift = Boon("Shapeshift", power_level = [2,3,4,5,6,7,8], attack_attributes = ["Alteration"], invocation = "Major Action", duration = 1, description ="description", effect ="effect")
define Summon_Creature = Boon("Summon Creature", power_level = [4,5,6,7,8,9], attack_attributes = ["Alteration", "Creation", "Entropy", "Energy"], invocation = "Focus Action", duration = 1, description ="description", effect ="You create or summon a temporary NPC companion that is under your control, though of limited intelligence. Your minion's statistics are determined by the power level of this boon.")
define Sustenance = Boon("Sustenance", power_level = [3,4,5,7,9], attack_attributes = ["Alteration", "Creation", "Protection"], invocation = "Major Action", duration = 1, description ="description", effect ="You protect the target from one environmental danger, biological need, or similar condition.")
define Telekinesis = Boon("Telekinesis", power_level = [3,5,7,9], attack_attributes = ["Movement"], invocation = "Major Action", duration = 1, description ="description", effect ="Immediately upon invoking the boon, and again each round when you sustain the boon, you may move the target object up to 5' times your invoking attribute score. As part of moving an object, you may also manipulate it (for example, turning a door knob or opening a coin purse). A new invocation of this boon must be attempted whenever you wish to target a different object. The power level of the boon determines the size and weight of the objects you may target")
define Telepathy = Boon("Telepathy", power_level = [3,5,6,7], attack_attributes = ["Influence", "Prescience"], invocation = "Major Action", duration = 1, description ="description", effect ="You and the target can communicate with each other simply through thought. Note that this telepathy does not bestow intelligence upon creatures, so you could not use it to communicate with a squirrel unless you already possessed other means of doing so. Additionally, telepathy does not bypass language barriers, so you would need to already speak the language of your target.")
define Teleport = Boon("Teleport", power_level = [3,5,7,9], attack_attributes = ["Movement"], invocation = "Major Action", duration = 1, description ="description", effect ="effect")
define Tongues = Boon("Tongues", power_level = [5,6], attack_attributes = ["Prescience"], invocation = "Major Action", duration = 1, description ="description", effect ="effect")
define Transmutation = Boon("Transmutation", power_level = [3,5,7,8,9], attack_attributes = ["Alteration"], invocation = "Major Action", duration = 1, description ="description", effect ="effect")
define Truesight = Boon("Truesight", power_level = [5,6,7,8,9], attack_attributes = ["Prescience"], invocation = "Major Action", duration = 1, description ="description", effect ="effect")

#Perks
define Ageless = Perk("Ageless","Whether you are an android constructed of space age material that does not erode over time, the loyal servant of a higher power, or the subject of an arcane ritual, you have unlocked the secret to immortality. You are immune to the passage of time and the effects of old age. Your body does not age and you cannot be harmed by extraordinary effects that cause aging. Based on the source of your agelessness, you can decide whether or not your appearance changes over time.")
define Artisan = Perk("Artisan","Choose a specific craft, such as gunsmithing, hardware assembly, glass blowing, or brewing. You are a master of a chosen craft, and your reputation goes far and wide. In a time frame decided by the GM, you can craft any mundane item of wealth level 2 or less, if you have access to the right tools. Furthermore, whenever you are performing a task in which your crafting skills would play a role, you gain advantage 1 to any action rolls that you must make. Your reputation means that other students of your craft may actively seek you out as a teacher. Experts in any field that makes use of the items you create will actively recommend that others seek you out.")
define Ascetic = Perk("Ascetic","You are well-versed in the art of living with less. Whether a cloistered monk, a transcendent psion, or a wizened sage who spent years locked away in a tower of books, you are experienced at going long stretches of time with very little food, water, or company - and as such, these situations tend not to affect you as they do others. You are hardened against physical and mental deprivation and have developed an enviable degree of self-mastery. Whenever your asceticism would play a role in a situation, you gain advantage 1 to any relevant action rolls.")
define Attractive = Perk("Attractive","When it comes to physical appearance, you're an absolute knockout. This plays to your favor more than just romantically, and your good looks tend to help you out in all sorts of social situations. Whenever your attractiveness would play a role in a situation, you gain advantage 1 to any relevant action rolls.")
define Brute = Perk("Brute","While others might convince with a silver tongue, you speak the universal language of fear. Once per game session, if you make a show of physical force, you can use your Might attribute for a Persuasion roll. If your Persuasion score is already greater than or equal to your Might score, you get advantage 1 on the roll.")
define Courageous = Perk("Courageous","When the odds are stacked against you, you never falter or waiver. Once per game session, as a free action you can cancel all negative effects afflicting you that relate to fear or low morale.")
define Crowd_Favorite = Perk("Crowd Favorite","Whether you are an actor, musician, storyteller, magician, or some other type of performer, the common folk love your work. They adore you for your ability to use your art to transport them to a world beyond their daily drudgery, and you can always find a place to perform and make money at the local tavern or inn.")
define Disease_Immunity = Perk("Disease Immunity","You are immune to natural disease. This protection does not guard against supernatural curses such as lycanthropy.")
define Divine_Agent = Perk("Divine Agent","You serve a higher being and have earned their protection. Once per game session, when you are subject to a Finishing Blow while your hit points are below 1, you automatically heal to a hit point total of 1.")
define Divine_Insight = Perk("Divine Insight","You possess a supernatural connection to a deity, demi-god, or other divine being which grants you otherworldly insight. Once per game session, you can choose a topic relevant to the story. The GM shares some information about that topic which might be useful. If you've just failed a Learning attribute roll and use this ability, the GM decides whether to give you information related to that roll or to give you knowledge that is completely unrelated.")
define Ear_of_the_Emperor = Perk("Ear of the Emperor","You have done something in the past to earn the favor of someone in a high place: a senator, the general of an army, a merchant lord, etc. Perhaps you saved their life or spared them from significant monetary loss. Whatever you did, they owe you, and they are willing to help you with minor favors as long as the favors do not subject them to any risk or cost. Once during the campaign, you can call in a large favor that does put your contact in risk or cost them something significant. They will perform the favor, but you immediately lose this trait, as their debt has been repaid.")
define Extraordinary_Presence = Perk("Extraordinary Presence","Your inherent extraordinary nature manifests itself in a tangible way of your choosing. For example, your eyes may glow, your skin might emanate an icy chill, or a trail of withering plants could follow you wherever you set foot. Depending on the nature of your extraordinary presence, it might make others more likely to fear, admire, or trust you—or otherwise alter their initial perceptions of you. Whenever your extraordinary presence is relevant in a social situation, you gain advantage 1 on any action rolls you make.")
define Fugitive = Perk("Fugitive","You are part of a illegal network, whether it be a thieves' guild, an underground network of stolen data brokers, or otherwise. Once per game session, you can call in a favor from a contact within your network to perform a mundane task such as gathering information or arranging safe passage. If the favor puts your contact at risk, they will still perform it but may ask for an equally risky favor from you in return.")
define Idol = Perk("Idol","Your reputation for some outstanding virtue precedes you, and people tend to hold you in high esteem. Once per session, you can call upon your reputation to inspire trust from someone who is skeptical of you, your actions, or your allies.")
define Innocent = Perk("Innocent","Whether from a distant fey ancestry or simply an air of naivety, you possess a childlike quality that can melt even the coldest of hearts. Once per game session, you can leverage your innocence to turn an enemy and cause them to take pity on you. The enemy might choose to look the other way when you've done something illegal, forgive a debt you could never pay, or vouch in your favor before the authorities.")
define Jack_of_All_Trades = Perk("Jack of All Trades","You have a knack for picking up new skills. Once per game session, provided you are not under pressure from an inordinately tight deadline, you can automatically succeed at a non-attack action roll that relates to some craft, trade, skill, or similar work provided its Challenge Rating is less than or equal to 14.")
define Legendary_Bloodline = Perk("Legendary Bloodline","Your ancestry can be traced to dragons, Void Templars, an ancient order of Archmagi, an intergalactic dynasty, or a similar powerful group. As such, a sense of awe follows you when met by those who know and respect your heritage. Choose an area of expertise, such as arcana, politics, or warfare. You are assumed to have knowledge and a destiny for greatness in the chosen area of expertise, and others treat you with deference. This influence could guarantee your placement within an Arcane College, grant you access to the Void Templars securely encrypted database, secure a mentorship under a famous Senator, or cause a Lieutenant who does not know you well to take combat orders from you based on your training in an elite task force.")
define Local_Hero = Perk("Local Hero","You are well-known and respected as a protector of the common folk in a small region. The average citizen in this area will look up to you, and will offer you food, shelter, and other necessities. They will even take risks or assume minor costs to aid or protect you, so long as the risk is not death.")
define Lucky = Perk("Lucky","Once per game session, in a moment of need, you can call on luck to shine upon you. The GM decides what form this luck takes. For example, an attack that was meant for you might target an ally instead, you may discover a secret passage to escape from a rolling boulder, or a local law enforcement officer decides to overlook your crime because you happen to have grown up on the same street.")
define Merchant = Perk("Merchant","You understand the art of economics as well as the best of businessmen. A master of supply and demand, you have a knack for knowing when to buy and when to sell. You cannot be swindled when it comes to bartering, and you always know whether or not you are getting a fair price. Furthermore, you have friends in merchant circles and guilds in your home city, and you can easily gain such connections in new locations given enough time.")
define Natures_Ally = Perk("Nature's Ally","The natural world responds to your deep connection with it. Perhaps you are a preservationist, seeking to restore organic life in a shattered post-apocalyptic wasteland, or maybe you are a hermit closely attuned to the animals and plants of the Sylvan woodlands. Whatever your circumstance, people and creatures connected to the land can sense your deep respect for the natural order. Wild animals are more receptive to your desires, primitive tribes give you the benefit of the doubt by assuming you do not have destructive intentions, and you can typically gain an audience with an elusive Druid or Shaman in a given region who shares your goal in defending nature.")
define Observant = Perk("Observant","Your keen senses allow you to notice details that others typically miss. Once per game session, you can use this ability to notice something out of the ordinary. For example, you might spot a hidden passage behind a bookcase, a trace of blood under the fingernails of another character, or a wig that is not quite convincing. If you use this ability after failing a Perception roll, the GM decides whether you notice the initial target of your roll or a different detail.")
define Profession = Perk("Profession","Choose a specific trade, such as sailor, soldier, or miner. You know everything there is to know about the business and are a master of the requisite skills. A sailor, for example, can tie a knot for all occasions, navigate by the stars, and man any station aboard a ship. A soldier is well-versed in a variety of arms, understands military tactics, and knows how to navigate the chain of command with ease. Furthermore, whenever you are performing a task in which your professional skills would play a role, you gain advantage 1 to any non-combat action rolls that you must make.")
define Pure_hearted = Perk("Pure-hearted","Any goodly-natured creature you encounter is friendly toward you by default rather than neutral. Circumstances can alter this, but even if rumors or actions you've taken would influence a good creature negatively, it remains one step friendlier than it otherwise would have been.")
define Resilient = Perk("Resilient","You are exceptionally difficult to kill or wear down. Once per game session, you can automatically succeed a Fortitude action roll of Challenge Rating less than or equal to 10 + twice your Fortitude score.")
define Scavenger = Perk("Scavenger","You have lived a life of need, and thus know how to make do when others would go without. Once per game session, you can easily acquire a single mundane item even though it would otherwise take time to get or be completely unattainable. Depending on the circumstances, the GM may decide that your acquisition is only temporary or subject to reasonable conditions. For example, you might use this perk to acquire a rope in the middle of a desert, but the GM may rule that it is so sunbaked and ancient that it will likely snap after a few uses.")
define Scent = Perk("Scent","Your sense of smell is almost feral or otherwise ultra-heightened. As a focus action, you can discern the number and relative location of living creatures within 60'. With an additional focus action you can lock onto a particular scent and maintain its relative location as long as it remains within 60'. Furthermore, you gain advantage 1 on attempts to track a creature if it has left a scent trail.")
define Scholar = Perk("Scholar","You have spent years studying a particular discipline, such as physics, herbalism, dragon lore, history, politics, or religion. Once per session, you can re-attempt a failed Learning roll related to your discipline, gaining advantage 2 on the re-roll. Furthermore, you have colleagues and connections within your discipline, and know the proper channels for gaining access to specialty laboratories, libraries, temples, or other collections of lore related to your field of scholarship.")
define Silver_Tongue = Perk("Silver Tongue","You have practiced the ways of sneaking hidden charms and subliminal messages within everyday conversation. Once per session, when you converse with an intelligent creature for at least five minutes, you will learn one useful secret of the GM's choosing about the creature.")
define Stone_Sense = Perk("Stone Sense","While underground you may fail to find what you're looking for, but you can never be truly lost. You can always find your way back to the entrance through which you entered. Furthermore, you have advantage 1 on any action rolls in which a familiarity with underground environments would prove helpful, such as attempts to identify the risk of a cave-in or to find a secret passage within a cavern.")
define Street_Rat = Perk("Street Rat","You were raised on the streets or at least spent a good deal of time crawling about them. As such, you know how to navigate urban areas quickly, make yourself unseen, and find a bite to eat when you're down on your luck. As one of the invisible urchins that crawl the city, you are also quite adept at picking up rumors in taverns and crowded streets. You gain advantage 1 on rolls for situations in which your street rat nature would be helpful.")
define Upper_Class = Perk("Upper Class","Being of high birth, old money, or otherwise given access to resources beyond the common citizen, you are treated as a benefactor by the lower classes. They will trust and help you in the hopes of being rewarded for their efforts. You are also treated as a peer by those of similar or slightly higher social standing and can typically request an audience with them. In addition, representatives of the law generally assume you to be beyond reproach unless they are presented with compelling evidence to the contrary.")
define Vagabond = Perk("Vagabond","Having spent significant time fending for yourself in the wilderness, you excel at surviving and navigating in the wild. You always know the direction of true north and you can automatically find enough food to feed yourself plus a number of additional people equal to your Learning attribute score.")
define Warriors_Code = Perk("Warrior's Code","As a veteran warrior, you command respect even from foes. Once per session, you can use this perk to cause an enemy or group of enemies to extend special concessions or favorable treatment toward you via an unspoken warrior's code. The GM decides what these concessions look like. For example, your enemies might choose to trust you to come quietly and not shackle you, or overlook an insult that would have otherwise have been cause for bloodshed.")
define Whisperer_of_the_Wild = Perk("Whisperer of the Wild","Once per game session, you can ask a single “yes” or “no” question of a plant or animal within earshot. The plant or animal automatically trusts you at least enough to answer the question truthfully. You receive the answer by way of an inner sense, and so this ability cannot be used for further two-way communication.")

#Flaws
define Absent_minded = Flaw("Absent-minded","You live with your head in the clouds. You might just be ditzy, or maybe you just spend your time contemplating loftier matters. Whatever the source of your absent-mindedness, you are slow to notice important details and have a tendency to get distracted at exactly the worst possible moment.")
define Addiction = Flaw("Addiction","The roll of the dice, the smoke of the Black Lotus, or the escape of the virtual reality machine. Whether your addiction is physical, mental, or social, the effect is generally the same: you've got an itch that you need to scratch, and you'll sometimes do reckless or atrocious things to make sure that you can get your fix. You get to decide the nature and severity of your addiction.")
define Ambitious = Flaw("Ambitious","You are willing to do anything to get ahead in life and often that means trampling upon other people on your way to the top. When presented with a situation requiring empathy for those beneath you, it's typical for you to ignore their need. In addition, you may sometimes overreach in your attempts to get ahead, making bold and risky choices that can put you and those close to you in danger.")
define Bloodlust = Flaw("Bloodlust","Battle isn't just a way of life, it is the way of life. There isn't a conflict you've encountered that wasn't best solved with steel or lead, and your allies will have a hard time convincing you otherwise. You are prone to starting fights when they aren't necessary and prolonging them even after the enemy has surrendered.")
define Brash = Flaw("Brash","You are bold and daring to the point of recklessness. You have no time for plans, calculations, or strategic thinking. A lot of brass and a bit of luck are all you need. Kick in the door and let the details sort themselves out.")
define Bravado = Flaw("Bravado","You have a flair for the dramatic, and will often undertake bold or daring maneuvers simply for the thrill of it. For example, in combat you might swing from a chandelier even if it offers no tactical advantage.")
define Compulsion = Flaw("Compulsion","You have an irresistible urge to perform a behavior of your choice. Examples include, grinding your teeth, tapping your foot, biting your fingernails, counting coinage, and washing your hands. Your compulsion can sometimes put you in awkward or embarrassing situations, such as needing to wash your hands immediately after shaking hands with an ambassador.")
define Cosmetic_Deformity = Flaw("Cosmetic Deformity","Something about you makes you less attractive, undesirable to behold, or even just downright abominable. You get to decide the nature and severity of your deformity. Examples include a scarred cheek, vacant white eyes, a burn-covered body, and a missing nose. Whatever form this flaw takes, it is merely cosmetic and thus will generally only affect you in social situations.")
define Cowardly = Flaw("Cowardly","You have honed self-preservation into a way of life, and you will do almost anything to avoid danger, pain, and death. Sometimes, the situation at hand and the pumping of adrenaline will lead you to perform acts that appear courageous, but sooner or later your cowardly nature will emerge. You are easy to intimidate and you will almost assuredly crack under interrogation. In combat, you can still choose to fight, but you will attempt to distance yourself as much as possible from harm's way, even if it means leaving an ally in a tough spot.")
define Dimwitted = Flaw("Dimwitted","You aren't the sharpest tack in the box. It's not just that you weren't gifted with skill in academia, it's that you pick up on things pretty slowly overall. With the exception of your areas of expertise, you have a hard time learning new skills, following instructions, and maybe even remembering names.")
define Disabled = Flaw("Disabled","You have some physical deficiency that holds you back in life. You decide the nature and severity of your disability. Some examples of disabilities include blindness, deafness, missing limbs, partial paralysis, bone deficiencies, or allergies.")
define Greedy = Flaw("Greedy","You can't help it: you just like things. Money, gems, items of power - they beckon you at every turn and you'll often take great risks and maybe even betray your allies if the monetary reward is great enough. You're easy to bribe, and you will often push the limits of negotiation or bartering in order to increase your share in the profits, even if it makes you a few enemies.")
define Honest = Flaw("Honest","You won't tell a lie or engage in deceitful speech, even to save your own life or the life of another.")
define Hot_Tempered = Flaw("Hot Tempered","Your fuse is short and your explosions are destructive. Sometimes your anger boils slowly over time and other times it erupts completely unexpectedly. But when you do fly off the handle, things rarely go well for you.")
define Illiterate = Flaw("Illiterate","You can't read or write, even in languages that you speak fluently.")
define Literal_Minded = Flaw("Literal Minded","You struggle with concepts and turns of phrase that are not literally true, such as idioms and metaphors. You might think sorcery is afoot if someone tells you it is “raining cats and dogs”. If a friend exaggerates by saying “I'd kill myself if Melzak were elected Supreme Justice”, you would be genuinely concerned for your friend's life if Melzak did get elected.")
define Mood_Disorder = Flaw("Mood Disorder","You suffer from a psychological condition that directly affects your mood, such as depression or anxiety. You get to determine the nature and severity of your mood disorder.")
define Naive = Flaw("Naive","Whether you are innocent, uninformed, or inexperienced, the results are the same: you are pretty gullible. You get to define the scope of your naivety. For example, maybe you're a greenhorn from a big city on the east coast, so you are unlearned in the ways of the Wild West. Or maybe your memory was completely wiped out a few weeks ago and you are relearning the rules of civilization, thus your naivety presents itself much more universally.")
define Overt = Flaw("Overt","You have a strong aversion to subterfuge, legerdemain, and smooth talking. After all, the shortest distance between two points is a straight line, so why not follow the straight and narrow path? Your overtness may lead to you mistakenly foil the plans of allies, such as by blurting out a sensitive truth in the midst of a tense negotiation.")
define Overweight = Flaw("Overweight","You are carrying a few extra pounds, and they tend to get in the way at all the wrong times, such as when climbing a ladder or crossing a decrepit rope bridge.")
define Pacifist = Flaw("Pacifist","You disdain combat and bloodshed of any kind, and will generally do whatever possible to avoid it. You can decide the extent of your pacifism. You might just revert to violence as a last resort, or you may be so averse to combat that you won't lift a weapon even in defense of yourself or others.")
define Phobia = Flaw("Phobia","You are terrified and incapable of rational thought when you are presented with the object of your fear. It could be spiders, snakes, closed spaces, crowds, or something less common like co-dependence: a fear of being alone that causes you to always seek out companionship, even if that companionship has a negative impact on your life overall.")
define Proud = Flaw("Proud","Some call it an inflated ego. Others call it conceit. But you know that you really are just that good. The rabble are inferior, and you're not afraid to let them know. Your pride may be a universal sense of self-worth, or it may only manifest itself within certain spheres or situations. For example, your rank in the Royal Star Force leads you to look down upon anyone trained in less illustrious armed forces.")
define Psychotic = Flaw("Psychotic","You are severely mentally deranged to the extent that you occasionally lose touch with reality. You get to determine the extent and nature of your psychosis, including any potential triggers. For example, you might believe that beings from another dimension are trying to abduct you, or perhaps you relive a nightmarish scene from your past whenever you are in the midst of a gun fight.")
define Short_winded = Flaw("Short-winded","You have poor lung capacity and easily tire. Sprints, long runs, and forced marches are either impossible for you or they tend to leave you completely incapacitated afterwards.")
define Sick = Flaw("Sick","You suffer from some sort of chronic illness or condition, such as tuberculosis, cancer, arthritis, or irritable bowel syndrome. Even if you possess the means to treat your disease or control the symptoms, you might still have episodes or flare ups that hinder your adventuring life.")
define Socially_Awkward = Flaw("Socially Awkward","Something about your behavior tends to rub people the wrong way. Perhaps you don't respect the personal space of others, tend to ramble in conversation, or share overly personal details. Whatever the nature of your awkwardness, it makes social situations difficult for you at times.")
define Stubborn = Flaw("Stubborn","It's your way or the highway. Maybe not all of the time, but once you've made your mind up on an important matter, you won't budge. You probably won't even compromise.")
define Uncoordinated = Flaw("Uncoordinated","Your body just doesn't work well with itself. You have trouble balancing, catching, throwing, and performing similar physical tasks that require dexterity or nimbleness.")
define Vengeful = Flaw("Vengeful","You let no slight go unpunished. While some might be able to shake off an insult from a tavern drunk, you take it as a personal assault that demands satisfaction. The more severe the crime, the greater the vengeance you will mete out.")
define Zealous = Flaw("Zealous","You stand for a cause—whether it is a religion, a nation, a code, a way of life, or otherwise—and you will push the boundaries of normal behavior to uphold your cause. This might mean that you make yourself a social outcast by attempting to convert others to your cause, or it could mean that you are willing to perform an act you might otherwise consider evil, such as putting innocent lives in danger, if doing so would promote your cause.")