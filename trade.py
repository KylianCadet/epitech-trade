#!/usr/bin/python3

import sys
import statistics
import math

def getmiddleBB(arr, period):
	new_list = arr[-period:]
	return (statistics.mean(new_list))

def getStandartDeviation(arr, period):
	newList = arr[-period:]
	mean = statistics.mean(newList)
	deviationSum = 0
	for i in newList:
		deviationSum += (abs(i - mean))**2
	return (math.sqrt(deviationSum / period))

class Trade:
	_input = ""
	settings = {}
	timebank = 0
	time_per_move = 0
	player_names = ""
	your_bot = ""
	candle_interval = 0
	candles_total = 0
	candles_given = 0
	initial_stack = 0
	candle_format = ""
	transaction_fee_percent = 0
	_format = {}
	BTC_stack = 0
	ETH_stack = 0
	USDT_stack = 0
	BTC_ETH_array = [{}]
	USDT_ETH_array = [{}]
	USDT_BTC_array = [{}]

	def get_input(self):
		try:
			self._input = input()
		except:
			exit(0)

	def get_settings(self):
		for i in range(0, 10):
			self.get_input()
			arr = self._input.split(" ")
			if (arr[0] != "settings" or len(arr) < 3):
				print("Bad formatted setting : " + self._input, file=sys.stderr)
				exit(84)
			self.settings[arr[1]] = arr[2]

	def set_format(self):
		good_val = 0
		candle_arr = ["pair", "date", "high", "low", "open", "close", "volume"]
		self.candle_format = self.candle_format.split(",")
		if (len(self.candle_format) != 7):
			print("Error with candle_format : ", end='', file=sys.stderr)
			print(self.candle_format, file=sys.stderr)
			exit(84)
		for i in self.candle_format:
			for j in candle_arr:
				if i == j:
					self._format[j] = good_val
					good_val = good_val + 1
					candle_arr.remove(j)
		if (good_val != 7):
			print("Error with candle_format : ", end='', file=sys.stderr)
			print(self.candle_format, file=sys.stderr)
			exit(84)

	def set_settings(self):
		try:
			self.timebank = int(self.settings["timebank"])
			self.time_per_move = int(self.settings["time_per_move"])
			self.player_names = self.settings["player_names"]
			self.your_bot = self.settings["your_bot"]
			self.candle_interval = int(self.settings["candle_interval"])
			self.candles_total = int(self.settings["candles_total"])
			self.candles_given = int(self.settings["candles_given"])
			self.initial_stack = int(self.settings["initial_stack"])
			self.candle_format = self.settings["candle_format"]
			self.transaction_fee_percent = float(self.settings["transaction_fee_percent"])
		except:
			print("Bad settings", file=sys.stderr)
			exit(84)
		self.set_format()

	def get_info(self, arr, info):
		return arr[self._format[info]]

	def append_candles(self, string):
		arr = string.split(";")
		for i in arr:
			info = i.split(",")
			if (self.get_info(info, "pair") == "BTC_ETH"):
				self.BTC_ETH_array[-1]["date"] = float(self.get_info(info, "date"))
				self.BTC_ETH_array[-1]["high"] = float(self.get_info(info, "high"))
				self.BTC_ETH_array[-1]["low"] = float(self.get_info(info, "low"))
				self.BTC_ETH_array[-1]["open"] = float(self.get_info(info, "open"))
				self.BTC_ETH_array[-1]["close"] = float(self.get_info(info, "close"))
				self.BTC_ETH_array[-1]["volume"] = float(self.get_info(info, "volume"))
				self.BTC_ETH_array.append({})
			if (self.get_info(info, "pair") == "USDT_ETH"):
				self.USDT_ETH_array[-1]["date"] = float(self.get_info(info, "date"))
				self.USDT_ETH_array[-1]["high"] = float(self.get_info(info, "high"))
				self.USDT_ETH_array[-1]["low"] = float(self.get_info(info, "low"))
				self.USDT_ETH_array[-1]["open"] = float(self.get_info(info, "open"))
				self.USDT_ETH_array[-1]["close"] = float(self.get_info(info, "close"))
				self.USDT_ETH_array[-1]["volume"] = float(self.get_info(info, "volume"))
				self.USDT_ETH_array.append({})
			if (self.get_info(info, "pair") == "USDT_BTC"):
				self.USDT_BTC_array[-1]["date"] = float(self.get_info(info, "date"))
				self.USDT_BTC_array[-1]["high"] = float(self.get_info(info, "high"))
				self.USDT_BTC_array[-1]["low"] = float(self.get_info(info, "low"))
				self.USDT_BTC_array[-1]["open"] = float(self.get_info(info, "open"))
				self.USDT_BTC_array[-1]["close"] = float(self.get_info(info, "close"))
				self.USDT_BTC_array[-1]["volume"] = float(self.get_info(info, "volume"))
				self.USDT_BTC_array.append({})

	def set_stack(self, string):
		arr = string.split(",")
		if (len(arr) != 3):
			print("Wrong value :" + string, file=sys.stderr)
			print("Wrong value : " + string, file=sys.stderr)
			exit(84)
		for i in arr:
			info = i.split(":")
			if (len(info) != 2):
				print("Wrong value : " + i, file=sys.stderr)
				exit(84)
			elif (info[0] == "BTC"):
				self.BTC_stack = float(info[1])
			elif (info[0] == "ETH"):
				self.ETH_stack = float(info[1])
			elif (info[0] == "USDT"):
				self.USDT_stack = float(info[1])
			else:
				print("Unknow val : " + i, file=sys.stderr)
				exit(84)

	def buyMoney(self, chart_data, trading_pair, money_stack, sell_money_stack, hasBought):
		openArr = list()
		closeArr = list()
		for i in chart_data[:-1]:
			openArr.append(i["open"])
			closeArr.append(i["close"])
		middleBB = getmiddleBB(closeArr, self.candles_given)
		standartDeviation = getStandartDeviation(closeArr, self.candles_given)
		highBB = middleBB + (2 * standartDeviation)
		lowBB = middleBB - (2 * standartDeviation)
		buyVal = ((lowBB - closeArr[-1]) / 10) * money_stack
		sellVal = ((closeArr[-1] - highBB) / 10) * sell_money_stack
		if (closeArr[-1] < lowBB and money_stack > buyVal and buyVal > 0.001):
			if (hasBought):
				print(";", end='')
			print("buy " + trading_pair + " " + str(buyVal), end='')
			return (True)
		elif (closeArr[-1] > highBB and sell_money_stack > sellVal and sellVal > 0.5):
			if (hasBought):
				print(";", end='')
			print("sell " + trading_pair + " " + str(sellVal), end='')
			print("should sell !", file=sys.stderr)
			return (True)
		return (False)

	def order(self, milliseconds):
		passBool = False
		hasBought = self.buyMoney(self.USDT_ETH_array, "USDT_ETH", self.USDT_stack / self.USDT_ETH_array[-2]["close"], self.ETH_stack, False)
		passBool = hasBought or passBool
		hasBought = self.buyMoney(self.BTC_ETH_array, "BTC_ETH", self.BTC_stack / self.BTC_ETH_array[-2]["close"], self.ETH_stack, passBool)
		passBool = hasBought or passBool
		hasBought = self.buyMoney(self.USDT_BTC_array, "USDT_BTC", self.USDT_stack / self.USDT_BTC_array[-2]["close"], self.BTC_stack, passBool)
		passBool = hasBought or passBool
		if (passBool == False):
			print("pass")
		else:
			print("")

	def main_loop(self):
		while (1):
			self.get_input()
			arr = self._input.split(" ")
			if (arr[0] == "update" and arr[1] == "game" and arr[2] == "next_candles"):
				self.append_candles(arr[3])
			elif (arr[0] == "update" and arr[1] == "game" and arr[2] == "stacks"):
				self.set_stack(arr[3])
			elif (arr[0] == "action" and arr[1] == "order"):
				self.order(float(arr[2]))
			else:
				print("Unknow cmd : " + self._input, file=sys.stderr)

	def start(self):
		self.get_settings()
		self.set_settings()
		self.main_loop()

def main():
	obj = Trade()
	obj.start()

if __name__ == '__main__':
	main()