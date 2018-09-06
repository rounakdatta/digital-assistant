from flask import Flask, render_template, request, send_file, flash, redirect, session, abort, url_for

import os
from nlp.rasa import RasaNLP
from dataprovider.dataprovider import DataProvider
import traceback

app = Flask(__name__)

def process_msg(data, rasa_nlu):
	print("message received" + data)
	text_to_reply = rasa_nlu.find_reply(data)
	if text_to_reply:
		return text_to_reply

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


@app.route('/process', methods=['GET', 'POST'])
def process():
	if request.method == 'POST':
		print(request.form)
		myPayload = request.form['chatInput']
		print('received at flask server : ' + myPayload)

		return process_msg(myPayload, rasa_nlu)

		return 'Got it!'

	return "Didn't get it!"


app.secret_key = "jlg-ops"

if __name__ == '__main__':

	try:
		dp = DataProvider(os.environ.get("RL222P-RT8L7JURJR"))
	
		r = RasaNLP(dp, "rasa-config.json", "./data/training_data.json", "./rasa-model")
		r.train()
	
		rasa_nlu = r
	
		'''
		while(True):
			x = input("Enter : ")
			reply = process_msg(x, rasa_nlu)
			print(reply)
		'''
	
	except KeyboardInterrupt:
		r.snapshot_unparsed_messages("rasa-unparsed.txt")
		sys.exit(0)
	except:
		r.snapshot_unparsed_messages("rasa-unparsed.txt")
		traceback.print_exc()

	app.run(debug=True, threaded=True)