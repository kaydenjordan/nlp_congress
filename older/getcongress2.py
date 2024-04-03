#Packages needed
import re, urllib, sys, os, datetime, urllib2
from itertools import islice
#Open getcongress2.py and change filenames on lines 17,23,92,109,120

###Examples of url
# http://www.gpo.gov/fdsys/pkg/CREC-2015-01-02/html/CREC-2015-01-02-pt1-PgH10327-2.htm
# http://www.gpo.gov/fdsys/pkg/CREC-2015-01-02/html/CREC-2015-01-02-pt1-PgH10327-3.htm
# http://www.gpo.gov/fdsys/pkg/CREC-2015-01-02/html/CREC-2015-01-02-pt1-PgH10327-4.htm
# http://www.gpo.gov/fdsys/pkg/CREC-2015-01-02/html/CREC-2015-01-02-pt1-PgS6935-2.htm
#http://www.gpo.gov/fdsys/pkg/CREC-2010-01-15/html/CREC-2010-01-15-pt1-PgE32-2.htm
# prac = urllib.urlopen("http://www.gpo.gov/fdsys/pkg/CREC-2015-01-02/html/CREC-2015-01-02-pt1-PgS6937.htm").read()
# print prac
#http://www.gpo.gov/fdsys/pkg/CREC-2017-01-03/html/CREC-2017-01-03-pt1-PgH28.htm
loop = range(1,2)
try:
	folder = "C:/Users/knj543/Desktop/Test/2017/" 
	os.makedirs(folder)
except:
	print("Already exists")


with open("D:/Dropbox/2017 urls.txt", "rb") as f:
	links = []
	for l in f:
		if ".htm" in l:
			print(l)
			if ("PgH" in l or "PgS" in l):
				if l not in links:
					links.append(l)

g = open("D:/Dropbox/programs/congressjunk.txt", "rb")
junk = g.read()

id =0
badspeech=False
newspeaker=False
dir = 1
n = 1
basedir = "C:/Users/knj543/Desktop/Test/2017/"

