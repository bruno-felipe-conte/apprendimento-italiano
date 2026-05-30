/**
 * _expandir_gramatica.js
 * Expands grammar.json: A2 5→15, B1 5→12, B2 5→10 units
 * Run: node data/_expandir_gramatica.js
 */

'use strict';
const fs = require('fs');
const path = require('path');

const gramPath = path.join(__dirname, 'grammar.json');
const g = JSON.parse(fs.readFileSync(gramPath, 'utf8'));

// ─── Helpers ─────────────────────────────────────────────────────────────────

function e(tipo, pergunta, opcoes, resposta, explicacao) {
  if (tipo === 'escolha') {
    return { tipo, pergunta, opcoes, resposta, explicacao };
  }
  // revelar
  return { tipo: 'revelar', pergunta, resposta, explicacao };
}

function esc(pergunta, opcoes, resposta, explicacao) {
  return e('escolha', pergunta, opcoes, resposta, explicacao);
}
function rev(pergunta, resposta, explicacao) {
  return e('revelar', pergunta, resposta, explicacao);
}
function dig(pergunta, resposta, dica, explicacao, variantes) {
  const obj = { tipo: 'digitar', pergunta, resposta, explicacao };
  if (dica) obj.dica = dica;
  if (variantes && variantes.length) obj.variantes = variantes;
  return obj;
}

// ─── A2 NEW UNITS (6–15) ──────────────────────────────────────────────────────

