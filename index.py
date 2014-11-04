import praw
import random
import json

DEFAULT_SUB = 'funny'
SUBS = 3
USERS_PER_SUB = 40
COMMENTS_PER_USER = 25


r = praw.Reddit(user_agent='EE126')
currSub = r.get_subreddit(DEFAULT_SUB)
used = {}
totalVal = {}


for i in xrange(SUBS):
	data = {}
	used[str(currSub)] = True
	print ('currently working on ' + str(currSub))
	data[str(currSub)] = {}
	currSub_comments = currSub.get_comments(limit = USERS_PER_SUB)

	for comment in currSub_comments:
		auth = comment.author
		refComments = auth.get_comments(limit = COMMENTS_PER_USER)

		for comment in refComments:
			if (str(comment.subreddit) in data[str(currSub)]):
				data[str(currSub)][str(comment.subreddit)] += 1
				totalVal[str(comment.subreddit)] += 1
			else:
				if (str(comment.subreddit) in totalVal):
					totalVal[str(comment.subreddit)] += 1
				else:
					totalVal[str(comment.subreddit)] = 1
				data[str(currSub)][str(comment.subreddit)] = 1

	#SAVE DATA
	with open('data/' + str(currSub) + '.json', 'w') as outfile:
  		json.dump(data[str(currSub)], outfile)

	nextSubVal = 0
	nextSub = None
	for sub in totalVal:
		if (str(sub) not in used):
			if (totalVal[sub] > nextSubVal):
				nextSub = sub
				nextSubVal = totalVal[sub]
	if (nextSub):
		currSub = r.get_subreddit(nextSub)
	else:
		break

	#SAVE OUR WORK SO THAT WE CAN RESUME IF IT CRASHES (REALLY DON'T WANT TO RESTART)
	if (i % 5 == 0):
		with open('data/saveWork.json', 'w') as outfile:
			json.dump([used, totalVal, nextSub], outfile)



