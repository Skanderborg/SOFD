from model.position import Position
from model.person import Person
import xml.etree.ElementTree as ET


class Employee_service:
    def __init__(self, xmlpath):
        self.tree = ET.parse(xmlpath)
        self.root = self.tree.getroot()
