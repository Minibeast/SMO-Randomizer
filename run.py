# Made by Ian C aka Minibeast

import json
import datetime
import random
import configparser
import urllib.request
import sys
import pyperclip

version = "1.1.9"

cmd_run = len(sys.argv) > 1 and str(sys.argv[1]) == "console"

try:
    moons = open('moons.json')
    moons = json.load(moons)['results']
except FileNotFoundError:
    print('Moon data not found locally, downloading...')
    with urllib.request.urlopen('https://smo.kek.tech/api/v1/moons') as moondata:
        moons = (json.loads(moondata.read()))
    print('Download successful')

    if cmd_run:
        save = 'y'
    else:
        save = str(input('Would you like to store the moon data locally in the current directory (roughly 404 '
                         'kilobytes)? (y/n): '))

    if save.lower() == 'y':
        with open('moons.json', 'w+') as output:
            json.dump(moons, output)
    moons = moons['results']

collectedMoons = []
overrideArray = []

coin_moons = [217, 283, 329, 412, 453, 528, 598, 658, 740]
purple_moons = [228, 285, 342, 465, 466, 536, 537, 604, 660, 661, 742, 743]
deep_woods = list(range(334, 343))

settings = configparser.ConfigParser()
settings.read('settings.ini')

for items in settings['Overrides']:
    overrideArray.append(items)

peaceSkips = settings.getboolean('Settings', 'Peace-Skips')

if peaceSkips:
    # Sand
    moons[175]['moonTypes'] = None
    moons[176]['moonPrerequisites'] = None
    moons[184]['moonPrerequisites'] = None
    moons[188]['moonPrerequisites'] = None
    moons[220]['moonPrerequisites'] = None
    moons[176]['moonTypes'] = None
    # Snow
    moons[507]['moonTypes'] = None
    moons[508]['moonTypes'] = None
    moons[509]['moonTypes'] = None
    moons[510]['moonTypes'] = None


bowserSprinkle = settings.getboolean('Settings', 'Bowser-Story-End')
html_old = settings.getboolean('Settings', 'Old-CSS')


def rand(min, max):
    return random.randint(min, max)


print()

if cmd_run:
    if len(sys.argv) > 2:
        seed_option = sys.argv[2]
    else:
        print("No seed given, exiting")
        sys.exit()
else:
    seed_option = input("Seed (leave blank for none): ")
if not seed_option:
    seed = random.randrange(999999)
    print("\nNOTE: Due to a bug with Python random number generation, the application must be relaunched to use the "
          "generated seed properly.\nApologies for the inconvenience.")
    pyperclip.copy(seed)
    print("\nYour seed is {}. It has been copied to your clipboard.\n".format(str(seed)))
    input("Press enter to continue... ")
    sys.exit()
else:
    seed = seed_option
    random.seed(seed)

increment = 0

randomizer = open("randomizer.txt", "w+")
htmlrandomizer = open("randomizer.html", "w+")


def checkbox_generate(text):
    global increment
    increment += 1
    if html_old:
        return '<div class="checkbox"><input type="checkbox" id="' + str(increment) + '"/>\n<label class="strikethrough" for="' + str(increment) + '">' + str(text) + '</label>\n</div>\n'
    else:
        return '<li class="list-group-item" onclick="clicked(' + str(increment) + ')">\n<div class="checkbox"><input type="checkbox" id="' + str(increment) + '" onclick="clicked(' + str(increment) + ')"/>\n<label class="strikethrough">' + str(text) + '</label>\n</div>\n</li>\n'


def header_generate(text):
    if html_old:
        return "\n<h2>" + str(text) + "</h2>\n"
    else:
        return '<h3><div class="card">\n<div class="card-header">\n' + str(text) + '\n</div>\n<ul class="list-group list-group-flush">\n'


def randomize(min, max):
    value = rand(min, max)
    return moons[value]