for link in links:
	speaker = None
	speech = []
	next = True
	url = "http://www.gpo.gov/fdsys/pkg/"+ link
	print(link)
	data = urllib2.urlopen(url, timeout=100)
	# try:
		# preview = urllib.urlopen(url)
		# print "Success"
	# except:
		# print "Error in url-1", url
		# continue
	# for j in junk:
		# if j in preview:
			# badspeech = True
			# continue
	# if badspeech is True:
		# continue
	try:
		data = urllib2.urlopen(url, timeout=100)
		print("Parsing")
	except:
		print("Error in url: ", url)
		continue
	id = id+1
	lineno=0
	match = 0
	for line in data:
		lineno+=1
		print(lineno)
		if lineno<6 or (lineno>8 and lineno<13):
			continue
		if lineno==6:
			date = re.findall("\(.+?,\s(.+?)\)", line)
			date = (str(date))[2:len(date)-3]
			print(date)
		if lineno==7:
			chamber = str((str(line))[1:len(line)-2])
			print(chamber)
		if lineno<16:
			if re.match("\s*[A-Z]+", line):
				content = line.replace(" ", "")
				content = line.replace("\n", "")
				content = content.strip(" ")
				content = re.sub("\/", " ", content)
				content = re.sub("[?\.!\,:\;\"]", "",content)
				
		if re.match("^\[\[", line) or re.match("^\[", line) or re.match("^\(", line):
			continue
		#Ms. Jackson Lee
		if speech:
			if re.match("^\s\sMr\.\s[A-Za-z-]*\.", line) or re.match("^\s\sMrs\.\s[A-Za-z-]*\.", line) or re.match("^\s\sMs\.\s[A-Za-z-]*\.", line) or re.match("^\s\sMr\.\s[A-Za-z-]*\s[a-z][a-z]\s[A-Za-z]*\.", line) or re.match("^\s\sMrs\.\s[A-Za-z-]*\s[a-z][a-z]\s[A-Za-z]*\.", line) or re.match("^\s\sMs\.\s[A-Za-z-]*\s[a-z][a-z]\s[A-Za-z]*\.", line) or re.match("^\s\sMs\.[A-Za-z]*\s[A-Za-z]*\.", line):
				print("New Speech")
				if (speaker is not None) and (content not in junk) and (chamber!="Extensions of Remarks"):
					filename = basedir+str(date)+"." +str(speaker) +"." +str(chamber) + "." +str(content) + ".txt"
					with open(filename, "ab") as output:
						for x in speech:
							output.write(x)
						n = n+1
				speech = []
				#print speech
				speaker = re.findall("^.*?\.\s([A-Za-z-]*\s[a-z][a-z]\s[A-Za-z]*)\.", line)
				if not speaker:
					speaker = re.findall("^.*?\.\s([A-Za-z-]*)\.", line)
				speaker = str(speaker)[2:len(speaker)-3]
				line = re.sub("^.*?\.\s([A-Za-z-]*)\.", "",line)
				speech.append(line)
				
			elif re.match("^\s*The VICE", line) or re.match("^\s*The Acting", line) or re.match("^\s*The PRESIDING", line) or re.match("^\s*The CLERK", line) or re.match("\[Roll No\. 211\]", line) or re.match("\s*The SPEAKER", line):
				print("Bureaucratic Bullshit")
				if (speaker is not None) and (content not in junk) and (chamber!="Extensions of Remarks"):
					filename = basedir+str(date)+"." +str(speaker) +"." +str(chamber) + "." +str(content) + ".txt"
					with open(filename, "ab") as output:
						for x in speech:
							output.write(x)
						n = n+1
				speech = []
				#print speech
				continue
			elif re.match("^<\/pre><\/body>", line):
				print("End of file")
				if (speaker is not None) and (content not in junk) and (chamber!="Extensions of Remarks"):
					filename = basedir+str(date)+"." +str(speaker) +"." +str(chamber) + "." +str(content) + ".txt"
					with open(filename, "ab") as output:
						for x in speech:
							output.write(x)
						n = n+1
				speech = []
				#print speech
				continue
			else:
				#print "Just another line"
				if re.match("^\s\s\s\s", line) or re.match("^<", line):
					continue
				speech.append(line)
		else:
			if re.match("^\s\sMr\.\s[A-Za-z-]*\.", line) or re.match("^\s\sMrs\.\s[A-Za-z-]*\.", line) or re.match("^\s\sMs\.\s[A-Za-z-]*\.", line)or re.match("^\s\sMr\.\s[A-Za-z-]*\s[a-z][a-z]\s[A-Za-z]*\.", line) or re.match("^\s\sMrs\.\s[A-Za-z-]*\s[a-z][a-z]\s[A-Za-z]*\.", line) or re.match("^\s\sMs\.\s[A-Za-z-]*\s[a-z][a-z]\s[A-Za-z]*\.", line) or re.match("^\s\sMs\.[A-Za-z]*\s[A-Za-z]*\.", line):
				print("New speaker")
				speaker = re.findall("^.*?\.\s([A-Za-z-]*\s[a-z][a-z]\s[A-Za-z]*)\.", line)
				if not speaker:
					speaker = re.findall("^.*?\.\s([A-Za-z-]*)\.", line)
				speaker = str(speaker)[2:len(speaker)-3]
				line = re.sub("^.*?\.\s([A-Za-z-]*)\.", "",line)
				if re.match("^\s\s\s\s", line) or re.match("^<", line):
					continue
				speech.append(line)	
		# if re.match("^\s\sMr\.\s[A-Za-z-]*\.", line) or re.match("^\s\sMrs\.\s[A-Za-z-]*\.", line) or re.match("^\s\sMs\.\s[A-Za-z-]*\.", line):
			# match += 1
			# newspeaker = True
			# if speech and filewritten is True:
				# print "Not empty"
				# if speaker is not None and content not in junk and chamber!="Extensions of Remarks":
					# filename = "D://Desktop/congress prac/2014clean/" + str(date)+ str(speaker) +str(chamber) + str(content) + ".txt"
					# with open(filename, "ab") as output:
						# for line in speech:
							# output.write(line)
						# print "File written", filename
						# filewritten = True
						# next = False
				# speech = []
			# speaker = re.findall("^.*?\.\s([A-Za-z-]*)\.", line)
			# #speaker = speaker[0]
			# print speaker			
		# #((((((Mr)|(Ms)|(Mrs))\. [A-Za-z \-]+(of [A-Z][a-z]+)?)|((The (VICE |Acting |ACTING )?(PRESIDENT|SPEAKER)( pro tempore)?)|(The PRESIDING OFFICER)|(The CLERK))( \([A-Za-z.\- ]+\))?))\. )?(?P<start>.)
		# if re.match("^\s*The VICE", line) or re.match("^\s*The Acting", line) or re.match("^\s*The PRESIDING", line) or re.match("^\s*The CLERK", line):
			# newspeaker=False
			# if speaker is not None and content not in junk and chamber!="Extensions of Remarks":
				# filename = "D://Desktop/congress prac/2014clean/" + str(date)+ str(speaker) +str(chamber) + str(content) + ".txt"
				# with open(filename, "ab") as output:
					# for line in speech:
						# output.write(line)
					# print "File written", filename
					# filewritten = True
					# next = False
			# speech = []
			# continue
		# if newspeaker is True:
			# if re.match("^\s\s\s\s", line) or re.match("^<", line):
				# continue
			# speech.append(line)
		# if next is True:
			# filewritten = False
	# if speaker is not None and content not in junk and chamber!="Extensions of Remarks":
		# filename = "D://Desktop/congress prac/2014clean/" + str(date)+ str(speaker) +str(chamber) + str(content) + ".txt"
		# with open(filename, "ab") as output:
			# for x in speech:
				# output.write(x)
			# print "File written", filename
		# newspeaker=False
		