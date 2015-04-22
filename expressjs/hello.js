var express = require('express');
var app = express();
app.engine('.html', require('jade'));
app.get('/', function(req, res){
  res.send('hello world');
});

app.get('/hello', function(req, res){
  res.render('index');
});

app.listen(3000);
