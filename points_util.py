import re

def clean(message):
	"""Standardize spacing and capitalization"""
	return ' '.join(m.lower() for m in message.split() if m)

def detect_points(message):
	amounts = re.findall(r'\d+', clean(message))
	if len(amounts) == 1:
		return int(amounts[0]) * detect_point_polarity(message)
	else:
		return 0

def detect_point_polarity(message):
	"""Discern whether this is a point awarding or deduction"""
	message = clean(message)
	if "points to" or "points for" in message:
		return 1
	elif "points from" in message:
		return -1
	else:
		return 0

def proper_name_for(house):
	"""Forgive house misspelling"""
	if "raven" in house:
		return "Ravenclaw"
	if "huffle" in house:
		return "Hufflepuff"
	if "gryf" in house:
		return "Gryffendor"
	if "slyt" in house:
		return "Slytherin"

def get_houses_from(message):
	return [proper_name_for(w) for w in clean(message).split() if proper_name_for(w)]