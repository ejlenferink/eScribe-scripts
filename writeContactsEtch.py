#!/usr/bin/python

# Write contacts and etching pattern file from template files
# Use "-c" and "-e" arguments to specify names of contacts and etching pattern files to copy layers from
# Use "-E" argument to enable editing mode wherein the x and y center values are loaded from the existing vector file

import re, sys,math

contactsL1_fName = "contacts"
etchLs_fName = "etch"

re_line = "\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)"
re_circ = "\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)"
re_tri = "\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)"
re_poly = "\s+(-?[\d.]+)\s+(-?[\d.]+)"

def rotate(x, y, theta):
	return x*math.cos(theta)+y*math.sin(theta),-x*math.sin(theta)+y*math.cos(theta)

def rotateLine(line, xc, yc, theta):
	# Rotate shape
	if(re.match(re_tri,line)):
		repeats, rate, linewidth, x1, y1, x2, y2, x3, y3 = [float(x) for x in (re.match(re_tri,line).groups())]
		x1, y1 = rotate(x1, y1, theta)
		x2, y2 = rotate(x2, y2, theta)
		x3, y3 = rotate(x3, y3, theta)
		line = "%.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f"%(repeats,rate,linewidth,x1+xc,y1+yc,x2+xc,y2+yc,x3+xc,y3+yc)
	elif(re.match(re_line,line)):
		repeats, rate, linewidth, x1, y1, x2, y2 = [float(x) for x in (re.match(re_line,line).groups())]
		x1, y1 = rotate(x1, y1, theta)
		x2, y2 = rotate(x2, y2, theta)
		line = "%.3f %.3f %.3f %.3f %.3f %.3f %.3f"%(repeats,rate,linewidth,x1+xc,y1+yc,x2+xc,y2+yc)
	elif(re.match(re_circ,line)):
		repeats, rate, linewidth, x, y, r = [float(x) for x in (re.match(re_circ,line).groups())]
		x, y = rotate(x, y, theta)
		line = "%.3f %.3f %.3f %.3f %.3f %.3f"%(repeats,rate,linewidth,x+xc,y+yc,r)
	elif(re.match(re_poly,line)):
		x1, y1 = [float(x) for x in (re.match(re_poly,line).groups())]
		x1, y1 = rotate(x1, y1, theta)
		line = "%.3f %.3f"%(x1+xc,y1+yc)
	return line

def main(argv):
	# User inputs sample name
	sName = raw_input("Enter sample name: ")

	# See if user inputs contact or etch file names
	global contactsL1_fName, etchLs_fName
	if '-c' in argv:
		contactsL1_fName = argv[argv.index("-c")+1]
	if '-e' in argv:
		etchLs_fName = argv[argv.index("-e")+1]

	# User inputs x and y centers or they are loaded from the vector file for editing mode

	if '-E' in argv:
		xc, yc, theta =  [float(x) for x in re.match("(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)",open(sName+"/"+sName+"-vector2.txt",'r').readline()).groups()]
	else:
		xc = float(raw_input("Enter x: "))
		yc = float(raw_input("Enter y: "))
		theta = float(raw_input("Enter angle (degrees): "))

		f_v2 = open(sName+"/"+sName+"-vector2.txt",'w')
		f_v2.write("%f\t%f\t%f"%(xc,yc,theta))
		theta *= math.pi/180.

	# Write contacts pattern file
	lines_contactsTemp = open(sName+"/"+sName+"-contactsTemp.ebl",'r').readlines()
	f_contacts = open(sName+"/"+sName+"-contacts.ebl",'w')
	lines_contactsL1 = open(contactsL1_fName+".ebl",'r').readlines()

	for line in lines_contactsTemp[:4]:
		f_contacts.write(line)

	for line in lines_contactsL1[4:]:
		f_contacts.write(rotateLine(line, xc, yc, theta))

	for line in lines_contactsTemp[4:]:
		f_contacts.write(line)

	f_contacts.close()

	# Write etching pattern file
	lines_etchTemp = open(sName+"/"+sName+"-etchTemp.ebl",'r').readlines()
	f_etch = open(sName+"/"+sName+"-etch.ebl",'w')
	lines_etchLs = open(etchLs_fName+".ebl",'r').readlines()

	f_etch.write(lines_etchLs[0])

	for line in lines_etchTemp[1:]:
		f_etch.write(line)

	for line in lines_etchLs[4:]:
		f_etch.write(rotateLine(line, xc, yc, theta))

	f_etch.close()

if __name__ == "__main__":
	main(sys.argv[1:])