const a2Novas = [

  // A2-VI: Passato Prossimo com avere
  {
    id: 'a2-vi', titulo: 'Passato Prossimo con avere',
    subtitulo: 'Ações completadas no passado', nivel: 'A2',
    teoria: `**Passato Prossimo** = *ausiliare* (avere/essere) + *participio passato*

Com **avere**: ho, hai, ha, abbiamo, avete, hanno + participio

**Participio regolare:**
- -are → **-ato**: mangiare → mangiato
- -ere → **-uto**: credere → creduto
- -ire → **-ito**: dormire → dormito

**Participi irregolari comuni:**
fare → fatto | dire → detto | leggere → letto
scrivere → scritto | vedere → visto | prendere → preso`,
    exemplos: [
      'Ho mangiato una pizza.',
      'Hai dormito bene?',
      'Abbiamo fatto una passeggiata.',
      'Non ho capito niente.',
    ],
    exercicios: [
      esc('Com "avere", o participio de "mangiare" é:',['mangiato','mangiuto','mangito','mangato'],0,'Verbos em -are formam o participio com -ato: mangiare → mangiato.'),
      esc('Come si dice "Eu comi uma pizza"?',['Ho mangiato una pizza.','Sono mangiato una pizza.','Ho mangiuto una pizza.','Avevo mangiato una pizza.'],0,'"Mangiare" usa "avere". Io → ho. Participio: mangiato.'),
      esc('Qual è la forma corretta? "Lei ___ una lettera."',['ha scritto','ha scrivuto','è scritta','ha scrivo'],0,'"Scrivere" è irregolare: participio → scritto. Con lei → ha scritto.'),
      esc('"Você dormiu bem?" em italiano:',['Hai dormito bene?','Sei dormito bene?','Hai dormire bene?','Avevi dormito bene?'],0,'"Dormire" usa avere. Tu → hai. Participio: dormito.'),
      esc('Participio de "fare":',['fatto','fato','facuto','farito'],0,'"Fare" è irregolare. Participio: fatto.'),
      esc('"Noi ___ un film ieri sera."',['abbiamo visto','siamo visti','abbiamo veduto','avevamo visto'],0,'"Vedere" usa avere. Noi → abbiamo. Participio: visto.'),
      esc('Participio de "dire":',['detto','dito','dicuto','direto'],0,'"Dire" è irregolare. Participio: detto.'),
      esc('"Loro ___ tutto il giorno."',['hanno lavorato','sono lavorati','hanno lavorito','avevano lavorato'],0,'"Lavorare" usa avere. Loro → hanno. Participio: lavorato.'),
      rev('Traduzi: "Eu li um livro ontem."','Ho letto un libro ieri.','Leggere: participio irregolare → letto. Con io → ho letto.'),
      rev('Traduzi: "Vocês comeram em casa?"','Avete mangiato a casa?','Mangiare: avere, participio mangiato. Voi → avete.'),
      dig('Completa: "Ieri Maria ___ (scrivere) una email."','ha scritto','Ausiliare + participio irregolare','Scrivere usa avere. Lei → ha. Participio: scritto.'),
      dig('Participio passato de "prendere":','preso','Irregolare','Prendere è irregolare: participio → preso.'),
      esc('Qual frase é incorreta?',['Sono mangiato la pasta.','Ho comprato il pane.','Hai dormito?','Abbiamo fatto la spesa.'],0,'"Mangiare" usa avere, non essere. Corretto: Ho mangiato la pasta.'),
      rev('Traduzi: "Ele disse uma mentira."','Ha detto una bugia.','Dire: participio irregolare → detto. Lui → ha.'),
      esc('"Ho ___ (capire) la lezione."',['capito','caputo','capire','capisco'],0,'"Capire" usa avere. Participio regolare: capito.'),
    ]
  },

  // A2-VII: Passato Prossimo com essere
  {
    id: 'a2-vii', titulo: 'Passato Prossimo con essere',
    subtitulo: 'Verbos de movimento e stati', nivel: 'A2',
    teoria: `Com **essere** o participio **concorda** com il soggetto:

**Verbi con essere (mnemonica VANDERTRAMP + riflessivi):**
Venire, Andare, Nascere, Dovere (intransitivo), Entrare, Restare, Tornare, Rimanere, Arrivare, Morire, Partire

| Soggetto | Forma |
|----------|-------|
| io (m) | sono andato |
| io (f) | sono andata |
| loro (m/mista) | sono andati |
| loro (f) | sono andate |`,
    exemplos: [
      'Sono andato al supermercato.',
      'Maria è arrivata tardi.',
      'Siamo partiti ieri.',
      'I bambini sono nati a Roma.',
    ],
    exercicios: [
      esc('"Andare" usa quale ausiliare nel passato prossimo?',['essere','avere','stare','venire'],0,'"Andare" è un verbo di movimento → usa essere.'),
      esc('"Maria ___ a casa." (tornare)',['è tornata','ha tornato','è tornato','ha tornata'],0,'"Tornare" usa essere. Maria = femminile singular → tornata.'),
      esc('"Io (m) ___ a Milano." (andare)',['sono andato','sono andati','ho andato','sono andata'],0,'"Andare" + essere. Io maschile → andato.'),
      esc('"Le ragazze ___ presto." (partire)',['sono partite','sono partiti','hanno partito','sono partito'],0,'"Partire" usa essere. Le ragazze = femminile plural → partite.'),
      esc('"Noi ___ a Venezia." (arrivare)',['siamo arrivati','abbiamo arrivato','siamo arrivato','avevamo arrivato'],0,'"Arrivare" usa essere. Noi → siamo arrivati.'),
      rev('Traduzi (f): "Eu nasci em São Paulo."','Sono nata a San Paolo.','"Nascere" usa essere. Io femminile → nata.'),
      esc('"Tu (m) ___ a lungo." (rimanere)',['sei rimasto','hai rimasto','sei rimasta','eri rimasto'],0,'"Rimanere" usa essere. Tu maschile singular → rimasto.'),
      esc('Qual frase é correta?',['Sono venuta da Roma.','Ho venuto da Roma.','Sono venuto da Roma (dita da una donna).','Ho venuta da Roma.'],0,'"Venire" usa essere. Donna = venuta. Homem = venuto.'),
      dig('Completa: "I turisti ___ (arrivare) ieri."','sono arrivati','Movimento + plurale maschile','"Arrivare" usa essere. I turisti = maschile plurale → arrivati.'),
      esc('"La bambina ___ alle 8." (svegliarsi)',['si è svegliata','ha svegliata','è svegliata','si ha svegliata'],0,'Verbi riflessivi usano essere + si. Bambina = femminile → svegliata.'),
      rev('Traduzi: "Eles ficaram em casa."','Sono rimasti a casa.','"Rimanere" usa essere. Loro maschile → rimasti.'),
      esc('"Quanto tempo ___ qui?" (restare, tu)',['sei restato/a','hai restato','eri restato/a','hai rimasto'],0,'"Restare" usa essere.'),
      dig('Participio passato de "venire":','venuto','Irregolare','"Venire" è irregolare: participio → venuto.'),
      rev('Traduzi (misto): "Os meninos e as meninas chegaram."','I ragazzi e le ragazze sono arrivati.','Com grupos mistos, usa-se il maschile plural: arrivati.'),
      esc('Qual verbo usa AVERE (non essere)?',['mangiare','andare','partire','arrivare'],0,'"Mangiare" è transitivo → usa avere. I verbi di movimento usano essere.'),
    ]
  },

  // A2-VIII: Imperfetto
  {
    id: 'a2-viii', titulo: "L'Imperfetto Indicativo",
    subtitulo: 'Ações habituais ou contínuas no passado', nivel: 'A2',
    teoria: `**Imperfetto** = ação habitual, stato o descrizione nel passato

**Formazione** (radice + desinenza):
| | -are | -ere | -ire |
|--|------|------|------|
| io | -avo | -evo | -ivo |
| tu | -avi | -evi | -ivi |
| lui/lei | -ava | -eva | -iva |
| noi | -avamo | -evamo | -ivamo |
| voi | -avate | -evate | -ivate |
| loro | -avano | -evano | -ivano |

**Irregolari:** essere → ero/eri/era/eravamo/eravate/erano`,
    exemplos: [
      'Da bambino, giocavo ogni giorno.',
      'Quando ero piccola, abitavo a Milano.',
      'Leggeva sempre prima di dormire.',
      'Che tempo faceva ieri?',
    ],
    exercicios: [
      esc('"Parlare" all\'imperfetto, io:',['parlavo','parlevi','parlivo','parlavo'],0,'Imperfetto di -are: io → -avo. Parlare → parlavo.'),
      esc('"Credere" all\'imperfetto, lui:',['credeva','credava','crediva','aveva creduto'],0,'"Credere" è -ere. Lui → -eva. Credeva.'),
      esc('"Dormire" all\'imperfetto, noi:',['dormivamo','dormavamo','dormiamo','dormimmo'],0,'"Dormire" è -ire. Noi → -ivamo. Dormivamo.'),
      esc('"Essere" all\'imperfetto, io:',['ero','sono stato','stavo','fui'],0,'"Essere" è irregolare all\'imperfetto: io → ero.'),
      esc('"Essere" all\'imperfetto, loro:',['erano','stavano','erano stati','eravano'],0,'"Essere" imperfetto: loro → erano.'),
      rev('Traduzi: "Quando era bambino, mangiava molta pasta."','Quando era bambino, mangiava molta pasta.','Desccrição habitual no passado → imperfetto.'),
      esc('Quale frase usa correttamente l\'imperfetto?',['Da piccola, andavo al mare ogni estate.','Ieri, andavo al mare.','Domani, andavo al mare.','Adesso, andavo al mare.'],0,"L'imperfetto indica abitudine nel passato. 'Da piccola...ogni estate' → corretto."),
      esc('"Fare" all\'imperfetto, tu:',['facevi','favi','facevi','faevi'],0,'"Fare" imperfetto: tu → facevi (radice fac- + evi).'),
      dig('Coniuga "abitare" all\'imperfetto, voi:','abitavate','Radice + -avate','Abitare → radice abit- + -avate = abitavate.'),
      esc('"Che lavoro ___ (fare) tuo padre da giovane?"',['faceva','ha fatto','fece','faceva fare'],0,"Descrizione nel passato → imperfetto. Fare → faceva."),
      rev('Traduzi: "Eles estudavam italiano todos os dias."','Studiavano italiano tutti i giorni.','Imperfetto per abitudine. Loro → -avano. Studiare → studiavano.'),
      dig('Coniuga "essere" all\'imperfetto, noi:','eravamo','Irregolare','Essere imperfetto: noi → eravamo.'),
      esc('"Mentre tu ___ (dormire), io lavoravo."',['dormivi','hai dormito','dormi','dormiresti'],0,'Azione contemporanea nel passato → imperfetto. Tu → dormivi.'),
      esc('"Leggere" all\'imperfetto, loro:',['leggevano','leggevono','leggivano','leggavano'],0,'"Leggere" è -ere. Loro → -evano. Leggevano.'),
      rev('Traduzi: "Era una bella giornata."','Era una bella giornata.','Descrição de estado no passado → imperfetto. Era.'),
    ]
  },

  // A2-IX: Passato Prossimo vs Imperfetto
  {
    id: 'a2-ix', titulo: 'Passato Prossimo vs Imperfetto',
    subtitulo: 'Quando usare l\'uno o l\'altro', nivel: 'A2',
    teoria: `**Passato Prossimo** → azione **completa**, con limite di tempo, fatto specifico
**Imperfetto** → azione **abituale**, continua, descrizione, sfondo

| Passato Prossimo | Imperfetto |
|---|---|
| Ho mangiato una pizza (ieri) | Mangiavo la pizza ogni venerdì |
| È arrivato alle 8 | Arrivava sempre in ritardo |
| Ho visto il film | Vedeva i film il sabato |

**Parole-chiave:**
- PP: ieri, stamattina, una volta, l'anno scorso
- IMP: sempre, ogni giorno, di solito, da bambino`,
    exemplos: [
      'Ieri ho mangiato la pizza. (PP — fatto specifico)',
      'Da bambino mangiavo la pizza ogni venerdì. (IMP — abitudine)',
      'Mentre leggevo, ha suonato il telefono. (IMP sfondo + PP interruzione)',
    ],
    exercicios: [
      esc('"Ieri ___ una pizza." (mangiare)',['ho mangiato','mangiavo','mangiai','mangiato'],0,'"Ieri" = fatto specifico passato → passato prossimo. Ho mangiato.'),
      esc('"Da bambina, ___ la bicicletta ogni giorno." (usare)',['usavo','ho usato','uso','usai'],0,'"Da bambina...ogni giorno" = abitudine passata → imperfetto. Usavo.'),
      esc('"Mentre ___ (leggere, io), è arrivato Marco."',['leggevo','ho letto','leggerei','lessi'],0,"'Mentre' + azione di sfondo → imperfetto. Leggevo."),
      esc('"L\'anno scorso ___ (andare) in Italia."',['sono andato/a','andavo','vado','andrei'],0,'"L\'anno scorso" = fatto specifico → PP. Sono andato/a.'),
      esc('"Di solito, ___ (alzarsi) alle 7."',['mi alzavo','mi sono alzato','mi alzo','mi alzerei'],0,'"Di solito" = abitudine → imperfetto. Mi alzavo.'),
      rev('Scegli il tempo giusto: "Ieri mattina ho bevuto (PP) il caffè mentre _____(leggere, io) il giornale."','leggevo','Sfondo = imperfetto; azione puntuale = PP.'),
      esc('Quale frase è SBAGLIATA?',['Ogni giorno ho mangiato la pasta.','Ieri ho mangiato la pasta.','Di solito mangiavo la pasta.','Mangiavo la pasta ogni giorno.'],0,'"Ogni giorno" richiede imperfetto (abitudine), non PP.'),
      dig('Scegli: "Una volta alla settimana, (andare, noi) al cinema."','andavamo','Imperfetto — abitudine','Una volta alla settimana = abitudine → imperfetto. Andavamo.'),
      esc('"Stamattina mi ___ (svegliarsi) alle 6."',['sono svegliato/a','svegliavo','mi svegliavo','sveglierei'],0,'"Stamattina" = azione specifica recente → PP. Mi sono svegliato/a.'),
      esc('"Quando ___ (essere) piccolo, non ___ (guardare) la TV."',['ero / guardavo','ho ero / ho guardavo','ero / ho guardato','fui / guardai'],0,'"Quando ero piccolo" = descrizione + abitudine → entrambi imperfetto.'),
      rev('Traduzi: "Eu estava dormindo quando o telefone tocou."','Stavo dormendo quando ha suonato il telefono.','Sfondo (stavo dormendo = imperfetto) + interruzione (ha suonato = PP).'),
      esc('"Ieri sera ___ (vedere) un bel film."',['ho visto','vedevo','vedo','avevo visto'],0,'"Ieri sera" = fatto specifico → PP. Vedere: participio visto. Ho visto.'),
      esc('Quale parola di tempo chiede l\'imperfetto?',['sempre','ieri','stamattina','l\'anno scorso'],0,'"Sempre" indica abitudine → imperfetto. Le altre indicano fatti specifici → PP.'),
      rev('Scegli: "Da giovane, (lavorare) in un ristorante."','lavoravo','Da giovane = periodo passato continuo → imperfetto.'),
      esc('"Mentre Maria ___ (cucinare), io ___ (apparecchiare) la tavola."',['cucinava / apparecchiavo','ha cucinato / ho apparecchiato','cucinava / ho apparecchiato','cucinavo / apparecchiava'],0,'Azioni contemporanee nel passato → entrambe imperfetto.'),
    ]
  },

  // A2-X: Futuro Semplice
  {
    id: 'a2-x', titulo: 'Il Futuro Semplice',
    subtitulo: 'Ações e previsões futuras', nivel: 'A2',
    teoria: `**Futuro Semplice** = azione futura, previsione, probabilità

**Formazione** (infinito − e + desinenza):
| | -are/-ere | -ire |
|--|-----------|------|
| io | -erò | -irò |
| tu | -erai | -irai |
| lui/lei | -erà | -irà |
| noi | -eremo | -iremo |
| voi | -erete | -irete |
| loro | -eranno | -iranno |

**Irregolari comuni:**
essere → sarò | avere → avrò | fare → farò
andare → andrò | venire → verrò | volere → vorrò`,
    exemplos: [
      'Domani andrò al mare.',
      'L\'anno prossimo studieremo il giapponese.',
      'Sarà stanco dopo il lavoro. (probabilità)',
      'Cosa farai questo weekend?',
    ],
    exercicios: [
      esc('"Parlare" al futuro, io:',['parlerò','parlerà','parlarò','parlirò'],0,'Futuro di -are: io → -erò. Parl- + erò = parlerò.'),
      esc('"Partire" al futuro, noi:',['partiremo','parteremo','partiremo','partiamo'],0,'Futuro di -ire: noi → -iremo. Partir- + emo = partiremo.'),
      esc('"Essere" al futuro, loro:',['saranno','sarebbero','sono stati','saranno stati'],0,'"Essere" è irregolare. Futuro: loro → saranno.'),
      esc('"Andare" al futuro, tu:',['andrai','anderai','andirai','vai'],0,'"Andare" è irregolare. Tu → andrai.'),
      rev('Traduzi: "Amanhã faremos uma festa."','Domani faremo una festa.','Fare: irregolare. Noi → faremo. Domani = futuro.'),
      esc('"Cosa ___ (fare) questo weekend?"',['farai','facevi','fai','avresti fatto'],0,'Fare irregolare al futuro. Tu → farai.'),
      dig('Coniuga "venire" al futuro, io:','verrò','Irregolare','Venire è irregolare: io verrò (dopppia r).'),
      esc('"Avere" al futuro, lei:',['avrà','averà','avrebbe','aveva'],0,'"Avere" è irregolare. Futuro: lui/lei → avrà.'),
      esc('Quale frase esprime una probabilità?',['Sarà a casa — non risponde al telefono.','Sarà a casa domani.','Domani sarò a casa.','Lui sarebbe a casa.'],0,'Futuro per probabilità nel presente: "Sarà a casa" = probabilmente è a casa.'),
      rev('Traduzi: "No próximo ano, viajaremos pela Itália."','L\'anno prossimo viaggeremo per l\'Italia.','Viaggiare futuro: noi viaggeremo (gg mantido).'),
      esc('"Volere" al futuro, voi:',['vorrete','volereste','volete','vorreste'],0,'"Volere" è irregolare. Voi → vorrete.'),
      dig('Coniuga "essere" al futuro, noi:','saremo','Irregolare','Essere futuro: noi → saremo.'),
      esc('"Se piove, ___ (restare) a casa."',['resterò','rimarrò','rimango','resterei'],0,'Futuro per condizione reale: "se + presente → futuro". Restare → resterò.'),
      esc('"Potere" al futuro, loro:',['potranno','possono','potranno','poterebbero'],0,'"Potere" è irregolare. Loro → potranno.'),
      rev('Traduzi: "Ele terá 30 anos no próximo mês."','Il mese prossimo avrà trent\'anni.','Avere irregolare al futuro. Lui → avrà.'),
    ]
  },

  // A2-XI: Comparativi e Superlativi
  {
    id: 'a2-xi', titulo: 'Comparativi e Superlativi',
    subtitulo: 'Comparar qualidades e graus', nivel: 'A2',
    teoria: `**Comparativo di maggioranza:** più + aggettivo + di/che
**Comparativo di minoranza:** meno + aggettivo + di/che
**Comparativo di uguaglianza:** (così/tanto)... come/quanto

**Quando usare "di" vs "che":**
- "di" + pronome/nome semplice: Marco è più alto **di** me.
- "che" + aggettivo/verbo/preposizione: È più bello **che** intelligente.

**Superlativo relativo:** il/la più + aggettivo
**Superlativo assoluto:** aggettivo + -issimo/a/i/e

**Irregolari:** buono → migliore / ottimo | cattivo → peggiore / pessimo
grande → maggiore | piccolo → minore`,
    exemplos: [
      'Roma è più grande di Firenze.',
      'Questo libro è meno interessante di quello.',
      'Maria è (tanto) brava quanto Sofia.',
      'È il film più bello che ho visto.',
      'Questa pizza è buonissima!',
    ],
    exercicios: [
      esc('"Roma è ___ Firenze." (grande)',['più grande di','più grande che','grande di più','grande quanto'],0,'Comparativo di maggioranza tra due nomi: più + aggettivo + di.'),
      esc('Superlativo assoluto di "bello":',['bellissimo','il più bello','belissimo','bello molto'],0,'Superlativo assoluto: aggettivo + -issimo. Bello → bell- + issimo = bellissimo.'),
      esc('"È ___ (buono) della pizza che ho mangiato ieri."',['migliore','più buona','ottima','buonissima'],0,'"Buono" ha comparativo irregolare: migliore.'),
      esc('"Questo film è ___ quello." (interessante, -)',['meno interessante di','meno interessante che','più interessante di','tanto interessante come'],0,'Comparativo di minoranza: meno + adj + di + termine.'),
      rev('Traduzi: "Ela é tão inteligente quanto Marco."','È (tanto) intelligente quanto Marco.','Comparativo di uguaglianza: tanto... quanto.'),
      esc('"Parigi è ___ bella ___ romantica." (ugualmente)',['tanto / quanto','più / di','tanto / come','così / di'],0,'"Tanto bella quanto romantica" — uguaglianza tra due aggettivi.'),
      dig('Superlativo assoluto di "cattivo":','cattivissimo','Regolare: -issimo','Cattivo → cattivissimo. Irregolare: pessimo.','pessimo'),
      esc('"È più facile ___ difficile." (che/di?)',['che','di','quanto','così'],0,'"Che" si usa tra due aggettivi/verbi/avverbi. "Più facile che difficile".'),
      esc('Superlativo relativo: "È ___ ristorante della città."',['il migliore','il più buono','il buonissimo','il meglio'],0,'Superlativo relativo di "buono" → il migliore.'),
      rev('Traduzi: "Este exercício é mais difícil que o anterior."','Questo esercizio è più difficile del precedente / di quello precedente.','Comparativo di maggioranza: più... di/del.'),
      esc('"Grande" ha quale comparativo irregolare?',['maggiore','più grande','grandissimo','massimo'],0,'"Grande" → comparativo irregolare: maggiore.'),
      esc('"Questa torta è ___!" (buono — superlativo assoluto)',['buonissima','la più buona','ottimissima','buona assai'],0,'Superlativo assoluto regolare: buon- + -issima = buonissima.'),
      dig('Comparativo irregolare di "piccolo":','minore','Per età, importanza','Piccolo → minore (anche: più piccolo per dimensione fisica).','più piccolo'),
      rev('Traduzi: "Você é o melhor aluno da turma."','Sei il/la migliore studente della classe.','Superlativo relativo di buono → il migliore.'),
      esc('"Questo caffè è ___ (cattivo) di quello di ieri."',['peggiore','più cattivo','pessimo','molto cattivo'],0,'"Cattivo" ha comparativo irregolare: peggiore.'),
    ]
  },

  // A2-XII: Pronomi diretti
  {
    id: 'a2-xii', titulo: 'I Pronomi Diretti',
    subtitulo: 'lo, la, li, le — substituindo il complemento', nivel: 'A2',
    teoria: `**Pronomi diretti** sostituiscono il complemento oggetto diretto:

| Persona | Singolare | Plurale |
|---------|-----------|---------|
| 1ª | mi (me) | ci (nos) |
| 2ª | ti (te) | vi (vós) |
| 3ª m | lo (o) | li (os) |
| 3ª f | la (a) | le (as) |

**Posizione:** prima del verbo coniugato, o attaccato all'infinito/gerundio.
**Con il PP:** il participio concorda con il pronome diretto: Ho *visto* Maria → L'ho *vista*.`,
    exemplos: [
      'Mangio la pizza → La mangio.',
      'Conosco Marco → Lo conosco.',
      'Ho incontrato le ragazze → Le ho incontrate.',
      'Vuoi vedere il film? → Vuoi vederlo?',
    ],
    exercicios: [
      esc('"Conosco Marco." Con pronome:',['Lo conosco.','La conosco.','Li conosco.','Gli conosco.'],0,'Marco = maschile singolare → lo. Lo conosco.'),
      esc('"Mangio la mela." Con pronome:',['La mangio.','Lo mangio.','Le mangio.','Li mangio.'],0,'La mela = femminile singolare → la. La mangio.'),
      esc('"Vedo i ragazzi." Con pronome:',['Li vedo.','Le vedo.','Lo vedo.','Gli vedo.'],0,'I ragazzi = maschile plurale → li. Li vedo.'),
      esc('"Chiamo le amiche." Con pronome:',['Le chiamo.','Li chiamo.','La chiamo.','Gli chiamo.'],0,'Le amiche = femminile plurale → le. Le chiamo.'),
      esc('"Ho mangiato la pizza." Con pronome:',['L\'ho mangiata.','L\'ho mangiato.','La ho mangiata.','La ho mangiato.'],0,'La pizza = la. Con PP, il participio concorda: mangiata (f). L\'ho mangiata.'),
      rev('Sostituisci: "Compro i libri ogni settimana."','Li compro ogni settimana.','I libri = maschile plurale → li.'),
      esc('"Hai visto Maria?" Risposta affermativa:',['Sì, l\'ho vista.','Sì, la ho vista.','Sì, lo ho visto.','Sì, l\'ho visto.'],0,'Maria = la. Con PP femminile: vista. L\'ho vista (elisione con ho).'),
      esc('Dove va il pronome con l\'infinito?',['Si attacca: voglio vederlo','Va prima: lo voglio vedere','Entrambi sono corretti.','Non si usa con l\'infinito.'],2,'Con l\'infinito, il pronome può stare attaccato O prima del verbo modale.'),
      dig('Sostituisci: "Leggo il giornale ogni mattina."','Lo leggo ogni mattina.','Il giornale = m. sing. → lo','Il giornale = maschile singolare → lo.'),
      esc('"Hai chiamato tua sorella?" Risposta negativa:',['No, non l\'ho chiamata.','No, non la ho chiamata.','No, non lo ho chiamato.','No, non l\'ho chiamato.'],0,'Sorella = la. PP femminile: chiamata. Non l\'ho chiamata.'),
      rev('Sostituisci: "Aspetto gli amici al bar."','Li aspetto al bar.','Gli amici = maschile plurale → li.'),
      esc('"Vuoi mangiare la torta?" Con pronome:',['Vuoi mangiarla? / La vuoi mangiare?','Vuoi la mangiare?','Vuoi mangiarle?','Vuoi lo mangiare?'],0,'La torta = la. Con infinito: mangiarla / la vuoi mangiare.'),
      dig('Sostituisci "le ragazze": "Invito ___ alla festa."','le invito','Femminile plurale → le','Le ragazze = femminile plurale → le.'),
      esc('"Ci" come pronome diretto significa:',['noi (oggetto)','a noi','con noi','ci sono'],0,'"Ci" come pronome diretto = noi come complemento. Es: Mi vede → vede me. Ci vede → vede noi.'),
      rev('Sostituisci: "Ho perso i miei occhiali."','Li ho persi.','I miei occhiali = maschile plurale → li. PP concorda: persi.'),
    ]
  },

  // A2-XIII: Pronomi indiretti
  {
    id: 'a2-xiii', titulo: 'I Pronomi Indiretti',
    subtitulo: 'mi, ti, gli, le, ci, vi, loro', nivel: 'A2',
    teoria: `**Pronomi indiretti** sostituiscono il complemento di termine (a qualcuno):

| Persona | Forma |
|---------|-------|
| a me | mi |
| a te | ti |
| a lui | gli |
| a lei | le |
| a noi | ci |
| a voi | vi |
| a loro | gli (moderno) / loro |

**Verbi comuni con indiretto:** dare, dire, scrivere, telefonare, mandare, chiedere, rispondere, piacere, sembrare`,
    exemplos: [
      'Scrivo a Maria → Le scrivo.',
      'Telefono a Marco → Gli telefono.',
      'Mi piace la musica.',
      'Ci ha mandato un messaggio.',
    ],
    exercicios: [
      esc('"Scrivo a Maria." Con pronome:',['Le scrivo.','Gli scrivo.','La scrivo.','Lo scrivo.'],0,'A Maria = a lei → le. Le scrivo.'),
      esc('"Telefono a Marco." Con pronome:',['Gli telefono.','Le telefono.','Lo telefono.','La telefono.'],0,'A Marco = a lui → gli. Gli telefono.'),
      esc('"Mando un messaggio a te." Con pronome:',['Ti mando un messaggio.','Ti lo mando.','Gli mando un messaggio.','Le mando un messaggio.'],0,'A te → ti. Ti mando un messaggio.'),
      esc('"Piace" si usa con quale pronome indiretto?',['mi/ti/gli/le/ci/vi/gli','lo/la/li/le','me/te/lui/lei','si'],0,'"Piacere" richiede il pronome indiretto: mi piace, ti piace, gli piace...'),
      rev('Sostituisci: "Dico la verità a voi."','Vi dico la verità.','A voi → vi.'),
      esc('"A noi" diventa quale pronome?',['ci','vi','gli','le'],0,'"A noi" = ci come pronome indiretto.'),
      esc('"Ha risposto a me e a te."',['Ci ha risposto.','Vi ha risposto.','Gli ha risposto.','Le ha risposto.'],0,'A me e a te = a noi → ci.'),
      dig('Sostituisci "a Marco": "Dò il libro ___ Marco."','gli do il libro','A lui → gli','A Marco = a lui → gli.'),
      esc('"Mi piace" significa:',['Eu gosto (lit: para mim agrada)','Eu gosto de mim','Ele me gosta','Gosto dela'],0,'"Mi piace" = "a me piace" = eu gosto. Estrutura invertida.'),
      rev('Sostituisci: "Scrivo una lettera a mia madre."','Le scrivo una lettera.','A mia madre = a lei → le.'),
      esc('Differenza tra "lo" e "gli":',['lo = complemento diretto; gli = complemento indiretto','sono intercambiabili','lo = indiretto; gli = diretto','dipende dal verbo'],0,'"Lo" sostituisce il C.O. diretto. "Gli" sostituisce il C. di termine (a lui).'),
      esc('"Gli ho detto tutto." Significa:',['Ho detto tutto a lui.','L\'ho detto tutto.','Ho detto di tutto.','Gli ho parlato.'],0,'"Gli" = a lui. Ho detto tutto a lui.'),
      dig('Sostituisci "a loro": "Mando un regalo ___ loro."','gli mando un regalo','Moderno: gli per a loro','A loro → gli (moderno). Gli mando un regalo.'),
      esc('"Non ti ho chiamato." Significa:',['Não liguei para você.','Não me ligou.','Não o chamei.','Não me chamou.'],0,'"Ti" = complemento indiretto = a te = para você. Non ti ho chiamato.'),
      rev('Sostituisci: "Chiedo un favore a voi."','Vi chiedo un favore.','A voi → vi.'),
    ]
  },

  // A2-XIV: I Verbi Riflessivi
  {
    id: 'a2-xiv', titulo: 'I Verbi Riflessivi',
    subtitulo: 'alzarsi, lavarsi, vestirsi e altri', nivel: 'A2',
    teoria: `**Verbi riflessivi** = azione che ricade sul soggetto stesso.

**Pronomi riflessivi:** mi, ti, si, ci, vi, si

**Presente:**
| | alzarsi |
|--|---------|
| io | mi alzo |
| tu | ti alzi |
| lui/lei | si alza |
| noi | ci alziamo |
| voi | vi alzate |
| loro | si alzano |

**Al PP:** usano sempre **essere**. Il participio concorda col soggetto.
→ Mi sono alzato/a. | Si sono alzati/e.`,
    exemplos: [
      'Mi sveglio alle 7.',
      'Lei si trucca ogni mattina.',
      'Ci siamo divertiti molto!',
      'Come ti chiami?',
    ],
    exercicios: [
      esc('"Io ___ alle 7." (alzarsi)',['mi alzo','si alzo','mi alzi','ti alzo'],0,'Riflessivo di "alzarsi": io → mi alzo.'),
      esc('"Lei ___ prima di uscire." (truccarsi)',['si trucca','si trucco','ti trucca','la trucca'],0,'Riflessivo: lui/lei → si + verbo. Si trucca.'),
      esc('"Come ___ ?" (chiamarsi, tu)',['ti chiami','si chiami','ti chiama','vi chiami'],0,'Riflessivo: tu → ti chiami.'),
      rev('Coniuga: "Noi ci divertiamo molto."','Ci divertiamo molto.','Noi → ci. Il soggetto "noi" è spesso omesso.'),
      esc('"Loro ___ prima di andare a letto." (lavarsi)',['si lavano','si lavono','li lavano','si lavono'],0,'Riflessivo: loro → si lavano.'),
      esc('Al PP, "io (m) mi sono ___."',['alzato','alzata','alzati','alzate'],0,'PP riflessivo usa essere. Io maschile → alzato.'),
      dig('Coniuga "vestirsi" alla 3ª sing.: "Marco ___ in fretta."','si veste','Riflessivo: si + veste','Riflessivo: lui/lei → si + veste. Si veste.'),
      esc('"Vi siete divertiti?" significa:',['Você(s) se divertiram?','Vocês se divertiram (masc.)?','Nos divertimos?','Eles se divertiram?'],0,'"Vi" = 2ª plurale (voi). Vi siete = vós (plural) no PP. Maschile: divertiti.'),
      esc('"Mi sono ___ alle 8." (svegliarsi, f)',['svegliata','svegliato','svegliata','svegliate'],0,'Femminile singolare → svegliata. Mi sono svegliata.'),
      rev('Traduzi: "Eles se casaram em junho."','Si sono sposati a giugno.','Sposarsi: riflessivo. PP con essere. Maschile plurale → sposati.'),
      esc('Qual verbo NON è riflessivo?',['chiamare (qualcuno)','chiamarsi','lavarsi','vestirsi'],0,'"Chiamare" (transitivo) ≠ "chiamarsi" (riflessivo). "Chiamo Maria" vs "Mi chiamo Marco".'),
      dig('Coniuga "sedersi" alla 1ª sing. al presente:','mi siedo','Riflessivo irregolare','Sedersi: io mi siedo (irregolare).'),
      esc('"Ci siamo incontrati al bar." Soggetto:',['noi (m o misto)','voi','loro','io e te'],0,'"Ci" = noi. Siamo = PP essere. Incontrati = maschile/misto.'),
      rev('Coniuga all\'imperativo (tu): "si alzare"','Alzati!','Imperativo tu riflessivo: alzati (pronome si diventa ti).'),
      esc('"Loro ___ presto ogni mattina." (svegliarsi)',['si svegliano','si svegliamo','vi svegliano','si svegliano loro'],0,'Loro → si svegliano. La forma è la stessa del singolare ma il verbo è plurale.'),
    ]
  },

  // A2-XV: Pronomi combinati
  {
    id: 'a2-xv', titulo: 'Pronomi Combinati (intro)',
    subtitulo: 'me lo, te la, glielo...', nivel: 'A2',
    teoria: `Quando c'è un **pronome indiretto + diretto**, si combinano:

| Indiretto | + lo | + la | + li | + le |
|-----------|------|------|------|------|
| mi → | me lo | me la | me li | me le |
| ti → | te lo | te la | te li | te le |
| gli/le → | glielo | gliela | glieli | gliele |
| ci → | ce lo | ce la | ce li | ce le |
| vi → | ve lo | ve la | ve li | ve le |
| gli (loro) → | glielo | gliela | glieli | gliele |

**Ordine:** indiretto + diretto + verbo`,
    exemplos: [
      'Dammi il libro → Dammelo.',
      'Le ho dato la chiave → Gliel\'ho data.',
      'Ti mando il messaggio → Te lo mando.',
    ],
    exercicios: [
      esc('"Ti do il libro." Con combinato:',['Te lo do.','Me lo do.','Glielo do.','Ti lo do.'],0,'"Ti" + "lo" (il libro) → "te lo". Te lo do.'),
      esc('"Le porto la borsa." Con combinato:',['Gliela porto.','Le la porto.','Glielo porto.','La le porto.'],0,'"Le" + "la" (la borsa) → "gliela". Gliela porto.'),
      esc('"Mi manda il messaggio." Con combinato:',['Me lo manda.','Mi lo manda.','Ce lo manda.','Te lo manda.'],0,'"Mi" + "lo" (il messaggio) → "me lo". Me lo manda.'),
      esc('"Gli do i soldi." Con combinato:',['Glieli do.','Glielo do.','Li gli do.','Gli li do.'],0,'"Gli" + "li" (i soldi, m.pl.) → "glieli". Glieli do.'),
      rev('Trasforma: "Vi porto le pizze."','Ve le porto.','Vi + le → ve le.'),
      esc('"Ci dai le informazioni?" Con combinato:',['Ce le dai?','Vi le dai?','Ce li dai?','Gliele dai?'],0,'"Ci" + "le" (le informazioni, f.pl.) → "ce le". Ce le dai?'),
      dig('Combina: "ti" + "la":','te la','Indiretto mi/ti/ci/vi cambiano vocale','Ti + la = te la. (Mi → me, ti → te, ci → ce, vi → ve)'),
      esc('"Gli ho portato la torta." Con combinato:',['Gliel\'ho portata.','Gli la ho portata.','Gliela ho portata.','L\'ho portata.'],0,'"Gli" + "la" → "gliela". Con PP, participio concorda (la torta → portata). Gliel\'ho portata.'),
      esc('"Me lo" si forma da:',['mi + lo','me + lo','mi + la','me + li'],0,'"Mi" (indiretto 1ª sing.) + "lo" (diretto m.sing.) → "me lo".'),
      rev('Trasforma: "Gli spiego il problema."','Glielo spiego.','Gli + lo (il problema) = glielo.'),
      esc('Qual è la forma combinata di "vi + le"?',['ve le','vi le','ve li','gli le'],0,'"Vi" + "le" → "ve le". (Vi diventa ve prima del pronome diretto).'),
      dig('Combina: "gli" + "li":','glieli','Gli + li = glieli','Irregolare: gli + li = glieli.'),
      esc('"Me la dai?" Espandita:',['Mi dai la (cosa)?','Mi dai lo (cosa)?','Ti do la (cosa)?','Gli dai la (cosa)?'],0,'"Me la dai" = mi dai + la (cosa femminile).'),
      rev('Trasforma: "Ti mando le foto."','Te le mando.','Ti + le → te le.'),
      esc('"Glielo" può riferirsi a:',['a lui/a lei/a loro + lo','a lui + lo (solo)','a lei + lo (solo)','a loro + lo (solo)'],0,'"Gli" è usato per lui, lei e loro al moderno. Glielo può riferirsi a tutti e tre.'),
    ]
  },

];

