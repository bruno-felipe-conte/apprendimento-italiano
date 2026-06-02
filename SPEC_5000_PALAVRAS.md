# SPEC — Expansão para 5.000 Palavras Italianas
## App: Italiano Autentico | Repo: bruno-felipe-conte/apprendimento-italiano

---

## CONTEXTO

App PWA de aprendizado de italiano. Já tem **718 palavras** em `data/templo-1.json` até `data/templo-10.json`.
Foram gerados **templo-11.json, templo-12.json, templo-13.json** (321 palavras) com o script `data/gerar_5000.py`.
**Faltam gerar: templo-14.json até templo-50.json** (37 arquivos × ~107 palavras = ~3.959 palavras).

**Meta total:** ~5.000 palavras em 50 templos.

---

## SCHEMA EXATO DE CADA PALAVRA

```json
{
  "id": "t14_001",
  "italiano": "parola",
  "portugues": "palavra",
  "genero": "f",
  "plural": "parole",
  "exemplo": "Questa parola è difficile.",
  "exemplo_pt": "Esta palavra é difícil.",
  "categoria": "nome_categoria",
  "dificuldade": "medio",
  "audio_ipa": "/paˈrɔːla/"
}
```

**Regras:**
- `id`: formato `tNN_XXX` (ex: `t14_001`, `t14_107`)
- `genero`: `"m"`, `"f"`, `"m/f"` ou `null` (verbos/advérbios)
- `plural`: string com plural ou `null`
- `dificuldade`: sempre `"medio"` para os novos templos
- `audio_ipa`: com barras `/` obrigatórias. Se não souber, use `""`
- Para verbos: `genero: null`, `plural: null`
- `exemplo` e `exemplo_pt`: frases naturais de uso cotidiano

---

## SCHEMA DO ARQUIVO TEMPLO

```json
{
  "templo": 14,
  "nome": "Nome do Templo",
  "cidade": "Cidade Italiana",
  "nivel": "B1",
  "palavras": [ ...array de 107 palavras... ]
}
```

---

## PALAVRAS JÁ EXISTENTES — NÃO REPETIR

**Templos 1-10 (718 palavras) cobrem:**
- Saudações: ciao, buongiorno, buonasera, buonanotte, arrivederci, grazie, prego, scusi, per favore, bene, male, così così
- Números: zero a cento, mille, milione
- Pronomes: io, tu, lui, lei, noi, voi, loro, me, te, si, ci, vi
- Verbos base: essere, avere, fare, andare, venire, potere, volere, dovere, sapere, stare, dire, vedere, sentire, parlare, capire, leggere, scrivere, mangiare, bere, dormire, lavorare, studiare, abitare, comprare, vendere, pagare, aspettare, arrivare, partire, tornare, uscire, entrare, aprire, chiudere
- Família: padre, madre, fratello, sorella, figlio, figlia, marito, moglie, nonno, nonna, zio, zia, cugino, nipote
- Cores: rosso, blu, verde, giallo, bianco, nero, arancione, viola, rosa, grigio, marrone
- Corpo: testa, occhio, naso, bocca, orecchio, dente, capelli, braccio, mano, dito, gamba, piede, cuore, stomaco, schiena
- Giorni: lunedì, martedì, mercoledì, giovedì, venerdì, sabato, domenica
- Mesi: gennaio a dicembre
- Stagioni: primavera, estate, autunno, inverno
- Aggettivi comuni: bello, brutto, grande, piccolo, buono, cattivo, nuovo, vecchio, giovane, alto, basso, lungo, corto, largo, stretto, pesante, leggero, caldo, freddo, facile, difficile, veloce, lento, forte, debole, ricco, povero, felice, triste, stanco, malato, sano
- Cibo base: pane, pasta, pizza, riso, carne, pesce, formaggio, uovo, latte, burro, olio, sale, zucchero, caffè, acqua, vino, birra, frutta, verdura
- Casa base: casa, stanza, cucina, bagno, camera, porta, finestra, tavolo, sedia, letto, divano
- Trasporti: macchina, autobus, treno, aereo, bici, moto, taxi, nave, metropolitana
- Numeri ordinali: primo, secondo, terzo, quarto, quinto
- Preposizioni: di, a, da, in, con, su, per, tra, fra
- Avverbi comuns: molto, poco, mai, sempre, spesso, ancora, già, subito, presto, tardi, qui, lì, dentro, fuori, sopra, sotto, davanti, dietro, insieme, anche, solo, così, però, quindi, allora, forse, magari, purtroppo
- Emozioni: felice, triste, arrabbiato, sorpreso, paura, amore, odio, gelosia, ansia, gioia
- Personalità: simpatico, antipatico, gentile, scortese, timido, estroverso, onesto, bugiardo, pigro, diligente

