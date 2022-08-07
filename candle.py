class Candle:
	def __init__(self, open_time, open, high, low, close, volume, close_time) -> None:
		self.open_time = open_time
		self.open = open
		self.high = high
		self.low = low
		self.close = close
		self.volume = volume
		self.close_time = close_time

	def __repr__(self) -> str:
		return (
			f"open_time:{str(self.open_time)}"
			f", open:{str(self.open)}"
			f", high:{str(self.high)}"
			f", low:{str(self.low)}"
			f", close:{str(self.close)}"
			f", volume:{str(self.volume)}"
			f", close_time:{str(self.close_time)}"
		)
