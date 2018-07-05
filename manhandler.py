import os, gzip
from shutil import copyfile

path = "/usr/share/man/"								# path where all manuals for all commands are (in Unix)

error_strings = [
	("exit status", "exitstatus"),
	("error level", "errorlevel"),
	("exit code", "exitcode"),
	("error code", "errorcode")	
]

man_dir_list = ["man1/", "man2/", "man3/", "man4/", "man5/", "man6/", "man7/", "man8/"]	# list of all subdirectories to be searched

for man in man_dir_list:								# for every subdirectory
	for file in os.listdir(path+man) :					# and for every file in that subdirectory
		filepath = path+man+file						# store the filepath for later
		fopen = gzip.open(path+man+file, 'rb')			# and unzip the file (manual)
		f = fopen.read()								# and read it
		f_lower = f.lower()								# turn all characters to lowercase
		for er_string in error_strings :				# search for every possible error string in the manual you just opened
			f_lower = f_lower.replace( *er_string )
			if er_string[1] in f_lower :				# if you found some error code documentation
				name = file.split('.')[0]				# store the name of the file (the command)
				which = os.popen( "which %s" % name).read().strip()	# check if this is an actual command
				if which :
					os.popen("man %s > /home/sotiris/projects/why/mans_with_error_code/%s--%s.txt" % (name, name, er_string[0]))
					print filepath,					# print the filepath
					print er_string[0]				# and the exact way errors are documented ("error code", "error status", etc)
					fopen.close()
			break