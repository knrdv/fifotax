#!/usr/bin/python3

import config
import logging
import collections
from transaction import Transactions

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main():
	transactions = Transactions("taxes.csv")
	print(transactions)

	state = {}
	for tr in transactions:
		if tr.ticker not in state:
			state[tr.ticker] = {}
			state[tr.ticker]["buyqueue"] = collections.deque()
			state[tr.ticker]["gains"] = 0.0
			state[tr.ticker]["buy_quantity"] = 0.0

		if tr.action == "BUY":
			state[tr.ticker]["buyqueue"].appendleft(tr)
			state[tr.ticker]["buy_quantity"] += tr.quantity

		elif tr.action == "SELL":
			logger.info("Got a SELL order:")
			logger.info(tr)
			logger.info(f"Total buy quantity: {state[tr.ticker]['buy_quantity']}")
			while tr.quantity > 0:
				logger.info(f"{tr.ticker} quantity: {tr.quantity}")
				buy_trans = state[tr.ticker]["buyqueue"].pop()
				logger.info(f"Popped: {buy_trans}")

				# buy_trans will get spent
				if tr.quantity >= buy_trans.quantity:
					state[tr.ticker]["gains"] += (tr.price - buy_trans.price)*buy_trans.quantity
					tr.quantity = round(tr.quantity - buy_trans.quantity, 8)

				# buy_trans will get put back in queue
				elif tr.quantity < buy_trans.quantity:
					state[tr.ticker]["gains"] += (tr.price - buy_trans.price)*tr.quantity
					buy_trans.quantity -= tr.quantity
					state[tr.ticker]["buyqueue"].append(buy_trans)
					tr.quantity -= tr.quantity

	total_gains = 0.0
	for key in state:
		ticker_gains = state[key]['gains']
		print(f"{key} gains: {ticker_gains}")
		total_gains += ticker_gains

	tax = total_gains * config.TAX
	tax += tax * config.SURTAX

	print(f"Total tax to pay: {tax}")


if __name__ == "__main__":
	logging.basicConfig(format=config.LOG_FORMAT, filename=config.LOG_FILE)
	main()