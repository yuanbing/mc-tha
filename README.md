# Introduction

This is the MVP for the [Monte-Carlo](https://www.montecarlodata.com/) home assignment.

# How to run?

## Prerequisites

- [docker](https://www.docker.com/)
- docker-compose (it comes with the installation of docker desktop)
- make
- [Postman](https://www.postman.com/downloads/)
- (optional) [python 3.9+](https://www.python.org/downloads/)
- (optional) [python virtual environment](https://docs.python.org/3/library/venv.html)
- (optional) [VSCode](https://code.visualstudio.com/)
- (optional) [VSCode Remote Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

If you only run the service to see how it works, then you don't need to install those optional components. 

## Get the code
open a terminal, then type in the following commands

```
# create a temporary folder to hold the code, please feel free to choose a proper folder name.
mkdir ~/mywork
cd ~/mywork
git clone https://github.com/yuanbing/mc-tha.git
cd mc-tha
```

## Run the service

```
# assume you're in the same folder where the source code is checked out to

# build the containers, patient...
make build

# start the service
make run
```

For the first time, it will take some time for downloading and building the docker images. 

If everything goes fine, you should see something like this in the terminal.

```
...
[+] Running 2/2
 ⠿ Network pricesapi_default  Created                                                                                                                     0.1s
 ⠿ Container pricesapi-api-1  Started                                                                                                                     0.6s
...
```

You could tail the log output of the running container:

```
make logs
```

## Sanity check
After making sure the service is up and running, it's time to run a simple sanity check:

```
make test
WARN[0000] Found orphan containers ([queryapi-vscode-1]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
===================================================================== test session starts =====================================================================
platform linux -- Python 3.9.15, pytest-7.2.0, pluggy-1.0.0
rootdir: /workspace
plugins: cov-4.0.0, anyio-3.6.2
collected 1 item

tests/test_app.py .                                                                                                                                     [100%]

====================================================================== 1 passed in 0.10s ======================================================================

```

## Functional tests
The above sanity check proves whether the container(s) are running properly. But it won't tell whether the service is working accordingly. For that we need to run the function tests. This time we would use [postman](https://www.postman.com/downloads/) to run the test suite.

- Launch postman
- Import [test suite](https://drive.google.com/file/d/17VOWY5x66-4j287ew8LefurHM8FGgbO7/view?usp=share_link)
![screen shot of test suite](https://drive.google.com/file/d/11DCE5o6nMlHoztQ6zLbft0x2ZfmYius8/view?usp=sharing)
- In postman, you could execute the tests:
	- collect the price data (from the provider) by executing the collection actions (5 in total)
	- wait for a while (10 - 15) minutes, the collection interval is set to 1 minute. You could see the data collection from the logging output.
	- get the latest price for *btcusd*
	- get the volatility rank


## Shutdown the service

```
# in the same folder where you start the service
make shutdown
```

# Service API

The service provides a *RESTful* like API that doesn't follow the *REST* canon by the book, more discussions on that later.

The API supports

- collecting the exchange rate of a crypto currency;
- getting the latest exchange rate of a crypto currency;
- getting the volatility rank of a set of crypto currencies.

## API: collect the exchange rate

It asks the service to start collecting the exchange rate for a particular crypto currency.

 API | Detail
------------- | -------------
entry point  | `prices/collect`
HTTP method  | PUT
input 	| `{"exchange": "binance-us", "pair": "btcusd"}`
output | `"scheduled"` if succeeded or some error message if failed

*Note:* for the MVP, we *ONLY* support getting the exchange rate for a fixed exchange. It's my understanding that there are multiple exchanges and the exchange rate could vary for the same pair of crypto currency and concrete currency.

## API: get the latest exchange rate

It provides the latest exchange rate for a crypto currency whose rate is being collected. In other words, one *MUST* use the above API to collect the exchange rate first.

 
 API | Detail
------------- | -------------
entry point  | `prices/binance-us/{name_of_crypto_currency}/price`
HTTP method  | GET
input	| None
output | exchange rate (e.g.16854.97) or -1.0 (if the data is not collected)

## API: get the volatility rank

It rank the volatility for a set of crypto currencies. The rank is determined by reverse sorting the standard deviation of the exchange rate for the last *24* hours. If there is *no* data collected for a particular crypto currency, then its rank is *-1*.

 API | Detail
------------- | -------------
entry point  | `prices/rank`
HTTP method  | POST
input 	| `{"exchange": "binance-us","pairs": ["ethusd","btcusd",...]}`
output | `[{"pair":"btcusd","stdev":1.4990663761147605,"rank": 1},{"pair": "ethusd","stdev":0.28991378028654236,"rank": 2},...]}`

# Technical details

## Design
<<<need a system diagram>>>

### Components

The service is composed of three components: *api*, *database* and *data provider*. The *data provider* is considered as the *external* dependency that we have no control over. Thus our discussion is mainly focused on *api* and *database*.

Since the *api* component is influenced by the [requirement](https://drive.google.com/file/d/1Z9WAjceg8AjuhaF94mqjN-yyaLmPkWfU/view?usp=sharing) and influences the *database* component, thus we start our discussion with *api* component.

#### component: api

The *api* component has three sub-components:
- api/service entry points. this is the client facing interface that meets the [requirements](https://drive.google.com/file/d/1Z9WAjceg8AjuhaF94mqjN-yyaLmPkWfU/view?usp=sharing). 
	- it 
