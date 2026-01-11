const express = require('express');
const app = express();
const port = 8080;
let last_scanned = undefined;

const phrases = ["Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn", 
  "We live on a placid island of ignorance... amid black seas of infinity, and it was not meant that we should voyage far.", 
  "The oldest and strongest emotion of mankind is fear, and the oldest and strongest kind of fear is fear of the unknown.", 
  "The Old Ones were, the Old Ones are, and the Old Ones shall be.", 
  "The stars are right.",
  "Who knows the end? What has risen may sink, and what has sunk may rise. Loathsomeness waits and dreams in the deep, and decay spreads over the tottering cities of men.",
  "The sciences, each straining in its own direction, have hitherto harmed us little; but some day the piecing together of dissociated knowledge will open up such terrifying vistas of reality, and of our frightful position therein, that we shall either go mad from the revelation or flee from the deadly light into the peace and safety of a new dark age.",
  "If I say that my somewhat extravagant imagination yielded simultaneous pictures of an octopus, a dragon, and a human caricature, I shall not be unfaithful to the spirit of the thing. A pulpy, tentacled head surmounted a grotesque and scaly body with rudimentary wings; but it was the general outline of the whole which made it most shockingly frightful.",
  "The world is indeed comic, but the joke is on mankind.",
  "The most merciful thing in the world is the inability of the human mind to correlate all its contents. We live on a placid island of ignorance in the midst of black seas of the infinity, and it was not meant that we should voyage far.",
  "Ultimate horror often paralyses memory in a merciful way.",

]

function response_quote() {
  return `<div style="font-size: 80px;">${phrases[Math.floor(Math.random() * phrases.length)]}</div>`
};

app.get('/scan/:video', (req, res) => {
  last_scanned = req.params.video;
  res.send(response_quote());
});

app.get('/debug/:file', (req, res) => {
  last_scanned = req.params.file;
  res.send('Received ' + last_scanned);
  console.log('Received debug: ' + last_scanned)
});

app.get('/watch', (req,res) => {
  res.send(last_scanned);
  last_scanned = undefined;
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});