// ─── B1 NEW UNITS (6–12) ──────────────────────────────────────────────────────

const b1Novas = [

  // B1-VI: Congiuntivo Presente
  {
    id: 'b1-vi', titulo: 'Il Congiuntivo Presente',
    subtitulo: 'Opinioni, dubbi e emozioni', nivel: 'B1',
    teoria: `**Congiuntivo presente** = soggettività, dubbio, emozione, volontà.

**Quando usarlo** (dopo):
- Penso che, Credo che, Spero che
- Voglio che, Preferisco che
- È importante che, È necessario che
- Benché, sebbene, affinché, prima che

**Formazione:**
| | -are | -ere | -ire |
|--|------|------|------|
| io/tu/lui | -i | -a | -a / -isca |
| noi | -iamo | -iamo | -iamo |
| voi | -iate | -iate | -iate |
| loro | -ino | -ano | -ano / -iscano |`,
    exemplos: [
      'Penso che lui abbia ragione.',
      'Voglio che tu studi di più.',
      'È importante che parliamo.',
      'Benché sia stanco, continuo a lavorare.',
    ],
    exercicios: [
      esc('"Penso che lei ___ (avere) ragione."',['abbia','ha','avrà','aveva'],0,'Dopo "penso che" → congiuntivo. Avere: lui/lei → abbia.'),
      esc('"Voglio che tu ___ (venire)."',['venga','viene','verrà','veniva'],0,'Dopo "voglio che" → congiuntivo. Venire: tu → venga.'),
      esc('Congiuntivo di "essere", io/tu/lui/lei:',['sia','è','era','sarebbe'],0,'"Essere" congiuntivo: io/tu/lui/lei → sia.'),
      esc('"È necessario che voi ___ (parlare)."',['parliate','parlate','parlino','parlerete'],0,'Voi → congiuntivo -iate. Parlare → parliate.'),
      rev('Completa: "Spero che Marco ___ (arrivare) in tempo."','arrivi','Sperare che → congiuntivo. Lui → arrivi.'),
      esc('"Benché ___ (essere) tardi, rimango."',['sia','è','fosse','sarà'],0,'"Benché" → congiuntivo presente. Essere → sia.'),
      dig('Coniuga "fare" al congiuntivo, io:','faccia','Irregolare','Fare congiuntivo: io faccia (irregolare).'),
      esc('"Penso che loro ___ (capire)."',['capiscano','capiscono','capiranno','capissero'],0,'"Capire" (-ire isc): loro → capiscano al congiuntivo.'),
      esc('"Prima che lui ___ (partire), parliamo."',['parta','parte','partirà','partiva'],0,'"Prima che" → congiuntivo. Partire: lui → parta.'),
      rev('Completa: "È importante che noi ___ (studiare)."','studiamo','Noi → congiuntivo. Studiare: noi → studiamo (uguale al presente!).'),
      esc('"Avere" al congiuntivo, loro:',['abbiano','avranno','hanno','avessero'],0,'Avere congiuntivo: loro → abbiano.'),
      dig('Congiuntivo di "sapere", tu:','sappia','Irregolare','Sapere congiuntivo: tu sappia.'),
      esc('"Affinché tu ___ (capire), spiego ancora."',['capisca','capisci','capirai','capivi'],0,'"Affinché" → congiuntivo. Capire (isc): tu → capisca.'),
      rev('Completa: "Sebbene ___ (fare) freddo, escono."',  'faccia','Sebbene → congiuntivo. Fare: lui → faccia.'),
      esc('"Dubito che ___ (essere, loro) a casa."',['siano','sono','saranno','fossero'],0,'"Dubitare che" → congiuntivo. Essere: loro → siano.'),
    ]
  },

  // B1-VII: Condizionale Presente
  {
    id: 'b1-vii', titulo: 'Il Condizionale Presente',
    subtitulo: 'Ipotesi, desideri, richieste cortesi', nivel: 'B1',
    teoria: `**Condizionale presente** = ipotesi, desiderio, richiesta gentile, consiglio.

**Formazione** (stessa radice del futuro + desinenze):
| | Desinenza |
|--|-----------|
| io | -ei |
| tu | -esti |
| lui/lei | -ebbe |
| noi | -emmo |
| voi | -este |
| loro | -ebbero |

**Irregolari** (stessa radice del futuro):
essere → sarei | avere → avrei | andare → andrei
fare → farei | venire → verrei | volere → vorrei`,
    exemplos: [
      'Vorrei un caffè, per favore.',
      'Potresti aiutarmi?',
      'Al posto tuo, studierei di più.',
      'Con più tempo, farei un viaggio.',
    ],
    exercicios: [
      esc('"Volere" al condizionale, io:',['vorrei','voglio','vorrò','volevo'],0,'"Vorrei" = condizionale di volere. Irregolare (radice vorr- + ei).'),
      esc('"Potere" al condizionale, tu:',['potresti','puoi','potrài','potessi'],0,'Potere condizionale: tu → potresti.'),
      esc('"Essere" al condizionale, lui:',['sarebbe','è','sarà','fosse'],0,'"Essere" condizionale: lui/lei → sarebbe.'),
      esc('"Al posto tuo, io ___ (studiare) di più."',['studierei','studio','studierò','studiavo'],0,'"Al posto tuo" + condizionale. Studiare: io → studierei.'),
      rev('Traduzi cortesemente: "Posso avere il conto?"','Potrei avere il conto? / Vorrei il conto.','Condizionale per cortesia: potrei, vorrei.'),
      dig('Coniuga "fare" al condizionale, noi:','faremmo','Irregolare: far- + emmo','Fare condizionale: noi faremmo.'),
      esc('"Con più soldi, ___ (comprare, noi) una casa."',['compreremmo','compremo','compreremo','compriamo'],0,'Condizionale noi: compr- + eremmo = compreremmo.'),
      esc('"Avere" al condizionale, loro:',['avrebbero','hanno','avranno','avessero'],0,'Avere condizionale: loro → avrebbero.'),
      esc('Come si chiede cortesemente?',['Potresti aprire la finestra?','Puoi aprire la finestra?','Apri la finestra!','Aprirai la finestra?'],0,'Il condizionale "potresti" è più gentile del presente "puoi".'),
      rev('Traduzi: "Eu gostaria de aprender o piano."','Vorrei imparare il pianoforte.','Volere condizionale = vorrei. Seguito da infinito.'),
      esc('"Venire" al condizionale, voi:',['verreste','venite','verrete','veniste'],0,'Venire condizionale: voi → verreste.'),
      dig('Coniuga "andare" al condizionale, io:','andrei','Irregolare: andr- + ei','Andare condizionale: io andrei.'),
      esc('"Mi ___ (dare, tu) una mano?"',['daresti','dai','darai','davi'],0,'Condizionale per richiesta cortese. Dare: tu → daresti.'),
      rev('Traduzi: "Eles viriam, mas são ocupados."','Verrebbero, ma sono occupati.','Venire condizionale: loro → verrebbero.'),
      esc('"Sapere" al condizionale, lei:',['saprebbe','sa','saprà','sapesse'],0,'Sapere condizionale: lui/lei → saprebbe.'),
    ]
  },

  // B1-VIII: Pronomi Relativi
  {
    id: 'b1-viii', titulo: 'I Pronomi Relativi',
    subtitulo: 'che, cui, il quale', nivel: 'B1',
    teoria: `**Pronomi relativi** collegano due frasi riferendosi allo stesso elemento.

**Che** (soggetto o complemento diretto):
→ Il ragazzo **che** studia. / Il libro **che** leggo.

**Cui** (dopo preposizione):
→ La città **in cui** vivo. / L\'amico **con cui** parlo.

**Il quale/la quale/i quali/le quali** (formale, con preposizione):
→ La signora **alla quale** ho scritto.

**Chi** = colui che (chi studia vince):
→ **Chi** non risica, non rosica.`,
    exemplos: [
      'La pizza che ho mangiato era buonissima.',
      'Il ragazzo con cui studio si chiama Marco.',
      'Questo è il motivo per cui sono qui.',
      'Chi studia ottiene buoni risultati.',
    ],
    exercicios: [
      esc('"Il libro ___ ho comprato è interessante."',['che','cui','quale','chi'],0,'"Che" sostituisce il complemento diretto (ho comprato il libro). → che.'),
      esc('"La città ___ vivo si chiama Roma."',['in cui','che','chi','il quale'],0,'"In cui" = preposizione + cui. Vivo in Roma → la città in cui vivo.'),
      esc('"L\'amico ___ parlo si chiama Luca."',['con cui','che','con quale','cui'],0,'"Parlo con Luca" → con cui. L\'amico con cui parlo.'),
      rev('Completa: "La ragazza ___ ho visto è bella."','che','Complemento diretto (ho visto la ragazza) → "che".'),
      esc('"Il motivo ___ sono qui è importante."',['per cui','che','per il quale','per chi'],0,'"Per cui" = per + cui. "Per" richiede "cui" non "che".'),
      esc('"___ non studia, non impara."',['Chi','Che','Cui','Il quale'],0,'"Chi" = colui/colei che. Senso generico. Chi non studia, non impara.'),
      dig('Inserisci il pronome: "La professoressa ___ insegna è brava."','che','Soggetto della relativa → che','La professoressa + che + verbo. Soggetto → "che".'),
      esc('"Il collega con ___ lavoro è simpatico."',['cui','che','il quale','chi'],0,'Con = preposizione → cui. Con cui lavoro.'),
      esc('"La casa in ___ abito è grande."',['cui','che','quale','chi'],0,'In = preposizione → cui. In cui abito.'),
      rev('Completa: "Gli amici ___ ho invitato sono arrivati."','che','Complemento diretto → che. Ho invitato gli amici → che.'),
      esc('"La signora ___ ho parlato è la direttrice."',['con cui / con la quale','che','di cui','la quale'],0,'"Parlo con la signora" → con cui / con la quale (formale).'),
      dig('Scegli: "Il paese ___ vengo si chiama Napoli."','da cui','Da + cui','Da Napoli vengo → da cui. Il paese da cui vengo.'),
      esc('"Il libro di ___ ti ho parlato..."',['cui','che','chi','il quale'],0,'"Di" + pronome relativo → di cui. (Ti ho parlato del libro → di cui).'),
      rev('Completa: "___ arriva primo vince il premio."','Chi','Chi = colui che. Senso indefinito/generico.'),
      esc('"La ragione ___ me ne vado è personale."',['per cui','che','per la quale','per chi'],0,'"Per cui" = la ragione per la quale. Può usarsi anche "per la quale" (formale).'),
    ]
  },

  // B1-IX: La Forma Passiva
  {
    id: 'b1-ix', titulo: 'La Forma Passiva',
    subtitulo: 'essere/venire + participio passato', nivel: 'B1',
    teoria: `**Passivo** = l\'azione È SUBITA dal soggetto.

**Formazione:** essere/venire + participio passato (concorda col soggetto)

| Tempo | Attivo | Passivo |
|-------|--------|---------|
| Presente | Mangiano la pizza | La pizza è/viene mangiata |
| Passato | Hanno scritto il libro | Il libro è stato scritto |
| Futuro | Scriveranno la lettera | La lettera sarà scritta |

**Agente:** introdotto da "da":
→ Il pane è fatto **dalla** nonna.

**"Venire"** sostituisce essere al presente/imperfetto (non al PP).`,
    exemplos: [
      'La torta è/viene preparata dalla mamma.',
      'Il documento è stato firmato dal direttore.',
      'Questa casa sarà venduta presto.',
      'La legge viene rispettata da tutti.',
    ],
    exercicios: [
      esc('Trasforma in passivo: "Lo chef prepara la cena."',['La cena è/viene preparata dallo chef.','La cena ha preparato dallo chef.','La cena prepara dallo chef.','La cena viene preparato dallo chef.'],0,'La cena (f) = soggetto passivo. Essere + preparata (f). Agente: dallo chef.'),
      esc('Il participio nel passivo concorda con:',['il soggetto grammaticale','il verbo essere','il complemento di agente','il tempo verbale'],0,'Nel passivo, il participio concorda con il soggetto (chi subisce l\'azione).'),
      esc('"Il libro ___ (scrivere, presente pass.) da Calvino."',['è/viene scritto','è scritto da','viene scrivuto','è scrittura'],0,'Presente passivo: è/viene + scritto (m.sing.). Concordanza: il libro → scritto.'),
      rev('Trasforma: "Hanno costruito il ponte nel 1900."','"Il ponte è stato costruito nel 1900."','Passato passivo: essere al PP + participio. Il ponte (m) → costruito.'),
      esc('"La lettera sarà ___ domani." (spedire)',['spedita','spedito','spediti','spedata'],0,'Futuro passivo: sarà + participio. La lettera (f) → spedita.'),
      esc('Quale ausiliare NON si usa nel passivo al PP?',['venire','essere','stare (in alcuni casi)','andare'],0,'"Venire" non si usa al passato prossimo. Al PP si usa solo "essere stato".'),
      dig('Trasforma: "Tutti rispettano la legge." → Passivo','La legge è/viene rispettata da tutti.','Soggetto nuovo = la legge (f); agente = da tutti','La legge (f) → rispettata. Agente: da tutti.'),
      esc('"I libri ___ (leggere, presente passivo) dagli studenti."',['vengono letti','sono letti','vengono letto','sono leto'],0,'"Venire" al presente passivo. I libri (m.pl.) → letti. Vengono letti.'),
      esc('"Da" nel passivo introduce:',['l\'agente (chi fa l\'azione)','il tempo','il luogo','il fine'],0,'"Da" nel passivo introduce l\'agente: "scritto da Dante" → Dante è l\'agente.'),
      rev('Trasforma: "Il governo approverà la legge."','La legge sarà approvata dal governo.','Futuro passivo: sarà + approvata (f). Agente: dal governo.'),
      esc('"Le case erano ___ (costruire, imperf. passivo) velocemente."',['costruite','costruiti','costruito','costruendo'],0,'Imperfetto passivo: erano + costruite (f.pl.). Le case → costruite.'),
      dig('Trasforma: "Gli studenti capiscono il problema." → Passivo','Il problema è/viene capito dagli studenti.','Il problema (m) → capito; agente: dagli studenti','Il problema (m.sing.) → capito. Agente: dagli studenti.'),
      esc('"Si mangia bene in Italia." È una forma:',['passiva impersonale con "si"','attiva','riflessiva','imperativa'],0,'"Si + verbo attivo" può avere valore passivo impersonale: si mangia = viene mangiato.'),
      rev('Trasforma: "Michelangelo ha dipinto la Cappella Sistina."','La Cappella Sistina è stata dipinta da Michelangelo.','PP passivo: essere al PP + dipinta (f). Agente: da Michelangelo.'),
      esc('"Il progetto ___ (completare, futuro passivo) entro maggio."',['sarà completato','viene completato','è completato','verrà completato'],2,'Futuro passivo: sarà / verrà + completato (m). Entrambi sono corretti.'),
    ]
  },

  // B1-X: Il Gerundio
  {
    id: 'b1-x', titulo: 'Il Gerundio',
    subtitulo: 'Stare + gerundio, azioni simultanee', nivel: 'B1',
    teoria: `**Gerundio:**
- Presente: -are → -ando | -ere/-ire → -endo
- Irregolari: fare → facendo | dire → dicendo | bere → bevendo

**Usi principali:**
1. **Stare + gerundio** = azione in corso (progressivo)
   → Sto studiando. Stavo mangiando.
2. **Azione simultanea:** Camminando, penso. (mentre cammino)
3. **Mezzo/modo:** Studiando ogni giorno, si impara.
4. **Causa:** Essendo stanco, ho dormito.`,
    exemplos: [
      'Sto leggendo un libro.',
      'Stava piovendo quando sono uscito.',
      'Studiando, ho capito tutto.',
      'Essendo in ritardo, ho corso.',
    ],
    exercicios: [
      esc('Gerundio di "mangiare":',['mangiando','mangiante','mangiato','mangiare'],0,'Gerundio di -are: mangi- + ando = mangiando.'),
      esc('"Sto ___ (leggere) un romanzo."',['leggendo','letto','leggere','leggo'],0,'"Stare + gerundio" per azione in corso. Leggere → leggendo.'),
      esc('Gerundio di "fare":',['facendo','fando','faccendo','facente'],0,'"Fare" è irregolare. Gerundio: facendo.'),
      esc('"Stava ___ (dormire) quando ho chiamato."',['dormendo','dormito','dormire','dormiente'],0,'Imperfetto progressivo: stava + dormendo.'),
      rev('Trasforma: "Mentre studiava, ascoltava musica."','Studiando, ascoltava musica.','Gerundio sostituisce "mentre" + imperfetto.'),
      esc('Gerundio di "dire":',['dicendo','dendo','dicente','direndo'],0,'"Dire" è irregolare. Gerundio: dicendo.'),
      dig('Coniuga il progressivo: "Loro ___ (mangiare) adesso."','stanno mangiando','Stare (pl.) + gerundio','Stare: loro → stanno. Gerundio: mangiando. Stanno mangiando.'),
      esc('"___ (Camminare), ho incontrato un amico."',['Camminando','Camminato','Camminare','Cammino'],0,'Gerundio in apertura = azione simultanea. Camminare → camminando.'),
      esc('Gerundio di "bere":',['bevendo','berendo','bevuto','berendo'],0,'"Bere" è irregolare. Gerundio: bevendo.'),
      rev('Completa: "___ (essere) stanca, sono andata a letto presto."','Essendo','Gerundio di essere = essendo. Causa.'),
      esc('"Stai ___ (scrivere) una lettera?"',['scrivendo','scritto','scrivere','scriva'],0,'"Stare + gerundio". Scrivere → scrivendo.'),
      dig('Forma il progressivo passato: "Io ___ (lavorare) quando hai chiamato."','stavo lavorando','Stavo + gerundio','Imperfetto progressivo: stavo (io) + lavorando.'),
      esc('"Essendo in ritardo, ___ (correre)."',['ho corso','correndo','corsi','corro'],0,'"Essendo" = causa. La frase principale usa il PP: ho corso.'),
      rev('Trasforma in progressivo: "Leggo adesso."','Sto leggendo adesso.','Stare (io) → sto. Leggere → leggendo.'),
      esc('"___ (Studiare) ogni giorno, si imparano molte cose."',['Studiando','Studiato','Studiare','Studio'],0,'Gerundio = mezzo/condizione. Studiare → studiando.'),
    ]
  },

  // B1-XI: Il Congiuntivo Imperfetto
  {
    id: 'b1-xi', titulo: 'Il Congiuntivo Imperfetto',
    subtitulo: 'Periodo ipotetico e frasi al passato', nivel: 'B1',
    teoria: `**Congiuntivo imperfetto** dopo "se" (tipo 2), "come se", e frasi al passato.

**Formazione:**
| | -are | -ere | -ire |
|--|------|------|------|
| io/tu | -assi | -essi | -issi |
| lui/lei | -asse | -esse | -isse |
| noi | -assimo | -essimo | -issimo |
| voi | -aste | -este | -iste |
| loro | -assero | -essero | -issero |

**Essere:** fossi, fossi, fosse, fossimo, foste, fossero

**Periodo ipotetico (tipo 2):** Se + congiuntivo imp. → condizionale presente`,
    exemplos: [
      'Se avessi più tempo, studierei di più.',
      'Vorrei che tu venissi con me.',
      'Parlava come se fosse un professore.',
      'Pensavo che lui partisse domani.',
    ],
    exercicios: [
      esc('"Se ___ (avere) i soldi, comprerei una moto."',['avessi','ho','avrò','abbia'],0,'Periodo ipotetico tipo 2: se + congiuntivo imperfetto. Avere: io → avessi.'),
      esc('"Essere" al congiuntivo imperfetto, io:',['fossi','ero','sia','fosse'],0,'"Essere" congiuntivo imperfetto: io → fossi.'),
      esc('"Se ___ (potere) volare, andrei ovunque."',['potessi','posso','potrei','possa'],0,'Se + congiuntivo imp. Potere: io → potessi.'),
      rev('Completa: "Vorrei che lui ___ (venire) alla festa."','venisse','Vorrire che → congiuntivo. Venire imperfetto: lui → venisse.'),
      esc('"Parlava come se ___ (essere) stanco."',['fosse','è','sia','sarà'],0,'"Come se" → congiuntivo imperfetto. Essere: lui → fosse.'),
      dig('Coniuga "andare" al cong. imperfetto, tu:','andassi','Radice + -assi','Andare congiuntivo imperfetto: tu → andassi.'),
      esc('"Se ___ (sapere, tu) la verità, cosa faresti?"',['sapessi','sai','saprai','sappia'],0,'Tipo 2. Sapere: tu → sapessi.'),
      esc('"Pensavo che lei ___ (partire) oggi."',['partisse','parte','partirà','parta'],0,'"Pensavo che" (passato) → congiuntivo imperfetto. Lei → partisse.'),
      rev('Completa: "Se ___ (essere) in Italia, mangerei la pizza vera."','fossi','Tipo 2. Essere: io → fossi.'),
      esc('"Magari ___ (avere) più coraggio!"',['avessi','abbia','ho','avrò'],0,'"Magari" esprime desiderio irreale → congiuntivo imperfetto. Io → avessi.'),
      dig('Congiuntivo imperfetto di "fare", loro:','facessero','Radice fac- + -essero','Fare congiuntivo imperfetto: loro → facessero.'),
      esc('"Se ___ (essere) ricco, viaggerei tutto l\'anno."',['fossi','sia','ero','sarò'],0,'Tipo 2. Essere: io → fossi.'),
      esc('"Credevo che voi ___ (volere) venire."',['voleste','volete','vorreste','vogliate'],0,'Credevo che (passato) → congiuntivo imperfetto. Voi → voleste.'),
      rev('Completa: "Come se non ___ (capire, lei) niente!"','capisse','Come se → congiuntivo imperfetto. Lei → capisse.'),
      esc('Dove si usa il congiuntivo imperfetto invece di quello presente?',['Quando la frase principale è al passato','Sempre','Con "penso che"','Con frasi al futuro'],0,'Consecutio temporum: frase principale al passato → congiuntivo imperfetto nella frase dipendente.'),
    ]
  },

  // B1-XII: I Verbi Modali al Passato
  {
    id: 'b1-xii', titulo: 'I Modali al Passato',
    subtitulo: 'dovere, potere, volere al PP', nivel: 'B1',
    teoria: `**Modali al passato prossimo:**

**Con avere:** se il verbo successivo usa avere
→ Ho dovuto lavorare. | Ho potuto venire.

**Con essere:** se il verbo successivo usa essere
→ Sono dovuto/a andare. | Sono potuto/a partire.

**Significati:**
- **Ho dovuto:** ero obbligato (e l\'ho fatto)
- **Avrei dovuto:** ero obbligato (ma non l\'ho fatto) — condizionale passato
- **Ho potuto:** ho avuto la possibilità (e l\'ho fatto)
- **Non ho potuto:** non ho avuto la possibilità`,
    exemplos: [
      'Ho dovuto lavorare tutto il giorno.',
      'Sono dovuta andare dal medico.',
      'Avrebbe potuto chiamare! (ma non ha chiamato)',
      'Non ho voluto mangiare la carne.',
    ],
    exercicios: [
      esc('"Ieri ___ (dovere) lavorare fino a tardi." (io)',['ho dovuto','sono dovuto','dovevo','dovrò'],0,'"Lavorare" usa avere → modale usa avere. Ho dovuto lavorare.'),
      esc('"Maria ___ (dovere) andare dal medico."',['è dovuta andare','ha dovuto andare','era dovuta','è dovuta'],0,'"Andare" usa essere → modale usa essere. È dovuta (f) andare.'),
      esc('"___ (potere, noi) finalmente partire!"',['Siamo potuti partire','Abbiamo potuto partire','Eravamo potuti','Siamo potuti'],0,'"Partire" usa essere. Modali → siamo potuti (m/misto) partire.'),
      rev('Completa: "Lui ___ (volere, neg.) mangiare la verdura."','non ha voluto mangiare','Mangiare usa avere → ha voluto. Non ha voluto mangiare.'),
      esc('"Avrebbe dovuto chiamare" significa:',['Era obbligato ma non l\'ha fatto.','Ha chiamato.','Dovrà chiamare.','Stava chiamando.'],0,'Condizionale passato del modale = obbligo non adempiuto.'),
      esc('"___ (potere, tu) venire ieri?"',['Hai potuto venire?','Sei potuto venire?','Potevi venire?','Potresti venire?'],0,'"Venire" usa essere, ma il modale con venire può usare anche avere nella prassi. Formalmente: sei potuto venire. Colloquialmente: hai potuto venire.'),
      dig('Completa: "Non ___ (volere, lei) uscire ieri."','ha voluto','Uscire usa essere, ma colloquialmente avere è accettato','Non ha voluto uscire (colloquiale). Non è voluta uscire (formale).','è voluta'),
      esc('"Ho voluto" indica:',['Ho fatto la cosa liberamente / per scelta','Ero obbligato','Non ho potuto','Sarò obbligato'],0,'"Volere al PP" = ho scelto di farlo. "Non ho voluto" = ho rifiutato.'),
      rev('Traduzi: "Eu tive que estudar a noite toda."','Ho dovuto studiare tutta la notte.','Dovere + studiare (avere) → ho dovuto studiare.'),
      esc('"Avrei potuto farlo, ma ___ (non fare)."',['non l\'ho fatto','non faccio','non farei','non facevo'],0,'"Avrei potuto" = c\'era possibilità ma non ho sfruttato. Implica che non l\'ho fatto.'),
      dig('Completa: "I bambini ___ (dovere) andare a letto presto."','sono dovuti andare','Andare = essere → sono dovuti','Andare usa essere → modali: sono dovuti (m.pl.) andare.'),
      esc('"Non ho potuto dormire" significa:',['Non sono riuscito a dormire.','Non volevo dormire.','Non dovevo dormire.','Dormivo male.'],0,'"Non ho potuto dormire" = impossibilità. Non c\'era la possibilità di dormire.'),
      rev('Completa: "___ (volere, voi) venire, ma eravate occupati."',  'Avreste voluto venire','Condizionale passato = desiderio non realizzato.'),
      esc('"Avrebbe dovuto studiare" implica:',['Non ha studiato (e avrebbe dovuto).','Ha studiato.','Studia adesso.','Studierà domani.'],0,'Condizionale passato di "dovere" = rimprovero / obbligo non rispettato.'),
      esc('Quando si usa "essere" con i modali al PP?',['Quando il verbo all\'infinito usa essere','Sempre','Mai','Con solo "andare" e "venire"'],0,'La scelta di essere/avere dipende dal verbo che segue il modale.'),
    ]
  },

];

