__author__ = 'Wangj1'
# Written by Junlin Wang
import numpy
import xml.etree.cElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
def gettree():
    dict = {}
    for event, elem in ET.iterparse('learninglength.xml'):
        dict['%s' % (elem.tag)] = elem.text
    return dict