def generatestory(min, max):
    while True:
        value = rand(min, max)
        if moons[value]["id"] not in collectedMoons:
            collectedMoons.append(moons[value]["id"])
            return moons[value]["name"]


def generate(min, max, prerequisite, amount):
    i = 0
    while i < amount:
        x = randomize(min, max)
        if str(x['id']) in overrideArray:
            if settings.getboolean('Overrides', str(x['id'])):
                if (x["moonPrerequisites"] is None or x["moonPrerequisites"][0]["id"] <= prerequisite) and (
                        x["id"] not in collectedMoons):
                    trait = ""
                    if x["id"] in coin_moons:
                        trait += " [100 Coins] "
                    if x["id"] in deep_woods:
                        trait += " [Deep Woods] "
                    if x["id"] in purple_moons:
                        trait += " [Outfit Moon] "
                    if x["id"] == 339:
                        trait += " [500 Coins] "
                    randomizer.write(x["name"] + trait + "\n")
                    htmlrandomizer.write(checkbox_generate(x["name"] + "<b>" + trait + "</b>"))
                    collectedMoons.append(x["id"])
                    i += 1
            else:
                collectedMoons.append(x["id"])
        if (x["moonPrerequisites"] is None or x["moonPrerequisites"][0]["id"] <= prerequisite) and (
                x["moonTypes"] is None or x["moonTypes"][0]["name"] != "Warp Painting") and (
                x["isPostGame"] is not True) and (x["requiresRevisit"] is not True) and (
                x["isStoryMoon"] is not True) and (x["moonTypes"] is None or (
                x["moonTypes"][0]["name"] != "Hint Art" and x["moonTypes"][0]["name"] != "Tourist")) and (
                x["id"] not in collectedMoons):
            trait = ""
            if x["id"] in coin_moons:
                trait += " [100 Coins] "
            if x["id"] in deep_woods:
                trait += " [Deep Woods] "
            if x["id"] in purple_moons:
                trait += " [Outfit Moon] "
            if x["id"] == 339:
                trait += " [500 Coins] "
            randomizer.write(x["name"] + trait + "\n")
            htmlrandomizer.write(checkbox_generate(x["name"] + "<b>" + trait + "</b>"))
            collectedMoons.append(x["id"])
            i += 1


date = datetime.datetime.now()

randomizer.write("SMO Randomizer generated on " + date.strftime("%b") + " " + date.strftime("%d") + " " + date.strftime("%Y") + " at " + date.strftime("%I") + ":" + date.strftime("%M") + " " + date.strftime("%p") + " (Version: " + version + ")")
randomizer.write("\nGenerated Seed: " + str(seed) + "\n")

header = '''<!DOCTYPE html>
<head>
    <title>Seed: {}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    <style>
        label.strikethrough {{
            line-height: 0.3;
            font-size: 15px;
        }}
        input[type=checkbox]:checked + label.strikethrough {{
            text-decoration: line-through;
        }}
        body {{
            width:50vw;
            margin:auto;
        }}
        .card{{
            margin-top:20px;
        }}
        .card-header{{
            font-size: 20px;
        }}
        li:hover {{
            background-color: #d3d3d3;
        }}
        
    </style>
</head>
<body>'''

if html_old:
    header = '''<!DOCTYPE html>
<head>
    <title>Seed: {}</title>
    <style>
        label.strikethrough{{
            line-height: 1.8;
        }}
        input[type=checkbox]:checked + label.strikethrough{{
            text-decoration: line-through;
        }}
    </style>
</head>
<body>'''

htmlrandomizer.write(header.format(str(seed)))
if html_old:
    htmlrandomizer.write("<h3>Generated on: " + date.strftime("%b") + " " + date.strftime("%d") + " " + date.strftime("%Y") + " at " + date.strftime("%I") + ":" + date.strftime("%M") + " " + date.strftime("%p") + " (Version: " + version + ")")
