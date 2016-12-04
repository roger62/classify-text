import os

def write_to_file(file_id, topic, content):

	if not topic:
		topic = "misc"

	filename = "reuters_data/"+topic+"/"+str(file_id)+".txt" 
	#print filename
	create_dir(filename)

	f = open(filename, 'w')

	for line in content:
		f.write(line)
	f.close()


def create_dir(filename):
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

def parse_topics(topics):

	topics = topics.replace("<TOPICS>","")
	topics = topics.replace("</TOPICS>","")
	filtered_topics = []

	if topics:
		all_topics = topics.split("</D>")
		for topic in all_topics:
			topic = topic.replace("<D>", "")
			if '\n' not in topic:
				filtered_topics.append(topic)

	return filtered_topics


def add_topics_to_counter(counter, topics):

	for topic in topics:

		if topic in counter:
			counter[topic] += 1
		else:
			counter[topic] = 1

	return counter

def parse_file(id, topic_counter, file):
		
	f = open(file)

	line = f.readline();

	doc_content = []
	topics = []

	while line:
		doc_content.append(line)
		if  line == "</REUTERS>\n" :
			#print "going to write"
			#print topics
			if not topics:
				topics = ["misc"]

			for topic in topics:
				id+=1
				write_to_file(id, topic, doc_content)
			doc_content = []
			topics = []

		if "<TOPICS>" in line:
			topics = parse_topics(line)

			if topics:
				counter = add_topics_to_counter(topic_counter, topics)


		line = f.readline()

	f.close()

topic_counter = {}
file_id  = 0
for i in range(0, 21):
	file = ""
	
	if i < 10:
		file = "reuters/reut2-00{}.sgm".format(i)
	else:
		file = "reuters/reut2-0{}.sgm".format(i)

	parse_file(file_id, topic_counter, file)

print file_id