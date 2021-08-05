from PIL import Image, ImageChops
import os


def photo_comparison(file_1, file_2):
    result = ImageChops.difference(file_1, file_2).getbbox()
    return result


class Equalizer:
    image_formats = ('.jpg', '.png')

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
                if filenames != [] and file[-4:] in self.image_formats:
                    dirnames = os.path.join(dirpath, file)
                    self.dict_all_photos[n] = [dirpath, dirnames, file]
                    n += 1

    def search_for_identical_photos(self):
        task_dick = self.dict_all_photos
        for i in self.dict_all_photos.keys():
            current_file_path = self.dict_all_photos[i][1]
            current_file = self.work_with_photos(photo=current_file_path)
            del task_dick[i]
            for n in task_dick.keys():
                check_file_path = task_dick[n][1]
                check_file = self.work_with_photos(photo=check_file_path)
                result = photo_comparison(file_1=current_file, file_2=check_file)
                if result is None:
                    self.identical_photos.append([current_file_path, check_file_path])

    def work_with_photos(self, photo):
        file = Image.open(photo)
        file.thumbnail(self.size)
        return file

# print(result.getbbox())
# path = '/Users/shemistan/фото/Азербайджан/'
# photo = Equalizer(path=path)
# photo.looking_for_all_photos()
# photo.search_for_identical_photos()
# photo.try_except()
# photo.search_for_identical_photos()
