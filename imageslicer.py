#!/usr/bin/PYTHON
# -*-coding:utf-8 -*

#===================================================================#
#-------------------------------------------------------------------#
#                     Image Slicer                                  #
#-------------------------------------------------------------------#
#*******************************************************************#
#                  BFTeck - 24-04-2019                              #
#-------------------------------------------------------------------#
#                         Notes                                     #
#                                                                   #
#-------------------------------------------------------------------#
#                            HISTORY                                #
#   V0.1.0    BFTeck - 24-04-2019                                   #
#             Initial                                               #
#===================================================================#


#--------------------------------------------#
#                  Packages                  #
#--------------------------------------------#
import os
from math import sqrt, ceil, floor
from PIL import Image




#--------------------------------------------#
#                Variables                   #
#--------------------------------------------#


#--------------------------------------------#
#                    Code                    #
#--------------------------------------------#

def get_basename(filename):
    """Strip path and extension. Return basename."""
    return os.path.splitext(os.path.basename(filename))[0]

def open_images_in(directory):
    """Open all images in a directory. Return tuple of Image instances."""
    return [Image.open(file) for file in os.listdir(directory)]

def get_columns_rows(filenames):
    """Derive number of columns and rows from filenames."""
    tiles = []
    for filename in filenames:
        row, column = os.path.splitext(filename)[0][-5:].split('_')
        tiles.append((int(row), int(column)))
    rows = [pos[0] for pos in tiles]; columns = [pos[1] for pos in tiles]
    num_rows = max(rows); num_columns = max(columns)
    return (num_columns, num_rows)

class Tile(object):
    """Represents a single tile."""

    def __init__(self, image, number, position, coords, filename=None):
        self.image = image
        self.number = number
        self.position = position
        self.coords = coords
        self.filename = filename

    @property
    def row(self):
        return self.position[0]

    @property
    def column(self):
        return self.position[1]

    @property
    def basename(self):
        """Strip path and extension. Return base filename."""
        return get_basename(self.filename)

    def generate_filename(self, directory=os.getcwd(), prefix='tile',
                          format='png', path=True):
        """Construct and return a filename for this tile."""
        filename = prefix + '_{col:02d}_{row:02d}.{ext}'.format(
                      col=self.column, row=self.row, ext=format.lower().replace('jpeg', 'jpg'))
        if not path:
            return filename
        return os.path.join(directory, filename)

    def save(self, filename=None, format='png'):
        if not filename:
            filename = self.generate_filename(format=format)
        self.image.save(filename, format)
        self.filename = filename

    def __repr__(self):
        """Show tile number, and if saved to disk, filename."""
        if self.filename:
            return '<Tile #{} - {}>'.format(self.number,
                                            os.path.basename(self.filename))
        return '<Tile #{}>'.format(self.number)


def calc_columns_rows(n):
    """
    Calculate the number of columns and rows required to divide an image
    into ``n`` parts.
    Return a tuple of integers in the format (num_columns, num_rows)
    """
    num_columns = int(ceil(sqrt(n)))
    num_rows = int(ceil(n / float(num_columns)))
    return (num_columns, num_rows)

def calc_columns_rows_to_join(tiles):
    """
    Return a tuple of integers in the format (num_columns, num_rows)
    """
    
    linmax=0
    colmax=0
    numberoftile=0
    for tile in tiles:

        columns=tile.position[0]
        rows=tile.position[1]
        numberoftile=numberoftile+1
        if columns > colmax:
            colmax=columns
        if rows > linmax:
            linmax=rows
    return (colmax, linmax)

def get_combined_size(tiles):
    """Calculate combined size of tiles."""
    tile_size = tiles[0].image.size
    hsize=tile_size[0]
    vsize=tile_size[1]
    hrest=0
    vrest=0
    lin=0
    col=0
    linmax=0
    colmax=0
    print(tile_size)
    print(hsize)
    print(vsize)
    for tile in tiles:
        col=col+1
        if tile.image.size[1] != vsize:
            if vrest==0:
                vrest=tile.image.size[1]
                linmax=lin
        if tile.image.size[0] != hsize:
            lin=lin+1
            if hrest==0:
                hrest=tiles[0].image.size
                colmax=col

    if linmax==0 and colmax==0:
        """
        columns, rows = calc_columns_rows_to_join(tiles)

        largeur=hsize * columns
        hauteur=vsize * rows
        print("largeur:")
        print(largeur)
        print("hauteur:")
        print(hauteur)
        return (largeur, hauteur)
        """
        columns, rows = calc_columns_rows(len(tiles))
        tile_size = tiles[0].image.size
        return (tile_size[0] * columns, tile_size[1] * rows)
    else:
        if linmax==0:
            linmax = len(tiles)/colmax
        if colmax==0:
            colmax = len(tiles)/linmax
        columns=colmax
        rows=linmax
        if vrest==0:
            hauteur=vsize*rows
        else:
            hauteur=(vsize*(rows-1))+vrest

        if hrest==0:
            largeur=hsize*columns
        else:
            largeur=(hsize*(columns-1))+hrest
        print("largeur:")
        print(largeur)
        print("hauteur:")
        print(hauteur)

        return (largeur, hauteur)
    


