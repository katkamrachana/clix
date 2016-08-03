# -*- coding: utf-8 -*-
'''
Please find updated script here: https://github.com/katkamrachana/clix
Accept file name as arg
'''

import xlrd
import  mimetypes
import os
from html import HTML
# import eng_master_doc
# activities_template_file = raw_input('Enter Template path(.xlsx file): ')
# media_mgmt_file = raw_input('Enter Media Mgmt file path (.xlsx file): ')
# activities_template_workbook = xlrd.open_workbook(activities_template_file)
# media_mgmt_workbook = xlrd.open_workbook(activities_template_file)
activities_template_workbook = xlrd.open_workbook('../U1L01 Final Template.xlsx', encoding_override="cp1252")

media_mgmt_workbook = xlrd.open_workbook('../English_MAM_U01L01.xlsx')
# Since MAM file has ONLY 1 sheet
media_file_sheet = media_mgmt_workbook.sheet_by_index(0)			

print "\n Total Template sheets: ", activities_template_workbook.nsheets
print "\n Total Media sheets: ", media_mgmt_workbook.nsheets
if media_mgmt_workbook.nsheets == 0:
	print "\n More than 1 sheet found in Media Mgmt file.\n\n" 
	"Stopping execution."
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
	# print "\n key_list", key_list
	# print "\n fval_list",fval_list
	each_sheet_on_screen_data = {}
	try:
		each_sheet_on_screen_data = dict((k.strip(), v.strip()) for k, v in zip(key_list, fval_list) if v and v != u'None' and unicode(k).strip() in each_sheet_on_screen_data_keys)
	except UnicodeEncodeError as e:
		pass
	except Exception as fill_dict_err:
		print "\n Error occurred in fill_dict!!! ", fill_dict_err
		pass
	# print"\neach_sheet_on_screen_data: ", each_sheet_on_screen_data
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
	# header1.h1('Activity ' + activity_num + ' - ' +activity_name)
	header1.h1(activity_name)
	header1.hr
	return body_DOM

def getVideoRowHTML(vfn, DOM_obj, full_dict_obj):
    for each_video_file in vfn:

        article_ele = DOM_obj.article(klass='group')
        vid_ele = {
            "id":each_video_file,"src":"../Video/"+each_video_file, "alt":"", \
            "klass":"video-js vis-skin-colors-clix vjs-big-play-centered", \
            "controls":"controls", "preload":"auto", "width":"480", "height":"360", \
            "data-setup":'{}'
        }
        vid_ele = article_ele.video(**vid_ele)

        # print full_dict_obj
        subtitles_file_name = (full_dict_obj['Subtitles (Video)'])
        vid_ele.source(src="../Video/"+ each_video_file, type="video/mp4; codecs='avc1.42E01E, mp4a.40.2'")
        # vid_ele.track(kind="captions", src="../Video/"+subtitles_file_name+"_en.vtt", srclang="en", label="English", type="text/vtt")
        vid_ele.track(kind="captions", src="../Video/"+subtitles_file_name, srclang="en", label="English", type="text/vtt")

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


def parseOnScreenEle(dictionary_obj, body_DOM):
	for ele_type, ele_val in dictionary_obj.items():
		each_sheet_on_screen_data_keys = ['Image', 'Video', 'Text', 'Word cloud', 'Audio Track', 'Subtitles (Audio)', 'Subtitles (Video)']
		# print ele_type, " === " ,ele_val
		if ele_type.strip() == "Text" and ele_val != 'NONE':
			new_val = ele_val.replace('\n', '<br />')
			section_ele = body_DOM.section
			section_ele.p(new_val,escape=False)
		if ele_type.strip() == "Image" and ele_val != 'NONE':
			img_files = []
			img_files = ele_val.split(',')
			if img_files:
				getImgRowHTML(img_files, body_DOM)
			# 	# print "\n\n img_files", img_files

		if ele_type.strip() == "Video" and ele_val != 'NONE':
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
			vid_files = []
			vid_files = ele_val.split(',')
			if vid_files:
				getVideoRowHTML(vid_files, body_DOM, dictionary_obj)
			# print vid_files
		'''
		if ele_type.strip() == "Word cloud" and ele_val != 'NONE':
			pass
		'''
		if ele_type.strip() == "Audio Track" and ele_val != 'NONE':
			'''
			<audio width="360" height="360" controls="" class="span_12_of_12">
				<source src="../Audio/" type="audio/mpeg"/>
			</audio>
			'''

			audio_ele_data = {
				'width': '360',
				'height': '360',
				'klass':'span_12_of_12',
			}
			audio_ele = body_DOM.audio(**audio_ele_data)
			audio_ele.source(src='../Audio/' + ele_val, type='audio/mpeg')


		if ele_type.strip() == "Subtitles (Audio)" and ele_val != 'NONE':
			pass

		'''
		Handled in Video tag generation function getVideoRowHTML.

		if ele_type.strip() == "Subtitles (Video)" and ele_val != 'NONE':
			pass
		'''
	# print "\n body_DOM == ", body_DOM
	return body_DOM
try:
	for each_sheet in activities_template_workbook.sheets():
		# print " || No. of rows found: ", each_sheet.nrows
		# if "Activity" in each_sheet.name:
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
				dict_obj = {k.encode('utf8'): v.encode('utf8') for k, v in dict_obj.items()}
				# print "\n final dict = ", dict_obj
				if dict_obj:
					if activity_num and activity_name:
						header_ele = createHTMLHeaderElement(activity_num, activity_name, body_html)
					main_tag_in_body = body_html.main(klass="group span_10_of_12")
					html_content = parseOnScreenEle(dict_obj, main_tag_in_body)
					continue

		if body_html:
			w = open(str(each_sheet.name)+'.html', 'w+')
			w.write(doc_defination + str(init_html())+str(head_block())+str(body_html)+"</html>")
			w.close()
			# print "\n sheet_obj : ", each_sheet.name
			print "\n Created file: ", each_sheet.name
			print "*"*80
		# else:
		# 	print "\n Skipping: ", each_sheet.name
		# 	print "*"*80

except Exception as e:
	print "\n Error occurred!!!  ", e