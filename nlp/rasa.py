import random
import time
import logging
from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer, Metadata, Interpreter
from rasa_nlu.components import ComponentBuilder

import numpy as np

def getTime():
	timeVar = time.localtime()
	if((timeVar[3]) <= 10):
		timeOfTheDay = "Good Morning!"
	elif((timeVar[3]) > 10 and (timeVar[3]) <= 13):
		timeOfTheDay = "Have a great Day!"
	elif((timeVar[3]) > 13 and (timeVar[3]) <= 17):
		timeOfTheDay = "Good Afternoon!"
	elif((timeVar[3]) > 17):
		timeOfTheDay = "Good Evening!"
	else:
		timeOfTheDay = "Thank you!"
	return "It's " + str(timeVar[3]) + "H " + str(timeVar[4]) + "M " + str(timeVar[5]) + "S now. " + timeOfTheDay

def getDate():
	timeVar = time.localtime()
	return "Today's " + str(timeVar[2]) + "-" + str(timeVar[1]) + "-" + str(timeVar[0]) + "!"

class RasaNLP(object):

	COULD_NOT_PARSE_MSGS = [
		"Sorry, I don't know it",
		"Next time I will know, but not now",
		"Sorry, can't get what do you mean",
		"Try something else"
	]
	GREET_MSGS = ["Hi, I'm a bot and here to assist you get your service. Tell me your needs?", "Welcome, how can I help you? Do you need something, have ideas to enquire?", "Hey, nice to see you here! I'm an automated service here to help you deliver services. So, how can I be useful to you?"]
	PRODUCT_MSGS = ["I can help you choose from a variety of brands/choices based on the product you want. So what's your pick?", "I'm a bot but can help you get the perfect product of your choice. We have a wide variety available, lets finds out the best of what you want!"]
	SHOP_MSGS = ["Well, I never sleep and am always ready to your service, go forward and demand something!", "We are 24x7 online and I'll be always there to assist you!", "Unlike a brick-and-mortar store, we'll always be available round-the-clock to help you, accept orders and address grievances!"]
	BOT_MSGS = ["It's the Bot - always speaking and never sleepy!", "I'm the store's Bot at your service! 🙏", "I'm your friend, philosopher and guide!"]
	TIME_MSGS = [getTime()]
	DATE_MSGS = [getDate()]

	INTENT_GREET = "greet"
	INTENT_PRODUCT = "products"
	INTENT_SHOP = "shop"
	INTENT_BOT = "bot"
	INTENT_TIME = "time"
	INTENT_DATE = "date"
	INTENTS_QUESTION = ["is", "can", "whatis", "what", "how", "whats", "howto", "when", "do", "who", "where", "which"]
	
	INTENTS_ASK = "askq"
	ENTITY_QUERY = "query"

	# all enquiries regarding a product
	INTENTS_PRICE = "price"
	INTENTS_COD = "cod"
	INTENTS_DISCOUNT = "discount"
	INTENTS_ORDER = ["order", "orderq"]

	def __init__(self, data_provider, config_file, data_file, model_dir):
		logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

		# store unparsed messages, so later we can train bot
		self.unparsed_messages = []

		self.data_provider = data_provider
		self.data_file = data_file
		self.model_dir = model_dir
		self.rasa_config = config.load(config_file)

	def train(self):
		training_data = load_data(self.data_file)
		trainer = Trainer(self.rasa_config)
		trainer.train(training_data)

		self.interpreter = Interpreter.load(trainer.persist(self.model_dir))

		logging.info("rasa trained successfully")

	def parse(self, msg):
		return self.interpreter.parse(msg)

	def find_reply(self, msg, cookies):
		res = self.parse(msg)
		logging.info("rasa parse res: {}".format(res))

		if not "intent" in res or res["intent"] is None:
			# later we can do something with unparsed messages, probably train bot
			self.unparsed_messages.append(msg)
			return ['', '', '', ['', '']], random.choice(self.COULD_NOT_PARSE_MSGS)

		# greet the user with a welcome messages
		if res["intent"]["name"] == self.INTENT_GREET:
			return ['', '', '', ['', '']], random.choice(self.GREET_MSGS)

		# if user asks what all are available
		if res["intent"]["name"] == self.INTENT_PRODUCT:
			return ['', '', '', ['', '']], random.choice(self.PRODUCT_MSGS)

		# if user asks questions regarding store
		if res["intent"]["name"] == self.INTENT_SHOP:
			return ['', '', '', ['', '']], random.choice(self.SHOP_MSGS)

		if res["intent"]["name"] == self.INTENT_BOT:
			return ['', '', '', ['', '']], random.choice(self.BOT_MSGS)

		# if user asks about the current time
		if res["intent"]["name"] == self.INTENT_TIME:
			return ['', '', '', ['', '']], random.choice(self.TIME_MSGS)

		# if user asks about current date
		if res["intent"]["name"] == self.INTENT_DATE:
			return ['', '', '', ['', '']], random.choice(self.DATE_MSGS)

		# if user asks about the price of the product and I know it
		if res["intent"]["name"] == self.INTENTS_PRICE:

			if cookies['product'] == '' : return ['', '', '', ['', '']], "Please tell me the product you're enquiring!"
			if cookies['product_price'] == '' : return ['', '', '', ['', '']], "Price might not be available at the moment. Can you please check back with me later?"

			return [cookies['product'], cookies['product_price'], cookies['product_cod'], [cookies['product_discount'], 0]], 'It costs ' + cookies['product_price'] + ' INR.'

		# if user asks whether COD is available for a product
		if res["intent"]["name"] == self.INTENTS_COD:

			if cookies['product'] == '' : return ['', '', '', ['', '']], "Please tell me the product you're enquiring!"
			if cookies['product_cod'] == '' : return ['', '', '', ['', '']], "COD details might not be available at the moment. Can you please check back with me later?"

			if(cookies['product_cod']):
				return [cookies['product'], cookies['product_price'], cookies['product_cod'], [cookies['product_discount'], 0]], 'Yes! Cash on Delivery is available!'
			else:
				return [cookies['product'], cookies['product_price'], cookies['product_cod'], [cookies['product_discount'], 0]], 'Sorry, Cash on Delivery is not available for this product. Please try any other methods of payment. Thanks.'

		# if user asks is discount is available, randomly assign him discount - numpy rand with biasing
		if res["intent"]["name"] == self.INTENTS_DISCOUNT:

			if cookies['product'] == '' : return ['', '', '', ['', '']], "Please tell me the product you're enquiring!"
			if cookies['product_discount'] == '' : return ['', '', '', ['', '']], "Discount might not be available at the moment. Can you please check back with me later?"

			myDiscount = str(int(np.random.choice([0, cookies['product_discount']], p=[0.6, 0.4])))

			return [cookies['product'], cookies['product_price'], cookies['product_cod'], [cookies['product_discount'], myDiscount]], str(myDiscount) + '% discount is available for this product for you.'

		# if user wants to place an order
		if res["intent"]["name"] in self.INTENTS_ORDER:

			if cookies['product'] == '' : return ['', '', '', ['', '']], "Please tell me the product you're enquiring!"

			# single product order
			if res["intent"]["name"] == 'order':
				print(int(cookies['product_discount']))
				return [cookies['product'], cookies['product_price'], cookies['product_cod'], [cookies['product_discount'], cookies['product_discount']]], 'Thanks for placing an order. To confirm, your order is ' + cookies['product'] + ' at ' + str((int(cookies['product_price']) * (100 - int(cookies['myDiscount']))) / 100) + ' INR. Lets complete the other details.'

			qty = str(res["entities"][0]["value"])
			return [cookies['product'], cookies['product_price'], cookies['product_cod'], [cookies['product_discount'], cookies['product_discount']]], 'Thanks for placing order of ' + qty + ' items. To confirm, your haved ordered ' + cookies['product'] + '. Total amount = ' + str((int(cookies['product_price']) * int(qty) * (100 - int(cookies['myDiscount']))) / 100) + ' Lets complete the other details.'

		# user asks [details] about a [product] <-- needs special care
		if res["intent"]["name"] == self.INTENTS_ASK:
			print(res["entities"])
			return ['', '', '', ['', '']], "No!"

		# user enquires about a particular product
		if res["intent"]["name"] in self.INTENTS_QUESTION:
			print(res["entities"])
			for e in res["entities"]:
				if e["entity"] == self.ENTITY_QUERY:
					return self.get_short_answer(e["value"])

		self.unparsed_messages.append(msg)
		return ['', '', '', ['', '']], random.choice(self.COULD_NOT_PARSE_MSGS)

	def get_short_answer(self, query):
		return self.data_provider.get_short_answer(query)

	# saves unparsed messages into a file
	def snapshot_unparsed_messages(self, filename):
		with open(filename, "a") as f:
			for msg in self.unparsed_messages:
				f.write("{}\n".format(msg))