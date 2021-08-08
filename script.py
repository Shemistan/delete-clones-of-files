from PIL import Image, ImageChops
import os
from collections import defaultdict


class Equalizer:
    IMAGE_FORMATS = ('.jpg', '.png', '.JPG', '.PNG', '.bmp', '.BMP')

    def __init__(self, path, size=None):
        self.dict_all_photos = {}
        self.identical_photos = []
        if size is None:
            size = [100, 75]
        self.path = os.path.normpath(path)
        self.size = size

    def looking_for_all_photos(self):
        n = 0
        for dirpath, dirnames, filenames in os.walk(self.path):
            for file in filenames:
                if filenames != [] and file[-4:] in self.IMAGE_FORMATS:
                    dirnames = os.path.join(dirpath, file)
                    self.dict_all_photos[n] = [dirpath, dirnames, file]
                    n += 1

    def check_for_size(self):
        comparision_dick = dict(self.dict_all_photos)
        new_dict_all_photos = defaultdict(int)
        ch = len(self.dict_all_photos)
        for i in self.dict_all_photos.keys():
            ch -= 1
            print('Progress of implementation check_by_size ----->  ', ch)
            list_identic_photo = []
            current_file = os.stat(self.dict_all_photos[i][1]).st_size
            del comparision_dick[i]
            for n in comparision_dick.keys():
                check_file = os.stat(comparision_dick[n][1]).st_size
                if current_file == check_file:
                    list_identic_photo.append(comparision_dick[n][1])
            if list_identic_photo:
                new_dict_all_photos[self.dict_all_photos[i][1]] = list_identic_photo
        self.dict_all_photos = dict(new_dict_all_photos)

    def check_for_pixel(self):
        ch = len(self.dict_all_photos)
        for foto, identic_fotos in self.dict_all_photos.items():
            ch -= 1
            print('Progress of implementation check_for_pixel ----->  ', ch)
            current_file = self.work_with_photos(photo=foto)
            for identic_foto in identic_fotos:
                check_file = self.work_with_photos(photo=identic_foto)
                result = ImageChops.difference(current_file, check_file).getbbox()
                if result is None:
                    self.identical_photos.append([foto, identic_foto])

    def work_with_photos(self, photo):
        file = Image.open(photo)
        file.thumbnail(self.size)
        return file

    def remove_clones_of_photo(self):
        for i in self.identical_photos:
            os.remove(i[1])

    def show(self):
        n = 0
        for i in self.identical_photos:
            print(n, ' ', i[0], ' <--------> ', i[1])
            n += 1


path = '/Users/shemistan/фото/'
photo = Equalizer(path=path)
photo.looking_for_all_photos()
photo.check_for_size()
photo.check_for_pixel()
photo.show()
#photo.remove_clones_of_photo()
