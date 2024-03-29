import requests

with open('../aws_data/tickers.csv', 'r') as file:
    file.readline()
    tickers = file.readlines()
    tickers = [x.strip() for x in tickers]

    
api_url = 'https://financialmodelingprep.com/api/v3/financials/income-statement/{}?period=quarter'
Q_file = '../aws_data/{}.csv'


# for (q, year) in [(3, '2016'), (4, '2016'), 
#                   (1, '2017'), (2, '2017'), (3, '2017'), (4, '2017'), 
#                   (1, '2018'), (2, '2018'), (3, '2018'), (4, '2018'), 
#                   (1, '2019'), (2, '2019')]:

for (q, year) in [(1, '2019'), (2, '2019')]:

    yq = year + 'Q' + str(q)

    with open(Q_file.format(yq), 'w') as file:
        file.write('')

    with open(Q_file.format(yq), 'w') as file:
        for j, ticker in enumerate(tickers):
            print(j, ticker)
            def _write_blank(file, ticker):
                file.write('\n')
                file.write(ticker)

            def _write(file, r, ticker):
                ls = [ticker] + list(r.values())
                file.write('\n')
                file.write(','.join(ls))

            try:
                url = api_url.format(ticker)
                record = requests.get(url).json()['financials']
                dates = [r['date'] for r in record]
                date2018 = [x for x in dates if x.startswith(year)]

                # some company has date like 4-27, so we just take the first data of 2018
                if len(date2018) >= q:
                    date = date2018[-q]
                else:
                    _write_blank(file, ticker)
                    continue

                for i, r in enumerate(record):
                    if j == 0 and i == 0:
                        file.write(','.join([''] + list(r.keys())))                
                    if r['date'] == date: 
                        _write(file, r, ticker)   
            except:
                print(ticker)
                _write_blank(file, ticker) 
