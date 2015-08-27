# coding=utf-8
label lb_event_thief_spawn(thief):
    show expression "img/scene/thief.jpg" as bg
    nvl clear
    "[thief.title] known as [game.thief.name] going to get some trinkets from great dragon treasury!"
    nvl clear
    thief "Treasures will be mine!"
    return

label lb_event_thief_steal_items(thief, items):
    $ descriptions = "\n".join(game.lair.treasury.treasures_description(items))
    show expression "img/scene/loot.jpg" as bg
    nvl clear
    "[game.thief.name] steals: [descriptions]"
    thief "That's it! Barely anything left. But now I can live in luxury as a king until the end my days!"
    nvl clear
    return

label lb_event_thief_lair_unreachable(thief):
    nvl clear    
    thief "Damn [game.dragon.kind] He could not choose a den in a more accessible location? How to get there somehow? That same Galoot .."
    return

label lb_event_thief_prepare(thief):
    # nvl clear    
    # thief "If I want to leave the dragon den alive and rich, I'd better get ready for the Cause."
    return

label lb_event_thief_prepare_usefull(thief):
    nvl clear    
    thief "Heh-heh ... right on schedule!."
    return

label lb_event_thief_receive_item(thief, item):
    show expression "img/scene/quest_thief.jpg" as bg
    nvl clear
    "[game.thief.name] systematically preparing for the great cause. His new acquisition: [item.name]"
    thief "This is useful to me!"
    nvl clear
    return

label lb_event_thief_prepare_useless(thief):
    nvl clear
    show expression "img/scene/quest_thief.jpg" as bg
    '[game.thief.name] He trys to find the dragon's lair, but to no avail.'
    thief "But where is this hidden entrance ... Damn!"
    return

label lb_event_thief_lair_enter(thief):
    nvl clear
    show expression "img/scene/thief_in_lair.jpg" as bg
    thief "Well, that's it - the dragon's lair. I'll go like a shadow and sneak back with a bag of treasure as grave as my sins..."
    return

label lb_event_thief_die_inaccessability(thief):
    "[thief.title] [game.thief.name] I could not even get into the lair - its strength is overly robust."
    thief 'Damn [game.dragon.kind] holed up better than the King of the dwarfs - walls, ditches, shutters, grilles and locks ... I do not see a single loophole. Looks like the things tougher than i thought.'
    return

label lb_event_thief_die_trap(thief, trap):
    nvl clear    
    show expression "img/scene/thief_in_lair.jpg" as bg    
    $ txt = game.interpolate(random.choice(data.lair_upgrades[trap].fail))
    '[txt]' 
    return

label lb_event_thief_pass_trap(thief, trap):
    if config.debug:
        'pass_trap [trap]'
    show expression "img/scene/thief_in_lair.jpg" as bg    
    $ txt = game.interpolate(random.choice(data.lair_upgrades[trap].success))
    '[txt]' 
    return

label lb_event_thief_receive_no_item(thief):
    nvl clear    
    show expression "img/scene/thief_in_lair.jpg" as bg    
    "The thief got nothing"
    return
    
# @Review: Alex: Added a bunch of new events to fill in the gaps:
label lb_event_thief_checking_accessability(thief):
    # Checking if thief can get past layer defences:
    # Debug message: thief(u"checkin accessability")
    return
    
label lb_event_thief_checking_accessability_success(thief):
    # Thief can gain access:
    # Debug message: thief(u"I can get into the Layer!")
    return
    
label lb_event_thief_trying_to_avoid_traps_and_guards(thief):
    # Thief is trying to avoid traps and guards:
    # Debug message: thief(u"Trying to get around the traps and guards")
    return
    
label lb_event_thief_retreat_and_try_next_year(thief):
    # Could not get passed traps and guards but did not die either:
    # Debug message: thief(u"No luck, ill try the following year")
    thief "So thats as far as i go... It is necessary to prepare krutovato better. But I do not give up!"
    return
    
label lb_event_thief_starting_to_rob_the_lair(thief):
    # Got past all traps and guards, thief is starting to rob the lair:
    # Debug message: thief(u"I begin to clean up the den")
    show expression "img/scene/loot.jpg" as bg    
    thief "Wow! Here it is a treasure trove. AND [game.dragon.kind], infection directly on gold is ... nothing, I neatly ... you just have to choose the things potsennee."
    return

label lb_event_thief_took_an_item(thief, item):
    # Got an item!
    # Debug message: thief(u"Взял шмотку %s" % stolen_items[i])
    # show expression "img/scene/loot.jpg" as bg    
    # "[game.thief.name] gently pull out from under the belly of the sleeping dragon's favorite item:"
    # "[item]"
    return
    
label lb_event_thief_lair_empty(thief):
    # There were no treasures in the lair:
    # Debug message: thief(u"The treasury has nothing to take. dump.")
    show expression "img/scene/thief_in_lair.jpg" as bg        
    thief "There is nothing else to profit ... damn, I thought dragons were richer. It is necessary to pass the buck!"
    return
    
label lb_event_thief_awakened_dragon(thief, stolen_items):
    # Thief awakens the dragon and gets killed... stolen_items: items that dragon takes back from the thief.
    # Debug message: thief(u"I woke the dragon")
    show expression "img/scene/wokeup.jpg" as bg    
    "thief unleashes a pile of coins, which are rolled with a clatter on the floor."
    thief "Oops ..."
    game.dragon "Well, well ... what a meeting. And I thought someone here sheburshitsya."
    nvl clear
    "[game.dragon.fullname] rips unlucky Cryptstalker into pieces and having had a bite, once again goes to bed."
    return