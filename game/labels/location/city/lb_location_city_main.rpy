# coding=utf-8
init python:
    from pythoncode import treasures
    from pythoncode.characters import Enemy
        
label lb_location_city_main:
    python:
        if not renpy.music.is_playing():
            renpy.music.play(get_random_files('mus/ambient'))        
    $ place = "city_gates"
    hide bg
    show place as bg
    nvl clear
    
    if game.dragon.energy() == 0:
        'Even dragons have to sleep sometime. Particularly this dragon!'
        return      
        
    'Capital of the kingdoms people.'
    menu:
        'Disguise as a human' if game.dragon.mana > 0:
            'Dragon transformed into a human and goes to the city. It had to spend precious magic power ...'
            $ game.dragon.drain_mana()
            nvl clear
            call lb_city_walk from _call_lb_city_walk
        'Storm the gates' if not game.dragon.can_fly:
            'Noticing the approach of danger alerts the guards and they close the gate. Will have to break with in force ...'
            call lb_city_gates from _call_lb_city_gates
        'Fly in' if game.dragon.can_fly:
            'Easy peremahnuv through the city wall, [game.dragon.kind] It is in the heart of the city. From strengthening volatile enemy will not save ...'
            call lb_city_raze from _call_lb_city_raze
        'Get away':
            return
            
    return

label lb_city_gates:
    $ game.dragon.drain_energy()
    $ game.foe = Enemy('city', game_ref=game)
    call lb_fight from _call_lb_fight_68
    call lb_city_raze from _call_lb_city_raze_1
    return

label lb_city_raze:
    'Defenseless city is ready to learn the rage offspring Lady.'
    nvl clear
    menu:
        'Royal palace':
            call lb_city_palace_atk from _call_lb_city_palace_atk

        'Marketplace':
            call lb_city_market_atk from _call_lb_city_market_atk

        'Cathedral':
            call lb_city_cathedral_atk from _call_lb_city_cathedral_atk
            
        'Rich district':
            call lb_city_jew_atk from _call_lb_city_jew_atk
            
        'Get away':
            return
            
    return

label lb_city_walk:
    show expression 'img/bg/city/inside.jpg' as bg
    'A mysterious stranger walks past the watchful guards and enters the bustling city life.'
    nvl clear

    menu:
        'Royal palace':
            call lb_city_palace from _call_lb_city_palace

        'Marketplace':
            call lb_city_market from _call_lb_city_market

        'Cathedral':
            call lb_city_cathedral from _call_lb_city_cathedral
            
        'Jewelers shop':
            call lb_city_jewler from _call_lb_city_jewler
            
        'Get away':
            return
            
    return

label lb_city_palace:
    'The proud citadel on a hill in the city center. Here is the winter residence of the king. Inside the seductive aromas waft precious and noble maidens. At the gate are vigilant guards.'
    $ game.foe = Enemy('palace_guards', game_ref=game)
    $ chances = show_chances(game.foe)
    nvl clear
    menu:
        'Attack':
            call lb_city_palace_atk from _call_lb_city_palace_atk_1
        'Get away':
            call lb_city_walk from _call_lb_city_walk_1
    
    return