else:
    htmlrandomizer.write("\n<h3>Generated on " + date.strftime("%b") + " " + date.strftime("%d") + " " + date.strftime("%Y") + " at " + date.strftime("%I") + ":" + date.strftime("%M") + " " + date.strftime("%p") + "</h3>\n<h4>Version: " + version + "</h4>\n")

if len(overrideArray) > 0:
    randomizer.write("\nOVERRIDES:\n")
    htmlrandomizer.write("\n<h3>Overrides</h3>\n<ul>\n")

for x in overrideArray:
    randomizer.write(moons[int(x) - 1]["name"] + " = " + settings["Overrides"][x] + "\n")
    htmlrandomizer.write("<li>" + moons[int(x) - 1]["name"] + " = " + settings["Overrides"][x] + "</li>\n")

if len(overrideArray) > 0:
    htmlrandomizer.write("</ul>")

# Cascade
randomizer.write("\nCASCADE:\n")
htmlrandomizer.write(header_generate("Cascade"))

randomizer.write(moons[135]["name"] + "\n")
htmlrandomizer.write(checkbox_generate(moons[135]["name"]))

randomizer.write(moons[136]["name"] + " [3]\n")
htmlrandomizer.write(checkbox_generate(moons[136]["name"] + " [3]"))

generate(135, 174, 137, 1)
#

# Sand
moonCount = 0

randomizer.write("\nSAND: \n")
if not html_old:
    htmlrandomizer.write("</ul>\n</div>\n")
htmlrandomizer.write(header_generate("Sand"))

local = rand(0, 16)
moonCount += local

generate(175, 263, 0, local)

if moonCount < 16:
    randomizer.write(moons[175]["name"] + "\n")
    htmlrandomizer.write(checkbox_generate(moons[175]["name"]))
    moonCount += 1

    local = rand(0, 16 - moonCount)
    moonCount += local

    generate(175, 263, 176, local)

if not peaceSkips:
    if moonCount < 16:
        randomizer.write(moons[176]["name"] + "\n")
        htmlrandomizer.write(checkbox_generate(moons[176]["name"]))
        moonCount += 1

        local = rand(0, 16 - moonCount)
        moonCount += local

        generate(175, 263, 177, local)

        if moonCount < 14:
            randomizer.write(moons[177]["name"] + " [3]\n")
            htmlrandomizer.write(checkbox_generate(moons[177]["name"] + " [3]"))
            moonCount += 3

            local = rand(0, 16 - moonCount)
            moonCount += local

            generate(175, 263, 178, local)

            if moonCount < 14:
                randomizer.write(moons[178]["name"] + " [3]\n")
                htmlrandomizer.write(checkbox_generate(moons[178]["name"] + " [3]"))
                moonCount += 3

                generate(175, 263, 179, 16 - moonCount)
            elif 16 > moonCount >= 14:
                generate(175, 263, 177, 16 - moonCount)

        elif 16 > moonCount >= 14:
            generate(175, 263, 177, 16 - moonCount)
else:
    if moonCount < 14:
        randomizer.write(moons[177]["name"] + " [3]\n")
        htmlrandomizer.write(checkbox_generate(moons[177]["name"] + " [3]"))
        moonCount += 3

        local = rand(0, 16 - moonCount)
        moonCount += local

        generate(175, 263, 178, local)

        if moonCount < 14:
            randomizer.write(moons[178]["name"] + " [3]\n")
            htmlrandomizer.write(checkbox_generate(moons[178]["name"] + " [3]"))
            moonCount += 3

            generate(175, 263, 179, 16 - moonCount)
        elif 16 > moonCount >= 14:
            generate(175, 263, 177, 16 - moonCount)

    elif 16 > moonCount >= 14:
        generate(175, 263, 177, 16 - moonCount)

#

# Lake
moonCount = 0

randomizer.write("\nLAKE: \n")
if not html_old:
    htmlrandomizer.write("</ul>\n</div>\n")
htmlrandomizer.write(header_generate("Lake"))

