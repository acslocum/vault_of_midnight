const express = require('express');
const app = express();
const port = 3000;
const PopeCookie = "PopeID";

const innocent = {
    PopeID: "205",
    name: "Innocent IV",
    holiness: 8,
    miracles: 7,
    wisdom: 7,
    legacy: 5,
    length_of_reign: 11,

  }

function lookupPope(PopeID) {
  return innocent;
}

function setPopeCookie(id, res) {
  res.cookie('PopeCookie', id);
  return lookupPope(id);
}

function getPopeFromCookie(res) {
  const popeid = res.cookie.PopeCookie;
  if(popeid === null) {
    return "You need to ascend to the papcy by scanning the QR code on the back of your lanyard.";
  }
  return lookupPope(popeid);
}

app.get('/pope/:id', (req, res) => {
  const PopeID = req.params.id;
  const pope = lookupPope(PopeID);
  res.send(`${JSON.stringify(pope)}`);
});

app.get('/register/:id', (req,res) => {
  const PopeID = req.params.id;
  const pope = setPopeCookie(PopeID);
  res.send(`You are ${pope.name}. Become the most powerful pope.`);
});

//Holiness	Miracles	Wisdom	Legacy
//8	7	7	5

app.get('/upgrade/holiness', (req,res) => {
  const pope = getPopeFromCookie(res);
  pope.holiness = 11;
  res.send(`${JSON.stringify(pope)}`);
})

app.get('/upgrade/miracles', (req,res) => {
  const pope = getPopeFromCookie(res);
  pope.miracles = 11;
  res.send(`${JSON.stringify(pope)}`);
})

app.get('/upgrade/wisdom', (req,res) => {
  const pope = getPopeFromCookie(res);
  pope.wisdom = 11;
  res.send(`${JSON.stringify(pope)}`);
})

app.get('/upgrade/legacy', (req,res) => {
  const pope = getPopeFromCookie(res);
  pope.legacy = 11;
  res.send(`${JSON.stringify(pope)}`);
})

app.get('/upgrade/all', (req,res) => {
  const pope = getPopeFromCookie(res);
  pope.holiness = 11;
  pope.miracles = 11;
  pope.wisdom = 11;
  pope.legacy = 11;
  res.send(`${JSON.stringify(pope)}`);
})



app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});

