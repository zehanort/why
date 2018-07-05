from subprocess import check_output as run
from os import listdir

################################################################
# NOTE: The strings list below can be modified to one's liking #
################################################################

strings = ["ERROR", "EXIT STATUS", "DIAGNOSTICS"]

mandirs_ = run(['manpath'])[:-1].split(':')
mandirs = [(m + '/man1/') for m in mandirs_ if (run(['file', m]).split(':')[1][1:-1] == "directory")]

############################
# some useful dictionaries #
############################

# a dictionary to hold all manpages (as all_progs) per manpath
x = [[] for i in xrange(len(mandirs))]
all_progs = dict(zip(mandirs, x))

for mandir in mandirs:
	print "[!] Discarding all irelevant files in directory : %s" % mandir
	print "[!] This may take a while..."

	progs = all_progs[mandir]

	for filename in listdir(mandir):

		# we are interested in man pages (gzipped) only

		filetype = run(['file', mandir+filename])
		if "gzip compressed data" not in filetype:
			continue

		progs.append(filename)

	print "[!] Done."

# we now need to create 2 dictionaries, based on the strings we are
# looking for inside the manpages

# first dict: counters for the times we found each string in a manpage

counters_for_strings = [0 for i in xrange(len(strings))]
counters = dict(zip(strings, counters_for_strings))

# second dict: the names of the files where we will log our results (per string)

outfiles_names_for_strings = [("/tmp/%s.txt" % ''.join(i.lower().split(' '))) for i in strings]
outfiles_names = dict(zip(strings, outfiles_names_for_strings))

#########################
# some useful functions #
#########################

def open_outfiles(files, mode):
	strings = [key for key in files]
	outfiles = []

	for string in strings:
		outfiles.append(open(files[string], mode))

	return dict(zip(strings, outfiles))

def close_outfiles(open_files):

	for i in open_files:
		open_files[i].close()

	return

##########################################################
# SOME USEFUL FUNCTIONS TO HANDLE GROFF FILES (MANPAGES) #
##########################################################

# true if the line is a GROFF header (.SH), false otherwise
# if a header string is specified, return true if the line
# is a header AND that header is the one specified
def lineIsHeader(line, *args):
	if not line:
		return True 		# semantically dirty ( ? ), but works
	elif len(args) == 0:
		return line.startswith(".SH") or line.startswith(".Sh")
	else:
		return line.startswith(".SH %s" % args[0]) or line.startswith(".SH \"%s\"" % args[0]) or line.startswith(".Sh %s" % args[0]) or line.startswith(".Sh \"%s\"" % args[0])
