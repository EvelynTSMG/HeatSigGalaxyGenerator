import math
import random
from os import listdir
from os.path import isfile, join
from random_util import *
from generator_util import *
import generator_util
import datetime


def generate_stations(desired_stations, character_names, station_names, greek_letters) -> list[Station]:
	stations = []
	stations.append(generator_util._COLDROCKHAVEN)

	last_x = 0
	last_y = 0
	last_theta = 0

	for i in range(0, desired_stations):
		tries = 0
		start_time = datetime.datetime.now()
		delta  = 0
		while True:
			r = math.sqrt(random.randint(10000,20000))
			while True:
				theta = random.random() * 2 * math.pi
				if theta <= last_theta - 0.3 or theta >= last_theta + 0.3:
					break
			x = r * math.cos(theta) + last_x
			y = r * math.sin(theta) + last_y
			if check_station_density(stations, x, y):
				break
			tries += 1
			if tries > 25:
				last_x = 0
				last_y = 0
			end_time = datetime.datetime.now()
			if (end_time - start_time).total_seconds() > 10: # If it takes too long
				# Frick this, just restart generation
				return generate_stations(desired_stations, character_names, station_names, greek_letters)

	
		while True:
			character = random.choice(character_names)
			noun_idx = random.randint(0, len(station_names) - 1)
			noun = station_names[noun_idx]
			greek = random.randint(0, 9) == 1
			name = character + ' ' + noun
			if greek:
				name += ' ' + random.choice(greek_letters)
			if check_station_name(stations, name):
				break
	
		stations.append(Station(name=name, x=x, y=y, economy=2, founder=character, noun=noun, noun_idx=noun_idx, is_greek=greek))
	
		last_x = x
		last_y = y

	return stations


def add_station_connections(stations):
	"""Adds connections to all stations within a certain distance from each other"""
	for s1 in stations:
		for s2 in stations:
			if can_connect(s1, s2, 150):
				s1.connections.append(s2.name)
				s2.connections.append(s1.name)


def add_station_defectors(stations, defectors: list[Defector]):
	"""Adds defectors to all stations if available"""
	new_defectors = defectors.copy() # Immutable
	for s in stations:
		if s != generator_util._COLDROCKHAVEN:
			s.challenge = new_defectors.pop(0)


def add_station_factions(generation, stations, wanted_factions, independent_coldrock, min_independent, max_independent):
	match generation:
		case 'standard':
			enemy_factions = wanted_factions.copy()
			enemy_factions.remove(4)
			stations_per_faction = len(stations) / len(enemy_factions)
			stations_left = stations_per_faction

			for s in stations:
				if s.name == 'Coldrock Haven' and independent_coldrock:
					continue
				if len(enemy_factions) > 0:
					if enemy_factions[0] != 4:
						s.faction_idx = enemy_factions[0]
						s.orig_faction_idx = enemy_factions[0]
						stations_left -= 1
						if stations_left <= 0:
							stations_left = stations_per_faction
							enemy_factions.pop(0)
			if 4 in wanted_factions:
				for i in range(1, random.randint(min_independent, max_independent + 1)):
					stations[i].faction_idx = 4
		case 'scattered':
			enemy_factions = wanted_factions.copy()
			enemy_factions.remove(4)
			stations_per_faction = len(stations) / len(enemy_factions)
			stations_left = stations_per_faction

			new_stations = safe_shuffle(stations)

			for s in new_stations:
				if s.name != 'Coldrock Haven' and len(enemy_factions) > 0:
					if enemy_factions[0] != 4:
						s.faction_idx = enemy_factions[0]
						s.orig_faction_idx = enemy_factions[0]
						stations_left -= 1
						if stations_left <= 0:
							stations_left = stations_per_faction
							enemy_factions.pop(0)
			if 4 in wanted_factions:
				for i in range(1, random.randint(min_independent, max_independent + 1)):
					stations[i].faction_idx = 4
			for s1 in stations:
				for s2 in new_stations:
					if s1.name == s2.name:
						s1.faction_idx = s2.faction_idx
						s1.orig_faction_idx = s2.orig_faction_idx


def add_station_tech(stations, possible_tech):
    pass


def make_strongholds(stations, wanted_factions):
	strongholds_left = wanted_factions.copy()
	strongholds_left.remove(4) # Independent doesn't have a stronghold
	while len(strongholds_left) > 0:
		s = get_outermost_station(stations, strongholds_left[0])
		s.is_stronghold = True
		print('Making stronghold from faction:', s.faction_idx, 'originally', s.orig_faction_idx)
		strongholds_left.pop(0)


def write_header(file, header):
	"""Writes a HeatSig style {header} to {file}"""
	file.write('\n<{}>\n'.format(header))


def write_key(file, key, value):
	"""Writes a HeatSig style {key} and {value} combination to {file}"""
	file.write('{} = {}\n'.format(key, value))


