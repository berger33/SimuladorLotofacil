import 'dart:async';
import 'package:in_app_purchase/in_app_purchase.dart';
import 'package:hive_flutter/hive_flutter.dart';

class IAPService {
  final InAppPurchase _inAppPurchase = InAppPurchase.instance;
  late StreamSubscription<List<PurchaseDetails>> _subscription;
  
  static const String monthlyId = 'lotofacil_pro_monthly';
  static const String yearlyId = 'lotofacil_pro_yearly';
  static const String lifetimeId = 'lotofacil_pro_lifetime';
  
  static const Set<String> productIds = {monthlyId, yearlyId, lifetimeId};
  
  List<ProductDetails> _products = [];
  bool _isAvailable = false;
  bool _isPremium = false;
  
  Future<void> init() async {
    _isAvailable = await _inAppPurchase.isAvailable();
    if (!_isAvailable) return;
    
    // Carrega produtos
    var response = await _inAppPurchase.queryProductDetails(productIds);
    _products = response.productDetails;
    
    // Listener
    _subscription = _inAppPurchase.purchaseStream.listen(_onPurchase);
    
    // Restore
    await _inAppPurchase.restorePurchases();
    
    // Checa premium local
    var box = Hive.box('settings');
    _isPremium = box.get('is_premium', defaultValue: false);
    
    // Valida assinatura ativa (simplificado)
    // Em produção, validar com backend e Google Play Developer API
  }
  
  void _onPurchase(List<PurchaseDetails> purchases) {
    for (var purchase in purchases) {
      if (purchase.status == PurchaseStatus.purchased ||
          purchase.status == PurchaseStatus.restored) {
        _deliverPremium(purchase);
        if (purchase.pendingCompletePurchase) {
          _inAppPurchase.completePurchase(purchase);
        }
      } else if (purchase.status == PurchaseStatus.error) {
        // Tratar erro
      }
    }
  }
  
  Future<void> _deliverPremium(PurchaseDetails purchase) async {
    // Validação servidor aqui (ideal)
    var box = Hive.box('settings');
    await box.put('is_premium', true);
    await box.put('premium_product_id', purchase.productID);
    await box.put('premium_purchase_token', purchase.verificationData.serverVerificationData);
    _isPremium = true;
  }
  
  Future<bool> isPremium() async {
    var box = Hive.box('settings');
    return box.get('is_premium', defaultValue: false) || _isPremium;
  }
  
  List<ProductDetails> get products => _products;
  
  ProductDetails? getProduct(String id) {
    try {
      return _products.firstWhere((p) => p.id == id);
    } catch (_) {
      return null;
    }
  }
  
  Future<bool> buyMonthly() async {
    var product = getProduct(monthlyId);
    if (product == null) return false;
    var param = PurchaseParam(productDetails: product);
    return await _inAppPurchase.buyNonConsumable(purchaseParam: param);
  }
  
  Future<bool> buyYearly() async {
    var product = getProduct(yearlyId);
    if (product == null) return false;
    var param = PurchaseParam(productDetails: product);
    return await _inAppPurchase.buyNonConsumable(purchaseParam: param);
  }
  
  Future<bool> buyLifetime() async {
    var product = getProduct(lifetimeId);
    if (product == null) return false;
    var param = PurchaseParam(productDetails: product);
    return await _inAppPurchase.buyNonConsumable(purchaseParam: param);
  }
  
  Future<void> restore() async {
    await _inAppPurchase.restorePurchases();
  }
  
  void dispose() {
    _subscription.cancel();
  }
}
