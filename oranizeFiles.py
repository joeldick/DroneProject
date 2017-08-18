import os
import time
import datetime
import exifread
import shutil


def seconds_to_date(seconds):
    ms = round(seconds % 1, 3) * 1000
    ms_str = '{:03.0f}'.format(ms)
    timestruct = time.localtime(seconds)
    timestring = time.strftime('%Y%m%d%H%M%S', timestruct) + ms_str
    return timestring


if __name__ == '__main__':

    file_handler = open('media/' + os.listdir('media')[0], 'rb')
    tags = exifread.process_file(file_handler)

    last_file_created = 0
    for file in os.listdir('media'):
        # get filename and extension
        filename, file_extension = os.path.splitext(file)
        print("old name: " + str(filename) + str(file_extension))

        if file_extension == '.MP4':
            new_filename = 'media/video/' + file
            print("new name: " + new_filename)
            shutil.move('media/' + file, new_filename)
            continue

        # get time created, and difference from previous
        file_handler = open('media/' + file, 'rb')
        tags_next = exifread.process_file(file_handler)

        for tag in tags_next:
            if str(tags[tag]) != str(tags_next[tag]):
                print(str(tag) + ": " + str(tags[tag]) + " - " + str(tags_next[tag]))

        tags = tags_next

        time_taken = datetime.datetime.strptime(str(tags['EXIF DateTimeOriginal']),
                                                '%Y:%m:%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        delta = (int(time_taken) - last_file_created)
        print("file created: " + str(delta))
        last_file_created = int(time_taken)

        if file_extension == '.JPG':
            new_filename = 'media/images/' + time_taken + file_extension
            print("new name: " + new_filename)
            # copyfile('media/' + file, new_filename)

        print()
