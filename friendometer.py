import re
import random
# new_text_length = int(input("New text length:\n"))
# text = input().split()
iotext = open("gc.txt", "r", encoding="utf8")
import matplotlib.pyplot as plt
# text = iotext.read().split()

word_dict = {}

#Things to do:
#1. Use python datetime instead of tuples to store dates?
#2. Possible stats: Texting times, messages sent, messages sent over time

def stringify(l):
	return list(map(lambda x: str(x), l))

def intify(l):
	return map(lambda x: int(x), l)

class message:
	def __init__(self, date, time, text, speaker_num):
		self.date = date
		self.time = time
		self.text = text
		self.speaker_num = speaker_num

class chat:
	def __init__(self, chat_text):
		self.message_list = []
		self.speakers = [] #speakers is integer -> speaker name
		self.num_speak = {} #num_speak is name -> integer
		for i in chat_text:
			if re.search("(\d\d|\d)/(\d\d|\d)/(\d\d|\d), (\d\d|\d):(\d\d|\d) (AM|PM) - (.*):", i):
				date = i.split(",")[0]
				time = re.search("(\d\d|\d):(\d\d|\d) (AM|PM)", i)
				if date:
					date = tuple(intify(date.split("/")))
				if time:
					time = time.group().split()
					time[0] = list(intify(time[0].split(":")))
					if time[1] == "PM":
						time[0][0] += 12
					time = tuple(time[0])
				# Will bug a bit if somebodies name conbtains ": "inside.....
				# Stop at first ":"?
				# print(i.split(":"))
				speaker = re.search(" - (.*)", i.split(": ")[0])
				# print(speaker)
				text = re.split("(.*): ", i, 1)[-1]
				if speaker:
					speaker = speaker.group()[3:]
					if speaker in self.num_speak:
						self.message_list.append(message(date, time, text[:-1], self.num_speak[speaker]))
					else:
						self.num_speak[speaker] = len(self.speakers)
						self.speakers.append(speaker)
						self.message_list.append(message(date, time, text[:-1], self.num_speak[speaker]))
	def __str__(self):
		string = ""
		for i in self.message_list:
			string += "{}|{}|{}|{}\n".format("/".join(stringify(i.date)), "".join(stringify(i.time), self.speakers[i.speaker_num], i.text))
		return string

def stats(i_chat):
	#smt - speaker message tally
	smt = [{'total_messages':0,'initiated':0,'ert':0, 'trt':0.0, 'trs': 0}]*len(i_chat.speakers)
	start_date = i_chat.message_list[0].date
	# print("start date:" + str(start_date))
	end_date = i_chat.message_list[-1].date
	#mmt - month message tally, key - (month,year), value - tally
	month_keys = [((i+start_date[0])%12 if (i+start_date[0])%12 != 0  else 12, start_date[2] + int((i+start_date[0]-1)/12)) for i in range((end_date[2]-start_date[2])*12+end_date[0]-start_date[0]+1)]
	mmt = {key: [0]*len(i_chat.speakers) for key in month_keys}
	# print(mmt)
	for i in i_chat.message_list:
		smt[i.speaker_num]['total_messages'] += 1
		mmt[(i.date[0], i.date[2])][i.speaker_num] += 1
	print(mmt)
	for sn, vals in enumerate(smt):
		speaker_name = i_chat.speakers[sn]
		print("Number of messages sent by %s: %d"%(speaker_name, vals['total_messages']))
		plt.plot(["%d/%d"%(key[0], key[1]) for key in month_keys], [mmt[key][sn] for key in month_keys], label = speaker_name)
		plt.legend()
	plt.show()
	# plt.savefig('chat_graph.png', bbox_inches = 'tight', dpi = 300, figsize = [1600, 1600])



#def reformat(messages):
	# mess_list = []
	# for i in messages:
	# 	if re.search("(\d\d|\d)/(\d\d|\d)/(\d\d|\d), (\d\d|\d):(\d\d|\d) (AM|PM) - (.*):", i):
	# 		date = i.split(",")[0]
	# 		if date:
	# 			date = list(map(lambda x: int(x), date.split("/")))
	# 		time = re.search("(\d\d|\d):(\d\d|\d) (AM|PM)", i)
	# 		if time:
	# 			time = time.group().split()
	# 			time[0] = list(map(lambda x: int(x),time[0].split(":")))
	# 			if time[1] == "PM":
	# 				time[0][0] += 12
	# 			time = time[0]
	# 		#Will bug a bit if somebodies name has a colon inside.....
	# 		speaker = re.search(" - (.*): ", i)
	# 		text = re.split("(.*): ", i, 1)[-1]
	# 		if speaker:
	# 			mess_list.append({"date":date, "time":time, "speaker":speaker.group()[3:-2], "text":text[:-1]})
	# return mess_list

x = chat(iotext)

# print(str(x))
stats(x)

# def stats(mess_list):
# 	time = {i:[0,0] for i in range(1,25)}
# 	for i in mess_list:

# for i in range(len(text)-1):
# 	if text[i] in word_dict:
# 		word_dict[text[i]].append(text[i+1])
# 	else:
# 		word_dict[text[i]] = [text[i+1]]
# word_dict[text[-1]] = random.choice(text)
# new_string = ""
# word = random.choice(list(word_dict.keys()))
# for i in range(new_text_length):
# 	word = random.choice(word_dict[word])
# 	new_string += word + " "

# print(new_string)
