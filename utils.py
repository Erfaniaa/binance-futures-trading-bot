def round_down(x: float, precision: int) -> int:
	return round(x - 5 * (10 ** (-precision - 1)), precision)


def retry(max_retries, on_fail):
	def wrapper(fn):
		def inner(*args, **kwargs):
			so_far = 0
			exceptions = {}
			while so_far <= max_retries:
				try:
					return fn(*args, **kwargs)
				except Exception as e:
					exceptions[type(e)] = str(e)
					so_far += 1
			return on_fail('\n'.join(exceptions.values()))
		return inner
	return wrapper