local = rand(0, 8)
moonCount += local

generate(264, 305, 0, local)

if moonCount < 6:
    randomizer.write(moons[264]["name"] + " [3]\n")
    htmlrandomizer.write(checkbox_generate(moons[264]["name"] + " [3]"))
    moonCount += 3

    generate(264, 305, 265, 8 - moonCount)
elif 8 > moonCount >= 6:
    generate(264, 305, 0, 8 - moonCount)
#

# Wooded
moonCount = 0

randomizer.write("\nWOODED: \n")
if not html_old:
    htmlrandomizer.write("</ul>\n</div>\n")
htmlrandomizer.write(header_generate("Wooded"))

local = rand(0, 16)
moonCount += local

generate(306, 381, 0, local)

if moonCount < 16:
    randomizer.write(moons[306]["name"] + "\n")
    htmlrandomizer.write(checkbox_generate(moons[306]["name"]))
    moonCount += 1

    local = rand(0, 16 - moonCount)
    moonCount += local

    generate(306, 381, 307, local)

    if moonCount < 14:
        randomizer.write(moons[307]["name"] + " [3]\n")
        htmlrandomizer.write(checkbox_generate(moons[307]["name"] + " [3]"))
        moonCount += 3

        local = rand(0, 16 - moonCount)
        moonCount += local

        generate(306, 381, 308, local)

        if moonCount < 16:
            randomizer.write(moons[308]["name"] + "\n")
            htmlrandomizer.write(checkbox_generate(moons[308]["name"]))
            moonCount += 1

            local = rand(0, 16 - moonCount)
            moonCount += local

            generate(306, 381, 309, local)

            if moonCount < 14:
                randomizer.write(moons[309]["name"] + " [3]\n")
                htmlrandomizer.write(checkbox_generate(moons[309]["name"] + " [3]"))
                moonCount += 3

                generate(306, 381, 310, 16 - moonCount)
            elif 16 > moonCount >= 14:
                generate(306, 381, 309, 16 - moonCount)
    elif 16 > moonCount >= 14:
        generate(306, 381, 307, 16 - moonCount)
#

# Lost
randomizer.write("\nLOST: \n")
if not html_old:
    htmlrandomizer.write("</ul>\n</div>\n")
htmlrandomizer.write(header_generate("Lost"))

generate(391, 425, 0, 10)
#

# Metro
moonCount = 0

randomizer.write("\nMETRO: \n")
if not html_old:
    htmlrandomizer.write("</ul>\n</div>\n")
htmlrandomizer.write(header_generate("Metro"))

randomizer.write(moons[426]["name"] + " [3]\n")
htmlrandomizer.write(checkbox_generate(moons[426]["name"] + " [3]"))
moonCount += 3

local = rand(0, 20 - moonCount)
moonCount += local

generate(426, 506, 427, local)

if moonCount < 20:
    story = generatestory(427, 430)
    randomizer.write(story + "\n")
    htmlrandomizer.write(checkbox_generate(story))
    moonCount += 1

    local = rand(0, 20 - moonCount)
    moonCount += local

    generate(426, 506, 427, local)

    if moonCount < 20:
        story = generatestory(427, 430)
        randomizer.write(story + "\n")
        htmlrandomizer.write(checkbox_generate(story))
        moonCount += 1

        local = rand(0, 20 - moonCount)
        moonCount += local

        generate(426, 506, 427, local)

        if moonCount < 20:
            story = generatestory(427, 430)
            randomizer.write(story + "\n")
            htmlrandomizer.write(checkbox_generate(story))
            moonCount += 1

            local = rand(0, 20 - moonCount)
            moonCount += local

            generate(426, 506, 427, local)

            if moonCount < 20:
                story = generatestory(427, 430)
                randomizer.write(story + "\n")
                htmlrandomizer.write(checkbox_generate(story))
                moonCount += 1

                local = rand(0, 20 - moonCount)
                moonCount += local

                generate(426, 506, 428, local)

                if moonCount < 20:
                    randomizer.write(moons[431]["name"] + "\n")
                    htmlrandomizer.write(checkbox_generate(moons[431]["name"]))
                    moonCount += 1

                    local = rand(0, 20 - moonCount)
                    moonCount += local

                    generate(426, 506, 432, local)

                    if moonCount < 18:
                        randomizer.write(moons[432]["name"] + " [3]\n")
                        htmlrandomizer.write(checkbox_generate(moons[432]["name"] + " [3]"))
                        moonCount += 3

                        generate(426, 506, 433, 20 - moonCount)
                    elif 20 > moonCount >= 18:
                        generate(426, 506, 432, 20 - moonCount)

