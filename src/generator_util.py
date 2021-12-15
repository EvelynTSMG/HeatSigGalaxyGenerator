from dataclasses import dataclass, field
from random_util import get_distance_from, get_avg_coords

@dataclass
class Defector:
    path: str = ''

@dataclass
class Station:
	name: str = 'Created Station'
	x: int = 0
	y: int = 0
	faction_idx: int = 0
	orig_faction_idx: int = 1
	trait: str = ''
	item: str = 'oNoone'
	economy: int = 0
	founder: str = ''
	noun: str = ''
	noun_idx: int = 0
	is_greek: bool = False
	is_stronghold: bool = False
	challenge: str = ''
	client: str = ''
	connections: list = field(default_factory=list)


_COLDROCKHAVEN = Station('Coldrock Haven', 0, 0, 4, 1, '', 'oNoone', 0, 'Sader Fiasco', 'Haven', 0, False, False, 'Scenarios\\SpecialChallenges\\DAN.dat')


def can_connect(s1, s2, max_dist):
    """Returns if two stations can conenct to each other"""
    return s2.name not in s1.connections and s1.name not in s2.connections and len(s1.connections) < 4 and len(s2.connections) < 4 and s1.name != s2.name and get_distance_from(s1.x, s1.y, s2.x, s2.y) < max_dist


def check_station_density(stations, x, y):
	"""Checks whether a generated set of coordinates is too close to an already generated station. Returns True if generated coordinates are okay"""
	for s in stations:
		if get_distance_from(s.x, s.y, x, y) < 75:
			return False
	return True


def check_station_name(stations, name):
	"""Checks whether a generated name hasn't been used before. Returns True if generated name is okay"""
	for s in stations:
		if s.name == name:
			return False
	return True


def get_outermost_station(stations, faction: int, relative_to: str = 'Average'):
	"""Returns the outermost station for the given faction"""
	match relative_to:
		case 'Coldrock Haven', _:
			center = [0, 0]
		case 'Average':
			coords = []
			for s in stations:
				coords.append([s.x, s.y])
			center = get_avg_coords(coords)
	max_dist = 0
	max_station = Station()
	for s in stations:
		dist = get_distance_from(center[0], center[1], s.x, s.y)
		if s.faction_idx == faction and dist > max_dist:
			max_dist = dist
			max_station = s
	return max_station