def join(tiles):
    """
    @param ``tiles`` - Tuple of ``Image`` instances.
    @return ``Image`` instance.
    """
    im = Image.new('RGB', get_combined_size(tiles), None)
    columns, rows = calc_columns_rows_to_join(tiles)
    for tile in tiles:
        im.paste(tile.image, tile.coords)
    return im


def validate_image(image, number_tiles):
    """Basic sanity checks prior to performing a split."""
    TILE_LIMIT = 99 * 99

    try:
        number_tiles = int(number_tiles)
    except:
        raise ValueError('number_tiles could not be cast to integer.')

    if number_tiles > TILE_LIMIT or number_tiles < 2:
        raise ValueError('Number of tiles must be between 2 and {} (you \
                          asked for {}).'.format(TILE_LIMIT, number_tiles))

def slice(filename, number_tiles, save=True):

    im = Image.open(filename)

    return slice_by_number(im, number_tiles, save)

def slice_by_number(im, number_tiles, save):
    """
    Split an image into a specified number of tiles.
    Args:
       filename (str):  The filename of the image to split.
       number_tiles (int):  The number of tiles required.
    Kwargs:
       save (bool): Whether or not to save tiles to disk.
    Returns:
        Tuple of :class:`Tile` instances.
    """
    validate_image(im, number_tiles)

    im_w, im_h = im.size
    columns, rows = calc_columns_rows(number_tiles)
    extras = (columns * rows) - number_tiles
    tile_w, tile_h = int(floor(im_w / columns)), int(floor(im_h / rows))

    tiles = []
    number = 1
    for pos_y in range(0, im_h - rows, tile_h): # -rows for rounding error.
        for pos_x in range(0, im_w - columns, tile_w): # as above.
            area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
            image = im.crop(area)
            position = (int(floor(pos_x / tile_w)) + 1,
                        int(floor(pos_y / tile_h)) + 1)
            coords = (pos_x, pos_y)
            tile = Tile(image, number, position, coords)
            tiles.append(tile)
            number += 1
    if save:
        save_tiles(tiles,
                   prefix=get_basename(filename),
                   directory=os.path.dirname(filename))
    return tuple(tiles)

def slice_by_size(im, number_tiles_row, number_tiles_col, save=True):
    """
    Split an image into a specified number of tiles.
    Args:
       filename (str):  The filename of the image to split.
       number_tiles (int):  The number of tiles required.
    Kwargs:
       save (bool): Whether or not to save tiles to disk.
    Returns:
        Tuple of :class:`Tile` instances.
    """
    number_tiles=number_tiles_row * number_tiles_col
    validate_image(im, number_tiles)

    im_w, im_h = im.size
    columns = number_tiles_col
    rows = number_tiles_row
    extras = (columns * rows) - number_tiles
    tile_w, tile_h = int(floor(im_w / columns)), int(floor(im_h / rows))

    tiles = []
    number = 1
    for pos_y in range(0, im_h - rows, tile_h): # -rows for rounding error.
        for pos_x in range(0, im_w - columns, tile_w): # as above.
            area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
            image = im.crop(area)
            position = (int(floor(pos_x / tile_w)) + 1,
                        int(floor(pos_y / tile_h)) + 1)
            coords = (pos_x, pos_y)
            tile = Tile(image, number, position, coords)
            tiles.append(tile)
            number += 1
    if save:
        save_tiles(tiles,
                   prefix=get_basename(filename),
                   directory=os.path.dirname(filename))
    return tuple(tiles)


