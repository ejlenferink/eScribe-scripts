#!/usr/bin/python

# Create alignment pattern file as well as contacts and etching pattern template files. x and y centers are also stored in a vector text file
# Use "-E" argument to enable editing mode wherein the x and y center values are loaded from the existing vector file

import re, os, sys, math

# Rough (existing) alignment marker parameters
Dr = 100
Lr = 10

# Fine aligment marker size parameters
Df = 8
Lf = 2.5
Wf = .5

# Line parameters for contacts pattern template
N = 20
dTheta = 2*math.pi/N
Wl1, l1i, l1f = 1.25, 0, 26
Wl2, l2i, l2f = 3, 24, 85
Wl3, l3i, l3f = 7.5, 80, 240

# Define some useful things
preambleString = "Number of Levels: %d\r\nGrid Parameters {xmin, ymin, xmax, ymax, xtic, ytic}\r\n -20 -15 20 15 1 1\r\n"
levelString = "Level: %d\r\n"
rasterString = "Raster\r\n{Repeats, x1, y1, x2, y2}\r\n %.3f %.3f %.3f %.3f\r\n\r\n"
lineString = "Line\r\n{Repeats, rate, linewidth, xc, yc, xc, yc}\r\n 1 1.000 %.3f %.3f %.3f %.3f %.3f\r\n\r\n"

def ctanceil(x):
	return max(min(math.tan(-math.pi/2.+abs(x-math.pi)), 1), -1)

def stanceil(x):
	return ctanceil((3*math.pi/2.+x)%(2*math.pi))

def main(argv):
	# User inputs sample name
	sName = raw_input("Enter sample name: ")
	while not os.path.isdir(sName):
		sName2 = raw_input("No folder located. Enter a new sample name or press enter to create folder: ")
		if sName2 == '':
			os.mkdir(sName)
		elif not sName2 == sName:
			sName = sName2

	# User inputs x and y centers or they are loaded from the vector file for editing mode
	if '-E' in argv:
		xc, yc =  [float(x) for x in re.match("(-?[\d.]+)\s+(-?[\d.]+)", open(sName+"/"+sName+"-vector.txt", 'r').readline()).groups()]
	else:
		xc = float(raw_input("Enter x: "))
		yc = float(raw_input("Enter y: "))
		open(sName+"/"+sName+"-vector.txt", 'w').write("%.3f\t%.3f"%(xc, yc))

	# Write alignment pattern file
	f_align = open(sName+"/"+sName+"-alignMarks.ebl", 'w')
	f_align.write(preambleString%1)
	f_align.write(levelString%1)

	for i in (-1, 1):
		for j in (-1, 1):
			f_align.write(rasterString%((Dr-Lr)/2.*i-xc, (Dr-Lr)/2.*j-yc, (Dr+Lr)/2.*i-xc, (Dr+Lr)/2.*j-yc))
			f_align.write(lineString%(Wf, i*Df-.5*Lf+xc, j*Df+yc, i*Df+.5*Lf+xc, j*Df+yc))
			f_align.write(lineString%(Wf, i*Df+xc, j*Df-.5*Lf+yc, i*Df+xc, j*Df+.5*Lf+yc))

	f_align.close()

	# Write contacts pattern template file
	f_contactsTemp = open(sName+"/"+sName+"-contactsTemp.ebl", 'w')
	f_contactsTemp.write(preambleString%3)
	f_contactsTemp.write(levelString%1)

	for i in range(N/4):
		xi, yi = l1i*math.cos((i+.5)*dTheta), l1i*math.sin((i+.5)*dTheta)
		xf, yf = l1f*math.cos((i+.5)*dTheta), l1f*math.sin((i+.5)*dTheta)
		f_contactsTemp.write(lineString%(Wl1, xi, yi, xf, yf))
	for i in (-1, 1):
		for j in (-1, 1):
			f_contactsTemp.write(rasterString%((Dr-Lr)/2.*i-xc, (Dr-Lr)/2.*j-yc, (Dr+Lr)/2.*i-xc, (Dr+Lr)/2.*j-yc))
			f_contactsTemp.write(rasterString%(i*Df-.5*Lf, j*Df-.5*Lf, i*Df+.5*Lf, j*Df+.5*Lf))

	f_contactsTemp.write(levelString%2)

	for i in range(N):
		xi, yi = l2i*math.cos((i+.5)*dTheta), l2i*math.sin((i+.5)*dTheta)
		xf, yf = l2f*math.cos((i+.5)*dTheta)-xc, l2f*math.sin((i+.5)*dTheta)-yc
		f_contactsTemp.write(lineString%(Wl2, xi, yi, xf, yf))

	f_contactsTemp.write(levelString%3)

	for i in range(N):
		xi, yi = l3i*math.cos((i+.5)*dTheta)-xc, l3i*math.sin((i+.5)*dTheta)-yc
		xf, yf = l3f*ctanceil((i+.5)*dTheta)-xc, l3f*stanceil((i+.5)*dTheta)-yc
		f_contactsTemp.write(lineString%(Wl3, xi, yi, xf, yf))

	f_contactsTemp.close()

	# Write etching pattern template file
	f_etchTemp = open(sName+"/"+sName+"-etchTemp.ebl", 'w')
	f_etchTemp.write(preambleString%4)
	f_etchTemp.write(levelString%1)

	for i in (-1, 1):
		for j in (-1, 1):
			f_etchTemp.write(rasterString%((Dr-Lr)/2.*i-xc, (Dr-Lr)/2.*j-yc, (Dr+Lr)/2.*i-xc, (Dr+Lr)/2.*j-yc))
			f_etchTemp.write(rasterString%(i*Df-.5*Lf, j*Df-.5*Lf, i*Df+.5*Lf, j*Df+.5*Lf))

	f_etchTemp.close()

if __name__ == "__main__":
	main(sys.argv[1:])

