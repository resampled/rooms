Warning: This software is in *very* early alpha. Vital components are missing. At this stage, don't bother with this one. My apologies...

### But if you want to deploy this, anyway...
So far there are no human-friendly setup scripts or tutorials. Only those with patience and Django experience should proceed.

All required dependencies are listed in `requirements.txt`.

Please review the file `rooms/settings.py` and fill out your .env files accordingly. Feel free to change some of the settings to suit your deployment, especially those marked with the comment `# [change-me]`.

Our settings assume HTTP for DEBUG=True, and HTTPS w/ HSTS for DEBUG=False.

Deployment has not been tested, so you may also need to make some changes if/when errors occur. Crack the whole thing apart, if you need to.

