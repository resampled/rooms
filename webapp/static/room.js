// this script runs only inside rooms & is deferred (runs AFTER fully loaded page)
// auto scroll to bottom of feed
const feed=document.getElementById("r-feed");
feed.scrollTop=feed.scrollHeight;
// dynamic feed refreshing (5 sec delay)
const delay = ms => new Promise(res => setTimeout(res, ms));
const dyn = new XMLHttpRequest();
dyn.onload = () => { rsp = dyn.responseXML.body.innerHTML; feed.innerHTML = rsp; }
function refresh() { let xhrurl = '/=/xhr_room_feed?r='+'qqz'; dyn.open('GET',xhrurl); dyn.responseType = 'document'; dyn.send(); }
i = 0;
window.onload = async () => { while (true) { await delay(5000); i += 1; console.log('refresh #'+i); refresh(); } }
