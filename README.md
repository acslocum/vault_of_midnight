# vault_of_midnight
VoM variant of big red button

Hitting the /scan url (scanning a QR code) sets a variable in server memory.
Hitting the /watch url (the button polls this) will get that variable *one time only*

The button code polls /watch and launches a video if there is a non-empty response from the server


TODO: what should the response be for scanning a video?