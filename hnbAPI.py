"""This clas implements Croatian National Bank API interface."""
import logging
import config
import requests
import json
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class HnbAPI:

	def __init__(self):
		self.endpoint = config.HNB_API
		self.dateformat = config.HNB_DATE_FORMAT

	def getMiddleExchangeToday(self, currency="USD") -> float:
		"""Returns middle exchange rate for currency to HRK at current date."""
		query = f"{self.endpoint}?valuta={currency.upper()}"
		response = requests.get(query)
		json_response = json.loads(response.text)[0]
		print(json_response)
		text_date = json_response["datum_primjene"]
		date = datetime.strptime(text_date, self.dateformat)

		if datetime.today().date() != date.date():
			logger.info("Date missmatch")
			raise ValueError("Date missmatch")
		else:
			logger.info("Date ok")

		if json_response["valuta"].lower() == currency.lower():
			middle = json_response["srednji_tecaj"].replace(",", ".")
			return float(middle)
		else:
			logger.info("Wrong currency")
			raise ValueError("Wrong currency")

	def getMiddleExchangeAtDate(self, date, currency="USD") -> float:
		hnb_date = date.strftime(config.HNB_DATE_FORMAT)
		query = f"{self.endpoint}?valuta={currency}&datum-primjene={hnb_date}"
		response = requests.get(query)
		json_response = json.loads(response.text)
		exchange_data = json_response[0]
		
		text_date = exchange_data["datum_primjene"]
		received_date = datetime.strptime(text_date, self.dateformat)
		if received_date.date() != date.date():
			logger.info("Date missmatch")
			raise ValueError("Date missmatch")
		else:
			logger.info("Date ok")

		if exchange_data["valuta"].lower() == currency.lower():
			middle = exchange_data["srednji_tecaj"].replace(",", ".")
			return float(middle)
		else:
			logger.info("Wrong currency")
			raise ValueError("Wrong currency")