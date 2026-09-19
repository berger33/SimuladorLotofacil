import 'package:flutter/material.dart';

class AppColors {
  // Brand - Pixel Perfect from screenshots 01-09
  static const primary = Color(0xFF7C3AED);
  static const primaryLight = Color(0xFF8B5CF6);
  static const primaryLighter = Color(0xFFA855F7);
  static const primaryDark = Color(0xFF5B21B6);
  static const primaryDarker = Color(0xFF4C1D95);
  static const secondary = Color(0xFF0EA5E9);
  static const secondaryLight = Color(0xFF06B6D4);
  static const tertiary = Color(0xFFFFD700);
  static const tertiaryLight = Color(0xFFFFE55C);
  static const gold = Color(0xFFFFD700);
  static const goldDark = Color(0xFFFFA500);

  // Semantic - matching badges ALTA/MEDIA/BAIXA
  static const success = Color(0xFF10B981);
  static const successLight = Color(0xFF22C55E);
  static const warning = Color(0xFFF97316);
  static const warningLight = Color(0xFFFB923C);
  static const error = Color(0xFFEF4444);
  static const errorLight = Color(0xFFF43F5E);
  static const info = Color(0xFF0EA5E9);
  static const infoLight = Color(0xFF06B6D4);
  static const blue = Color(0xFF0EA5E9);
  static const orange = Color(0xFFF97316);
  static const yellow = Color(0xFFEAB308);

  // Dark - #0A0A0F background from screenshots
  static const background = Color(0xFF0A0A0F);
  static const background2 = Color(0xFF12121A);
  static const backgroundDark = Color(0xFF0A0A0F);
  static const surfaceDark = Color(0xFF1A1D29);
  static const surface2 = Color(0xFF1E202E);
  static const surface3 = Color(0xFF222538);
  static const surfaceVariantDark = Color(0xFF2D2D3F);
  static const border = Color(0xFF2D2D3F);
  static const border2 = Color(0xFF3F3F5A);
  static const onBackgroundDark = Color(0xFFE0E0E0);
  static const onSurfaceDark = Color(0xFFFFFFFF);
  static const textSecondary = Color(0xFF9CA3AF);
  static const textTertiary = Color(0xFF6B7280);

  // Light
  static const backgroundLight = Color(0xFFFAFAFA);
  static const surfaceLight = Color(0xFFFFFFFF);
  static const surfaceVariantLight = Color(0xFFF0F0F0);
  static const onBackgroundLight = Color(0xFF121212);

  // Heatmap - Fria → Muito Quente from screenshots
  static const heatFria = Color(0xFF1E3A8A);
  static const heatFria2 = Color(0xFF2563EB);
  static const heatMedia = Color(0xFF3730A3);
  static const heatMedia2 = Color(0xFF6D28D9);
  static const heatQuente = Color(0xFFFB923C);
  static const heatMuitoQuente = Color(0xFFEF4444);
  static const heatCold = Color(0xFF1E3A8A);
  static const heatWarm = Color(0xFFFB923C);
  static const heatHot = Color(0xFFF97316);
  static const heatBurn = Color(0xFFEF4444);

  // Gradients - Pixel perfect from Top Score card
  static const gradientPrimary = LinearGradient(
    colors: [Color(0xFF7C3AED), Color(0xFF6D28D9), Color(0xFF4C1D95), Color(0xFF1E1B4B)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  static const gradientTopScore = LinearGradient(
    colors: [Color(0xFF7C3AED), Color(0xFF6D28D9), Color(0xFF4C1D95), Color(0xFF1E1B4B)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  static const gradientGold = LinearGradient(
    colors: [Color(0xFFFFD700), Color(0xFFFFA500)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  static const gradientSuccess = LinearGradient(
    colors: [Color(0xFF10B981), Color(0xFF059669)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  static const gradientPremium = LinearGradient(
    colors: [Color(0xFF1A1A2E), Color(0xFF0F0F1A)],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );
  static const gradientHeatFria = LinearGradient(
    colors: [Color(0xFF1E40AF), Color(0xFF1D4ED8)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  static const gradientHeatMuitoQuente = LinearGradient(
    colors: [Color(0xFFDC2626), Color(0xFFEF4444)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
}
