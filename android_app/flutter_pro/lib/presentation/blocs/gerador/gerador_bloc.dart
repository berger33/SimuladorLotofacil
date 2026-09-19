import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';
import '../../../domain/entities/matriz.dart';
import '../../../domain/usecases/gerar_matriz.dart';
import '../../../services/ads_service.dart';
import '../../../services/iap_service.dart';

// Events
abstract class GeradorEvent extends Equatable {
  @override
  List<Object?> get props => [];
}

class GerarMatrizEvent extends GeradorEvent {
  final GerarMatrizParams params;
  GerarMatrizEvent(this.params);
  @override
  List<Object?> get props => [params];
}

class PararGeracaoEvent extends GeradorEvent {}
class PausarGeracaoEvent extends GeradorEvent {}

// States
abstract class GeradorState extends Equatable {
  @override
  List<Object?> get props => [];
}

class GeradorInitial extends GeradorState {}
class GeradorLoading extends GeradorState {
  final int geracao;
  final double score;
  GeradorLoading({this.geracao = 0, this.score = 0});
  @override
  List<Object?> get props => [geracao, score];
}
class GeradorProgress extends GeradorState {
  final Matriz matriz;
  final int geracaoAtual;
  final int maxGeracoes;
  GeradorProgress({required this.matriz, required this.geracaoAtual, required this.maxGeracoes});
  @override
  List<Object?> get props => [matriz, geracaoAtual, maxGeracoes];
}
class GeradorSuccess extends GeradorState {
  final Matriz matriz;
  GeradorSuccess(this.matriz);
  @override
  List<Object?> get props => [matriz];
}
class GeradorError extends GeradorState {
  final String message;
  GeradorError(this.message);
  @override
  List<Object?> get props => [message];
}
class GeradorPremiumRequired extends GeradorState {
  final String feature;
  GeradorPremiumRequired(this.feature);
  @override
  List<Object?> get props => [feature];
}

// Bloc
class GeradorBloc extends Bloc<GeradorEvent, GeradorState> {
  final GerarMatrizUseCase gerarMatrizUseCase;
  final AdsService adsService;
  final IAPService iapService;
  
  GeradorBloc({
    required this.gerarMatrizUseCase,
    required this.adsService,
    required this.iapService,
  }) : super(GeradorInitial()) {
    on<GerarMatrizEvent>(_onGerar);
    on<PararGeracaoEvent>(_onParar);
  }
  
  Future<void> _onGerar(GerarMatrizEvent event, Emitter<GeradorState> emit) async {
    try {
      // Checa premium
      final isPremium = await iapService.isPremium();
      
      if (!isPremium && event.params.numJogos > 10) {
        emit(GeradorPremiumRequired("Gerar ${event.params.numJogos} jogos é Pro. Free limita 10."));
        return;
      }
      
      if (!isPremium && (event.params.apriori || event.params.autoPiloto)) {
        emit(GeradorPremiumRequired("Apriori e Auto-Piloto são recursos Pro"));
        return;
      }
      
      // Mostra interstitial a cada 3 gerações se free
      if (!isPremium && adsService.shouldShowInterstitial()) {
        await adsService.showInterstitial();
      }
      
      emit(GeradorLoading());
      
      await for (final matriz in gerarMatrizUseCase.call(event.params)) {
        emit(GeradorProgress(
          matriz: matriz,
          geracaoAtual: matriz.geracao,
          maxGeracoes: event.params.maxGeracoes,
        ));
      }
      
      // Última matriz como sucesso
      if (state is GeradorProgress) {
        emit(GeradorSuccess((state as GeradorProgress).matriz));
      }
      
    } catch (e) {
      if (e.toString().contains("Free limita") || e.toString().contains("Pro")) {
        emit(GeradorPremiumRequired(e.toString()));
      } else {
        emit(GeradorError(e.toString()));
      }
    }
  }
  
  void _onParar(PararGeracaoEvent event, Emitter<GeradorState> emit) {
    emit(GeradorInitial());
  }
}
