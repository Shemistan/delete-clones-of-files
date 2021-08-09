import os
from PIL import Image, ImageChops


class ValueError(Exception):
    pass


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
                    self.dict_all_photos[dictonary_key] = [
                        dirpath,
                        dirnames,
                        file
                    ]
                    dictonary_key += 1
        if self.dict_all_photos == {}:
            raise ValueError('No images found in the specified path!')

    def check_for_size(self):
        comparision_dick = dict(self.dict_all_photos)
        new_dict_all_photos = {}
        progress_of_implementation = len(self.dict_all_photos)

        for key_dict_1 in self.dict_all_photos.keys():
            progress_of_implementation -= 1
            print('Progress of implementation '
                  f'check_by_size ----->  {progress_of_implementation}')
            list_identic_photo = []

            current_file = self.find_out_the_size_of_the_image(
                image=self.dict_all_photos[key_dict_1][1]
            )
            del comparision_dick[key_dict_1]

            for key_dict_2 in comparision_dick.keys():
                if comparision_dick[key_dict_2]:
                    check_file = self.find_out_the_size_of_the_image(
                        image=comparision_dick[key_dict_2][1]
                    )
                    if current_file == check_file:
                        list_identic_photo.append(comparision_dick[key_dict_2][1])
                        comparision_dick[key_dict_2] = None
            if list_identic_photo:
                key_new_dict_all_photos = self.dict_all_photos[key_dict_1][1]
                new_dict_all_photos[key_new_dict_all_photos] = list_identic_photo
        self.dict_all_photos = dict(new_dict_all_photos)

    def check_for_pixel(self):
        progress_of_implementation = len(self.dict_all_photos)
        clones = []
        for foto, identic_fotos in self.dict_all_photos.items():
            progress_of_implementation -= 1
            print('Progress of implementation '
                  f'check_for_pixel ----->   {progress_of_implementation}')
            current_file = self.open_photo_and_resize(photo=foto)
            for identic_foto in identic_fotos:
                check_file = self.open_photo_and_resize(photo=identic_foto)
                result = ImageChops.difference(current_file, check_file).getbbox()
                if result is None:
                    clones.append(identic_foto)
            self.identical_photos.append([foto, clones])
            clones = []

    def open_photo_and_resize(self, photo):
        file = Image.open(photo)
        file.thumbnail(self.size)
        return file

    def find_out_the_size_of_the_image(self, image):
        return os.stat(image).st_size

    def remove_clones_of_photo(self):
        self.run()
        for foto in self.identical_photos:
            for clones in foto[1]:
                if clones:
                    os.remove(clones)

    def show(self):
        number_of_clones = 0
        print('**' * 20, 'List of identical photos')
        for clones in self.identical_photos:
            print(number_of_clones, ' Original ->', clones[0], ' Clones-->', clones[1])
            number_of_clones += 1

    def run(self):
        self.looking_for_all_photos()
        self.check_for_size()
        self.check_for_pixel()
        self.show()


path = '/Users/shemistan/фото/'
photo = Equalizer(path=path)
photo.run()
photo.remove_clones_of_photo()
