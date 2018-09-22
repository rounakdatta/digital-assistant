import wolframalpha
import wikipedia
import logging
import pymongo

def form_sentence(words_bucket):
	if words_bucket.count() == 1:
		return ""

	add_sentences = " Also available "
	if words_bucket.count() > 2:
		add_sentences += "are "
		for word_i in range(1, words_bucket.count() - 1):
			add_sentences += words_bucket[word_i]['item'] + ", "
		add_sentences = add_sentences[:-2] + " and " + words_bucket[words_bucket.count() - 1]['item'] + "."
		return add_sentences
	else:
		add_sentences += "is " + words_bucket[1]['item'] + "."

class DataProvider(object):
	NOT_FOUND_MSG = "Oops, Oops, Oops! I tried my best! 😢"

	def __init__(self, app_id):
		logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

		self.wolfram_client = wolframalpha.Client(app_id)
		logging.info("connected to wolfram")

		self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
		self.mydb = self.myclient["digitalAssistant"]
		self.shopData = self.mydb["shopData"]

		print(self.myclient.list_database_names())
		logging.info("connected to MongoDB")

	def get_short_answer(self, query):
		logging.info("searching in mongodb: {}".format(query))
		
		try:
			avq = self.shopData.find({"tags": str(query)})

			if(avq.count() != 0):
				return [str(avq[0]['item']), str(avq[0]['sellingPrice']), avq[0]['cod'], [avq[0]['maxDiscountPercent'], 0]], str(avq[0]['item']) + " found! " + str(avq[0]['availableQuantity']) + " units available." + form_sentence(avq)
			else:
				return [str(avq[0]['item']), str(avq[0]['sellingPrice']), avq[0]['cod'], [avq[0]['maxDiscountPercent'], 0]], "Sorry, " + str(avq[0]['item']) + " isn't currently available."
		except Exception as e:
			print(e)
			return ['', '', '', ''], "Oops, we don't yet have it available here!"

		# needn't search through wolfram or wikipedia
		# code below is redundant and will be removed later
		logging.info("searching in wolfram: {}".format(query))

		try:
			wolfram_res = self.wolfram_client.query(query)
			logging.info("wolfram res: {}".format(wolfram_res))

			return next(wolfram_res.results).text
		except:
			# use wikipedia as failover
			wikiepedia_res = wikipedia.summary(query, sentences=1)
			logging.info("wikipedia res: {}".format(wikiepedia_res))
			if wikiepedia_res:
				return wikiepedia_res

			return self.NOT_FOUND_MSG