#

# Snow
moonCount = 0

randomizer.write("\nSNOW: \n")
if not html_old:
    htmlrandomizer.write("</ul>\n</div>\n")
htmlrandomizer.write(header_generate("Snow"))

local = rand(0, 10)
moonCount += local

generate(507, 561, 0, local)

if not peaceSkips:
    if moonCount < 10:
        story = generatestory(507, 510)
        randomizer.write(story + "\n")
        htmlrandomizer.write(checkbox_generate(story))
        moonCount += 1

        local = rand(0, 10 - moonCount)
        moonCount += local

        generate(507, 561, 0, local)

        if moonCount < 10:
            story = generatestory(507, 510)
            randomizer.write(story + "\n")
            htmlrandomizer.write(checkbox_generate(story))
            moonCount += 1

            local = rand(0, 10 - moonCount)
            moonCount += local

            generate(507, 561, 0, local)

            if moonCount < 10:
                story = generatestory(507, 510)
                randomizer.write(story + "\n")
                htmlrandomizer.write(checkbox_generate(story))
                moonCount += 1

                local = rand(0, 10 - moonCount)
                moonCount += local

                generate(507, 561, 0, local)

                if moonCount < 10:
                    story = generatestory(507, 510)
                    randomizer.write(story + "\n")
                    htmlrandomizer.write(checkbox_generate(story))
                    moonCount += 1

                    local = rand(0, 10 - moonCount)
                    moonCount += local

                    generate(507, 561, 0, local)

                    if moonCount < 8:
                        randomizer.write(moons[511]["name"] + " [3]\n")
                        htmlrandomizer.write(checkbox_generate(moons[511]["name"] + " [3]"))
                        moonCount += 3

                        generate(507, 561, 512, 10 - moonCount)
                    elif 10 > moonCount >= 8:
                        generate(507, 561, 0, 10 - moonCount)
else:
    if moonCount < 8:
        randomizer.write(moons[511]["name"] + " [3]\n")
        htmlrandomizer.write(checkbox_generate(moons[511]["name"] + " [3]"))
        moonCount += 3

        generate(507, 561, 512, 10 - moonCount)
    elif 10 > moonCount >= 8:
        generate(507, 561, 0, 10 - moonCount)
#

# Seaside
moonCount = 0

randomizer.write("\nSEASIDE: \n")
if not html_old:
    htmlrandomizer.write("</ul>\n</div>\n")
htmlrandomizer.write(header_generate("Seaside"))

local = rand(0, 10)
moonCount += local

generate(562, 632, 0, local)

