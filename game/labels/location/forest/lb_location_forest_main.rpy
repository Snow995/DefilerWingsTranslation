# coding=utf-8
init python:
    from pythoncode.utils import weighted_random
    from pythoncode.characters import Enemy
        
label lb_location_forest_main:
    python:
        if not renpy.music.is_playing():
            renpy.music.play(get_random_files('mus/ambient'))    
    $ place = 'forest'
    hide bg
    show expression get_place_bg(place) as bg
    nvl clear
    
    if game.dragon.energy() == 0:
        '[game.dragon.name] need some sleep!'
        return
        
    $ nochance = game.poverty.value * 3
    $ choices = [
        ("lb_enc_lumberjack", 10),
        ("lb_enc_onegirl", 10),
        ("lb_enc_wandergirl", 10),
        ("lb_enc_ogre", 10),
        ("lb_enc_deer", 10),
        ("lb_enc_boar", 10),
        ("lb_enc_berries", 10),
        ("lb_enc_shrooms", 10),
        ("lb_enc_guardian", 10),
        ("lb_enc_lumbermill", 10),
        ("lb_enc_klad", 5),
        ("lb_enc_domiki", 3),
        ("lb_patrool_forest", 3 * game.mobilization.level),
        ("lb_enc_noting", nochance)]
    $ enc = weighted_random(choices)
    $ renpy.call(enc)
    
    return
    
label lb_enc_domiki:
    if "domiki_done" in persistent.easter_eggs:
        jump lb_location_forest_main
    $ persistent.easter_eggs.append("domiki_done")
    "SUDDENLY! From the forest thickets on the dragon nabigaet ..."
    show expression 'img/scene/fight/domik.jpg' as bg    
    'Wooden cottage? !!!! Apparently this is a legendary creature of ancient mad wandering Archmage Cyril "Korovanusa" - a wooden golem battle. He is clearly aggressive ...'
    $ game.foe = Enemy('domik', game_ref=game)    
    $ chances = show_chances(game.foe)   
    call lb_fight from _call_lb_fight_69    
    'Among the wreckage of the house is a sign: "Made by the order of the wicked one (the name I have not yet invented)." What a crazy and brilliant creation ...'
    return

label lb_enc_lumberjack:
    'Nearby are audible rhythmic beats, echoing raznosyaschiesya throughout the forest. It looks like a lumberjacks ax. By itself, the wood-cutter production completely uninteresting, but the time is now right for lunch, and in the human food traditions of working from home brings the eldest of the unmarried daughters. It is necessary to sneak up and have a look ...'
    nvl clear
    python:
        if game.dragon.size < 3: 
            succes = True
        else:
            succes = False
    if succes: 
        '[game.dragon.name] He falls to the ground and slowly, trying not to make noise sneaks toward the noise. Fortunately woodcutter too busy with their interesting and creative work, to note that in the neighboring bushes added a giant lizard. Now we can only wait ...'
        nvl clear
        menu:
            'Watch secretly':
                $ game.dragon.drain_energy()
                $ description = game.girls_list.new_girl('peasant')
                'Within an hour, the path appears as another figure, female. She has in her hands a heavy basket covered with a white rag. [game.dragon.name] NPPOs draws air and determines with accuracy - girl! Although nizkorodnaya ...'
                game.girl 'Papaaa! I brought you something to eat. I've got a sweet bread in the basket.'
                nvl clear
                'She runs to her father to hug him, but he freezes in horror looking behind her daughter where a full-length rises [game.dragon.name]. Not giving people time to recover, [game.dragon.name] kills lumberjack and knocks down his daughter.'
                $ game.dragon.reputation.points += 1
                '[game.dragon.reputation.gain_description]'
                nvl clear
                game.girl.third "[description]"
                call lb_nature_sex from _call_lb_nature_sex_21      
                return        
            'Go away' if game.dragon.bloodiness < 5:
                $ game.dragon.gain_rage()
    else: 
        'Crouch and slowly, trying not to make noise sneaks toward the noise. But it is too large for such Fok course woodcutter heard panting and crackling of broken saplings and ax throwing terrified runs away. What a shame ...' 
        $ if game.dragon.bloodiness < 5: game.dragon.gain_rage()
            
    return
    
    
