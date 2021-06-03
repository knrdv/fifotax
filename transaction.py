"""Trasaction module.

This module implements transaction container class and other helper classes.
	Transactions: container class
	Transaction: class representing one transaction
	TransactionParser: class used for parsing transactions CSV file
"""

import csv
import config
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Transactions:
	"""This clas implements a transaction container.

	Attributes:
		tp: transaction parser object
		transactions: list of transactions parsed from filename
	"""
	def __init__(self, filename : str):
		"""Initializes class with transactions located in CSV file."""
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

	def sort(self) -> None:
		"""Sorts transactions by date"""
		srt = sorted(self.transactions, key=lambda tr: tr.date)
		self.transactions = srt


class Transaction:
	"""This class represents a transaction.

	Attributes:
		date: transaction date
		action: buy or sell
		ticker: ticker name
		quantity: transaction quantity
		price: price at which trans. is executed
		total: total transaction cost
	"""
	def __init__(self, date : datetime, action : str, ticker : str, quantity : float, price : float):
		self.date = date
		self.action = self.validateAction(action)
		self.ticker = ticker
		self.quantity = quantity
		self.price = price
		self.total = round(self.quantity * self.price, 2)

	def __str__(self):
		return f"{self.date.date()} {self.action} {self.ticker} {self.quantity} {self.price} {self.total}"

	def validateAction(self, action : str) -> str:
		"""Validates if action is correct and returns it lowercase"""
		if action.lower() != "buy" and action.lower() != "sell":
			raise ValueError(f"Action {action} is invalid")
		else:
			return action.lower()


class TransactionParser:
	"""This class serves as transaction parser from CSV files.

	Attributes:
		dateformat: format of date to be parsed from CSV file
	"""
	def __init__(self, dateformat=config.DATE_FORMAT):
		self.dateformat = dateformat

	def parse(self, filename : str) -> list:
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
		logger.info("Transactions parsed successfully")
		return transactions