**Templos 11-13 (321 palavras) cobrem:**
- T11: cucina (ingredienti, tecniche, utensili, ricette, piatti tipici, bevande, frutta/verdura avanzata)
- T12: lavoro (professioni, ufficio, contratto, stipendio, colloquio, azienda)
- T13: casa (appartamento, arredamento, elettrodomestici, manutenzione, affitto)

---

## OS 37 TEMPLOS A GERAR (14-50)

| Templo | Nome | Cidade | Nível | Tema Principal |
|--------|------|--------|-------|----------------|
| 14 | La Natura e l'Ambiente | Firenze | B1 | animali, piante, paesaggio, ecologia, clima |
| 15 | Lo Sport e il Tempo Libero | Torino | A2 | sport, esercizio, hobby, giochi, svago |
| 16 | La Salute e la Medicina | Roma | B1 | malattia, sintomi, medico, farmacia, corpo avanzato |
| 17 | La Città e i Servizi | Napoli | A2 | servizi pubblici, banca, posta, supermercato, negozi |
| 18 | L'Arte e la Cultura | Firenze | B1 | arte, musica, cinema, teatro, letteratura, musei |
| 19 | La Tecnologia | Milano | B1 | computer, internet, smartphone, social media, app |
| 20 | La Politica e la Società | Roma | B2 | governo, elezioni, leggi, diritti, cittadinanza |
| 21 | L'Economia e la Finanza | Milano | B2 | banca, investimenti, mercato, tasse, commercio |
| 22 | L'Istruzione e la Scienza | Bologna | B1 | scuola, università, materie, ricerca, scoperte |
| 23 | La Moda e lo Shopping | Milano | A2 | abbigliamento dettagliato, accessori, taglia, stile |
| 24 | Gli Animali | Venezia | A2 | animali domestici, selvatici, uccelli, insetti, pesci |
| 25 | Il Tempo e il Meteo | Venezia | A2 | clima avanzato, previsioni, fenomeni, temperature |
| 26 | I Trasporti Avanzati | Roma | A2 | aeroporto, stazione, autostrada, navigazione |
| 27 | Le Azioni Quotidiane | Napoli | A2 | verbi quotidiani (svegliarsi, lavarsi, vestirsi, uscire) |
| 28 | Le Relazioni Sociali | Palermo | A2 | amicizia, amore, matrimonio, famiglia estesa |
| 29 | Il Corpo e la Salute | Roma | B1 | anatomia, sintomi avanzati, cura personale |
| 30 | I Media e la Comunicazione | Milano | B1 | giornale, radio, TV, podcast, pubblicità |
| 31 | Il Diritto e la Giustizia | Roma | B2 | legge, crimine, tribunale, polizia, avvocato |
| 32 | La Psicologia e le Emozioni | Bologna | B2 | emozioni complesse, carattere, mente, comportamento |
| 33 | La Storia d'Italia | Roma | B2 | storia italiana, guerra, impero, Risorgimento, tradizioni |
| 34 | La Religione e la Tradizione | Assisi | B1 | religione, feste, tradizioni regionali, riti |
| 35 | Verbi di Azione Avanzati | Roma | B1 | 107 verbi frequenti non ancora coperti |
| 36 | Avverbi ed Espressioni | Milano | B1 | avverbi di modo/tempo/luogo, locuzioni |
| 37 | Congiunzioni e Connettori | Bologna | B1 | connettivi, congiunzioni, marcatori discorsivi |
| 38 | Sinonimi e Sfumature | Roma | B2 | sinonimi di parole comuni, differenze di significato |
| 39 | Espressioni Idiomatiche | Napoli | B2 | modi di dire, proverbi, espressioni fisse |
| 40 | Il Gergo Moderno | Milano | B2 | linguaggio colloquiale, slang, informale moderno |
| 41 | Il Linguaggio Formale | Roma | B2 | corrispondenza formale, discorso ufficiale |
| 42 | Parole Internazionali | Milano | B1 | anglicismi in uso, false friends, latinismi |
| 43 | La Gastronomia Regionale | Sicilia | B1 | cucina regionale, ingredienti tipici, denominazioni |
| 44 | L'Architettura e l'Arte | Roma | B2 | architettura, arte classica, terminologia artistica |
| 45 | Il Commercio e gli Affari | Milano | B2 | business, marketing, export, imprenditoria |
| 46 | L'Ambiente e l'Ecologia | Toscana | B1 | ambiente, sostenibilità, energia, inquinamento |
| 47 | La Letteratura e la Scrittura | Firenze | B2 | letteratura, scrittura, narrativa, poesia |
| 48 | Matematica e Scienze | Pisa | B1 | matematica, fisica, chimica, biologia |
| 49 | False Friends e Trabocchetti | Roma | B2 | falsi amici italiano-portoghese, errori comuni |
| 50 | Revisione Avanzata | Venezia | B2 | vocabolario avanzato C1, parole di alta frequenza |

