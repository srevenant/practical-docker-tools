var app = require('express')()
app.get('/hello', function (req, res) {
  res.send('World\n')
  console.log(req.ip + ' ' + req.method + ' ' + req.originalUrl)
});
app.listen(process.env.PORT)
console.log('Started on port ' + process.env.PORT)
