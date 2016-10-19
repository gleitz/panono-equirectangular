# Convert http://panono.com spheres to equirectanglar images

import os
import re
import requests
import sys


def convert(panono_id):
    directions = ['0', '1', '5', '4', '3', '2']
    filenames = []

    api_url = 'https://api3-dev.panono.com/panorama/{}'.format(panono_id)
    api_json = requests.get(api_url).json()
    base_url = api_json['data']['images']['cubemaps'][0]['base_url']
    image_id = re.match(r"https://tiles.panono.com/5/(\w+)/", base_url).group(1)

    for direction in directions:
        filename = 'tile_{}_0_0_0.jpg'.format(direction)
        filenames.append(filename)
        os.system('wget https://tiles.panono.com/5/' + image_id + '/' + filename + ' -O ' + filename)

    png_filenames = [f.replace('jpg', 'png') for f in filenames]

    os.system('mogrify -format png *.jpg')
    os.system('trash *.jpg')
    filename = png_filenames[5]
    os.system('convert ' + filename + ' -rotate 270 ' + filename)
    filename = png_filenames[4]
    os.system('convert ' + filename + ' -rotate 90 ' + filename)

    command = 'cube2sphere --format=png --blender-path=/Applications/blender.app/Contents/MacOS/blender ' + ' '.join(png_filenames)
    os.system(command)

    os.system('convert out0001.png -flop {}.png'.format(panono_id))
    os.system('trash out0001.png')
    os.system('trash tile*.png')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python convert.py panono_url1 [panono_url2 panono_url3...]'
    for panono_url in sys.argv[1:]:
        panono_id = re.match(r"https://www.panono.com/p/(\w+)", panono_url).group(1)
        convert(panono_id)
