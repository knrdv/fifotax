#!/usr/bin/python3
"""FIFO tax calculator.

This program is used for calculating taxes in first-in-first-out order of buying.
This program expects a .csv file containing transaction information in format:
	1. column: date
	2. column: action (BUY/SELL)
	3. column: ticker
	4. column: quantity
	5. column: price

For example:
	2021-02-18 BUY PLTR 0.67062549 25.26 16.94
	- in this case the last columnt (16.94) will get discarded
"""
import config
import logging
import collections
import argparse
from transaction import Transactions
from trailmaker import TrailMaker
from datetime import datetime
from hnbAPI import HnbAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main(args):
	transactions = Transactions(args.transactions_csv)
	print(f"Transactions:\n{transactions}")

	# Initialize Croatian National Bank API interface
	hnb = HnbAPI()

	# Initialize trail maker
	tm = TrailMaker() if not args.output else TrailMaker(args.output)
	tm.writeFirst(transactions)

	state = {}
	gains_usd = "gains_usd"
	gains_hrk = "gains_hrk"
	for tr in transactions:

		# If first time seeing the ticker, initialize its state
		if tr.ticker not in state:
			logger.info(f"Adding new ticker to state: {tr.ticker}")
			state[tr.ticker] = {}
			state[tr.ticker]["buyqueue"] = collections.deque()
			state[tr.ticker][gains_usd] = 0.0
			state[tr.ticker][gains_hrk] = 0.0
			state[tr.ticker]["buy_quantity"] = 0.0

		# Buy transaction
		if tr.action.lower() == "buy":
			state[tr.ticker]["buyqueue"].appendleft(tr)
			state[tr.ticker]["buy_quantity"] += tr.quantity

		# Sell transaction
		elif tr.action.lower() == "sell":
			logger.info("Got a SELL order:")
			logger.info(tr)
			logger.info(f"Total buy quantity: {state[tr.ticker]['buy_quantity']}")

			# Write buy trail
			tm.writeSell(tr)

			# Get currency middle exchange rate at sell date
			middle_rate = hnb.getMiddleExchangeAtDate(tr.date, currency="USD")
			logger.info(f"Middle rate at {tr.date} was {middle_rate}")

			# Do while selling quantity is not depleted
			while tr.quantity > 0:
				logger.info(f"{tr.ticker} quantity: {tr.quantity}")
				buy_trans = state[tr.ticker]["buyqueue"].pop()
				logger.info(f"Popped: {buy_trans}")

				# If buy transaction is older than 2y, no tax is paid
				passed_2y = False
				time_delta = abs(tr.date - buy_trans.date)
				logger.info(f"Time delta: {time_delta.days}")
				if time_delta.days >= 365 * 2:
					logger.info(f"Time delta is {time_delta} and greater than 2 years, no taxes are paid on it")
					passed_2y = True

				# If buy_trans will get spent
				if tr.quantity >= buy_trans.quantity:
					if not passed_2y:
						state[tr.ticker][gains_usd] += (tr.price - buy_trans.price)*buy_trans.quantity
						state[tr.ticker][gains_hrk] += (tr.price - buy_trans.price)*buy_trans.quantity*middle_rate
						tm.writeCalculation(tr, buy_trans, middle_rate, state[tr.ticker][gains_hrk])

					tr.quantity = round(tr.quantity - buy_trans.quantity, 8)

				# If buy transaction has greater quantity than the current selling,
				# buy transaction will get put back in queue with reduced quantity
				elif tr.quantity < buy_trans.quantity:
					if not passed_2y:
						state[tr.ticker][gains_usd] += (tr.price - buy_trans.price)*tr.quantity
						state[tr.ticker][gains_hrk] += (tr.price - buy_trans.price)*tr.quantity*middle_rate
						tm.writeCalculation(tr, buy_trans, middle_rate, state[tr.ticker][gains_hrk])
					buy_trans.quantity -= tr.quantity
					state[tr.ticker]["buyqueue"].append(buy_trans)
					tr.quantity -= tr.quantity

	total_gains_usd = 0.0
	total_gains_hrk = 0.0
	for key in state:
		ticker_gains_usd = state[key][gains_usd]
		ticker_gains_hrk = state[key][gains_hrk]
		print(f"{key} gains: {ticker_gains_usd} USD, {ticker_gains_hrk} HRK")
		total_gains_usd += ticker_gains_usd
		total_gains_hrk += ticker_gains_hrk
	if total_gains_usd < 0:
		logger.info(f"Operating at loss: {total_gains_usd}, no taxes need to be paid")
		total_gains_usd = 0.0
		total_gains_hrk = 0.0
	tax = total_gains_hrk * config.TAX
	tax += tax * config.SURTAX
	tm.writeLast(state)

	print(f"Total tax to pay: {tax} HRK")

if __name__ == "__main__":
	logging.basicConfig(format=config.LOG_FORMAT, filename=config.LOG_FILE)
	parser = argparse.ArgumentParser()
	parser.add_argument("transactions_csv", type=str, help="file containing transactions in CSV format")
	parser.add_argument("-o", "--output", help="output file")
	args = parser.parse_args()
	main(args)