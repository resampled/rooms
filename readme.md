**rooms** is a Django web application for easy chatrooms. Significantly, user accounts are not required to join a room, while preserving  authenticity and moderation through the "namekey" system.

*Warning: This software is no longer being developed. Some complex components may need to be added in.*

## Features
### Namekeys
Before entering a room, users will enter two fields, "name" and "key".

"Name" is your display name, and "Key" is a secret field that generates a unique sha256 hash.

| name   | key    | chat display           |
| ------ | ------ | ---------------------- |
| lorem  | ipsum  | `<lorem [OoWEKagiuu..]>` |
| lorem  | dolor  | `<lorem [bvEdCbsdxK..]>` |
| ipsum  | dolor  | `<ipsum [v6ZIJCGrZM..]>` |

These namekeys are tied to your browser session. The same namekey works across rooms.

(The full hash can also be viewed in-app, but is displayed shortened in the chat window.)
### Edit code
When rooms are created, they require a strong *edit code*.

Anyone with the edit code can alter and moderate the room.

## Deployment
So far there are no human-friendly setup scripts or tutorials. Only those with patience and Django experience should proceed.

Please review the file `rooms/settings.py` and fill out your .env files accordingly. Feel free to change some of the settings to suit your deployment, especially those marked with the comment `# [change-me]`.

All required dependencies are listed in `requirements.txt`.

Static file handling is required (Whitenoise used). Default database is SQLite, but should work on other DBs (especially Postgres) without trouble.

Our settings assume HTTP for DEBUG=True, and HTTPS w/ HSTS for DEBUG=False.

Deployment has not been tested, so you may also need to make some changes if/when errors occur. Crack the whole thing apart, if you need to.

