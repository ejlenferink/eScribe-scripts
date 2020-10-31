#!/usr/bin/python

# Make grid of letters and alignment mark crosses

import sys

# Number of columns (x) and rows (y) of letters plus their spacings and height in um
Nx = 5
Ny = 5
ax = 200.0
ay = 200.0
height = 20.0

# Whether to also have a grid of crosses, the crosses per row/column, and their size parameters
crosses = True
nx = 2
ny = 2
l = 10.0
w = 2.0

# Define some useful things
Dx = (Nx-1)*ax
Dy = (Ny-1)*ay
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
preambleString = "Number of Levels: %d\r\nGrid Parameters {xmin, ymin, xmax, ymax, xtic, ytic}\r\n-20 -15 20 15 1 1\r\n"
levelString = "Level: %d\r\n"
textString = "TEXT\r\n{Repeats, rate, u, t, height, rotation, Font, Text}\r\n 1 1.000 %3.3f %3.3f %3.3f 0.000\r\nLucida Console\r\n%s\r\n\r\n"
lineString = "Line\r\n{Repeats, rate, linewidth, x1, y1, x2, y2}\r\n 1 1.000 %.3f %.3f %.3f %.3f %.3f\r\n\r\n"

def main(argv):
	# Write preamble
	f = open("grid.ebl", 'w')
	f.write(preambleString%1)
	f.write(levelString%1)

	# Write grid label at top
	f.write(textString%(0,.5*Dy+50,height*1.5,"1-1"))

	# Write grid
	for i in range(Nx):
		for j in range(Ny):
			f.write(textString%(-.5*Dx+i*ax,.5*Dy-j*ay+.5*height,height,letters[j]+letters[i]))
			if(crosses):
				for ii in range(nx):
					xii = -.5*Dx+(i+ii/(nx*1.))*ax
					for jj in range(ny):
						yjj = .5*Dy-(j+jj/(nx*1.))*ay
						f.write(lineString%(w,xii-.5*l,yjj,xii+.5*l,yjj))
						f.write(lineString%(w,xii,yjj-.5*l,xii,yjj+.5*l))

	f.close()
		
if __name__ == "__main__":
	main(sys.argv[1:])

