const express = require('express');
const fs = require('fs');
const cors = require('cors');
const app = express();

app.use(express.json());
app.use(cors());

app.post('/api/code', async (req, res)  => {
  //console.log(req.body);
  fs.writeFile('code.py', req.body.code, () => {
    console.log("File Saved");
  });
  res.send({stdout : output});
});

app.listen(3000, () => {
  console.log("App started on PORT 3000");
});