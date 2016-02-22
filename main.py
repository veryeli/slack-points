import points_util
import cup_image
from consts import HOUSES, SLACK_TOKEN, PREFECTS, ANNOUNCERS, CHANNEL, POINTS_FILE

from collections import Counter
import os
import re
import pickle
from slackclient import SlackClient
import time

nth = {
    1: "first",
    2: "second",
    3: "third",
    4: "fourth"
}

class PointCounter(object):
    def __init__(self, prefects=PREFECTS, announcers=ANNOUNCERS):
        try:
            self.points = pickle.load(open(POINTS_FILE, 'rb'))
        except:
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
        return "%s gets %d point%s" % (house, points, '' if points in [-1, 1] else 's')

    def award_points(self, message, awarder):
        points = self.get_points_from(message, awarder)
        houses = points_util.get_houses_from(message)
        if points and houses:
            for house in houses:
                self.points[house] += points
                pickle.dump(self.points, open(POINTS_FILE, 'wb'))
                print self.points
                yield self.message_for(house, points)

    def print_status(self):
        for place, (house, points) in enumerate(sorted(self.points.items(), key=lambda x: x[-1])):
            yield "In %s place, %s with %d points" % (
                nth[len(HOUSES) - place], house, points)


def is_hogwarts_related(message):
    return (
        message["type"] == "message" and
        message["channel"] == CHANNEL and
        "text" in message and
        "user" in message and
        "point" in message["text"] and
        points_util.get_houses_from(message["text"]))

def main():
    sc = SlackClient(SLACK_TOKEN)
    p = PointCounter()
    if sc.rtm_connect():
        while True:
            messages = sc.rtm_read()
            for message in messages:
                if 'text' in message:
                    print points_util.get_houses_from(message["text"])
                if is_hogwarts_related(message):
                    print 'is_hogwarts_related'
                    for m in p.award_points(message['text'], message['user']):
                        sc.api_call(
                            "chat.postMessage", channel=CHANNEL, text=m)
                    os.system(
                        "curl -F file=@%s -F title=%s -F channels=%s -F token=%s https://slack.com/api/files.upload"
                         % (cup_image.image_for_scores(p.points), '"House Points"', CHANNEL, SLACK_TOKEN))


                time.sleep(1)
    else:
        print "Connection Failed, invalid token?"


if __name__ == "__main__":
    main()
