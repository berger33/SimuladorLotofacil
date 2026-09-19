import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../constants/colors.dart';

class AppTheme {
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      primaryColor: AppColors.primary,
      scaffoldBackgroundColor: AppColors.backgroundDark,
      colorScheme: const ColorScheme.dark(
        primary: AppColors.primary,
        secondary: AppColors.secondary,
        tertiary: AppColors.tertiary,
        surface: AppColors.surfaceDark,
        background: AppColors.backgroundDark,
        error: AppColors.error,
      ),
      textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme).copyWith(
        displayLarge: GoogleFonts.outfit(fontSize: 32, fontWeight: FontWeight.bold),
        headlineMedium: GoogleFonts.sora(fontSize: 24, fontWeight: FontWeight.w600),
      ),
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        color: AppColors.surfaceDark,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.surfaceDark,
        elevation: 0,
        centerTitle: false,
      ),
      bottomNavigationBarTheme: const BottomNavigationBarThemeData(
        backgroundColor: AppColors.surfaceDark,
        selectedItemColor: AppColors.primaryLight,
        unselectedItemColor: Colors.grey,
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
        ),
      ),
      chipTheme: ChipThemeData(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      ),
    );
  }

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      primaryColor: AppColors.primary,
      scaffoldBackgroundColor: AppColors.backgroundLight,
      colorScheme: const ColorScheme.light(
        primary: AppColors.primary,
        secondary: AppColors.secondary,
        tertiary: AppColors.tertiary,
      ),
      textTheme: GoogleFonts.interTextTheme(ThemeData.light().textTheme).copyWith(
        displayLarge: GoogleFonts.outfit(fontSize: 32, fontWeight: FontWeight.bold),
        headlineMedium: GoogleFonts.sora(fontSize: 24, fontWeight: FontWeight.w600),
      ),
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        color: AppColors.surfaceLight,
      ),
    );
  }
}
