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

# ----------------- TEMPLO 4 (Napoli: Comida, Restaurante) -----------------
# Needs 37 words
t4_data = load(4)
t4_words = t4_data.get("palavras", t4_data.get("vocabulario", []))
start_idx = len(t4_words) + 1

t4_new = [
    gen_word(f"t4_{start_idx+0:03}", "cucchiaio", "colher", "cibo", "Prendo il brodo con il cucchiaio.", "Tomo o caldo com a colher.", "/kukˈkjajo/", "m", "cucchiai"),
    gen_word(f"t4_{start_idx+1:03}", "forchetta", "garfo", "cibo", "Mangio gli spaghetti con la forchetta.", "Como o espaguete com o garfo.", "/forˈketta/", "f", "forchette"),
    gen_word(f"t4_{start_idx+2:03}", "coltello", "faca", "cibo", "Taglia la carne con il coltello.", "Corte a carne com a faca.", "/kolˈtɛllo/", "m", "coltelli"),
    gen_word(f"t4_{start_idx+3:03}", "piatto", "prato", "cibo", "Il piatto è vuoto.", "O prato está vazio.", "/ˈpjatto/", "m", "piatti"),
    gen_word(f"t4_{start_idx+4:03}", "bicchiere", "copo", "cibo", "Voglio un bicchiere d'acqua.", "Quero um copo de água.", "/bikˈkjɛːre/", "m", "bicchieri"),
    gen_word(f"t4_{start_idx+5:03}", "tovagliolo", "guardanapo", "cibo", "Può portarmi un tovagliolo?", "Pode me trazer um guardanapo?", "/tovaʎˈʎɔːlo/", "m", "tovaglioli"),
    gen_word(f"t4_{start_idx+6:03}", "tovaglia", "toalha de mesa", "cibo", "La tovaglia è sporca.", "A toalha de mesa está suja.", "/toˈvaʎʎa/", "f", "tovaglie"),
    gen_word(f"t4_{start_idx+7:03}", "menu", "cardápio", "ristorante", "Posso vedere il menu?", "Posso ver o cardápio?", "/meˈnu/", "m", "menu"),
    gen_word(f"t4_{start_idx+8:03}", "conto", "conta", "ristorante", "Il conto, per favore.", "A conta, por favor.", "/ˈkonto/", "m", "conti"),
    gen_word(f"t4_{start_idx+9:03}", "mancia", "gorjeta", "ristorante", "Lasciamo una mancia al cameriere.", "Vamos deixar uma gorjeta para o garçom.", "/ˈmantʃa/", "f", "mance"),
    gen_word(f"t4_{start_idx+10:03}", "cameriere", "garçom", "ristorante", "Il cameriere ci porta il vino.", "O garçom nos traz o vinho.", "/kameˈrjɛːre/", "m", "camerieri"),
    gen_word(f"t4_{start_idx+11:03}", "cameriera", "garçonete", "ristorante", "La cameriera è molto gentile.", "A garçonete é muito gentil.", "/kameˈrjɛːra/", "f", "cameriere"),
    gen_word(f"t4_{start_idx+12:03}", "antipasto", "entrada (comida)", "ristorante", "Prendiamo un antipasto misto.", "Vamos pedir uma entrada mista.", "/antiˈpasto/", "m", "antipasti"),
    gen_word(f"t4_{start_idx+13:03}", "primo", "primeiro prato", "ristorante", "Come primo voglio la pasta.", "Como primeiro prato, quero a massa.", "/ˈpriːmo/", "m", "primi"),
    gen_word(f"t4_{start_idx+14:03}", "secondo", "segundo prato", "ristorante", "Per secondo preferisco il pesce.", "Para o segundo prato prefiro peixe.", "/seˈkondo/", "m", "secondi"),
    gen_word(f"t4_{start_idx+15:03}", "contorno", "acompanhamento", "ristorante", "Un'insalata come contorno.", "Uma salada como acompanhamento.", "/konˈtorno/", "m", "contorni"),
    gen_word(f"t4_{start_idx+16:03}", "dolce", "sobremesa / doce", "ristorante", "Hai spazio per il dolce?", "Tem espaço para a sobremesa?", "/ˈdoltʃe/", "m", "dolci"),
    gen_word(f"t4_{start_idx+17:03}", "amaro", "amargo / licor digestivo", "ristorante", "Un caffè e un amaro.", "Um café e um licor digestivo.", "/aˈmaːro/", "m", "amari"),
    gen_word(f"t4_{start_idx+18:03}", "piccante", "apimentado", "cibo", "Questa salsa è molto piccante.", "Este molho é muito apimentado.", "/pikˈkante/", "m/f", "piccanti"),
    gen_word(f"t4_{start_idx+19:03}", "salato", "salgado", "cibo", "La zuppa è troppo salata.", "A sopa está muito salgada.", "/saˈlaːto/", "m", "salati"),
    gen_word(f"t4_{start_idx+20:03}", "cucina", "cozinha", "casa", "La cucina italiana è famosa.", "A cozinha italiana é famosa.", "/kuˈtʃiːna/", "f", "cucine"),
    gen_word(f"t4_{start_idx+21:03}", "forno", "forno", "casa", "La pizza cuoce nel forno.", "A pizza assa no forno.", "/ˈforno/", "m", "forni"),
    gen_word(f"t4_{start_idx+22:03}", "frigorifero", "geladeira", "casa", "Metti il latte nel frigorifero.", "Coloque o leite na geladeira.", "/friɡoˈriːfero/", "m", "frigoriferi"),
    gen_word(f"t4_{start_idx+23:03}", "padella", "frigideira", "casa", "Frigge l'uovo in padella.", "Ele frita o ovo na frigideira.", "/paˈdɛlla/", "f", "padelle"),
    gen_word(f"t4_{start_idx+24:03}", "pentola", "panela", "casa", "L'acqua bolle nella pentola.", "A água ferve na panela.", "/ˈpɛntola/", "f", "pentole"),
    gen_word(f"t4_{start_idx+25:03}", "aglio", "alho", "cibo", "Uno spicchio d'aglio.", "Um dente de alho.", "/ˈaʎʎo/", "m", "agli"),
    gen_word(f"t4_{start_idx+26:03}", "cipolla", "cebola", "cibo", "Taglio la cipolla per il sugo.", "Corto a cebola para o molho.", "/tʃiˈpolla/", "f", "cipolle"),
    gen_word(f"t4_{start_idx+27:03}", "pepe", "pimenta-do-reino", "cibo", "Aggiungi un po' di sale e pepe.", "Adicione um pouco de sal e pimenta.", "/ˈpeːpe/", "m", "pepi"),
    gen_word(f"t4_{start_idx+28:03}", "succo", "suco", "cibo", "Un succo d'arancia.", "Um suco de laranja.", "/ˈsukko/", "m", "succhi"),
    gen_word(f"t4_{start_idx+29:03}", "torta", "torta / bolo", "cibo", "Una fetta di torta al cioccolato.", "Uma fatia de bolo de chocolate.", "/ˈtorta/", "f", "torte"),
    gen_word(f"t4_{start_idx+30:03}", "gelato", "sorvete", "cibo", "Voglio un gelato al limone.", "Quero um sorvete de limão.", "/dʒeˈlaːto/", "m", "gelati"),
    gen_word(f"t4_{start_idx+31:03}", "biscotto", "biscoito", "cibo", "I biscotti per la colazione.", "Os biscoitos para o café da manhã.", "/bisˈkɔtto/", "m", "biscotti"),
    gen_word(f"t4_{start_idx+32:03}", "formaggio", "queijo", "cibo", "Il formaggio parmigiano.", "O queijo parmesão.", "/forˈmaddʒo/", "m", "formaggi"),
    gen_word(f"t4_{start_idx+33:03}", "prosciutto", "presunto", "cibo", "Un panino col prosciutto crudo.", "Um sanduíche com presunto cru.", "/proʃˈʃutto/", "m", "prosciutti"),
    gen_word(f"t4_{start_idx+34:03}", "pomodoro", "tomate", "cibo", "Insalata con pomodoro e mozzarella.", "Salada com tomate e muçarela.", "/pomoˈdɔːro/", "m", "pomodori"),
    gen_word(f"t4_{start_idx+35:03}", "patata", "batata", "cibo", "Le patate fritte sono buone.", "As batatas fritas são boas.", "/paˈtaːta/", "f", "patate"),
    gen_word(f"t4_{start_idx+36:03}", "fungho", "cogumelo", "cibo", "Pizza ai funghi.", "Pizza de cogumelos.", "/ˈfunɡo/", "m", "funghi")
]

