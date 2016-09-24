import os
import csv
import json
import shutil
import zipfile

# src will be basic EB epub extraction directory structure
src = "C:\Users\/rkatkam\Documents\EB_BaseStructure"
lesson_num = raw_input("Enter Lesson Number:\t")
dest = "C:\Users\/rkatkam\Documents\Lesson"+lesson_num
zf = zipfile.ZipFile('C:\Users\/rkatkam\Documents\Lesson'+lesson_num+'.epub','w', zipfile.ZIP_DEFLATED)

def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

copyDirectory(src,dest)

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        [ziph.write(os.path.join(root, file)) for file in files]

# sheet_loc = raw_input("Enter Content csv file path:\t")

# with open(sheet_loc, 'rb') as csvfile:
with open('C:\Users\/rkatkam\Downloads\SampleEBSheet.csv', 'rb') as csvfile:
	csv_file_content = csv.DictReader(csvfile, delimiter=",")
	json_files_list = []
	for json_file in csv_file_content:
		# print json_file['Activity']
		json_files_list.append(json_file)


# Pick up each json file and update html/xhtml file from dest
for each_jf in json_files_list:
	if "Introduction" in each_jf['Activity'] and "Introduction2" not in each_jf['Activity']:
		print dest
		with open("C:\Users\/rkatkam\Documents\Lesson"+lesson_num+"\OEBPS\Text\Introduction.html", 'w+') as introf:
			print introf
			print "\nhii==="
			print introf.readlines()





zipdir(dest,zf)
zf.close()

print "\n Following new files created:\n\t1. Lesson", lesson_num, "\n\t2. Lesson", lesson_num, ".epub"
