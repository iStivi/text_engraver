import xml.etree.ElementTree as etree
import re

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

def GetMoves(character, fontname='arial.svg'):
	tree = et.parse(fontname)
	glyph_data = tree.find('.//glyph[@glyph-name="'+character+'"]')
	glyph_path = glyph_data.attrib.get('d')	#get the glyph svg format path
	move_split = re.finditer("[A-Za-z]",glyph_path)	#get position of each move code letter
	point_1 = next(move_split)
	last_point = point_1.start()
	move_list = []
	for match in move_split:
		move_list.append(glyph_path[last_point:match.start()].strip())
		last_point = match.start()
	move_list.append(glyph_path[last-point:])
	return move_list
	
def getCutPath(path_list):
	#incomplete at the moment - still need to add steps for curve cuts
	cut_paths = []
	move_start = [0.0,0.0] #make default start in case first move is not "M" for some reason
	for movement in path_list:
		move_points = movement[1:].split(' ')
		print(movement[0],move_points)
		#upper case letters are absolute moves, lower case relative moves
		if movement[0].lower() == 'm':
			if movement[0].isupper():
				x_point = float(move_points[0])
				y_point = float(move_points[1])
				cut_paths.append(['G0',x_point,y_point])
			if movement[0].islower():
				x_point = float(move_points[0])+move_start[0]
				y_point = float(move_points[1])+move_start[1]
				cut_paths.append(['G0',x_point,y_point])
			move_start = [x_point,y_point]
		elif movement[0].lower() == 'l':
			if movement[0].isupper():
				x_point = float(move_points[0])
				y_point = float(move_points[1])
				cut_paths.append(['G1',x_point,y_point])
			if movement[0].islower():    
				x_point = float(move_points[0])+move_start[0]
				y_point = float(move_points[1])+move_start[1] 
				cut_paths.append(['G1',x_point,y_point])
			move_start = [x_point,y_point]
		elif movement[0].lower() == 'v':
			if movement[0].isupper():
				x_point = move_start[0]
				y_point = float(move_points[0])
				cut_paths.append(['G1',x_point,y_point])
			if movement[0].islower():
				x_point = move_start[0]
				y_point = float(move_points[0])+move_start[1] 
				cut_paths.append(['G1',x_point,y_point])
			move_start = [x_point,y_point]
		elif movement[0].lower() == 'h':
			if movement[0].isupper():
				x_point = float(move_points[0])
				y_point = move_start[1] 
				cut_paths.append(['G1',x_point,y_point])
			if movement[0].islower():
				x_point = float(move_points[0])+move_start[0]
				y_point = move_start[1] 
				cut_paths.append(['G1',x_point,y_point])
			move_start = [x_point,y_point]
		elif movement[0].lower() == 'q':
			#only start and end points at the moment, will fill out curve later
			if movement[0].isupper():
				x_point = float(move_points[2])
				y_point = float(move_points[3])
				x_control = float(move_points[0])
				y_control = float(move_points[1])
				cut_paths.append([movement[0],x_point,y_point,x_control,y_control])
			if movement[0].islower():
				x_point = float(move_points[2])+move_start[0]
				y_point = float(move_points[3])+move_start[1] 
				x_control = float(move_points[0])+move_start[0]
				y_control = float(move_points[1])+move_start[1]  
				cut_paths.append([movement[0],x_point,y_point,x_control,y_control])
			move_start = [x_point,y_point]
			control_start = [x_control,y_control]
		elif movement[0].lower() == 't':
			if movement[0].isupper():
				x_point = float(move_points[0])
				y_point = float(move_points[1])
				#taking a guess at how reflected control points work for now
				x_control = move_start[0] + (move_start[0] - control_start[0])
				y_control = move_start[1] + (move_start[1] - control_start[1])
				cut_paths.append([movement[0],x_point,y_point,x_control,y_control])
			#only start and end points at the moment, will fill out curve later
			if movement[0].islower():
				x_point = float(move_points[0])+move_start[0]
				y_point = float(move_points[1])+move_start[1] 
				#taking a guess at how reflected control points work for now
				x_control = move_start[0] + (move_start[0] - control_start[0])
				y_control = move_start[1] + (move_start[1] - control_start[1])
				cut_paths.append([movement[0],x_point,y_point,x_control,y_control])
			move_start = [x_point,y_point]
			control_start = [x_control,y_control]
		elif movement[0].lower() == 'z':
			cut_paths.append(["z"])
		else:
			cut_paths.append('unknown')
	return cut_paths
	
