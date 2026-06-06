# 🇮🇹 Italiano Autentico

**🔗 App online:** https://bruno-felipe-conte.github.io/apprendimento-italiano/

PWA para aprendizado de italiano — Flashcards, Quiz, Vocabulário e Gramática estruturada pelo método do Pe. Napoleão Mendes de Almeida (NMA).

> **Funciona 100% offline** após a primeira visita. Todo progresso salvo localmente no navegador. Instale como app: no Chrome/Edge clique em ⊕ na barra de endereço; no Safari iOS use Compartilhar → "Adicionar à Tela de Início".

## Branches

| Branch | Propósito |
|---|---|
| `master` | Desenvolvimento — todos os commits vão aqui |
| `gh-pages` | Produção — GitHub Pages serve deste branch |

**Para publicar uma versão:**
```bash
git push origin master:gh-pages
```
Execute este comando apenas quando a versão estiver pronta para os usuários.

---

## ✨ Funcionalidades

| Módulo | Descrição |
|---|---|
| **🏛️ Templi** | 51 templos de vocabulário com progresso e heatmap de atividade |
| **🃏 Flashcard** | Sistema de revisão espaçada com blur-reveal e áudio |
| **❓ Quiz** | Questões de múltipla escolha por categoria |
| **📖 Vocabolario** | Vocabulário organizado por templo |
| **📚 Grammatica** | 82 lezioni (A1/A2/B1/B2 + C1/C2 avançados) com método pedagógico NMA de 7 camadas |

### Gramática — Método NMA
Cada lição segue 7 camadas pedagógicas:
1. **Alerta** — frase motivacional de abertura
2. **Inventário** — estrutura numerada do conteúdo
3. **Definição indutiva** — Fenômeno → Causa → Conceito
4. **Técnica** — algoritmo verbal de aplicação
5. **Exemplos P→R→C** — Pergunta / Resposta / Conclusão
6. **Ponte** — equivalência Português → Italiano
7. **Coda** — responsabilização do aluno

---

## 🚀 Rodar localmente

```bash
npx serve -l 5500 .
```

Acesse: `http://localhost:5500`

### Celular (mesma rede Wi-Fi)

1. Descubra o IP do seu computador: `ipconfig` → IPv4
2. No celular: `http://192.168.x.x:5500`
3. Ou instale como PWA — o app aparecerá na tela inicial

---

## 📦 Estrutura do projeto

```
italian-learning-app-pro/
├── index.html                  # App completo (HTML + CSS inline + imports JS)
├── manifest.webmanifest        # Configuração PWA
├── sw.js                       # Service Worker (cache offline)
├── js/
│   ├── core.js                 # App singleton — navegação, XP, progresso, TTS
│   ├── flashcards.js           # Módulo de flashcards
│   ├── quiz.js                 # Módulo de quiz
│   ├── vocab.js                # Módulo de vocabulário
│   ├── grammar.js              # Módulo de gramática (renderer NMA)
│   └── heatmap.js              # Heatmap de atividade diária
├── data/
│   ├── grammar.json            # 82 lezioni com campos NMA (PT e IT)
│   ├── quizzes.json            # Questões de quiz
│   └── templo-[1-51].json      # Vocabulário por templo
└── icons/
    └── icon.svg
```

---

## 💾 Dados persistidos

Tudo no `localStorage` do navegador — sem backend, sem conta:

| Chave | Conteúdo |
|---|---|
| `it_progresso` | XP, nível, streak, lições completadas |
| `it_diario` | Atividade diária `{"2026-05-27": 14, ...}` |

---

## 📱 Instalar como app (PWA)

**Android/Chrome:** Menu ⋮ → *Adicionar à tela inicial*  
**iOS/Safari:** Compartilhar → *Adicionar à Tela de Início*  
**Desktop/Chrome:** Ícone ⊕ na barra de endereços

O app funciona offline após a primeira visita.
