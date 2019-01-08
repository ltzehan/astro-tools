#
#   Handles writing data to files and the various output types
#

import sys
import os
import shutil
from threading import Lock, Thread
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

class Writer:

    def __init__(self, n, using_pdf):

        self.using_pdf = using_pdf
        self.manage_outdir()

        if using_pdf:
            self.img_list = []

        else:
            # python has no atomics ;;
            self.counter = 0
            self.lock = Lock()

    # clear directory if exists or create one
    def manage_outdir(self):

        out_dir = os.path.join(sys.path[0], "output")

        if os.path.exists(out_dir) and os.path.isdir(out_dir):
            print(">> Cleared output directory")
            # work around for how python flags directories for deletion
            del_dir = "del"
            os.rename(out_dir, del_dir)
            shutil.rmtree(del_dir)

        # make empty output directory
        os.makedirs(out_dir)
        os.chdir(out_dir)

    # if output type is PDF, stores image bytes in a list for writing later
    # otherwise write to JPG in parallel
    def write(self, img):

        if self.using_pdf:
            self.img_list.append(img)
        else:
            Thread(target=self.write_jpg, args=(img, )).start()

    # writes to JPG files
    def write_jpg(self, img):

        # increment counter
        with self.lock:
            idx = self.counter
            self.counter += 1

        # JPG requires RGB mode
        img.convert("RGB").save("img-{}.jpg".format(idx))

    # writes to PDF files
    def write_pdf(self):

        c = Canvas("skyline.pdf", pagesize=A4)
        w, h = A4

        for img in self.img_list:
            # draw a square image that fits to page width
            c.drawInlineImage(img, 0, h-w, w, w)
            c.showPage()

        c.save()

    # writes PDF files or clean up threads used for JPG writing
    def close(self):

        if self.using_pdf:
            self.write_pdf()
