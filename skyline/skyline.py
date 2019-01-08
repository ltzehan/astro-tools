#
#   Handles run-time input and calls
#

import time
import argparse
from yoursky import Yoursky

# check if value is a positive integer
def pos_int(x):

    try:
        n = int(x)
    except ValueError:
        raise argparse.ArgumentTypeError("{} is not a positive integer".format(x))

    if n < 1:
        raise argparse.ArgumentTypeError("{} is not a positive integer".format(x))
    else:
        return n

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Fetches randomized star maps")

    # number of star maps to be generated
    parser.add_argument("-n", metavar="N", type=pos_int, default=1, help="number of star maps to be generated")

    # limiting magntitude of stars
    parser.add_argument("-l", metavar="LMAG", type=float, default=5.5, dest="lmag", help="limiting magnitude of stars to be shown")

    # size of image
    parser.add_argument("-i", metavar="IMGSIZE", type=pos_int, default=1024, dest="imgsize", help="size of image in pixels")

    # output type of images
    # if pdf is selected, aggregates all images in a single PDF sile
    parser.add_argument("--pdf", action="store_true", default=False, dest="using_pdf", help="if present, outputs all images in a single PDF")

    # parse args and return dict
    opts = vars(parser.parse_args())

    start = time.time()

    ys = Yoursky(**opts)
    ys.fetch_imgs()

    end = time.time()
    print(">> Done in {}s".format(round(end - start, 2)))
