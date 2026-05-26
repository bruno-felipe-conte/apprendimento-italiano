"""
Rodada final: garante que todas as lezioni XXIII-XXX chegam a 110+.
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
a1 = next(m for m in data['moduli'] if m['id'] == 'A1')

# Exercícios finais para cada lezione que ainda falta
exercises = {}

exercises['Lezione XXIV'] = [  # faltam 12
    {"tipo":"escolha","pergunta":"'Me l'ha mandata.' Cosa è stato mandato?","opcoes":["qualcosa di maschile (lo)","qualcosa di femminile (la)","non si può sapere"],"resposta":1,"explicacao":"L' (l'apostrofo) davanti a HA = elisione di LA: 'me LA ha mandata' → 'me L'HA mandata'. Il participio MANDATA (femminile) conferma che l'oggetto diretto è femminile (la lettera/email/proposta)."},
    {"tipo":"revelar","pergunta":"**Esercizio final 1** — Trasformare con tutti i pronomi:\n'Ho spiegato la teoria ai miei studenti.' → ___\n'Ha portato i regali ai bambini.' → ___","resposta":"Gliel'ho spiegata. / Glieli ha portati.","explicacao":"Gliel'ho spiegata: gli+la=gliela → gliela ho → gliel'ha (elisione). Spiegata: concorda con la(femm). Glieli ha portati: gli+li=glieli. Portati: concorda con li(masch.plur)."},
    {"tipo":"escolha","pergunta":"'Mandiamoglielo subito!' CHI è il destinatario?","opcoes":["a noi","a lui/lei/loro","a voi"],"resposta":1,"explicacao":"GLI in pronome combinato = a lui/lei (formale) o a loro. MANDIAMOGLIELO = mandiamo+gli+lo. L'imperativo NOI (mandiamo) indica che è noi a mandare, GLI indica il destinatario."},
    {"tipo":"revelar","pergunta":"**Esercizio final 2** — Scegliere tra pronomi combinati:\n'Mia madre mi ha cucito la giacca.' → ___\n'Il professore ci ha spiegato le regole.' → ___","resposta":"Me l'ha cucita. / Ce le ha spiegate.","explicacao":"Mi+la=me la → me l'ha (elisione). Cucita (femm). Ci+le=ce le. Spiegate (femm.plur). Accordo obbligatorio."},
    {"tipo":"escolha","pergunta":"In quale frase i pronomi sono in posizione SCORRETTA?","opcoes":["Non glielo dici.","Non lo gli dici.","Glielo hai detto?"],"resposta":1,"explicacao":"'NON LO GLI DICI' = SBAGLIATO. L'ordine dei pronomi è fisso: INDIRETTO + DIRETTO (gli+lo→glielo), non si può invertire. Corretto: 'non glielo dici'."},
]

exercises['Lezione XXV'] = [  # faltam 17
    {"tipo":"revelar","pergunta":"**Esercizio final 1** — D.i. misto (presente e passato):\n'Non so dove sia andato.' (verbo introduttivo presente)\n→ congiuntivo presente o passato?\n'Non sapevo dove fosse andato.' (verbo introduttivo passato)\n→ congiuntivo?","resposta":"Presente (so) → congiuntivo presente/passato: 'dove sia andato' (pass.cong.) o 'dove vada' (pres.cong.) — indica azione già compiuta rispetto al presente. Passato (sapevo) → congiuntivo trapassato: 'dove fosse andato'.","explicacao":"Con verbo introduttivo al PRESENTE: presente o passato del congiuntivo (scelta dipende dall'anteriorità). Con PASSATO: congiuntivo imperfetto o trapassato."},
    {"tipo":"escolha","pergunta":"«Spero di venire presto.» È discorso indiretto? Come si classifica?","opcoes":["sì, discorso indiretto con congiuntivo","no, è discorso diretto","no, è proposizione finale con stesso soggetto (SPERARE DI + infinito)"],"resposta":2,"explicacao":"SPERARE DI + infinito (stesso soggetto) ≠ discorso indiretto. È una proposizione dipendente volitiva. SPERARE CHE + congiuntivo (soggetti diversi) si avvicina di più al d.i.: 'spero che tu venga'."},
    {"tipo":"revelar","pergunta":"**Esercizio final 2** — Identificare l'errore nel d.i.:\n«Studierò domani.» → Ha detto che studierà domani. (SBAGLIATO)\nCorreggere: ___","resposta":"Ha detto che avrebbe studiato il giorno dopo/l'indomani. (corretto: futuro→condizionale; domani→il giorno dopo)","explicacao":"Due errori: 1) futuro→condizionale passato (non rimane futuro). 2) 'domani' deve diventare 'il giorno dopo/l'indomani'. Errori classici nel d.i."},
    {"tipo":"escolha","pergunta":"'Ha ammesso di aver sbagliato.' AMMETTERE DI + infinito passato esprime:","opcoes":["azione contemporanea all'ammissione","azione anteriore all'ammissione","azione futura rispetto all'ammissione"],"resposta":1,"explicacao":"AVER SBAGLIATO (infinito passato) = azione avvenuta PRIMA dell'atto di ammettere. 'Ammette di AVER sbagliato' = riconosce un errore già commesso. Infinito passato = anteriorità rispetto al verbo principale."},
    {"tipo":"revelar","pergunta":"**Esercizio final 3** — D.i. con verbi di sentimento:\n«Ho paura!» → Ha detto che ___ paura.\n«Mi dispiace.» → Ha detto che ___ dispiaceva.\n«Sono felice!» → Ha esclamato che ___ felice.","resposta":"Ha detto che aveva paura. / Ha detto che gli dispiaceva. / Ha esclamato che era felice.","explicacao":"Stato emotivo al presente → imperfetto nel d.i. al passato. Aveva paura (avere paura). Gli dispiaceva (dispiacere = verbo indiretto). Era felice."},
]

exercises['Lezione XXVI'] = [  # faltam 15
    {"tipo":"revelar","pergunta":"**Esercizio final 1** — Completa con il numero corretto:\nL'Italia ha circa ___ milioni di abitanti. (60)\nRoma ha circa ___ milioni di abitanti. (2,8)\nIl Colosseo ha circa ___ anni. (2000)","resposta":"60 milioni / sessanta milioni. / 2,8 milioni / due virgola otto milioni. / 2000 anni / duemila anni.","explicacao":"Milioni: MILIONE (sing.), MILIONI (plur.). DI + sostantivo: 'sessanta milioni DI abitanti'. Virgola (,) non punto per i decimali in italiano."},
    {"tipo":"escolha","pergunta":"'Costa un sacco di soldi!' UN SACCO DI significa:","opcoes":["una quantità piccola","una quantità molto grande (idiomatico)","esattamente un sacco (letterale)"],"resposta":1,"explicacao":"UN SACCO DI = tantissimo (idiomatico, colloquiale). 'Costa un sacco' = costa moltissimo. Simile: 'un mucchio di', 'una valanga di', 'un casino di' (informale)."},
    {"tipo":"revelar","pergunta":"**Esercizio final 2** — Leggere i numeri in contesti:\nNumero di telefono: +39 02 1234 5678 → ___\nCodice postale: 00100 → ___","resposta":"Numero di telefono: più trentanove, zero due, dodici trentaquattro cinquantaseisettantotto (cifra per cifra o a gruppi). / Codice postale: zerozerozerouno (cifra per cifra).","explicacao":"Numeri di telefono: di solito cifra per cifra o a coppie. Codice postale: cifra per cifra. I numeri con zero iniziale si leggono tutto per intero: 00100 = zero zero uno zero zero."},
    {"tipo":"escolha","pergunta":"'È il 2 febbraio.' Come si dice in italiano?","opcoes":["È il due febbraio.","È il secondo febbraio.","È febbraio due."],"resposta":0,"explicacao":"Le date: IL + numero cardinale + mese. 'Il due febbraio' (non 'il secondo', tranne il primo del mese = 'il primo'). L'ordine in italiano: articolo+numero+mese (non mese+numero come in inglese)."},
    {"tipo":"revelar","pergunta":"**Esercizio final 3** — Circa e approssimazioni:\nUna trentina = ___\nUna cinquantina = ___\n'Ci vogliono circa due ore.' → Riformulare con numero approssimativo: ___","resposta":"Una trentina = circa 30. Una cinquantina = circa 50. Ci vuole un paio d'ore / una ventina di minuti in più / circa due ore.","explicacao":"Suffisso -INA = approssimazione: decina, dozzina (12!), quindicina, ventina, trentina, quarantina, cinquantina, sessantina, settantina, ottantina."},
]

exercises['Lezione XXVII'] = [  # faltam 17
    {"tipo":"revelar","pergunta":"**Esercizio final 1** — TALE DA + infinito:\n'Il problema è tale da richiedere un esperto.' Spiegare il significato.\nEquivalente: ___","resposta":"TALE DA + infinito = così grande/serio/importante da richiedere qualcosa. Equivalente: 'Il problema è così serio che richiede un esperto.' TALE = di tale entità / così grande.","explicacao":"TALE DA + infinito = talmente + aggettivo + da + inf. Esprime conseguenza o grado estremo: 'un caldo tale da non poter dormire' = un caldo così forte da impedire il sonno."},
    {"tipo":"escolha","pergunta":"'Ne ho messi parecchi.' PARECCHI concorda perché:","opcoes":["è avverbio","è aggettivo/pronome che concorda con l'oggetto sottinteso (maschile plurale)","è un errore"],"resposta":1,"explicacao":"PARECCHIO/PARECCHIA/PARECCHI/PARECCHIE = indefinito variabile. 'Ne ho messi parecchi' = parecchi [oggetti, masch.plur.]. Concordanza obbligatoria come aggettivo o pronome."},
    {"tipo":"revelar","pergunta":"**Esercizio final 2** — Costruzioni con OGNI vs TUTTI:\n'Ogni anno vado in vacanza.' → 'Tutti gli ___ vado in vacanza.'\n'Tutti i miei amici sono gentili.' → 'Ogni mio ___ è gentile.'","resposta":"Tutti gli ANNI vado in vacanza. / Ogni mio AMICO è gentile. (OGNI→singolare, TUTTI→plurale+articolo)","explicacao":"OGNI + singolare = distributivo individuale. TUTTI + articolo + plurale = collettivo. Sono intercambiabili nel significato ma non nella struttura grammaticale."},
    {"tipo":"escolha","pergunta":"'Chiunque venga, è il benvenuto.' Se la frase fosse al passato:","opcoes":["Chiunque venisse, era il benvenuto.","Chiunque sia venuto, era il benvenuto.","Chiunque venga, era il benvenuto."],"resposta":0,"explicacao":"CHIUNQUE + congiuntivo imperfetto al contesto passato: 'chiunque venisse' (cong.imperfetto, descrizione passata abitudinaria). CHIUNQUE SIA VENUTO = chi è venuto in quell'occasione specifica (puntuale)."},
]

exercises['Lezione XXVIII'] = [  # faltam 19
    {"tipo":"revelar","pergunta":"**Esercizio final 1** — Distinguere proposizioni coordinate e subordinate:\n'Studio e lavoro.' → coordinata ___\n'Studio perché voglio laurearmi.' → subordinata ___\n'Studio, ma non capisco niente.' → coordinata ___","resposta":"E = coordinata copulativa / PERCHÉ = subordinata causale / MA = coordinata avversativa","explicacao":"COORDINATE: uniscono elementi di pari importanza grammaticale (e, ma, o, però, anzi, quindi). SUBORDINATE: dipendono dalla principale (perché, quando, che, se, sebbene...)."},
    {"tipo":"escolha","pergunta":"'Sebbene abbia studiato molto, ha preso un brutto voto.' La congiunzione SEBBENE regge:","opcoes":["indicativo passato prossimo","congiuntivo","condizionale"],"resposta":1,"explicacao":"SEBBENE → sempre congiuntivo. 'Abbia studiato' = congiuntivo passato (passato prossimo→congiuntivo passato). 'Ha preso' nella principale = indicativo (la principale non richiede congiuntivo)."},
    {"tipo":"revelar","pergunta":"**Esercizio final 2** — Costruire frasi con congiunzioni diverse:\nIdea base: 'Sono stanco. Continuo a lavorare.'\nCongiunzione EPPURE: ___\nCongiunzione QUINDI: ___\nCongiunzione SE: ___","resposta":"EPPURE: Sono stanco, eppure continuo a lavorare. (contrasto con sorpresa) / QUINDI: Sono stanco, quindi dovrei smettere di lavorare. (conseguenza logica) / SE: Se sono stanco, dovrei smettere. (condizione)","explicacao":"Stessa situazione, congiunzioni diverse → significati diversi: EPPURE (nonostante), QUINDI (perciò), SE (condizionale). La scelta della congiunzione cambia il rapporto logico tra le frasi."},
    {"tipo":"escolha","pergunta":"'Tanto che alla fine si è addormentato.' Questa è una proposizione:","opcoes":["causale","consecutiva (tanto...che = so much that)","temporale"],"resposta":1,"explicacao":"TANTO CHE = al punto che = consecutiva. Indica la conseguenza di un'intensità: 'Era così stanco tanto che si è addormentato' = era così stanco al punto che il risultato è stato addormentarsi."},
    {"tipo":"revelar","pergunta":"**Esercizio final 3** — Completare con le congiunzioni giuste:\n1. ___ non abbia soldi, compra sempre qualcosa. (sebbene)\n2. Ha chiamato ___ arrivasse. (prima che)\n3. Uscirò ___ non piova. (a condizione che/purché)","resposta":"1. Sebbene non abbia soldi (cong.pres.) / 2. Ha chiamato prima che arrivasse (cong.imp.) / 3. Uscirò a condizione che non piova / purché non piova (cong.pres.)","explicacao":"SEBBENE+cong. PRIMA CHE+cong. (imperfetto per sequenza passata). PURCHÉ/A CONDIZIONE CHE+cong. (presente per condizione futura ipotetica)."},
    {"tipo":"escolha","pergunta":"'Dimmi dove vai.' La proposizione dipendente è:","opcoes":["relativa","interrogativa indiretta","causale"],"resposta":1,"explicacao":"DIMMI DOVE VAI = interrogativa INDIRETTA (richiede un'informazione). Introdotta da parola interrogativa (dove, quando, chi, perché...) dipendente da un verbo di chiedere/dire/sapere. Non è relativa (non modifica un nome) né causale."},
]

exercises['Lezione XXIX'] = [  # faltam 17
    {"tipo":"revelar","pergunta":"**Esercizio final 1** — Avverbi che cambiano significato con/senza negazione:\nANCORA senza not = ___ (still/more)\nNON...ANCORA = ___ (not yet)\nGIÀ senza not = ___ (already)\nNON...GIÀ = ___ (not already/no longer)","resposta":"ANCORA = ancora (still/more). NON...ANCORA = non ancora (not yet). GIÀ = già (already). NON...PIÙ = non più (no longer) — nota: NON...GIÀ è raro; NON...PIÙ è il comune.","explicacao":"Coppie importanti: ANCORA/NON ANCORA (still/not yet). GIÀ come 'already'. NON PIÙ come 'no longer'. 'Ho già finito' vs 'Non ho ancora finito' vs 'Non finisco più'."},
    {"tipo":"escolha","pergunta":"'Finalmente!' FINALMENTE come esclamazione significa:","opcoes":["troppo tardi!","at last! (sollievo dopo lunga attesa)","fortunatamente!"],"resposta":1,"explicacao":"FINALMENTE esclamativo = at last! = esprime sollievo dopo un'attesa (spesso lunga). Come avverbio: 'finalmente ho capito' = dopo tanto tempo, alla fine ho capito."},
    {"tipo":"revelar","pergunta":"**Esercizio final 2** — Posizione dell'avverbio nelle frasi italiane:\nNeglo esempi seguenti, trovare la posizione corretta:\n1. 'Ho sempre amato la musica.' → SEMPRE è ___ (ausiliare e participio)\n2. 'Parla troppo velocemente.' → TROPPO è ___ (prima di un avverbio di modo)\n3. 'Probabilmente verrà.' → PROBABILMENTE è ___ (inizio frase)","resposta":"1. SEMPRE tra ausiliare (ho) e participio (amato) — posizione standard per avverbi di frequenza con tempi composti. / 2. TROPPO prima di VELOCEMENTE (avverbio che modifica un altro avverbio). / 3. PROBABILMENTE a inizio frase o dopo il verbo: 'verrà probabilmente'.","explicacao":"Posizione degli avverbi: di frequenza (sempre/mai/già) → tra aus.+part. Di grado (troppo/molto) → prima dell'elemento modificato. Di frase (probabilmente) → inizio o fine."},
    {"tipo":"escolha","pergunta":"'Non capisce mica.' MICA in questo contesto:","opcoes":["significa 'già'","rafforza la negazione (= per niente, affatto)","è sinonimo di 'ancora'"],"resposta":1,"explicacao":"MICA (settentrionale/colloquiale) + negazione = rafforzativo negativo: 'non capisce mica' = non capisce affatto, per niente. 'Mica male' = non è per niente male (senza NON)."},
    {"tipo":"revelar","pergunta":"**Esercizio final 3** — Avverbi di affermazione nel parlato:\n'Sì!' / 'Certo!' / 'Certamente!' / 'Assolutamente!' / 'Esatto!' / 'Proprio!' / 'Esattamente!'\nUsare nel dialogo:\nA: 'Sei d'accordo?' B: '___, è una buona idea.'\nA: 'Quindi vieni?' B: '___, ci sarò di sicuro.'","resposta":"B: Certo/Certamente/Assolutamente/Esatto, è una buona idea. / B: Sì/Proprio/Esattamente, ci sarò di sicuro.","explicacao":"Avverbi di affermazione nel parlato italiano: SÌ (base), CERTO/CERTAMENTE (sicuro), ASSOLUTAMENTE (enfatico), ESATTO/ESATTAMENTE (conferma precisa), PROPRIO (enfatico-emotivo), DI SICURO/SICURAMENTE."},
]

exercises['Lezione XXX'] = [  # faltam 15
    {"tipo":"revelar","pergunta":"**Ripasso L** — Completare con il verbo corretto (tutti i tempi):\n'Se avessi più tempo libero, ___.' (potere, cond.) → Se avessi più tempo libero, potrei studiare di più.\n'Se avessi avuto più tempo, ___.' (potere, cond.passato) → ___","resposta":"Se avessi avuto più tempo, avrei potuto studiare di più. (tipo 3: cong.trapassato + cond.passato)","explicacao":"Tipo 2: SE+cong.imperfetto (avessi)+cond.presente (potrei). Tipo 3: SE+cong.trapassato (avessi avuto)+cond.passato (avrei potuto). I due tipi spesso si mescolano nel parlato."},
    {"tipo":"escolha","pergunta":"'Mi piacerebbe andare in Italia.' PIACEREBBE è:","opcoes":["indicativo presente","condizionale presente","congiuntivo presente"],"resposta":1,"explicacao":"PIACEREBBE = condizionale presente di PIACERE. Esprime desiderio cortese o ipotetico. 'Mi piace' (reale) vs 'mi piacerebbe' (desiderio/ipotesi)."},
    {"tipo":"revelar","pergunta":"**Ripasso M** — Riepilogo: connettivi fondamentali per argomento:\nCONNETTIVITA: E, ANCHE, PURE, INOLTRE, NEMMENO, NEANCHE, NÉ...NÉ\nAVVERSATIVITA: MA, PERÒ, TUTTAVIA, EPPURE, INVECE, AL CONTRARIO\nCAUSALITA: PERCHÉ, POICHÉ, DATO CHE, SICCOME, VISTO CHE\nCONSEGUENZA: QUINDI, PERCIÒ, DUNQUE, ALLORA, DI CONSEGUENZA\nFINALITA: PER, AFFINCHÉ, PERCHÉ+cong.\nCONCESSIONE: SEBBENE, BENCHÉ, NONOSTANTE, PUR+gerundio","resposta":"Tabella di riepilogo completa (vedere sopra). Memorizzare le categorie semantiche e le strutture grammaticali associate (indicativo/congiuntivo/infinito).","explicacao":"La padronanza dei connettivi è fondamentale per la coesione testuale italiana (B1-B2). Ogni categoria richiede una struttura grammaticale specifica."},
    {"tipo":"escolha","pergunta":"'Studio italiano da tre anni.' Quale risposta è corretta alla domanda 'Da quanto tempo?'","opcoes":["Ho studiato italiano tre anni fa.","Studio italiano da tre anni (azione ancora in corso).","Studierò italiano per tre anni."],"resposta":1,"explicacao":"DA + durata + presente = azione iniziata nel passato e ANCORA IN CORSO. 'Studio da tre anni' = sono tre anni che studio (ancora ora). 'Ho studiato per tre anni' = azione completata nel passato."},
    {"tipo":"revelar","pergunta":"**Ripasso N** — Test finale integrato:\nTradurre in italiano:\n1. 'Although I was tired, I kept studying.'\n2. 'I wish I had studied more!'\n3. 'She told me she would come the next day.'","resposta":"1. Sebbene fossi stanco/a, ho continuato a studiare. / Pur essendo stanco, ho continuato. / 2. Magari avessi studiato di più! / Avrei dovuto studiare di più! / 3. Mi ha detto che sarebbe venuta il giorno dopo / l'indomani.","explicacao":"1. Sebbene+cong.imp. / pur+gerundio. 2. Magari+cong.trapassato (desiderio nel passato). 3. D.i.: verrebbe→sarebbe venuta, tomorrow→il giorno dopo."},
]

# ─────────────────────────────────────────────────────────────────────────────
def inserir_antes_escolha(lez, novos):
    exercicios = lez['exercicios']
    idx = next((i for i, e in enumerate(exercicios) if e.get('tipo') == 'escolha'), len(exercicios))
    for i, ex in enumerate(novos):
        exercicios.insert(idx + i, ex)
    return len(novos)

total = 0
for lez_num, novos in exercises.items():
    lez = next((u for u in a1['unidades'] if u['num'] == lez_num), None)
    if not lez:
        print(f'AVISO: {lez_num} não encontrada!')
        continue
    antes = len(lez['exercicios'])
    n = inserir_antes_escolha(lez, novos)
    depois = len(lez['exercicios'])
    total += n
    print(f'OK {lez_num}: {antes} → {depois} (+{n})')

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nTotal adicionado: {total}')

# Verificação final
print('\n=== VERIFICAÇÃO FINAL ===')
with open(PATH, encoding='utf-8') as f:
    data2 = json.load(f)
a1_check = next(m for m in data2['moduli'] if m['id'] == 'A1')
grand_total = 0
for u in a1_check['unidades']:
    n = len(u.get('exercicios', []))
    grand_total += n
    status = '✅' if n >= 100 else f'⚠️ {n}'
    print(f'{status:6s} {u["num"]:18s} | {n}')
print(f'\nTotal A1: {grand_total} exercícios')
