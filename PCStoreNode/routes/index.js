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
  res.render('account', {title: 'PCStore - User Home'});
});

router.get('/account/register', function(req, res, next) {
  res.render('register', {title: 'PCStore - Registration'});
});

router.get('/account/login', function(req, res, next) {
  res.render('login', {title: 'PCStore - Login'});
});

router.get('/account/logout', function(req, res, next) {
  res.render('logout');
});

router.get('/basket/view-basket', function(req, res, next) {
  res.render('basket', {title: 'PCStore - Basket'});
});

module.exports = router;
