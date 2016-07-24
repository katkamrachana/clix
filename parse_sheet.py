import xlrd
import  mimetypes
import os
from html import HTML

workbook = xlrd.open_workbook('/home/rbkatkam/Downloads/U1L2Activities Template.xlsx')
print "\n Total sheets: ", workbook.nsheets
doc_defination = '<?xml version="1.0" encoding="utf-8" standalone="no"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'


def init_html():
	html_tag = '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">'
	return html_tag

def head_block():
	'''
	<head>
		<meta content="IE=edge" http-equiv="X-UA-Compatible" />
		<title>CLIx</title>
		<link href="../Styles/style.css" rel="stylesheet" type="text/css" />
	</head>
	'''
	head_block = '<head><meta content="IE=edge" http-equiv="X-UA-Compatible" /><title>CLIx</title><link href="../Styles/style.css" rel="stylesheet" type="text/css" /></head>'
	return head_block

def fill_dict(sheet_obj, row_index):
	each_sheet_on_screen_data_keys = ['Image', 'Video', 'Text', 'Word cloud', 'Audio Track', 'Subtitles (Audio)', 'Subtitles (Video)']
	# for each_frow in xrange(row_index, sheet_obj.nrows):
	# fval_list = sheet_obj.row_values(each_frow, 1,2)
	key_list = sheet_obj.col_values(1, row_index, row_index + 7)
	fval_list = sheet_obj.col_values(2, row_index, row_index + 7)
	each_sheet_on_screen_data = {}
	# print "fval_list = ", key_list, " -- ", fval_list
	# each_sheet_on_screen_data.update()
	try:
		each_sheet_on_screen_data = dict((k, str(v)) for k, v in zip(key_list, fval_list) if v and k in each_sheet_on_screen_data_keys)
	except UnicodeEncodeError as e:
		pass
		# print sheet_obj.name
		# print e
		# print fval_list
	# each_sheet_on_screen_data = dict(zip(key_list,fval_list))
	# print "\n final dict = ", each_sheet_on_screen_data
	# print "*"*80
	# print "*"*80
	return each_sheet_on_screen_data


def createHTMLHeader1Element(activity_num, activity_name, body_DOM):
	# print activity_num
	'''
	<header class="group span_10_of_12">
	<small>this is small header text, for the activity number or lesson title</small>

	<h1>Heading 1</h1>
	<hr/>
	<p>Some subtitle text can go here. </p>
	<hr/>
	</header>
	'''
	# h = HTML()

	header1 = body_DOM.header(klass="group span_10_of_12")
	header1.small("CONVERSATIONAL ENGLISH")
	header1.h1('Activity ' + activity_num + ' - ' +activity_name)
	header1.hr
	return body_DOM

# def createHTMLHeader2Element(heading, body_DOM):
# 	# print heading

# 	# header2 = HTML('h2',heading)
# 	body_DOM.h2(heading)
# 	# header2 = HTML('h2',heading)
# 	# body_html.h2(heading)
# 	# return header2
# 	return body_DOM

def getImgRowHTML(fn, DOM_obj):

	'''
	SINGLE PHOTO
		<!-- begin 1up photo -->
		<h2>Heading 2 with a 1up photo.</h2>

		<article class="group">
			<img src="../Images/tmp_lg_0013.jpg" alt="" class="photo-01up zoom-but-lg" onclick="zoom01.showModal()"/>
		</article>
		<!-- end 1up photo -->

	2 PHOTOS IN A ROW
		<!-- begin 2up photo -->
		<h2>Heading 2. And 2 photos in a row.</h2>

		<article class="group">
			<img src="../Images/tmp_md_0001.jpg" alt="" class="photo-02up row span_6_of_12 zoom-but-md" onclick="zoom01.showModal()"/>
			<img src="../Images/tmp_md_0002.jpg" alt="" class="photo-02up row span_6_of_12 zoom-but-md" onclick="zoom01.showModal()"/>
		</article>

		<!-- end 2up photo -->	

	3 PHOTOS IN A ROW

		<!-- begin 3up photo -->
		<h2>Heading 2. And 3 photos in a row.</h2>
		<article class="group">
			<img src="../Images/tmp_sm_0003.jpg" alt="" class="photo-03up row span_4_of_12 zoom-but-sm" onclick="zoom01.showModal()"/>
			<img src="../Images/tmp_sm_0004.jpg" alt="" class="photo-03up row span_4_of_12 zoom-but-sm" onclick="zoom01.showModal()"/>
			<img src="../Images/tmp_sm_0005.jpg" alt="" class="photo-03up row span_4_of_12 zoom-but-sm" onclick="zoom01.showModal()"/>
		</article>

		<!-- end 3up photo -->

	'''
	article_start = True
	main_list = []
	mod_div = 2
	if len(fn) > 4:
		mod_div = 3
	for i in xrange(1,len(fn)+1):
		if i <= len(fn):
			if article_start:
				s_list = []
				article_start = False

			if (i > 0 and i%mod_div == 0) or i == len(fn):
				article_start = True
				s_list.append(fn[i-1])
				main_list.append(s_list)
			else:
				s_list.append(fn[i-1])

	# print "\n main_list +++ ", main_list
	class_def = None
	for each_sub_list in main_list:
		article_ele = DOM_obj.article(klass='group')
		for each_img in each_sub_list:
			if len(each_sub_list) == 1:
				class_def = "photo-01up zoom-but-lg"
			if len(each_sub_list) == 2:
				class_def = "photo-02up row span_6_of_12 zoom-but-md"
			if len(each_sub_list) == 3:
				class_def = "photo-03up row span_4_of_12 zoom-but-sm"
			article_ele.img(src="../Images/"+each_img, alt="", \
				 klass=class_def, onclick="zoom01.showModal()")

	
	# ===========================================================				
	
	# for i in xrange(len(fn)):
	# 	print i,
	# 	if article_start:
	# 		article_ele = DOM_obj.article(klass='group')
	# 		article_start = False
	# 		# print "\n article start", article_ele
	# 	if len(fn) > 4:
	# 		mod_div = 3
	# 	if i%mod_div == 0:
	# 		print "\n  article_start", i
	# 		article_start = True
	# 		# print "\n article end"

	# 	article_ele.img(src="../Images/"+fn[i], alt="", \
	# 		 klass="photo-02up row span_6_of_12 zoom-but-md", onclick="zoom01.showModal()")


	# print "\n  DOM_obj :   ", str(DOM_obj)
	# return DOM_obj


