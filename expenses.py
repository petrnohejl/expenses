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
CATEGORY_TRANSPORT = "Doprava"
CATEGORY_HOLIDAY = "Dovolená"
CATEGORY_TRANSACTION = "Interní transakce"
CATEGORY_IT = "IT služby & SW"
CATEGORY_FOOD = "Jídlo"
CATEGORY_CULTURE = "Kultura & hobby"
CATEGORY_CLOTHES = "Oblečení"
CATEGORY_SHOPPING = "Ostatní nákupy"
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
			if string.count(line, ";")==12:

				# invert sign of amounts because of pie chart
				# earnings gonna be negative, expenses gonna be positive
				try:
					line = self.invert_amount(line)
				except ValueError, e:
					e

				# category patterns
				self.pattern_car = re.compile("SHELL BM|ROBIN OIL|AGIP|AVIA|AUTOCENTRUM ROS|CERPACI ST", re.DOTALL | re.IGNORECASE)
				self.pattern_atm = re.compile("Výběr z bankomatu", re.DOTALL | re.IGNORECASE)
				self.pattern_living = re.compile("Byt Brno", re.DOTALL | re.IGNORECASE)
				self.pattern_gifts = re.compile("dárek", re.DOTALL | re.IGNORECASE)
				self.pattern_transport = re.compile("STUDENT AGENCY|DPMB", re.DOTALL | re.IGNORECASE)
				self.pattern_holiday = re.compile("HOTEL|INTER PARTNER ASSISTA|allianz|GENERALI", re.DOTALL | re.IGNORECASE)
				self.pattern_transaction = re.compile("PŘEVOD NA OSOBNÍ ÚČET", re.DOTALL | re.IGNORECASE)
				self.pattern_it = re.compile("VPS hosting|GOOGLE", re.DOTALL | re.IGNORECASE)
				self.pattern_food = re.compile("TESCO|ALBERT|KAUFLAND|INTERSPAR|LIDL|BILLA|PENNY MARKET|RESTAURACE|MOTOREST|LEKARNA", re.DOTALL | re.IGNORECASE)
				self.pattern_culture = re.compile("bubnovani", re.DOTALL | re.IGNORECASE)
				self.pattern_clothes = re.compile("H & M|H&M|CROPP TOWN|CROPPTOWN|MARKS&SPENCER|NEW YORKER|C&A|PRIMARK|Deichmann", re.DOTALL | re.IGNORECASE)
				self.pattern_shopping = re.compile("Alza|SLEVOMAT CZ|VYKUPTO CZ|kasa.cz|KNIHY DOBROVSKY|KANZELSBERGER|HERVIS", re.DOTALL | re.IGNORECASE)
				self.pattern_savings = re.compile("Penzijní připojištění", re.DOTALL | re.IGNORECASE)
				self.pattern_phone = re.compile("Vodafone", re.DOTALL | re.IGNORECASE)
				self.pattern_home = re.compile("IKEA CR|HORNBACH|BAUHAUS|MEUBLE", re.DOTALL | re.IGNORECASE)

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

			file_output.write(line)

		file_input.close
		file_output.close


	def invert_amount(self, line):
		start = self.find_nth(line, ";", 2) + 1 # amount value is between second and third semicolon
		end = self.find_nth(line, ";", 3)
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
		transport = self.pattern_transport.findall(line)
		holiday = self.pattern_holiday.findall(line)
		transaction = self.pattern_transaction.findall(line)
		it = self.pattern_it.findall(line)
		food = self.pattern_food.findall(line)
		culture = self.pattern_culture.findall(line)
		clothes = self.pattern_clothes.findall(line)
		shopping = self.pattern_shopping.findall(line)
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
		elif(len(transport)>0):
			category = CATEGORY_TRANSPORT
		elif(len(holiday)>0):
			category = CATEGORY_HOLIDAY
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
		start = self.find_nth(line, ";", 2) + 1 # date value is between second and third semicolon
		end = self.find_nth(line, ";", 3)
		date_str = line[start:end] # get date
		month_str = string.split(date_str, ".")[1] # get month string
		month_num = string.atoi(month_str) # get month number
		month = str(month_num).zfill(2) + " " + MONTHS[month_num-1]
		line = month + ";" + line # new line
		return line


	def is_header(self, line):
		# check if this line is CSV header
		return ";Datum;Objem;" in line


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