label lb_enc_onegirl:
    'If you hide from the forest path, then sooner or later it will be held by anyone. Here, for example, this time on the path shows a young peasant woman with a basket. Apparently bears whitewash working in the forest father or brother.'
    nvl clear
    menu:
        'Get the girl':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            '[game.dragon.name] prolamyvayas falls on the road through the bushes. Peasant Woman horrified and throws the picture freezes in terror. It looks like it is not going to run, even though ... it would be pointless.'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_22      
        'Let her run' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return

label lb_enc_wandergirl:
    'From the forest thicket hear cries of "Ay!", The voice of women, young. Apparently she strayed from the group and got lost in the woods.She hopes that her someone would hear. Well, here it heard the dragon. I wonder if she will from this easier?'
    nvl clear
    menu:
        'Call in human woice':
            $ game.dragon.drain_energy()
            $ description = game.girls_list.new_girl('peasant')
            'Dragons are very insidious and talented. One of the many great skills is their ability to forge a vote. It is necessary to respond to the call by a human girl, and now she herself runs to you in the legs!'
            $ game.dragon.reputation.points += 1
            '[game.dragon.reputation.gain_description]'
            nvl clear
            game.girl.third "[description]"
            call lb_nature_sex from _call_lb_nature_sex_23      
        'Go away' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return

label lb_enc_deer:
    'In the woods the deer fattened grazing seasoned. Not a bad appetizer, but nothing special. Descend if the stomach rumbles.'
    nvl clear
    menu:
        'Hunt down the deer' if game.dragon.hunger > 0:
            $ game.dragon.drain_energy()
            '[game.dragon.name] catches and eats deer.'
            python:
                if game.dragon.bloodiness > 0:
                    game.dragon.bloodiness = 0
                    game.dragon.hunger -= 1
        'Rip the deer in pieces' if game.dragon.bloodiness >= 5 and game.dragon.hunger == 0:
            $ game.dragon.drain_energy()
            '[game.dragon.name] brutally bullies deer just for fun.'    
        'Roar' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    return

label lb_enc_boar:
    'The wind brings the smell of large animals. In the undergrowth rustled a giant boar. More than a meter at the shoulder, thick-skinned and a massive beast armed with huge curved fangs. He's not afraid of anyone in the forest - not an easy prey, but it will gain strength before more serious battles.'
    $ game.foe = Enemy('boar', game_ref=game)
    $ chances = show_chances(game.foe)
    nvl clear
    menu:
        'Fight the boar':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_53
            if game.dragon.hunger > 0:
                '[game.dragon.name] eats fallen wild Boar. The strength of the inmate in the old boar meat will give a dragon killer power.'
                python:
                    if game.dragon.bloodiness > 0:
                        game.dragon.bloodiness = 0
                    game.dragon.hunger -= 1
                    game.dragon.add_effect('boar_meat')
            else:
                'Dragon triumphs.'
        'retreat' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_guardian:
    $ txt = game.interpolate(random.choice(txt_enc_forest_guardian[0]))
    '[txt]'
    show expression 'img/scene/fight/elf_ranger.jpg' as bg
    $ txt = game.interpolate(random.choice(txt_enc_forest_guardian[1]))
    $ game.foe = Enemy('elf_ranger', game_ref=game)
    '[txt]'
    $ chances = show_chances(game.foe)
    nvl clear
    menu:
        'Attack':
            $ game.dragon.drain_energy()
            call lb_fight from _call_lb_fight_54
            python:
                txt = game.interpolate(random.choice(txt_enc_forest_guardian[2]))
                if game.dragon.magic > 0:
                    txt = game.interpolate(random.choice(txt_enc_forest_guardian[3]))
                    game.dragon.add_special_place('enchanted_forest', 'enter_ef')
            '[txt]'
        'Flee' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
            return            
    return

