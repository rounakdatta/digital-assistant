### Usage

#### Add data to MongoDB

```make data```

#### Get the application running

```make run```

Head over to [localhost:5000](http://localhost:5000)

### System Design

**/dataprovider/dataprovider.py** - After core query is parsed, control passes to get_short_answer() where the processing logic lies. There, MongoDB lookup occurs. The priority of search is MongoDB -> wolfram -> wikipedia.

**/nlp/rasa.py** - Parsing logic - What to do with intents + all the hard-coded replies are defined here. Based on intent, if falls into hard-coded case, _randomly_ one of the replies in the reply array is returned.

**initDb.py** - General documentation of how to push/pull to/from MongoDB - also includes the data which has already been inserted to MongoDB. This is the file needed to insert data to MongoDB (manually).

**rasa-data.json** - Training dataset containing all the intents as well as entities. Use ```rasa-nlu-trainer``` instead of manual filling.

### Development Status

- [x] The bot learns to speak
- [x] Database integration
- [x] Flask API
- [x] Front-End to interact
- [x] The bot remembers
- [ ] The bot is mature
- [ ] The bot doesn't faint at all

_Tip: Make use of [Studio 3T](https://studio3t.com/) on any platform to view MongoDB using an UI._