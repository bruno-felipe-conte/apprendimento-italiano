import json
import os

def load(templo_num):
    path = f'data/templo-{templo_num}.json'
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save(templo_num, data):
    path = f'data/templo-{templo_num}.json'
    if "vocabulario" in data:
        data["palavras"] = data.pop("vocabulario")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def gen_word(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {
        "id": tid, "italiano": it, "portugues": pt, "genero": gen, "plural": pl,
        "exemplo": ex_it, "exemplo_pt": ex_pt, "categoria": cat, "dificuldade": "medio", "audio_ipa": ipa
    }

# ----------------- TEMPLO 2 (Venezia: Familia, Casa, Personalidade) -----------------
# Needs 32 words (T2 has 75, target 107)
# Let's add extended family, household objects, and more emotions.
t2_data = load(2)
t2_words = t2_data.get("palavras", t2_data.get("vocabulario", []))
start_idx = len(t2_words) + 1

t2_new = [
    gen_word(f"t2_{start_idx+0:03}", "cugino", "primo", "familia", "Mio cugino vive a Roma.", "Meu primo mora em Roma.", "/kuˈdʒiːno/", "m", "cugini"),
    gen_word(f"t2_{start_idx+1:03}", "cugina", "prima", "familia", "Mia cugina è molto simpatica.", "Minha prima é muito simpática.", "/kuˈdʒiːna/", "f", "cugine"),
    gen_word(f"t2_{start_idx+2:03}", "nipote", "sobrinho(a) / neto(a)", "familia", "Il nonno gioca con suo nipote.", "O avô brinca com seu neto.", "/niˈpoːte/", "m/f", "nipoti"),
    gen_word(f"t2_{start_idx+3:03}", "suocero", "sogro", "familia", "Mio suocero cucina benissimo.", "Meu sogro cozinha muito bem.", "/ˈswɔːtʃero/", "m", "suoceri"),
    gen_word(f"t2_{start_idx+4:03}", "suocera", "sogra", "familia", "Vado d'accordo con mia suocera.", "Me dou bem com minha sogra.", "/ˈswɔːtʃera/", "f", "suocere"),
    gen_word(f"t2_{start_idx+5:03}", "cognato", "cunhado", "familia", "Mio cognato lavora in banca.", "Meu cunhado trabalha no banco.", "/koɲˈɲaːto/", "m", "cognati"),
    gen_word(f"t2_{start_idx+6:03}", "cognata", "cunhada", "familia", "Mia cognata aspetta un bambino.", "Minha cunhada espera um bebê.", "/koɲˈɲaːta/", "f", "cognate"),
    gen_word(f"t2_{start_idx+7:03}", "genero", "genro", "familia", "Il genero di Marco è medico.", "O genro do Marco é médico.", "/ˈdʒɛnero/", "m", "generi"),
    gen_word(f"t2_{start_idx+8:03}", "nuora", "nora", "familia", "La mia nuora è straniera.", "Minha nora é estrangeira.", "/ˈnwɔːra/", "f", "nuore"),
    gen_word(f"t2_{start_idx+9:03}", "parente", "parente", "familia", "Abbiamo molti parenti in Italia.", "Temos muitos parentes na Itália.", "/paˈrɛnte/", "m/f", "parenti"),
    
    gen_word(f"t2_{start_idx+10:03}", "soffitto", "teto", "casa", "Il soffitto della stanza è alto.", "O teto do quarto é alto.", "/sofˈfitto/", "m", "soffitti"),
    gen_word(f"t2_{start_idx+11:03}", "pavimento", "chão / piso", "casa", "Ho pulito il pavimento stamattina.", "Limpei o chão hoje de manhã.", "/paviˈmento/", "m", "pavimenti"),
    gen_word(f"t2_{start_idx+12:03}", "parete", "parede", "casa", "La parete è dipinta di bianco.", "A parede está pintada de branco.", "/paˈreːte/", "f", "pareti"),
    gen_word(f"t2_{start_idx+13:03}", "balcone", "sacada", "casa", "Mi piace leggere sul balcone.", "Gosto de ler na sacada.", "/balˈkoːne/", "m", "balconi"),
    gen_word(f"t2_{start_idx+14:03}", "tetto", "telhado", "casa", "Il gatto cammina sul tetto.", "O gato anda pelo telhado.", "/ˈtetto/", "m", "tetti"),
    gen_word(f"t2_{start_idx+15:03}", "corridoio", "corredor", "casa", "La prima porta nel corridoio.", "A primeira porta no corredor.", "/korriˈdoːjo/", "m", "corridoi"),
    gen_word(f"t2_{start_idx+16:03}", "scala", "escada", "casa", "Faccio la scala a piedi.", "Subo a escada a pé.", "/ˈskaːla/", "f", "scale"),
    gen_word(f"t2_{start_idx+17:03}", "cantina", "porão / adega", "casa", "Teniamo il vino in cantina.", "Guardamos o vinho no porão.", "/kanˈtiːna/", "f", "cantine"),
    gen_word(f"t2_{start_idx+18:03}", "soffitta", "sótão", "casa", "La soffitta è piena di vecchie cose.", "O sótão está cheio de coisas velhas.", "/sofˈfitta/", "f", "soffitte"),
    
    gen_word(f"t2_{start_idx+19:03}", "stupido", "estúpido / burro", "personalidade", "È stato un errore stupido.", "Foi um erro estúpido.", "/ˈstuːpido/", "m", "stupidi"),
    gen_word(f"t2_{start_idx+20:03}", "intelligente", "inteligente", "personalidade", "Quella ragazza è molto intelligente.", "Aquela garota é muito inteligente.", "/intelliˈdʒɛnte/", "m/f", "intelligenti"),
    gen_word(f"t2_{start_idx+21:03}", "coraggioso", "corajoso", "personalidade", "Il pompiere è stato coraggioso.", "O bombeiro foi corajoso.", "/koradˈdʒoːzo/", "m", "coraggiosi"),
    gen_word(f"t2_{start_idx+22:03}", "timido", "tímido", "personalidade", "Il bambino è ancora molto timido.", "O menino ainda é muito tímido.", "/ˈtiːmido/", "m", "timidi"),
    gen_word(f"t2_{start_idx+23:03}", "pigro", "preguiçoso", "personalidade", "Mio fratello è un po' pigro.", "Meu irmão é um pouco preguiçoso.", "/ˈpiːɡro/", "m", "pigri"),
    gen_word(f"t2_{start_idx+24:03}", "attivo", "ativo", "personalidade", "Lei è una persona molto attiva.", "Ela é uma pessoa muito ativa.", "/atˈtiːvo/", "m", "attivi"),
    gen_word(f"t2_{start_idx+25:03}", "educato", "educado", "personalidade", "Un giovane molto educato.", "Um jovem muito educado.", "/eduˈkaːto/", "m", "educati"),
    gen_word(f"t2_{start_idx+26:03}", "maleducato", "mal-educado", "personalidade", "Non sopporto le persone maleducate.", "Não suporto pessoas mal-educadas.", "/maleduˈkaːto/", "m", "maleducati"),
    
    gen_word(f"t2_{start_idx+27:03}", "ridere", "rir", "verbos_emocao", "Mi fa sempre ridere.", "Ele sempre me faz rir.", "/ˈriːdere/", None, None),
    gen_word(f"t2_{start_idx+28:03}", "piangere", "chorar", "verbos_emocao", "Il film mi ha fatto piangere.", "O filme me fez chorar.", "/ˈpjandʒere/", None, None),
    gen_word(f"t2_{start_idx+29:03}", "sorridere", "sorrir", "verbos_emocao", "Lei sorride sempre a tutti.", "Ela sempre sorri para todos.", "/sorˈriːdere/", None, None),
    gen_word(f"t2_{start_idx+30:03}", "sperare", "esperar (ter esperança)", "verbos_emocao", "Spero che vada tutto bene.", "Espero que tudo dê certo.", "/speˈraːre/", None, None),
    gen_word(f"t2_{start_idx+31:03}", "odiare", "odiar", "verbos_emocao", "Non odio nessuno.", "Não odeio ninguém.", "/oˈdjaːre/", None, None)
]

t2_words.extend(t2_new)
t2_data["palavras"] = t2_words[:107]
save(2, t2_data)
print(f"T2 salvo com {len(t2_data['palavras'])} palavras.")

# ----------------- TEMPLO 3 (Firenze: Viagem, Hotel, Direções) -----------------
# Needs 37 words (T3 has 70, target 107)
t3_data = load(3)
t3_words = t3_data.get("palavras", t3_data.get("vocabulario", []))
start_idx = len(t3_words) + 1

t3_new = [
    gen_word(f"t3_{start_idx+0:03}", "bagaglio", "bagagem", "viaggio", "Ho un bagaglio a mano.", "Tenho uma bagagem de mão.", "/baˈɡaʎʎo/", "m", "bagagli"),
    gen_word(f"t3_{start_idx+1:03}", "valigia", "mala", "viaggio", "Devo preparare la mia valigia.", "Preciso arrumar minha mala.", "/vaˈliːdʒa/", "f", "valigie"),
    gen_word(f"t3_{start_idx+2:03}", "zaino", "mochila", "viaggio", "Lo zaino è molto pesante.", "A mochila está muito pesada.", "/ˈdzajno/", "m", "zaini"),
    gen_word(f"t3_{start_idx+3:03}", "passaporto", "passaporte", "viaggio", "Il mio passaporto è scaduto.", "Meu passaporte venceu.", "/passaˈpɔrto/", "m", "passaporti"),
    gen_word(f"t3_{start_idx+4:03}", "biglietto", "passagem / bilhete", "viaggio", "Ho comprato il biglietto online.", "Comprei a passagem online.", "/biʎˈʎetto/", "m", "biglietti"),
    gen_word(f"t3_{start_idx+5:03}", "prenotazione", "reserva", "viaggio", "Ho una prenotazione a nome Rossi.", "Tenho uma reserva em nome de Rossi.", "/prenotatˈtsjoːne/", "f", "prenotazioni"),
    gen_word(f"t3_{start_idx+6:03}", "volo", "voo", "viaggio", "Il volo per Roma parte alle dieci.", "O voo para Roma sai às dez.", "/ˈvoːlo/", "m", "voli"),
    gen_word(f"t3_{start_idx+7:03}", "partenza", "partida", "viaggio", "Siamo in ritardo per la partenza.", "Estamos atrasados para a partida.", "/parˈtɛntsa/", "f", "partenze"),
    gen_word(f"t3_{start_idx+8:03}", "arrivo", "chegada", "viaggio", "Il mio arrivo è previsto alle due.", "Minha chegada está prevista para as duas.", "/arˈriːvo/", "m", "arrivi"),
    gen_word(f"t3_{start_idx+9:03}", "ritardo", "atraso", "viaggio", "Il treno ha un ritardo di venti minuti.", "O trem tem um atraso de vinte minutos.", "/riˈtardo/", "m", "ritardi"),
    gen_word(f"t3_{start_idx+10:03}", "binario", "plataforma / trilho", "stazione", "Il treno parte dal binario quattro.", "O trem parte da plataforma quatro.", "/biˈnaːrjo/", "m", "binari"),
    gen_word(f"t3_{start_idx+11:03}", "stazione", "estação", "stazione", "Andiamo alla stazione centrale.", "Vamos para a estação central.", "/statˈtsjoːne/", "f", "stazioni"),
    gen_word(f"t3_{start_idx+12:03}", "aeroporto", "aeroporto", "viaggio", "L'aeroporto è fuori città.", "O aeroporto fica fora da cidade.", "/aeroˈpɔrto/", "m", "aeroporti"),
    gen_word(f"t3_{start_idx+13:03}", "passeggero", "passageiro", "viaggio", "Ogni passeggero deve mostrare il biglietto.", "Cada passageiro deve mostrar a passagem.", "/passedˈdʒɛːro/", "m", "passeggeri"),
    gen_word(f"t3_{start_idx+14:03}", "b&b", "pousada (bed & breakfast)", "hotel", "Dormiamo in un piccolo B&B.", "Vamos dormir numa pequena pousada.", "/bi e bi/", "m", "b&b"),
    gen_word(f"t3_{start_idx+15:03}", "camera doppia", "quarto duplo", "hotel", "Vorrei una camera doppia con bagno.", "Gostaria de um quarto duplo com banheiro.", "/ˈkaːmera ˈdoppja/", "f", "camere doppie"),
    gen_word(f"t3_{start_idx+16:03}", "camera singola", "quarto de solteiro", "hotel", "Ho prenotato una camera singola.", "Reservei um quarto de solteiro.", "/ˈkaːmera ˈsinɡola/", "f", "camere singole"),
    gen_word(f"t3_{start_idx+17:03}", "chiave", "chave", "hotel", "Ecco la chiave della sua camera.", "Aqui está a chave do seu quarto.", "/ˈkjaːve/", "f", "chiavi"),
    gen_word(f"t3_{start_idx+18:03}", "reception", "recepção", "hotel", "Chiedi informazioni alla reception.", "Peça informações na recepção.", "/riˈsɛpʃon/", "f", "reception"),
    gen_word(f"t3_{start_idx+19:03}", "ascensore", "elevador", "hotel", "L'ascensore è guasto.", "O elevador está quebrado.", "/aʃʃenˈsoːre/", "m", "ascensori"),
    gen_word(f"t3_{start_idx+20:03}", "scale", "escadas", "hotel", "Andiamo per le scale.", "Vamos pelas escadas.", "/ˈskaːle/", "f", "scale"),
    gen_word(f"t3_{start_idx+21:03}", "Nord", "Norte", "direzioni", "Milano è nel nord dell'Italia.", "Milão fica no norte da Itália.", "/nɔrd/", "m", None),
    gen_word(f"t3_{start_idx+22:03}", "Sud", "Sul", "direzioni", "Napoli è nel sud dell'Italia.", "Nápoles fica no sul da Itália.", "/sud/", "m", None),
    gen_word(f"t3_{start_idx+23:03}", "Est", "Leste", "direzioni", "Il sole sorge a est.", "O sol nasce a leste.", "/ɛst/", "m", None),
    gen_word(f"t3_{start_idx+24:03}", "Ovest", "Oeste", "direzioni", "Il sole tramonta a ovest.", "O sol se põe a oeste.", "/ˈɔːvest/", "m", None),
    gen_word(f"t3_{start_idx+25:03}", "diritto", "reto (em frente)", "direzioni", "Vai sempre diritto.", "Vá sempre reto.", "/diˈritto/", "m", None),
    gen_word(f"t3_{start_idx+26:03}", "girare", "virar", "direzioni", "Devi girare a destra al semaforo.", "Você deve virar à direita no semáforo.", "/dʒiˈraːre/", None, None),
    gen_word(f"t3_{start_idx+27:03}", "destra", "direita", "direzioni", "La farmacia è sulla destra.", "A farmácia fica à direita.", "/ˈdɛstra/", "f", "destre"),
    gen_word(f"t3_{start_idx+28:03}", "sinistra", "esquerda", "direzioni", "Gira a sinistra dopo la banca.", "Vire à esquerda depois do banco.", "/siˈnistra/", "f", "sinistre"),
    gen_word(f"t3_{start_idx+29:03}", "incrocio", "cruzamento", "direzioni", "Fermati all'incrocio.", "Pare no cruzamento.", "/inˈkroːtʃo/", "m", "incroci"),
    gen_word(f"t3_{start_idx+30:03}", "semaforo", "semáforo / farol", "direzioni", "Il semaforo è rosso.", "O semáforo está vermelho.", "/seˈmaːforo/", "m", "semafori"),
    gen_word(f"t3_{start_idx+31:03}", "piazza", "praça", "direzioni", "Ci vediamo in piazza.", "Nos vemos na praça.", "/ˈpjattsa/", "f", "piazze"),
    gen_word(f"t3_{start_idx+32:03}", "via", "rua / via", "direzioni", "Abito in Via Roma.", "Moro na Via Roma.", "/ˈviːa/", "f", "vie"),
    gen_word(f"t3_{start_idx+33:03}", "strada", "estrada / rua", "direzioni", "Questa strada è molto lunga.", "Esta estrada é muito longa.", "/ˈstraːda/", "f", "strade"),
    gen_word(f"t3_{start_idx+34:03}", "ponte", "ponte", "direzioni", "Dobbiamo attraversare il ponte.", "Temos que atravessar a ponte.", "/ˈponte/", "m", "ponti"),
    gen_word(f"t3_{start_idx+35:03}", "mappa", "mapa", "viaggio", "Hai una mappa della città?", "Você tem um mapa da cidade?", "/ˈmappa/", "f", "mappe"),
    gen_word(f"t3_{start_idx+36:03}", "guida", "guia", "viaggio", "La nostra guida turistica è molto brava.", "Nosso guia turístico é muito bom.", "/ˈɡwiːda/", "f", "guide")
]

t3_words.extend(t3_new)
t3_data["palavras"] = t3_words[:107]
save(3, t3_data)
print(f"T3 salvo con {len(t3_data['palavras'])} palavras.")
