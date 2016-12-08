import os

dirs = [x[0] for x in os.walk("reuters_data")]

def get_files_count(directory):
	dirs = [x[0] for x in os.walk(directory)]
	results =[]
	for i in range(1, len(dirs)):
		dir = dirs[i]
		size = len(os.listdir(dir))
		results.append((dir, size))
	return results

counters = get_files_count("reuters_data")

print counters 
print(filter(lambda (x,y): y > 100, counters))