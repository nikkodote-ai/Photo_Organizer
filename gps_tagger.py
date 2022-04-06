import os.path

from PIL import Image
from pprint import pprint

#because getexif() is not human-readable, using GPSTAGS and TAGS will make it readable
from PIL.ExifTags import GPSTAGS, TAGS

#this bit is inspired by https://python.hotexamples.com/site/redirect?url=https%3A%2F%2Fgithub.com%2Frollinginsanity%2FNameTheLocation
filename = 'sample3_loc.JPG'
class GPS_tagger():
    def __init__(self):
        self.tags = {}
        self.gpstags = {}


    def get_tags(self,filename):
        img = Image.open(filename)
        raw_exif = img._getexif()
        #iterate through all the EXIF data to group photos by date or location
        for tag, value in raw_exif.items():
             #translate the bits to string
             tag_name = TAGS.get(tag,tag)
             #save tag_name in tags dictionary with the value
             self.tags[tag_name] = value
        #we can get the 'GPSinfo' from the translated exif data.
        #therefore, we can can get translate it using GPSTAGS module
        try:
            raw_GPSexif = self.tags['GPSInfo']
            # print(f'raw {raw_GPSexif}')

            #using similar process but using GPSTAGS:
            for gpstag, value in raw_GPSexif.items():
                # translate the bits to string
                gps_name = GPSTAGS.get(gpstag, gpstag)

                self.gpstags[gps_name] = value
        except:
            pass
        return{'tags': self.tags, 'gpstags': self.gpstags}

    def print_tags(self):
        for tag, value in self.tags.items():
            pprint(f'{tag}: {value}')

    def print_gps_tags(self):
        for gpstag, value in self.gpstags.items():
            pprint(f'{gpstag}: {value}')

    def get_coordinates(self):
        #inspired by https://medium.com/geekculture/extract-gps-information-from-photos-using-python-79288c58ccd9

        lat_dms = self.gpstags['GPSLatitude']
        lon_dms = self.gpstags['GPSLongitude']
        lat_ref = self.gpstags['GPSLatitudeRef']
        lon_ref = self.gpstags['GPSLongitudeRef']


        #convert DMS(degree, minute, seconds) for to Decimals
        lat_dd = float(lat_dms[0] + (lat_dms[1] / 60) + (lat_dms[2] / (3600 * 100)))
        lon_dd = float(lon_dms[0] + (lon_dms[1] / 60) + (lon_dms[2] / (3600 * 100)))

        # Negative if LatitudeRef:S or LongitudeRef:W
        if self.gpstags['GPSLatitudeRef'] == 'S':
            lat_dd = -lat_dd
        if self.gpstags['GPSLongitudeRef'] == 'W':
            lon_dd = -lon_dd

        return {'lat': lat_dd, 'lng': lon_dd}

# trial = GPS_tagger()
# trial.get_tags("C:\\Users\\nikko\\OneDrive\\Pictures\\qld holiday\\Strad ata or brissu\\pictures\\IMG_8803.JPG")
# trial.print_tags()

# print(os.path.getctime("C:\\Users\\nikko\\OneDrive\\Pictures\\SORTED_PICTURES\\2000\\January-week-52--\\IMG_8295.JPG"))