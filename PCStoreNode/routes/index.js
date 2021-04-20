var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'PCStore' });
});

router.get('/all-products', function(req, res, next) {
  res.render('all-products', { title: 'PCStore - All Products' });
});

router.get('/single-product/:productID', function(req, res, next) {
  const productID = req.params.productID;
  res.render('product', {title: 'PCStore - Products', productID});
});

router.get('/account', function(req, res, next) {
  res.render('account', {title: 'User Home'});
});

router.get('/account/register', function(req, res, next) {
  res.render('register', {title: 'Registration'});
});

module.exports = router;
