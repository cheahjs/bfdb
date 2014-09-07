#!/usr/bin/python

import glob
import json
import sys
from util import *
from leaderskill import parse_leader_skill
from braveburst import parse_bb


def parse_unit(unit, skills, bbs, leader_skills, dictionary):
    data = dict()

    data['name'] = dictionary.get(unit[UNIT_NAME], unit[UNIT_NAME])
    data['element'] = elements[unit[UNIT_ELEMENT]]
    data['rarity'] = int(unit[UNIT_RARITY])
    data['base hp'] = int(unit[UNIT_BASE_HP])
    data['lord hp'] = int(unit[UNIT_LORD_HP])
    data['base atk'] = int(unit[UNIT_BASE_ATK])
    data['lord atk'] = int(unit[UNIT_LORD_ATK])
    data['base def'] = int(unit[UNIT_BASE_DEF])
    data['lord def'] = int(unit[UNIT_LORD_DEF])
    data['base rec'] = int(unit[UNIT_BASE_REC])
    data['lord rec'] = int(unit[UNIT_LORD_REC])
    data['hits'] = len(unit[DMG_FRAME].split(','))
    data['hit dmg% distribution'] = [
        int(hit.split(':')[1]) for hit in unit[DMG_FRAME].split(',')
    ]
    data['max bc generated'] = data['hits'] * int(unit[DROP_CHECK_CNT])
    data['lord damage range'] = '~'.join(
        map(str, damage_range(data['lord atk'])))

    if UNIT_IMP in unit:
        data[UNIT_IMP] = parse_imps(unit[UNIT_IMP].split(':'))

    if unit[BB_ID] != '0':
        data['bb'] = parse_bb(data, unit[BB_ID], skills, bbs, dictionary)

    if unit[SBB_ID] != '0':
        data['sbb'] = parse_bb(data, unit[SBB_ID], skills, bbs, dictionary)

    if unit[LS_ID] != '0':
        data['leader skill'] = parse_leader_skill(
            data, leader_skills[unit[LS_ID]], dictionary)

    return data

if __name__ == '__main__':
    _dir = 'data/decoded_dat/'
    if len(sys.argv) > 1:
        _dir = sys.argv[1]

    with open(glob.glob(_dir+'Ver*_2r9cNSdt*')[-1]) as f:
        with open(glob.glob('data/dictionary_raw.txt')[-1]) as f2:
            with open(glob.glob(_dir+'Ver*_zLIvD5o2*')[-1]) as f3:
                with open(glob.glob(_dir+'Ver*_wkCyV73D*')[-1]) as f4:
                    with open(glob.glob(_dir+'Ver*_4dE8UKcw*')[-1]) as f5:
                        units = json.load(f)
                        skills_js = json.load(f4)
                        bbs_js = json.load(f3)
                        leader_skills_js = json.load(f5)
                        dictionary = dict([
                            line.split('^')[:2] for line in f2.readlines()
                        ])

                        skills = dict()
                        for skill in skills_js:
                            skills[skill[BB_ID]] = skill

                        bbs = dict()
                        for bb in bbs_js:
                            bbs[bb[BB_ID]] = bb

                        leader_skills = dict()
                        for leader_skill in leader_skills_js:
                            leader_skills[leader_skill[LS_ID]] = leader_skill

                        units_data = {}
                        for unit in units:
                            unit_data = parse_unit(
                                unit, skills, bbs, leader_skills, dictionary)
                            units_data[unit_data['name']] = unit_data
                            unit_data.pop('name')

                        print json.dumps(units_data)
