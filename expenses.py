#!/usr/bin/python
# -*- coding: utf-8 -*-


import re
import string
import sys


MONTHS = [ "leden", "únor", "březen", "duben", "květen", "červen", "červenec", "srpen", "září", "říjen", "listopad", "prosinec" ]
CATEGORY_CAR = "Auto"
CATEGORY_ATM = "Bankomat"
CATEGORY_LIVING = "Bydlení"
CATEGORY_GIFTS = "Dary"
CATEGORY_KIDS = "Děti"
CATEGORY_TRANSPORT = "Doprava"
CATEGORY_HOLIDAY = "Dovolená"
CATEGORY_DRUG = "Drogerie"
CATEGORY_TRANSACTION = "Interní transakce"
CATEGORY_IT = "IT služby & SW"
CATEGORY_FOOD = "Jídlo"
CATEGORY_CULTURE = "Kultura & hobby"
CATEGORY_CLOTHES = "Oblečení"
CATEGORY_SHOPPING = "Ostatní nákupy"
CATEGORY_RESTAURANT = "Restaurace"
CATEGORY_SAVINGS = "Spoření"
CATEGORY_PHONE = "Telefon"
CATEGORY_HOME = "Vybavení domácnosti"


# EXPENSES
class Expenses():
	def __init__(self, filename):
		self.analyze_file(filename)


	def analyze_file(self, filename):
		file_input = open(filename, "r")
		file_output = open(string.split(filename, ".")[0] + "_categorized.csv", "w")

		for line in file_input:
			if string.count(line, ";")==7:

				line = self.remove_quotes(line)

				# invert sign of amounts because of pie chart
				# earnings gonna be negative, expenses gonna be positive
				try:
					line = self.invert_amount(line)
				except ValueError, e:
					e

				# category patterns
				self.pattern_car = re.compile("SHELL|ROBIN OIL|AGIP|AUTOCENTRUM|CERPACI ST|EUROOIL|OMV|Videnska - PFS|MOL - OBORISTE|MOL - PRAHA|UNICORN|STK BRNO|OIL|AUTONOVA|FORS CS", re.DOTALL | re.IGNORECASE)
				self.pattern_atm = re.compile("Výběr z bankomatu", re.DOTALL | re.IGNORECASE)
				self.pattern_living = re.compile("Byt Brno|Nájem|Pojištění domácnosti|E.ON|Internet O2", re.DOTALL | re.IGNORECASE)
				self.pattern_gifts = re.compile("dárek|JEZISEK|narozenin|Vanoce", re.DOTALL | re.IGNORECASE)
				self.pattern_kids = re.compile("baby|SPUNTIK|BAMBULE|MAJKA - SHOP|AGATIN SVET", re.DOTALL | re.IGNORECASE)
				self.pattern_transport = re.compile("STUDENT AGENCY|DPMB|CESKE DRAHY|CD PRAHA HL.N.|CD BRNO HL.N.|regiojet|ZLUTY.CZ|CD.CZ|DOPRAVNI PODNIK|ARRIVA|DPP AUTOMATY|DP AUTOMATY|DPP, Praha|ASC DOBRIS|ASC PRIBRAM|BRNOID|OPERATOR ICT|DPP - HLAVNI NADRAZI", re.DOTALL | re.IGNORECASE)
				self.pattern_holiday = re.compile("AIRBNB|HOTEL|INTER PARTNER ASSISTA|GENERALI|axa-assistance|Dovolená", re.DOTALL | re.IGNORECASE)
				self.pattern_drug = re.compile("DROGERIE|LEKARNA|ROSSMANN|YVES ROCHER|MANUFAKTURA|FINCLUB|DUMEKO|USTAVNI LEK", re.DOTALL | re.IGNORECASE)
				self.pattern_transaction = re.compile("PŘEVOD NA OSOBNÍ ÚČET|Převod na osobní účet|e-Broker|PAYPAL PTE LTD|živobytí", re.DOTALL | re.IGNORECASE)
				self.pattern_it = re.compile("VPS hosting|GOOGLE|Spotify|subreg.cz|STEAMGAMES|rozhlas", re.DOTALL | re.IGNORECASE)
				self.pattern_food = re.compile("TESCO|ALBERT|KAUFLAND|INTERSPAR|LIDL|BILLA|PENNY MARKET|COOP|CARREFOUR|SAFEWAY|WALGREENS|RALPHS|RELAY|OXALIS|zdrave vyzivy|GAZDA MARKET|SKLIZENO|KARLOVA PEKARNA|UVOZ BRNO|TCHIBO|PEKARNA|PEKARSTVI|Potraviny|BIOPOINT|BRANA KE ZDRAVI|BRNENKA|Penny|PODNIKOVA PRODEJNA AW|OCEAN 48", re.DOTALL | re.IGNORECASE)
				self.pattern_culture = re.compile("bubnovani|djembe|festival|KINO SCALA|TICKETLIVE.CZ", re.DOTALL | re.IGNORECASE)
				self.pattern_clothes = re.compile("H & M|H&M|CROPP TOWN|CROPPTOWN|MARKS&SPENCER|NEW YORKER|C&A|PRIMARK|Deichmann|CCC|ECCO|ZOOT|CAMAIEU|LINDEX|ORSAY|TEZENIS|BANDI|HUMANIC|CLOPPENBURG|KIK TEXTIL|TOMMY HILFIGER|RESERVED|youngprimitive", re.DOTALL | re.IGNORECASE)
				self.pattern_shopping = re.compile("Alza|SLEVOMAT CZ|VYKUPTO CZ|kasa.cz|KNIHY DOBROVSKY|KANZELSBERGER|HERVIS|hithit.cz|DX.COM|CZC|Datart|ALIEXPRESS|OKAY|SALON EXCLUSIVE", re.DOTALL | re.IGNORECASE)
				self.pattern_restaurant = re.compile("RESTAURACE|RESTAURANT|MOTOREST|RISTORANTE|CUKRARNA|JEDNA BASEN|Henry am Zug|JLV, A.S.|MYFOODMARKET|KTERY NEEXISTUJE|PIZZA|SPACEK|SPORTBAR|MAMUT|NA-TAHU|PADOWETZ|BURGER|MAMY|SUBWAY|STARBUCKS|SKOG|ZLATA LOD|TANKOVNA|U ZABRANSKYCH|CAIPLA|POTREFENA HUSA|BAROKO|JLV - FRANCHISING|Mitrovski|UMAMI|ANNAPURNA|4POKOJE|JBM Brew|PIVOVARSKY|VESELA VACICE|GO, BRNO|GO,  BEHOUNSKA|KAVARNA SPOLEK|PIVNICE U CAPA|COSMOPOLIS GRILL|U Hoveziho pupku|KFC|TRAPAS BAR|Kamil Mucha|WOKER|GRIL|JIDELNI VUZ|HOSPODA|Burrito|PARODIE|SALATERIE|CHARLIES SQUARE|U TRECH CERTU|BISTRO|KAVARNA|CAFE|COFFEE|NORDSEE|Pho Brno|HIMALAYA|PECEME JINAK|HAIKKY|RED HOT CHILLI|MONTE BU|BILBO SMAK|AKOMI|WOK U FUGIHO|JLV|CHILLI TREE|RAMEN|SUNRICE|CATTANI|LISELOTTE|KOFI KOFI|HONG KONG|VIET PALACE|DALLUCI|SINGHA THAI|STAROBRNO|KEBAP|Morning Invest|MAZANY ANDEL|KAFEC|Wolt|VLNENA,  PRIZOVA|BANH-MI-BA", re.DOTALL | re.IGNORECASE)
				self.pattern_savings = re.compile("Penzijní připojištění", re.DOTALL | re.IGNORECASE)
				self.pattern_phone = re.compile("Vodafone|T-mobile", re.DOTALL | re.IGNORECASE)
				self.pattern_home = re.compile("HORNBACH|BAUHAUS|MEUBLE|SCONTO|Nanu-Nana|TIGER", re.DOTALL | re.IGNORECASE)

				# add category column
				if self.is_header(line):
					line = "Kategorie;" + line # header line
				else:
					line = self.add_category(line)

				# add month column
				try:
					line = self.add_month(line)
				except IndexError, e:
					if self.is_header(line): line = "Měsíc;" + line # header line
					else: line = ";" + line
				except ValueError, e:
					if self.is_header(line): line = "Měsíc;" + line # header line
					else: line = ";" + line
			else:
				print "CSV schema has been changed!"

			file_output.write(line)

		file_input.close
		file_output.close


	def remove_quotes(self, line):
		line = string.replace(line, '";"', ';')
		start = string.find(line, '"') + 1;
		end = string.rfind(line, '"');
		return line[start:end] + "\n"


	def invert_amount(self, line):
		start = self.find_nth(line, ";", 1) + 1 # amount value is between first and second semicolon
		end = self.find_nth(line, ";", 2)
		num_str = line[start:end] # get amount
		num_str = string.replace(num_str, " ", "") # remove whitespace
		num_str = string.replace(num_str, ",", ".") # replace decimal comma
		num = string.atof(num_str) * -1 # invert
		num_str = string.replace(str(num), ".", ",") # replace decimal point
		line = line[:start] + num_str + line[end:] # new line
		return line


	def add_category(self, line):
		# TODO: remove diacritic
		# intab =  u"ÀÁÂÃÄÅàáâãäåÒÓÔÕÖØòóôõöøÈÉÊËĚèéêëěÇČçÌÍÎÏìíîïÙÚÛÜŮùúûüůÿÑñňčďřšťýžĎŇŘŠŤÝŽ"
		# outtab = u"AAAAAAaaaaaaOOOOOOooooooEEEEEeeeeeCCcIIIIiiiiUUUUUuuuuuyNnncdrstyzDNRSTYZ"

		car = self.pattern_car.findall(line)
		atm = self.pattern_atm.findall(line)
		living = self.pattern_living.findall(line)
		gifts = self.pattern_gifts.findall(line)
		kids = self.pattern_kids.findall(line)
		transport = self.pattern_transport.findall(line)
		holiday = self.pattern_holiday.findall(line)
		drug = self.pattern_drug.findall(line)
		transaction = self.pattern_transaction.findall(line)
		it = self.pattern_it.findall(line)
		food = self.pattern_food.findall(line)
		culture = self.pattern_culture.findall(line)
		clothes = self.pattern_clothes.findall(line)
		shopping = self.pattern_shopping.findall(line)
		restaurant = self.pattern_restaurant.findall(line)
		savings = self.pattern_savings.findall(line)
		phone = self.pattern_phone.findall(line)
		home = self.pattern_home.findall(line)

		if(len(car)>0):
			category = CATEGORY_CAR
		elif(len(atm)>0):
			category = CATEGORY_ATM
		elif(len(living)>0):
			category = CATEGORY_LIVING
		elif(len(gifts)>0):
			category = CATEGORY_GIFTS
		elif(len(kids)>0):
			category = CATEGORY_KIDS
		elif(len(transport)>0):
			category = CATEGORY_TRANSPORT
		elif(len(holiday)>0):
			category = CATEGORY_HOLIDAY
		elif(len(drug)>0):
			category = CATEGORY_DRUG
		elif(len(transaction)>0):
			category = CATEGORY_TRANSACTION
		elif(len(it)>0):
			category = CATEGORY_IT
		elif(len(food)>0):
			category = CATEGORY_FOOD
		elif(len(culture)>0):
			category = CATEGORY_CULTURE
		elif(len(clothes)>0):
			category = CATEGORY_CLOTHES
		elif(len(shopping)>0):
			category = CATEGORY_SHOPPING
		elif(len(restaurant)>0):
			category = CATEGORY_RESTAURANT
		elif(len(savings)>0):
			category = CATEGORY_SAVINGS
		elif(len(phone)>0):
			category = CATEGORY_PHONE
		elif(len(home)>0):
			category = CATEGORY_HOME
		else:
			category = ""
		
		line = category + ";" + line # new line
		return line


	def add_month(self, line):
		start = self.find_nth(line, ";", 1) + 1 # date value is between first and second semicolon
		end = self.find_nth(line, ";", 2)
		date_str = line[start:end] # get date
		month_str = string.split(date_str, ".")[1] # get month string
		month_num = string.atoi(month_str) # get month number
		month = str(month_num).zfill(2) + " " + MONTHS[month_num-1]
		line = month + ";" + line # new line
		return line


	def is_header(self, line):
		# check if this line is CSV header
		return "Datum;Objem;" in line


	def find_nth(self, haystack, needle, n):
		start = haystack.find(needle)
		while start >= 0 and n > 1:
			start = haystack.find(needle, start+len(needle))
			n -= 1
		return start


# MAIN
if (__name__=="__main__"):
	if len(sys.argv)==2:
		Expenses(string.strip(sys.argv[1]))
	else:
		print "Invalid arguments! First argument must be a name of CSV file, exported via Fio banking."
