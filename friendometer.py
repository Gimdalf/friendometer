import re
import random
# new_text_length = int(input("New text length:\n"))
# text = input().split()
filename = input("Chat history filename: \n")
iotext = open("%s"%(filename), "r", encoding="utf8")
import matplotlib.pyplot as plt
# text = iotext.read().split()
from datetime import datetime, date, timedelta

word_dict = {}

#Things to do:
#1. Use python datetime instead of tuples to store dates?
#2. Possible stats: Texting times, messages sent, messages sent over time

def stringify(l):
	return list(map(lambda x: str(x), l))

def intify(l):
	return map(lambda x: int(x), l)

class message:
	def __init__(self, dt, text, speaker_num):
		self.dt = dt
		self.text = text
		self.speaker_num = speaker_num

class chat:
	def __init__(self, chat_text):
		self.message_list = []
		self.speakers = [] #speakers is integer -> speaker name
		self.num_speak = {} #num_speak is name -> integer
		for i in chat_text:
			if re.search("(\d\d|\d)/(\d\d|\d)/(\d\d|\d), (\d\d|\d):(\d\d|\d) (AM|PM) - (.*):", i):
				i = i.split(" - ")
				dt = datetime.strptime(i[0], "%m/%d/%y, %I:%M %p")
				speaker = i[1].split(": ")[0]
				text = "".join(i[1].split(": ")[1:])
				if speaker:
					if speaker in self.num_speak:
						self.message_list.append(message(dt, text[:-1], self.num_speak[speaker]))
					else:
						print(i)
						self.num_speak[speaker] = len(self.speakers)
						self.speakers.append(speaker)
						self.message_list.append(message(dt, text[:-1], self.num_speak[speaker]))
	def __str__(self):
		string = ""
		for i in self.message_list:
			string += "{}|{}|{}\n".format(i.dt.strftime("%d/%m/%y %H:%M"), self.speakers[i.speaker_num], i.text)
		return string

def stats(i_chat):
	#smt - speaker message tally
	start_time = i_chat.message_list[0].dt 
	#ert - Earliest Response Time, trt - Total Response Time, trs - Total ResponseS
	smt = [{'total_messages':0,'initiated':0,'ert':start_time, 'trt':timedelta(), 'trs': 0} for i in range(len(i_chat.speakers))]
	# print("start date:" + str(start_time))
	end_time = i_chat.message_list[-1].dt
	#mmt - month message tally, key - (month,year), value - tally
	month_keys = [((i+start_time.month)%12 if (i+start_time.month)%12 != 0  else 12, start_time.year + int((i+start_time.month-1)/12)) for i in range((end_time.year-start_time.year)*12+end_time.month-start_time.month+1)]
	mmt = {key: [0]*len(i_chat.speakers) for key in month_keys}
	# print(mmt)
	#p_speak - previous speaker
	p_speak = i_chat.message_list[0].speaker_num
	p_time = start_time
	for i in i_chat.message_list:
		speaker = i.speaker_num
		if speaker != p_speak:
			smt[speaker]['trt'] += (i.dt - smt[speaker]['ert'])
			smt[speaker]['trs'] += 1 
			smt[p_speak]['ert'] = i.dt
			p_speak = speaker
		#6 hours parameter was chosen arbitrarily
		if (i.dt - p_time) > timedelta(hours = 6):
			smt[speaker]['initiated'] += 1
		p_time = i.dt
		smt[speaker]['total_messages'] += 1
		mmt[(i.dt.month, i.dt.year)][speaker] += 1
	for sn, vals in enumerate(smt):
		speaker_name = i_chat.speakers[sn]
		#art - average response time
		art = (vals['trt'] + (end_time - vals['ert']))/vals['trs']
		print("%s: \nNumber of messages sent: %d\nAverage Response time: %s\nConversations initiated: %d\n"%(speaker_name, vals['total_messages'], str(art), vals['initiated']))
		plt.plot(["%d/%d"%(key[0], key[1]) for key in month_keys], [mmt[key][sn] for key in month_keys], label = speaker_name)
		plt.legend()
	plt.show()
	# plt.savefig('chat_graph.png', bbox_inches = 'tight', dpi = 300, figsize = [1600, 1600])

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