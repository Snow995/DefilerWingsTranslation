# coding=utf-8
# interactions location

label lb_nature_sex:
    if game.girl.jailed:
        $ place = 'prison'
        show place as bg
    nvl clear
    menu:
        'Defile and impregnate' if game.girls_list.is_mating_possible:
            # Alex: Added sex images:
            $ description = game.girls_list.impregnate()
            stop music fadeout 1.0            
            game.girl "[description]"
            show expression sex_imgs(game.girl.sex_expression) as xxx
            play sound get_random_file("sound/sex")
            pause (500.0)
            stop sound fadeout 1.0
            hide xxx
        'Mock and rob' if game.girl.treasure:
            $ description = game.girls_list.rob_girl()
            game.girl.third "[description]"
        'Drop in the jail' if game.girl.jailed:
            $ description = game.girls_list.jail_girl()
            game.girl.third "[description]"
            return
        'Flitch to the lair' if not game.girl.jailed:
            $ description = game.girls_list.steal_girl()
            game.girl.third "[description]"
            $ place = game.lair.type_name
            show place
            nvl clear
            $ description = game.girls_list.jail_girl()
            game.girl.third "[description]"
            return
        'Let her go':
            $ description = game.girls_list.free_girl()
            game.girl.third "[description]"
            return
        'Vore lustfully' if game.dragon.hunger > 0:
            $ description =  game.girls_list.eat_girl()
            game.girl "[description]"
            play sound "sound/eat.ogg"
            show expression sex_imgs.get_eat_image() as eat_image
            pause (500.0)
            hide eat_image     
            return
    jump lb_nature_sex


label lb_lair_sex:
    game.girl "Я хочу домой. Ну пожалуйста..."
    python:
        if game.girl.type == 'ice' or game.girl.type == 'fire' or game.girl.type == 'ogre' or game.girl.type == 'titan' or game.girl.type == 'siren':
            renpy.jump('lb_gigant_sex')
    jump lb_nature_sex

label lb_gigant_sex:
    nvl clear
    menu:
        'Defile and impregnate' if game.girls_list.is_mating_possible:
            $ description = game.girls_list.impregnate()
            stop music fadeout 1.0   
            game.girl "[description]"
            show expression sex_imgs("girl") as xxx
            play sound get_random_file("sound/sex")
            pause (500.0)
            stop sound fadeout 1.0            
            hide xxx
        'Magical growth' if not game.girls_list.is_mating_possible and game.girl.virgin and game.dragon.mana > 0 and game.dragon.lust > 0:
            $ game.dragon.drain_mana()
            game.dragon 'Заклятье временного роста!'
            $ description = game.girls_list.impregnate()
            game.girl "[description]"
            show expression sex_imgs("girl") as xxx
            play sound 'sound//sex/01.ogg'
            pause (500.0)
            stop sound fadeout 1.0
            hide xxx
        'Mock and rob' if game.girl.treasure:
            $ description = game.girls_list.rob_girl()
            game.girl.third "[description]"
        'Flitch to the lair' if not game.girl.jailed:
            $ description = game.girls_list.steal_girl()
            game.girl.third "[description]"
            $ place = game.lair.type_name
            show place
            nvl clear
            $ description = game.girls_list.jail_girl()
            game.girl.third "[description]"
            return          
        'Drop in the jail' if game.girl.jailed:
            $ description = game.girls_list.jail_girl()
            game.girl.third "[description]"
            return            
        'Let her go':
            $ description = game.girls_list.free_girl()
            game.girl.third "[description]"
            return
        'Vore lustfully' if game.dragon.hunger > 0:
            $ description = game.girls_list.eat_girl()
            game.girl.third "[description]"
            show expression sex_imgs.get_eat_image() as eat_image
            play sound "sound/eat.ogg"
            pause (500.0)
            hide eat_image                 
            return
    jump lb_gigant_sex


label lb_knight_new:
    show expression 'img/bg/special/oath.jpg' as bg
    'Рыцарь дал клятву убить дракона.'
    return

label lb_water_sex:
    jump lb_nature_sex
    return
    