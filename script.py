import os
from PIL import Image, ImageChops
from collections import defaultdict


class Equalizer:
    """Script for finding identical photos
     of various formats with the ability
     to remove clones"""

    IMAGE_FORMATS = ('.jpg', '.JPG',
                     '.png', '.PNG',
                     '.bmp', '.BMP')

    def __init__(self, path, size=None):
        self.dict_all_photos = {}
        self.identical_photos = []
        if size is None:
            size = [200, 150]
        self.path = os.path.normpath(path)
        self.size = size

    def looking_for_all_photos(self):
        dictonary_key = 0
        for dirpath, dirnames, filenames in os.walk(self.path):
            for file in filenames:
                if file != [] and file[-4:] in self.IMAGE_FORMATS:
                    dirnames = os.path.join(dirpath, file)
                    self.dict_all_photos[dictonary_key] = [dirpath, dirnames, file]
                    dictonary_key += 1

    def check_for_size(self):
        comparision_dick = dict(self.dict_all_photos)
        new_dict_all_photos = defaultdict(int)
        execution_process = len(self.dict_all_photos)
        for key_dict_1 in self.dict_all_photos.keys():
            execution_process -= 1
            print('Progress of implementation check_by_size ----->  ', execution_process)
            list_identic_photo = []
            current_file = os.stat(self.dict_all_photos[key_dict_1][1]).st_size
            del comparision_dick[key_dict_1]
            for key_dict_2 in comparision_dick.keys():
                if comparision_dick[key_dict_2]:
                    check_file = os.stat(comparision_dick[key_dict_2][1]).st_size
                    if current_file == check_file:
                        list_identic_photo.append(comparision_dick[key_dict_2][1])
                        comparision_dick[key_dict_2] = None
            if list_identic_photo:
                key_new_dict_all_photos = self.dict_all_photos[key_dict_1][1]
                new_dict_all_photos[key_new_dict_all_photos] = list_identic_photo
        self.dict_all_photos = dict(new_dict_all_photos)

    def check_for_pixel(self):
        execution_process = len(self.dict_all_photos)
        clones = []
        for foto, identic_fotos in self.dict_all_photos.items():
            execution_process -= 1
            print('Progress of implementation check_for_pixel ----->  ', execution_process)
            current_file = self.work_with_photos(photo=foto)
            for identic_foto in identic_fotos:
                check_file = self.work_with_photos(photo=identic_foto)
                result = ImageChops.difference(current_file, check_file).getbbox()
                if result is None:
                    clones.append(identic_foto)
            self.identical_photos.append([foto, clones])
            clones = []

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
# photo.remove_clones_of_photo()
