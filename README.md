# trade


To use coinone export two env variables in your shell env
```
export COINONE_ACCESS_TOKEN=[your coinone access token]
export COINONE_SECRET_KEY=[you coinone secret key]
```

for upbit
```
export UPBIT_OPEN_API_ACCESS_KEY=[ your upbit open api access key]
export UPBIT_OPEN_API_SECRET_KEY=[your upbit open api secret key]
```


example
```
from upbit import Upbit
from coinone import Coinone



# configuration
Broker = Coinone
broker = Broker()

broker.price('ada')
```
