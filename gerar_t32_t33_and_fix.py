import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def w(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {
        "id": tid, "italiano": it, "portugues": pt, "genero": gen, "plural": pl,
        "exemplo": ex_it, "exemplo_pt": ex_pt, "categoria": cat, "dificuldade": "medio", "audio_ipa": ipa
    }

t30_add = [
    ("pergamena", "pergaminho", "oggetti", "Un'antica pergamena.", "Um antigo pergaminho.", "/perɡaˈmɛna/", "f", "pergamene"),
    ("tomo", "tomo", "oggetti", "Il primo tomo dell'enciclopedia.", "O primeiro tomo da enciclopédia.", "/ˈtɔmo/", "m", "tomi"),
    ("trilogia", "trilogia", "generi", "Una famosa trilogia fantasy.", "Uma famosa trilogia de fantasia.", "/triloˈdʒia/", "f", "trilogie"),
    ("saga", "saga", "generi", "La saga familiare.", "A saga familiar.", "/ˈsaɡa/", "f", "saghe"),
    ("antologia", "antologia", "generi", "Un'antologia di poesie.", "Uma antologia de poesias.", "/antoloˈdʒia/", "f", "antologie"),
    ("bibliotecario", "bibliotecário", "persone", "Chiedi al bibliotecario.", "Pergunte ao bibliotecário.", "/bibljoteˈkarjo/", "m", "bibliotecari"),
    ("rilegare", "encadernar", "verbi", "Rilegare un vecchio libro.", "Encadernar um velho livro.", "/rileˈɡare/", None, None),
    ("impaginazione", "diagramação", "concetti", "L'impaginazione del testo.", "A diagramação do texto.", "/impadʒinatˈtsjone/", "f", "impaginazioni"),
    ("leggenda", "lenda", "generi", "Una vecchia leggenda.", "Uma velha lenda.", "/ledˈdʒɛnda/", "f", "leggende")
]

t31_add = [
    ("provetta", "tubo de ensaio", "strumenti", "Il sangue nella provetta.", "O sangue no tubo de ensaio.", "/proˈvetta/", "f", "provette"),
    ("siringa", "seringa", "strumenti", "Un'iniezione con la siringa.", "Uma injeção com a seringa.", "/siˈrinɡa/", "f", "siringhe"),
    ("stetoscopio", "estetoscópio", "strumenti", "Il dottore usa lo stetoscopio.", "O médico usa o estetoscópio.", "/stetosˈkɔpjo/", "m", "stetoscopi"),
    ("bisturi", "bisturi", "strumenti", "Il chirurgo prende il bisturi.", "O cirurgião pega o bisturi.", "/ˈbisturi/", "m", "bisturi"),
    ("genoma", "genoma", "elementi", "Mappare il genoma umano.", "Mapear o genoma humano.", "/dʒeˈnɔma/", "m", "genomi"),
    ("cromosoma", "cromossomo", "elementi", "Un cromosoma X.", "Um cromossomo X.", "/kromoˈzɔma/", "m", "cromosomi"),
    ("radiologia", "radiologia", "discipline", "Il reparto di radiologia.", "O departamento de radiologia.", "/radjoloˈdʒia/", "f", "radiologie"),
    ("ecografia", "ultrassom", "discipline", "Fare un'ecografia.", "Fazer um ultrassom.", "/ekoɡraˈfia/", "f", "ecografie"),
    ("diagnosi", "diagnóstico", "concetti", "Una diagnosi precoce.", "Um diagnóstico precoce.", "/diˈaɲɲozi/", "f", "diagnosi")
]

# T32: La Storia d'Italia (110 parole)
t32_data = [
    # Epoche
    ("storia", "história", "epoche", "La storia d'Italia è ricca.", "A história da Itália é rica.", "/ˈstɔrja/", "f", "storie"),
    ("antichità", "antiguidade", "epoche", "Un vaso dell'antichità.", "Um vaso da antiguidade.", "/antikiˈta/", "f", "antichità"),
    ("medioevo", "idade média", "epoche", "Nel buio medioevo.", "Na sombria idade média.", "/medjoˈɛvo/", "m", "medioevi"),
    ("rinascimento", "renascimento", "epoche", "Il rinascimento fiorentino.", "O renascimento florentino.", "/rinaʃʃiˈmento/", "m", "rinascimenti"),
    ("risorgimento", "ressurgimento", "epoche", "Il risorgimento italiano.", "O ressurgimento italiano.", "/rizordʒiˈmento/", "m", "risorgimenti"),
    ("novecento", "século XX", "epoche", "La storia del Novecento.", "A história do século XX.", "/noveˈtʃɛnto/", "m", "novecenti"),
    ("epoca", "época", "epoche", "In quell'epoca lontana.", "Naquela época distante.", "/ˈɛpoka/", "f", "epoche"),
    ("secolo", "século", "epoche", "Nel ventesimo secolo.", "No século vinte.", "/ˈsɛkolo/", "m", "secoli"),
    ("millennio", "milênio", "epoche", "Nel terzo millennio.", "No terceiro milênio.", "/milˈlɛnnjo/", "m", "millenni"),
    ("decennio", "década", "epoche", "Un decennio di pace.", "Uma década de paz.", "/deˈtʃɛnnjo/", "m", "decenni"),
    # Roma Antica
    ("impero", "império", "romani", "L'impero romano.", "O império romano.", "/imˈpɛro/", "m", "imperi"),
    ("repubblica", "república", "romani", "La repubblica romana.", "A república romana.", "/reˈpubblika/", "f", "repubbliche"),
    ("imperatore", "imperador", "romani", "L'imperatore Augusto.", "O imperador Augusto.", "/imperaˈtore/", "m", "imperatori"),
    ("gladiatore", "gladiador", "romani", "Il gladiatore nell'arena.", "O gladiador na arena.", "/ɡladjaˈtore/", "m", "gladiatori"),
    ("colosseo", "coliseu", "romani", "Il Colosseo a Roma.", "O Coliseu em Roma.", "/kolosˈsɛo/", "m", "colossei"),
    ("legione", "legião", "romani", "Una legione romana.", "Uma legião romana.", "/leˈdʒone/", "f", "legioni"),
    ("senato", "senado", "romani", "Il senato romano.", "O senado romano.", "/seˈnato/", "m", "senati"),
    ("barbaro", "bárbaro", "romani", "L'invasione dei barbari.", "A invasão dos bárbaros.", "/ˈbarbaro/", "m", "barbari"),
    ("acquedotto", "aqueduto", "romani", "Un antico acquedotto.", "Um antigo aqueduto.", "/akkweˈdotto/", "m", "acquedotti"),
    ("rovina", "ruína", "romani", "Le rovine di Pompei.", "As ruínas de Pompeia.", "/roˈvina/", "f", "rovine"),
    # Medioevo e Rinascimento
    ("castello", "castelo", "medioevo", "Un castello medievale.", "Um castelo medieval.", "/kasˈtɛllo/", "m", "castelli"),
    ("cavaliere", "cavaleiro", "medioevo", "Il cavaliere con l'armatura.", "O cavaleiro com a armadura.", "/kavaˈljɛre/", "m", "cavalieri"),
    ("re", "rei", "medioevo", "Il re d'Italia.", "O rei da Itália.", "/re/", "m", "re"),
    ("regina", "rainha", "medioevo", "La regina di Savoia.", "A rainha de Saboia.", "/reˈdʒina/", "f", "regine"),
    ("feudo", "feudo", "medioevo", "Un feudo medievale.", "Um feudo medieval.", "/ˈfɛudo/", "m", "feudi"),
    ("papa", "papa", "medioevo", "Il Papa a Roma.", "O Papa em Roma.", "/ˈpapa/", "m", "papi"),
    ("chiesa", "igreja", "medioevo", "La chiesa cattolica.", "A igreja católica.", "/ˈkjɛza/", "f", "chiese"),
    ("crociata", "cruzada", "medioevo", "La prima crociata.", "A primeira cruzada.", "/kroˈtʃata/", "f", "crociate"),
    ("ducato", "ducado", "rinascimento", "Il ducato di Milano.", "O ducado de Milão.", "/duˈkato/", "m", "ducati"),
    ("repubblica marinara", "república marítima", "rinascimento", "Venezia era una repubblica marinara.", "Veneza era uma república marítima.", "/reˈpubblika mariˈnara/", "f", "repubbliche marinare"),
    ("mercante", "mercador", "rinascimento", "Un ricco mercante.", "Um rico mercador.", "/merˈkante/", "m", "mercanti"),
    ("mecenate", "mecenas", "rinascimento", "I Medici come mecenati.", "Os Médici como mecenas.", "/metʃeˈnate/", "m", "mecenati"),
    ("scoperta", "descoberta", "rinascimento", "La scoperta dell'America.", "A descoberta da América.", "/skoˈpɛrta/", "f", "scoperte"),
    ("invenzione", "invenção", "rinascimento", "L'invenzione della stampa.", "A invenção da imprensa.", "/inventˈtsjone/", "f", "invenzioni"),
    ("artista", "artista", "rinascimento", "I grandi artisti italiani.", "Os grandes artistas italianos.", "/arˈtista/", "m/f", "artisti"),
    ("genio", "gênio", "rinascimento", "Il genio di Leonardo.", "O gênio de Leonardo.", "/ˈdʒɛnjo/", "m", "geni"),
    # Risorgimento ed Età Moderna
    ("patria", "pátria", "risorgimento", "L'amore per la patria.", "O amor pela pátria.", "/ˈpatrja/", "f", "patrie"),
    ("unificazione", "unificação", "risorgimento", "L'unificazione d'Italia.", "A unificação da Itália.", "/unifikatˈtsjone/", "f", "unificazioni"),
    ("eroe", "herói", "risorgimento", "Garibaldi è un eroe.", "Garibaldi é um herói.", "/eˈrɔe/", "m", "eroi"),
    ("bandiera", "bandeira", "risorgimento", "La bandiera tricolore.", "A bandeira tricolor.", "/banˈdjɛra/", "f", "bandiere"),
    ("inno", "hino", "risorgimento", "L'inno di Mameli.", "O hino de Mameli.", "/ˈinno/", "m", "inni"),
    ("costituzione", "constituição", "risorgimento", "La costituzione italiana.", "A constituição italiana.", "/kostitutˈtsjone/", "f", "costituzioni"),
    ("rivoluzione", "revolução", "risorgimento", "La rivoluzione industriale.", "A revolução industrial.", "/rivolutˈtsjone/", "f", "rivoluzioni"),
    ("indipendenza", "independência", "risorgimento", "La guerra d'indipendenza.", "A guerra de independência.", "/indipenˈdɛntsa/", "f", "indipendenze"),
    ("fascismo", "fascismo", "novecento", "Il periodo del fascismo.", "O período do fascismo.", "/faʃˈʃizmo/", "m", "fascismi"),
    ("dittatore", "ditador", "novecento", "Il dittatore Mussolini.", "O ditador Mussolini.", "/dittaˈtore/", "m", "dittatori"),
    ("guerra", "guerra", "novecento", "La seconda guerra mondiale.", "A segunda guerra mundial.", "/ˈɡwɛrra/", "f", "guerre"),
    ("pace", "paz", "novecento", "Un trattato di pace.", "Um tratado de paz.", "/ˈpatʃe/", "f", "paci"),
    ("partigiano", "partisan/guerrilheiro", "novecento", "La resistenza partigiana.", "A resistência partisan.", "/partiˈdʒano/", "m", "partigiani"),
    ("liberazione", "libertação", "novecento", "Il giorno della liberazione.", "O dia da libertação.", "/iberatˈtsjone/", "f", "liberazioni"),
    ("miracolo economico", "milagre econômico", "novecento", "Il miracolo economico italiano.", "O milagre econômico italiano.", "/miˈrakolo ekoˈnɔmiko/", "m", "miracoli economici"),
    ("terrorismo", "terrorismo", "novecento", "Gli anni del terrorismo.", "Os anos do terrorismo.", "/terrorˈizmo/", "m", "terrorismi"),
    ("strage", "massacre", "novecento", "Una strage di civili.", "Um massacre de civis.", "/ˈstradʒe/", "f", "stragi"),
    ("mafia", "máfia", "novecento", "La lotta alla mafia.", "A luta contra a máfia.", "/ˈmafja/", "f", "mafie"),
    ("magistrato", "magistrado", "novecento", "Un magistrato coraggioso.", "Um magistrado corajoso.", "/madʒisˈtrato/", "m", "magistrati"),
    ("repubblica", "república", "novecento", "La nascita della repubblica.", "O nascimento da república.", "/reˈpubblika/", "f", "repubbliche"),
    # Verbi e Aggettivi (20+20)
    ("fondare", "fundar", "verbi", "Fondare una città.", "Fundar uma cidade.", "/fonˈdare/", None, None),
    ("conquistare", "conquistar", "verbi", "Conquistare un territorio.", "Conquistar um território.", "/konkwisˈtare/", None, None),
    ("invadere", "invadir", "verbi", "Invadere il paese vicino.", "Invadir o país vizinho.", "/inˈvadere/", None, None),
    ("governare", "governar", "verbi", "Governare l'impero.", "Governar o império.", "/ɡoverˈnare/", None, None),
    ("sconfiggere", "derrotar", "verbi", "Sconfiggere il nemico.", "Derrotar o inimigo.", "/skonˈfiddʒere/", None, None),
    ("combattere", "combater", "verbi", "Combattere in guerra.", "Combater na guerra.", "/komˈbattere/", None, None),
    ("difendere", "defender", "verbi", "Difendere la patria.", "Defender a pátria.", "/diˈfɛndere/", None, None),
    ("unire", "unir", "verbi", "Unire l'Italia.", "Unir a Itália.", "/uˈnire/", None, None),
    ("ribellarsi", "rebelar-se", "verbi", "Ribellarsi al dittatore.", "Rebelar-se contra o ditador.", "/ribelˈlarsi/", None, None),
    ("liberare", "libertar", "verbi", "Liberare gli schiavi.", "Libertar os escravos.", "/libeˈrare/", None, None),
    ("firmare", "assinar", "verbi", "Firmare la pace.", "Assinar a paz.", "/firˈmare/", None, None),
    ("costruire", "construir", "verbi", "Costruire un monumento.", "Construir um monumento.", "/kostruˈire/", None, None),
    ("distruggere", "destruir", "verbi", "Distruggere la città.", "Destruir a cidade.", "/disˈtruddʒere/", None, None),
    ("ricostruire", "reconstruir", "verbi", "Ricostruire dopo il terremoto.", "Reconstruir após o terremoto.", "/rikostruˈire/", None, None),
    ("eleggere", "eleger", "verbi", "Eleggere il presidente.", "Eleger o presidente.", "/eˈlɛddʒere/", None, None),
    ("votare", "votar", "verbi", "Votare al referendum.", "Votar no referendo.", "/voˈtare/", None, None),
    ("emigrare", "emigrar", "verbi", "Emigrare all'estero.", "Emigrar para o exterior.", "/emiˈɡrare/", None, None),
    ("immigrare", "imigrar", "verbi", "Immigrare in cerca di lavoro.", "Imigrar em busca de trabalho.", "/immiˈɡrare/", None, None),
    ("scoprire", "descobrir", "verbi", "Scoprire nuove terre.", "Descobrir novas terras.", "/skoˈprire/", None, None),
    ("inventare", "inventar", "verbi", "Inventare la radio.", "Inventar o rádio.", "/invenˈtare/", None, None),
    ("antico", "antigo", "aggettivi", "Un antico vaso romano.", "Um antigo vaso romano.", "/anˈtiko/", "m", "antichi"),
    ("storico", "histórico", "aggettivi", "Un evento storico.", "Um evento histórico.", "/ˈstɔriko/", "m", "storici"),
    ("moderno", "moderno", "aggettivi", "Stato moderno.", "Estado moderno.", "/moˈdɛrno/", "m", "moderni"),
    ("contemporaneo", "contemporâneo", "aggettivi", "Storia contemporanea.", "História contemporânea.", "/kontempoˈranɛo/", "m", "contemporanei"),
    ("medievale", "medieval", "aggettivi", "Un borgo medievale.", "Um vilarejo medieval.", "/medjoˈvale/", "m", "medievali"),
    ("romano", "romano", "aggettivi", "L'esercito romano.", "O exército romano.", "/roˈmano/", "m", "romani"),
    ("italiano", "italiano", "aggettivi", "Il popolo italiano.", "O povo italiano.", "/itaˈljano/", "m", "italiani"),
    ("eroico", "heroico", "aggettivi", "Un atto eroico.", "Um ato heroico.", "/eˈrɔiko/", "m", "eroici"),
    ("glorioso", "glorioso", "aggettivi", "Un passato glorioso.", "Um passado glorioso.", "/ɡloˈrjozo/", "m", "gloriosi"),
    ("tragico", "trágico", "aggettivi", "Un evento tragico.", "Um evento trágico.", "/ˈtradʒiko/", "m", "tragici"),
    ("cruento", "cruento/sangrento", "aggettivi", "Una battaglia cruenta.", "Uma batalha sangrenta.", "/kruˈɛnto/", "m", "cruenti"),
    ("pacifico", "pacífico", "aggettivi", "Un periodo pacifico.", "Um período pacífico.", "/paˈtʃifiko/", "m", "pacifici"),
    ("coraggioso", "corajoso", "aggettivi", "Un soldato coraggioso.", "Um soldado corajoso.", "/koradˈdʒozo/", "m", "coraggiosi"),
    ("nazionale", "nacional", "aggettivi", "Festa nazionale.", "Feriado nacional.", "/natsjoˈnale/", "m", "nazionali"),
    ("unito", "unido", "aggettivi", "Un paese unito.", "Um país unido.", "/uˈnito/", "m", "uniti"),
    ("diviso", "dividido", "aggettivi", "Un paese diviso.", "Um país dividido.", "/diˈvizo/", "m", "divisi"),
    ("monumentale", "monumental", "aggettivi", "Un'opera monumentale.", "Uma obra monumental.", "/monumenˈtale/", "m", "monumentali"),
    ("archeologico", "arqueológico", "aggettivi", "Sito archeologico.", "Sítio arqueológico.", "/arkeoˈlɔdʒiko/", "m", "archeologici"),
    ("culturale", "cultural", "aggettivi", "Patrimonio culturale.", "Patrimônio cultural.", "/kultuˈrale/", "m", "culturali"),
    ("artistico", "artístico", "aggettivi", "Patrimonio artistico.", "Patrimônio artístico.", "/arˈtistiko/", "m", "artistici"),
    ("tradizionale", "tradicional", "aggettivi", "Festa tradizionale.", "Festa tradicional.", "/traditsjoˈnale/", "m", "tradizionali")
]

# T33: Il Turismo e i Musei (110 parole)
t33_data = [
    # Turismo base
    ("turismo", "turismo", "viaggio", "Il turismo in Italia.", "O turismo na Itália.", "/tuˈrizmo/", "m", "turismi"),
    ("turista", "turista", "viaggio", "Un turista giapponese.", "Um turista japonês.", "/tuˈrista/", "m/f", "turisti"),
    ("viaggio", "viagem", "viaggio", "Un lungo viaggio.", "Uma longa viagem.", "/ˈvjaddʒo/", "m", "viaggi"),
    ("vacanza", "férias", "viaggio", "Andare in vacanza.", "Ir de férias.", "/vaˈkantsa/", "f", "vacanze"),
    ("ferie", "férias (trabalho)", "viaggio", "Prendere le ferie.", "Tirar férias.", "/ˈfɛrje/", "f", "ferie"),
    ("destinazione", "destino", "viaggio", "Destinazione preferita.", "Destino preferido.", "/destinatˈtsjone/", "f", "destinazioni"),
    ("meta", "meta/destino", "viaggio", "Una meta turistica.", "Um destino turístico.", "/ˈmɛta/", "f", "mete"),
    ("itinerario", "itinerário", "viaggio", "L'itinerario del tour.", "O itinerário do tour.", "/itineˈrarjo/", "m", "itinerari"),
    ("guida", "guia", "viaggio", "Una guida turistica.", "Um guia turístico.", "/ˈɡwida/", "f", "guide"),
    ("mappa", "mapa", "viaggio", "Guardare la mappa.", "Olhar o mapa.", "/ˈmappa/", "f", "mappe"),
    ("cartina", "mapa (físico)", "viaggio", "Una cartina della città.", "Um mapa da cidade.", "/karˈtina/", "f", "cartine"),
    ("biglietto", "bilhete/ingresso", "viaggio", "Biglietto per il museo.", "Ingresso para o museu.", "/biʎˈʎetto/", "m", "biglietti"),
    ("prenotazione", "reserva", "viaggio", "Ho una prenotazione.", "Tenho uma reserva.", "/prenotatˈtsjone/", "f", "prenotazioni"),
    ("passaporto", "passaporte", "viaggio", "Controllo passaporti.", "Controle de passaportes.", "/passaˈpɔrto/", "m", "passaporti"),
    ("visto", "visto", "viaggio", "Serve il visto d'ingresso.", "Precisa do visto de entrada.", "/ˈvisto/", "m", "visti"),
    # Alloggi e Luoghi
    ("albergo", "hotel", "luoghi", "Un albergo a cinque stelle.", "Um hotel de cinco estrelas.", "/alˈbɛrɡo/", "m", "alberghi"),
    ("hotel", "hotel", "luoghi", "Prenotare l'hotel.", "Reservar o hotel.", "/oˈtɛl/", "m", "hotel"),
    ("pensione", "pensão", "luoghi", "Una piccola pensione.", "Uma pequena pensão.", "/penˈsjone/", "f", "pensioni"),
    ("ostello", "hostel/albergue", "luoghi", "Dormire in ostello.", "Dormir num hostel.", "/osˈtɛllo/", "m", "ostelli"),
    ("campeggio", "camping", "luoghi", "Andare in campeggio.", "Ir acampar.", "/kamˈpeddʒo/", "m", "campeggi"),
    ("camera", "quarto", "luoghi", "Una camera doppia.", "Um quarto duplo.", "/ˈkamera/", "f", "camere"),
    ("stanza", "quarto/cômodo", "luoghi", "La stanza d'albergo.", "O quarto de hotel.", "/ˈstantsa/", "f", "stanze"),
    ("reception", "recepção", "luoghi", "Chiedi alla reception.", "Pergunte na recepção.", "/reˈsɛpʃon/", "f", "reception"),
    ("bagaglio", "bagagem", "oggetti", "Portare il bagaglio.", "Levar a bagagem.", "/baˈɡaʎʎo/", "m", "bagagli"),
    ("valigia", "mala", "oggetti", "Disfare la valigia.", "Desfazer a mala.", "/vaˈlidʒa/", "f", "valigie"),
    ("zaino", "mochila", "oggetti", "Viaggiare con lo zaino.", "Viajar com a mochila.", "/ˈdzaino/", "m", "zaini"),
    ("souvenir", "suvenir/lembrança", "oggetti", "Comprare un souvenir.", "Comprar um suvenir.", "/suveˈnir/", "m", "souvenir"),
    ("cartolina", "cartão postal", "oggetti", "Spedire una cartolina.", "Enviar um cartão postal.", "/kartoˈlina/", "f", "cartoline"),
    ("monumento", "monumento", "luoghi", "Visitare il monumento.", "Visitar o monumento.", "/monuˈmento/", "m", "monumenti"),
    ("piazza", "praça", "luoghi", "Una piazza affollata.", "Uma praça lotada.", "/ˈpjattsa/", "f", "piazze"),
    ("fontana", "fonte", "luoghi", "La fontana di Trevi.", "A fonte de Trevi.", "/fonˈtana/", "f", "fontane"),
    ("chiesa", "igreja", "luoghi", "Entrare in chiesa.", "Entrar na igreja.", "/ˈkjɛza/", "f", "chiese"),
    ("cattedrale", "catedral", "luoghi", "La cattedrale gotica.", "A catedral gótica.", "/katteˈdrale/", "f", "cattedrali"),
    ("castello", "castelo", "luoghi", "Un castello antico.", "Um castelo antigo.", "/kasˈtɛllo/", "m", "castelli"),
    ("palazzo", "palácio/prédio", "luoghi", "Un palazzo reale.", "Um palácio real.", "/paˈlattso/", "m", "palazzi"),
    ("rovina", "ruína", "luoghi", "Rovine romane.", "Ruínas romanas.", "/roˈvina/", "f", "rovine"),
    ("scavi", "escavações", "luoghi", "Gli scavi di Pompei.", "As escavações de Pompeia.", "/ˈskavi/", "m", "scavi"),
    # Musei
    ("museo", "museu", "luoghi", "Andiamo al museo.", "Vamos ao museu.", "/muˈzɛo/", "m", "musei"),
    ("galleria", "galeria", "luoghi", "La galleria d'arte.", "A galeria de arte.", "/ɡalleˈria/", "f", "gallerie"),
    ("mostra", "exposição", "luoghi", "Una mostra fotografica.", "Uma exposição fotográfica.", "/ˈmostra/", "f", "mostre"),
    ("pinacoteca", "pinacoteca", "luoghi", "La pinacoteca di Brera.", "A pinacoteca de Brera.", "/pinakoˈtɛka/", "f", "pinacoteche"),
    ("quadro", "quadro", "oggetti", "Un quadro famoso.", "Um quadro famoso.", "/ˈkwadro/", "m", "quadri"),
    ("statua", "estátua", "oggetti", "La statua del David.", "A estátua do David.", "/ˈstatwa/", "f", "statue"),
    ("scultura", "escultura", "oggetti", "Una scultura di marmo.", "Uma escultura de mármore.", "/skulˈtura/", "f", "sculture"),
    ("affresco", "afresco", "oggetti", "Gli affreschi di Giotto.", "Os afrescos de Giotto.", "/afˈfresko/", "m", "affreschi"),
    ("opera d'arte", "obra de arte", "oggetti", "Un'opera d'arte unica.", "Uma obra de arte única.", "/ˈɔpera ˈdarte/", "f", "opere d'arte"),
    ("capolavoro", "obra-prima", "oggetti", "Ammirare un capolavoro.", "Admirar uma obra-prima.", "/kapolaˈvoro/", "m", "capolavori"),
    ("collezione", "coleção", "oggetti", "Una collezione privata.", "Uma coleção privada.", "/kolletˈtsjone/", "f", "collezioni"),
    ("ingresso", "entrada", "luoghi", "L'ingresso è gratuito.", "A entrada é gratuita.", "/inˈɡrɛsso/", "m", "ingressi"),
    ("uscita", "saída", "luoghi", "Dov'è l'uscita?", "Onde fica a saída?", "/uʃˈʃita/", "f", "uscite"),
    ("guardaroba", "guarda-volumes", "luoghi", "Lascia la giacca al guardaroba.", "Deixe a jaqueta no guarda-volumes.", "/ɡwardaˈrɔba/", "m", "guardaroba"),
    ("audioguida", "audioguia", "oggetti", "Noleggiare un'audioguida.", "Alugar um audioguia.", "/audjoˈɡwida/", "f", "audioguide"),
    ("bookshop", "loja do museu", "luoghi", "Comprare libri al bookshop.", "Comprar livros na loja do museu.", "/bukˈʃɔp/", "m", "bookshop"),
    # Verbi
    ("viaggiare", "viajar", "verbi", "Amo viaggiare molto.", "Amo viajar muito.", "/vjadˈdʒare/", None, None),
    ("visitare", "visitar", "verbi", "Visitare una città.", "Visitar uma cidade.", "/viziˈtare/", None, None),
    ("prenotare", "reservar", "verbi", "Prenotare il volo.", "Reservar o voo.", "/prenoˈtare/", None, None),
    ("alloggiare", "hospedar-se", "verbi", "Alloggiare in hotel.", "Hospedar-se em hotel.", "/allodˈdʒare/", None, None),
    ("pernottare", "pernoitar", "verbi", "Pernottare una notte.", "Pernoitar uma noite.", "/pernotˈtare/", None, None),
    ("partire", "partir", "verbi", "Partire per le vacanze.", "Partir para as férias.", "/parˈtire/", None, None),
    ("arrivare", "chegar", "verbi", "Arrivare in ritardo.", "Chegar atrasado.", "/arriˈvare/", None, None),
    ("tornare", "voltar", "verbi", "Tornare a casa.", "Voltar para casa.", "/torˈnare/", None, None),
    ("esplorare", "explorar", "verbi", "Esplorare i vicoli.", "Explorar os becos.", "/esploˈrare/", None, None),
    ("passeggiare", "passear", "verbi", "Passeggiare per il centro.", "Passear pelo centro.", "/passedˈdʒare/", None, None),
    ("ammirare", "admirar", "verbi", "Ammirare il panorama.", "Admirar a paisagem.", "/ammiˈrare/", None, None),
    ("fotografare", "fotografar", "verbi", "Fotografare il tramonto.", "Fotografar o pôr do sol.", "/fotoɡraˈfare/", None, None),
    ("scoprire", "descobrir", "verbi", "Scoprire posti nuovi.", "Descobrir lugares novos.", "/skoˈprire/", None, None),
    ("perdersi", "perder-se", "verbi", "Perdersi nelle strade.", "Perder-se nas ruas.", "/ˈpɛrdersi/", None, None),
    ("rilassarsi", "relaxar", "verbi", "Rilassarsi in spiaggia.", "Relaxar na praia.", "/rilasˈsarsi/", None, None),
    ("noleggiare", "alugar", "verbi", "Noleggiare un'auto.", "Alugar um carro.", "/noledˈdʒare/", None, None),
    ("assaggiare", "provar/degustar", "verbi", "Assaggiare cibi locali.", "Provar comidas locais.", "/assadˈdʒare/", None, None),
    ("fare le valigie", "fazer as malas", "verbi", "È ora di fare le valigie.", "É hora de fazer as malas.", "/ˈfare le vaˈlidʒe/", None, None),
    ("disfare", "desfazer", "verbi", "Disfare lo zaino.", "Desfazer a mochila.", "/disˈfare/", None, None),
    ("imbarcarsi", "embarcar", "verbi", "Imbarcarsi sull'aereo.", "Embarcar no avião.", "/imbarˈkarsi/", None, None),
    # Aggettivi e descrittori
    ("turistico", "turístico", "aggettivi", "Un villaggio turistico.", "Uma vila turística.", "/tuˈristiko/", "m", "turistici"),
    ("storico", "histórico", "aggettivi", "Il centro storico.", "O centro histórico.", "/ˈstɔriko/", "m", "storici"),
    ("affollato", "lotado", "aggettivi", "Un locale affollato.", "Um local lotato.", "/affolˈlato/", "m", "affollati"),
    ("tranquillo", "tranquilo", "aggettivi", "Un paesino tranquillo.", "Uma cidadezinha tranquila.", "/tranˈkwillo/", "m", "tranquilli"),
    ("famoso", "famoso", "aggettivi", "Un monumento famoso.", "Um monumento famoso.", "/faˈmozo/", "m", "famosi"),
    ("stupendo", "estupendo/maravilhoso", "aggettivi", "Un panorama stupendo.", "Uma paisagem maravilhosa.", "/stuˈpɛndo/", "m", "stupendi"),
    ("meraviglioso", "maravilhoso", "aggettivi", "Un viaggio meraviglioso.", "Uma viagem maravilhosa.", "/meraviˈʎʎozo/", "m", "meravigliosi"),
    ("indimenticabile", "inesquecibile", "aggettivi", "Un'esperienza indimenticabile.", "Uma experiência inesquecível.", "/indimentiˈkabile/", "m", "indimenticabili"),
    ("caro", "caro", "aggettivi", "Un hotel molto caro.", "Um hotel muito caro.", "/ˈkaro/", "m", "cari"),
    ("economico", "barato", "aggettivi", "Un volo economico.", "Um voo barato.", "/ekoˈnɔmiko/", "m", "economici"),
    ("comodo", "cômodo", "aggettivi", "Un letto comodo.", "Uma cama cômoda.", "/ˈkɔmodo/", "m", "comodi"),
    ("scomodo", "desconfortável", "aggettivi", "Un sedile scomodo.", "Um assento desconfortável.", "/ˈskɔmodo/", "m", "scomodi"),
    ("pittoresco", "pitoresco", "aggettivi", "Un villaggio pittoresco.", "Um vilarejo pitoresco.", "/pittoˈresko/", "m", "pittoreschi"),
    ("antico", "antigo", "aggettivi", "Un palazzo antico.", "Um palácio antigo.", "/anˈtiko/", "m", "antichi"),
    ("moderno", "moderno", "aggettivi", "Un museo moderno.", "Um museu moderno.", "/moˈdɛrno/", "m", "moderni"),
    ("gratuito", "gratuito", "aggettivi", "Il tour è gratuito.", "O tour é gratuito.", "/ɡraˈtuito/", "m", "gratuiti"),
    ("pagamento", "pago/pagamento", "aggettivi", "Ingresso a pagamento.", "Entrada paga.", "/paɡaˈmento/", "m", "pagamenti"),
    ("aperto", "aberto", "aggettivi", "Il museo è aperto.", "O museu está aberto.", "/aˈpɛrto/", "m", "aperti"),
    ("chiuso", "fechado", "aggettivi", "Il negozio è chiuso.", "A loja está fechada.", "/ˈkjuzo/", "m", "chiusi"),
    ("guidato", "guiado", "aggettivi", "Una visita guidata.", "Uma visita guiada.", "/ɡwiˈdato/", "m", "guidati"),
    ("locale", "local", "aggettivi", "Il cibo locale.", "A comida local.", "/loˈkale/", "m", "locali"),
    ("straniero", "estrangeiro", "aggettivi", "Un turista straniero.", "Um turista estrangeiro.", "/straˈnjɛro/", "m", "stranieri"),
    ("nazionale", "nacional", "aggettivi", "Un parco nazionale.", "Um parque nacional.", "/natsjoˈnale/", "m", "nazionali"),
    ("internazionale", "internacional", "aggettivi", "Volo internazionale.", "Voo internacional.", "/internatsjoˈnale/", "m", "internazionali"),
    ("tipico", "típico", "aggettivi", "Un piatto tipico.", "Um prato típico.", "/ˈtipiko/", "m", "tipici"),
    ("tradizionale", "tradicional", "aggettivi", "Festa tradizionale.", "Festa tradicional.", "/traditsjoˈnale/", "m", "tradizionali"),
    ("culturale", "cultural", "aggettivi", "Viaggio culturale.", "Viagem cultural.", "/kultuˈrale/", "m", "culturali"),
    ("rilassante", "relaxante", "aggettivi", "Una vacanza rilassante.", "Umas férias relaxantes.", "/rilasˈsante/", "m", "rilassanti"),
    ("avventuroso", "aventureiro/de aventura", "aggettivi", "Un viaggio avventuroso.", "Uma viagem de aventura.", "/avventuˈrozo/", "m", "avventurosi"),
    ("esotico", "exótico", "aggettivi", "Un paese esotico.", "Um país exótico.", "/eˈzɔtiko/", "m", "esotici"),
    ("incantevole", "encantador", "aggettivi", "Un posto incantevole.", "Um lugar encantador.", "/inkanˈtevole/", "m", "incantevoli"),
    ("spettacolare", "espetacular", "aggettivi", "Una vista spettacolare.", "Uma vista espetacular.", "/spettakoˈlare/", "m", "spettacolari"),
    ("noioso", "chato", "aggettivi", "Un tour noioso.", "Um tour chato.", "/noˈjozo/", "m", "noiosi"),
    ("interessante", "interessante", "aggettivi", "Un museo interessante.", "Um museu interessante.", "/interesˈsante/", "m", "interessanti"),
    ("lungo", "longo", "aggettivi", "Un volo lungo.", "Um voo longo.", "/ˈlunɡo/", "m", "lunghi"),
    ("breve", "curto", "aggettivi", "Una breve vacanza.", "Umas férias curtas.", "/ˈbreve/", "m", "brevi")
]

def create_new(templo_num, nome, citta, livello, parole_data):
    palavras = []
    for i, (it, pt, cat, ex_it, ex_pt, ipa, gen, pl) in enumerate(parole_data, 1):
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
    print(f"CREATED templo-{templo_num}.json -- {len(palavras)} parole")

if __name__ == "__main__":
    append_to_existing(30, t30_add)
    append_to_existing(31, t31_add)
    
    create_new(32, "La Storia d'Italia", "Roma", "B1", t32_data)
    create_new(33, "Il Turismo e i Musei", "Venezia", "A2", t33_data)
