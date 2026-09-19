import 'package:flutter/material.dart';

class AppColors {
  // Brand
  static const primary = Color(0xFF6F42C1);
  static const primaryLight = Color(0xFF9A6BFF);
  static const primaryDark = Color(0xFF4A1A8B);
  static const secondary = Color(0xFF17A2B8);
  static const secondaryLight = Color(0xFF5ED5E8);
  static const tertiary = Color(0xFFFFD700);
  static const tertiaryLight = Color(0xFFFFE55C);

  // Semantic
  static const success = Color(0xFF28A745);
  static const warning = Color(0xFFFFC107);
  static const error = Color(0xFFDC3545);
  static const info = Color(0xFF0DCAF0);

  // Dark
  static const backgroundDark = Color(0xFF121212);
  static const surfaceDark = Color(0xFF1E1E1E);
  static const surfaceVariantDark = Color(0xFF2D2D2D);
  static const onBackgroundDark = Color(0xFFE0E0E0);
  static const onSurfaceDark = Color(0xFFFFFFFF);

  // Light
  static const backgroundLight = Color(0xFFFAFAFA);
  static const surfaceLight = Color(0xFFFFFFFF);
  static const surfaceVariantLight = Color(0xFFF0F0F0);
  static const onBackgroundLight = Color(0xFF121212);

  // Heatmap
  static const heatCold = Color(0xFF4DABF7);
  static const heatWarm = Color(0xFFFFC107);
  static const heatHot = Color(0xFFFD7E14);
  static const heatBurn = Color(0xFFDC3545);

  // Gradients
  static const gradientPrimary = LinearGradient(
    colors: [primary, primaryDark],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  static const gradientGold = LinearGradient(
    colors: [tertiary, Color(0xFFFFA000)],
  );
  static const gradientSuccess = LinearGradient(
    colors: [success, Color(0xFF1E7E34)],
  );
}
