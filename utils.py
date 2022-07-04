def round_down(x, precision):
	return round(x - 5 * (10 ** (-precision - 1)), precision)
