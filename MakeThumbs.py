import os, sys, shutil, time
from wand.image import Image
from multiprocessing import Pool


XLname="SYNOPHOTO:THUMB_XL.jpg"
XLsize=1280
Lname="SYNOPHOTO:THUMB_L.jpg"
Lsize=800
Bname="SYNOPHOTO:THUMB_B.jpg"
Bsize=640
Mname="SYNOPHOTO:THUMB_M.jpg"
Msize=320
Sname="SYNOPHOTO:THUMB_S.jpg"
Ssize=160
imgtypes = ['.jpg', '.jpeg', '.png', '.tif', '.bmp']

def eaDir_exists(directory):
	if directory == '.':
		directory = os.getcwd()
	if '@eaDir' in directory: return None
	subfolders = os.listdir(directory)
	if os.path.isdir(directory + '/@eaDir'):
		return True
	else:
		return False

def thumbs_already_created(directory):
	if directory == '.':
		directory = os.getcwd()
	if eaDir_exists(directory):
		 return os.listdir(directory + '/@eaDir')
	else:
		return []

def thumbs_to_make(directory):
	if directory == '.':
		directory = os.getcwd()
	to_make = []
	made = thumbs_already_created(directory)
	for f in os.listdir(directory):
		if (f[-4:] in imgtypes or f[-5:] in imgtypes) and not f in made:
			to_make.append(f)
	return to_make

def clean_up(directory):
	if directory == '.':
		directory = os.getcwd()
	made = thumbs_already_created(directory)
	files = os.listdir(directory)
	thumbs_to_remove = []
	for f in made:
		if not f in files:
			shutil.rmtree(directory + '/@eaDir/' + f)

def write_thumb(params):
	file_name, directory = params
	img = Image(filename=directory + '/' + file_name)
	if not os.path.isdir(directory + '/@eaDir/' + file_name):
		os.mkdir(directory + '/@eaDir/' + file_name)
	img.resize(XLsize, XLsize)
	img.save(filename=directory + '/@eaDir/' + file_name + '/' + XLname)
	img.resize(Lsize, Lsize)
	img.save(filename=directory + '/@eaDir/' + file_name + '/' + Lname)
	img.resize(Bsize, Bsize)
	img.save(filename=directory + '/@eaDir/' + file_name + '/' + Bname)
	img.resize(Msize, Msize)
	img.save(filename=directory + '/@eaDir/' + file_name + '/' + Mname)
	img.resize(Ssize, Ssize)
	img.save(filename=directory + '/@eaDir/' + file_name + '/' + Sname)

if __name__ == "__main__":
	os.chdir(sys.argv[1])
	original_directory = os.getcwd()
	job_list = list(os.walk(original_directory))
	pool = Pool(processes=2)
	for job in job_list:
		cwd = job[0]
		os.chdir(cwd)
		if '@eaDir' in cwd:
			continue
		# print "Working against: " + cwd
		to_do = thumbs_to_make(cwd)
		for i, x in enumerate(to_do[:]):
			to_do[i] = (x, cwd)
		if not eaDir_exists(cwd):
			os.mkdir(cwd + '/@eaDir')
		pool.map(write_thumb, to_do)
		clean_up(cwd)