def slice_by_px(im, px_tiles_row, px_tiles_col, restinlast=True, save=True, filename="c:\\temp\\test.jpg"):

    """def slice_by_px(im, px_tiles_row, px_tiles_col, save=True):"""

    """
    Split an image into a specified number of tiles.
    Args:
       filename (str):  The filename of the image to split.
       number_tiles (int):  The number of tiles required.
    Kwargs:
       save (bool): Whether or not to save tiles to disk.
    Returns:
        Tuple of :class:`Tile` instances.
    """

    im_w, im_h = im.size

    extras_row=im_w % px_tiles_row
    extras_col= im_h % px_tiles_col

    lastcolwillbedifferent = False
    lastrowwillbedifferent = False



    if extras_col != 0:
        if restinlast==False:
            columns = (im_h // px_tiles_col)+1
        else:
            columns = (im_h // px_tiles_col)
            lastcolwillbedifferent=True
    else:
        columns = (im_h // px_tiles_col)

    if extras_row != 0:
        if restinlast==False:
            rows = (im_w // px_tiles_row)+1
        else:
            lastrowwillbedifferent = True
            rows = (im_w // px_tiles_row)
    """
    if extras_col != 0:
        columns = (im_h // px_tiles_col)+1
    else:
        columns = (im_h // px_tiles_col)
    if extras_row != 0:
        rows = (im_w // px_tiles_row)+1
    """
    else:
        rows = (im_w // px_tiles_row)



    tile_w = px_tiles_row
    tile_h = px_tiles_col

    tiles = []
    number = 1
    for pos_y in range(0, im_h - rows, tile_h): # -rows for rounding error.
        for pos_x in range(0, im_w - columns, tile_w): # as above.

            print("pos_x:")
            print(pos_x)
            print("pos_y:")
            print(pos_y)

            if lastrowwillbedifferent == True and lastcolwillbedifferent == True:
                if (pos_x > im_w - tile_w) and (pos_y > im_h - tile_h):
                    # On est dans la dernière case
                    if restinlast==True:
                        area = (pos_x, pos_y, pos_x + tile_w+extras_row, pos_y + tile_h+extras_col)
                    else:
                        area = (pos_x, pos_y, pos_x + extras_row, pos_y + extras_col)

                elif (pos_x > im_w - tile_w):
                    # On est dans la dernière case
                    if restinlast == True:
                        area = (pos_x, pos_y, pos_x + tile_w + extras_row, pos_y + tile_h)
                    else:
                        area = (pos_x, pos_y, pos_x + extras_row, pos_y + tile_h)
                elif (pos_y > im_h - tile_h):
                    # On est dans la dernière case
                    if restinlast == True:
                        area = (pos_x, pos_y, pos_x + tile_w , pos_y + tile_h + extras_col)
                    else:
                        area = (pos_x, pos_y, pos_x + tile_w, pos_y + extras_col)
                else:
                    area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)

                position = (int(floor(pos_x / tile_w)) + 1,
                            int(floor(pos_y / tile_h)) + 1)
                coords = (pos_x, pos_y)

            elif lastrowwillbedifferent == False and lastcolwillbedifferent == True:
                if (pos_y > im_h - tile_h):
                    # On est dans la dernière case
                    if restinlast == True:
                        area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h + extras_col)
                    else:
                        area = (pos_x, pos_y, pos_x + tile_w, pos_y + extras_col)
                else:
                    area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)

                position = (int(floor(pos_x / tile_w)) + 1,
                            int(floor(pos_y / tile_h)) + 1)
                coords = (pos_x, pos_y)
            elif lastrowwillbedifferent == True and lastcolwillbedifferent == False:
                if (pos_x > im_w - tile_w):
                    # On est dans la dernière case
                    if restinlast == True:
                        area = (pos_x, pos_y, pos_x + tile_w + extras_row, pos_y + tile_h)
                    else:
                        area = (pos_x, pos_y, pos_x + extras_row, pos_y + tile_h)

                else:
                    area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
                position = (int(floor(pos_x / tile_w)) + 1,
                            int(floor(pos_y / tile_h)) + 1)
                coords = (pos_x, pos_y)

            else:

                area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
                position = (int(floor(pos_x / tile_w)) + 1,
                            int(floor(pos_y / tile_h)) + 1)
                coords = (pos_x, pos_y)

            image = im.crop(area)
            tile = Tile(image, number, position, coords)
            tiles.append(tile)
            number += 1

    if save:
        save_tiles(tiles,
                   prefix=get_basename(filename),
                   directory=os.path.dirname(filename))
    return tuple(tiles)



def save_tiles(tiles, prefix='', directory=os.getcwd(), format='png'):
    """
    Write image files to disk. Create specified folder(s) if they
       don't exist. Return list of :class:`Tile` instance.
    Args:
       tiles (list):  List, tuple or set of :class:`Tile` objects to save.
       prefix (str):  Filename prefix of saved tiles.
    Kwargs:
       directory (str):  Directory to save tiles. Created if non-existant.
    Returns:
        Tuple of :class:`Tile` instances.
    """
#    Causes problems in CLI script.
#    if not os.path.exists(directory):
#        os.makedirs(directory)
    for tile in tiles:
        tile.save(filename=tile.generate_filename(prefix=prefix,
                                                  directory=directory,
                                                  format=format),
                                                  format=format)
    return tuple(tiles)
