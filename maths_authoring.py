from docx import Document

document = Document('../CLIxmaths_U1_A1.2Digital_v1.0 (1).docx')
tables = document.tables
shapes = document.inline_shapes
print len(tables)
for table in tables:
	rows = table.rows
	for ind,row in enumerate(rows):
		cells = row.cells
		for cell in cells:
			if "Task" == cell.text: 
				c = table.row_cells(ind)
				for e in c:
					print e.text
					print "*"*80
