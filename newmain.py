from alpaca_trade_api.rest import REST, TimeFrame

path_to_keys='C:\\Users\\Giaco\\Documents\\ALPACA-API-KEY'
with open(path_to_keys+'\\apikey.txt','r') as f:
    keys=f.readlines()


api = REST(keys[0].strip('\n'),keys[1].strip('\n'))

data=api.get_bars("AAPL", TimeFrame.Hour, "2022-01-08", "2022-01-10", adjustment='raw').df

print(data)