def parseOnScreenEle(dictionary_obj, body_DOM):
	for ele_type, ele_val in dictionary_obj.items():
		each_sheet_on_screen_data_keys = ['Image', 'Video', 'Text', 'Word cloud', 'Audio Track', 'Subtitles (Audio)', 'Subtitles (Video)']
		# print ele_type, " === " ,ele_val

		if ele_type == "Text":
			new_val = ele_val.replace('\n', '<br />')
			section_ele = body_DOM.section
			section_ele.p(new_val,escape=False)
		if ele_type == "Image":
			sheet_imgs_path = 'images/' + each_sheet.name
			if os.path.exists(sheet_imgs_path):
				filelist = os.listdir(sheet_imgs_path)
				img_files = []
				for eachfile in filelist:
					try:
						valid_img = mimetypes.guess_type(sheet_imgs_path + '/' +eachfile)
					except Exception as valid_img_err:
						valid_img = None
					if valid_img and 'image' in valid_img[0]:
						img_files.append(eachfile)
				# print "\n final list: ", img_files
				if img_files:
					getImgRowHTML(img_files, body_DOM)


				# print "\n\n img_files", img_files
		if ele_type == "Video":
			pass
		if ele_type == "Word cloud":
			pass
		if ele_type == "Audio Track":
			'''
			<audio width="360" height="360" controls="" class="span_12_of_12">
				<source src="../Audio/" type="audio/mpeg"/>
			</audio>
			section_ele = body_DOM.section
			section_ele.audio(new_val,escape=False)
			'''
			pass
		if ele_type == "Subtitles (Audio)":
			pass
		if ele_type == "Subtitles (Video)":
			pass
	# print "\n ", body_html
	return body_DOM

for each_sheet in workbook.sheets():
	if "Activity" in each_sheet.name:
		html_content = header_ele = None
		body_html = HTML('body')
		
		for each_row in xrange(each_sheet.nrows):
			val_list = each_sheet.row_values(each_row)
			if "Activity Number" in val_list:
				# Default Activity Name columns is 0(Zero)
				# print "\n val list = ", val_list
				try:
					activity_num = val_list[1]
				except IndexError as name_not_found:
					print "\n Error !! ", name_not_found
					pass

				# print "Activity Name== ", val_list[2]

			if "Activity Name" in val_list:
				# Default Activity Name columns is 0(Zero)
				# print "\n val list = ", val_list
				try:
					activity_name = val_list[2]
				except IndexError as name_not_found:
					print "\n Error !! ", name_not_found
					pass

				# print "Activity Name== ", val_list[2]

			if "On Screen / UnPlatform" in val_list:
				dict_obj = fill_dict(each_sheet, each_row)
				if dict_obj:
					if activity_num and activity_name:
						header_ele = createHTMLHeader1Element(activity_num, activity_name, body_html)
					main_tag_in_body = body_html.main(klass="group span_10_of_12")
					html_content = parseOnScreenEle(dict_obj, main_tag_in_body)
					# print "\n Processing: ", each_sheet.name,
					# print " || No. of rows found: ", each_sheet.nrows	
					# print "\n final dict = ", dict_obj
					continue
		# print "\n html_content: "
		# if (html_content):
		# 	print "Yes"
		# else:
		# 	print "No"
		# print "\n h1_ele: ", h1_ele
		# print "\n h2_ele: ", h2_ele
		if html_content and header_ele:
			# print "\n body_html = ", body_html
			# global doc_defination
			w = open(str(each_sheet.name)+'.html', 'w+')
			w.write(doc_defination + str(init_html())+str(head_block())+str(body_html)+"</html>")
			# w.write(doc_defination + str(init_html(1))+str(head_block())+str(h1_ele)+ str(h2_ele)+ str(html_content)+"</html>")
			w.close()
			# print "\n sheet_obj : ", each_sheet.name
			# print "\n Created file: ", each_sheet.name
			print "*"*80
