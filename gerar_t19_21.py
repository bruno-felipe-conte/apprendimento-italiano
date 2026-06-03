#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def w(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {
        "id": tid, "italiano": it, "portugues": pt, "genero": gen, "plural": pl,
        "exemplo": ex_it, "exemplo_pt": ex_pt, "categoria": cat, "dificuldade": "medio", "audio_ipa": ipa
    }

t19_data = [
    # Mezzi di trasporto
    ("aereo", "avião", "mezzi", "Prendo l'aereo per Roma.", "Pego o avião para Roma.", "/aˈɛreo/", "m", "aerei"),
    ("treno", "trem", "mezzi", "Il treno parte in orario.", "O trem parte no horário.", "/ˈtrɛno/", "m", "treni"),
    ("autobus", "ônibus", "mezzi", "L'autobus è sempre pieno.", "O ônibus está sempre cheio.", "/ˈautobus/", "m", "autobus"),
    ("macchina", "carro", "mezzi", "Ho comprato una macchina nuova.", "Comprei um carro novo.", "/ˈmakkina/", "f", "macchine"),
    ("bicicletta", "bicicleta", "mezzi", "Vado in bicicletta al parco.", "Vou de bicicleta ao parque.", "/bitʃiˈkletta/", "f", "biciclette"),
    ("moto", "moto", "mezzi", "La mia moto è molto veloce.", "Minha moto é muito rápida.", "/ˈmɔto/", "f", "moto"),
    ("barca", "barco", "mezzi", "Facciamo un giro in barca.", "Vamos dar um passeio de barco.", "/ˈbarka/", "f", "barche"),
    ("nave", "navio", "mezzi", "La nave è nel porto.", "O navio está no porto.", "/ˈnave/", "f", "navi"),
    ("traghetto", "balsa", "mezzi", "Il traghetto collega le isole.", "A balsa liga as ilhas.", "/traˈɡetto/", "m", "traghetti"),
    ("metropolitana", "metrô", "mezzi", "La metropolitana è rapida.", "O metrô é rápido.", "/metropoliˈtana/", "f", "metropolitane"),
    ("tram", "bonde", "mezzi", "Il tram passa per il centro.", "O bonde passa pelo centro.", "/tram/", "m", "tram"),
    ("elicottero", "helicóptero", "mezzi", "L'elicottero vola in alto.", "O helicóptero voa alto.", "/eliˈkɔttero/", "m", "elicotteri"),
    ("furgone", "furgão", "mezzi", "Uso il furgone per lavorare.", "Uso o furgão para trabalhar.", "/furˈɡone/", "m", "furgoni"),
    ("camion", "caminhão", "mezzi", "Il camion trasporta merci.", "O caminhão transporta mercadorie.", "/ˈkamjon/", "m", "camion"),
    ("taxi", "táxi", "mezzi", "Chiamo un taxi per l'hotel.", "Chamo um táxi para o hotel.", "/ˈtaksi/", "m", "taxi"),
    ("scooter", "scooter", "mezzi", "Lo scooter è comodo in città.", "A scooter é cômoda na cidade.", "/ˈskuter/", "m", "scooter"),
    ("funivia", "teleférico", "mezzi", "Prendiamo la funivia per la montagna.", "Pegamos o teleférico para a montanha.", "/funiˈvia/", "f", "funivie"),
    
    # Infrastrutture e Luoghi
    ("stazione", "estação", "infrastrutture", "La stazione ferroviaria è vicina.", "A estação ferroviária é perto.", "/statˈtsjone/", "f", "stazioni"),
    ("aeroporto", "aeroporto", "infrastrutture", "L'aeroporto è fuori città.", "O aeroporto fica fora da cidade.", "/aeroˈpɔrto/", "m", "aeroporti"),
    ("porto", "porto", "infrastrutture", "Le navi arrivano al porto.", "Os navios chegam ao porto.", "/ˈpɔrto/", "m", "porti"),
    ("fermata", "parada", "infrastrutture", "Scendo alla prossima fermata.", "Desço na próxima parada.", "/ferˈmata/", "f", "fermate"),
    ("binario", "plataforma/trilho", "infrastrutture", "Il treno parte dal binario due.", "O trem parte da plataforma dois.", "/biˈnarjo/", "m", "binari"),
    ("autostrada", "rodovia", "infrastrutture", "Guidiamo sull'autostrada.", "Dirigimos na rodovia.", "/autoˈstrada/", "f", "autostrade"),
    ("strada", "rua/estrada", "infrastrutture", "La strada è chiusa.", "A rua está fechada.", "/ˈstrada/", "f", "strade"),
    ("incrocio", "cruzamento", "infrastrutture", "Gira a destra all'incrocio.", "Vire à direita no cruzamento.", "/inˈkrotʃo/", "m", "incroci"),
    ("semaforo", "semáforo", "infrastrutture", "Fermati al semaforo rosso.", "Pare no semáforo vermelho.", "/seˈmaforo/", "m", "semafori"),
    ("parcheggio", "estacionamento", "infrastrutture", "C'è un parcheggio gratuito.", "Há um estacionamento gratuito.", "/parˈkeddʒo/", "m", "parcheggi"),
    ("benzinaio", "posto de gasolina", "infrastrutture", "Devo fermarmi al benzinaio.", "Preciso parar no posto de gasolina.", "/bendziˈnajo/", "m", "benzinai"),
    ("biglietteria", "bilheteria", "infrastrutture", "La biglietteria è aperta.", "A bilheteria está aberta.", "/biʎʎetteˈria/", "f", "biglietterie"),
    ("casello", "pedágio", "infrastrutture", "Paga al casello autostradale.", "Pague no pedágio da rodovia.", "/kaˈzɛllo/", "m", "caselli"),
    ("pista", "pista", "infrastrutture", "L'aereo è sulla pista.", "O avião está na pista.", "/ˈpista/", "f", "piste"),
    ("banchina", "caís", "infrastrutture", "Aspettiamo sulla banchina.", "Esperamos no cais.", "/banˈkina/", "f", "banchine"),
    
    # Viaggio e Concetti
    ("biglietto", "bilhete/passagem", "viaggio", "Hai comprato il biglietto?", "Você comprou a passagem?", "/biʎˈʎetto/", "m", "biglietti"),
    ("passaporto", "passaporte", "viaggio", "Mostra il passaporto.", "Mostre o passaporte.", "/passaˈpɔrto/", "m", "passaporti"),
    ("valigia", "mala", "viaggio", "Ho preparato la valigia.", "Arrumei a mala.", "/vaˈlidʒa/", "f", "valigie"),
    ("bagaglio", "bagagem", "viaggio", "Il bagaglio a mano.", "A bagagem de mão.", "/baˈɡaʎʎo/", "m", "bagagli"),
    ("partenza", "partida", "viaggio", "L'orario di partenza è alle sei.", "O horário de partida é às seis.", "/parˈtɛntsa/", "f", "partenze"),
    ("arrivo", "chegada", "viaggio", "Siamo nella sala arrivi.", "Estamos na sala de chegadas.", "/arˈrivo/", "m", "arrivi"),
    ("ritardo", "atraso", "viaggio", "Il treno ha un forte ritardo.", "O trem tem um grande atraso.", "/riˈtardo/", "m", "ritardi"),
    ("coincidenza", "conexão", "viaggio", "Ho perso la coincidenza.", "Perdi a conexão.", "/kointʃiˈdɛntsa/", "f", "coincidenze"),
    ("orario", "horário", "viaggio", "Consulta l'orario dei treni.", "Consulte o horário dos trens.", "/oˈrarjo/", "m", "orari"),
    ("passeggero", "passageiro", "viaggio", "Ci sono molti passeggeri.", "Há muitos passageiros.", "/passeidˈdʒɛro/", "m", "passeggeri"),
    ("volo", "voo", "viaggio", "Il volo è stato cancellato.", "O voo foi cancelado.", "/ˈvolo/", "m", "voli"),
    ("crociera", "cruzeiro", "viaggio", "Una crociera nel Mediterraneo.", "Um cruzeiro no Mediterrâneo.", "/kroˈtʃɛra/", "f", "crociere"),
    ("viaggio", "viagem", "viaggio", "Buon viaggio a tutti!", "Boa viagem a todos!", "/ˈvjaddʒo/", "m", "viaggi"),
    ("destinazione", "destino", "viaggio", "Qual è la tua destinazione?", "Qual é o seu destino?", "/destinatˈtsjone/", "f", "destinazioni"),
    ("mappa", "mapa", "viaggio", "Guardo la mappa della città.", "Olho o mapa da cidade.", "/ˈmappa/", "f", "mappe"),
    ("rotta", "rota", "viaggio", "La nave ha cambiato rotta.", "O navio mudou de rota.", "/ˈrotta/", "f", "rotte"),
    ("dogana", "alfândega", "viaggio", "Controlli alla dogana.", "Controles na alfândega.", "/doˈɡana/", "f", "dogane"),
    ("frontiera", "fronteira", "viaggio", "Passiamo la frontiera oggi.", "Passamos a fronteira hoje.", "/fronˈtjɛra/", "f", "frontiere"),
    ("visto", "visto", "viaggio", "Serve il visto per entrare.", "É preciso visto para entrar.", "/ˈvisto/", "m", "visti"),
    ("turista", "turista", "viaggio", "La città è piena di turisti.", "A cidade está cheia de turistas.", "/tuˈrista/", "m", "turisti"),
    ("guida", "guia", "viaggio", "Abbiamo una guida turistica.", "Temos um guia turístico.", "/ˈɡwida/", "f", "guide"),
    ("itinerario", "itinerário", "viaggio", "Questo è il nostro itinerario.", "Este é o nosso itinerário.", "/itineˈrarjo/", "m", "itinerari"),
    
    # Veicoli e Particolari
    ("motore", "motor", "veicoli", "Il motore è molto rumoroso.", "O motor é muito barulhento.", "/moˈtore/", "m", "motori"),
    ("ruota", "roda", "veicoli", "Ho forato una ruota.", "Furei uma roda.", "/ˈrwɔta/", "f", "ruote"),
    ("freno", "freio", "veicoli", "Il freno non funziona bene.", "O freio não funciona bem.", "/ˈfreno/", "m", "freni"),
    ("volante", "volante", "veicoli", "Tieni le mani sul volante.", "Mantenha as mãos no volante.", "/voˈlante/", "m", "volanti"),
    ("sedile", "assento", "veicoli", "Il sedile è molto comodo.", "O assento é muito confortável.", "/seˈdile/", "m", "sedili"),
    ("cintura", "cinto", "veicoli", "Metti la cintura di sicurezza.", "Coloque o cinto de segurança.", "/tʃinˈtura/", "f", "cinture"),
    ("targa", "placa", "veicoli", "Non ricordo la targa.", "Não lembro a placa.", "/ˈtarɡa/", "f", "targhe"),
    ("benzina", "gasolina", "veicoli", "Devo fare benzina.", "Preciso abastecer com gasolina.", "/benˈdzina/", "f", "benzine"),
    ("diesel", "diesel", "veicoli", "L'auto va a diesel.", "O carro funciona a diesel.", "/ˈdizel/", "m", "diesel"),
    ("carburante", "combustível", "veicoli", "Il prezzo del carburante.", "O preço do combustível.", "/karbuˈrante/", "m", "carburanti"),
    ("pedaggio", "pedágio", "veicoli", "Il pedaggio è caro.", "O pedágio é caro.", "/peˈdaddʒo/", "m", "pedaggi"),
    ("multa", "multa", "veicoli", "Ho preso una multa.", "Levei uma multa.", "/ˈmulta/", "f", "multe"),
    
    # Verbi
    ("viaggiare", "viajar", "verbi", "Amo viaggiare per il mondo.", "Amo viajar pelo mundo.", "/vjadˈdʒare/", None, None),
    ("partire", "partir", "verbi", "Domani partiamo per Napoli.", "Amanhã partimos para Nápoles.", "/parˈtire/", None, None),
    ("arrivare", "chegar", "verbi", "Siamo appena arrivati.", "Acabamos de chegar.", "/arriˈvare/", None, None),
    ("prendere", "pegar", "verbi", "Voglio prendere il treno.", "Quero pegar o trem.", "/ˈprɛndere/", None, None),
    ("guidare", "dirigir", "verbi", "So guidare la macchina.", "Sei dirigir o carro.", "/ɡwiˈdare/", None, None),
    ("volare", "voar", "verbi", "Gli uccelli amano volare.", "Os pássaros amam voar.", "/voˈlare/", None, None),
    ("navigare", "navegar", "verbi", "Navigare in mare aperto.", "Navegar em mar aberto.", "/naviˈɡare/", None, None),
    ("parcheggiare", "estacionar", "verbi", "Dove posso parcheggiare?", "Onde posso estacionar?", "/parkedˈdʒare/", None, None),
    ("prenotare", "reservar", "verbi", "Devo prenotare il volo.", "Preciso reservar o voo.", "/prenoˈtare/", None, None),
    ("annullare", "cancelar", "verbi", "Hanno dovuto annullare il viaggio.", "Tiveram que cancelar a viagem.", "/annulˈlare/", None, None),
    ("salire", "subir", "verbi", "Dobbiamo salire sull'autobus.", "Temos que subir no ônibus.", "/saˈlire/", None, None),
    ("scendere", "descer", "verbi", "Scendi alla prossima fermata.", "Desça na próxima parada.", "/ˈʃendere/", None, None),
    ("noleggiare", "alugar", "verbi", "Voglio noleggiare un'auto.", "Quero alugar um carro.", "/noledˈdʒare/", None, None),
    ("camminare", "caminhar", "verbi", "Camminare fa molto bene.", "Caminhar faz muito bem.", "/kammiˈnare/", None, None),
    ("attraversare", "atravessar", "verbi", "Attraversare la strada con cura.", "Atravessar a rua com cuidado.", "/attraverˈsare/", None, None),
    ("accelerare", "acelerar", "verbi", "Non devi accelerare qui.", "Você não deve acelerar aqui.", "/attʃeleˈrare/", None, None),
    ("frenare", "frear", "verbi", "Frenare all'improvviso è pericoloso.", "Frear de repente é perigoso.", "/freˈnare/", None, None),
    ("decollare", "decolar", "verbi", "L'aereo sta per decollare.", "O avião está prestes a decolar.", "/dekolˈlare/", None, None),
    ("atterrare", "aterrissar", "verbi", "Atterrare a Roma alle due.", "Aterrissar em Roma às duas.", "/atterˈrare/", None, None),
    ("esplorare", "explorar", "verbi", "Esplorare nuovi paesi.", "Explorar novos países.", "/esploˈrare/", None, None),
    
    # Aggettivi e Altro
    ("veloce", "rápido", "altro", "Il treno è molto veloce.", "O trem é muito rápido.", "/veˈlotʃe/", "m", "veloci"),
    ("lento", "lento", "altro", "Il traffico è lento oggi.", "O trânsito está lento hoje.", "/ˈlɛnto/", "m", "lenti"),
    ("lontano", "longe", "altro", "La stazione è lontana.", "A estação é longe.", "/lonˈtano/", "m", "lontani"),
    ("vicino", "perto", "altro", "L'aeroporto è vicino.", "O aeroporto é perto.", "/viˈtʃino/", "m", "vicini"),
    ("comodo", "cômodo", "altro", "Un sedile comodo.", "Um assento cômodo.", "/ˈkɔmodo/", "m", "comodi"),
    ("scomodo", "desconfortável", "altro", "Il viaggio è stato scomodo.", "A viagem foi desconfortável.", "/ˈskɔmodo/", "m", "scomodi"),
    ("diretto", "direto", "altro", "Ho un volo diretto.", "Tenho um voo direto.", "/diˈrɛtto/", "m", "diretti"),
    ("pubblico", "público", "altro", "Uso i mezzi pubblici.", "Uso o transporte público.", "/ˈpubbliko/", "m", "pubblici"),
    ("privato", "privado", "altro", "Un aereo privato.", "Um avião privado.", "/priˈvato/", "m", "privati"),
    ("estero", "estrangeiro", "altro", "Un viaggio all'estero.", "Uma viagem ao exterior.", "/ˈɛstero/", "m", "esteri"),
    ("nazionale", "nacional", "altro", "Un volo nazionale.", "Um voo nacional.", "/natsjoˈnale/", "m", "nazionali"),
    ("internazionale", "internacional", "altro", "L'aeroporto internazionale.", "O aeroporto internacional.", "/internatsjoˈnale/", "m", "internazionali"),
    ("turistico", "turístico", "altro", "Un villaggio turistico.", "Uma vila turística.", "/tuˈristiko/", "m", "turistici")
]

