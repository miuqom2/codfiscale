import sqlite3


def main():

	## Creates and definethe sqlite table.
	db = sqlite3.connect("/home/miuqom2/Sviluppo/python/codicefiscale/listacomuni.db")
	sql3cur = db.cursor()

	strSQL = "CREATE TABLE tblComuni (IDComune integer primary key autoincrement, ComIstat text, ComDescrizione text, ComProvincia text, ComRegione text, ComPrefisso text, ComCAP text, ComCodFisco text, ComAbitanti text, ComLink text);"
	sql3cur.execute(strSQL)
	db.commit()

	## Populates the table with the comma-separated-values in the txt townlist file.
	fdListaComuni = open("listacomuni.txt")
	lstLinee = fdListaComuni.readlines()
	fdListaComuni.close()
	lstLinee=lstLinee[1:] ## Removes the header.
	for strLinea in lstLinee:
		lstCampi = strLinea.split(';')
		strSQL = "INSERT INTO tblComuni (ComIstat, ComDescrizione, ComProvincia, ComRegione, ComPrefisso, ComCAP, ComCodFisco, ComAbitanti, ComLink) VALUES ('" + lstCampi[0] + "', '" + lstCampi[1].replace("'","''") + "', '" + lstCampi[2] + "', '" + lstCampi[3] + "', '" + lstCampi[4] + "', '" + lstCampi[5] + "', '" + lstCampi[6] + "', '" + lstCampi[7] + "', '" + lstCampi[8] + "')"
		print strSQL
		sql3cur.execute(strSQL)

	db.commit()

	strSQL = "SELECT ComCodFisco FROM tblComuni WHERE ComDescrizione LIKE 'Civitella Messer Raimondo'"
	sql3cur.execute(strSQL)
	myEntries = sql3cur.fetchall()
	for myEntry in myEntries:
		print "Codice ISTAT per Civitella Messer Raimondo: " + str(myEntry[0])

	db.close()



if __name__ == '__main__':
	main()