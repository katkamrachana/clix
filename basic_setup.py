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
	css_files_path = raw_input("Enter path of folder containing CSS files.\n " + \
		"Don't worry, ONLY CSS type files will be picked up after your confirmation:\t")
	all_css_files = os.listdir(css_files_path)
	print "\n1. Add file: Enter y/Y"
	print "2. I will add later: Enter any key"
	for each_css_file in all_css_files:
		if each_css_file.endswith('.css'):
			confirmation_css = (raw_input("Do you want to add file: ", each_css_file)).strip()
			if confirmation_css == 'y' or confirmation_css == 'Y':
				hd.link(href="../Styles/"+ each_css_file, rel="stylesheet", type="text/css")
				
	# hd.link(href="../Styles/style.css", rel="stylesheet", type="text/css")
	# print hd
	# head_block = '<head><meta content="IE=edge" http-equiv="X-UA-Compatible" /><title>CLIx</title><link href="../Styles/style.css" rel="stylesheet" type="text/css" /></head>'
	# return head_block
	return hd
