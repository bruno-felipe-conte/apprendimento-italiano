<div align="center">
  <img src="https://raw.githubusercontent.com/bruno-felipe-conte/apprendimento-italiano/master/icons/icon.svg" width="120" alt="Logo">
  <h1>🇮🇹 Italiano Autentico</h1>
  <p><strong>Uma experiência Premium de Aprendizado de Italiano em PWA</strong></p>

  <p>
    <a href="https://bruno-felipe-conte.github.io/apprendimento-italiano/"><img src="https://img.shields.io/badge/Acessar%20App-Online-success?style=for-the-badge&logo=googlechrome"></a>
    <img src="https://img.shields.io/badge/PWA-100%25%20Offline-blue?style=for-the-badge&logo=pwa">
    <img src="https://img.shields.io/badge/N%C3%ADveis-A1%20a%20C2-orange?style=for-the-badge">
  </p>
</div>

---

## 🌟 O Projeto

**Italiano Autentico** é uma aplicação web progressiva (PWA) de alto nível para o ensino do idioma italiano. Desenvolvido para oferecer imersão completa, o aplicativo funciona inteiramente no navegador e **100% offline** após o primeiro acesso, salvando o progresso do usuário de forma segura e local. 

Com um design requintado (Premium/Luxo), fontes amigáveis à dislexia (*Atkinson Hyperlegible*), Modo Escuro nativo, e TTS (Text-to-Speech) integrado, ele eleva a experiência do usuário a um patamar excepcional.

---

## ✨ Módulos Principais

| Módulo | Descrição |
| :--- | :--- |
| **🏛️ Templi (Módulos)** | 51 Templos de aprendizagem gamificados com XP e Heatmap de atividade diária. |
| **📚 Grammatica** | 82 Lições completas (A1 a C2) estruturadas rigorosamente no método do Pe. Napoleão Mendes de Almeida (NMA). |
| **📜 Storie** | Contos interativos com tradução parágrafo-a-parágrafo, tooltip flutuante de vocabulário e áudio TTS. |
| **🎵 Canzoni** | Aprenda com músicas italianas reais! Exercícios de preencher as lacunas com correção automática. |
| **💬 Dialoghi** | Diálogos práticos do dia a dia para desenvolver compreensão conversacional. |
| **🗣️ Imitazione** | Exercícios de *Shadowing* para aperfeiçoar a pronúncia e entonação. |
| **🃏 Flashcards** | Sistema poderoso de repetição espaçada (SM-2) com interface Blur-Reveal e áudio. |
| **❓ Quizzes** | Questões de múltipla escolha focadas na morfologia e retenção. |

---

## 🏛 Metodologia Gramatical NMA

Nossa seção de gramática utiliza as 7 camadas pedagógicas clássicas:
1. **Alerta** — Frase motivacional de abertura
2. **Inventário** — Estrutura numerada do conteúdo
3. **Definição indutiva** — Fenômeno → Causa → Conceito
4. **Técnica** — Algoritmo verbal de aplicação prática
5. **Exemplos (P→R→C)** — Pergunta / Resposta / Conclusão
6. **Ponte** — Equivalência Português → Italiano
7. **Coda** — Responsabilização do aluno

---

## 📱 Instalação como App (PWA)

Esqueça as lojas de aplicativos! Instale direto do seu navegador:

- 🟢 **Android / Chrome:** Clique em `Menu ⋮` → **Adicionar à tela inicial**
- 🍎 **iOS / Safari:** Clique em `Compartilhar` → **Adicionar à Tela de Início**
- 💻 **Desktop:** Clique no ícone `⊕` (instalar) na barra de endereços do Chrome/Edge.

---

## 🚀 Como Rodar Localmente

Clone o repositório e rode um servidor estático simples.

```bash
git clone https://github.com/bruno-felipe-conte/apprendimento-italiano.git
cd apprendimento-italiano

# Usando npx
npx serve -l 5500 .

# Ou usando Python
python -m http.server 5500
```
Em seguida, abra `http://localhost:5500` no seu navegador!

---

## 📦 Estrutura da Aplicação

```text
italian-learning-app-pro/
├── index.html           # Core App (Single Page Application)
├── css/                 # Estilização Premium (italia.css)
├── js/                  # Lógica Modular (core, gramática, histórias, flashcards, etc.)
├── data/                # Base de dados em JSON (Storie, Canzoni, Grammatica, Templi)
├── sw.js                # Service Worker para PWA (Cache Offline)
└── manifest.webmanifest # Configurações de App PWA
```

> **Privacidade:** Todos os dados (XP, Ofensivas, Lições Completadas) são armazenados localmente no seu dispositivo via `localStorage`. Nenhuma nuvem, nenhuma conta necessária. Seus dados são seus!

---

## 🌿 Branches e Deploy

O fluxo de trabalho Git é simples:
- `master`: Desenvolvimento principal.
- `gh-pages`: Deploy de Produção (GitHub Pages).

Para publicar uma nova versão:
```bash
git push origin master:gh-pages
```

<div align="center">
  <br>
  <p><i>Fatto con ❤️ per gli amanti della lingua italiana.</i></p>
</div>
