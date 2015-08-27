﻿# coding=utf-8

import random
import data
import renpy.exports as renpy
import renpy.store as store
import girls_data
from treasures import gen_treas
from utils import call
from characters import Girl
from data import achieve_target

class GirlsList(object):
    def __init__(self, game_ref, base_character):
        self.game = game_ref
        self.character = base_character
        self.prisoners = []  # jailed girls list
        self.free_list = []  # free girls list
        self.spawn = []  # list of spawns, that will come after sleep
        self.active = 0  # cureent girl number
        self.offspring = []  # offspings type for quest

    def new_girl(self, girl_type='peasant'):
        """
        Generate new girl with specified type.
        """
        self.game.girl = Girl(game_ref=self.game, girl_type=girl_type)
        self.game.girl.treasure = self.gen_tres()
        return self.description('new')

    def gen_tres(self):
        """
        List of personam treasures for current girl
        """
        g_type = self.game.girl.type  # simplified access to girl's type
        girl_info = girls_data.girls_info[g_type]  # simplified access to information for girl's type
        count = random.randint(girl_info['t_count_min'], girl_info['t_count_max'])
        t_list = girl_info['t_list']
        alignment = girl_info['t_alignment']
        min_cost = girl_info['t_price_min']
        max_cost = girl_info['t_price_max']
        obtained = u"Принадлежало красавице по имени %s" % self.game.girl.name
        return gen_treas(count, t_list, alignment, min_cost, max_cost, obtained)

    def impregnate(self):
        """
        Girl impregnation.
        """
        # self.description('prelude', True)
        # self.description('sex', True)
        # self.description('impregnate', True)
        self.game.girl.virgin = False
        if self.game.girl.quality < self.game.dragon.magic or \
                'impregnator' in self.game.dragon.modifiers():
            self.game.girl.pregnant = 2
        else:
            self.game.girl.pregnant = 1
        self.game.dragon.lust -= 1
        achieve_target(self.game.girl.type, "impregnate")
        return self.description('shout')

    def free_girl(self):
        """
        Free current girl.
        """
        # girl is tracked only if pregnant
        if self.game.girl.pregnant:
            self.free_list.append(self.game.girl)
        if self.game.girl.jailed:
            return self.description('free_prison')
        else:
            return self.description('free')

    def free_all_girls(self):
        """
        Frees all girls.
        """
        for girl_i in reversed(xrange(self.prisoners_count)):
            self.game.girl = self.prisoners[girl_i]
            if self.game.girl.pregnant:
                self.free_list.append(self.game.girl)
        self.prisoners = []

    def steal_girl(self):
        return self.description('steal')

    def jail_girl(self):
        """
        Jail current girl.
        """
        if self.game.girl.jailed:
            text = self.description('jailed')
            self.prisoners.insert(self.active, self.game.girl)
        else:
            text = self.description('jail')
            self.game.girl.jailed = True
            self.prisoners.append(self.game.girl)
        return text

    def set_active(self, index):
        """
        Get girl with number <index> for prison
        """
        self.game.girl = self.prisoners[index]
        self.active = index
        del self.prisoners[index]

    def eat_girl(self):
        """
        Eat girl.
        """
        self.game.dragon.hunger -= 1
        if self.game.dragon.lust < 3:
            self.game.dragon.lust += 1
        self.game.dragon.bloodiness = 0
        return self.description('eat')

    def rob_girl(self):
        """
        Rob girl.
        """
        self.game.lair.treasury.receive_treasures(self.game.girl.treasure)
        return self.description('rob')

    def prisoners_list(self):
        """
        Return list of jailed girls.
        """
        jail_list = []
        for girl_i in xrange(len(self.prisoners)):
            jail_list.append(self.prisoners[girl_i].name)
        return jail_list

    @property
    def prisoners_count(self):
        """
        Return amount of jailed girls.
        """
        return len(self.prisoners)

    def description(self, status, say=False):
        """
        Generate situation description for current girl (self.game.girl).
        status - code description of situation
        say - if true - description outputs to screen right away
        Returns description text or None, if there is no text in a list
        """
        format_dict = {
            'dragon_name': self.game.dragon.name,
            'dragon_name_full': self.game.dragon.fullname,
            'dragon_type': self.game.dragon.kind,
            'girl_name': self.game.girl.name,
            'girl_title': girls_data.girls_info[self.game.girl.type]['description'],
        }
        girl_type = self.game.girl.type
        if girl_type not in girls_data.girls_texts or status not in girls_data.girls_texts[girl_type]:
            girl_type = 'girl'
        if status in girls_data.girls_texts[girl_type]:
            text = random.choice(girls_data.girls_texts[girl_type][status])
            if self.spawn:
                # If list of spawns is not empty - get last spawn name for possible substitution
                format_dict['spawn_name'] = girls_data.spawn_info[self.spawn[-1]]['born'].capitalize()
            if status == 'rob':
                treas_description = self.game.lair.treasury.treasures_description(self.game.girl.treasure)
                treas_description = '\n'.join(treas_description) + u'.'
                self.game.girl.treasure = []
                format_dict['rob_list'] = treas_description
            text = text % format_dict
        else:
            text = None
        if say and text:
            self.game.girl.third(text)  # message give away
            store.nvl_list = []  # nvl clear for python
        else:
            return text

    @staticmethod
    def event(event_type, *args, **kwargs):
        if event_type in girls_data.girl_events:
            if girls_data.girl_events[event_type] is not None:
                call(girls_data.girl_events[event_type], *args, **kwargs)
        else:
            raise Exception("Unknown event: %s" % event_type)
        return

    def next_year(self):
        """
        All actions with girrls in a year.
        """
        # jailed girls
        for girl_i in reversed(xrange(self.prisoners_count)):
            self.game.girl = self.prisoners[girl_i]
            # Attempt to escape
            if (random.randint(1, 2) == 1) and self.game.lair.reachable([]) and \
                    'regular_guards' not in self.game.lair.upgrades and \
                    'elite_guards' not in self.game.lair.upgrades and \
                    'smuggler_guards' not in self.game.lair.upgrades:
                # Girls escaped chamber
                del self.prisoners[girl_i]
                self.event('escape')  # even "Escape from prison"
                if self.game.girl.pregnant:
                    self.free_list.append(self.game.girl)
            else:
                # girl didn't escape
                if ('servant' in self.game.lair.upgrades) or ('gremlin_servant' in self.game.lair.upgrades):
                    if self.game.girl.pregnant:
                        girl_type = girls_data.girls_info[self.game.girl.type]

                        if self.game.girl.pregnant == 1:
                            spawn_class = 'regular_spawn'
                        else:
                            spawn_class = 'advanced_spawn'
                        if 'educated_spawn' not in self.offspring:
                            self.offspring.append('educated_spawn')
                        if girl_type['giantess']:
                            girl_size = 'giantess'
                        else:
                            girl_size = 'common_size'
                        if girl_size not in self.offspring:
                            self.offspring.append(girl_size)

                        self.spawn.append(girl_type[spawn_class])
                        self.event('spawn', girl_type[spawn_class])  # event "spawns birth"
                        self.game.girl.pregnant = 0
                else:
                    self.event('hunger_death')  # event "girl died from starvation"
                    del self.prisoners[girl_i]
        # Free and just escaped girls. Only preganat girls are tracked
        for girl_i in xrange(len(self.free_list)):
            self.game.girl = self.free_list[girl_i]
            if (random.randint(1, 3) == 1) and not girls_data.girls_info[self.game.girl.type]['giantess']:
                self.event('kill')  # event "pregnant girl is killed in the wild"
            else:
                girl_type = girls_data.girls_info[self.game.girl.type]

                if self.game.girl.pregnant == 1:
                    spawn_class = 'regular_spawn'
                else:
                    spawn_class = 'advanced_spawn'
                if 'free_spawn' not in self.offspring:
                    self.offspring.append('free_spawn')
                if girl_type['giantess']:
                    girl_size = 'giantess'
                else:
                    girl_size = 'common_size'
                if girl_size not in self.offspring:
                    self.offspring.append(girl_size)

                spawn_type = girls_data.girls_info[self.game.girl.type][spawn_class]
                spawn = girls_data.spawn_info[spawn_type]
                self.event('free_spawn', spawn_type)  # event "spawns birth in the wild"
                self.free_spawn(spawn['power'])
        self.free_list = []  # list clear - gave birth or killed - no reason to track anymore

    def before_sleep(self):
        """
        All actions beore sleep - death from yearning, something else?
        """
        for girl_i in reversed(xrange(self.prisoners_count)):
            self.game.girl = self.prisoners[girl_i]
            if (not self.game.girl.virgin) and (not self.game.girl.pregnant):
                self.description('anguish', True)  # умирает c тоски
                del self.prisoners[girl_i]

    # noinspection PyTypeChecker
    def after_awakening(self):
        """
        All actions after awakening - sort out spawns.
        """
        for spawn_i in xrange(len(self.spawn)):
            spawn_type = self.spawn[spawn_i]  # simplified access to spawns's type
            spawn = girls_data.spawn_info[spawn_type]  # simplified access to spawns's data
            renpy.show("meow", what=store.Image("img/scene/spawn/%s.jpg" % spawn_type))
            spawn_mod = spawn['modifier']  # simplified access to spawns's modifiers list
            # Make check. True if not sea spawn or sea spawn in underwater lair
            # TODO: Возможно стоит сделать умирание слуги, если оно не морское и в морском логове.
            marine_check = ('marine' not in spawn_mod) or \
                           (self.game.lair.type.require and 'swimming' in self.game.lair.type.require)
            spawn_menu = [(u"К Вам приходит %s и просит назначения" % spawn['name'], None)]  # меню отродий
            # Possible menu points
            if ('poisonous' in spawn_mod) and ('poison_guards' not in self.game.lair.upgrades) and marine_check:
                spawn_menu.append((u"Выпустить в логово", u'poison_guards'))
            if ('servant' in spawn_mod) and ('servant' not in self.game.lair.upgrades) and marine_check:
                spawn_menu.append((u"Сделать слугой", 'servant'))
            if ('warrior' in spawn_mod) and ('regular_guards' not in self.game.lair.upgrades) and marine_check:
                spawn_menu.append((u"Сделать охранником", 'regular_guards'))
            if ('elite' in spawn_mod) and ('elite_guards' not in self.game.lair.upgrades) and marine_check:
                spawn_menu.append((u"Сделать элитным охранником", 'elite_guards'))
            spawn_menu.append((u"Выпустить в королевство", 'free'))
            if (('servant' in spawn_mod) or
                    ('warrior' in spawn_mod) or
                    ('elite' in spawn_mod)) and \
                    ('marine' not in spawn_mod):
                spawn_menu.append((u"Отправить в армию тьмы", 'army_of_darkness'))

            menu_action = renpy.display_menu(spawn_menu)

            if menu_action == 'free':
                renpy.say(self.game.narrator, u"%s отправляется бесчинствовать в королевстве." % spawn['name'])
                self.free_spawn(spawn['power'])
            elif menu_action == 'army_of_darkness':
                renpy.say(self.game.narrator, u"%s отправляется в армию тьмы." % spawn['name'])
                self.army_of_darkness(spawn_type)
            else:
                # Message about work start
                renpy.say(self.game.narrator, u"%s приступает к выполнению обязанностей." % spawn['name'])
                # Message about work end
                if 'replaces' in data.lair_upgrades[menu_action].keys():
                    replace = data.lair_upgrades[menu_action]['replaces']
                    renpy.say(self.game.narrator,
                              u"%s больше не требуются и уходят." % data.lair_upgrades[replace]['name'])
                # add lair improvement
                self.game.lair.add_upgrade(menu_action)
                
        renpy.hide("meow")
        self.spawn = []

    def free_spawn(self, power):
        """
        Spawns actions in the wild
        """
        # Increase poverty. Should work once by spawn type.
        self.game.poverty.value += 1
        pass

    def army_of_darkness(self, warrior_type):
        """
        Send to army of darkness
        """
        self.game.army.add_warrior(warrior_type)

    @property
    def is_mating_possible(self):
        """
        Return coition possibility - True or False.
        # TODO: проверка на превращение в человека
        """
        assert self.game.girl, "Girl not found"
        mating_possible = self.game.girl.virgin and self.game.dragon.lust > 0
        if girls_data.girls_info[self.game.girl.type]['giantess']:
            mating_possible = self.game.dragon.size > 3 and mating_possible
        return mating_possible