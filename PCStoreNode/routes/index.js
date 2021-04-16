var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'PCStore' });
});

router.get('/all-products', function(req, res, next) {
  res.render('all-products', { title: 'PCSTore - All Products' });
});

module.exports = router;