if moonCount < 10:
    story = generatestory(562, 565)
    randomizer.write(story + "\n")
    htmlrandomizer.write(checkbox_generate(story))
    moonCount += 1

    local = rand(0, 10 - moonCount)
    moonCount += local

    generate(562, 632, 0, local)

    if moonCount < 10:
        story = generatestory(562, 565)
        randomizer.write(story + "\n")
        htmlrandomizer.write(checkbox_generate(story))
        moonCount += 1

        local = rand(0, 10 - moonCount)
        moonCount += local

        generate(562, 632, 0, local)

        if moonCount < 10:
            story = generatestory(562, 565)
            randomizer.write(story + "\n")
            htmlrandomizer.write(checkbox_generate(story))
            moonCount += 1

            local = rand(0, 10 - moonCount)
            moonCount += local

            generate(562, 632, 0, local)

            if moonCount < 10:
                story = generatestory(562, 565)
                randomizer.write(story + "\n")
                htmlrandomizer.write(checkbox_generate(story))
                moonCount += 1

                local = rand(0, 10 - moonCount)
                moonCount += local

                generate(562, 632, 0, local)

                if moonCount < 8:
                    randomizer.write(moons[566]["name"] + " [3]\n")
                    htmlrandomizer.write(checkbox_generate(moons[566]["name"] + " [3]"))
                    moonCount += 3

                    generate(562, 632, 567, 10 - moonCount)
                elif 10 > moonCount >= 8:
                    generate(562, 632, 0, 10 - moonCount)

#

# Luncheon
moonCount = 0

randomizer.write("\nLUNCHEON: \n")
if not html_old:
    htmlrandomizer.write("</ul>\n</div>\n")
htmlrandomizer.write(header_generate("Luncheon"))

randomizer.write(moons[633]["name"] + "\n")
htmlrandomizer.write(checkbox_generate(moons[633]["name"]))
moonCount += 1

local = rand(0, 14)
moonCount += local

generate(633, 700, 634, local)

if moonCount < 18:
    randomizer.write(moons[634]["name"] + "\n")
    htmlrandomizer.write(checkbox_generate(moons[634]["name"]))
    moonCount += 1

    local = rand(0, 18 - moonCount)
    moonCount += local

    generate(633, 700, 635, local)

    if moonCount < 16:
        randomizer.write(moons[635]["name"] + " [3]\n")
        htmlrandomizer.write(checkbox_generate(moons[635]["name"] + " [3]"))
        moonCount += 3

        local = rand(0, 18 - moonCount)
        moonCount += local

        generate(633, 700, 636, local)

        if moonCount < 18:
            randomizer.write(moons[636]["name"] + "\n")
            htmlrandomizer.write(checkbox_generate(moons[636]["name"]))
            moonCount += 1

            local = rand(0, 18 - moonCount)
            moonCount += local

            generate(633, 700, 637, local)

            if moonCount < 16:
                randomizer.write(moons[637]["name"] + " [3]\n")
                htmlrandomizer.write(checkbox_generate(moons[637]["name"] + " [3]"))
                moonCount += 3

                generate(633, 700, 638, 18 - moonCount)

            elif 18 > moonCount >= 16:
                generate(633, 700, 637, 18 - moonCount)
    elif 18 > moonCount >= 16:
        generate(633, 700, 635, 18 - moonCount)
#

# Bowser's
moonCount = 6

randomizer.write("\nBOWSERS: \n")
if not html_old:
    htmlrandomizer.write("</ul>\n</div>\n")
htmlrandomizer.write(header_generate("Bowsers"))

randomizer.write(moons[711]["name"] + "\n")
htmlrandomizer.write(checkbox_generate(moons[711]["name"]))
randomizer.write(moons[712]["name"] + "\n")
htmlrandomizer.write(checkbox_generate(moons[712]["name"]))
randomizer.write(moons[713]["name"] + "\n")
htmlrandomizer.write(checkbox_generate(moons[713]["name"]))
randomizer.write(moons[714]["name"] + " [3]\n")
htmlrandomizer.write(checkbox_generate(moons[714]["name"] + " [3]"))

sprinkleID = 715

if bowserSprinkle:
    sprinkleID = 714

generate(711, 772, sprinkleID, 8 - moonCount)

randomizer.close()
if not html_old:
    htmlrandomizer.write("<script>\nfunction clicked(id) {\ndocument.getElementById(id).checked = !document.getElementById(id).checked;\n}\n</script>\n")
htmlrandomizer.write("</body>")
htmlrandomizer.close()
