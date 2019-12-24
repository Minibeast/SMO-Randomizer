# Made by Ian C aka Minibeast

import json
import datetime
import random
import configparser


with open("moons.json") as moondata:
    moons = json.load(moondata)["results"]

randomizer = open("randomizer.txt", "w+")
collectedMoons = []
overrideArray = []


settings = configparser.ConfigParser()
settings.read('settings.ini')

for items in settings['Overrides']:
    overrideArray.append(items)


def rand(min, max):
    return int(random.uniform(min, max) + 0.5)


seed_option = input("Seed (leave blank for none): ")
if not seed_option:
    seed = rand(10000, 99999)
    random.seed(seed)
else:
    seed = seed_option
    random.seed(seed)


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
            if settings['Overrides'][str(x['id'])] == 'true':
                if x["moonPrerequisites"] is None or x["moonPrerequisites"][0]["id"] <= prerequisite:
                    randomizer.write(x["name"] + "\n")
                    collectedMoons.append(x["id"])
                    i += 1
            else:
                collectedMoons.append(x["id"])
        if (x["moonPrerequisites"] is None or x["moonPrerequisites"][0]["id"] <= prerequisite) and (x["moonTypes"] is None or x["moonTypes"][0]["name"] != "Warp Painting") and (x["isPostGame"] is not True) and (x["requiresRevisit"] is not True) and (x["isStoryMoon"] is not True) and (x["moonTypes"] is None or (x["moonTypes"][0]["name"] != "Hint Art" and x["moonTypes"][0]["name"] != "Tourist")) and (x["id"] not in collectedMoons):
            randomizer.write(x["name"] + "\n")
            collectedMoons.append(x["id"])
            i += 1


date = datetime.datetime.now()

randomizer.write("SMO Randomizer generated on " + date.strftime("%b") + " " + date.strftime("%d") + " " + date.strftime("%Y") + " at " + date.strftime("%I") + ":" + date.strftime("%M") + " " + date.strftime("%p"))
randomizer.write("\nGenerated Seed: " + str(seed) + "\n")

moonCount = 0

# Cascade
randomizer.write("\nCASCADE:\n")

randomizer.write(moons[135]["name"] + "\n")

local = rand(moonCount, 1)
moonCount += local

generate(135, 174, 136, local)

randomizer.write(moons[136]["name"] + " [3]\n")

generate(135, 174, 137, 1 - moonCount)
#

# Sand
moonCount = 0

randomizer.write("\nSAND: \n")

local = rand(0, 16)
moonCount += local

generate(175, 263, 0, local)

if moonCount < 16:
    randomizer.write(moons[175]["name"] + "\n")
    moonCount += 1

    local = rand(0, 16 - moonCount)
    moonCount += local

    generate(175, 263, 176, local)

    if moonCount < 16:
        randomizer.write(moons[176]["name"] + "\n")
        moonCount += 1

        local = rand(0, 16 - moonCount)
        moonCount += local

        generate(175, 263, 177, local)

        if moonCount < 14:
            randomizer.write(moons[177]["name"] + " [3]\n")
            moonCount += 3

            local = rand(0, 16 - moonCount)
            moonCount += local

            generate(175, 263, 178, local)

            if moonCount < 14:
                randomizer.write(moons[178]["name"] + " [3]\n")
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

local = rand(0, 8)
moonCount += local

generate(264, 305, 0, local)

if moonCount < 6:
    randomizer.write(moons[264]["name"] + " [3]\n")
    moonCount += 3

    generate(264, 305, 265, 8 - moonCount)
elif 8 > moonCount >= 6:
    generate(264, 305, 0, 8 - moonCount)
#

# Wooded
moonCount = 0

randomizer.write("\nWOODED: \n")

local = rand(0, 16)
moonCount += local

generate(306, 381, 0, local)

if moonCount < 16:
    randomizer.write(moons[306]["name"] + "\n")
    moonCount += 1

    local = rand(0, 16 - moonCount)
    moonCount += local

    generate(306, 381, 307, local)

    if moonCount < 14:
        randomizer.write(moons[307]["name"] + " [3]\n")
        moonCount += 3

        local = rand(0, 16 - moonCount)
        moonCount += local

        generate(306, 381, 308, local)

        if moonCount < 16:
            randomizer.write(moons[308]["name"] + "\n")
            moonCount += 1

            local = rand(0, 16 - moonCount)
            moonCount += local

            generate(306, 381, 309, local)

            if moonCount < 14:
                randomizer.write(moons[309]["name"] + " [3]\n")
                moonCount += 3

                generate(306, 381, 310, 16 - moonCount)
            elif 16 > moonCount >= 14:
                generate(306, 381, 309, 16 - moonCount)
    elif 16 > moonCount >= 14:
        generate(306, 381, 307, 16 - moonCount)
#

# Lost
randomizer.write("\nLOST: \n")

generate(391, 425, 0, 8)
#

# Metro
moonCount = 0

randomizer.write("\nMETRO: \n")

local = rand(0, 5)
moonCount += local

generate(426, 506, 0, local)

randomizer.write(moons[426]["name"] + " [3]\n")
moonCount += 3

local = rand(0, 20 - moonCount)
moonCount += local

generate(426, 506, 427, local)

