import os
from nlp.rasa import RasaNLP
from dataprovider.dataprovider import DataProvider
import traceback

def process_msg(data, rasa_nlu):
	print("message received" + data)
	text_to_reply = rasa_nlu.find_reply(data)
	if text_to_reply:
		return text_to_reply

try:
	dp = DataProvider(os.environ.get("RL222P-RT8L7JURJR"))

	r = RasaNLP(dp, "rasa-config.json", "./data/training_data.json", "./rasa-model")
	r.train()

	rasa_nlu = r

	while(True):
		x = input("Enter : ")
		reply = process_msg(x, rasa_nlu)
		print(reply)


except KeyboardInterrupt:
	r.snapshot_unparsed_messages("rasa-unparsed.txt")
	sys.exit(0)
except:
	r.snapshot_unparsed_messages("rasa-unparsed.txt")
	traceback.print_exc()