// ─── B2 NEW UNITS (6–10) ──────────────────────────────────────────────────────

const b2Novas = [

  // B2-VI: Congiuntivo Passato e Trapassato
  {
    id: 'b2-vi', titulo: 'Congiuntivo Passato e Trapassato',
    subtitulo: 'Azioni passate nella frase subordinata', nivel: 'B2',
    teoria: `**Congiuntivo passato** = azione precedente rispetto alla principale al presente.
Formazione: congiuntivo di essere/avere + participio passato.
→ Penso che **abbia mangiato**. | Spero che **sia partita**.

**Congiuntivo trapassato** = azione precedente rispetto alla principale al passato.
Formazione: congiuntivo imperfetto di essere/avere + participio passato.
→ Pensavo che **avesse mangiato**. | Credevo che **fosse partita**.

**Consecutio Temporum:**
| Principale | Congiuntivo |
|---|---|
| presente (penso) | presente / passato |
| passato (pensavo) | imperfetto / trapassato |`,
    exemplos: [
      'Penso che lui abbia già mangiato.',
      'È probabile che lei sia partita ieri.',
      'Credevo che tu avessi capito.',
      'Pensavo che fossero rimasti a casa.',
    ],
    exercicios: [
      esc('"Penso che lui ___ già (mangiare)."',['abbia mangiato','ha mangiato','abbia mangiare','avesse mangiato'],0,'Principale al presente → cong. passato. Avere + mangiato. Lui → abbia mangiato.'),
      esc('"È probabile che lei ___ (partire)."',['sia partita','è partita','fosse partita','abbia partito'],0,'Partire usa essere. Cong. passato: sia + partita (f).'),
      esc('"Credevo che tu ___ (capire)."',['avessi capito','abbia capito','hai capito','capissi'],0,'Principale al passato → cong. trapassato. Avere + capito. Tu → avessi capito.'),
      rev('Completa: "Pensavo che loro ___ (andare) via."','fossero andati','Andare usa essere. Trapassato: fossero + andati (m.pl.).'),
      esc('"Spero che ___ (essere) un buon viaggio."',['sia stato','fosse stato','è stato','sia'],0,'Sperare + passato. Essere: congiuntivo passato → sia stato.'),
      dig('Congiuntivo trapassato di "fare", lei:','avesse fatto','Avesse (cong. imp.) + fatto','Trapassato: avesse (lei) + fatto.'),
      esc('"Non credo che lui ___ (dire) la verità."',['abbia detto','ha detto','avesse detto','dice'],0,'"Non credo che" + presente → cong. passato. Dire: avere + detto. Lui → abbia detto.'),
      esc('"Pensavo che voi ___ (venire) prima."',['foste venuti','siate venuti','aveste venuto','siete venuti'],0,'Venire usa essere. Trapassato: foste + venuti (voi).'),
      rev('Completa: "Sembra che qualcuno ___ (entrare) di notte."','sia entrato','Sembrare + cong. passato. Entrare usa essere → sia entrato.'),
      esc('"Dubitavo che lei ___ (finire) in tempo."',['avesse finito','abbia finito','ha finito','finisse'],0,'Dubitavo (passato) → trapassato. Finire + avere: avesse finito.'),
      dig('Cong. trapassato di "essere", loro:','fossero stati','Fossero (essere, cong. imp.) + stati','Essere: trapassato → fossero stati.'),
      esc('"È strano che non ci ___ (scrivere, loro)."',['abbiano scritto','avessero scritto','hanno scritto','scrivano'],0,'Cong. passato (principale al presente). Scrivere + avere: abbiano scritto.'),
      rev('Completa: "Credevo che Mario ___ (uscire) prima di me."','fosse uscito','Uscire usa essere. Trapassato: fosse + uscito.'),
      esc('"Mi dispiace che tu ___ (sentire) male ieri."',['ti sia sentito/a male','ti sentivi male','ti abbia sentito male','ti sentissi male'],0,'Dispiacere + cong. passato. Sentirsi (riflessivo + essere): ti sia sentito/a male.'),
      esc('Quale sequenza è corretta?',['Pensavo (passato) → cong. trapassato','Penso (presente) → cong. trapassato','Pensavo (passato) → cong. passato','Penso (presente) → cong. imperfetto'],0,'Consecutio: passato → trapassato; presente → passato.'),
    ]
  },

  // B2-VII: Il Periodo Ipotetico
  {
    id: 'b2-vii', titulo: 'Il Periodo Ipotetico',
    subtitulo: 'Tipo 1, 2 e 3: reale, possibile, impossibile', nivel: 'B2',
    teoria: `**Tre tipi di periodo ipotetico:**

| Tipo | Condizione | Conseguenza |
|------|-----------|-------------|
| 1 (reale) | se + presente | presente / futuro |
| 2 (possibile) | se + cong. imperfetto | condizionale presente |
| 3 (impossibile) | se + cong. trapassato | condizionale passato |

**Tipo 1:** Se ho tempo, vengo / verrò.
**Tipo 2:** Se avessi tempo, verrei.
**Tipo 3:** Se avessi avuto tempo, sarei venuto/a.
**Misto (2+3):** Se fossi partito prima, adesso non sarei qui.`,
    exemplos: [
      'Tipo 1: Se piove, resto a casa.',
      'Tipo 2: Se potessi volare, andrei ovunque.',
      'Tipo 3: Se avessi studiato, avrei superato l\'esame.',
      'Misto: Se avessi mangiato, adesso non avrei fame.',
    ],
    exercicios: [
      esc('"Se ___ (avere) tempo, vengo." (Tipo 1)',['ho','avessi','avrei','abbia'],0,'Tipo 1 (reale): se + presente. Ho.'),
      esc('"Se ___ (potere) volare, andrei ovunque." (Tipo 2)',['potessi','posso','potrò','abbia potuto'],0,'Tipo 2 (possibile): se + cong. imperfetto. Potere: io → potessi.'),
      esc('"Se ___ (studiare) di più, ___ superato l\'esame." (Tipo 3)',['avessi studiato / avrei','ho studiato / ho','studiassi / supererei','studiavo / supererei'],0,'Tipo 3 (impossibile): se + cong. trapassato → condizionale passato. Avessi studiato / avrei superato.'),
      rev('Completa (Tipo 2): "Se ___ (essere) ricco, comprerei una villa."','fossi','Se + cong. imperfetto. Essere: io → fossi.'),
      esc('"Se avessi avuto i soldi, ___ (comprare) la casa." (Tipo 3)',['avrei comprato','comprerei','compravo','comprassi'],0,'Tipo 3. Conseguenza: condizionale passato. Comprare → avrei comprato.'),
      esc('Quale frase usa il periodo ipotetico misto?',['Se fossi partito ieri, adesso sarei già a Roma.','Se parto, vengo.','Se partissi, verrei.','Se fossi partito, sarei venuto.'],0,'Misto: condizione nel passato (fossi partito) + conseguenza nel presente (sarei già a Roma).'),
      dig('Completa (Tipo 1): "Se ___ (fare) bel tempo, andiamo al mare."','fa','Presente → presente','Tipo 1: se + presente indicativo. Fare: fa.'),
      esc('"Se avessimo saputo, ___ (venire, noi)." (Tipo 3)',['saremmo venuti','veremmo','siamo venuti','verremmo'],0,'Tipo 3. Venire usa essere. Condizionale passato: saremmo + venuti.'),
      esc('"Se ___ (lavorare) di più, guadagneresti di più." (Tipo 1 o 2?)',['Tipo 2 (possibile)','Tipo 1 (reale)','Tipo 3 (impossibile)','Tipo misto'],0,'Cong. imperfetto (lavorassi) → Tipo 2.'),
      rev('Completa (Tipo 3): "Se Maria ___ (arrivare) prima, avremmo parlato."','fosse arrivata','Arrivare usa essere. Cong. trapassato: fosse + arrivata (f).'),
      esc('"Se studiassi ogni giorno, ___ in italiano."',['parleresti bene / parleresti bene','avrei parlato','hai parlato','parli'],0,'Tipo 2. Consequenza: condizionale presente.'),
      dig('Costruisci il Tipo 3: "se + lui + avere + tempo"','se avesse avuto tempo','Cong. trapassato di avere','Avere + cong. imp. + avuto = avesse avuto.'),
      esc('"Se avessi dormito di più, adesso ___ stanco." (misto)',['non sarei','non sono','non fosse','non saresti'],0,'Misto: condizione passata (avessi dormito) + conseguenza presente (non sarei stanco adesso).'),
      rev('Tipo 2: "Se ___ (volere, tu) imparare, dovresti studiare."','volessi','Se + cong. imperfetto. Volere: tu → volessi.'),
      esc('Il condizionale passato è formato da:',['condizionale presente di essere/avere + participio','congiuntivo imperfetto + participio','futuro + participio','imperfetto + participio'],0,'Condizionale passato: avrei/sarei (condizionale pres.) + participio passato.'),
    ]
  },

  // B2-VIII: Il Discorso Indiretto
  {
    id: 'b2-viii', titulo: 'Il Discorso Indiretto',
    subtitulo: 'Riportare le parole di qualcuno', nivel: 'B2',
    teoria: `**Discorso diretto → indiretto:**

**Trasformazioni principali:**
| Diretto | Indiretto |
|---------|-----------|
| presente | imperfetto |
| futuro | condizionale presente |
| PP | trapassato prossimo |
| imperativo | che + congiuntivo / di + infinito |

**Pronomi e avverbi:**
- io → lui/lei | qui → lì | oggi → quel giorno | domani → il giorno dopo

**Verbi introduttori:** dire, spiegare, chiedere, rispondere, affermare, negare`,
    exemplos: [
      '"Studio italiano." → Ha detto che studiava italiano.',
      '"Verrò domani." → Ha detto che sarebbe venuto il giorno dopo.',
      '"Studia!" → Gli ha detto di studiare.',
      '"Hai mangiato?" → Mi ha chiesto se avevo mangiato.',
    ],
    exercicios: [
      esc('"Mangio la pizza." → Ha detto che ___',['mangiava la pizza.','mangia la pizza.','avrebbe mangiato la pizza.','abbia mangiato la pizza.'],0,'Discorso indiretto: presente → imperfetto.'),
      esc('"Verrò domani." → Ha detto che ___',['sarebbe venuto il giorno dopo.','verrà il giorno dopo.','è venuto il giorno dopo.','venisse il giorno dopo.'],0,'Futuro → condizionale presente. Domani → il giorno dopo.'),
      esc('"Ho già mangiato." → Ha detto che ___',['aveva già mangiato.','ha già mangiato.','avesse già mangiato.','mangiai.'],0,'PP → trapassato prossimo. Aveva mangiato.'),
      rev('Trasforma: "Vieni qui!" → Gli ha detto ___','di venire lì.','Imperativo → di + infinito. Qui → lì.'),
      esc('"Sono stanco." → Ha detto che ___',['era stanco.','è stanco.','fosse stanco.','sia stanco.'],0,'Presente essere → imperfetto: era stanco.'),
      esc('"Studia di più!" → Gli ha detto ___',['di studiare di più.','che studiasse di più.','di studio di più.','che studia di più.'],0,'Imperativo → di + infinito (stessa persona). Di studiare.'),
      dig('Trasforma: "Abito a Roma." → Mi ha detto che ___','abitava a Roma.','Presente → imperfetto','Abito → abitavo (imperfetto). Io → lui/lei.'),
      esc('"Hai fame?" → Mi ha chiesto ___',['se avevo fame.','che avevo fame.','se ho fame.','di avere fame.'],0,'Domanda → se + imperfetto (al passato). Se avevo fame.'),
      esc('"Non so niente." → Ha detto che ___',['non sapeva niente.','non sa niente.','non sapesse niente.','non sappia niente.'],0,'So (presente) → sapeva (imperfetto).'),
      rev('Trasforma: "Partirò la settimana prossima." → Ha detto che ___','sarebbe partito la settimana successiva.','Futuro → condizionale. Prossima → successiva.'),
      esc('"Telefona a Marco!" → Gli ha detto ___',['di telefonare a Marco.','che telefonasse a Marco.','di telefonerà a Marco.','che telefona a Marco.'],0,'Imperativo → di + infinito. Di telefonare.'),
      dig('Trasforma: "Siamo arrivati ieri." → Ha detto che ___','erano arrivati il giorno prima.','PP → trapassato; ieri → il giorno prima','Essere arrivati → erano arrivati. Ieri → il giorno prima.'),
      esc('"Dove sei?" → Mi ha chiesto ___',['dove fossi. / dove ero.','dove sono.','se ero là.','che ero lì.'],0,'Domanda indiretta + imperfetto. Dove fossi (cong.) o dove ero (ind.).'),
      rev('Trasforma: "Non ho capito niente." → Ha detto che ___','non aveva capito niente.','PP → trapassato prossimo.'),
      esc('"Puoi aiutarmi?" → Mi ha chiesto ___',['se potevo aiutarlo/a.','di aiutarlo/a.','se posso aiutarlo/a.','che potessi aiutarlo/a.'],0,'Domanda con modale → se + condiz. o imperfetto. Se potevo aiutarlo.'),
    ]
  },

  // B2-IX: Connettivi e Strutture Avanzate
  {
    id: 'b2-ix', titulo: 'Connettivi e Strutture Avanzate',
    subtitulo: 'Coesione testuale e registro formale', nivel: 'B2',
    teoria: `**Connettivi causali:** perché, poiché, dato che, siccome, visto che
**Connettivi concessivi:** benché/sebbene/nonostante + congiuntivo; pur + gerundio
**Connettivi finali:** affinché, perché (+ cong.), in modo che
**Connettivi temporali:** non appena, una volta che, dopo che, prima che
**Connettivi avversativi:** tuttavia, eppure, ciononostante, d\'altra parte
**Connettivi consecutivi:** quindi, pertanto, di conseguenza, dunque`,
    exemplos: [
      'Poiché era tardi, siamo andati a casa.',
      'Benché fosse stanco, ha continuato a lavorare.',
      'Studio affinché tu possa essere orgoglioso di me.',
      'Non appena arriverà, ti chiamerò.',
      'Ha piovuto; tuttavia, siamo usciti lo stesso.',
    ],
    exercicios: [
      esc('"___ (causa) era tardi, siamo partiti." Quale connettivo?',['Poiché / Siccome / Dato che','Benché','Affinché','Tuttavia'],0,'"Poiché", "siccome", "dato che" introducono una causa. "Era tardi" = causa della partenza.'),
      esc('"___ (concessione) fosse stanco, ha lavorato."',['Benché/Sebbene','Perché','Quindi','Dunque'],0,'Connettivo concessivo + congiuntivo: benché/sebbene fosse stanco.'),
      esc('"Studio ___ tu possa essere orgoglioso."',['affinché','perché (indicativo)','siccome','tuttavia'],0,'"Affinché" introduce uno scopo/fine + congiuntivo.'),
      rev('Scegli il connettivo giusto: "___ è arrivato, abbiamo iniziato la riunione."','Non appena / Appena','Connettivo temporale di immediata successione.'),
      esc('"Ha mangiato troppo; ___, si è sentito male."',['di conseguenza / pertanto','tuttavia','benché','affinché'],0,'"Di conseguenza/pertanto" introduce una conseguenza.'),
      esc('"Pur ___ (studiare), non supera gli esami."',['studiando','studii','studiasse','studio'],0,'"Pur + gerundio" = concessione. Pur studiando = anche se studia.'),
      dig('Scegli: "Non è venuto; ___, l\'aspettavamo."','eppure / tuttavia / ciononostante','Avversativo','Connettivi avversativi: eppure, tuttavia, ciononostante.'),
      esc('"Parla italiano ___ (come se, ipotetico) fosse italiano."',['come se','benché','affinché','siccome'],0,'"Come se" + congiuntivo introduce un confronto ipotetico.'),
      esc('"___ aver studiato, non ricordo niente." (nonostante)',['Nonostante','Benché','Poiché','Siccome'],0,'"Nonostante" può essere seguito da infinito (stesso soggetto): nonostante aver studiato.'),
      rev('Collega con un connettivo: "Era malata. Ha lavorato lo stesso."','Sebbene/Benché fosse malata, ha lavorato lo stesso. / Era malata; tuttavia ha lavorato.','Concessione (benché+cong.) o avversativo (tuttavia).'),
      esc('"___ arriverai, chiamami." (temporale di anteriorità)',['Non appena','Dopo che','Prima che','Quando'],0,'"Non appena" = immediatamente dopo. Temporale di immediata successione.'),
      esc('"È partito ___ avvisarci." (senza che)',['senza','senza che','prima di','affinché'],0,'"Senza" + infinito (stesso soggetto). È partito senza avvisarci.'),
      dig('Connettivo di conclusione/sintesi:','in conclusione / dunque / quindi','Connettivi conclusivi','Dunque, quindi, in conclusione, pertanto = risultato/conclusione.'),
      esc('"___ le difficoltà, ha portato a termine il progetto."',['Nonostante','Poiché','Affinché','Dunque'],0,'"Nonostante" + sostantivo = concessione (senza congiuntivo).'),
      rev('Riscrivi: "Visto che non ho soldi, non posso andare al cinema."','Siccome/Poiché/Dato che non ho soldi, non posso andare al cinema.','Sinonimi di "visto che" (causali).'),
    ]
  },

  // B2-X: Stile Formale e Letterario
  {
    id: 'b2-x', titulo: 'Stile Formale e Letterario',
    subtitulo: 'Registro scritto, passato remoto, inversioni', nivel: 'B2',
    teoria: `**Passato Remoto** (vs PP): usato nel Sud Italia, testi storici e letterari.
→ Dante nacque nel 1265. | Mio nonno conobbe mia nonna nel 1950 (registro formale).

**Infinito sostantivato:** il mangiare, il bere, il sapere (nominalizzazione).
**Costruzioni impersonali formali:** si afferma, si ritiene, si è dimostrato.
**Inversione soggetto-verbo:** "Ha detto lui" → énfasi.
**Nominalizzazioni formali:** realizzazione, comprensione, elaborazione.
**Forme participiali:** trattandosi di, tenuto conto di, fermo restando che.`,
    exemplos: [
      'Si è dimostrato che il progetto è fattibile.',
      'Tenuto conto delle circostanze, la decisione appare giusta.',
      'Il sapere è potere.',
      'Trattandosi di una questione urgente, agiremo subito.',
    ],
    exercicios: [
      esc('"Dante ___ (nascere) nel 1265." (letterario)',['nacque','è nato','era nato','nasce'],0,'Passato remoto per fatti storici lontani: nascere → nacque.'),
      esc('"___ ritenuto opportuno rimandare la riunione." (impersonale formale)',['Si è','È stato','Si è stato','Si'],0,'"Si è ritenuto" = costruzione impersonale passiva formale.'),
      esc('"___ di una questione urgente, agiremo subito."',['Trattandosi','Siccome si tratta','Sebbene trattando','Trattando si'],0,'"Trattandosi di" = forma participiale assoluta formale. = Dato che si tratta di.'),
      rev('Nominalizza: "capire bene un testo"','la comprensione di un testo / il capire bene un testo','Nominalizzazione formale.'),
      esc('"___ conto delle difficoltà, il risultato è soddisfacente."',['Tenuto','Tenendo','Avendo tenuto','Tenuta'],0,'"Tenuto conto di" = locuzione formale assoluta. Invariabile.'),
      esc('"Il sapere ___ potere." (proverbio/registro elevato)',['è','fa','dà','ha'],0,'Infinito sostantivato come soggetto: "il sapere" = la conoscenza. È potere.'),
      dig('Passato remoto di "fare", lui (storico):','fece','Irregolare','Fare passato remoto: lui → fece.'),
      esc('"Si è dimostrato che" = ?',['È stato provato/dimostrato (impersonale).','Ha dimostrato.','Mi ha dimostrato.','Si dimostra (presente).'],0,'"Si è dimostrato" = costruzione impersonale formale al PP.'),
      esc('"___ restando le condizioni attuali, il piano è valido."',['Fermo','Restando fermo','Fermo rimanendo','Rimasto fermo'],0,'"Fermo restando (che)" = locuzione formale = "sempre che/a condizione che".'),
      rev('Trasforma in stile formale: "Pensando ai risultati, possiamo essere soddisfatti."','Alla luce dei risultati / Considerati i risultati, possiamo ritenerci soddisfatti.','Stile formale: nominalizz., participio assoluto.'),
      esc('Passato remoto di "essere", loro:',['furono','erano','sono stati','sarebbero'],0,'Essere passato remoto: loro → furono.'),
      esc('"Ha detto lui" (con inversione) enfatizza:',['chi ha parlato (lui, non altri)','quando ha parlato','cosa ha detto','come ha parlato'],0,"L'inversione soggetto-verbo in italiano è usata per enfatizzare il soggetto."),
      dig('Forma impersonale formale di "si ritiene":','si ritiene che + congiuntivo','Impersonale formale + congiuntivo','Si ritiene che + cong.: "Si ritiene che il progetto sia fattibile."'),
      esc('"L\'___ del problema richiede tempo." (elaborare → nominalizz.)',['elaborazione','elaborato','elaborare','elaborazione'],0,'Nominalizzazione: elaborare → l\'elaborazione. Registro formale/burocratico.'),
      rev('Passato remoto di "nascere", io (formale):','nacqui','Irregolare: nasc- → nacqui','"Nascere" passato remoto: io → nacqui.'),
    ]
  },

];

// ─── Inject into grammar.json ────────────────────────────────────────────────

// A2 (module index 1)
const a2 = g.moduli['1'];
a2Novas.forEach(u => a2.unidades.push(u));
console.log('A2: ' + a2.unidades.length + ' unidades');

// B1 (module index 2)
const b1 = g.moduli['2'];
b1Novas.forEach(u => b1.unidades.push(u));
console.log('B1: ' + b1.unidades.length + ' unidades');

// B2 (module index 3)
const b2 = g.moduli['3'];
b2Novas.forEach(u => b2.unidades.push(u));
console.log('B2: ' + b2.unidades.length + ' unidades');

// Save
fs.writeFileSync(gramPath, JSON.stringify(g, null, 2), 'utf8');
console.log('grammar.json atualizado com sucesso!');