t4_words.extend(t4_new)
t4_data["palavras"] = t4_words[:107]
save(4, t4_data)
print(f"T4 salvo con {len(t4_data['palavras'])} palavras.")


# ----------------- TEMPLO 5 (Milano: Tempo, Rotina, Trabalho) -----------------
# Needs 42 words
t5_data = load(5)
t5_words = t5_data.get("palavras", t5_data.get("vocabulario", []))
start_idx = len(t5_words) + 1

t5_new = [
    gen_word(f"t5_{start_idx+0:03}", "secondo", "segundo", "tempo", "Aspetta un secondo.", "Espere um segundo.", "/seˈkondo/", "m", "secondi"),
    gen_word(f"t5_{start_idx+1:03}", "minuto", "minuto", "tempo", "Torno tra cinque minuti.", "Volto em cinco minutos.", "/miˈnuːto/", "m", "minuti"),
    gen_word(f"t5_{start_idx+2:03}", "orologio", "relógio", "tempo", "Guardo l'orologio.", "Olho para o relógio.", "/oroˈlɔːdʒo/", "m", "orologi"),
    gen_word(f"t5_{start_idx+3:03}", "sveglia", "despertador", "rotina", "La sveglia suona presto.", "O despertador toca cedo.", "/ˈzveʎʎa/", "f", "sveglie"),
    gen_word(f"t5_{start_idx+4:03}", "calendario", "calendário", "tempo", "Segno la data sul calendario.", "Marco a data no calendário.", "/kalenˈdaːrjo/", "m", "calendari"),
    gen_word(f"t5_{start_idx+5:03}", "appuntamento", "compromisso / encontro", "lavoro", "Ho un appuntamento dal dentista.", "Tenho um compromisso no dentista.", "/appuntaˈmento/", "m", "appuntamenti"),
    gen_word(f"t5_{start_idx+6:03}", "agenda", "agenda", "lavoro", "Scrivo tutto sull'agenda.", "Escrevo tudo na agenda.", "/aˈdʒɛnda/", "f", "agende"),
    gen_word(f"t5_{start_idx+7:03}", "riunione", "reunião", "lavoro", "La riunione dura due ore.", "A reunião dura duas horas.", "/ri.uˈnjoːne/", "f", "riunioni"),
    gen_word(f"t5_{start_idx+8:03}", "ufficio", "escritório", "lavoro", "Lavoro in ufficio.", "Trabalho no escritório.", "/ufˈfiːtʃo/", "m", "uffici"),
    gen_word(f"t5_{start_idx+9:03}", "capo", "chefe", "lavoro", "Il mio capo è severo.", "Meu chefe é rigoroso.", "/ˈkaːpo/", "m", "capi"),
    gen_word(f"t5_{start_idx+10:03}", "collega", "colega", "lavoro", "Un bravo collega ti aiuta.", "Um bom colega te ajuda.", "/kolˈlɛːɡa/", "m/f", "colleghi"),
    gen_word(f"t5_{start_idx+11:03}", "stipendio", "salário", "lavoro", "Lo stipendio arriva a fine mese.", "O salário chega no fim do mês.", "/stiˈpɛndjo/", "m", "stipendi"),
    gen_word(f"t5_{start_idx+12:03}", "lavoro", "trabalho", "lavoro", "Vado al lavoro.", "Vou para o trabalho.", "/laˈvoːro/", "m", "lavori"),
    gen_word(f"t5_{start_idx+13:03}", "azienda", "empresa", "lavoro", "Un'azienda internazionale.", "Uma empresa internacional.", "/adˈdzjɛnda/", "f", "aziende"),
    gen_word(f"t5_{start_idx+14:03}", "carriera", "carreira", "lavoro", "Ha fatto una bella carriera.", "Fez uma bela carreira.", "/karˈrjɛːra/", "f", "carriere"),
    gen_word(f"t5_{start_idx+15:03}", "alba", "aurora / amanhecer", "tempo", "Ci svegliamo all'alba.", "Acordamos ao amanhecer.", "/ˈalba/", "f", "albe"),
    gen_word(f"t5_{start_idx+16:03}", "tramonto", "pôr do sol", "tempo", "Guardare il tramonto al mare.", "Assistir ao pôr do sol no mar.", "/traˈmonto/", "m", "tramonti"),
    gen_word(f"t5_{start_idx+17:03}", "mattino", "manhã", "tempo", "Di mattino bevo il caffè.", "De manhã eu bebo café.", "/matˈtiːno/", "m", "mattini"),
    gen_word(f"t5_{start_idx+18:03}", "pomeriggio", "tarde", "tempo", "Ci vediamo nel pomeriggio.", "Nos vemos à tarde.", "/pomeˈriddʒo/", "m", "pomeriggi"),
    gen_word(f"t5_{start_idx+19:03}", "sera", "noite (início)", "tempo", "La sera guardo la TV.", "À noite assisto à TV.", "/ˈseːra/", "f", "sere"),
    gen_word(f"t5_{start_idx+20:03}", "notte", "noite (tarde)", "tempo", "Buona notte!", "Boa noite!", "/ˈnɔtte/", "f", "notti"),
    gen_word(f"t5_{start_idx+21:03}", "oggi", "hoje", "tempo", "Oggi piove.", "Hoje chove.", "/ˈɔddʒi/", None, None),
    gen_word(f"t5_{start_idx+22:03}", "ieri", "ontem", "tempo", "Ieri sono andato al cinema.", "Ontem fui ao cinema.", "/ˈjɛːri/", None, None),
    gen_word(f"t5_{start_idx+23:03}", "domani", "amanhã", "tempo", "Domani lavoro tutto il giorno.", "Amanhã trabalho o dia todo.", "/doˈmaːni/", None, None),
    gen_word(f"t5_{start_idx+24:03}", "presto", "cedo / rápido", "tempo", "Devo alzarmi presto.", "Preciso acordar cedo.", "/ˈprɛsto/", None, None),
    gen_word(f"t5_{start_idx+25:03}", "tardi", "tarde (adv)", "tempo", "È troppo tardi.", "É tarde demais.", "/ˈtardi/", None, None),
    gen_word(f"t5_{start_idx+26:03}", "subito", "imediatamente / logo", "tempo", "Arrivo subito.", "Chego logo.", "/ˈsuːbito/", None, None),
    gen_word(f"t5_{start_idx+27:03}", "adesso", "agora", "tempo", "Vieni qui adesso.", "Venha aqui agora.", "/aˈdɛsso/", None, None),
    gen_word(f"t5_{start_idx+28:03}", "mai", "nunca", "tempo", "Non bevo mai alcol.", "Nunca bebo álcool.", "/ˈmai/", None, None),
    gen_word(f"t5_{start_idx+29:03}", "sempre", "sempre", "tempo", "Lui è sempre in ritardo.", "Ele está sempre atrasado.", "/ˈsɛmpre/", None, None),
    gen_word(f"t5_{start_idx+30:03}", "spesso", "frequentemente", "tempo", "Vado spesso in palestra.", "Vou frequentemente à academia.", "/ˈspesso/", None, None),
    gen_word(f"t5_{start_idx+31:03}", "qualche volta", "às vezes", "tempo", "Qualche volta leggo un libro.", "Às vezes leio um livro.", "/ˈkwalke ˈvɔlta/", None, None),
    gen_word(f"t5_{start_idx+32:03}", "quotidiano", "diário", "rotina", "La mia routine quotidiana.", "Minha rotina diária.", "/kwotiˈdjaːno/", "m", "quotidiani"),
    gen_word(f"t5_{start_idx+33:03}", "settimana", "semana", "tempo", "Lavoro cinque giorni a settimana.", "Trabalho cinco dias na semana.", "/settiˈmaːna/", "f", "settimane"),
    gen_word(f"t5_{start_idx+34:03}", "mese", "mês", "tempo", "Il mese prossimo vado in vacanza.", "Mês que vem vou de férias.", "/ˈmeːze/", "m", "mesi"),
    gen_word(f"t5_{start_idx+35:03}", "anno", "ano", "tempo", "Buon anno nuovo!", "Feliz ano novo!", "/ˈanno/", "m", "anni"),
    gen_word(f"t5_{start_idx+36:03}", "secolo", "século", "tempo", "Il ventesimo secolo.", "O século vinte.", "/ˈsɛːkolo/", "m", "secoli"),
    gen_word(f"t5_{start_idx+37:03}", "finesettimana", "fim de semana", "tempo", "Cosa fai nel finesettimana?", "O que você faz no fim de semana?", "/finesettiˈmaːna/", "m", "finesettimana"),
    gen_word(f"t5_{start_idx+38:03}", "giorno", "dia", "tempo", "Oggi è un bel giorno.", "Hoje é um belo dia.", "/ˈdʒorno/", "m", "giorni"),
    gen_word(f"t5_{start_idx+39:03}", "pausa", "pausa / intervalo", "rotina", "Facciamo una pausa caffè.", "Vamos fazer um intervalo para o café.", "/ˈpawza/", "f", "pause"),
    gen_word(f"t5_{start_idx+40:03}", "abitudine", "hábito", "rotina", "È una buona abitudine.", "É um bom hábito.", "/abiˈtuːdine/", "f", "abitudini"),
    gen_word(f"t5_{start_idx+41:03}", "stanco", "cansado", "rotina", "Dopo il lavoro sono stanco.", "Depois do trabalho fico cansado.", "/ˈstaŋko/", "m", "stanchi")
]

t5_words.extend(t5_new)
t5_data["palavras"] = t5_words[:107]
save(5, t5_data)
print(f"T5 salvo con {len(t5_data['palavras'])} palavras.")
