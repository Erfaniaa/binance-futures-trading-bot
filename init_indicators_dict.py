import pickle

indicators_dict_btcusdt_m1 = {
	"candle_open_timestamp": 1650207540,
	"candle_close_timestamp": 1650207600,
	"ema_50": 40371.0,
	"ema_40": 40368.8,
	"ema_30": 40367.3,
	"ema_20": 40365.6,
	"ema_10": 40358.1,
	"macd_ema_12": 40360.6,
	"macd_ema_26": 40366.8,
	"macd_line": -6.2,
	"signal_line": -0.4
}
# POSITION_QUANTITY_DECIMAL_DIGITS = 3

indicators_dict_btcusdt_h1 = {
	"candle_open_timestamp": 1656885600,
	"candle_close_timestamp": 1656889199,
	"ema_50": 19252.09,
	"ema_40": 19226.85,
	"ema_30": 19212.71,
	"ema_20": 19214.55,
	"ema_10": 19254.93,
	"macd_ema_12": 19251.00,
	"macd_ema_26": 19218.02,
	"macd_line": 32.98,
	"signal_line": 30.47
}
# POSITION_QUANTITY_DECIMAL_DIGITS = 3

indicators_dict_ethusdt_m1 = {
	"candle_open_timestamp": 1650265140,
	"candle_close_timestamp": 1650265200,
	"ema_50": 2916.64,
	"ema_40": 2916.77,
	"ema_30": 2916.98,
	"ema_20": 2917.13,
	"ema_10": 2916.65,
	"macd_ema_12": 2916.85,
	"macd_ema_26": 2917.06,
	"macd_line": -0.21,
	"signal_line": 0.42
}
# POSITION_QUANTITY_DECIMAL_DIGITS = 3

indicators_dict_ethusdt_m15 = {
	"candle_open_timestamp": 1655726400,
	"candle_close_timestamp": 1655727299,
	"ema_50": 1107.64,
	"ema_40": 1113.20,
	"ema_30": 1119.82,
	"ema_20": 1129.13,
	"ema_10": 1142.61,
	"macd_ema_12": 1139.74,
	"macd_ema_26": 1123.09,
	"macd_line": 16.64,
	"signal_line": 15.15
}
# POSITION_QUANTITY_DECIMAL_DIGITS = 3


indicators_dict_ethbusd_m15 = {
	"candle_open_timestamp": 1655823600,
	"candle_close_timestamp": 1655824499,
	"ema_50": 1151.07,
	"ema_40": 1154.70,
	"ema_30": 1158.77,
	"ema_20": 1163.58,
	"ema_10": 1171.10,
	"macd_ema_12": 1170.08,
	"macd_ema_26": 1161.66,
	"macd_line": 8.55,
	"signal_line": 5.74
}
# POSITION_QUANTITY_DECIMAL_DIGITS = 3


indicators_dict_dogebusd_m1 = {
	"candle_open_timestamp": 1650531540,
	"candle_close_timestamp": 1650531599,
	"ema_50": 0.140322,
	"ema_40": 0.140352,
	"ema_30": 0.140383,
	"ema_20": 0.140417,
	"ema_10": 0.140451,
	"macd_ema_12": 0.140446,
	"macd_ema_26": 0.140396,
	"macd_line": 0.000050,
	"signal_line": 0.000059
}
# POSITION_QUANTITY_DECIMAL_DIGITS = 0

indicators_dict_dogebusd_m15 = {
	"candle_open_timestamp": 1650530700,
	"candle_close_timestamp": 1650531599,
	"ema_50": 0.140742,
	"ema_40": 0.140574,
	"ema_30": 0.140403,
	"ema_20": 3042.09,
	"ema_10": 3040.86,
	"macd_ema_12": 0.140168,
	"macd_ema_26": 0.140338,
	"macd_line": -0.000170,
	"signal_line": -0.000281
}
# POSITION_QUANTITY_DECIMAL_DIGITS = 0

indicators_dict_xrpbusd_m1 = {
	"candle_open_timestamp": 1650531540,
	"candle_close_timestamp": 1650531599,
	"ema_50": 0.7489,
	"ema_40": 0.7491,
	"ema_30": 0.7494,
	"ema_20": 0.7497,
	"ema_10": 0.7499,
	"macd_ema_12": 0.7499,
	"macd_ema_26": 0.7495,
	"macd_line": 0.0004,
	"signal_line": 0.005
}
# POSITION_QUANTITY_DECIMAL_DIGITS = 1

indicators_dict_xrpbusd_m15 = {
	"candle_open_timestamp": 1650530700,
	"candle_close_timestamp": 1650531599,
	"ema_50": 0.7513,
	"ema_40": 0.7506,
	"ema_30": 0.7499,
	"ema_20": 0.7491,
	"ema_10": 0.7484,
	"macd_ema_12": 0.7484,
	"macd_ema_26": 0.7495,
	"macd_line": -0.0011,
	"signal_line": -0.0015
}
# POSITION_QUANTITY_DECIMAL_DIGITS = 1

pickle.dump(indicators_dict_btcusdt_h1, open("indicators_dict.pkl", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
