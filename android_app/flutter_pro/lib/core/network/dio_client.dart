import 'package:dio/dio.dart';

class DioClient {
  static Dio create({String baseUrl = 'https://api.lotofacilpro.com'}) {
    final dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 30),
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'LotofacilPro-Flutter/1.0.0 (Educational)',
        },
      ),
    );

    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          // Log request
          print('🌐 ${options.method} ${options.path}');
          return handler.next(options);
        },
        onResponse: (response, handler) {
          print('✅ ${response.statusCode} ${response.requestOptions.path}');
          return handler.next(response);
        },
        onError: (e, handler) {
          print('❌ ${e.message} ${e.requestOptions.path}');
          // Não falha, deixa repository fazer fallback local
          return handler.next(e);
        },
      ),
    );

    return dio;
  }
}
