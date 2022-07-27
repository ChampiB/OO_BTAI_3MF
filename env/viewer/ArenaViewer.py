from tkinter import *
from PIL import ImageTk


#
# Class implementing a grid viewer displaying an environment visually.
#
class ArenaViewer:

    def __init__(self, title, imgs, warriors_lps, mages_lps):
        """
        Constructor.
        :param title: the window's title.
        :param imgs: the images to display in the grid.
        :param warriors_lps: the life points of the warriors.
        :param mages_lps: the life points of the mages.
        """

        # Create the root window.
        self.root = Tk()
        self.root.title(title)

        # Add the image to the root window.
        self.imgs = []
        self.img_labels = []
        height = len(imgs[0])
        for x in range(0, height):
            self.img_labels.append([])
            for y in range(len(imgs[0])):
                img = self.to_photo_image(imgs[x][y])
                self.img_labels[x].append(Label(self.root, image=img))
                self.img_labels[x][y].grid(row=x, column=y)
                self.imgs.append(img)

        # Add the life point label to the root window.
        self.warriors_lps_labels = []
        for y in range(len(warriors_lps)):
            self.warriors_lps_labels.append(Label(self.root, text="Warrior {}: ".format(y)))
            self.warriors_lps_labels[2 * y].grid(row=height + y, column=0)
            self.warriors_lps_labels.append(Label(self.root, text=str(warriors_lps[y]) + " LP"))
            self.warriors_lps_labels[2 * y + 1].grid(row=height + y, column=1)
        self.mages_lps_labels = []
        for y in range(len(mages_lps)):
            self.mages_lps_labels.append(Label(self.root, text="Mage {}: ".format(y)))
            self.mages_lps_labels[2 * y].grid(row=height + y, column=2)
            self.mages_lps_labels.append(Label(self.root, text=str(warriors_lps[y]) + " LP"))
            self.mages_lps_labels[2 * y + 1].grid(row=height + y, column=3)

        # Refresh the main window.
        self.root.update()

    def update(self, imgs, warriors_lps, mages_lps):
        """
        Update the viewer.
        :param imgs: the images to display in the grid.
        :param warriors_lps: the life points of the warriors.
        :param mages_lps: the life points of the mages.
        :return: nothing.
        """
        # Update the image.
        self.imgs.clear()
        for x in range(0, len(imgs)):
            for y in range(len(imgs[0])):
                img = self.to_photo_image(imgs[x][y])
                self.img_labels[x][y].configure(image=img)
                self.imgs.append(img)

        # Update the life points.
        for y in range(len(warriors_lps)):
            self.warriors_lps_labels[2 * y + 1].configure(text=str(warriors_lps[y]) + " LP")
        for y in range(len(mages_lps)):
            self.mages_lps_labels[2 * y + 1].configure(text=str(mages_lps[y]) + " LP")

        # Refresh the main window.
        self.root.update()

    @staticmethod
    def to_photo_image(img):
        """
        Returns the input image as an PhotoImage, i.e. the format require for display.
        :return: the formatted input image required by pillow and tkinter for render.
        """
        return ImageTk.PhotoImage(img)
