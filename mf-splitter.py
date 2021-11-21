#!/usr/bin/python
# -*- coding: utf-8 -*-

# Unofficial Minifantasy sprite splitter and organizer by dn503 (Python is not my main language - so be kind)
# Apache License 2.0 - see accompanying file

import sys, getopt, os, re

def getfilesrecursive(dir, ext):
    files = []
    dot_ext = "." + ext.lower()
    for it in os.scandir(dir):
        if it.is_file:
            if it.path.lower().endswith(dot_ext):
                files.append(it.path)
            elif it.is_dir():
                files += getfilesrecursive(it.path, ext)
    return files

def print_usage():
    print('splitter.py -i <inputdir> -o <outputdir>')

def main(argv):
    input_path = ''
    output_path = ''
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'hi:o:',
                ['input_path=','output_path='])
    except getopt.GetoptError as err:
        print(err)
        print_usage()
        sys.exit(2)
    for (opt, arg) in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ('-i', '--input_path'):
            input_path = arg
        elif opt in ('-o', '--output_path'):
            output_path = arg
    if input_path == '' or output_path == '':
        print_usage()
        sys.exit(2)
        
    if not os.path.exists(input_path):
        print("supplied input_path (" + input_path + ") does not exist!")
        sys.exit(2)
        
    if not os.path.isdir(input_path):
        print("supplied input_path (" + input_path + ") is not a directory!")
        sys.exit(2)
    
    replacement_words = { "Sorcer" : "Sorcery", "Bir" : "Bird", "Wamp" : "Swamp", "Merchan" : "Merchant", "Campsites" : "Campsite", "Minifanasy" : "Minifantasy", "Munifantasy" : "Minifantasy", "Fotgotten" : "Forgotten", "Cunting" : "Cutting", "Mocku" : "Mockup", "Castingl":"Casting", "Tiless":"Tiles", "Stallt":"Stall", "Candels":"Candles", "Structureshadows":"Structure Shadows", "Lengendary":"Legendary", "()":"", ", ":"", "Goshbuster":"Ghostbuster", "L":"", "- ":""}
    
    words_to_merge = {"Icy":["Wilderness", "Breeze"], "Tiny":["Overworld"], "Desolate":["Desert"], "Mock":["Up"], "Silent":["Swamp"], "Forgotten":["Plains"], "All":["Props","Tiles","Traps"], "Deep":["Caves"], "Mad":["Inventor"], "Giant":["Sword","Mushrooms","Spider"], "Tall":["Grass"], "Ancient":["Vampire","Troll"], "Spider":["Queen"], "Mid":["Bird"], "Small":["Bird"], "Big":["Bird"], "Bronze":["Cultist"], "Green":["Cultist", "Frog"], "Legendary":["Set"], "Text":["Input"], "Text Input":["Field"], "Check":["Boxes"], "Check Boxes And Radio":["Buttons"], "Speech":["Bubbles"], "Day":["Night"], "Day Night":["Dial"], "Pine":["Trees","Tree"], "Birch":["Tree"], "Willow":["Tree"], "Chopping":["Tree"], "Ground":["Light"], "Not":["Lit"], "Pole":["Light"], "Takeoff":["Landing"], "Petrified":["People"], "Armored":["Warrior"], "Sacrifice":["Altar","Candles"], "Wooden":["House", "Bridge"], "Blade":["Trap"], "Stone":["Wall","Block"], "Pit":["Trap"], "Towns":["II"], "Belts":["Pants"], "Belts Pants":["Gloves"], "Belt Pants Gloves":["Cloaks"], "Dr.":["Who"], "Polar":["Bear","Fox"], "Adventurers":["Campsite"], "Murky":["Swamp"], "Orange":["Fox"], "Plant":["Pots"], "Poisonous":["Swamp"] }
    
    words_to_compress = {"Dr":".", "NP":["Cs"]}
    
    words_to_combine_with_gap = ["And", "Or", "To", "Of"]
    
    words_to_combine_no_gap = ["-"]
    
    animals = ["Mouse", "Gorilla", "Rat", "Bear", "Hedgehog", "Skunk", "Squirrel", "Badger", "Ostrich", "Tortoise", "Cat","Horse", "Kangaroo", "Goat", "Camel", "Panda", "Hippo", "Moose", "Platypus", "Elephant", "Tiger", "Hyena", "Rhino", "Polar Bear", "Polar Fox","Lion","Lioness","Snake", "Bird", "Mid Bird", "Small Bird", "Big Bird", "Skink", "Lizard", "Green Frog", "Orange Fox", "Dog"]
    
    creatures = ["Dragon", "Werewolf", "Beholder", "Beholder 360", "Wraith", "Giant Spider", "Giant Mushrooms", "Ancient Vampire", "Spider Queen", "Giant", "Medusa", "Gargoyle", "Ancient Troll", "Saurus"]
    
    humanoids = ["Bronze Cultist", "Cultist", "Cultist 1", "Cultist 2","Cultist 3","Green Cultist","Hunter","King","Lumberjack","Mad Inventor","Merchant","Miner","Petrified People","Armored Warrior","Farmer"]

    files = getfilesrecursive(input_path, "png")
    for filename in files:
