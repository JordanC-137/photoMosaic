from PIL import Image, ImageOps, ImageDraw, ImageFont
import numpy as np
import glob
from scipy import spatial
import sys

tile_size = (0,0)

if __name__ == "__main__":
	tile_size = (int(sys.argv[1]), int(sys.argv[1]))

photo_path = "IMG_2624.jpg"
tile_photos_path = "albums/*"

#tile_size = (10,10)
tiles = []


def importAndResizeTiles(path, outputDimensions):
	#Adding each image path to a list
	tile_paths = []
	images = []
	for file in glob.glob(tile_photos_path):
		tile_paths.append(file)
	#Opening each image and resizing them
	for path in tile_paths:
		tile = Image.open(path)
		tile = tile.resize(outputDimensions)
		images.append(tile)
	return images

#Takes each tile from provided list and calculates the average colour across all the pixels
def avgColourOfEachTile(tiles):
	colours = []
	for tile in tiles:
		meanColour = np.array(tile).mean(axis=0).mean(axis=0)
		colours.append(meanColour)
	return colours


#Possible that the code can be made more distinctive by combining colours and tile lists into a dictionary

tiles = importAndResizeTiles(tile_photos_path, tile_size)
colours = avgColourOfEachTile(tiles)

#Pixelate the image so each pixel corresponds to a tile to be drawn
photo = Image.open(photo_path)
width = int(np.round(photo.size[0] / tile_size[0]))
height = int(np.round(photo.size[1] / tile_size[1]))

pixelatedImage = photo.resize((width, height))

#Finding the 
tree = spatial.KDTree(colours)
closest_colour_indices = np.zeros((width, height), dtype = np.uint32)

#Creating grid of numbers corresponding to index of most appropriate colour/tile
for i in range(width):
	for j in range(height):
		pixel = pixelatedImage.getpixel((i,j))
		closest = tree.query(pixel)
		closest_colour_indices[i,j] = closest[1]

output = Image.new('RGB', photo.size)
for i in range(width):
	for j in range(height):
		x, y = i*tile_size[0], j*tile_size[1]
		index = closest_colour_indices[i,j]
		output.paste(tiles[index], (x,y))

#output.show()
#Add border
outputWithBorder = ImageOps.expand(output, border = (0, 0, 0, 100))

#Add text
draw = ImageDraw.Draw(outputWithBorder)
font = ImageFont.truetype("16020_FUTURAM.ttf", 30)
#draw.text((outputWithBorder.width / 2, outputWithBorder.height - 100), "Title", (255,255,255), font = font)
msg = "Title"
w, h = draw.textsize(msg, font = font)
draw.text(((outputWithBorder.width - w )/ 2, outputWithBorder.height - 100), msg, (255,255,255), font = font)


outputWithBorder.show()
#output.save("output.jpg")