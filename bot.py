import os
import sys
import traceback
from slack.bot import SlackBot
from nlp.rasa import RasaNLP
from dataprovider.dataprovider import DataProvider

try:
	dp = DataProvider(os.environ.get("RL222P-RT8L7JURJR"))

	r = RasaNLP(dp, "rasa-config.json", "rasa-data.json", "./rasa-model")
	r.train()

	b = SlackBot("xoxb-411949009943-410690833188-Sxt4KFxQdfxu7jKdN7zaluiA", r)
	b.start()
except KeyboardInterrupt:
	r.snapshot_unparsed_messages("rasa-unparsed.txt")
	sys.exit(0)
except:
	r.snapshot_unparsed_messages("rasa-unparsed.txt")
	traceback.print_exc()