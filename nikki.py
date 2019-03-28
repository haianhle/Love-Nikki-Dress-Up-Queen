#!/usr/bin/python

import numpy as np
import json
import sys
from operator import itemgetter
try:
    from urllib.request import urlopen 
except ImportError:
    from urllib2 import urlopen

######### define class Wardrobe_item ##########
class Wardrobe_item:
    kind = 'Clothing'

    def __init__(self, unique_id, itemid, title, type, supertype, subtype, rarity, tags):
        self.unique_id = unique_id
        self.itemid = itemid
        self.title = title
        self.type = type
        self.supertype = supertype
        self.subtype = subtype
        self.rarity = rarity
        self.stats = []
        self.tags = tags

    def add_stats(self, stat):
        self.stats.append(stat)

######### define class Wardrobe_stats##########
class Wardrobe_stats:
    def __init__(self, stat, score):
        self.stat = stat
        self.score = score 

#########
clothing_type = ["Hair", "Dress", "Top", "Bottom", "Coat", "Hosiery", "Shoes", "Makeup", "Accessory"]
supertype_tree = [[], [], [], [], [], ["Socks", "Anklet"], [], [], \
                 ["Headwear", "Earrings", "Neckwear", "Bracelet", "Handheld", "Waist", "Special"]]
subtype_tree = [[], [], [], [], [], [[], []], [], [], [["Hair ornaments", "Veil", "Hairpin", "Ear"], [], \
               ["Scarf", "Necklace"], ["Right hand ornaments", "Left hand ornaments", "Gloves"], \
               ["Right hand holding", "Left hand holding", "Both hand holding"], [], \
               ["Face", "Brooch", "Tattoo", "Wing", "Tail", "Foreground", "Background", "Head ornaments", "Ground", "Skin"]]]
tag_list = ["Sun Care", "Dancer", "Floral", "Winter", "Britain", "Swimsuit", "Shower", "Kimono", "Pajamas", "Wedding", \
            "Army", "Office", "Apron", "Cheongsam", "Maiden", "Evening Gown", "Navy", "Traditional", "Bunny", "Lady", \
            "Lolita", "Gothic", "Sports", "Harajuku", "Preppy", "Unisex", "Future", "Fairy", "Rock", "Denim", "Pet", \
            "Goddess", "POP", "Homewear", "Chinese Classical", "Hindu", "Republic of China", "European", "Swordsman", \
            "Rain", "Modern China", "Dryad", "Bohemia", "Paramedics"]
type_list = []
uniquetype_list = []
for i in range(0, len(clothing_type)):
    assert(len(supertype_tree[i]) == len(subtype_tree[i]))
    if len(supertype_tree[i]) == 0:
        type_list.append([clothing_type[i], None, None])
        uniquetype_list.append(clothing_type[i])
    else:
        for j in range(0, len(supertype_tree[i])):
            if len(subtype_tree[i][j]) == 0:
                type_list.append([clothing_type[i], supertype_tree[i][j], None])
                uniquetype_list.append(supertype_tree[i][j])
            else:
                for k in range(0, len(subtype_tree[i][j])):
                    type_list.append([clothing_type[i], supertype_tree[i][j], subtype_tree[i][j][k]])
                    uniquetype_list.append(subtype_tree[i][j][k])
generaltype_list = clothing_type
for i in supertype_tree:
    for j in i:
        if j not in generaltype_list:
            generaltype_list.append(j)
for i in subtype_tree:
    for j in i:
        for k in j:
            if k not in generaltype_list:
                generaltype_list.append(k)

stats_list = ["Simple", "Gorgeous", "Elegance", "Lively", "Mature", "Cute", "Sexy", "Pure", "Warm", "Cool"]

## score_num is 10.00 for SS+, then decrease in increments of 0.45 (which gives 3.70 for C-), then jump to 0.0 for F
## This approximately reproduces the empirically determined point values which can be found online
score_list = ["SSS", "SS+", "SS", "SS-", "S+", "S", "S-", "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-"]
score_num =  []
for i in range(0, len(score_list)-1):
    score_num.append(10.0 - i*0.45)
score_map = dict(zip(score_list, score_num))
##print "Score mapping:", score_map

########## parse data from raw wardrobe info ##########
#with open("WardrobeInfo.json") as wardrobe_file:
#    wardrobe = json.load(wardrobe_file)
url = 'http://db.lovenikki.world/json/WardrobeInfo.json'
response = urlopen(url)
wardrobe_file = response.read()
wardrobe = json.loads(wardrobe_file)

