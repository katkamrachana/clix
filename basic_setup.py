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
