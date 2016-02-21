from consts import HOUSES, IMAGE_PATH
from PIL import Image, ImageDraw


BAR_WIDTH = 103.5
BAR_BOTTOM = 947
BAR_HEIGHT = 650

BAR_X = {
	"Gryffendor": 306,
	"Hufflepuff": 551,
	"Slytherin": 806,
	"Ravenclaw": 1043,
}

BAR_COLOR = {
	"Gryffendor": "#ff0000",
	"Ravenclaw": "#0000ff",
	"Hufflepuff": "#ffff00",
	"Slytherin": "#00ff00",
}


def calculate_scales(house_points):
	total_points = float(sum(house_points.values())) or 1.0

	return {house: house_points.get(house, 0) / total_points for house in HOUSES}

def draw_bar_for_house(im, house, scale):
	draw = ImageDraw.Draw(im)
	draw.rectangle((BAR_X[house], BAR_BOTTOM,
		 			BAR_X[house] + BAR_WIDTH, BAR_BOTTOM - scale * BAR_HEIGHT),
	                fill=BAR_COLOR[house])
	draw.ellipse((BAR_X[house], BAR_BOTTOM - 50, BAR_X[house] + BAR_WIDTH, BAR_BOTTOM + 50), fill=BAR_COLOR[house])
	del draw


def image_for_scores(scores, upload=True):
	"""Generate a sweet house cup image
   Arguments: a dictionary with house names as keys and scores as values
   Returns: an imgur link to a house cup image representing the
   scores
	"""
	scaled = calculate_scales(scores)
	points_image = Image.open(IMAGE_PATH)
	for house in HOUSES:
		draw_bar_for_house(points_image, house, scaled[house])

	outfile = str(abs(hash(str(scores)))) + '.png'
	points_image.save(outfile, "PNG")
	return outfile


if __name__=="__main__":
	image_for_scores(BAR_X, upload=False)