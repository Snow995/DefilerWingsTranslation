# coding=utf-8
label lb_event_knight_spawn(knight):
    scene
    show expression "img/scene/oath.jpg" as bg
    nvl clear
    "[knight.title] pleges a sacrament vow to kill a dragon!"
    knight "Prepare evil fiend, I'm coming for you!"
    return

label lb_event_knight_receive_item(knight, item):
    scene
    show expression "img/scene/quest_knight.jpg" as bg
    nvl clear
    "Knight Quest performs and receives [item.name]"
    knight "Now the dragon can not get away from my vengeance!"
    return

label lb_event_knight_challenge_start(knight):
    scene
    show expression "img/scene/quest_knight.jpg" as bg
    nvl clear
    $ game.foe = knight
    "[knight.title] I found a lair where sleeps [game.dragon.name] [game.dragon.surname] and causes it to fight."
    knight "Come sneaky [game.dragon.kind] on a fair fight on pobranochku!!!"
    $ narrator(knight.intro % game.format_data)
    $ narrator(show_chances(knight))  #TODO: the level of danger of battle
    menu:
        "Protect your lair":
            "You are entering into battle"
            return True
        "Flee and abandon your lair":
            # Here, the wrong should be to check on the success of the escape from the dragon knight, but it is not. (No unnecessary. Escape always successful, a dragon's lair lose, gold and women - OH)
            if random.choice(range(4)) in range(3): # 75% that Knight will
                knight "I still find you!"
                return False
            else:
                knight "You cowards [game.dragon.kind], this enemy is not worthy of me"
                return False

label lb_event_knight_challenge_end(knight, result):
    if result in ["defeat", "retreat"]:
        "The dragon was defeated valiant knight."
    if result in ["win"]:
        "Dragon Knight ripped to shreds."