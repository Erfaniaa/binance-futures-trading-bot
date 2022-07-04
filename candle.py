class Candle:
	def __init__(self, open_time, open, high, low, close, volume, close_time):
		self.open_time = open_time
		self.open = open
		self.high = high
		self.low = low
		self.close = close
		self.volume = volume
		self.close_time = close_time
	
	def __repr__(self):
		return "open_time:" + str(self.open_time) + \
			", open:" + str(self.open) + \
			", high:" + str(self.high) + \
			", low:" + str(self.low) + \
			", close:" + str(self.close) + \
			", volume:" + str(self.volume) + \
			", close_time:" + str(self.close_time)
