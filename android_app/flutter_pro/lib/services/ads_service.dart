import 'package:google_mobile_ads/google_mobile_ads.dart';
import 'dart:async';

class AdsService {
  BannerAd? _bannerAd;
  InterstitialAd? _interstitialAd;
  RewardedAd? _rewardedAd;
  
  int _geracoesDesdeUltimoInterstitial = 0;
  bool _isInterstitialReady = false;
  bool _isRewardedReady = false;
  
  // Teste IDs - trocar por produção
  static const String bannerAdUnitId = 'ca-app-pub-3940256099942544/6300978111';
  static const String interstitialAdUnitId = 'ca-app-pub-3940256099942544/1033173712';
  static const String rewardedAdUnitId = 'ca-app-pub-3940256099942544/5224354917';
  
  Future<void> init() async {
    await MobileAds.instance.initialize();
    await _loadInterstitial();
    await _loadRewarded();
  }
  
  BannerAd createBanner() {
    _bannerAd = BannerAd(
      adUnitId: bannerAdUnitId,
      size: AdSize.banner,
      request: const AdRequest(),
      listener: BannerAdListener(
        onAdFailedToLoad: (ad, error) {
          ad.dispose();
        },
      ),
    )..load();
    return _bannerAd!;
  }
  
  Future<void> _loadInterstitial() async {
    await InterstitialAd.load(
      adUnitId: interstitialAdUnitId,
      request: const AdRequest(),
      adLoadCallback: InterstitialAdLoadCallback(
        onAdLoaded: (ad) {
          _interstitialAd = ad;
          _isInterstitialReady = true;
        },
        onAdFailedToLoad: (error) {
          _isInterstitialReady = false;
        },
      ),
    );
  }
  
  Future<void> _loadRewarded() async {
    await RewardedAd.load(
      adUnitId: rewardedAdUnitId,
      request: const AdRequest(),
      rewardedAdLoadCallback: RewardedAdLoadCallback(
        onAdLoaded: (ad) {
          _rewardedAd = ad;
          _isRewardedReady = true;
        },
        onAdFailedToLoad: (error) {
          _isRewardedReady = false;
        },
      ),
    );
  }
  
  bool shouldShowInterstitial() {
    _geracoesDesdeUltimoInterstitial++;
    if (_geracoesDesdeUltimoInterstitial >= 3) {
      _geracoesDesdeUltimoInterstitial = 0;
      return _isInterstitialReady;
    }
    return false;
  }
  
  Future<void> showInterstitial() async {
    if (_isInterstitialReady && _interstitialAd != null) {
      await _interstitialAd!.show();
      _isInterstitialReady = false;
      _interstitialAd = null;
      await _loadInterstitial();
    }
  }
  
  Future<bool> showRewarded() async {
    if (!_isRewardedReady || _rewardedAd == null) {
      await _loadRewarded();
      return false;
    }
    
    bool completed = false;
    Completer<bool> completer = Completer();
    
    _rewardedAd!.fullScreenContentCallback = FullScreenContentCallback(
      onAdDismissedFullScreenContent: (ad) {
        ad.dispose();
        _loadRewarded();
        if (!completer.isCompleted) completer.complete(completed);
      },
      onAdFailedToShowFullScreenContent: (ad, error) {
        ad.dispose();
        _loadRewarded();
        if (!completer.isCompleted) completer.complete(false);
      },
    );
    
    await _rewardedAd!.show(
      onUserEarnedReward: (ad, reward) {
        completed = true;
      },
    );
    
    return completer.future;
  }
  
  void dispose() {
    _bannerAd?.dispose();
    _interstitialAd?.dispose();
    _rewardedAd?.dispose();
  }
}
