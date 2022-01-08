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

			mappings = self.getMappings(temp_transactions[0])
			temp_transactions = temp_transactions[1:]
			transactions = []
			for t in temp_transactions:
				print(f"current tx: {t}")
				date = datetime.strptime(t[mappings["date"]], self.dateformat)
				action = t[mappings["action"]].lower()
				if action != "sell" and action != "buy":
					logger.info(f"Skipping transaction {t}")
					continue
				ticker = t[mappings["ticker"]].lower()
				quantity = float(t[mappings["quantity"]])
				price = float(t[mappings["price"]])
				transaction = Transaction(date, action, ticker, quantity, price)
				transactions.append(transaction)
		logger.info("Transactions parsed successfully")
		return transactions

	def getMappings(self, columns : list) -> dict:
		"""Find correct column mappings to relevant information from CSV file.
		
		Returns dictionary mappings of correct fields to csv column indices.
		"""
		mappings = {
			"date"		: None,
			"action" 	: None,
			"ticker" 	: None,
			"quantity"  : None,
			"price" 	: None,
		}
		index = 0
		for column in columns:
			col = column.lower()
			logger.info(f"Current column in parser:{col}")
			if col == "date":
				mappings["date"] = index
				logger.info(f"DATE detected at column {index}")
			elif col == "action" or col == "type":
				mappings["action"] = index
				logger.info(f"ACTION detected at column {index}")
			elif col == "ticker":
				mappings["ticker"] = index
				logger.info(f"TICKER detected at column {index}")
			elif col == "quantity":
				mappings["quantity"] = index
				logger.info(f"QUANTITY detected at column {index}")
			elif col == "price" or col == "price per share":
				mappings["price"] = index
				logger.info(f"PRICE detected at column {index}")
			else:
				logger.info(f"Unsupported column {col}")
			index += 1
		for key in mappings.keys():
			if mappings[key] == None:
				logger.error("Found uninitialized mapping")
				raise ValueError(f"Found uninitialized mapping for {key}")
		return mappings
