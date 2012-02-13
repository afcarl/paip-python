def tree_search(states, goal_reached, get_successors, combine_states):
    print states
    if not states:
        return None
    if goal_reached(states[0]):
        return states[0]
    successors = get_successors(states[0])
    next = combine_states(successors, states[1:])
    return tree_search(next, goal_reached, get_successors, combine_states)


def dfs(start, goal_reached, get_successors):
    def combine(new_states, existing_states):
        return new_states + existing_states
    return tree_search([start], goal_reached, get_successors, combine)


def bfs(start, goal_reached, get_successors):
    def combine(new_states, existing_states):
        return existing_states + new_states
    return tree_search([start], goal_reached, get_successors, combine)


def best_first_search(start, goal_reached, get_successors, cost):
    def combine(new_states, existing_states):
        return sorted(new_states + existing_states, key=cost)
    return tree_search([start], goal_reached, get_successors, combine)


def beam_search(start, goal_reached, get_successors, cost, beam_width):
    def combine(new_states, existing_states):
        return sorted(new_states + existing_states, key=cost)[:beam_width]
    return tree_search([start], goal_reached, get_successors, combine)
        

def widening_search(start, goal_reached, get_successors, cost, width=1, max=100):
    print 'Width: %d' % width
    if width > max:
        return
    res = beam_search(start, goal_reached, get_successors, cost, width)
    if res:
        return res
    else:
        return widening_search(start, goal_reached, get_successors, cost, width + 1)
        
    
# =============================================================================

import math

class City(object):
    def __init__(self, name, lat, long):
        self.name = name
        self.lat = lat
        self.long = long


CITIES = {city.name: city for city in [
    City('Atlanta', 84.23, 33.45),
    City('Boston', 71.05, 42.21),
    City('Chicago', 87.37, 41.50),
    City('Denver', 105.00, 39.45),
    City('Eugene', 123.05, 44.03),
    City('Flagstaff', 111.41, 35.13),
    City('Grand Junction', 108.37, 39.05),
    City('Houston', 105.00, 34.00),
    City('Indianapolis', 86.10, 39.46),
    City('Jacksonville', 81.40, 30.22),
    City('Kansas City', 94.35, 39.06),
    City('Los Angeles', 118.15, 34.03),
    City('Memphis', 90.03, 35.09),
    City('New York', 73.58, 40.47),
    City('Oklahoma City', 97.28, 35.26),
    City('Pittsburgh', 79.57, 40.27),
    City('Quebec', 71.11, 46.49),
    City('Reno', 119.49, 39.30),
    City('San Francisco', 122.26, 37.47),
    City('Tampa', 82.27, 27.57),
    City('Victoria', 123.21, 48.25),
    City('Wilmington', 77.57, 34.14)
]}

def dist(city1, city2):
    return math.sqrt(abs(city1.lat - city2.lat) ** 2 + abs(city1.long - city2.long) ** 2)

def neighbors(city):
    return [c for c in CITIES.values() if dist(c, city) < 10 and c is not city]

class Segment(object):
    def __init__(self, state, prev=None, running_cost=0, est_remaining=0):
        self.state = state
        self.prev = prev
        self.cost = running_cost
        self.est_remaining = est_remaining

def trip(start, dest, beam_width=1):
    return beam_search(Segment(start),
                       lambda seg: seg.state is dest,
                       path_saver(neighbors, dist, lambda c: dist(c, dest)),
                       lambda seg: seg.est_remaining,
                       beam_width)

def path_saver(get_successors, cost, remaining_cost):
    def build_path(prev_seg):
        prev_state = prev_seg.state
        next_states = get_successors(prev_state)
        next_segs = []
        for next_state in next_states:
            updated_cost = prev_seg.cost + cost(prev_state, next_state)
            est_remaining = updated_cost + remaining_cost(next_state)
            next_segs.append(Segment(next_state, prev_seg,
                                     updated_cost, est_remaining))
        return next_segs
    return build_path

def collect_path(seg):
    path = [seg.state]
    if seg.prev:
        path += collect_path(seg.prev)
    return path

def print_path(seg):
    print 'Total distance: %s' % seg.prev.cost
    print [city.name for city in collect_path(seg)]
        