import xml.etree.ElementTree as etree

class FontData(object):
	    """Holds variables to convert em to real units"""
    def __init__(self, fontname='arial.svg'):
    	tree = et.parse(fontname)
        data = tree.find('.//font-face')
        self.name = data.attrib.get('font-family') #name of font
        self.em = float(data.attrib.get('units-per-em')) #max units per character
        self.cap = float(data.attrib.get('cap-height')) #height of capital letters
        self.ascent = float(data.attrib.get('ascent')) #full height above line
        self.descent = float(data.attrib.get('descent')) #amount drop below line
    def SetUnits(self, mm):
        self.mm_height = mm #total height in mm
        self.mm_per_em = mm / self.em #number of mm per each em unit
        self.mm_cap = self.mm_per_em * self.cap
        self.mm_ascent = self.mm_per_em * self.ascent
        self.mm_descent = self.mm_per_em * self.descent

class WordSize(object):
	def __init__(self, textstring):
		self.textstring = textstring
	def SetText(self, textstring):
		self.textstring = textstring
	def GetStartEm(self):
		char_pos = []
		itertext = iter(self.textstring)
		first_char = next(itertext)
		last_char = first_char
		char_pos.append(0)
		char_advance = 0.0
		for char in itertext:
    		char_data = tree.find('.//glyph[@glyph-name="'+last_char+'"]')
    		char_width = float(char_data.attrib.get('horiz-adv-x'))
    		kern_val = tree.find('.//hkern[@u1="'+last_char+'"][@u2="'+char+'"]') #get kerning data
    		if kern_val is not None:
        		char_width -= float((kern_val.attrib.get('k')))
    		char_advance += char_width
    		char_pos.append(char_advance)
    		last_char = char
    	self.StartEm = char_pos
    	self.WidthEm = full_width