label lb_city_palace_atk:
    $ game.dragon.drain_energy()
    $ game.foe = Enemy('palace_guards', game_ref=game)
    $ chances = show_chances(game.foe)
    call lb_fight from _call_lb_fight
    'While the rest of the defenders of the citadel are in disarray, the dragon appeared otilinchy chance for looting and robbery.'
    $ game.dragon.reputation.points += 3
    '[game.dragon.reputation.gain_description]'
    menu:
        'Defile noble lady':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('princess')
            '[game.dragon.fullname] catches Noble Maidens'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex     
        'plunder @ murder':
            $ game.dragon.drain_energy()
            python:
                count = random.randint(4, 9)
                alignment = 'knight'
                min_cost = 200
                max_cost = 2000
                obtained = "This is the subject of the royal treasury."
                trs = treasures.gen_treas(count, data.loot['palace'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
            'With a bloodthirsty roar [game.dragon.fullname] sweeping through the corridors of the palace killing all in its path, and assigning each item it ponravivshusya:'
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
        'Flee':
            'Having decided not to tempt fate and use commotion for hazardous waste, [game.dragon.kind] walks away from the city.'
    return

label lb_city_market:
    show expression 'img/bg/city/market.jpg' as bg
    'The market square is full of people. People buy and sell all sorts of unnecessary things like potatoes and clothing. Foolish mortals do not even know that right here is their most terrifying nightmare. They are vulnerable to surprise attack.'
    nvl clear
    menu:
        'Drop the disguise':
            call lb_city_market_atk from _call_lb_city_market_atk_1
        'Get away':
            call lb_city_walk from _call_lb_city_walk_2

    return

label lb_city_market_atk:
    show expression 'img/bg/city/market.jpg' as bg
    'Dragon regains true form. People flee in terror.'
    nvl clear
    menu:
        'Massacre':
            $ game.dragon.drain_energy()
            play sound "sound/eat.ogg"
            show expression 'img/scene/fire.jpg' as bg
            'In vain the inhabitants thought that the walls of the capital they bezopsnosti. [game.dragon.fullname] off in full, so people certainly did not forget. Blood, guts, raspidorasilo ...'
            $ game.dragon.reputation.points += 10
            '[game.dragon.reputation.gain_description]'
        'Defile merchant daughter':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('citizen')
            '[game.dragon.fullname] catches maiden prettier but richer. Noble will give the market certainly is not found, but the daughter of the rich here can sometimes appear.'
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_1     
        'Get away':
            return
    return

label lb_city_cathedral:
    'The huge Gothic cathedral, towering over the city. All around there is no building that could match the heights of the cathedral bell tower with a spire.'
    nvl clear
    menu:
        'Pillage the Cathedral':
            'A mysterious stranger comes under the arches of the temple and in front of the congregation is transformed into a monster.'
            call lb_city_cathedral_atk from _call_lb_city_cathedral_atk_1

        'Get away':
            call lb_city_walk from _call_lb_city_walk_4
    return

label lb_city_cathedral_atk:
    $ game.dragon.drain_energy()
    python:
        count = random.randint(4, 10)
        alignment = 'cleric'
        min_cost = 10
        max_cost = 500
        obtained = "This is the subject of the capital cathedral."
        trs = treasures.gen_treas(count, data.loot['church'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    'With demonic laughter [game.dragon.fullname] burst into the sanctuary, killing all in its path, and assigning each item it ponravivshusya:'
    '[trs_descrptn]'
    $ game.lair.treasury.receive_treasures(trs)
    $ game.dragon.reputation.points += 5
    '[game.dragon.reputation.gain_description]'    
    return

label lb_city_jewler:
    'In this work the most affluent quarter iskustno artisans - armorers, jewelers and cabinetmakers. All around is intoxicating smell of treasures and noble women left for shopping. Unfortunately, too many guards there - standing on every corner.'
    $ game.foe = Enemy('city_guard', game_ref=game)
    $ chances = show_chances(game.foe)
    nvl clear
    menu:
        'Buy jewels':
            $ new_item = game.lair.treasury.craft(**data.craft_options['jeweler_buy'])
            if new_item:
                $ game.lair.treasury.receive_treasures([new_item])
                $ test_description = new_item.description()
                "bought: [test_description]."
            call lb_city_jewler from _call_lb_city_jewler_1
        'Sell jewels':
            menu:
                'Most expensive' if len(game.lair.treasury.jewelry) > 0:
                    $ item_index = game.lair.treasury.most_expensive_jewelry_index
                'Cheapest' if len(game.lair.treasury.jewelry) > 0:
                    $ item_index = game.lair.treasury.cheapest_jewelry_index
                'Random' if len(game.lair.treasury.jewelry) > 0:
                    $ item_index = random.randint(0, len(game.lair.treasury.jewelry) - 1)
                'All of them' if len(game.lair.treasury.jewelry) > 0:
                    $ item_index = None
                'Cancel':
                    call lb_city_jewler from _call_lb_city_jewler_2
            python:
                if (item_index is None):
                    description = u"Sell decorations for all %s?" % (
                        treasures.number_conjugation_rus(game.lair.treasury.all_jewelries, u"фартинг"))
                else:
                    description = u"%s.\nПродать украшение за %s?" % (
                        game.lair.treasury.jewelry[item_index].description().capitalize(),
                        treasures.number_conjugation_rus(game.lair.treasury.jewelry[item_index].cost, u"фартинг"))
            menu:
                "[description]"
                'Sell':
                    python:
                        if (item_index is None):
                            description = u"All jewelry sold for %s?" % (
                                treasures.number_conjugation_rus(game.lair.treasury.all_jewelries, u"фартинг"))
                            game.lair.treasury.money += game.lair.treasury.all_jewelries
                            game.lair.treasury.jewelry = []
                        else:
                            description = u"%s.\nПродано за %s" % (
                                game.lair.treasury.jewelry[item_index].description().capitalize(),
                                treasures.number_conjugation_rus(game.lair.treasury.jewelry[item_index].cost, u"фартинг"))
                            game.lair.treasury.money += game.lair.treasury.jewelry[item_index].cost
                            game.lair.treasury.jewelry.pop(item_index)

                    call lb_city_jewler from _call_lb_city_jewler_3
                'Do not sell':
                    call lb_city_jewler from _call_lb_city_jewler_4
        'Make jewel':
            $ new_item = game.lair.treasury.craft(**data.craft_options['jeweler_craft'])
            if new_item:
                $ game.lair.treasury.receive_treasures([new_item])
                $ test_description = new_item.description()
                "manufactured: [test_description]."
            call lb_city_jewler from _call_lb_city_jewler_5
        'Drop the disguise':
            call lb_city_jew_atk from _call_lb_city_jew_atk_1
        'Go to main street':
            call lb_city_walk from _call_lb_city_walk_5
    return


label lb_city_jew_atk:
    $ game.dragon.drain_energy()
    $ game.foe = Enemy('city_guard', game_ref=game)
    call lb_fight from _call_lb_fight_1
    'In the neighborhood there was not a living guard. All around a panic, people run away from the dragon to save the most valuable. [game.dragon.name] He looks at the scene of destruction and chaos. Thick jeweler, dragging heavy wooden jewelry box. Blagnorodnaya girl runs away with a squeal. In the basement of a burning house that is about to collapse lie unattended precious stones and bars.'
    $ game.dragon.reputation.points += 3
    '[game.dragon.reputation.gain_description]'
    menu:
        'Rob the jeweler':
            python:
                count = random.randint(3, 10)
                alignment = 'human'
                min_cost = 10
                max_cost = 500
                obtained = "This is the subject of a jeweler shop."
                trs = treasures.gen_treas(count, data.loot['jeweler'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
            'Robbing a clumsy jeweler is like taking candy from a baby. In the jewelry box are many interesting things:'
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]' 
    
        'Rape the noble virgin':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('princess')
            'Dragon catches Noble Maidens'
            $ game.dragon.reputation.points += 5
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_2     
            return
            
        'Get jewels from burning shop':
            python:
                count = random.randint(3, 10)
                alignment = 'human'
                min_cost = 10
                max_cost = 1000
                obtained = "This is the subject of a jeweler shop."
                trs = treasures.gen_treas(count, data.loot['raw_material'], alignment, min_cost, max_cost, obtained)
                trs_list = game.lair.treasury.treasures_description(trs)
                trs_descrptn = '\n'.join(trs_list)
            'We must act quickly, before the burning house collapses, burying all their valuebles under ruble:'
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]' 
    
    return
    