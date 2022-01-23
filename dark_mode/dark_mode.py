#! /bin/python

# author: Heart Of Rain
# email: heartofrain@outlook.com
# github: https://github.com/heartofrain

from PIL import Image
import os
import sys
import re

# gray level of output:
min=30
max=130

# map the gray range [0,255] to gray range [min,max]
def transform(x):
    return int( ((max-min)-x/255*(max-min))+min )

if __name__=="__main__":
    # todo: arg parse
    # todo: arg-pagerange
    pdf_input_name=sys.argv[1]
    # todo: check pdf_input_name

    # get info
    info = os.popen('mutool info {}'.format(pdf_input_name)).read()
    pages = int(re.search('Pages:\s*([0-9]*)',info).group(1))
    
    # pdf -> images
    os.system('mutool draw -r 600 -o {}_%05d.png {}'.format(
        pdf_input_name.replace('.pdf',''),pdf_input_name))
    # todo: arg-resolution

    # process images
    for i in range(1,pages+1):
        img_in=Image.open('{}_{:05}.png'.format(
            pdf_input_name.replace('.pdf',''),i)).convert('L')
        img_out = img_in.point(transform)
        img_out.save('{}_out_{:05}.png'.format(
            pdf_input_name.replace('.pdf',''),i))

    # images -> pdf
    os.system('convert {0}_out_*.png {0}_output.pdf'.format(
        pdf_input_name.replace('.pdf','')))

    # delete images
    os.system('rm {}_*.png'.format(
        pdf_input_name.replace('.pdf','')))
