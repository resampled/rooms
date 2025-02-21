// this script runs only inside rooms & is deferred (runs AFTER fully loaded page)
// auto scroll to bottom of feed
const feed=document.getElementById("r-feed");
feed.scrollTop=feed.scrollHeight;
// dynamic feed refreshing (5 sec delay)
const delay = ms => new Promise(res => setTimeout(res, ms));
const dyn = new XMLHttpRequest();
dyn.onload = () => { rsp = dyn.responseXML.body.innerHTML; feed.innerHTML = rsp; }
function refresh() { let xhrurl = getXhrUrl(); dyn.open('GET',xhrurl); dyn.responseType = 'document'; dyn.send(); }
function getXhrUrl() { const rm=document.getElementById("var_room"); return '/=/xhr_room_feed?r='+rm.getAttribute("content"); }
i = 0;
window.onload = async () => { while (true) { await delay(5000); i += 1; console.log('GET '+getXhrUrl()+' '+i); refresh(); } }
