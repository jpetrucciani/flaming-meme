import time
import praw
import wget
import re
import os
import sys
if len(sys.argv) != 4:
  print "USAGE ERROR: rid.py [subreddit] [top/hot] [limit]"
  exit()
sub = sys.argv[1]
toh = sys.argv[2]
lim = sys.argv[3]
pathex = os.path.exists(os.getcwd()+"/"+sub+"/")
if pathex == False:
    mkd = os.makedirs(os.getcwd()+"/"+sub+"/")
r = praw.Reddit(user_agent="kekkeroni downloader")
already_done = []
checkWords = ['i.imgur.com', 'jpg', 'png', 'gif', 'gfycat.com', 'webm',]
gyfwords = ['gfycat.com']
while True:
    subreddit = r.get_subreddit(sub)
    if toh == 'hot' :
      subs = subreddit.get_hot(limit=lim)
    else: 
      subs = subreddit.get_top(limit=lim)
    for submission in subs:
        url_text = submission.url
        has_domain = any(string in url_text for string in checkWords)
        #print '[LOG] Getting url:  ' + url_text
        is_gifcat = any(string in url_text for string in gyfwords)
        if submission.id not in already_done and has_domain:
           if is_gifcat:
              url = re.sub('http://.*gfycat.com/', '', url_text)
              url_text = 'http://giant.gfycat.com/' + url + '.gif' 
           wget.download(url_text, os.getcwd()+"/"+sub+"/" + str(time.time())[-8:-3] + url_text[-4:])
           already_done.append(submission.id)
           #print '[LOG] Done Getting ' + url_text
    exit()