label lb_enc_lumbermill:
    show expression 'img/bg/special/lumbermill.jpg' as bg
    'On the banks of the River Forest is a wooden building encompasses some huge mechanism, driven by a water wheel. Chances are people here process wood.'
    nvl clear
    python:
        doit = False
        if 'fire_breath' in game.dragon.modifiers(): 
            doit = True
    menu:
        'Breath fire' if doit:
            $ game.dragon.drain_energy()
            "[game.dragon.name] It spews a stream on the building of devouring flame. Dry tree immediately engaged and soon sawmill burns. Now people will have less building materials for their homes and castles."
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Conjure blue flames' if game.dragon.mana > 0:
            $ game.dragon.drain_energy()
            $ game.dragon.drain_mana()
            "[game.dragon.name] calling a spell magic fire. Dry tree immediately engaged and soon sawmill burns. Now people will have less building materials for their homes and castles."
            $ game.poverty.value += 1
            $ game.dragon.reputation.points += 3
            '[game.dragon.reputation.gain_description]'
        'Investigate' if game.dragon.size <= 3 and game.dragon.magic == 0:
            $ game.dragon.drain_energy()
            "[game.dragon.name] carefully examines the unusual structure for the importance and vulnerability. Rotating flow of water wheel drives a blade hidden inside the building, with the help of which people are made of logs boards. A huge stack of finished products complex nearby. If only it was what it's all set fire to ..."
            'Only time lost in vain. We'll have to leave empty-handed.'
        'Ignore' if game.dragon.bloodiness < 5:
            $ game.dragon.gain_rage()
    
    return
    
label lb_enc_klad:
    'Dragon could smell buried treasure.'
    nvl clear
    python:
        tr_lvl = random.randint(1, 100)
        count = random.randint(1, 10)
        alignment = 'human'
        min_cost = 1 * tr_lvl
        max_cost = 10 * tr_lvl
        obtained = "This is the subject of a treasure buried by someone in the woods."
        trs = treasures.gen_treas(count, data.loot['klad'], alignment, min_cost, max_cost, obtained)
        trs_list = game.lair.treasury.treasures_description(trs)
        trs_descrptn = '\n'.join(trs_list)
    menu:
        'Find the buried treasures':
            $ game.dragon.drain_energy()
            'Under the roots of an old oak buried slug Getting already ancient chest. Inside lies:'
            '[trs_descrptn]'
            $ game.lair.treasury.receive_treasures(trs)
            
        'Let it be' if game.dragon.bloodiness < 5:
            'Certainly useful treasures, but what then could bury pathetic little people hardly worth the precious time of the noble dragon.'
    return

label lb_patrool_forest:
    python:
        chance = random.randint(0, game.mobilization.level)
        if chance < 4:
            patrool = 'jagger'
            dtxt = 'Forest ranger patrols the royal - a ranger armed with a long yew bow and a sharp knife.'
        elif chance < 7:
            patrool = 'footman'
            dtxt = 'Forest road marching detachment of soldiers. It seems they patrol the area in search of the robbers and monsters. Well, one thing they found ...'
        elif chance < 11:
            patrool = 'heavy_infantry'
            dtxt = 'Forest roads are patrolled by troops of heavy infantry. If people are so much care about the safety of forests that have decided to send in the elite fighters, so they are really scared.'
        elif chance < 16:
            patrool = 'griffin_rider'
            dtxt = 'The shrill cry is heard from heaven - a rider on a gryphon swoops down from the height of the sight of the trees shine dragonscale.'
        else:
            patrool = 'angel'
            dtxt = '%s is forced to close his eyes from the bright light glaring. Hail loudly proclaims: "Die vile offspring of sin !!!". This guardian angel sent by Heaven to protect the people.' % game.dragon.name
    '[dtxt]'
    python:
        game.foe = Enemy(patrool, game_ref=game)
        battle_status = battle.check_fear(game.dragon, game.foe)
    if 'foe_fear' in battle_status:
        $ narrator(game.foe.battle_description(battle_status, game.dragon))
        return
    $ game.dragon.drain_energy()
    call lb_fight(skip_fear=True) from _call_lb_fight_55
    return
