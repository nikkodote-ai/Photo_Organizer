import os
import shutil
from opencage.geocoder import OpenCageGeocode
from gps_tagger import GPS_tagger
from tkinter import filedialog
import datetime

#use Opencage for reverse geocoding
GEO_API_KEY = os.getenv('OPEN_CAGE-API_KEY')
geocoder = OpenCageGeocode(GEO_API_KEY)

#----FUNCTIONS------
def reverse_geocode(lat, lng):
    location = geocoder.reverse_geocode(lat = lat, lng = lng)
    #use dict.get() function so a value can be substituted in case the key does not exist
    components = location[0]['components']
    municipality = components.get('municipality', '')
    locality = components.get('locality', '')
    state = components.get('state', '')
    country = components.get('country', '')
    city = components.get('city', '')
    formatted = {'municipality': municipality, 'locality': locality,'state': state, 'country':country, 'city': city}
    return formatted

def move_photos(source_folder_path, destination_folder):
    #choose all images in the folder
    images = os.listdir(source_folder_path)
    images = [img for img in images if img.lower().endswith(('jpg', 'jpeg'))] #capture all jpg, jpeg,


    #destination folder; can be substituted with filedialog

    #note for nikko : os.makedirs for nester directory, os.mkdir, direct, only one folder

    #get the coordinates in Decimal format
    for i, filename in enumerate(images):
        source_file_path = os.path.join(source_folder_path, filename)
        gps_tagger = GPS_tagger()
        gps_tagger.get_tags(source_file_path)
        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(source_file_path))
        format_ctime = datetime.datetime.strftime(creation_time, '%Y:%m:%d %H:%M:%S')
        raw_time_stamp = gps_tagger.tags.get('DateTime', format_ctime)

        #raw format : 'DateTime': '2021:05:03 14:57:24'
        #convert timestamp string
        dt = datetime.datetime.strptime(raw_time_stamp, '%Y:%m:%d %H:%M:%S')
        year = dt.year
        month =dt.strftime('%B')
        week = dt.isocalendar().week

        try:
            #If there is a GPSInfo group by location
            lat = gps_tagger.get_coordinates()['lat']
            lng = gps_tagger.get_coordinates()['lng']
            print(f'Got the coordinates - file {i} {filename}: lat: {lat}, lng {lng})')

            results = reverse_geocode(lat, lng)
            print(results)
            print(results["state"])
            year_path = os.path.normpath(f'{destination_folder}/{year}')
            state_path = os.path.normpath(f'{year_path}/BY_LOCATION/{results["state"]}-{results["country"]}/')
            municipal_path = os.path.normpath(f'{state_path}/{results["municipality"]}-{results["locality"]} {results["city"]}-{month}')

            if not os.path.exists(year_path):
                #if there's not year folder, make new folders
                print(f'{year_path} not found, making a new folder')
                #os.makedirs for nester directory, os.mkdir, direct, only one folder
                os.makedirs(municipal_path)

                #shutil move to new folder (source file to dest file)
                shutil.move(source_file_path, municipal_path + f'\\{filename}')
            else:
                #Avoid making duplicate folders.
                if os.path.isdir(state_path):
                    if os.path.isdir(municipal_path):
                        print(f'{municipal_path} already made, moving pictures...')
                        # shutil move to new folder (source file to dest file)
                        shutil.move(source_file_path, municipal_path + f'\\{filename}')
                    else:
                        os.makedirs(municipal_path)
                        shutil.move(source_file_path, municipal_path + f'\\{filename}')
                        print(f'FRESH {municipal_path} made, moving pictures...')

                else:
                    print(f'FRESH {municipal_path} made, moving pictures...')
                    os.makedirs(municipal_path)
                    shutil.move(source_file_path, municipal_path + f'\\{filename}')


        except KeyError:

            #for images WITHOUT coordinates; sort by date >
            # [folder: year][month][week] at the end iterate
            # ask [event] to rename

            #create folders: by year and month:

            print(f'{i}, {filename} time stamp year: {year}'
                  f' month: {month} week:{week} has no GPS INFO: '
                  f'use date to organize')

            year_path = os.path.normpath(f'{destination_folder}/{year}')
            month_week_path = os.path.normpath(f'{year_path}/{month}-week-{week}--')

            if not os.path.isdir(year_path):
                print(f'{year_path} not found, making a new folder')
                os.makedirs(month_week_path)
                shutil.move(source_file_path, month_week_path + f'\\{filename}')

            else:

                if os.path.isdir(month_week_path):
                    print(f'{month_week_path} already made, moving pictures...')
                    # shutil move to new folder (source file to dest file)
                    shutil.move(source_file_path, month_week_path + f'\\{filename}')

                else:
                    print(f'FRESH {month_week_path} made, moving pictures...')
                    os.makedirs(month_week_path)
                    shutil.move(source_file_path, month_week_path + f'\\{filename}')



#open file dialog to choose folder
source_folder_path = filedialog.askdirectory()
folders = os.listdir(source_folder_path)
print(f' source folder: {source_folder_path}')
destination_folder = "C:\\Users\\nikko\\OneDrive\\Desktop\\SORTED_PICTURES"

try:
    for folder in folders:
        move_photos(source_folder_path + '\\' + folder, destination_folder)
except:
    move_photos(source_folder_path, destination_folder)


