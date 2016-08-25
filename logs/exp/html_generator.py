import pandas as pd

def gen_html(name):
	df = pd.read_csv(name+"/results.csv")

	header = """
	<style type="text/css">
		table.tableizer-table {
			font-size: 12px;
			border: 1px solid #CCC; 
			font-family: Arial, Helvetica, sans-serif;
		} 
		.tableizer-table td {
			padding: 4px;
			margin: 3px;
			border: 1px solid #CCC;
		}
		.tableizer-table th {
			background-color: #104E8B; 
			color: #FFF;
			font-weight: bold;
		}
	</style>
	<table class="tableizer-table">
	"""

	columns = """<thead><tr class="tableizer-firstrow">"""
	for c in df.columns:
		columns += """<th nowrap="nowrap">"""+c+"""</th>"""
	columns += """</thead><tbody>"""

	body = ""
	for r in df.iterrows():
		body += "<tr>"
		for j in r[1]:
			body += """<td nowrap="nowrap">""" + str(j) + "</td>"
		body += "</tr>"
	 
	asser = """
	</tbody></table>
	"""

	f = open(name+"/page.html","w")
	f.write(header+columns+body+asser)
	f.close()
