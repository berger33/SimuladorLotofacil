# ✅ CHECKLIST PROFISSIONALIZAÇÃO - De Amador para Campeão

## Código

- [ ] Tipagem completa (mypy) em core_shared
- [ ] Docstrings Google style
- [ ] Pydantic Settings para config, não constantes soltas
- [ ] Repository pattern, injeção dependência
- [ ] Testes unitários >80% coverage
- [ ] CI/CD GitHub Actions: lint, test, build
- [ ] Versionamento semver + changelog
- [ ] .env para secrets, não hardcoded
- [ ] Logger abstraído: Crashlytics no mobile, file no desktop
- [ ] Sem prints, só logger

## Arquitetura

- [ ] Separação UI e lógica 100%
- [ ] core_shared sem dependência UI
- [ ] API FastAPI desacoplada
- [ ] Offline-first com cache TTL
- [ ] Feature flags via Remote Config
- [ ] Sem multiprocessing obrigatório, com fallback thread

## UI/UX Mobile

- [ ] Material 3, dark/light
- [ ] Onboarding 3 telas + disclaimer legal
- [ ] Bottom navigation 5 itens
- [ ] Empty states, loading shimmer, error retry
- [ ] Pull to refresh, haptic, animações 60fps
- [ ] Acessibilidade: TalkBack, contraste AA, 48dp touch
- [ ] Ícone adaptativo, splash screen
- [ ] Heatmap e gráfico com fl_chart, não matplotlib

## Play Store Compliance

- [ ] Target SDK 34, compile 34, min 24
- [ ] App Bundle AAB, 64-bit, assinado
- [ ] Privacy Policy URL
- [ ] Data Safety form
- [ ] Content rating IARC 12+
- [ ] Disclaimer jogo responsável em 3 lugares
- [ ] Categoria Tools, não Gambling
- [ ] Sem permissão desnecessária
- [ ] Sem promessa de ganho financeiro
- [ ] Descrição curta 80 chars, longa 4000 com ASO
- [ ] Ícone 512, feature 1024x500, 5+ screenshots, vídeo
- [ ] Teste interno 20 testers 14 dias (obrigatório novos devs)

## Monetização

- [ ] AdMob: banner, interstitial, rewarded com IDs produção
- [ ] IAP: monthly, yearly com trial, lifetime
- [ ] Paywall com alta conversão, timing contextual
- [ ] Validação receipt servidor anti-crack
- [ ] Restore purchases
- [ ] Analytics funil: onboarding, geração, paywall, compra

## Qualidade

- [ ] Firebase Crashlytics desde dia 1
- [ ] Firebase Analytics
- [ ] Testes em 5 devices físicos low-end a high-end
- [ ] Performance: cold start <2s, geração 10 jogos <5s em mid-end
- [ ] Bateria: não drena em background
- [ ] Tamanho APK <50MB Flutter, <150MB Kivy

## Crescimento

- [ ] Compartilhar WhatsApp com marca d'água free
- [ ] Avaliar app prompt após 3 gerações positivas
- [ ] Blog SEO + comunidade Telegram
- [ ] ASO experiments: ícone, screenshots, descrição
- [ ] UAC Google Ads

## Legal

- [ ] Terms of Service
- [ ] Privacy Policy
- [ ] Disclaimer +18 e jogo responsável
- [ ] Não afiliado Caixa em todo lugar
- [ ] Contato suporte

## Pós-lançamento

- [ ] Responder reviews <24h nos primeiros 30 dias
- [ ] Roadmap público
- [ ] Changelog
- [ ] Code push via Shorebird para hotfixes