if moonCount < 20:
    randomizer.write(generatestory(427, 430) + "\n")
    moonCount += 1

    local = rand(0, 20 - moonCount)
    moonCount += local

    generate(426, 506, 427, local)

    if moonCount < 20:
        randomizer.write(generatestory(427, 430) + "\n")
        moonCount += 1

        local = rand(0, 20 - moonCount)
        moonCount += local

        generate(426, 506, 427, local)

        if moonCount < 20:
            randomizer.write(generatestory(427, 430) + "\n")
            moonCount += 1

            local = rand(0, 20 - moonCount)
            moonCount += local

            generate(426, 506, 427, local)

            if moonCount < 20:
                randomizer.write(generatestory(427, 430) + "\n")
                moonCount += 1

                local = rand(0, 20 - moonCount)
                moonCount += local

                generate(426, 506, 428, local)

                if moonCount < 20:
                    randomizer.write(moons[431]["name"] + "\n")
                    moonCount += 1

                    local = rand(0, 20 - moonCount)
                    moonCount += local

                    generate(426, 506, 432, local)

                    if moonCount < 18:
                        randomizer.write(moons[432]["name"] + " [3]\n")
                        moonCount += 3

                        generate(426, 506, 433, 20 - moonCount)
                    elif 20 > moonCount >= 18:
                        generate(426, 506, 432, 20 - moonCount)

#

# Snow
moonCount = 0

randomizer.write("\nSNOW: \n")

local = rand(0, 10)
moonCount += local

generate(507, 561, 0, local)

if moonCount < 10:
    randomizer.write(generatestory(507, 510) + "\n")
    moonCount += 1

    local = rand(0, 10 - moonCount)
    moonCount += local

    generate(507, 561, 0, local)

    if moonCount < 10:
        randomizer.write(generatestory(507, 510) + "\n")
        moonCount += 1

        local = rand(0, 10 - moonCount)
        moonCount += local

        generate(507, 561, 0, local)

        if moonCount < 10:
            randomizer.write(generatestory(507, 510) + "\n")
            moonCount += 1

            local = rand(0, 10 - moonCount)
            moonCount += local

            generate(507, 561, 0, local)

            if moonCount < 10:
                randomizer.write(generatestory(507, 510) + "\n")
                moonCount += 1

                local = rand(0, 10 - moonCount)
                moonCount += local

                generate(507, 561, 0, local)

                if moonCount < 8:
                    randomizer.write(moons[511]["name"] + " [3]\n")
                    moonCount += 3

                    generate(507, 561, 512, 10 - moonCount)
                elif 10 > moonCount >= 8:
                    generate(507, 561, 0, 10 - moonCount)
#

# Seaside
moonCount = 0

randomizer.write("\nSEASIDE: \n")

local = rand(0, 10)
moonCount += local

generate(562, 632, 0, local)

if moonCount < 10:
    randomizer.write(generatestory(562, 565) + "\n")
    moonCount += 1

    local = rand(0, 10 - moonCount)
    moonCount += local

    generate(562, 632, 0, local)

    if moonCount < 10:
        randomizer.write(generatestory(562, 565) + "\n")
        moonCount += 1

        local = rand(0, 10 - moonCount)
        moonCount += local

        generate(562, 632, 0, local)

        if moonCount < 10:
            randomizer.write(generatestory(562, 565) + "\n")
            moonCount += 1

            local = rand(0, 10 - moonCount)
            moonCount += local

            generate(562, 632, 0, local)

            if moonCount < 10:
                randomizer.write(generatestory(562, 565) + "\n")
                moonCount += 1

                local = rand(0, 10 - moonCount)
                moonCount += local

                generate(562, 632, 0, local)

                if moonCount < 8:
                    randomizer.write(moons[566]["name"] + " [3]\n")
                    moonCount += 3

                    generate(562, 632, 567, local)
                elif 10 > moonCount >= 8:
                    generate(562, 632, 0, local)

#

# Luncheon
moonCount = 0

randomizer.write("\nLUNCHEON: \n")

local = rand(0, 4)
moonCount += local

generate(633, 700, 0, local)


randomizer.write(moons[633]["name"] + "\n")
moonCount += 1

local = rand(0, 14)
moonCount += local

generate(633, 700, 634, local)

if moonCount < 18:
    randomizer.write(moons[634]["name"] + "\n")
    moonCount += 1

    local = rand(0, 18 - moonCount)
    moonCount += local

    generate(633, 700, 635, local)

    if moonCount < 16:
        randomizer.write(moons[635]["name"] + " [3]\n")
        moonCount += 3

        local = rand(0, 18 - moonCount)
        moonCount += local

        generate(633, 700, 636, local)

        if moonCount < 18:
            randomizer.write(moons[636]["name"] + "\n")
            moonCount += 1

            local = rand(0, 18 - moonCount)
            moonCount += local

            generate(633, 700, 637, local)

            if moonCount < 16:
                randomizer.write(moons[637]["name"] + " [3]\n")
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

randomizer.write(moons[711]["name"] + "\n")
randomizer.write(moons[712]["name"] + "\n")
randomizer.write(moons[713]["name"] + "\n")
randomizer.write(moons[714]["name"] + " [3]\n")

generate(711, 772, 715, 8 - moonCount)
#

randomizer.close()
