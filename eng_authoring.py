'''
Please find updated script here: https://github.com/katkamrachana/clix
'''

import xlrd
import  mimetypes
import os
from html import HTML
import eng_master_doc

workbook = xlrd.open_workbook('../U1 L1 Activities Template.xlsx')
print "\n Total sheets: ", workbook.nsheets
doc_defination = '<?xml version="1.0" encoding="utf-8" standalone="no"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'


def init_html():
	'''
	<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
	'''

	html_ele = HTML()
	html_ele_dct = {
	       "xmlns" : "http://www.w3.org/1999/xhtml",
	       "xmlns:epub" : "http://www.idpf.org/2007/ops"
	}
	html_ele.html(**html_ele_dct)	
	return html_ele

def head_block():
	'''
	<head>
		<meta content="IE=edge" http-equiv="X-UA-Compatible" />
		<title>CLIx</title>
		<link href="../Styles/style.css" rel="stylesheet" type="text/css" />
	</head>
	'''
	hd = HTML('head')
	head_ele_dct = {
	       'http-equiv': 'X-UA-Compatible',
	       'content': 'IE=edge'
	}
	hd.meta(**head_ele_dct)	
	hd.title('CLIx')
	hd.link(href="../Styles/style.css", rel="stylesheet", type="text/css")
	# print hd
	# head_block = '<head><meta content="IE=edge" http-equiv="X-UA-Compatible" /><title>CLIx</title><link href="../Styles/style.css" rel="stylesheet" type="text/css" /></head>'
	# return head_block
	return hd

def fill_dict(sheet_obj, row_index):
	each_sheet_on_screen_data_keys = ['Image', 'Video', 'Text', 'Word cloud', 'Audio Track', 'Subtitles (Audio)', 'Subtitles (Video)']
	key_list = sheet_obj.col_values(1, row_index, row_index + 7)
	fval_list = sheet_obj.col_values(2, row_index, row_index + 7)
	each_sheet_on_screen_data = {}
	try:
		each_sheet_on_screen_data = dict((k, str(v)) for k, v in zip(key_list, fval_list) if v and unicode(k) in each_sheet_on_screen_data_keys)
	except UnicodeEncodeError as e:
		pass
	except Exception as fill_dict_err:
		print "\n Error occurred in fill_dict!!! ", fill_dict_err
		pass
	return each_sheet_on_screen_data


def createHTMLHeaderElement(activity_num, activity_name, body_DOM):
	'''
	<header class="group span_10_of_12">
	<small>this is small header text, for the activity number or lesson title</small>

	<h1>Heading 1</h1>
	<hr/>
	<p>Some subtitle text can go here. </p>
	<hr/>
	</header>
	'''

	header1 = body_DOM.header(klass="group span_10_of_12")
	header1.small("CONVERSATIONAL ENGLISH")
	header1.h1('Activity ' + activity_num + ' - ' +activity_name)
	header1.hr
	return body_DOM

def getVideoRowHTML(vfn, DOM_obj):
    for each_video_file in vfn:

        article_ele = DOM_obj.article(klass='group')
        vid_ele = {
            "id":each_video_file,"src":"../Video/"+each_video_file, "alt":"", \
            "klass":"video-js vis-skin-colors-clix vjs-big-play-centered", \
            "controls":"controls", "preload":"auto", "width":"480", "height":"360", \
            "data-setup":'{}'
        }
        vid_ele = article_ele.video(**vid_ele)
        subtitles_file_name_list = each_video_file.split('.')[:-1]
        subtitles_file_name = '.'.join(subtitles_file_name_list)
        vid_ele.source(src="../Video/"+ each_video_file, type='video/mp4; codecs="avc1.42E01E, mp4a.40.2"')
        vid_ele.track(kind="captions", src="../Video/"+subtitles_file_name+"_en.vtt", srclang="en", label="English", type="text/vtt")

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
			'''
				<video id="[filename without .mp4 here]" class="video-js vis-skin-colors-clix\
				vjs-big-play-centered" controls="controls" preload="auto" width="480" height="360" data-setup='{}'>
				<source src="../Video/[filename here]" type='video/mp4; codecs="avc1.42E01E, mp4a.40.2"'/>
				<track kind="captions" src="../Video/[filename without .mp4 here]_en.vtt" \
				srclang="en" label="English" type="text/vtt"/>
				<track kind="captions" src="../Video/[filename without .mp4 here]_hi.vtt" \
				srclang="hi" label="Hindi" type="text/vtt"/>
				<track kind="captions" src="../Video/[filename without .mp4 here]_te.vtt" \
				srclang="te" label="Telegu" type="text/vtt"/>
				<p class="vjs-no-js">To view this video please enable JavaScript, and \
				consider upgrading to a web browser that <a \ 
				href="http://videojs.com/html5-video-support/" \
				target="_blank">supports HTML5 video</a></p>
				</video>
			'''
			sheet_videos_path = 'videos/' + each_sheet.name
			if os.path.exists(sheet_videos_path):
				video_filelist = os.listdir(sheet_videos_path)
				vid_files = []
				for each_video in video_filelist:
					try:
						valid_video = mimetypes.guess_type(sheet_videos_path + '/' +each_video)
					except Exception as valid_video_err:
						valid_video = None
						# print valid_video_err
					if valid_video and valid_video[0] and 'video' in valid_video[0]:
						vid_files.append(each_video)
				if vid_files:
					getVideoRowHTML(vid_files, body_DOM)
		'''
		if ele_type == "Word cloud":
			pass
		'''
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
	# print "\n body_DOM == ", body_DOM
	return body_DOM
try:
	for each_sheet in workbook.sheets():
		# print " || No. of rows found: ", each_sheet.nrows
		if "Activity" in each_sheet.name:
			print "\n Processing: ", each_sheet.name,
			html_content = header_ele = None
			body_html = HTML('body')
			for each_row in xrange(each_sheet.nrows):
				val_list = each_sheet.row_values(each_row)
				val_list = map(unicode,val_list)
				# print "\n val list = ", val_list
				if "Activity Number" in val_list:
					try:
						activity_num = val_list[1]
					except IndexError as name_not_found:
						print "\n Error !! ", name_not_found
						pass

				if "Activity Name" in val_list:
					try:
						activity_name = val_list[2]
					except IndexError as name_not_found:
						print "\n Error !! ", name_not_found
						pass
				unplatform_row_exists = any('UnPlatform' in each_row for each_row in val_list)
				# print "\n unplatform_row_exists", unplatform_row_exists

				# if "On Screen / UnPlatform " in val_list:
				if unplatform_row_exists:
					dict_obj = fill_dict(each_sheet, each_row)
					# print "\n final dict = ", dict_obj
					if dict_obj:
						if activity_num and activity_name:
							header_ele = createHTMLHeaderElement(activity_num, activity_name, body_html)
						main_tag_in_body = body_html.main(klass="group span_10_of_12")
						html_content = parseOnScreenEle(dict_obj, main_tag_in_body)
						continue

			# print "\n html_content: "
			# if (html_content):
			# 	print "Yes"
			# else:
			# 	print "No"
			# print "\n h1_ele: ", html_content
			# print "\n h2_ele: ", header_ele
			if body_html:
				w = open(str(each_sheet.name)+'.html', 'w+')
				w.write(doc_defination + str(init_html())+str(head_block())+str(body_html)+"</html>")
				w.close()
				# print "\n sheet_obj : ", each_sheet.name
				print "\n Created file: ", each_sheet.name
				print "*"*80
		else:
			print "\n Skipping: ", each_sheet.name
			print "*"*80

except Exception as e:
	print "\n Error occurred!!!  ", e