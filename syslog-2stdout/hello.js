var app = require('express')()
app.get('/hello', function (req, res) {
  res.send('World with a Redeploy\n');
});
app.listen(process.env.PORT)
console.log('Started on port ' + process.env.PORT)
