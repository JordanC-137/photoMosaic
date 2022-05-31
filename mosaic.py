from PIL import Image
import numpy as np
import glob
from scipy import spatial

photo_path = "england.jpeg"
tile_photos_path = "albums/*"

tile_size = (100,100)
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

output.save("output.jpg")