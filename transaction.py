import csv
import config
from datetime import datetime

class Transactions:
	""" This clas implements a transaction container """

	def __init__(self, filename):
		self.tp = TransactionParser()
		self.transactions = self.tp.parse(filename)
		self.sort()

	def __str__(self):
		retstr = ""
		for t in self.transactions:
			retstr += str(t) + "\n"
		retstr = retstr.rstrip()
		return retstr

	def __iter__(self):
		return iter(self.transactions)

	def sort(self):
		srt = sorted(self.transactions, key=lambda tr: tr.date)
		self.transactions = srt

class Transaction:
	""" This class represents a transaction """

	def __init__(self, date : datetime, action : str, ticker : str, quantity : float, price : float):
		self.date = date
		self.action = self.validateAction(action)
		self.ticker = ticker
		self.quantity = quantity
		self.price = price
		self.total = round(self.quantity * self.price, 2)

	def __str__(self):
		return f"{self.date.date()} {self.action} {self.ticker} {self.quantity} {self.price} {self.total}"

	def validateAction(self, action):
		if action != "BUY" and action != "SELL":
			raise ValueError(f"Action {action} is invalid")
		else:
			return action

class TransactionParser:
	""" This class serves as transaction parser from CSV files """

	def __init__(self, dateformat=config.DATE_FORMAT):
		self.dateformat = dateformat

	def parse(self, filename):
		""" Parses CSV transaction data from file """
		with open(filename, newline="") as csvfile:
			csvreader = csv.reader(csvfile)
			temp_transactions = []
			for row in csvreader:
				temp_transactions.append(row)
			temp_transactions = temp_transactions[1:]
			transactions = []
			for t in temp_transactions:
				date = datetime.strptime(t[0], self.dateformat)
				action = t[1]
				ticker = t[2]
				quantity = float(t[3])
				price = float(t[4])
				transaction = Transaction(date, action, ticker, quantity, price)
				transactions.append(transaction)
		return transactions