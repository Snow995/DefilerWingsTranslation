# coding=utf-8
label lb_location_gremlin_main:
    python:
        if not renpy.music.is_playing():
            renpy.music.play(get_random_files('mus/ambient'))
    $ place = 'gremlins'
    hide bg
    show place as bg
        
    # The cost of the work, the gremlins-servants
    $ servant_cost = data.lair_upgrades['gremlin_servant']['cost']
    # The cost of installing mechanical traps
    $ mechanic_traps_cost = 500
    # The cost of building fortifications
    $ fortification_cost = 1000
    nvl clear
        
    menu:
        'Hire the servants' if 'servant' not in game.lair.upgrades and 'gremlin_servant' not in game.lair.upgrades:
            "Gremlins will serve in the den, watch over and protect their captives. Total for [servant_cost] farthings year"
            menu:
                "Swear to pay" if servant_cost <= game.lair.treasury.wealth:
                    $ game.lair.upgrades.add('gremlin_servant', deepcopy(data.lair_upgrades['gremlin_servant']))
                    "Gremlins are {s}treasure.{/s} take care of the captives awake."
                "Go away":
                    call lb_location_gremlin_main from _call_lb_location_gremlin_main
        'Instal lair traps' if (not game.lair.type.provide or 'mechanic_traps' not in game.lair.type.provide) and 'mechanic_traps' not in game.lair.upgrades:
            menu:
                "The cost of Trap: [mechanic_traps_cost] farthings"
                "Set traps" if mechanic_traps_cost <= game.lair.treasury.money:
                    $ game.lair.upgrades.add('mechanic_traps', deepcopy(data.lair_upgrades['mechanic_traps']))
                    $ game.lair.treasury.money -= mechanic_traps_cost
                    'Now the thief not be good. But after a thief will fall, mechanical traps have to be reinstalled.'
                "Leaving":
                    call lb_location_gremlin_main from _call_lb_location_gremlin_main_1
        'Fortify lair' if 'gremlin_fortification' not in game.lair.upgrades:
            menu:
                "The cost of the construction of fortifications: [fortification_cost] farthings"
                "Strengthen den" if fortification_cost <= game.lair.treasury.money:
                    $ game.lair.upgrades.add('gremlin_fortification', deepcopy(data.lair_upgrades['gremlin_fortification']))
                    $ game.lair.treasury.money -= fortification_cost
                    'Gremlins set in the lair of the dragon grilles and door locks with cunning, strengthen the walls. The thief will not work!'
                "Leaving":
                    call lb_location_gremlin_main from _call_lb_location_gremlin_main_2
        'Make jewelry':
            $ new_item = game.lair.treasury.craft(**data.craft_options['gremlin'])
            if new_item:
                $ game.lair.treasury.receive_treasures([new_item])
                $ test_description = new_item.description()
                "manufactured: [test_description]."
                call lb_location_gremlin_main from _call_lb_location_gremlin_main_3
        'Go away':
            $ pass
        
    return