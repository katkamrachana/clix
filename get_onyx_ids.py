'''
Input: Location of folder containing qti .zip files.
Output: QuestionName -- OnyxID
'''


import os
import zipfile
fp = raw_input('Enter qti zip files location\t:')
qti_path = fp
for a,b,c in os.walk(qti_path):
	for ee in c:
		if ee.endswith('.zip'):
			print ee , " -- ",
			n = os.path.join(a,ee)
			zip_obj = zipfile.ZipFile(n)
			zipped_files = zip_obj.namelist()
			for each_file in zipped_files:
				if each_file.startswith('id'):
					print each_file.split('.')[0], "\n"
