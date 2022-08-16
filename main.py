from time import sleep
from datetime import *
from indicators import *
from config import *
import pickle
import logging
import sys
from candle import Candle
from binance.um_futures import UMFutures
from credentials import *
from utils import *
from telegram_message_sender import *

is_price_increasing = False
is_price_decreasing = False
is_macd_increasing = False
is_macd_decreasing = False
is_macd_positive = False
is_macd_negative = False
account_available_balance = 0
total_account_balance = 0
is_bot_started = False
current_time = datetime.now()
indicators_dict = {}
orders_dict = {}
contract_open_orders_count = 0
open_orders_list = []
last_account_available_balances_list = []
last_total_account_balances_list = []


def update_current_time() -> int:
	global current_time
	global last_time
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			last_time = current_time
			current_time = datetime.fromtimestamp(binance_futures_api.time()["serverTime"] / 1000)
			return SUCCESSFUL
		except:
			pass
	logging.error("ERROR in update_current_time")
	return ERROR


def get_local_timestamp() -> int:
	return int(datetime.now().timestamp())


def convert_binance_data_list_to_candles_list(binance_data_list: list) -> list:
	candles_list = []
	for binance_data in binance_data_list:
		candle = Candle(datetime.fromtimestamp(binance_data[0] // 1000), binance_data[1], binance_data[2],
						binance_data[3], binance_data[4], None, datetime.fromtimestamp(binance_data[6] // 1000))
		candles_list.append(candle)
	return candles_list


def get_m1_candles(
	contract_symbol: str, 
	start_datetime: datetime, 
	end_datetime: datetime
) -> tuple:
	start_timestamp = int(start_datetime.timestamp() * 1000)
	end_timestamp = int(end_datetime.timestamp() * 1000)
	number_of_kline_candles_requests = (end_timestamp - start_timestamp + MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS - 1) // (MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS)
	all_m1_candles_list = []
	for i in range(number_of_kline_candles_requests):
		current_time_range_start = i * MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS + start_timestamp
		current_time_range_end = (i + 1) * MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS + start_timestamp - 1
		current_time_range_start = max(current_time_range_start, start_timestamp)
		current_time_range_start = min(current_time_range_start, end_timestamp)
		current_time_range_end = max(current_time_range_end, start_timestamp)
		current_time_range_end = min(current_time_range_end, end_timestamp)
		current_time_range_m1_candles_list = None
		for j in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
			try:
				current_time_range_m1_candles_list = binance_futures_api.klines(symbol=contract_symbol, interval="1m", startTime=current_time_range_start, endTime=current_time_range_end, limit=MAXIMUM_KLINE_CANDLES_PER_REQUEST)
				break
			except:
				pass
		if not current_time_range_m1_candles_list:
			logging.error("ERROR in get_m1_candles")
			return (ERROR, [])
		for m1_candle in current_time_range_m1_candles_list:
			all_m1_candles_list.append(Candle(datetime.fromtimestamp(m1_candle[0] // 1000),
											  m1_candle[1],
											  m1_candle[2],
											  m1_candle[3],
											  m1_candle[4],
											  m1_candle[5],
											  datetime.fromtimestamp(m1_candle[6] // 1000)))
	return (SUCCESSFUL, all_m1_candles_list)


def get_m15_candles(
	contract_symbol: str, 
	start_datetime: datetime, 
	end_datetime: datetime
) -> tuple:
	start_timestamp = int(start_datetime.timestamp() * 1000)
	end_timestamp = int(end_datetime.timestamp() * 1000)
	number_of_kline_candles_requests = (end_timestamp - start_timestamp + MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 15 - 1) // (MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 15)
	all_m15_candles_list = []
	for i in range(number_of_kline_candles_requests):
		current_time_range_start = i * MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 15 + start_timestamp
		current_time_range_end = (i + 1) * MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 15 + start_timestamp - 1
		current_time_range_start = max(current_time_range_start, start_timestamp)
		current_time_range_start = min(current_time_range_start, end_timestamp)
		current_time_range_end = max(current_time_range_end, start_timestamp)
		current_time_range_end = min(current_time_range_end, end_timestamp)
		current_time_range_m15_candles_list = None
		for j in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
			try:
				current_time_range_m15_candles_list = binance_futures_api.klines(symbol=contract_symbol, interval="15m", startTime=current_time_range_start, endTime=current_time_range_end, limit=MAXIMUM_KLINE_CANDLES_PER_REQUEST)
				break
			except:
				pass
		if not current_time_range_m15_candles_list:
			logging.error("ERROR in get_m15_candles")
			return (ERROR, [])
		for m15_candle in current_time_range_m15_candles_list:
			all_m15_candles_list.append(Candle(datetime.fromtimestamp(m15_candle[0] // 1000),
											   m15_candle[1],
											   m15_candle[2],
											   m15_candle[3],
											   m15_candle[4],
											   m15_candle[5],
											   datetime.fromtimestamp(m15_candle[6] // 1000)))
	return (SUCCESSFUL, all_m15_candles_list)


def get_h1_candles(
	contract_symbol: str, 
	start_datetime: datetime, 
	end_datetime: datetime
) -> tuple:
	start_timestamp = int(start_datetime.timestamp() * 1000)
	end_timestamp = int(end_datetime.timestamp() * 1000)
	number_of_kline_candles_requests = (end_timestamp - start_timestamp + MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 - 1) // (MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60)
	all_h1_candles_list = []
	for i in range(number_of_kline_candles_requests):
		current_time_range_start = i * MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 + start_timestamp
		current_time_range_end = (i + 1) * MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 + start_timestamp - 1
		current_time_range_start = max(current_time_range_start, start_timestamp)
		current_time_range_start = min(current_time_range_start, end_timestamp)
		current_time_range_end = max(current_time_range_end, start_timestamp)
		current_time_range_end = min(current_time_range_end, end_timestamp)
		current_time_range_h1_candles_list = None
		for j in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
			try:
				current_time_range_h1_candles_list = binance_futures_api.klines(symbol=contract_symbol, interval="1h", startTime=current_time_range_start, endTime=current_time_range_end, limit=MAXIMUM_KLINE_CANDLES_PER_REQUEST)
				break
			except:
				pass
		if not current_time_range_h1_candles_list:
			logging.error("ERROR in get_h1_candles")
			return (ERROR, [])
		for h1_candle in current_time_range_h1_candles_list:
			all_h1_candles_list.append(Candle(datetime.fromtimestamp(h1_candle[0] // 1000),
											  h1_candle[1],
											  h1_candle[2],
											  h1_candle[3],
											  h1_candle[4],
											  h1_candle[5],
											  datetime.fromtimestamp(h1_candle[6] // 1000)))
	return (SUCCESSFUL, all_h1_candles_list)


def get_h2_candles(
	contract_symbol: str, 
	start_datetime: datetime, 
	end_datetime: datetime
) -> tuple:
	start_timestamp = int(start_datetime.timestamp() * 1000)
	end_timestamp = int(end_datetime.timestamp() * 1000)
	number_of_kline_candles_requests = (end_timestamp - start_timestamp + MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 * 2 - 1) // (MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 * 2)
	all_h2_candles_list = []
	for i in range(number_of_kline_candles_requests):
		current_time_range_start = i * MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 * 2 + start_timestamp
		current_time_range_end = (i + 1) * MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 * 2 + start_timestamp - 1
		current_time_range_start = max(current_time_range_start, start_timestamp)
		current_time_range_start = min(current_time_range_start, end_timestamp)
		current_time_range_end = max(current_time_range_end, start_timestamp)
		current_time_range_end = min(current_time_range_end, end_timestamp)
		current_time_range_h2_candles_list = None
		for j in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
			try:
				current_time_range_h2_candles_list = binance_futures_api.klines(symbol=contract_symbol, interval="2h", startTime=current_time_range_start, endTime=current_time_range_end, limit=MAXIMUM_KLINE_CANDLES_PER_REQUEST)
				break
			except:
				pass
		if not current_time_range_h2_candles_list:
			logging.error("ERROR in get_h2_candles")
			return (ERROR, [])
		for h2_candle in current_time_range_h2_candles_list:
			all_h2_candles_list.append(Candle(datetime.fromtimestamp(h2_candle[0] // 1000),
									   h2_candle[1],
									   h2_candle[2],
									   h2_candle[3],
									   h2_candle[4],
									   h2_candle[5],
									   datetime.fromtimestamp(h2_candle[6] // 1000)))
	return (SUCCESSFUL, all_h2_candles_list)


def get_h4_candles(
	contract_symbol: str, 
	start_datetime: datetime, 
	end_datetime: datetime
) -> tuple:
	start_timestamp = int(start_datetime.timestamp() * 1000)
	end_timestamp = int(end_datetime.timestamp() * 1000)
	number_of_kline_candles_requests = (end_timestamp - start_timestamp + MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 * 4 - 1) // (MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 * 4)
	all_h4_candles_list = []
	for i in range(number_of_kline_candles_requests):
		current_time_range_start = i * MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 * 4 + start_timestamp
		current_time_range_end = (i + 1) * MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 * 4 + start_timestamp - 1
		current_time_range_start = max(current_time_range_start, start_timestamp)
		current_time_range_start = min(current_time_range_start, end_timestamp)
		current_time_range_end = max(current_time_range_end, start_timestamp)
		current_time_range_end = min(current_time_range_end, end_timestamp)
		current_time_range_h4_candles_list = None
		for j in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
			try:
				current_time_range_h4_candles_list = binance_futures_api.klines(symbol=contract_symbol, interval="4h", startTime=current_time_range_start, endTime=current_time_range_end, limit=MAXIMUM_KLINE_CANDLES_PER_REQUEST)
				break
			except:
				pass
		if not current_time_range_h4_candles_list:
			logging.error("ERROR in get_h4_candles")
			return (ERROR, [])
		for h4_candle in current_time_range_h4_candles_list:
			all_h4_candles_list.append(Candle(datetime.fromtimestamp(h4_candle[0] // 1000),
											  h4_candle[1],
											  h4_candle[2],
											  h4_candle[3],
											  h4_candle[4],
											  h4_candle[5],
											  datetime.fromtimestamp(h4_candle[6] // 1000)))
	return (SUCCESSFUL, all_h4_candles_list)


def get_d1_candles(
	contract_symbol: str, 
	start_datetime: datetime, 
	end_datetime: datetime
) -> tuple:
	start_timestamp = int(start_datetime.timestamp() * 1000)
	end_timestamp = int(end_datetime.timestamp() * 1000)
	number_of_kline_candles_requests = (end_timestamp - start_timestamp + MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 * 24 - 1) // (MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 * 24)
	all_d1_candles_list = []
	for i in range(number_of_kline_candles_requests):
		current_time_range_start = i * MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 * 24 + start_timestamp
		current_time_range_end = (i + 1) * MAXIMUM_KLINE_CANDLES_PER_REQUEST * ONE_MINUTE_IN_MILLISECONDS * 60 * 24 + start_timestamp - 1
		current_time_range_start = max(current_time_range_start, start_timestamp)
		current_time_range_start = min(current_time_range_start, end_timestamp)
		current_time_range_end = max(current_time_range_end, start_timestamp)
		current_time_range_end = min(current_time_range_end, end_timestamp)
		current_time_range_d1_candles_list = None
		for j in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
			try:
				current_time_range_d1_candles_list = binance_futures_api.klines(symbol=contract_symbol, interval="1d", startTime=current_time_range_start, endTime=current_time_range_end, limit=MAXIMUM_KLINE_CANDLES_PER_REQUEST)
				break
			except:
				pass
		if not current_time_range_d1_candles_list:
			logging.error("ERROR in get_d1_candles")
			return (ERROR, [])
		for d1_candle in current_time_range_d1_candles_list:
			all_d1_candles_list.append(Candle(datetime.fromtimestamp(d1_candle[0] // 1000),
											  d1_candle[1],
											  d1_candle[2],
											  d1_candle[3],
											  d1_candle[4],
											  d1_candle[5],
											  datetime.fromtimestamp(d1_candle[6] // 1000)))
	return (SUCCESSFUL, all_d1_candles_list)


def update_recent_prices_list(
	contract_symbol: str, 
	current_time: datetime, 
	candles_count: int,
	timeframe: str
) -> None:

	global recent_m1_open_prices_list
	global recent_m1_high_prices_list
	global recent_m1_low_prices_list
	global recent_m1_close_prices_list

	global recent_m15_open_prices_list
	global recent_m15_high_prices_list
	global recent_m15_low_prices_list
	global recent_m15_close_prices_list

	global recent_h1_open_prices_list
	global recent_h1_high_prices_list
	global recent_h1_low_prices_list
	global recent_h1_close_prices_list

	global recent_h2_open_prices_list
	global recent_h2_high_prices_list
	global recent_h2_low_prices_list
	global recent_h2_close_prices_list

	global recent_h4_open_prices_list
	global recent_h4_high_prices_list
	global recent_h4_low_prices_list
	global recent_h4_close_prices_list

	global recent_d1_open_prices_list
	global recent_d1_high_prices_list
	global recent_d1_low_prices_list
	global recent_d1_close_prices_list

	if timeframe == "m1":
		start_time = current_time - timedelta(minutes=candles_count + 10)
		end_time = current_time
		recent_candles_list = get_m1_candles(contract_symbol, start_time, end_time)[1][:-1][-candles_count:]
		recent_m1_open_prices_list = [float(candle.open) for candle in recent_candles_list]
		recent_m1_high_prices_list = [float(candle.high) for candle in recent_candles_list]
		recent_m1_low_prices_list = [float(candle.low) for candle in recent_candles_list]
		recent_m1_close_prices_list = [float(candle.close) for candle in recent_candles_list]
	if timeframe == "m15":
		start_time = current_time - timedelta(minutes=(candles_count + 10) * 15)
		end_time = current_time
		recent_candles_list = get_m15_candles(contract_symbol, start_time, end_time)[1][:-1][-candles_count:]
		recent_m15_open_prices_list = [float(candle.open) for candle in recent_candles_list]
		recent_m15_high_prices_list = [float(candle.high) for candle in recent_candles_list]
		recent_m15_low_prices_list = [float(candle.low) for candle in recent_candles_list]
		recent_m15_close_prices_list = [float(candle.close) for candle in recent_candles_list]
	if timeframe == "h1":
		start_time = current_time - timedelta(minutes=(candles_count + 10) * 60)
		end_time = current_time
		recent_candles_list = get_h1_candles(contract_symbol, start_time, end_time)[1][:-1][-candles_count:]
		recent_h1_open_prices_list = [float(candle.open) for candle in recent_candles_list]
		recent_h1_high_prices_list = [float(candle.high) for candle in recent_candles_list]
		recent_h1_low_prices_list = [float(candle.low) for candle in recent_candles_list]
		recent_h1_close_prices_list = [float(candle.close) for candle in recent_candles_list]
	if timeframe == "h2":
		start_time = current_time - timedelta(minutes=(candles_count + 10) * 60 * 2)
		end_time = current_time
		recent_candles_list = get_h2_candles(contract_symbol, start_time, end_time)[1][:-1][-candles_count:]
		recent_h2_open_prices_list = [float(candle.open) for candle in recent_candles_list]
		recent_h2_high_prices_list = [float(candle.high) for candle in recent_candles_list]
		recent_h2_low_prices_list = [float(candle.low) for candle in recent_candles_list]
		recent_h2_close_prices_list = [float(candle.close) for candle in recent_candles_list]
	if timeframe == "h4":
		start_time = current_time - timedelta(minutes=(candles_count + 10) * 60 * 4)
		end_time = current_time
		recent_candles_list = get_h4_candles(contract_symbol, start_time, end_time)[1][:-1][-candles_count:]
		recent_h4_open_prices_list = [float(candle.open) for candle in recent_candles_list]
		recent_h4_high_prices_list = [float(candle.high) for candle in recent_candles_list]
		recent_h4_low_prices_list = [float(candle.low) for candle in recent_candles_list]
		recent_h4_close_prices_list = [float(candle.close) for candle in recent_candles_list]
	if timeframe == "d1":
		start_time = current_time - timedelta(minutes=(candles_count + 10) * 60 * 24)
		end_time = current_time
		recent_candles_list = get_d1_candles(contract_symbol, start_time, end_time)[1][:-1][-candles_count:]
		recent_d1_open_prices_list = [float(candle.open) for candle in recent_candles_list]
		recent_d1_high_prices_list = [float(candle.high) for candle in recent_candles_list]
		recent_d1_low_prices_list = [float(candle.low) for candle in recent_candles_list]
		recent_d1_close_prices_list = [float(candle.close) for candle in recent_candles_list]


def load_orders_dict() -> None:
	global orders_dict
	orders_dict = load_orders_dict_from_file(ORDERS_DICT_FILENAME)


def load_orders_dict_from_file(filename: str = ORDERS_DICT_FILENAME) -> list:
	with open(filename, 'rb') as handle:
		return pickle.load(handle)


def save_orders_dict() -> None:
	save_orders_dict_to_file(ORDERS_DICT_FILENAME)


def save_orders_dict_to_file(filename : str = ORDERS_DICT_FILENAME) -> None:
	global orders_dict
	with open(filename, 'wb') as handle:
		pickle.dump(orders_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def update_orders_dict(current_time: datetime, key: str, value: str) -> None:
	global orders_dict
	orders_dict["timestamp"] = current_time
	orders_dict[key] = value


def load_indicators_dict() -> None:
	global indicators_dict
	indicators_dict = load_indicators_dict_from_file(INDICATORS_DICT_FILENAME)


def load_indicators_dict_from_file(filename: str = INDICATORS_DICT_FILENAME) -> list:
	global indicators_dict
	with open(filename, 'rb') as handle:
		return pickle.load(handle)


def save_indicators_dict() -> None:
	save_indicators_dict_to_file(INDICATORS_DICT_FILENAME)


def save_indicators_dict_to_file(filename: str = INDICATORS_DICT_FILENAME) -> None:
	global indicators_dict
	with open(filename, 'wb') as handle:
		pickle.dump(indicators_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def update_indicators_dict(
	contract_symbol: str,
	current_time: datetime, 
	timeframe: str
) -> None:
	global indicators_dict
	if timeframe == "m1":
		candles_list = get_m1_candles(contract_symbol, datetime.fromtimestamp(indicators_dict["candle_close_timestamp"]), current_time)[1]
	if timeframe == "m15":
		candles_list = get_m15_candles(contract_symbol, datetime.fromtimestamp(indicators_dict["candle_close_timestamp"]), current_time)[1]
	if timeframe == "h1":
		candles_list = get_h1_candles(contract_symbol, datetime.fromtimestamp(indicators_dict["candle_close_timestamp"]), current_time)[1]
	close_prices_list = [candle.close for candle in candles_list]
	open_times_list = [candle.open_time for candle in candles_list]
	close_times_list = [candle.close_time for candle in candles_list]
	_ema_50 = indicators_dict["ema_50"]
	_ema_40 = indicators_dict["ema_40"]
	_ema_30 = indicators_dict["ema_30"]
	_ema_20 = indicators_dict["ema_20"]
	_ema_10 = indicators_dict["ema_10"]
	_macd_ema_12 = indicators_dict["macd_ema_12"]
	_macd_ema_26 = indicators_dict["macd_ema_26"]
	_macd_line = indicators_dict["macd_line"]
	_signal_line = indicators_dict["signal_line"]
	for i in range(len(close_prices_list)):
		_close_price = round(float(close_prices_list[i]), PRICE_DECIMAL_DIGITS)
		_open_time = open_times_list[i].timestamp()
		_close_time = close_times_list[i].timestamp()
		if timeframe == "m1" and current_time - timedelta(minutes=1) < datetime.fromtimestamp(_open_time):
			break
		if timeframe == "m15" and current_time - timedelta(minutes=15) < datetime.fromtimestamp(_open_time):
			break
		if timeframe == "h1" and current_time - timedelta(minutes=60) < datetime.fromtimestamp(_open_time):
			break
		_ema_50 = round(get_new_ema(_ema_50, _close_price, 50), INDICATORS_DECIMAL_DIGITS)
		_ema_40 = round(get_new_ema(_ema_40, _close_price, 40), INDICATORS_DECIMAL_DIGITS)
		_ema_30 = round(get_new_ema(_ema_30, _close_price, 30), INDICATORS_DECIMAL_DIGITS)
		_ema_20 = round(get_new_ema(_ema_20, _close_price, 20), INDICATORS_DECIMAL_DIGITS)
		_ema_10 = round(get_new_ema(_ema_10, _close_price, 10), INDICATORS_DECIMAL_DIGITS)
		_macd_ema_12 = round(get_new_ema(_macd_ema_12, _close_price, 12), INDICATORS_DECIMAL_DIGITS)
		_macd_ema_26 = round(get_new_ema(_macd_ema_26, _close_price, 26), INDICATORS_DECIMAL_DIGITS)
		_macd_line = round(_macd_ema_12 - _macd_ema_26, INDICATORS_DECIMAL_DIGITS)
		_signal_line = round(get_new_ema(_signal_line, _macd_line, 9), INDICATORS_DECIMAL_DIGITS)
		indicators_dict = {
			"candle_open_timestamp": _open_time,
			"candle_close_timestamp": _close_time,
			"candle_close_price": _close_price,
			"ema_50": _ema_50,
			"ema_40": _ema_40,
			"ema_30": _ema_30,
			"ema_20": _ema_20,
			"ema_10": _ema_10,
			"macd_ema_12": _macd_ema_12,
			"macd_ema_26": _macd_ema_26,
			"macd_line": _macd_line,
			"signal_line": _signal_line,
		}


def update_account_balance_and_unrealized_profit(first_coin_symbol: str) -> int:
	global account_available_balance
	global total_account_balance
	global last_account_available_balances_list
	global last_total_account_balances_list
	global unrealized_profit
	last_account_available_balances_list.append(account_available_balance)
	last_total_account_balances_list.append(total_account_balance)
	if len(last_account_available_balances_list) > LAST_ACCOUNT_BALANCES_LIST_MAX_LENGTH:
		last_account_available_balances_list = last_account_available_balances_list[-LAST_ACCOUNT_BALANCES_LIST_MAX_LENGTH:]
	if len(last_total_account_balances_list) > LAST_ACCOUNT_BALANCES_LIST_MAX_LENGTH:
		last_total_account_balances_list = last_total_account_balances_list[-LAST_ACCOUNT_BALANCES_LIST_MAX_LENGTH:]
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			balance_list = binance_futures_api.balance()
			account_available_balance = 0
			total_account_balance = 0
			for balance_dict in balance_list:
				if balance_dict["asset"] == first_coin_symbol:
					account_available_balance = float(balance_dict["availableBalance"])
					total_account_balance = float(balance_dict["balance"])
					unrealized_profit = float(balance_dict["crossUnPnl"])
			return SUCCESSFUL
		except:
			pass
	logging.error("ERROR in update_account_balance_and_unrealized_profit")
	return ERROR


def update_contract_last_price(contract_symbol: str) -> int:
	global contract_last_price
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			contract_last_price = float(binance_futures_api.ticker_price(symbol=contract_symbol)["price"])
			return SUCCESSFUL
		except:
			pass
	logging.error("ERROR in update_contract_last_price")
	return ERROR


def close_all_open_positions_market_price() -> int:
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			all_open_positions = binance_futures_api.get_position_risk(timestamp=get_local_timestamp())
			for position in all_open_positions:
				position_quantity = float(position["positionAmt"])
				if position_quantity == 0.0:
					continue
				elif position_quantity > 0.0:
					binance_futures_api.new_order(symbol=position["symbol"],
												  side="SELL",
												  quantity=abs(position_quantity),
												  type="MARKET",
												  newClientOrderId=NEW_CLIENT_ORDER_ID_PREFIX + str(
													  get_local_timestamp())[-10:],
												  timestamp=get_local_timestamp())
					send_new_order_message(position["symbol"], "SELL", abs(position_quantity))
				elif position_quantity < 0.0:
					binance_futures_api.new_order(symbol=position["symbol"],
												  side="BUY",
												  quantity=abs(position_quantity),
												  type="MARKET",
												  newClientOrderId=NEW_CLIENT_ORDER_ID_PREFIX + str(
													  get_local_timestamp())[-10:],
												  timestamp=get_local_timestamp())
					send_new_order_message(position["symbol"], "BUY", abs(position_quantity))

			return SUCCESSFUL
		except:
			pass
	logging.error("ERROR in close_all_open_positions_market_price")
	return ERROR


def init_bot() -> None:
	global binance_futures_api
	binance_futures_api = UMFutures(key=API_KEY, secret=SECRET_KEY)


def update_is_price_increasing(
	price_direction_indicator_name_1: str, 
	price_direction_indicator_name_2: str
) -> None:
	global last_is_price_increasing
	global is_price_increasing
	global indicators_dict
	global contract_last_price
	last_is_price_increasing = is_price_increasing
	is_price_increasing = indicators_dict[price_direction_indicator_name_1] > indicators_dict[price_direction_indicator_name_2]


def update_is_price_decreasing(
	price_direction_indicator_name_1: str,
	price_direction_indicator_name_2: str
) -> None:
	global last_is_price_decreasing
	global is_price_decreasing
	global indicators_dict
	global contract_last_price
	last_is_price_decreasing = is_price_decreasing
	is_price_decreasing = indicators_dict[price_direction_indicator_name_1] < indicators_dict[price_direction_indicator_name_2]


def update_is_macd_increasing() -> None:
	global last_is_macd_increasing
	global is_macd_increasing
	global indicators_dict
	last_is_macd_increasing = is_macd_increasing
	is_macd_increasing = indicators_dict["macd_line"] > indicators_dict["signal_line"]


def update_is_macd_decreasing() -> None:
	global last_is_macd_decreasing
	global is_macd_decreasing
	global indicators_dict
	global contract_last_price
	last_is_macd_decreasing = is_macd_decreasing
	is_macd_decreasing = indicators_dict["macd_line"] < indicators_dict["signal_line"]


def update_is_macd_positive() -> None:
	global last_is_macd_positive
	global is_macd_positive
	global indicators_dict
	last_is_macd_positive = is_macd_positive
	is_macd_positive = indicators_dict["macd_line"] > 0


def update_is_macd_negative() -> None:
	global last_is_macd_negative
	global is_macd_negative
	global indicators_dict
	global contract_last_price
	last_is_macd_negative = is_macd_negative
	is_macd_negative = indicators_dict["macd_line"] < 0


def is_take_profit_unexecuted(contract_symbol: str, strategy_id: int) -> tuple:
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			order_id = orders_dict.get("strategy" + str(strategy_id) + "_last_take_profit_order_id", -1)
			if int(order_id) == -1:
				return (SUCCESSFUL, False)
			order = binance_futures_api.query_order(symbol=contract_symbol, orderId=order_id, timestamp=get_local_timestamp())
			if order["status"] == "FILLED" or order["status"] == "EXPIRED" or order["status"] == "CANCELED":
				return (SUCCESSFUL, False)
			else:
				return (SUCCESSFUL, True)
		except:
			pass
	logging.error("ERROR in is_take_profit_unexecuted")
	return (ERROR, False)


def is_stop_loss_unexecuted(contract_symbol: str, strategy_id: int) -> tuple:
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			order_id = orders_dict.get("strategy" + str(strategy_id) + "_last_stop_loss_order_id", -1)
			if int(order_id) == -1:
				return (SUCCESSFUL, False)
			order = binance_futures_api.query_order(symbol=contract_symbol, orderId=order_id, timestamp=get_local_timestamp())
			if order["status"] == "FILLED" or order["status"] == "EXPIRED" or order["status"] == "CANCELED":
				return (SUCCESSFUL, False)
			else:
				return (SUCCESSFUL, True)
		except:
			pass
	logging.error("ERROR in is_stop_loss_unexecuted")
	return (ERROR, False)


def is_position_active(contract_symbol: str, strategy_id: int) -> bool:
	return is_take_profit_unexecuted(contract_symbol, strategy_id)[1] and is_stop_loss_unexecuted(contract_symbol, strategy_id)[1]


def cancel_extra_open_order(contract_symbol: str, strategy_id: int) -> int:
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			order_id = None
			if is_take_profit_unexecuted(contract_symbol, strategy_id)[1] and not is_stop_loss_unexecuted(contract_symbol, strategy_id)[1]:
				order_id = orders_dict["strategy" + str(strategy_id) + "_last_take_profit_order_id"]
			elif not is_take_profit_unexecuted(contract_symbol, strategy_id)[1] and is_stop_loss_unexecuted(contract_symbol, strategy_id)[1]:
				order_id = orders_dict["strategy" + str(strategy_id) + "_last_stop_loss_order_id"]

			if order_id is not None:
				binance_futures_api.cancel_order(symbol=contract_symbol, orderId=order_id, timestamp=get_local_timestamp())
				send_cancel_order_message(order_id)
			return SUCCESSFUL
		except:
			pass
	logging.error("ERROR in cancel_extra_open_order")
	return ERROR


def is_it_time_to_open_long_position(strategy_id: int, current_time: datetime) -> bool:
	if strategy_id == 0:
		return is_bot_started and is_price_increasing and not last_is_price_increasing
	if strategy_id == 1:
		return is_bot_started and is_price_increasing and not last_is_price_increasing
	if strategy_id == 2:
		return is_bot_started and is_macd_increasing and not last_is_macd_increasing
	if strategy_id == 3:
		return is_bot_started and is_macd_increasing and not last_is_macd_increasing
	return False


def is_it_time_to_open_short_position(strategy_id: int, current_time: datetime) -> bool:
	if strategy_id == 0:
		return is_bot_started and is_price_decreasing and not last_is_price_decreasing
	if strategy_id == 1:
		return is_bot_started and is_price_decreasing and not last_is_price_decreasing
	if strategy_id == 2:
		return is_bot_started and is_macd_decreasing and not last_is_macd_decreasing
	if strategy_id == 3:
		return is_bot_started and is_macd_decreasing and not last_is_macd_decreasing
	return False


def is_it_time_to_update_and_trade(current_time: datetime) -> bool:
	return int(current_time.minute) == 0 and HANDLING_POSITIONS_TIME_SECOND <= int(
		current_time.second) % 60 <= HANDLING_POSITIONS_TIME_SECOND + 1


def is_it_time_to_cancel_extra_open_orders(current_time: datetime) -> bool:
	return int(current_time.minute) % 5 == 0 and HANDLING_POSITIONS_TIME_SECOND <= int(
		current_time.second) % 60 <= HANDLING_POSITIONS_TIME_SECOND + 1


def cancel_symbol_open_orders(contract_symbol: str) -> int:
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			binance_futures_api.cancel_open_orders(symbol=contract_symbol)
			send_cancel_open_orders_for_symbol_message(contract_symbol)
			return SUCCESSFUL
		except:
			pass
	logging.error("ERROR in cancel_symbol_open_orders")
	return ERROR


def set_leverage(contract_symbol: str, leverage: int) -> int:
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			binance_futures_api.change_leverage(symbol=contract_symbol, leverage=leverage, timestamp=get_local_timestamp())
			return SUCCESSFUL
		except:
			pass
	logging.error("ERROR in set_leverage")
	return ERROR


def set_position_mode(hedge_mode: bool) -> int:
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			if hedge_mode:
				binance_futures_api.change_position_mode(dualSidePosition="true", timestamp=get_local_timestamp())
			else:
				binance_futures_api.change_position_mode(dualSidePosition="false", timestamp=get_local_timestamp())
			return SUCCESSFUL
		except:
			pass
	logging.error("ERROR/WARNING in set_position_mode (this may happen normally when position mode is unchanged)")
	return ERROR


def open_long_position(
	contract_symbol: str,
	first_coin_amount: int,
	take_profit_percent: int, 
	stop_loss_percent: int,
	strategy_id: int
) -> int:
	logging.info("=" * 60)
	logging.info("open_long_position for strategy #" + str(strategy_id))
	market_order_created = False
	position_quantity = round_down(WALLET_USAGE_PERCENT / 100 / STRATEGIES_COUNT * first_coin_amount / contract_last_price, POSITION_QUANTITY_DECIMAL_DIGITS)
	if position_quantity < 10 ** (-POSITION_QUANTITY_DECIMAL_DIGITS):
		logging.info("=" * 60)
		return SUCCESSFUL
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			update_contract_last_price(contract_symbol)
			order_id = "strategy" + str(strategy_id) + "_last_position_order_id"
			market_order = binance_futures_api.new_order(symbol=contract_symbol,
														 side="BUY",
														 positionSide="LONG",
														 quantity=position_quantity,
														 type="MARKET",
														 newClientOrderId=NEW_CLIENT_ORDER_ID_PREFIX + str(get_local_timestamp())[-10:],
														 timestamp=get_local_timestamp())
			send_new_order_message(contract_symbol, "BUY", position_quantity)
			send_open_long_position_message(order_id)
			update_orders_dict(get_local_timestamp(), order_id, market_order["orderId"])
			market_order_created = True
			break
		except:
			pass
	if not market_order_created:
		logging.error("ERROR in open_long_position")
		logging.info("=" * 60)
		return ERROR
	sleep(4 * SLEEP_INTERVAL)
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			position_entry_price = contract_last_price
			market_order = binance_futures_api.query_order(symbol=contract_symbol, orderId=market_order["orderId"], timestamp=get_local_timestamp())
			try:
				if float(market_order["avgPrice"]) > 0:
					position_entry_price = contract_last_price
			except:
				pass
			take_profit_price = round((1 + take_profit_percent / 100) * position_entry_price, PRICE_DECIMAL_DIGITS)
			stop_loss_price = round((1 + stop_loss_percent / 100) * position_entry_price, PRICE_DECIMAL_DIGITS)
			take_profit_price_limit = round(take_profit_price - 10 ** (-PRICE_DECIMAL_DIGITS), PRICE_DECIMAL_DIGITS)
			stop_loss_price_limit = round(stop_loss_price - 10 ** (-PRICE_DECIMAL_DIGITS), PRICE_DECIMAL_DIGITS)
			take_profit_order = binance_futures_api.new_order(symbol=contract_symbol,
															  side="SELL",
															  positionSide="LONG",
															  type="TAKE_PROFIT_MARKET",
															  stopPrice=take_profit_price,
															  quantity=position_quantity,
															  timestamp=get_local_timestamp())
			send_new_order_message(contract_symbol, "SELL", position_quantity)
			send_open_long_position_message("strategy" + str(strategy_id) + "_last_take_profit_order_id")
			stop_loss_order = binance_futures_api.new_order(symbol=contract_symbol,
															side="SELL",
															positionSide="LONG",
															type="STOP_MARKET",
															stopPrice=stop_loss_price,
															quantity=position_quantity,
															timestamp=get_local_timestamp())
			send_new_order_message(contract_symbol, "SELL", position_quantity)
			send_open_long_position_message("strategy" + str(strategy_id) + "_last_stop_loss_order_id")
			update_orders_dict(get_local_timestamp(), "strategy" + str(strategy_id) + "_last_take_profit_order_id", take_profit_order["orderId"])
			update_orders_dict(get_local_timestamp(), "strategy" + str(strategy_id) + "_last_stop_loss_order_id", stop_loss_order["orderId"])
			logging.info("get_local_timestamp:", get_local_timestamp())
			logging.info("position_entry_price:", position_entry_price)
			logging.info("take_profit_price:", take_profit_price)
			logging.info("stop_loss_price:", stop_loss_price)
			logging.info("take_profit_price_limit:", take_profit_price_limit)
			logging.info("stop_loss_price_limit:", stop_loss_price_limit)
			logging.info("=" * 60)
			return SUCCESSFUL
		except:
			pass
	logging.error("ERROR in open_long_position")
	logging.info("=" * 60)
	return ERROR


def open_short_position(
	contract_symbol: str, 
	first_coin_amount: int, 
	take_profit_percent: int, 
	stop_loss_percent: int, 
	strategy_id: int
) -> int:
	logging.info("=" * 60)
	logging.info("open_short_position for strategy #" + str(strategy_id))
	market_order_created = False
	position_quantity = round_down(WALLET_USAGE_PERCENT / 100 / STRATEGIES_COUNT * first_coin_amount / contract_last_price, POSITION_QUANTITY_DECIMAL_DIGITS)
	if position_quantity < 10 ** (-POSITION_QUANTITY_DECIMAL_DIGITS):
		logging.info("=" * 60)
		return SUCCESSFUL
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			update_contract_last_price(contract_symbol)
			order_id = "strategy" + str(strategy_id) + "_last_position_order_id"
			market_order = binance_futures_api.new_order(symbol=contract_symbol,
														 side="SELL",
														 positionSide="SHORT",
														 quantity=position_quantity,
														 type="MARKET",
														 newClientOrderId=NEW_CLIENT_ORDER_ID_PREFIX + str(get_local_timestamp())[-10:],
														 timestamp=get_local_timestamp())
			send_new_order_message(contract_symbol, "SELL", position_quantity)
			send_open_short_position_message(order_id)
			update_orders_dict(get_local_timestamp(), order_id, market_order["orderId"])
			market_order_created = True
			break
		except:
			pass
	if not market_order_created:
		logging.error("ERROR in open_short_position")
		logging.info("=" * 60)
		return ERROR
	sleep(4 * SLEEP_INTERVAL)
	for i in range(MAXIMUM_NUMBER_OF_API_CALL_TRIES):
		try:
			position_entry_price = contract_last_price
			market_order = binance_futures_api.query_order(symbol=contract_symbol, orderId=market_order["orderId"], timestamp=get_local_timestamp())
			try:
				if float(market_order["avgPrice"]) > 0:
					position_entry_price = contract_last_price
			except:
				pass
			take_profit_price = round((1 - take_profit_percent / 100) * position_entry_price, PRICE_DECIMAL_DIGITS)
			stop_loss_price = round((1 - stop_loss_percent / 100) * position_entry_price, PRICE_DECIMAL_DIGITS)
			take_profit_price_limit = round(take_profit_price + 10 ** (-PRICE_DECIMAL_DIGITS), PRICE_DECIMAL_DIGITS)
			stop_loss_price_limit = round(stop_loss_price + 10 ** (-PRICE_DECIMAL_DIGITS), PRICE_DECIMAL_DIGITS)
			take_profit_order = binance_futures_api.new_order(symbol=contract_symbol,
															  side="BUY",
															  positionSide="SHORT",
															  type="TAKE_PROFIT_MARKET",
															  stopPrice=take_profit_price,
															  quantity=position_quantity,
															  timestamp=get_local_timestamp())
			send_new_order_message(contract_symbol, "BUY", position_quantity)
			send_open_short_position_message("strategy" + str(strategy_id) + "_last_take_profit_order_id")
			stop_loss_order = binance_futures_api.new_order(symbol=contract_symbol,
															side="BUY",
															positionSide="SHORT",
															type="STOP_MARKET",
															stopPrice=stop_loss_price,
															quantity=position_quantity,
															timestamp=get_local_timestamp())
			send_new_order_message(contract_symbol, "BUY", position_quantity)
			send_open_short_position_message("strategy" + str(strategy_id) + "_last_stop_loss_order_id")
			update_orders_dict(get_local_timestamp(), "strategy" + str(strategy_id) + "_last_take_profit_order_id", take_profit_order["orderId"])
			update_orders_dict(get_local_timestamp(), "strategy" + str(strategy_id) + "_last_stop_loss_order_id", stop_loss_order["orderId"])
			logging.info("get_local_timestamp:", get_local_timestamp())
			logging.info("position_entry_price:", position_entry_price)
			logging.info("take_profit_price:", take_profit_price)
			logging.info("stop_loss_price:", stop_loss_price)
			logging.info("take_profit_price_limit:", take_profit_price_limit)
			logging.info("stop_loss_price_limit:", stop_loss_price_limit)
			logging.info("=" * 60)
			return SUCCESSFUL
		except:
			pass
	logging.error("ERROR in open_short_position")
	logging.info("=" * 60)
	return ERROR


def check_and_cancel_extra_open_orders() -> None:
	if is_it_time_to_cancel_extra_open_orders(current_time):
		for i in range(STRATEGIES_COUNT):
			cancel_extra_open_order(CONTRACT_SYMBOL, i)


def main() -> None:
	logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
	                    datefmt='%Y/%m/%d %I:%M:%S %p',
	                    handlers=[logging.FileHandler("application.log"), logging.StreamHandler(sys.stdout)])
	global is_bot_started
	init_bot()
	update_account_balance_and_unrealized_profit(FIRST_COIN_SYMBOL)
	set_leverage(CONTRACT_SYMBOL, LEVERAGE)
	set_position_mode(hedge_mode=True)
	while True:
		sleep(SLEEP_INTERVAL)
		update_current_time()
		check_and_cancel_extra_open_orders()
		if not is_it_time_to_update_and_trade(current_time):
			continue
		load_orders_dict()
		load_indicators_dict()
		update_indicators_dict(CONTRACT_SYMBOL, current_time, TIMEFRAME)
		update_current_time()
		update_recent_prices_list(CONTRACT_SYMBOL, current_time, IMPORTANT_CANDLES_COUNT, TIMEFRAME)
		save_indicators_dict()
		update_contract_last_price(CONTRACT_SYMBOL)
		update_is_price_increasing(PRICE_DIRECTION_INDICATOR_NAME_1, PRICE_DIRECTION_INDICATOR_NAME_2)
		update_is_price_decreasing(PRICE_DIRECTION_INDICATOR_NAME_1, PRICE_DIRECTION_INDICATOR_NAME_2)
		update_is_macd_increasing()
		update_is_macd_decreasing()
		update_is_macd_positive()
		update_is_macd_negative()
		update_account_balance_and_unrealized_profit(FIRST_COIN_SYMBOL)
		log_results()
		sleep(4 * SLEEP_INTERVAL)
		for i in range(STRATEGIES_COUNT):
			if not is_position_active(CONTRACT_SYMBOL, i):
				if is_it_time_to_open_long_position(i, current_time):
					open_long_position(CONTRACT_SYMBOL, total_account_balance, TAKE_PROFIT_PERCENTS[i],
										STOP_LOSS_PERCENTS[i], i)
				elif is_it_time_to_open_short_position(i, current_time):
					open_short_position(CONTRACT_SYMBOL, total_account_balance, TAKE_PROFIT_PERCENTS[i],
										STOP_LOSS_PERCENTS[i], i)
		save_orders_dict()
		is_bot_started = True


def log_results() -> None:
	output = (
		f"{'_' * 60}\n"
		f"LEVERAGE:{str(LEVERAGE)}\n"
		f"CONTRACT_SYMBOL:{str(CONTRACT_SYMBOL)}\n"
		f"PRICE_DIRECTION_INDICATOR_NAMES:{str(PRICE_DIRECTION_INDICATOR_NAME_1)}{str(PRICE_DIRECTION_INDICATOR_NAME_2)}\n"
		f"current_time:{str(current_time)}\n"
		f"open_orders_list:{str(open_orders_list)}\n"
		f"account_available_balance:{str(account_available_balance)}{str(FIRST_COIN_SYMBOL)}\n"
		f"total_account_balance:{str(total_account_balance)}{str(FIRST_COIN_SYMBOL)}\n"
		f"unrealized_profit:{str(unrealized_profit)}{str(FIRST_COIN_SYMBOL)}\n"
		f"last_account_available_balances_list:{str(last_account_available_balances_list)}\n"
		f"last_total_account_balances_list:{str(last_total_account_balances_list)}\n"
		f"is_price_increasing:{str(is_price_increasing)}\n"
		f"is_price_decreasing:{str(is_price_decreasing)}\n"
		f"is_macd_increasing:{str(is_macd_increasing)}\n"
		f"is_macd_decreasing:{str(is_macd_decreasing)}\n"
		f"is_macd_positive:{str(is_macd_positive)}\n"
		f"is_macd_negative:{str(is_macd_negative)}\n"
		f"indicators_dict:{str(indicators_dict)}\n"
	)

	logging.info(output)
	send_message(output)


if __name__ == "__main__":
	main()