---

## COMO GERAR — INSTRUÇÕES PARA A LLM

### 1. Usar o script base já existente

O script `data/gerar_5000.py` já tem o padrão. Continue adicionando templos no mesmo arquivo usando a função `w()` e `salvar()`.

```python
def w(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {"id": tid, "italiano": it, "portugues": pt, "genero": gen, "plural": pl,
            "exemplo": ex_it, "exemplo_pt": ex_pt, "categoria": cat,
            "dificuldade": "medio", "audio_ipa": ipa}

def salvar(templo_num, nome, cidade, nivel, palavras):
    # já implementado no script
```

### 2. Gerar em blocos de 5 templos por vez

Para evitar limite de tokens, gere 5 templos por execução:
- Rodada 1: templos 14-18
- Rodada 2: templos 19-23
- Rodada 3: templos 24-28
- Rodada 4: templos 29-33
- Rodada 5: templos 34-38
- Rodada 6: templos 39-43
- Rodada 7: templos 44-48
- Rodada 8: templos 49-50

### 3. Critérios de qualidade por templo

- **107 palavras mínimo** por templo
- **Variedade de classes gramaticais**: substantivos, verbos, adjetivos, advérbios
- **Palavras reais e frequentes** do italiano contemporâneo
- **Exemplos naturais** — frases que um italiano usaria no dia a dia
- **IPA correto** — use a notação fonética padrão italiano
- **NÃO repetir** nenhuma palavra já listada na seção "PALAVRAS JÁ EXISTENTES"
- **Categorias**: usar nomes em italiano, snake_case (ex: `natura`, `sport`, `salute`, `arte`, `tecnologia`)

### 4. Atualizar core.js após gerar todos os templos

**Arquivo:** `js/core.js` linha ~127

**ANTES:**
```javascript
for (let i = 1; i <= 10; i++) {
```

**DEPOIS:**
```javascript
for (let i = 1; i <= 50; i++) {
```

### 5. Atualizar sw.js

**Arquivo:** `sw.js`

Incrementar versão de `italiano-v10` para `italiano-v11`.

Adicionar no array STATIC os novos arquivos:
```javascript
'./data/templo-11.json',
'./data/templo-12.json',
// ... até
'./data/templo-50.json',
```

### 6. Commit e push final

```bash
git add -A
git commit -m "feat: expand to 5000 words — add templos 14-50 with thematic vocabulary"
git push origin master
git push origin master:gh-pages --force
```

---

## EXEMPLOS DE PALAVRAS POR TEMPLO (guia de conteúdo)

### T14 — La Natura e l'Ambiente
**Animali:** lupo, volpe, cervo, aquila, serpente, rana, farfalla, ape, mosca, ragno, squalo, balena, delfino, elefante, leone, tigre, orso, scimmia, pappagallo, gufo
**Piante:** quercia, pino, ulivo, vite, rosa, girasole, margherita, orchidea, cactus, bambù, muschio, felce, fungo, radice, ramo, foglia, fiore, seme, corteccia, frutto
**Paesaggio:** collina, pianura, valle, scogliera, spiaggia, deserto, giungla, savana, tundra, ghiacciaio, vulcano, terremoto, alluvione, siccità, tsunami
**Ecologia:** inquinamento, riciclaggio, CO2, biodiversità, deforestazione, riscaldamento globale, energia solare, energia eolica, combustibile fossile, emissioni

### T15 — Lo Sport e il Tempo Libero
**Sport individuali:** nuoto, corsa, ciclismo, tennis, golf, boxe, judo, karate, yoga, ginnastica, arrampicata, sci, pattinaggio, surf, equitazione
**Sport di squadra:** calcio, pallavolo, basket, rugby, pallamano, hockey, baseball, cricket, polo, curling
**Attrezzatura:** pallone, racchetta, maglia, scarpe da ginnastica, casco, guantoni, rete, canestro, porta, pista
**Hobby:** fotografare, dipingere, suonare, cantare, ballare, giardinaggio, cucito, bricolage, videogiochi, lettura, viaggiare, collezione, cucina creativa

### T16 — La Salute e la Medicina
**Malattie:** influenza, raffreddore, febbre, tosse, mal di testa, mal di stomaco, allergia, diabete, ipertensione, asma, artrite, depressione, ansia, insonnia, cancro
**Sintomi:** dolore, nausea, vomito, diarrea, stitichezza, vertigini, svenimento, gonfiore, prurito, bruciore, stanchezza, mancanza di respiro
**Cure:** pillola, compressa, sciroppo, iniezione, vaccino, operazione, fisioterapia, radioterapia, chemioterapia, dialisi, trasfusione
**Strutture:** pronto soccorso, reparto, ambulatorio, laboratorio, radiologia, farmacia, ambulanza, barella, sedia a rotelle

