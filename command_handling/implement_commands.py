from map_etc.position import Vector
from map_etc.make_map import game_map
from map_etc.iterate_around import positions_around
from map_etc.find_path import FindPath
from map_etc.search_for_open_position import bfs_for_open_spot
from units.unit_and_villager import Villager
from units.all_classes import unit_kind_to_class
from command_handling.strings import NOW, LATER, BUILD_BUILDING, BUILD_UNIT
from command_handling.strings import COLLECT_RESOURCE, MOVE, RESEARCH, FARM

def implement_commands_if_possible(player):
    implement_build_building_command(player)
    implement_collect_resource_command(player)
    implement_move_commands(player)
    implement_build_unit_commands(player)
    implement_research_commands(player)
    implement_farm_commands(player)
    # Eventually, this will probably be replaced with the following code, where functions
    # is a list of all the functions which need to be run.
    # for function in functions:
    #     function(player)


def implement_build_building_command(player):
    for villager in player.commands[NOW][BUILD_BUILDING]:
        building, building_position = player.commands[NOW][BUILD_BUILDING][villager]
        delta = building_position - villager.position
        if delta == Vector(0, 0):
            pass
        else:
            villager.move_by(delta, game_map)
        building.build_by(villager)


def implement_collect_resource_command(player):
    for villager in player.commands[NOW][COLLECT_RESOURCE]:
        resource = player.commands[NOW][COLLECT_RESOURCE][villager]
        if villager.can_collect_resource_now(resource, player):
            villager.collect_resource(resource, player)


def implement_move_commands(player):
    for unit in player.commands[NOW][MOVE]:
        delta = player.commands[NOW][MOVE][unit]
        # end_goal is either None or the position unit is eventually trying
        # to get to
        end_goal = None
        if unit in player.commands[LATER][MOVE]:
            delta_2 = player.commands[LATER][MOVE][unit]
            end_goal = unit.position + delta + delta_2
        if isinstance(unit, Villager):
            move_unit_if_possible(player, unit, delta, end_goal)
        else:
            start = unit.position
            goal = unit.position + delta
            path = FindPath(start, goal, player)
            # The argument threshold in the following is somewhat arbitrary. It
            # does make sense to at least make it no more than 15, since that is
            # the maximum amount most (or all?) units can move in one turn.
            if path.end_is_within(threshold=13):
                delta = path.end - unit.position
                move_unit_if_possible(player, unit, delta, end_goal)
            else:
                # This is a backup, in case the if section failed to run
                delta = bfs_for_open_spot(unit, game_map)
                if delta is not None:
                    # If the next line runs, it should successfully move unit
                    move_unit_if_possible(player, unit, delta, end_goal)
                else:
                    # This is the backup to the backup
                    for position in positions_around(unit.position, radius=100):
                        delta = unit.position - position
                        if move_unit_if_possible(player, unit, delta, end_goal):
                            break


def move_unit_if_possible(player, unit, delta, end_goal):
    """Return True iff unit was successfully moved."""
    if unit.can_move(delta, game_map):
        unit.move_by(delta, game_map)
        if end_goal is not None:
            new_delta = end_goal - unit.position
            player.commands[LATER][MOVE][unit] = new_delta
        return True
    return False

def update_move_later_cmd_if_necessary(unit, end_goal_position):
    pass


def implement_build_unit_commands(player):
    for building in player.commands[NOW][BUILD_UNIT]:
        unit_type, num_to_build = player.commands[NOW][BUILD_UNIT][building]
        for i in range(num_to_build):
            if player.population < player.population_cap:
                if unit_type not in unit_kind_to_class:
                    continue
                building.build_unit(unit_type)
            else:
                print('Population cap reached. You cannot build more units.')
                return


def implement_research_commands(player):
    for building in player.commands[NOW][RESEARCH]:
        thing_to_research = player.commands[NOW][RESEARCH][building]
        building.research(thing_to_research)


def implement_farm_commands(player):
    for villager in player.commands[NOW][FARM]:
        the_farm = player.commands[NOW][FARM][villager]
        villager.farm(the_farm, player)
