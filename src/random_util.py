from math import sqrt
import random

def get_distance_from(x1, y1, x2, y2):
	"""Returns the distance between points (x1, y1) and (x2, y2)"""
	return sqrt((x2 - x1)**2 + (y2 - y1)**2)


def get_avg_coords(coords):
	"""Returns the average coordinates of all coords in a list"""
	count_x = 0
	count_y = 0
	for c in coords:
		count_x += c[0]
		count_y += c[1]
	count_x /= len(coords)
	count_y /= len(coords)
	return [count_x, count_y]


def safe_shuffle(to_shuffle):
	new_list = to_shuffle.copy()
	random.shuffle(new_list)
	return new_list