all_items = []
for item in wardrobe:
    itemid = item.get("ItemID")
    title = item.get("Title")
    typeindex = item.get("Type")-1

    # When designing full outfits the order items are listed in game is not the most convenient
    reorder_indices = [ 0, 1, 4, 2, 3, 5, 6, 8, 7 ]
    typeindex = reorder_indices[typeindex]
    type = clothing_type[typeindex]

    supertype = item.get("Supertype") 
    subtype = item.get("Subtype")

    # For some weird reason Waist items are labeled as "0" in the data dump
    supertype = supertype if supertype != "0" else "Waist"
    supertype = supertype if supertype != "Hosiery" else "Socks"
    supertype = supertype if supertype != "Necklace" else "Neckwear"

    # Correct for errors in the input file...
    supertype = supertype if supertype != "Wrists" else "Bracelet"
    subtype = subtype if subtype != "Hair Ornament" else "Hair ornaments"

    rarity = item.get("Rarity")
    number = item.get("N")

    tags = item.get("Tag")
    tags = [] if tags is None else str(tags).strip().strip(",").split(",")
    tags = map(str.strip, tags)

    new_item = Wardrobe_item(number, itemid, title, type, supertype, subtype, rarity, tags)
    for s in stats_list:
        score = item.get(s)
        if score is not None:
            score = str(score).strip()
            new_stat = Wardrobe_stats(s, score)
            new_item.add_stats(new_stat)        

    all_items.append(new_item)

#for n in all_items:
#    print n.unique_id, n.title, n.type, n.supertype, n.subtype, n.tags


##########
## Some assert checks on the fidelity of input data
##########

for n in all_items:
    assert(len(list(n.tags)) >= 0 and len(list(n.tags)) <= 2)
    assert(all(tag in tag_list for tag in n.tags))
##    assert([n.type, n.supertype, n.subtype] in type_list) ## Fri 2/16 not passed

########## Print items with specific stats ##########
def input_list(yourlist):
     listSTR=input(yourlist)     
     listSTR =listSTR[0:len(listSTR)]
     listT = listSTR.split(",")
     listEnd=[]
     for caseListT in listT:
          listEnd.append(str(caseListT).strip())
     return listEnd

############# Getting stats for stylst arena mode ###########
stylist_mode = str(input("Stylist arena mode? (Y/N) ")).capitalize()
manual_mode = True
if stylist_mode == "Y" or stylist_mode == "Yes":
    manual_mode = False
    target_theme = str(input("Which theme? (e.g., The Queen, Cloud Lady, etc.) ")).capitalize()
    with open("stylist_themes.json") as theme_file:
        items = json.load(theme_file)
    target_stats = []
    weights_s = []
    for i in items:
        theme = i.get("Theme")
        if theme.lower() == target_theme.lower():
            for s in stats_list:
                wt = i.get(s)
                if wt is not None:
                    target_stats.append(s)
                    weights_s.append(float(wt))

    print("For theme", target_theme, "the target stats and weights are:")
    for i in range(len(target_stats)):
        print(target_stats[i], weights_s[i])
else:
    ###### Ask the user for which stats we are trying to match, and verify valid input
    valid = False
    while not valid:
        valid = True
        target_stats = input_list("Stats you are looking for (e.g., Simple, Lively, Cute):  ")
        target_stats = [item for entry in target_stats for item in entry.split()]
        target_stats = list(map(str.capitalize, target_stats))
        for istat in target_stats:
            if istat not in stats_list:
                print("Requested stat not recognized: " + istat)
                print("Valid stats are as follows:  " + str(stats_list))
                valid = False
        if "Simple" in target_stats and "Gorgeous" in target_stats:
            print("Simple and Gorgeous are conflicting stats; choose only one.")
            valid = False
        if "Elegance" in target_stats and "Lively" in target_stats:
            print("Elegance and Lively are conflicting stats; choose only one.")
            valid = False
        if "Cute" in target_stats and "Mature" in target_stats:
            print("Cute and Mature are conflicting stats; choose only one.")
            valid = False
        if "Sexy" in target_stats and "Pure" in target_stats:
            print("Sexy and Pure are conflicting stats; choose only one.")
            valid = False
        if "Cool" in target_stats and "Warm" in target_stats:
            print("Cool and Warm are conflicting stats; choose only one.")
            valid = False

## now we should have the stats either entered manually or from stylist arena database
nstat = len(list(target_stats))
print(nstat, "stats: ", target_stats)

