import logging

# Logging
LOG_FILE = "fifotax.log"
LOG_FORMAT = "%(asctime)s:%(name)s:%(levelname)s:%(message)s"

# Transaction file
CSV_FILE = "taxes.csv"
DATE_FORMAT = "%d/%m/%Y %H:%M:%S"

# Output trail
TRAIL_FILE = "trail.txt"

# Tax information
TAX = 0.1
SURTAX = 0
TAX_YEAR = 2021

# HNB API
HNB_API = "https://api.hnb.hr/tecajn/v2"
HNB_DATE_FORMAT = "%Y-%m-%d"