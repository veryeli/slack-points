import points_util

from collections import Counter
import re
import time
from slackclient import SlackClient


HOUSES = ["Ravenclaw", "Hufflepuff", "Gryffendor", "Slytherin"]
PREFECTS = ["eli", "hillary"]
ANNOUNCERS = ["eli", "hillary"]

nth = {
	1: "first",
	2: "second",
	3: "third",
	4: "fourth"
}

class PointCounter(object):
	def __init__(self, prefects=PREFECTS, announcers=ANNOUNCERS):
		self.points = Counter()
		self.prefects = prefects
		self.announcers = announcers

	def get_points_from(self, message, awarder):
		amount = points_util.detect_points(message)
		# only prefects can award over one point at a time
		if awarder not in self.prefects:
			amount = max(min(amount, 1), -1)
		return amount

	@staticmethod
	def message_for(house, points):
		return "%d point%s to %s" % (points, '' if points in [-1, 1] else 's', house)

	def award_points(self, message, awarder):
		points = self.get_points_from(message, awarder)
		houses = points_util.get_houses_from(message)
		if points and houses:
			for house in houses:
				self.points[house] += points
			return [self.message_for(house, points) for house in houses]

	def print_status(self):
		for place, (house, points) in enumerate(sorted(self.points.items(), key=lambda x: x[-1])):
			print "In %s place, %s with %d points" % (
				nth[len(HOUSES) - place], house, points)



if __name__ == "__main__":

	token = "xoxp-22115174470-22115174518-22111747637-2aa0f76c63"
	sc = SlackClient(token)
	p = PointCounter()
	if sc.rtm_connect():
	    while True:
	        messages = sc.rtm_read()
	        for message in messages:
		        if message["type"] == "message":
		        	print message
		        	for m in p.award_points(message['text'], message['user']):
		        		print m
		        time.sleep(1)
	else:
	    print "Connection Failed, invalid token?"