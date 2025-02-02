**rooms** is a Django web application for easy chatrooms. Significantly, user accounts are not required to join a room, while preserving  authenticity and moderation. - managed through the "namekey" system.

*Warning: This software is in alpha. Certain components are missing.*

## Features

## Deployment
So far there are no human-friendly setup scripts or tutorials. Only those with patience and Django experience should proceed.

Please review the file `rooms/settings.py` and fill out your .env files accordingly. Feel free to change some of the settings to suit your deployment, especially those marked with the comment `# [change-me]`.

All required dependencies are listed in `requirements.txt`.

Our settings assume HTTP for DEBUG=True, and HTTPS w/ HSTS for DEBUG=False.

Deployment has not been tested, so you may also need to make some changes if/when errors occur. Crack the whole thing apart, if you need to.

