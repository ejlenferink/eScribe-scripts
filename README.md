# eScribe Scripts

## Summary

These scripts aid the creation of ElectronScribe pattern files for nanoelectronic devices based on two-dimensional semiconductors.

## Make Grid

This script creates a pattern file (grid.ebl) containing a two-dimensional grid of alignment marks (crosses) along with letter pairs (e.g. CF) which denote the row and column in the grid. The various size parameters can be edited in the script.

## Write Alignment Marks

This script is run after a sample is identified and patterned with rough alignment markers which are assumed to form a square around the sample in addition to contact pads. The user inputs the sample name and the x and y offsets in um of the sample in respect to the center of the alignment marks. The script saves the x and y offsets in a text file (vector.txt) and creates a pattern file for fine alignment marks around the sample. Additionally the script creates two template files for the contacts and etching patterns centered on the sample position. These contain alignment windows for the rough and fine alignment marks. The contact template file also contains electrical leads which extend from the contact pads to the center of the sample.

With the "-E" argument, editing mode can be turned on. In this mode, the x and y offsets of the sample do not need to be specified each time the script is run as they will be simply loaded from the exisiting file.

## Write Contacts / Etch

This script takes the shapes in existing contacts and etching pattern files and merges them using x and y offsets as well as a rotation specified by the user with the template files created previously. As with the previous script, the offset values as well as the rotation is stored in a text file (vector2.txt). The contacts pattern file should only contain one level for the shapes actually contacting the sample. The etching pattern can contain as many layers as needed. The merged patterns can then be edited by the user to connect the sample leads to the contact pads and delete any unnecessary shapes.

With the "-c" and "-e" arguments, the file names for the contacts and etching pattern files can be specified (do not enter ".ebl" file extension). Otherwise, the script simply looks for two files: "contacts.ebl" and "etch.ebl"
With the "-E" argument, editing mode can be turned on. In this mode, the x and y offsets of the sample do not need to be specified each time the script is run as they will be simply loaded from the existing file.
