#!/usr/bin/python

import sqlite3
import string
from flask import Flask, request, Response, url_for, render_template, flash, jsonify


## Global definitions.

codfiscapp = Flask(__name__)
codfiscapp.config['DEBUG']=True

#Strutture dati Globali
vocali = ('a','e','i','o','u')
mesi = ('a','b','c','d','e','h','l','m','p','r','s','t')

#CODICI DI CONTROLLO
regole_pari = {}
alfabeto = string.ascii_lowercase
for i in xrange (0,10):
	regole_pari[str(i)] = i
for i in xrange (0,26):
	regole_pari[alfabeto[i]] = i

regole_dispari = {}
temp_tuple = (1,0,5,7,9,13,15,17,19,21)
for i in xrange(0,10):
	regole_dispari[str(i)] = temp_tuple[i]
	regole_dispari[alfabeto[i]] = temp_tuple[i]

temp_tuple2 = (2,4,18,20,11,3,6,8,12,14,16,10,22,25,24,23)
index = 0
for i in xrange(10,26):
	regole_dispari[alfabeto[i]] = temp_tuple2[index]
	index += 1

regole_resto = [alfabeto[i] for i in xrange(0,26)]


##--------------------------------------------------------------------------------------------------------


def estrai_nome_cognome(aString):
	aString=aString.replace(" ","")
	temp_string = ''
	for aChar in aString:
		if not aChar in vocali:
			temp_string += aChar
		if len(temp_string) >= 3:
			break
	index = 0
	while len(temp_string) < 3:
		if not aString[index] in temp_string:
			temp_string += aString[index]
		index += 1

	return temp_string

def genera_mese(unMese):
	return mesi[int(unMese)-1]

def genera_giorno(unGiorno, unSesso):
	if int(unGiorno) in xrange(1,31):
		if unSesso == 'm':
			return unGiorno
		elif unSesso == 'f':
			return str(int(unGiorno)+40)


##--------------------------------------------------------------------------------------------------------


def genera_codice_controllo(aCodiceFiscale):
	parita = 1
	temp_dispari = 0
	temp_pari = 0

	for aChar in aCodiceFiscale:
		if parita:
			temp_dispari += int(regole_dispari.get(aChar))
			parita = 0
		else:
			temp_pari += int(regole_pari.get(aChar))
			parita = 1

	return regole_resto[(temp_dispari+temp_pari) % 26]


##--------------------------------------------------------------------------------------------------------


## Ajax answering functions for evaluating the code.
@codfiscapp.route('/_evaluate')
def evaluate():

	nome = request.args.get('nome', "", type=str)
	nome = nome.lower()
	cognome = request.args.get('cognome', "", type=str)
	cognome = cognome.lower()
	data_nascita = request.args.get('data_nascita', "", type=str)
	comune = request.args.get('comune', "", type=str)
	comune = comune.lower()
	sesso = request.args.get('sesso', "", type=str)
	sess = sesso.lower()

	## Compone gli elementi del codice fiscale.
	nomeCF = estrai_nome_cognome(nome)
	cognomeCF = estrai_nome_cognome(cognome)
	data_nascitaCF = data_nascita.split("/")
	anno_nascitaCF = data_nascitaCF[2][2:]
	mese_nascitaCF = genera_mese(data_nascitaCF[1])
	giorno_nascitaCF = genera_giorno(data_nascitaCF[0], sesso)

	codice_fiscale = cognomeCF + nomeCF + anno_nascitaCF + mese_nascitaCF + giorno_nascitaCF + comune
	codiceCF = genera_codice_controllo(codice_fiscale)
	codice_fiscale += codiceCF

	return jsonify(result=codice_fiscale.upper())


##--------------------------------------------------------------------------------------------------------


@codfiscapp.route("/")
def home():


	# Ricava il codice istat dal comune:
	db = sqlite3.connect("/var/www/html/static/listacomuni.db")
	sql3cur = db.cursor()
	strSQL = "SELECT ComCodFisco, ComDescrizione FROM tblComuni ORDER BY ComDescrizione;"
	sql3cur.execute(strSQL)
	Entries = sql3cur.fetchall()
	db.close()

	return render_template('home.html', entries=Entries)


##--------------------------------------------------------------------------------------------------------


#if __name__ == "__main__":
#	codfiscapp.run()

