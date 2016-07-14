import points_util
import cup_image
from consts import HOUSES, SLACK_TOKEN, PREFECTS, ANNOUNCERS, CHANNEL, POINTS_FILE, MODE, CARD_VALUES, BOT_USER

from collections import Counter
import os
import pickle
import random
from slackclient import SlackClient
import time

nth = {
    1: "first",
    2: "second",
    3: "third",
    4: "fourth"
}

class PointCounter(object):
    def __init__(self, client, prefects=PREFECTS,
                 announcers=ANNOUNCERS, points_file=POINTS_FILE):
        try:
            self.points = pickle.load(open(points_file, 'rb'))
            if "Gryffendor" in self.points:
                self.points["Gryffindor"] = self.points["Gryffendor"]
                del self.points["Gryffendor"]
        except:
            self.points = Counter()
        self.sc = client
        self.prefects = prefects
        self.announcers = announcers
        self.points_file = points_file

    def get_points_from(self, message, awarder):
        amount = points_util.detect_points(message)
        # only prefects can award over one point at a time
        if awarder not in self.prefects:
            amount = max(min(amount, 1), -1)
        return amount

    @staticmethod
    def message_for(house, points):
        if points > 0:
            return "%s gets %s" % (
                house, points_util.pluralized_points(points))
        return "%s loses %s" % (
            house, points_util.pluralized_points(abs(points)))

    def award_points(self, message, awarder):
        points = self.get_points_from(message, awarder)
        houses = points_util.get_houses_from(message)
        messages = []
        if points and houses:
            for house in houses:
                self.points[house] += points
                pickle.dump(self.points, open(self.points_file, 'wb'))
                messages.append(self.message_for(house, points))
        return messages

    def print_status(self):
        for place, (house, points) in enumerate(sorted(self.points.items(), key=lambda x: x[-1])):
            yield "In %s place, %s with %d points" % (
                nth[len(HOUSES) - place], house, points)

    @staticmethod
    def is_related(message):
        return (
            message.get("type", '') == "message" and
            message.get("channel", '') == CHANNEL and
            "text" in message and
            "user" in message and
            "point" in message["text"] and
            points_util.get_houses_from(message["text"]))

    def process_message(self, message):
        print 'is_hogwarts_related'
        for m in self.award_points(message['text'], message['user']):
            self.sc.api_call(
                "chat.postMessage", channel=CHANNEL, text=m)
        os.system(
            "curl -F file=@%s -F title=%s -F channels=%s -F token=%s https://slack.com/api/files.upload"
             % (cup_image.image_for_scores(self.points), '"House Points"', CHANNEL, SLACK_TOKEN))

    def print_points(self):
        m = str(self.points)
        self.sc.api_call(
            "chat.postMessage", channel=CHANNEL, text=m)


class AlicePointCounter(PointCounter):
    @staticmethod
    def is_related(message):
        return (
            message.get("type", '') == "message" and
            message.get("channel", '') == CHANNEL and
            "text" in message and
            "user" in message and
            (
            any(s in message["text"] for s in HOUSES)
            or
            'hedgehog' in message['text']))

    def process_message(self, message):
        print 'is_alice_related'
        for m in self.award_points(message):
            os.system(
                "curl -F file=@%s -F title=%s -F channels=%s -F token=%s https://slack.com/api/files.upload"
                 % (m['file'], m['file_title'], CHANNEL, SLACK_TOKEN))
        if 'hedgehog' in message['text']:
            self.sc.api_call(
                "chat.postMessage", channel=CHANNEL, text='\n'.join(["%s: %s" % (k, v) for k, v in self.points.iteritems()]))
            self.print_points()

    def award_points(self, message):
        if message.get('user', None) == BOT_USER:
            return []
        houses = list(set(s for s in HOUSES if s in message['text']))
        messages = []
        print "planning to award points to %s" % houses
        if houses:
            for house in houses:
                value = random.choice(CARD_VALUES.keys())
                print "drew %s for %s" % (value, house)
                self.points[house] += random.choice([1, 11]) if value == 'A' else CARD_VALUES[value]
                pickle.dump(self.points, open(self.points_file, 'wb'))
                messages.append({
                    'text': house * CARD_VALUES[value],
                    'file': self.file_for(house, value),
                    'file_title': house * CARD_VALUES[value]
                    })
        return messages

    def file_for(self, suit, value):
        return 'cards/%s%s.gif' % (suit[1], str(value))

    def print_points(self):
        cards = 'JQKA'
        for i, suit in enumerate(sorted(self.points, key=lambda x: self.points[x])):
            print self.file_for(suit, cards[i])
            os.system(
                "curl -F file=@%s -F title='%s' -F channels=%s -F token=%s https://slack.com/api/files.upload"
                 % (self.file_for(suit, cards[i]), '%s of %s' % (cards[i], suit), CHANNEL, SLACK_TOKEN))


def main():
    sc = SlackClient(SLACK_TOKEN)
    p = AlicePointCounter(sc) if MODE == 'alice' else PointCounter(sc)
    if sc.rtm_connect():
        while True:
            messages = sc.rtm_read()
            for message in messages:
                if p.is_related(message):
                    p.process_message(message)

                time.sleep(1)
    else:
        print "Connection Failed, invalid token?"


if __name__ == "__main__":
    main()
