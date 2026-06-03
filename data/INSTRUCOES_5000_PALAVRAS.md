# INSTRUÇÕES PARA COMPLETAR AS 5.000 PALAVRAS DO APPRENDIMENTO ITALIANO

## CONTEXTO DO PROJETO

Aplicação web de aprendizado de italiano. O vocabulário é organizado em "templos" temáticos.
Cada templo = um arquivo JSON em `data/templo-{N}.json`.

---

## ESTADO ATUAL

| Templos | Palavras | Status |
|---------|----------|--------|
| T1–T10  | 718      | ✅ prontos (schema A) |
| T11–T13 | 321      | ✅ prontos (schema B) |
| T15–T17 | 296      | ✅ prontos (schema B, não commitados) |
| **T14** | **0**    | ❌ falta criar |
| **T18–T50** | **0** | ❌ falta criar |
| **TOTAL ATUAL** | **1.335** | |
| **META** | **5.000** | |
| **FALTAM** | **3.665** | em ~34 templos |

---

## SCHEMA OBRIGATÓRIO (copiar exatamente)

### Função geradora (Python)
```python
def w(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {
        "id": tid,
        "italiano": it,
        "portugues": pt,
        "genero": gen,        # "m", "f", "m/f", ou None para verbos/adjetivos
        "plural": pl,         # plural italiano, ou None
        "exemplo": ex_it,     # frase de exemplo em italiano
        "exemplo_pt": ex_pt,  # tradução da frase para português
        "categoria": cat,     # categoria temática (string livre)
        "dificuldade": "medio",
        "audio_ipa": ipa      # transcrição IPA entre /barras/
    }
```

### Função de salvar
```python
def salvar(templo_num, nome, cidade, nivel, palavras):
    obj = {"templo": templo_num, "nome": nome, "cidade": cidade, "nivel": nivel, "palavras": palavras}
    path = os.path.join(OUT, f"templo-{templo_num}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"OK templo-{templo_num}.json -- {len(palavras)} palavras")
```

### Cabeçalho do script
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os

