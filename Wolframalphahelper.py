import numpy
import wolframalpha
import xml.etree.cElementTree as ET
import urllib2
import time
from random import randrange
# Written by Junlin Wang

def construct(levelmin = 1, levelmax = 7, anglemin = 20, anglemax = 90):
    root = ET.Element("root")
    collect = {}
    a = open('lengthdata.txt','w')
    for level in range(levelmin, levelmax + 1):
        for angle in range(anglemin, anglemax + 1):
            print angle
            segmentLength = 2.0 * numpy.cos(angle/180.0 * numpy.pi) + 2
            base = 4.0/segmentLength
            length = base**level
            ininch = length * 6

            appid = 'E929YY-HRP2LA22AV'
            client = wolframalpha.Client(appid)
            try:
                res = client.query('how long is %0.2f' % (ininch) + ' inches')
            except urllib2.HTTPError:
                tree = ET.ElementTree(root)
                tree.write("learninglength.xml")
                a.write('stop at level: %d, angle: %d' %(level, angle))
            text = ''
            for pod in res.pods:
                if pod.text[1] == "~":
                    new = pod.text.encode('ascii', 'replace')
                    new = new.replace('?', '*')
                    text = text + new + ' '


            key = ET.SubElement(root, "finches%0.2f" % (ininch))
            key.text = text



            collect['%0.2finches'%(ininch)] = text
            '''
            a.write('')
            a.write(text)
            a.write('\n')
            '''


    tree = ET.ElementTree(root)
    tree.write("learninglength.xml")
    return collect

construct(1, 7, 10, 90)

def find(level, angle):
    pass




