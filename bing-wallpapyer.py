#! /usr/bin/python3
# Author: Maximilian Muth <mail@maxi-muth.de>
# https://github.com/mammuth/bing-wallpaper
# Version: 1.0
# License: GPL-2.0
# Description: Downloads the Bing picture of the Day and sets it as wallpaper (Linux / Windows).

import datetime
from urllib.request import urlopen, urlretrieve
from xml.dom import minidom
import os
from win32api import GetSystemMetrics
import ctypes
from PIL import Image

#Variables:
idx = '0' #defines the day of the picture: 0 = today, 1 = yesterday, ... 20.
saveDir = 'D:\\bing-wallpaper\images\\' #in Windows you might put two \\ at the end
tempPath = 'D:\\bing-wallpaper\\images\\temp\\tempWallpaper.bmp' # for .bmp temp file
operatingSystem = 'windows' #windows or linux (gnome)

#Methods for setting a picture as Wallpaper
def setWindowsWallpaper(picPath):
    # convert to bmp file
    Image.open(picPath).save(tempPath)

    SPI_SETDESKWALLPAPER  = 20
    SPIF_UPDATEINIFILE    = 1 
    SPIF_SENDWININICHANGE = 2
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, tempPath, SPIF_UPDATEINIFILE|SPIF_SENDWININICHANGE)

    # cmd = 'REG ADD \"HKCU\Control Panel\Desktop\" /v Wallpaper /t REG_SZ /d \"%s\" /f' %picPath 
    # os.system(cmd)
    # os.system('rundll32.exe user32.dll, UpdatePerUserSystemParameters')
    # print(cmd)
    return


def setGnomeWallpaper(picPath):
    os.system('gsettings set org.gnome.desktop.background picture-uri file://' + picPath)
    return


#Getting the XML File
usock = urlopen(
    'http://www.bing.com/HPImageArchive.aspx?format=xml&idx=' + idx + '&n=1&mkt=zh-cn') #ru-RU, because they always have 1920x1200 resolution pictures
xmldoc = minidom.parse(usock)
#Parsing the XML File
for element in xmldoc.getElementsByTagName('url'):
    url = 'http://www.bing.com' + element.firstChild.nodeValue

    #Get Current Date as fileName for the downloaded Picture
    now = datetime.datetime.now()

    # Get monitor resolution
    resolution = str(GetSystemMetrics(0)) + 'x' + str(GetSystemMetrics(1))

    picPath = saveDir +  'bing_wp_' + resolution + '_' + now.strftime('%d-%m-%Y') + '.jpg'

    # if os.path.isfile( picPath )

    #Download and Save the Picture
    #Get a higher resolution by replacing the file name
    urlretrieve(url.replace('_1366x768', '_'+resolution), picPath)

    # #Set Wallpaper:
    if operatingSystem == 'windows':
        setWindowsWallpaper(picPath)
    elif operatingSystem == 'linux' or operatingSystem == 'gnome':
        setGnomeWallpaper(picPath)
