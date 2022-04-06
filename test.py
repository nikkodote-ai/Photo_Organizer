from PIL.ExifTags import GPSTAGS, TAGS
from PIL import Image

def getGPSTags(imagePath):
    image = Image.open(imagePath)
    #Get the EXIF data from the image.
    rawEXIF = image._getexif()

    #Somewhere to store the rest of the EXIF data, I might use it one day.
    tags = {}

    #Aaand a place to store the GPS data.
    gpsTags = {}

    #pulling out the EXIF tags.
    for tag, value in rawEXIF.items():
        decoded = TAGS.get(tag,tag)
        tags[decoded] = value

    rawGPS = tags['GPSInfo']
    print(rawGPS)
    #Pulling out the GPS specific tags.
    for gpstag , value in rawGPS.items():
        decoded = GPSTAGS.get(gpstag,gpstag)
        gpsTags[decoded] = value

    #Pull together our return variable that includes both tagsets.
    return {'tags' : tags, 'gps' : gpsTags}

print(getGPSTags('sample3_loc.jpg'))
