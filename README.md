Backtest Given Investment Strategy per century:

```python backtest.py```

Note:
* This python script is configured to read a predefined CSV file from the data directory.
* There are three CSV files to choose from: (snp500_1800s.csv, snp500_2000s.csv, snp500_1900s.csv)
* Each CSV file contains monthly price data for the snp500 index.
* To change which CSV data file is used, simply update the python script in the beginning


Print out monthly price data per century:

```python print.py```

Note:
* This operation will print SNP500 monthly price action data on a per century basis.


Other strategies:
* 10ma strategy: ```backtest_10ma_strat.py```
* Convention DCA: ```dca_stretegy.py```


Recommendations:
* Experiment around by running all 4 of these scripts.
* The average annual rate of return for the snp500 from 1871 to 2024 is around 4% which falls in line with the conventional DCA strategy
* Understand how the 10ma (backtest_10ma_strat.py) and the momentum (backtest.py) strategy differ from the DCA strategy
* Run backtests on the following timeframes: 150 years, century, decade, 5 year, and yearly
* Remember to run sanity checks of eye-ball the results to make sure everything seems kosher