### T17 — La Città e i Servizi
**Servizi pubblici:** municipio, prefettura, questura, tribunale, posta, banca, ospedale, biblioteca, università, scuola, asilo, cimitero
**Negozi:** panetteria, macelleria, pescheria, fruttivendolo, edicola, tabaccheria, cartoleria, gioielleria, ottico, parrucchiere, estetista, lavanderia, profumeria, libreria
**Burocrazia:** documento, carta d'identità, passaporto, patente, codice fiscale, permesso di soggiorno, certificato, tassa, multa, ricevuta, modulo, ufficio anagrafe

### T18 — L'Arte e la Cultura
**Arte visiva:** dipinto, scultura, affresco, mosaico, fotografia, installazione, acquerello, olio su tela, incisione, ceramica, vetro, bronzo, marmo
**Musica:** melodia, ritmo, accordo, spartito, orchestra, sinfonia, opera, jazz, rock, pop, musica classica, strumento, chitarra, pianoforte, violino, flauto, batteria, tromba
**Cinema e teatro:** film, regista, attore, sceneggiatura, scena, costumi, scenografia, biglietto, platea, palco, sipario, applauso, critica

### T19 — La Tecnologia
**Hardware:** computer, laptop, tablet, smartphone, tastiera, schermo, mouse, stampante, scanner, hard disk, RAM, processore, batteria, caricatore
**Internet:** sito web, browser, motore di ricerca, download, upload, password, account, login, email, spam, hacker, firewall, cloud, server
**Social media:** profilo, follower, like, condivisione, hashtag, stories, video, streaming, influencer, podcast, vlog, meme, notifica

### T20 — La Politica e la Società
**Istituzioni:** parlamento, senato, camera dei deputati, governo, ministero, presidente, premier, sindaco, prefetto, giudice, ambasciata, consolato
**Politica:** partito, elezione, voto, campagna, sondaggio, coalizione, opposizione, riforma, legge, decreto, referendum, costituzione, democrazia, dittatura
**Sociale:** immigrazione, integrazione, diseguaglianza, povertà, welfare, assistenza sociale, volontariato, ONG, sciopero, manifestazione, protesta

### T35 — Verbi di Azione (107 verbi frequenti)
accettare, aggiungere, aiutare, alzarsi, ammettere, annunciare, apparire, applicare, approvare, arrestare, assumere, aumentare, avvicinarsi, cambiare, cancellare, cercare, chiamare, citare, collegare, consegnare, costruire, coprire, correre, crescere, decidere, dichiarare, dimenticare, discutere, diventare, eliminare, emergere, entrare, esaminare, evitare, finire, formare, garantire, gestire, girare, guidare, immaginare, indicare, iniziare, insegnare, interessare, introdurre, lasciare, mantenere, migliorare, misurare, mostrare, muoversi, nascere, notare, offrire, organizzare, ottenere, perdere, permettere, prendere, presentare, produrre, proteggere, pubblicare, raggiungere, realizzare, ricevere, ricordare, ridurre, riferire, rispettare, rispondere, risultare, richiedere, salire, scegliere, scoprire, seguire, segnare, servire, smettere, sostenere, spiegare, stabilire, suggerire, trasformare, trattare, uccidere, usare, valutare, vincere, visitare, vivere

---

## VERIFICAÇÃO FINAL

Após gerar todos os templos, execute:

```python
import json, os
total = 0
for i in range(1, 51):
    path = f"data/templo-{i}.json"
    if os.path.exists(path):
        d = json.load(open(path, encoding='utf-8'))
        n = len(d['palavras'])
        total += n
        print(f"T{i}: {n} palavras")
print(f"\nTOTAL: {total} palavras")
```

**Meta:** ≥ 4.500 palavras (718 existentes + ~3.800 novas).

---

## ARQUIVOS A MODIFICAR

| Arquivo | Mudança |
|---------|---------|
| `data/gerar_5000.py` | Adicionar templos 14-50 e executar |
| `js/core.js` linha 127 | `i <= 10` → `i <= 50` |
| `sw.js` | Versão v10 → v11 + adicionar templo-11 a templo-50 no STATIC |

---

## NOTAS IMPORTANTES

1. **NÃO usar palavras dos templos 1-13** — há muita sobreposição se não verificar
2. **Verbos no infinitivo** — genero e plural null
3. **Exemplos curtos** — máximo 10 palavras, frases naturais
4. **IPA simplificado é OK** — melhor ter algo do que nada
5. O app já tem toda a infraestrutura pronta — flashcards, quiz, vocabulário, busca — tudo funciona automaticamente com os novos templos