t20_data = [
    # Testa e Viso
    ("testa", "cabeça", "testa", "Mi fa male la testa.", "Minha cabeça está doendo.", "/ˈtɛsta/", "f", "teste"),
    ("occhio", "olho", "testa", "Ha un occhio azzurro e uno verde.", "Tem um olho azul e um verde.", "/ˈɔkkjo/", "m", "occhi"),
    ("orecchio", "orelha", "testa", "Ho un'infezione all'orecchio.", "Tenho uma infecção na orelha.", "/oˈrekkjo/", "m", "orecchi"),
    ("naso", "nariz", "testa", "Ha il naso chiuso.", "O nariz dele está entupido.", "/ˈnazo/", "m", "nasi"),
    ("bocca", "boca", "testa", "Apri la bocca.", "Abra a boca.", "/ˈbokka/", "f", "bocche"),
    ("labbro", "lábio", "testa", "Si è morso il labbro.", "Ele mordeu o lábio.", "/ˈlabbro/", "m", "labbra"),
    ("dente", "dente", "testa", "Devo lavare i denti.", "Tenho que escovar os dentes.", "/ˈdɛnte/", "m", "denti"),
    ("lingua", "língua", "testa", "Mostra la lingua al dottore.", "Mostre a língua para o médico.", "/ˈlinɡwa/", "f", "lingue"),
    ("capello", "cabelo", "testa", "Ha i capelli lunghi.", "Ela tem cabelos longos.", "/kaˈpello/", "m", "capelli"),
    ("fronte", "testa (frente)", "testa", "Ha la fronte alta.", "Tem a testa grande.", "/ˈfronte/", "f", "fronti"),
    ("guancia", "bochecha", "testa", "Ha una guancia rossa.", "Tem uma bochecha vermelha.", "/ˈɡwantʃa/", "f", "guance"),
    ("mento", "queixo", "testa", "Ha un mento pronunciato.", "Tem um queixo pronunciado.", "/ˈmento/", "m", "menti"),
    ("collo", "pescoço", "testa", "Mi fa male il collo.", "Meu pescoço dói.", "/ˈkɔllo/", "m", "colli"),
    ("gola", "garganta", "testa", "Ho mal di gola.", "Estou com dor de garganta.", "/ˈɡola/", "f", "gole"),
    ("ciglio", "cílio", "testa", "Le ciglia lunghe.", "Os cílios longos.", "/ˈtʃiʎʎo/", "m", "ciglia"),
    ("sopracciglio", "sobrancelha", "testa", "Alza un sopracciglio.", "Levanta uma sobrancelha.", "/sopratˈtʃiʎʎo/", "m", "sopracciglia"),
    ("viso", "rosto", "testa", "Ha un bel viso.", "Tem um rosto bonito.", "/ˈvizo/", "m", "visi"),
    ("faccia", "cara", "testa", "Lavarsi la faccia.", "Lavar a cara.", "/ˈfattʃa/", "f", "facce"),
    ("mascella", "mandíbula", "testa", "La mascella forte.", "A mandíbula forte.", "/maʃˈʃɛlla/", "f", "mascelle"),
    
    # Tronco
    ("spalla", "ombro", "tronco", "Ho un dolore alla spalla.", "Tenho uma dor no ombro.", "/ˈspalla/", "f", "spalle"),
    ("petto", "peito", "tronco", "Respira gonfiando il petto.", "Respire inflando o peito.", "/ˈpɛtto/", "m", "petti"),
    ("seno", "seio", "tronco", "Il cancro al seno.", "O câncer de mama.", "/ˈseno/", "m", "seni"),
    ("pancia", "barriga", "tronco", "Mi fa male la pancia.", "Minha barriga está doendo.", "/ˈpantʃa/", "f", "pance"),
    ("addome", "abdômen", "tronco", "Dolori all'addome.", "Dores no abdômen.", "/adˈdɔme/", "m", "addomi"),
    ("schiena", "costas", "tronco", "Ho mal di schiena.", "Tenho dor nas costas.", "/ˈskjɛna/", "f", "schiene"),
    ("fianco", "flanco/quadril", "tronco", "Dorme sul fianco destro.", "Dorme do lado direito.", "/ˈfjanko/", "m", "fianchi"),
    ("bacino", "pelve", "tronco", "Frattura del bacino.", "Fratura da pelve.", "/baˈtʃino/", "m", "bacini"),
    ("vita", "cintura", "tronco", "Ha una vita sottile.", "Tem uma cintura fina.", "/ˈvita/", "f", "vite"),
    
    # Arti Superiori
    ("braccio", "braço", "superiori", "Ha un braccio rotto.", "Tem um braço quebrado.", "/ˈbrattʃo/", "m", "braccia"),
    ("gomito", "cotovelo", "superiori", "Ho battuto il gomito.", "Bati o cotovelo.", "/ˈɡomito/", "m", "gomiti"),
    ("polso", "pulso", "superiori", "Misura il polso.", "Meça o pulso.", "/ˈpolso/", "m", "polsi"),
    ("mano", "mão", "superiori", "Dammi la mano.", "Me dê a mão.", "/ˈmano/", "f", "mani"),
    ("dito", "dedo", "superiori", "Mi sono tagliato un dito.", "Cortei um dedo.", "/ˈdito/", "m", "dita"),
    ("unghia", "unha", "superiori", "Si mangia le unghie.", "Ele rói as unhas.", "/ˈunɡja/", "f", "unghie"),
    ("pollice", "polegar", "superiori", "Il dito pollice.", "O dedo polegar.", "/ˈpɔllitʃe/", "m", "pollici"),
    
    # Arti Inferiori
    ("gamba", "perna", "inferiori", "Mi fa male la gamba.", "Minha perna dói.", "/ˈɡamba/", "f", "gambe"),
    ("ginocchio", "joelho", "inferiori", "Sbucciarsi un ginocchio.", "Ralar um joelho.", "/dʒiˈnɔkkjo/", "m", "ginocchia"),
    ("caviglia", "tornozelo", "inferiori", "Mi sono slogato la caviglia.", "Torci o tornozelo.", "/kaˈviʎʎa/", "f", "caviglie"),
    ("piede", "pé", "inferiori", "Ho i piedi freddi.", "Estou com os pés frios.", "/ˈpjɛde/", "m", "piedi"),
    ("tallone", "calcanhar", "inferiori", "Il tallone d'Achille.", "O calcanhar de Aquiles.", "/talˈlone/", "m", "talloni"),
    ("coscia", "coxa", "inferiori", "La coscia di pollo.", "A coxa de frango.", "/ˈkɔʃʃa/", "f", "cosce"),
    
    # Organi e Interni
    ("cuore", "coração", "interni", "Il cuore batte forte.", "O coração bate forte.", "/ˈkwɔre/", "m", "cuori"),
    ("polmone", "pulmão", "interni", "Respirare a pieni polmoni.", "Respirar a plenos pulmões.", "/polˈmone/", "m", "polmoni"),
    ("fegato", "fígado", "interni", "Il fegato filtra il sangue.", "O fígado filtra o sangue.", "/ˈfeɡato/", "m", "fegati"),
    ("rene", "rim", "interni", "Un calcolo al rene.", "Um cálculo no rim.", "/ˈrɛne/", "m", "reni"),
    ("cervello", "cérebro", "interni", "Usare il cervello.", "Usar o cérebro.", "/tʃerˈvɛllo/", "m", "cervelli"),
    ("stomaco", "estômago", "interni", "Ho lo stomaco vuoto.", "Estou com o estômago vazio.", "/ˈstɔmako/", "m", "stomachi"),
    ("intestino", "intestino", "interni", "L'intestino tenue.", "O intestino delgado.", "/intesˈtino/", "m", "intestini"),
    ("sangue", "sangue", "interni", "Donare il sangue.", "Doar sangue.", "/ˈsanɡwe/", "m", "sangui"),
    ("vena", "veia", "interni", "Il sangue nelle vene.", "O sangue nas veias.", "/ˈvena/", "f", "vene"),
    ("osso", "osso", "interni", "L'osso del braccio.", "O osso do braço.", "/ˈɔsso/", "m", "ossa"),
    ("muscolo", "músculo", "interni", "Avere i muscoli sviluppati.", "Ter músculos desenvolvidos.", "/ˈmuskolo/", "m", "muscoli"),
    ("nervo", "nervo", "interni", "Un nervo scoperto.", "Um nervo exposto.", "/ˈnɛrvo/", "m", "nervi"),
    ("pelle", "pele", "interni", "Avere una pelle liscia.", "Ter uma pele lisa.", "/ˈpɛlle/", "f", "pelli"),
    ("scheletro", "esqueleto", "interni", "Lo scheletro umano.", "O esqueleto humano.", "/ˈskɛletro/", "m", "scheletri"),
    ("saliva", "saliva", "interni", "Produrre molta saliva.", "Produzir muita saliva.", "/saˈliva/", "f", "salive"),
    ("sudore", "suor", "interni", "Asciugarsi il sudore.", "Enxugar o suor.", "/suˈdore/", "m", "sudori"),
    ("lacrima", "lágrima", "interni", "Piangere calde lacrime.", "Chorar lágrimas quentes.", "/ˈlakrima/", "f", "lacrime"),
    
    # Condizioni
    ("salute", "saúde", "condizioni", "La salute è importante.", "A saúde é importante.", "/saˈlute/", "f", "saluti"),
    ("malattia", "doença", "condizioni", "Una malattia rara.", "Uma doença rara.", "/malatˈtia/", "f", "malattie"),
    ("febbre", "febre", "condizioni", "Ho la febbre alta.", "Estou com febre alta.", "/ˈfɛbbre/", "f", "febbri"),
    ("tosse", "tosse", "condizioni", "Una brutta tosse.", "Uma tosse forte.", "/ˈtosse/", "f", "tossi"),
    ("dolore", "dor", "condizioni", "Provo un grande dolore.", "Sinto uma grande dor.", "/doˈlore/", "m", "dolori"),
    ("ferita", "ferida", "condizioni", "Pulire una ferita.", "Limpar uma ferida.", "/feˈrita/", "f", "ferite"),
    ("cicatrice", "cicatriz", "condizioni", "Una cicatrice sul braccio.", "Uma cicatriz no braço.", "/tʃikaˈtritʃe/", "f", "cicatrici"),
    ("respiro", "respiração", "condizioni", "Fare un respiro profondo.", "Fazer uma respiração profunda.", "/reˈspiro/", "m", "respiri"),
    ("allergia", "alergia", "condizioni", "Ho un'allergia ai gatti.", "Tenho alergia a gatos.", "/allerˈdʒia/", "f", "allergie"),
    ("sintomo", "sintoma", "condizioni", "Un sintomo influenzale.", "Um sintoma de gripe.", "/ˈsintomo/", "m", "sintomi"),
    
    # Verbi
    ("respirare", "respirar", "verbi", "Respirare aria pura.", "Respirar ar puro.", "/respiˈrare/", None, None),
    ("mangiare", "comer", "verbi", "Mangiare la pizza.", "Comer a pizza.", "/manˈdʒare/", None, None),
    ("bere", "beber", "verbi", "Bere molta acqua.", "Beber muita água.", "/ˈbere/", None, None),
    ("vedere", "ver", "verbi", "Non riesco a vedere bene.", "Não consigo ver bem.", "/veˈdere/", None, None),
    ("sentire", "ouvir/sentir", "verbi", "Sento un rumore.", "Ouço um barulho.", "/senˈtire/", None, None),
    ("ascoltare", "escutar", "verbi", "Ascoltare la musica.", "Escutar a música.", "/askolˈtare/", None, None),
    ("annusare", "cheirar", "verbi", "Annusare i fiori.", "Cheirar as flores.", "/annuˈzare/", None, None),
    ("toccare", "tocar", "verbi", "Non toccare il fuoco.", "Não toque no fogo.", "/tokˈkare/", None, None),
    ("camminare", "caminhar", "verbi", "Camminare per la strada.", "Caminhar pela rua.", "/kammiˈnare/", None, None),
    ("correre", "correr", "verbi", "Correre nel parco.", "Correr no parque.", "/ˈkorrere/", None, None),
    ("saltare", "pular", "verbi", "Saltare di gioia.", "Pular de alegria.", "/salˈtare/", None, None),
    ("dormire", "dormir", "verbi", "Dormire otto ore.", "Dormir oito horas.", "/dorˈmire/", None, None),
    ("sbadigliare", "bocejar", "verbi", "Sbadigliare per il sonno.", "Bocejar de sono.", "/zbadiˈʎʎare/", None, None),
    ("starnutire", "espirrar", "verbi", "Starnutire per la polvere.", "Espirrar por causa da poeira.", "/starnuˈtire/", None, None),
    ("tossire", "tossir", "verbi", "Tossire forte.", "Tossir forte.", "/tosˈsire/", None, None),
    ("sudare", "suar", "verbi", "Sudare per il caldo.", "Suar por causa do calor.", "/suˈdare/", None, None),
    ("sanguinare", "sangrar", "verbi", "Il dito comincia a sanguinare.", "O dedo começa a sangrar.", "/sanɡwiˈnare/", None, None),
    ("guarire", "curar", "verbi", "Guarire presto.", "Curar-se logo.", "/ɡwaˈrire/", None, None),
    ("ammalarsi", "ficar doente", "verbi", "Ammalarsi di influenza.", "Ficar doente com gripe.", "/ammaˈlarsi/", None, None),
    ("sorridere", "sorrir", "verbi", "Sorridere alla telecamera.", "Sorrir para a câmera.", "/sorˈridere/", None, None)
]

