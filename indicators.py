def get_wma(candles: list) -> float:
	if len(candles) == 0:
		return 0
	if len(candles) == 1:
		return candles[0]
	coe = 1
	base = 2 ** (1 / (len(candles) - 1))
	coe_sum = 0
	sum = 0
	for i in range(len(candles)):
		sum += candles[i] * coe
		coe *= base
		coe_sum += coe
	return sum / coe_sum


def get_ma(candles: list) -> float:
	if len(candles) == 0:
		return 0
	rs = 0
	for item in range(len(candles)):
		rs += float(candles[item])
	rs = rs / len(candles)
	return rs


def get_new_ema(last_ema: int, price: int, count: int) -> float:
	m = 2 / (count + 1)
	price = price
	s1 = (float(price) * float(m))
	s2 = float(last_ema) * float((1 - m))
	return s1 + s2