def generate(gui, game_dir: str, save_dir: str, generation_type: str, balanced_tech: bool, nice_colours: bool, desired_stations: int,
			wanted_factions: tuple[int, int, int, int], independent_coldrock: bool, min_independent: int, max_independent: int):
	galaxy_colors = open(join(game_dir, 'Galaxy Colours.txt'), 'r').readlines()
	galaxy_colors = [x[:-1] for x in galaxy_colors if x != 'Next\n']
	color_count = len(galaxy_colors) / 2
	special_defectors = [d.split('.')[0] for d in listdir(join(game_dir, './Scenarios/SpecialChallenges/')) if isfile(join(game_dir, './Scenarios/SpecialChallenges/', d)) and d.split('.')[1] == 'dat' and d.split('.')[0] != 'DAN']
	regular_defectors = [d.split('.')[0] for d in listdir(join(game_dir, './Scenarios/Challenges/')) if isfile(join(game_dir, './Scenarios/Challenges/', d)) and d.split('.')[1] == 'dat']
	defectors = special_defectors + regular_defectors
	character_names = open(join(game_dir, 'Surnames.txt'), 'r').readlines()
	character_names = [x[:-1] for x in character_names] # Removes the new line character
	station_names = ['Outpost', 'Station', 'Bastion', 'Hub', 'Nexus', 'Port', 'Colony', 'City']
	greek_letters = ['Alpha', 'Beta', 'Chi', 'Delta', 'Epsilon', 'Eta', 'Gamma', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Omega', 'Omicron',' Phi', 'Pi', 'Psi', 'Rho', 'Sigma', 'Tau', 'Theta', 'Upsilon', 'Xi', 'Zeta']
	min_coord = -10000
	max_coord = 10000
	progress_steps = 5

	gui.update_progress(int(100 / (progress_steps / 1)), 'Initialized')

	stations = generate_stations(desired_stations, character_names, station_names, greek_letters)

	print('Added stations')
	add_station_connections(stations)
	print('Added connections')
	add_station_factions(generation_type, stations, wanted_factions, independent_coldrock, min_independent, max_independent)
	print('Added factions')
	# Tech goes here
	add_station_defectors(stations, defectors)
	print('Added defectors')
	make_strongholds(stations, wanted_factions)
	print('Made strongholds')


	print('Generating galaxy complete')

	with open(save_dir, 'w') as f:
		color_idx = random.randint(0, color_count)
		
		write_key(f, 'VersionNumber', '20170822')
		write_key(f, 'LiberationProgress', '0')
		write_key(f, 'LiberationsAvailable', '0')
		write_key(f, 'SecondsSinceLastLiberation', '0')
		write_key(f, 'SecondsSinceLastShopRestock', '0')
		write_key(f, 'Over', '0')
		write_key(f, 'ColourA', galaxy_colors[color_idx - 1][11:])
		write_key(f, 'ColourB', galaxy_colors[color_idx][11:])
		write_header(f, 'Galaxy')
		write_key(f, 'BackgroundVapourCloud', 'sBlob' + str(random.randint(1, 8)) + '')
		write_key(f, 'BackgroundColor', ' 17,255, 39') # I dunno what range this is
		for s in stations:
			write_header(f, 'Station')
			write_key(f, 'Name', s.name)
			write_key(f, 'x', str(int(s.x) * 10000))
			write_key(f, 'y', str(int(s.y) * 10000))
			write_key(f, 'FactionIndex', str(s.faction_idx))
			write_key(f, 'OriginalFactionIndex', str(s.orig_faction_idx))
			write_key(f, 'TraitToUnlock', s.trait)
			write_key(f, 'ObjectToUnlock', s.item)
			write_key(f, 'EconomyBoost', str(s.economy))
			write_key(f, 'Founder', s.founder)
			write_key(f, 'Noun', s.noun)
			write_key(f, 'StationNameIndex', str(s.noun_idx))
			write_key(f, 'IsGreek', str(int(s.is_greek)))
			write_key(f, 'Stronghold', str(int(s.is_stronghold)))
			write_key(f, 'ChallengeFilename', s.challenge)
			write_key(f, 'ChallengeCompleted', '0')
			write_key(f, 'Client', s.client)
			for c in s.connections:
				write_key(f, 'Connection', c)

		for i in range(0, random.randint(7, 17)):
			write_header(f, 'Blob')
			write_key(f, 'x', str(random.randint(min_coord, max_coord) * 1000))
			write_key(f, 'y', str(random.randint(min_coord, max_coord) * 1000))
			write_key(f, 'sprite_index', str(random.randint(1, 8)))
			write_key(f, 'image_blend', '  2,235,202') # I dunno what range this is
			write_key(f, 'InitialImageAngle', str(random.randrange(0, 360)))
			write_key(f, 'Size', '4800000')