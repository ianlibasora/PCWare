var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'PCStore' });
});

// Views for products
router.get('/all-products', function(req, res, next) {
  res.render('all-products', { title: 'PCStore - All Products' });
});

router.get('/single-product/:productID', function(req, res, next) {
  const productID = req.params.productID;
  res.render('product', {title: 'PCStore - Products', productID});
});

// User handling
router.get('/account', function(req, res, next) {
  res.render('account', {title: 'PCStore - User Home'});
});

router.get('/account/my-orders', function(req, res, next) {
  res.render('my-orders', {title: 'PCStore - My Orders'});
});

router.get('/account/my-orders/my-order-info/:orderID', function(req, res, next) {
  const orderID = req.params.orderID
  res.render('my-order-info', {"title": 'PCStore - My Order Info', orderID});
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

// Admin
router.get('/account/all-orders', function(req, res, next) {
  res.render('all-orders', {title: 'PCStore - All Orders'});
});

router.get('/account/all-orders/order-info/:orderID', function(req, res, next) {
  const orderID = req.params.orderID
  res.render('admin-order-info', {"title": 'PCStore - Admin Order Info', orderID});
});

// View basket
router.get('/basket/view-basket', function(req, res, next) {
  res.render('basket', {title: 'PCStore - Basket'});
});

module.exports = router;
