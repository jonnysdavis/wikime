import praw
from pygoogle import pygoogle
import urllib2

post = " "

def main(): 
	#Start Bot and Login
	r = praw.Reddit('Engage Bot')              
	r.login('wikime', 'PASSWORD')
	
	#While the bot is in alpha, it only works on a specified post as opposed to all of Reddit
	submission = r.get_submission(submission_id='POST NUMBER ID')
	
	flat_comments = praw.helpers.flatten_tree(submission.comments)
	already_done = set()
	
	for comment in flat_comments:
		if "wikime:" in comment.body and comment.id not in already_done:
			#Get their comment and find their search
			commentbody = comment.body
			print commentbody
			start = commentbody.find('wikime:')
			commentbody = commentbody[(start+7):]
			print commentbody
			#Get search link
			post = getpost(commentbody)
			comment.reply(post)
			already_done.add(comment.id)

#Create the post   
def getpost(name):
	searcht = name
	results = pygoogle(searcht + ' wikipedia')
	results.pages = 1
	links = results.get_urls()
	url = links[0]

	wikititle = arttitle(url)
	
	#Check if last char is a ) and fix link if needed
	if url[-1] == ')':
		url = url[:-1]
		url+='\)'
	
	print ('#Here is a Wikipedia link to [' + wikititle + '](' + url + ').\n\n^This ^message ^was ^created ^by ^a ^[bot](http://www.reddit.com/r/wikime/comments/1vweq5/what_is_this_bot/).')

	return ('#Here is a Wikipedia link to [' + wikititle + '](' + url + ').\n\n^This ^message ^was ^created ^by ^a ^[bot](http://www.reddit.com/r/wikime/comments/1vweq5/what_is_this_bot/).')

#Get the Wikipedia article title
def arttitle(wikipage):
	req = urllib2.Request(wikipage,headers={'User-Agent' : "Magic Browser"}) 
	con = urllib2.urlopen(req)
	page = con.read()
	titlestart = page.find('<title>')
	titleend = page.find('- Wikipedia,')
	#Gets just the title of the article
	fulltitle = page[titlestart+7:titleend-1]

	return fulltitle
	
	
	
if __name__ == '__main__':
	main()