t21_data = [
    # Emozioni Positive
    ("gioia", "alegria", "positive", "Provo grande gioia.", "Sinto grande alegria.", "/ˈdʒɔja/", "f", "gioie"),
    ("felicità", "felicidade", "positive", "La felicità è importante.", "A felicidade é importante.", "/felitʃiˈta/", "f", "felicità"),
    ("amore", "amor", "positive", "L'amore vince sempre.", "O amor vence sempre.", "/aˈmore/", "m", "amori"),
    ("affetto", "afeto", "positive", "Provo affetto per te.", "Sinto afeto por você.", "/afˈfɛtto/", "m", "affetti"),
    ("simpatia", "simpatia", "positive", "Provo simpatia per lui.", "Sinto simpatia por ele.", "/simpaˈtia/", "f", "simpatie"),
    ("speranza", "esperança", "positive", "Non perdere la speranza.", "Não perca a esperança.", "/speˈrantsa/", "f", "speranze"),
    ("sorpresa", "surpresa", "positive", "Che bella sorpresa!", "Que bela surpresa!", "/sorˈpreza/", "f", "sorprese"),
    ("entusiasmo", "entusiasmo", "positive", "Lavora con entusiasmo.", "Trabalha com entusiasmo.", "/entuˈzjazmo/", "m", "entusiasmi"),
    ("orgoglio", "orgulho", "positive", "Mio figlio è il mio orgoglio.", "Meu filho é meu orgulho.", "/orˈɡoʎʎo/", "m", "orgogli"),
    ("calma", "calma", "positive", "Mantieni la calma.", "Mantenha a calma.", "/ˈkalma/", "f", "calme"),
    ("pace", "paz", "positive", "Vogliamo la pace nel mondo.", "Queremos paz no mundo.", "/ˈpatʃe/", "f", "paci"),
    ("serenità", "serenidade", "positive", "Vivere in serenità.", "Viver em serenidade.", "/sereniˈta/", "f", "serenità"),
    ("soddisfazione", "satisfação", "positive", "Una grande soddisfazione.", "Uma grande satisfação.", "/soddisfatˈtsjone/", "f", "soddisfazioni"),
    ("allegria", "alegria", "positive", "Festeggiare in allegria.", "Festejar com alegria.", "/alleˈɡria/", "f", "allegrie"),
    ("coraggio", "coragem", "positive", "Ci vuole coraggio.", "É preciso coraggio.", "/koˈraddʒo/", "m", "coraggi"),
    ("fiducia", "confiança", "positive", "Avere fiducia nel futuro.", "Ter confiança no futuro.", "/fiˈdutʃa/", "f", "fiducie"),
    ("gratitudine", "gratidão", "positive", "Esprimo la mia gratitudine.", "Expresso minha gratidão.", "/ɡratiˈtudine/", "f", "gratitudini"),
    ("passione", "paixão", "positive", "Canta con passione.", "Canta com paixão.", "/pasˈsjone/", "f", "passioni"),
    ("tenerezza", "ternura", "positive", "Mi fa molta tenerezza.", "Me dá muita ternura.", "/teneˈrettsa/", "f", "tenerezze"),
    ("sollievo", "alívio", "positive", "Un grande sospiro di sollievo.", "Um grande suspiro de alívio.", "/solˈljɛvo/", "m", "sollievi"),
    ("meraviglia", "maravilha", "positive", "Guarda con meraviglia.", "Olha com maravilha.", "/meraˈviʎʎa/", "f", "meraviglie"),
    
    # Emozioni Negative
    ("tristezza", "tristeza", "negative", "Sento un po' di tristezza.", "Sinto um pouco de tristeza.", "/trisˈtettsa/", "f", "tristezze"),
    ("paura", "medo", "negative", "Ho paura dei ragni.", "Tenho medo de aranhas.", "/paˈura/", "f", "paure"),
    ("rabbia", "raiva", "negative", "È accecato dalla rabbia.", "Ele está cego de raiva.", "/ˈrabbja/", "f", "rabbie"),
    ("odio", "ódio", "negative", "L'odio non risolve nulla.", "O ódio não resolve nada.", "/ˈɔdjo/", "m", "odi"),
    ("gelosia", "ciúme", "negative", "La gelosia è pericolosa.", "O ciúme é perigoso.", "/dʒeloˈzia/", "f", "gelosie"),
    ("invidia", "inveja", "negative", "L'invidia fa male.", "A inveja faz mal.", "/inˈvidja/", "f", "invidie"),
    ("noia", "tédio", "negative", "Che noia questo film!", "Que tédio esse filme!", "/ˈnɔja/", "f", "noie"),
    ("vergogna", "vergonha", "negative", "Provare vergogna per un errore.", "Sentir vergonha por um erro.", "/verˈɡoɲɲa/", "f", "vergogne"),
    ("colpa", "culpa", "negative", "Non è colpa mia.", "A culpa não é minha.", "/ˈkolpa/", "f", "colpe"),
    ("ansia", "ansiedade", "negative", "Soffre di ansia.", "Sofre de ansiedade.", "/ˈansja/", "f", "ansie"),
    ("stress", "estresse", "negative", "Lo stress da lavoro.", "O estresse do trabalho.", "/strɛs/", "m", "stress"),
    ("preoccupazione", "preocupação", "negative", "Ho una grande preoccupazione.", "Tenho uma grande preocupação.", "/preokkupatˈtsjone/", "f", "preoccupazioni"),
    ("delusione", "decepção", "negative", "Che grande delusione.", "Que grande decepção.", "/deluˈzjone/", "f", "delusioni"),
    ("disperazione", "desespero", "negative", "Piange di disperazione.", "Chora de desespero.", "/disperatˈtsjone/", "f", "disperazioni"),
    ("solitudine", "solidão", "negative", "La solitudine pesa molto.", "A solidão pesa muito.", "/soliˈtudine/", "f", "solitudini"),
    ("timore", "temor", "negative", "Avere timore di parlare.", "Ter temor de falar.", "/tiˈmore/", "m", "timori"),
    ("panico", "pânico", "negative", "Ha avuto un attacco di panico.", "Teve um ataque de pânico.", "/ˈpaniko/", "m", "panichi"),
    ("terrore", "terror", "negative", "Un film di terrore.", "Um filme de terror.", "/terˈrore/", "m", "terrori"),
    ("malinconia", "melancolia", "negative", "Una dolce malinconia.", "Uma doce melancolia.", "/malinkoˈnia/", "f", "malinconie"),
    ("nostalgia", "nostalgia", "negative", "Ho nostalgia di casa.", "Tenho nostalgia de casa.", "/nostalˈdʒia/", "f", "nostalgie"),
    ("rancore", "rancor", "negative", "Non porto rancore.", "Não guardo rancor.", "/ranˈkore/", "m", "rancori"),
    ("angoscia", "angústia", "negative", "Provare una profonda angoscia.", "Sentir uma profunda angústia.", "/anˈɡɔʃʃa/", "f", "angosce"),
    ("imbarazzo", "constrangimento", "negative", "Un momento di imbarazzo.", "Um momento de constrangimento.", "/imbaˈrattso/", "m", "imbarazzi"),
    ("pena", "pena", "negative", "Mi fa pena quel cane.", "Tenho pena daquele cachorro.", "/ˈpena/", "f", "pene"),
    
    # Aggettivi emotivi
    ("felice", "feliz", "aggettivi", "Sono molto felice.", "Estou muito feliz.", "/feˈlitʃe/", "m", "felici"),
    ("triste", "triste", "aggettivi", "Perché sei così triste?", "Por que você está tão triste?", "/ˈtriste/", "m", "tristi"),
    ("arrabbiato", "zangado", "aggettivi", "Lui è arrabbiato con me.", "Ele está zangado comigo.", "/arrabˈbjato/", "m", "arrabbiati"),
    ("spaventato", "assustado", "aggettivi", "Il bambino è spaventato.", "A criança está assustada.", "/spavenˈtato/", "m", "spaventati"),
    ("sorpreso", "surpreso", "aggettivi", "Sono sorpreso dalla notizia.", "Estou surpreso com a notícia.", "/sorˈprezo/", "m", "sorpresi"),
    ("annoiato", "entediado", "aggettivi", "Mi sento annoiato qui.", "Me sinto entediado aqui.", "/annojˈjato/", "m", "annoiati"),
    ("emozionato", "emocionado", "aggettivi", "Sono emozionato per stasera.", "Estou emocionado para esta noite.", "/emotsjoˈnato/", "m", "emozionati"),
    ("preoccupato", "preocupado", "aggettivi", "Non essere preoccupato.", "Não fique preocupado.", "/preokkuˈpato/", "m", "preoccupati"),
    ("deluso", "decepcionado", "aggettivi", "Sono rimasto deluso.", "Fiquei decepcionado.", "/deˈluzo/", "m", "delusi"),
    ("calmo", "calmo", "aggettivi", "Devi restare calmo.", "Você deve ficar calmo.", "/ˈkalmo/", "m", "calmi"),
    ("nervoso", "nervoso", "aggettivi", "Oggi mi sento nervoso.", "Hoje me sinto nervoso.", "/nerˈvozo/", "m", "nervosi"),
    ("innamorato", "apaixonato", "aggettivi", "Lui è innamorato di lei.", "Ele é apaixonado por ela.", "/innamoˈrato/", "m", "innamorati"),
    ("orgoglioso", "orgulhoso", "aggettivi", "Sono orgoglioso di te.", "Sou orgulhoso de você.", "/orɡoˈʎʎozo/", "m", "orgogliosi"),
    ("geloso", "ciumento", "aggettivi", "Un marito molto geloso.", "Um marido muito ciumento.", "/dʒeˈlozo/", "m", "gelosi"),
    ("sicuro", "seguro", "aggettivi", "Mi sento sicuro con te.", "Me sinto seguro com você.", "/siˈkuro/", "m", "sicuri"),
    ("insicuro", "inseguro", "aggettivi", "Un ragazzo molto insicuro.", "Um menino muito inseguro.", "/insiˈkuro/", "m", "insicuri"),
    
    # Verbi emotivi
    ("amare", "amar", "verbi", "Amo la mia famiglia.", "Amo a minha família.", "/aˈmare/", None, None),
    ("odiare", "odiar", "verbi", "Lui odia il freddo.", "Ele odeia o frio.", "/oˈdjare/", None, None),
    ("piangere", "chorar", "verbi", "Il bambino comincia a piangere.", "O bebê começa a chorar.", "/ˈpjandʒere/", None, None),
    ("ridere", "rir", "verbi", "Mi fai sempre ridere.", "Você me faz rir sempre.", "/ˈridere/", None, None),
    ("sorridere", "sorrir", "verbi", "Sorridi alla vita.", "Sorria para a vida.", "/sorˈridere/", None, None),
    ("arrabbiarsi", "irritar-se", "verbi", "Non arrabbiarti per nulla.", "Não se irrite por nada.", "/arrabˈbjarsi/", None, None),
    ("spaventarsi", "assustar-se", "verbi", "Facile spaventarsi al buio.", "Fácil assustar-se no escuro.", "/spavenˈtarsi/", None, None),
    ("gioire", "alegrar-se", "verbi", "Gioire del successo altrui.", "Alegrar-se com o sucesso alheio.", "/dʒoˈire/", None, None),
    ("sperare", "esperar", "verbi", "Spero che vada tutto bene.", "Espero que vá tudo bem.", "/speˈrare/", None, None),
    ("temere", "temer", "verbi", "Teme di sbagliare.", "Teme errar.", "/teˈmere/", None, None),
    ("soffrire", "sofrer", "verbi", "Soffre di mal di testa.", "Sofre de dor de cabeça.", "/sofˈfrire/", None, None),
    ("desiderare", "desejar", "verbi", "Desidero un caffè.", "Desejo um café.", "/dezideˈrare/", None, None),
    ("sognare", "sonhar", "verbi", "Sognare a occhi aperti.", "Sonhar de olhos abertos.", "/soɲˈɲare/", None, None),
    ("preoccuparsi", "preocupar-se", "verbi", "Non preoccuparti per me.", "Não se preocupe comigo.", "/preokkuˈparsi/", None, None),
    ("vergognarsi", "envergonhar-se", "verbi", "Si vergogna di parlare.", "Ele se envergonha de falar.", "/verɡoɲˈɲarsi/", None, None),
    ("calmarsi", "acalmar-se", "verbi", "Devi calmarti subito.", "Você deve se acalmar agora.", "/kalˈmarsi/", None, None),
    ("esprimere", "expressar", "verbi", "Esprimere i propri sentimenti.", "Expressar os próprios sentimentos.", "/esˈprimere/", None, None),
    ("sentire", "sentir", "verbi", "Sentire una forte emozione.", "Sentir uma forte emoção.", "/senˈtire/", None, None)
]

def salvar(templo_num, nome, citta, livello, palavras_raw):
    palavras = []
    for i, (it, pt, cat, ex_it, ex_pt, ipa, gen, pl) in enumerate(palavras_raw, 1):
        tid = f"t{templo_num}_{i:03d}"
        palavras.append(w(tid, it, pt, cat, ex_it, ex_pt, ipa, gen, pl))
        
    obj = {
        "templo": templo_num,
        "nome": nome,
        "cidade": citta,
        "nivel": livello,
        "palavras": palavras
    }
    
    path = os.path.join(OUT, "data", f"templo-{templo_num}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"OK templo-{templo_num}.json -- {len(palavras)} palavras")

if __name__ == "__main__":
    salvar(19, "I Trasporti e i Viaggi", "Venezia", "A2", t19_data)
    salvar(20, "Il Corpo Umano", "Bologna", "B1", t20_data)
    salvar(21, "Le Emozioni e i Sentimenti", "Siena", "B1", t21_data)
