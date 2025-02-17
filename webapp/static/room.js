// this script runs only inside rooms & is deferred (runs AFTER fully loaded page)
// auto scroll to bottom of feed
const feed=document.getElementById("r-feed");
feed.scrollTop=feed.scrollHeight;
