const express = require('express');
const app = express();
const port = 8080;
let last_scanned = undefined;

app.get('/scan/:video', (req, res) => {
  last_scanned = req.params.video;
  res.send(`Your pathetic mind cannot comprehend what you are about to see.`);
});

app.get('/watch', (req,res) => {
  res.send(last_scanned);
  last_scanned = undefined;
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});