valid = False
while not valid:
    valid = True
    target_tags = "" if manual_mode == False else input_list("Tags you are looking for (e.g., Rock, Fairy, Kimono):  ")
    target_tags = target_tags if target_tags != [""] else []
    target_tags = list(map(str.title, target_tags))
    list_target_tags = list(target_tags)
    for i in range(0, len(list_target_tags)):
        list_target_tags[i] = list_target_tags[i] if list_target_tags[i] != "Pop" else "POP"
        list_target_tags[i] = list_target_tags[i] if list_target_tags[i] != "Republic Of China" else "Republic of China"
        if list_target_tags[i] not in tag_list:
            print("Requested tag not recognized: " + list_target_tags[i])
            print("Valid tags are as follows:  " + str(tag_list))
            valid = False
ntag = len(list_target_tags)
if ntag > 0:
    print(ntag, "tags: ", target_tags)

valid = False
while not valid:
    valid = True
    item_type = str(input("What are you looking for?  Name an item type or \"Outfit\":  ")).capitalize()
    if item_type != "" and item_type != "Outfit" and item_type not in generaltype_list:
        print("Here are the valid choices; you can also leave it blank or specify \"Outfit\":  ")
        print(generaltype_list)
        print("Requested item type not recognized: " + item_type)
        valid = False
print("All items searched" if item_type == "" else "Type: " + item_type)

if item_type == "Outfit":
    newval = str(input("How many items should we show for each category? (default 12) "))
    nitem_display = 12 if newval == "" else int(newval)

weights_t = [1.0]*len(list(target_tags))
if manual_mode:
    weights_s = [1.0]*len(list(target_stats))
    manual_mode = str(input("Scoring with different weights? (Y/N) ")).capitalize()
    if manual_mode == "Y" or manual_mode == "Yes":
        for i in range(len(list(target_stats))):
            weights_s[i] = float(input("Enter weight for " + target_stats[i] + ": "))
        for i in range(len(list(target_tags))):
            weights_t[i] = float(input("Enter weight for " + target_tags[i] + ": "))
weight_map_s = dict(zip(target_stats, weights_s))
weight_map_t = dict(zip(target_tags, weights_t))

if item_type == "Outfit":
    wrong_stats = True
else:
    wrong_stats = str(input("Display items with some wrong stats? (Y/N) ")).capitalize()
    wrong_stats = True if (wrong_stats == "Y" or wrong_stats == "Yes") else False

items = []
for n in all_items:
    if n.type == item_type or n.supertype == item_type or n.subtype == item_type or item_type == "" or item_type == "Outfit":
        current_stats = []
        for s in n.stats:
            current_stats.append(s.stat)
    
        if wrong_stats == True or (set(sorted(target_stats)) <= set(sorted(current_stats)) and set(sorted(target_tags)) <= set(sorted(n.tags))):
            score = 0.0
            for s in n.stats:
                if s.stat in target_stats:
                    trim_score = s.score.replace(" ", "")
                    score += weight_map_s[s.stat] * score_map[trim_score]
  
            #TODO What is the correct coefficient to apply to tag bonuses?
            #TODO 12.5 set here arbitrarily; probably does not match in-game value 
            for s in n.tags:
                if s in target_tags:
                    score += weight_map_t[s] * 12.5
            items.append([n, score])
          
if (item_type != "Outfit"):
    items = sorted(items, key=itemgetter(1))
    for n in items:
        print(n[0].unique_id, n[0].title, " *** score ", n[1])
        for s in n[0].stats:
            print(s.stat, s.score)
        if len(list(n[0].tags)) > 0:
            print(n[0].tags)
        print("")
    print("Number of items with desired stats = ", len(items))

else:
    items_by_type = []
    assert(len(uniquetype_list) == len(type_list))
    for index in range(0, len(type_list)):
        i = len(type_list) - index - 1
        print("Item type: ", uniquetype_list[i])
        print("")
        subset = []
        for j in items:
            if [j[0].type, j[0].supertype, j[0].subtype] == type_list[i]:
                subset.append(j)
        subset = sorted(subset, key=itemgetter(1))
        nprint = min(nitem_display, len(subset))
        for nindex in range(0, nprint):
            n = len(subset) - nprint + nindex
            print(subset[n][0].unique_id, subset[n][0].title, " *** score ", subset[n][1])
            for s in subset[n][0].stats:
                print(s.stat, s.score)
            if len(list(subset[n][0].tags)) > 0:
                print(subset[n][0].tags)
            print("")
        print("Item type: ", uniquetype_list[i])
        print("")
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("")

print("Happy landing!")

