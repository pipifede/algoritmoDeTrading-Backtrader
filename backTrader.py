from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt

from Strategies.Strategy1 import TestStrategy

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.broker.setcommission(commission=0.001)
    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join('./Data/TSLA.csv')

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2023, 12, 4),
        # Do not pass values after this date
        todate=datetime.datetime(2024, 11, 8),
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Add a strategy
    cerebro.addstrategy(TestStrategy)
    
    # Set our desired cash start
    cerebro.broker.setcash(1000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Graficar resultados
    cerebro.plot()