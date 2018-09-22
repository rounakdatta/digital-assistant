from flask import Flask, render_template, request, send_file, flash, redirect, session, abort, url_for

import os
from nlp.rasa import RasaNLP
from dataprovider.dataprovider import DataProvider
import traceback

app = Flask(__name__)

def process_msg(data, rasa_nlu):
	print("message received" + data)
	text_to_reply = rasa_nlu.find_reply(data, session)
	if text_to_reply:
		return text_to_reply

@app.route('/', methods=['GET', 'POST'])
def index():
	session['product'] = ''
	session['product_price'] = ''
	session['product_cod'] = ''
	session['product_discount'] = ''
	session['myDiscount'] = 0

	return render_template('index.html')


@app.route('/process', methods=['GET', 'POST'])
def process():
	if request.method == 'POST':
		print(request.form)
		myPayload = request.form['chatInput']
		print('received at flask server : ' + myPayload)

		chatContext, chatReply = process_msg(myPayload, rasa_nlu)

		if chatContext[0] != session['product'] :
			session['myDiscount'] = 0

		session['product'] = ''
		session['product_price'] = ''
		session['product_cod'] = ''
		session['product_discount'] = ''
		
		if chatContext[0] != '' : session['product'] = chatContext[0]
		if chatContext[1] != '' : session['product_price'] = chatContext[1]
		if chatContext[2] != '' : session['product_cod'] = chatContext[2]
		if chatContext[3][0] != '' : session['product_discount'] = chatContext[3][0]

		if session['myDiscount'] == 0 : session['myDiscount'] = chatContext[3][1]

		return chatReply

	return "Tricking me?"


app.secret_key = "digital-assistant"

if __name__ == '__main__':

	try:
		dp = DataProvider(os.environ.get("RL222P-RT8L7JURJR"))
	
		r = RasaNLP(dp, "rasa-config.json", "./data/training_data.json", "./rasa-model")
		r.train()
	
		rasa_nlu = r

	except KeyboardInterrupt:
		r.snapshot_unparsed_messages("rasa-unparsed.txt")
		sys.exit(0)
	except:
		r.snapshot_unparsed_messages("rasa-unparsed.txt")
		traceback.print_exc()

	app.run(debug=True, threaded=True)