OUT = os.path.dirname(os.path.abspath(__file__))
```

### Chamada de salvar
```python
salvar(14, "I Colori e le Qualità", "Firenze", "A2", t14)
```

---

## REGRAS DE QUALIDADE (NÃO NEGOCIÁVEIS)

1. **Palavras REAIS** do italiano cotidiano — nada inventado, nada repetido
2. **IPA correto** para cada palavra (consultar Wiktionary se necessário)
3. **Exemplos naturais** — frases que um falante nativo usaria
4. **IDs únicos** no formato `t{N}_{num:03d}` — ex: `t14_001`, `t14_002` ... `t14_111`
5. **Exatamente 107–115 palavras por templo** — não mais, não menos
6. **Sem duplicatas** entre templos — verificar palavras já usadas nos T1–T17
7. **Nível de dificuldade coerente** com o nível declarado do templo (A2/B1/B2)
8. **Português do Brasil** nas traduções

---

## TEMPLOS A CRIAR (em ordem)

### LOTE 1 — ~1.000 palavras (T14, T18–T25)

| # | Tema | Cidade | Nível | Palavras-chave do tema |
|---|------|--------|-------|------------------------|
| **T14** | I Colori e le Qualità Visive | Firenze | A2 | rosso, blu, chiaro, scuro, lucido, opaco, sfumatura, contrasto, tono, palette... |
| **T18** | La Scuola e l'Università | Napoli | A2 | aula, professore, studente, materia, esame, voto, compito, biblioteca, laurea, tesi... |
| **T19** | I Trasporti e i Viaggi | Venezia | A2 | aereo, treno, autobus, biglietto, stazione, aeroporto, partenza, arrivo, orario, ritardo... |
| **T20** | Il Corpo Umano | Bologna | B1 | testa, occhio, naso, bocca, orecchio, spalla, braccio, mano, dito, piede, cuore, polmone... |
| **T21** | Le Emozioni e i Sentimenti | Siena | B1 | gioia, tristezza, paura, rabbia, sorpresa, amore, odio, gelosia, nostalgia, orgoglio... |
| **T22** | La Natura e le Stagioni | Torino | A2 | primavera, estate, autunno, inverno, albero, fiore, foglia, pioggia, neve, vento, fiume... |
| **T23** | Gli Animali | Palermo | A2 | cane, gatto, cavallo, mucca, pecora, pollo, pesce, uccello, leone, tigre, orso, lupo... |
| **T24** | La Tecnologia Moderna | Milano | B1 | computer, smartphone, internet, applicazione, schermo, tastiera, software, password, rete... |
| **T25** | Il Commercio e i Soldi | Genova | A2 | negozio, prezzo, offerta, sconto, cassa, scontrino, banconota, moneta, carta di credito... |

### LOTE 2 — ~1.000 palavras (T26–T33)

| # | Tema | Cidade | Nível | Palavras-chave do tema |
|---|------|--------|-------|------------------------|
| **T26** | La Politica e la Società | Roma | B1 | governo, parlamento, elezione, voto, partito, legge, democrazia, cittadino, diritto... |
| **T27** | La Cultura e le Arti | Firenze | B1 | museo, opera, pittura, scultura, mostra, galleria, artista, capolavoro, affresco... |
| **T28** | La Musica | Verona | A2 | canzone, ritmo, melodia, chitarra, pianoforte, violino, voce, cantante, concerto, nota... |
| **T29** | Il Cinema e il Teatro | Roma | B1 | film, regista, attore, scena, copione, recitare, palcoscenico, platea, applauso, prova... |
| **T30** | La Letteratura e i Libri | Venezia | B1 | romanzo, racconto, poesia, autore, personaggio, trama, capitolo, prefazione, editore... |
| **T31** | La Scienza e la Ricerca | Bologna | B1 | ricerca, esperimento, laboratorio, ipotesi, risultato, scoperta, teoria, dati, metodo... |
| **T32** | La Storia d'Italia | Roma | B1 | impero, guerra, pace, rivoluzione, re, repubblica, unità, medioevo, rinascimento... |
| **T33** | Il Turismo e i Musei | Venezia | A2 | turista, guida, mappa, itinerario, monumento, palazzo, chiesa, piazza, visita, souvenir... |

### LOTE 3 — ~1.000 palavras (T34–T41)

| # | Tema | Cidade | Nível | Palavras-chave do tema |
|---|------|--------|-------|------------------------|
| **T34** | L'Ambiente e l'Ecologia | Torino | B1 | inquinamento, riciclaggio, energia, sostenibile, clima, riscaldamento, foresta, specie... |
| **T35** | La Medicina avanzata | Milano | B1 | diagnosi, sintomo, terapia, farmaco, chirurgia, ospedale, medico, paziente, ricetta... |
| **T36** | Il Diritto e la Legge | Roma | B2 | avvocato, tribunale, giudice, sentenza, reato, processo, prova, difesa, accusa, codice... |
| **T37** | L'Informatica e il Web | Milano | B1 | programma, codice, algoritmo, database, server, cloud, sicurezza, virus, aggiornamento... |
| **T38** | La Matematica e le Scienze | Bologna | B1 | numero, equazione, geometria, angolo, diametro, area, volume, formula, calcolo, misura... |
| **T39** | L'Architettura e l'Urbanistica | Roma | B1 | edificio, facciata, colonna, arco, cupola, fondamenta, mattone, cemento, progetto... |
| **T40** | La Moda e l'Abbigliamento | Milano | A2 | vestito, abito, giacca, camicia, pantaloni, gonna, scarpe, borsa, cintura, accessorio... |
| **T41** | La Gastronomia Avanzata | Bologna | B1 | antipasto, primo, secondo, dessert, sommelier, degustazione, stagionato, affumicato... |

### LOTE 4 — ~665 palavras (T42–T50)

| # | Tema | Cidade | Nível | Palavras-chave do tema |
|---|------|--------|-------|------------------------|
| **T42** | I Mestieri e l'Artigianato | Firenze | B1 | falegname, muratore, sarto, orafo, ceramista, fabbro, vetraio, scultura, intaglio... |
| **T43** | Le Feste e le Tradizioni | Napoli | A2 | Natale, Pasqua, Capodanno, carnevale, festa, fuochi, tradizione, regalo, auguri... |
| **T44** | Lo Sport Avanzato | Milano | B2 | campionato, arbitro, fallo, tattica, allenamento, infortunio, podio, record, semifinale... |
| **T45** | Il Mare e la Navigazione | Genova | B1 | barca, nave, porto, vela, ancora, marinaio, marea, onda, corrente, bussola, rotta... |
| **T46** | La Montagna e l'Alpinismo | Trento | B1 | vetta, sentiero, rifugio, ghiacciaio, valanga, rampone, piccozza, altitudine, roccia... |
| **T47** | L'Agricoltura e la Campagna | Bari | B1 | campo, raccolto, semina, trattore, concime, irrigazione, vigneto, oliveto, mietere... |
| **T48** | Avverbi e Connettivi | Roma | B1 | tuttavia, inoltre, perciò, dunque, nonostante, sebbene, affinché, benché, malgrado... |
| **T49** | I Materiali e le Sostanze | Milano | B2 | acciaio, alluminio, plastica, vetro, ceramica, gomma, tessuto, legno, pietra, ferro... |
| **T50** | Parole Colte e Formali | Roma | B2 | eloquenza, perspicacia, acume, discernimento, plausibile, verosimile, lacunoso, esimio... |

---

## PALAVRAS JÁ USADAS (NÃO REPETIR)

### T1–T10 (schema vocabulario): temas A1 — saudações, família, cores básicas, números, dias, meses, verbos ser/estar/ter/fazer, casa básica, comida básica

### T11 — La Cucina: cucinare, ricetta, ingrediente, olio, sale, pepe, aglio, cipolla, pomodoro, formaggio, burro, farina, uovo, latte, zucchero, aceto, brodo, risotto, minestra, zuppa, bistecca, pollo, maiale, agnello, salmone, tonno, gamberetto, verdura, frutta, melanzana, zucchina, peperone, spinaci, insalata, padella, pentola, forno, frigorifero, microonde, colino, tagliere, coltello, forchetta, cucchiaio, piatto, bicchiere, tovagliolo, tovaglia, pentolino, mestolo, grattugia, teglia, brocca, caraffa, maccheroni, spaghetti, penne, tagliatelle, lasagne, gnocchi, ravioli, pizza, bruschetta, focaccia, grissini, mortadella, prosciutto, salame, bresaola, carpaccio, affettato, antipasto, primo, secondo, contorno, dessert, tiramisù, panna cotta, cannolo, gelato, sorbetto, espresso, cappuccino, affogato, friggere, bollire, arrostire, grigliare, cuocere, saltare, mescolare, tritare, sbucciare, tagliare, grattugiare, impastare, lievitare, condire, marinare, servire

### T12 — Il Lavoro: lavorare, dipendente, impiegato, operaio, dirigente, manager, capo, collega, collaboratore, assunzione, licenziamento, contratto, stipendio, salario, busta paga, produzione, fabbrica, industria, azienda, impresa, società, filiale, sede, ufficio, riunione, progetto, relazione, report, obiettivo, scadenza, orario, turno, straordinario, ferie, permesso, congedo, sindacato, sciopero, sindaco (union), mansione, qualifica, carriera, promozione, formazione, stage, tirocinio, curriculum, colloquio, candidato, selezione, medico, avvocato, ingegnere, architetto, insegnante, professore, infermiere, farmacista, commerciante, artigiano, agricoltore, pescatore, cuoco, cameriere, autista, pilota, giornalista, scrittore, artista, musicista, attore, regista, fotografo, traduttore, informatico, programmatore, contabile, economista, psicologo, sociologo, fisico, chimico, biologo, matematico, statistico, geografo

### T13 — La Casa: appartamento, casa, villetta, condominio, affitto, mutuo, proprietario, inquilino, portiere, ascensore, scala, piano, garage, cantina, soffitta, soggiorno, salotto, cucina, camera, bagno, studio, corridoio, ingresso, terrazza, balcone, giardino, cortile, finestra, porta, portone, muro, pavimento, soffitto, tetto, sofà, divano, poltrona, sedia, tavolo, scrivania, letto, armadio, cassettiera, comodino, scaffale, libreria, specchio, quadro, lampada, tenda, tappeto, lavatrice, lavastoviglie, frigorifero, congelatore, forno, asciugatrice, aspirapolvere, ferro, stirare, pulire, lavare, spazzare, spolverare, riordinare, sistemare, aggiustare, riparare, dipingere, imbiancare, costruire, demolire, ristrutturare, arredare, affittare, comprare, vendere, scegliere, cambiare

### T15 — Lo Sport: calcio, pallone, rete, porta, campo, stadio, squadra, allenatore, capitano, giocatore, vittoria, sconfitta, punteggio, obiettivo, allenamento, corrida, nuoto, ciclismo, tennis, golf, boxe, judo...

### T16 — La Salute: febbre, tosse, mal di testa, nausea, dolore, farmaco, medicina, ospedale, pronto soccorso, ambulanza, chirurgo, infermiere, ricetta, diagnosi, sintomo...

### T17 — La Città e i Servizi: municipio, prefettura, questura, tribunale, poste, banca, supermercato, mercato, farmacia, ospedale, scuola, chiesa, parco, piazza, strada, semaforo, autobus, metro, taxi...

---

## ESTRUTURA DO ARQUIVO DE SAÍDA

Cada templo gera `data/templo-{N}.json` com esta estrutura:

```json
{
  "templo": 14,
  "nome": "I Colori e le Qualità Visive",
  "cidade": "Firenze",
  "nivel": "A2",
  "palavras": [
    {
      "id": "t14_001",
      "italiano": "rosso",
      "portugues": "vermelho",
      "genero": "m",
      "plural": "rossi",
      "exemplo": "Il vestito rosso è bellissimo.",
      "exemplo_pt": "O vestido vermelho é lindíssimo.",
      "categoria": "colori",
      "dificuldade": "medio",
      "audio_ipa": "/ˈrosso/"
    }
  ]
}
```

---

## COMO EXECUTAR

```bash
cd C:/Users/bruno/Documents/italian-learning-app-pro/data
python gerar_lote1.py   # gera T14, T18-T25
python gerar_lote2.py   # gera T26-T33
python gerar_lote3.py   # gera T34-T41
python gerar_lote4.py   # gera T42-T50
```

Após cada lote, verificar:
```bash
python -c "
import json, glob
total = 0
for f in sorted(glob.glob('templo-*.json')):
    d = json.load(open(f, encoding='utf-8'))
    p = d.get('palavras', d.get('vocabulario', []))
    total += len(p)
    print(f'{f}: {len(p)}')
print(f'TOTAL: {total}')
"
```

---

## CHECKLIST DE QUALIDADE POR TEMPLO

- [ ] Exatamente 107–115 palavras
- [ ] Todos os IDs únicos no formato `t{N}_{num:03d}`
- [ ] Nenhuma palavra repetida dos templos T1–T17
- [ ] Exemplos em italiano correto (frases naturais, não traduções literais)
- [ ] IPA entre barras `/ˈexemplo/`
- [ ] `genero`: "m" ou "f" para substantivos; `null` para verbos e adjetivos
- [ ] `plural`: plural correto para substantivos; `null` para invariáveis e verbos
- [ ] JSON válido (testar com `python -c "import json; json.load(open('templo-N.json', encoding='utf-8'))"`)
- [ ] Palavras do nível declarado (A2 = vocabulário comum, B1 = intermediário, B2 = avançado)
