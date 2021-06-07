# Fifotax
#### _Simple FIFO method tax calculator_

Fifotax is a simple first-in-first-out tax calculator, made as an aid for calculating taxes from a given transaction list, with Croatian tax residence.

#### Requirements
- Python 3
- Transaction list in .csv format

Transaction list compatible with this program should look like this:
```
Date,Action,Ticker,Quantity,Price
27.11.2020.,BUY,PLTR,10,32.89
27.11.2020.,BUY,PLTR,0.03344481,32.89
28.1.2021.,BUY,GME,1,299.53,299.53
```
First row hsd to contain the following keywords:
 -   Date: date with format specified in config.py file
 -   Action: is it a BUY or SELL action
 -   Ticker: ticker name
 -   Quantity: transaction quantity
 -   Price: transaction price
 
#### In file config.py, you can edit:
- Log file and log format
- Transaction date format
- Tax and Surtax paramteres

#### Running the program
The program can be run with: `fifotax.py transactions.csv`
The program should output the transaction list and tax calculation result.
For better understanding, the program also outputs a calculation trail in the file trail.txt