#        print(filename)
        
        file_path = os.path.normpath(filename)
        folder_list = file_path.split(os.sep)
        filename_without_extension = folder_list[-1].rsplit( ".", 1 )[ 0 ]
        
        words_in_filename = re.findall('[A-Z][a-z]*|[a-z]+|[^_ ][^A-Za-z0-9]*', filename_without_extension)
        cap_words = [w.capitalize() for w in words_in_filename]
 #       print(cap_words)
        
        clean_words = []
        for word in cap_words:
            if word in replacement_words:
                clean_words.append(replacement_words[word])
            else:
                clean_words.append(word.replace('_', ''))
#        print(clean_words)

        i = 0
        while i < len(clean_words) - 1:
            if len(clean_words[i]) == 1:
                j = i + 1
                while j < len(clean_words):
                    if len(clean_words[j]) == 1:
                        clean_words[i] += clean_words[j]
                        clean_words[j] = ""
                    j += 1
            i += 1
                
        while("" in clean_words) :
            clean_words.remove("")
            
        i = 0
        while i < len(clean_words):
            if clean_words[i].isdigit() and i > 0:
                clean_words[i] = clean_words[i - 1] + " " + clean_words[i]
                clean_words[i - 1] = ""
            elif clean_words[i] in words_to_combine_with_gap and i > 0 and i < len(clean_words) - 1:
                clean_words[i + 1] = clean_words[i - 1] + " " + clean_words[i] + " " + clean_words[i + 1]
                clean_words[i - 1] = ""
                clean_words[i] = ""
            elif clean_words[i] in words_to_combine_no_gap and i > 0 and i < len(clean_words) - 1:
                clean_words[i + 1] = clean_words[i - 1] + clean_words[i] + clean_words[i + 1]
                clean_words[i - 1] = ""
                clean_words[i] = ""
            elif clean_words[i] in words_to_merge and i < len(clean_words) - 1 and clean_words[i + 1] in words_to_merge[clean_words[i]]:
                clean_words[i + 1] = clean_words[i] + " " + clean_words[i + 1]
                clean_words[i] = ""
            elif clean_words[i] in words_to_compress and i < len(clean_words) - 1 and clean_words[i + 1] in words_to_compress[clean_words[i]]:
                clean_words[i + 1] = clean_words[i] + clean_words[i + 1]
                clean_words[i] = ""
            elif clean_words[i] == "Mini" and i < len(clean_words) - 1 and clean_words[i + 1] == "Fantasy":
                clean_words[i + 1] = "Minifantasy"
                clean_words[i] = ""
            else:
                i += 1
        
        while("" in clean_words) :
            clean_words.remove("")
        if len(clean_words) == 0:
            continue
        if clean_words[0].lower() != "minifantasy":
            clean_words.insert(0, "Minifantasy")
            
        i = 0
        while i < len(clean_words):
            if "Icons" in clean_words[i]:
                if clean_words[i] == "Icons":
                    clean_words[i] = ""
                if clean_words[1] != "Icons":
                    clean_words.insert(1, "Icons")
            elif clean_words[i].startswith("Crafting And Professions"):
                clean_words[i] = "Crafting And Professions"
            elif clean_words[i] == "Towns II":
                clean_words[i] = "Towns"
            elif clean_words[i].lower().endswith("walk") and not (clean_words[i].startswith("Side") or clean_words[i] == "Walk"):
                clean_words[i] = clean_words[i][:-4]
                clean_words.insert(i + 1, "Walk")
                i += 1
            elif i == 1 and clean_words[i] in animals:
                clean_words.insert(1, "Animals")
            elif i == 1 and clean_words[i] in creatures:
                clean_words.insert(1, "Creatures")
            elif i == 1 and clean_words[i] in humanoids:
                clean_words.insert(1, "Humanoids")
            i += 1
                    
        while("" in clean_words) :
            clean_words.remove("")
#        print(clean_words)
        
        clean_words.insert(0, output_path)
        new_path = os.path.join(*(clean_words))
        new_path_lower = new_path.lower()
        if "mockup" in new_path_lower or "mock up" in new_path_lower or "sample" in new_path_lower:
            continue
        print(new_path)


if __name__ == '__main__':
    main(sys.argv)
