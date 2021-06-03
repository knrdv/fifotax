"""This helper class is used for making calculation trails."""
import config
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TrailMaker:

	def __init__(self, filename=config.TRAIL_FILE):
		self.trail_file = filename

	def writeFirst(self, transactions):
		with open(self.trail_file, "a") as f:
			f.write("Trasnactions list\n")
			f.write("-----------------\n")
			f.write(str(transactions) + "\n\n")

	def writeSell(self, sell_order):
		with open(self.trail_file, "a") as f:
			line = f"Processing {sell_order}\n"
			f.write(line)

	def writeCalculation(self, t1, t2, rate, gains):
		line1 = f"    REMAINING:   {t1}\n"
		line2 = f"    SUBTRACTING: {t2}\n"
		line3 = f"    ----------\n"
		if t1.quantity >= t2.quantity:
			result = (t1.price - t2.price) * t2.quantity
			line4 = f"    GAIN(USD):{t2.quantity} * {t1.price} - {t2.quantity} * {t2.price} = {result} USD\n"
		elif t1.quantity < t2.quantity:
			result = (t1.price - t2.price) * t1.quantity
			line4 = f"    GAIN(USD):{t1.quantity} * {t1.price} - {t1.quantity} * {t2.price} = {result} USD\n"
		result = result*rate
		line5 = f"    GAIN(HRK):({t1.quantity} * {t1.price} - {t2.quantity} * {t2.price}) * {rate} = {result} HRK\n"
		line6 = f"    TOTAL GAINS: {gains}"
		with open(self.trail_file, "a") as f:
			line = line1 + line2 + line3 + line4 + line5 + line6 + "\n\n"
			f.write(line)

	def writeLast(self, state):
		gains_usd = "gains_usd"
		gains_hrk = "gains_hrk"
		total_gains_usd = 0.0
		total_gains_hrk = 0.0
		with open(self.trail_file, "a") as f:
			for key in state:
				ticker_gains_usd = state[key][gains_usd]
				ticker_gains_hrk = state[key][gains_hrk]
				f.write(f"{key} gains: {ticker_gains_usd} USD, {ticker_gains_hrk} HRK\n")
				total_gains_usd += ticker_gains_usd
				total_gains_hrk += ticker_gains_hrk
			if total_gains_usd < 0:
				f.write(f"Operating at loss: {total_gains_usd}, no taxes need to be paid\n")
				total_gains_usd = 0.0
				total_gains_hrk = 0.0
			tax = total_gains_hrk * config.TAX
			tax += tax * config.SURTAX
			f.write(f"Tax: {config.TAX*100}%\n")
			f.write(f"Surtax: {config.SURTAX*100}%\n")
			f.write(f"Total tax to be paid: {tax} HRK")