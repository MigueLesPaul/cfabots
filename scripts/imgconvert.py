#!/usr/bin/env python

import os
from os.path import basename
from glob import glob
import re
from imageio import imread,mimwrite,mimsave,get_writer
from imageio_ffmpeg import write_frames


def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def read_images(flist):
    imglist=[]
    for f in flist:
        imglist.append(imread(f))
    return imglist


def pngs2mp4(fileexpr, imagesize='640:480'):
    """ 
    input: globpath to files  /path/wrfout_sfc_*
    output: full path to mp4
    """
    newfilename = fileexpr[:-1]

    filelist = natural_sort(glob(fileexpr+'.png'))

    mimsave(newfilename+".gif",read_images(filelist))
    
    vidwriter = get_writer(newfilename+".mp4",format='FFMPEG',fps=1,codec='h264',bitrate='20k')

    for img in read_images(filelist):
        print(img.shape)
        vidwriter.append_data(img)
    vidwriter.close()


    

#    cmd1 = """cat {}|/usr/bin/ffmpeg -y -framerate 1 -i -  -vcodec libvpx -b:v 100k -s 640x480  "{}.webm" """.format(
#    " ".join(filelist), newfilename)


    # cmd1 = """/usr/bin/ffmpeg -y  -framerate 1/2.5 -i {}  -vcodec libvpx -b:v 100k -s 640x480  -r 25 -pix_fmt yuv420p "{}.webm" """.format(
    # " ".join(filelist), newfilename)



    # cmd2 = """/usr/bin/ffmpeg -y  -i {}.webm  -b:v 8k -s 640x480 "{}.gif" """.format(
        # fileexpr, newfilename)

#    print(cmd1)
#    os.system(cmd1)
    # os.system(cmd2)
    return """{}.webm""".format(newfilename)


if __name__ == "__main__":
    # pngs2mp4(
    # "/home/miguel/Projects/cfabots/images/wrfout_2020082800/SFC/RAIN/wrfout_2020082800_d3_rain_sfc_*",
    # imagesize='640x480')

    vidfile = pngs2mp4(
        "/home/miguel/Data/SispiImages/wrfout_2020082800/SFC/RAIN/wrfout_2020082800_d3_rain_sfc_*",
        imagesize='640:480')

    # pngs2mp4('/home/miguel/Pictures/.webcam/20200827/shot*')