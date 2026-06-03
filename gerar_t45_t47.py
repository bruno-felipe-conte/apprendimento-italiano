import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def w(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {
        "id": tid, "italiano": it, "portugues": pt, "genero": gen, "plural": pl,
        "exemplo": ex_it, "exemplo_pt": ex_pt, "categoria": cat, "dificuldade": "difficile", "audio_ipa": ipa
    }

def append_to_existing(templo_num, new_words_data):
    path = os.path.join(OUT, "data", f"templo-{templo_num}.json")
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    
    current_count = len(obj["palavras"])
    for i, (it, pt, cat, ex_it, ex_pt, ipa, gen, pl) in enumerate(new_words_data, current_count + 1):
        tid = f"t{templo_num}_{i:03d}"
        obj["palavras"].append(w(tid, it, pt, cat, ex_it, ex_pt, ipa, gen, pl))
        
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"APPENDED templo-{templo_num}.json -- now has {len(obj['palavras'])} parole")

t42_add = [
    ("manierismo", "maneirismo", "letteratura", "Il manierismo in letteratura.", "O maneirismo na literatura.", "/manjeˈrizmo/", "m", "manierismi"),
    ("illuminismo", "iluminismo", "letteratura", "L'illuminismo lombardo.", "O iluminismo lombardo.", "/illuminiˈzmo/", "m", "illuminismi"),
    ("verismo", "verismo", "letteratura", "Il verismo di Verga.", "O verismo de Verga.", "/veˈrizmo/", "m", "verismi"),
    ("decadentismo", "decadentismo", "letteratura", "Il decadentismo di D'Annunzio.", "O decadentismo de D'Annunzio.", "/dekadenˈtizmo/", "m", "decadentismi"),
    ("futurismo", "futurismo", "letteratura", "Il manifesto del futurismo.", "O manifesto do futurismo.", "/futuˈrizmo/", "m", "futurismi"),
    ("ermetismo", "hermetismo", "letteratura", "La poesia dell'ermetismo.", "A poesia do hermetismo.", "/ermeˈtizmo/", "m", "ermetismi"),
    ("neorealismo", "neorrealismo", "letteratura", "Il neorealismo italiano.", "O neorrealismo italiano.", "/neoreaˈlizmo/", "m", "neorealismi"),
    ("sonetto", "soneto", "letteratura", "Un sonetto di Petrarca.", "Um soneto de Petrarca.", "/soˈnetto/", "m", "sonetti"),
    ("cantica", "cântico", "letteratura", "La prima cantica.", "O primeiro cântico.", "/ˈkantika/", "f", "cantiche"),
    ("endecasillabo", "hendecassílabo", "letteratura", "Un verso endecasillabo.", "Um verso hendecassílabo.", "/endekaˈsillabo/", "m", "endecasillabi")
]

t43_add = [
    ("satiro", "sátiro", "creature", "Un satiro dispettoso.", "Um sátiro travesso.", "/ˈsatiro/", "m", "satiri"),
    ("arpa", "harpa", "oggetti", "Suonare l'arpa magica.", "Tocar a harpa mágica.", "/ˈarpa/", "f", "arpe"),
    ("pegaso", "pégaso", "creature", "Il cavallo alato Pegaso.", "O cavalo alado Pégaso.", "/ˈpɛɡazo/", "m", "pegasi"),
    ("unicorno", "unicórnio", "creature", "Il corno dell'unicorno.", "O chifre do unicórnio.", "/uniˈkɔrno/", "m", "unicorni"),
    ("grifone", "grifo", "creature", "Un fiero grifone.", "Um grifo orgulhoso.", "/ɡriˈfone/", "m", "grifoni"),
    ("sfinge", "esfinge", "creature", "L'enigma della sfinge.", "O enigma da esfinge.", "/ˈsfindʒe/", "f", "sfingi"),
    ("araba fenice", "fênix", "creature", "Rinasce la fenice.", "Renasce a fênix.", "/ˈaraba feˈnitʃe/", "f", None),
    ("medusa", "medusa", "creature", "Lo sguardo di Medusa.", "O olhar da Medusa.", "/meˈduza/", "f", "meduse"),
    ("gorgone", "górgona", "creature", "Una terribile gorgone.", "Uma terrível górgona.", "/ˈɡɔrɡone/", "f", "gorgoni"),
    ("idra", "hidra", "creature", "L'idra a sette teste.", "A hidra de sete cabeças.", "/ˈidra/", "f", "idre"),
    ("chimera", "quimera", "creature", "Inseguire una chimera.", "Perseguir uma quimera.", "/kiˈmɛra/", "f", "chimere"),
    ("cerbero", "cérbero", "creature", "Il cane a tre teste.", "O cão de três cabeças.", "/ˈtʃɛrbero/", "m", "cerberi"),
    ("valchiria", "valquíria", "creature", "Le valchirie in volo.", "As valquírias em voo.", "/valˈkirja/", "f", "valchirie"),
    ("troll", "troll (mitologia)", "creature", "Un troll di montagna.", "Um troll da montanha.", "/trɔl/", "m", "troll"),
    ("goblin", "goblin", "creature", "Un goblin dispettoso.", "Um goblin travesso.", "/ˈɡɔblin/", "m", "goblin"),
    ("oracolo", "oráculo", "luoghi", "Consultare l'oracolo.", "Consultar o oráculo.", "/oˈrakolo/", "m", "oracoli")
]

t44_add = [
    ("ergastolo", "prisão perpétua", "giurisprudenza", "Condannato all'ergastolo.", "Condenado à prisão perpétua.", "/erˈɡastolo/", "m", "ergastoli"),
    ("estradizione", "extradição", "giurisprudenza", "Chiedere l'estradizione.", "Pedir a extradição.", "/estraditˈtsjone/", "f", "estradizioni"),
    ("prescrizione", "prescrição", "giurisprudenza", "Il reato va in prescrizione.", "O crime prescreve.", "/preskritˈtsjone/", "f", "prescrizioni"),
    ("indulto", "indulto", "giurisprudenza", "Concedere un indulto.", "Conceder um indulto.", "/inˈdulto/", "m", "indulti"),
    ("amnistia", "anistia", "giurisprudenza", "Un'amnistia generale.", "Uma anistia geral.", "/amnisˈtia/", "f", "amnistie"),
    ("libertà vigilata", "liberdade condicional", "giurisprudenza", "È in libertà vigilata.", "Está em liberdade condicional.", "/liberˈta vidʒiˈlata/", "f", None),
    ("mandato", "mandado", "giurisprudenza", "Mandato di cattura.", "Mandado de prisão.", "/manˈdato/", "m", "mandati"),
    ("perquisizione", "busca (policial)", "giurisprudenza", "Mandato di perquisizione.", "Mandado de busca.", "/perkwizitˈtsjone/", "f", "perquisizioni"),
    ("sequestro", "apreensão/sequestro", "giurisprudenza", "Il sequestro dei beni.", "A apreensão dos bens.", "/seˈkwɛstro/", "m", "sequestri")
]

# T45: L'Ingegneria e le Costruzioni (110 parole)
t45_data = [
    # Professioni e Discipline
    ("ingegneria", "engenharia", "disciplina", "Facoltà di ingegneria.", "Faculdade de engenharia.", "/indʒeɲɲeˈria/", "f", "ingegnerie"),
    ("architettura", "arquitetura", "disciplina", "Studiare architettura.", "Estudar arquitetura.", "/arkitetˈtura/", "f", "architetture"),
    ("geometria", "geometria", "disciplina", "Le regole della geometria.", "As regras da geometria.", "/dʒomeˈtria/", "f", "geometrie"),
    ("ingegnere", "engenheiro", "persone", "L'ingegnere civile.", "O engenheiro civil.", "/indʒeˈɲɲɛre/", "m/f", "ingegneri"),
    ("architetto", "arquiteto", "persone", "Il progetto dell'architetto.", "O projeto do arquiteto.", "/arkiˈtetto/", "m", "architetti"),
    ("geometra", "topógrafo/técnico em edificações", "persone", "Il geometra misura il terreno.", "O técnico mede o terreno.", "/dʒeˈɔmetra/", "m/f", "geometri"),
    ("muratore", "pedreiro", "persone", "Il muratore costruisce il muro.", "O pedreiro constrói o muro.", "/muraˈtore/", "m", "muratori"),
    ("idraulico", "encanador", "persone", "Chiamare l'idraulico.", "Chamar o encanador.", "/iˈdrauliko/", "m", "idraulici"),
    ("elettricista", "eletricista", "persone", "L'elettricista ripara l'impianto.", "O eletricista conserta a rede elétrica.", "/elettriˈtʃista/", "m/f", "elettricisti"),
    ("falegname", "marceneiro", "persone", "Il falegname fa i mobili.", "O marceneiro faz os móveis.", "/faleˈɲɲame/", "m", "falegnami"),
    ("fabbro", "ferreiro", "persone", "Il fabbro forgia il ferro.", "O ferreiro forja o ferro.", "/ˈfabbro/", "m", "fabbri"),
    ("operaio", "operário", "persone", "L'operaio in cantiere.", "O operário no canteiro de obras.", "/opeˈrajo/", "m", "operai"),
    ("appaltatore", "empreiteiro", "persone", "L'appaltatore edile.", "O empreiteiro civil.", "/appaltaˈtore/", "m", "appaltatori"),
    # Cantiere e Strutture
    ("cantiere", "canteiro de obras", "luoghi", "Lavorare in cantiere.", "Trabalhar no canteiro de obras.", "/kanˈtjɛre/", "m", "cantieri"),
    ("progetto", "projeto", "costruzioni", "Il progetto della casa.", "O projeto da casa.", "/proˈdʒɛtto/", "m", "progetti"),
    ("piantina", "planta (de casa)", "costruzioni", "La piantina dell'appartamento.", "A planta do apartamento.", "/pjanˈtina/", "f", "piantine"),
    ("fondamenta", "fundações", "costruzioni", "Gettare le fondamenta.", "Lançar as fundações.", "/fondaˈmenta/", "f. pl.", None),
    ("pilastro", "pilar", "costruzioni", "Un pilastro in cemento.", "Um pilar de cimento.", "/piˈlastro/", "m", "pilastri"),
    ("colonna", "coluna", "costruzioni", "Una colonna di marmo.", "Uma coluna de mármore.", "/koˈlonna/", "f", "colonne"),
    ("trave", "viga", "costruzioni", "La trave di legno.", "A viga de madeira.", "/ˈtrave/", "f", "travi"),
    ("muro", "muro/parede", "costruzioni", "Un muro portante.", "Uma parede estrutural.", "/ˈmuro/", "m", "muri"),
    ("parete", "parede", "costruzioni", "Dipingere la parete.", "Pintar a parede.", "/paˈrete/", "f", "pareti"),
    ("soffitto", "teto", "costruzioni", "Un soffitto alto.", "Um teto alto.", "/sofˈfitto/", "m", "soffitti"),
    ("tetto", "telhado", "costruzioni", "Riparare il tetto.", "Consertar o telhado.", "/ˈtetto/", "m", "tetti"),
    ("pavimento", "piso/chão", "costruzioni", "Lavare il pavimento.", "Lavar o chão.", "/paviˈmento/", "m", "pavimenti"),
    ("scala", "escada", "costruzioni", "Salire la scala.", "Subir a escada.", "/ˈskala/", "f", "scale"),
    ("ascensore", "elevador", "costruzioni", "Prendere l'ascensore.", "Pegar o elevador.", "/aʃʃenˈsore/", "m", "ascensori"),
    ("finestra", "janela", "costruzioni", "Aprire la finestra.", "Abrir a janela.", "/fiˈnɛstra/", "f", "finestre"),
    ("porta", "porta", "costruzioni", "Chiudere la porta.", "Fechar a porta.", "/ˈpɔrta/", "f", "porte"),
    ("balcone", "sacada", "costruzioni", "Affacciarsi al balcone.", "Debruçar-se na sacada.", "/balˈkone/", "m", "balconi"),
    ("terrazza", "terraço", "costruzioni", "Una terrazza panoramica.", "Um terraço panorâmico.", "/terˈrattsa/", "f", "terrazze"),
    ("facciata", "fachada", "costruzioni", "La facciata del palazzo.", "A fachada do prédio.", "/fatˈtʃata/", "f", "facciate"),
    ("ponte", "ponte", "costruzioni", "Costruire un ponte.", "Construir uma ponte.", "/ˈponte/", "m", "ponti"),
    ("galleria", "túnel/galeria", "costruzioni", "Una lunga galleria.", "Um longo túnel.", "/ɡalleˈria/", "f", "gallerie"),
    ("diga", "represa", "costruzioni", "La diga idroelettrica.", "A represa hidrelétrica.", "/ˈdiɡa/", "f", "dighe"),
    ("grattacielo", "arranha-céu", "costruzioni", "Il grattacielo più alto.", "O arranha-céu mais alto.", "/ɡrattaˈtʃɛlo/", "m", "grattacieli"),
    ("gru", "guindaste", "attrezzi", "La gru solleva il peso.", "O guindaste levanta o peso.", "/ɡru/", "f", "gru"),
    ("scavatrice", "escavadeira", "attrezzi", "La scavatrice in azione.", "A escavadeira em ação.", "/skavaˈtritʃe/", "f", "scavatrici"),
    ("betoniera", "betoneira", "attrezzi", "La betoniera gira.", "A betoneira gira.", "/betoˈnjɛra/", "f", "betoniere"),
    ("ponteggio", "andaime", "attrezzi", "Montare il ponteggio.", "Montar o andaime.", "/ponˈteddʒo/", "m", "ponteggi"),
    ("caschetto", "capacete (obra)", "attrezzi", "Indossare il caschetto.", "Usar o capacete de obra.", "/kasˈketto/", "m", "caschetti"),
    # Materiali
    ("materiale", "material", "materiali", "Materiale da costruzione.", "Material de construção.", "/mateˈrjale/", "m", "materiali"),
    ("cemento", "cimento", "materiali", "Cemento armato.", "Concreto armado.", "/tʃeˈmento/", "m", "cementi"),
    ("calcestruzzo", "concreto", "materiali", "Gettare il calcestruzzo.", "Lançar o concreto.", "/kaltʃesˈtruttso/", "m", "calcestruzzi"),
    ("mattone", "tijolo", "materiali", "Muro di mattoni.", "Muro de tijolos.", "/matˈtone/", "m", "mattoni"),
    ("pietra", "pedra", "materiali", "Una casa in pietra.", "Uma casa de pedra.", "/ˈpjɛtra/", "f", "pietre"),
    ("marmo", "mármore", "materiali", "Pavimento in marmo.", "Piso de mármore.", "/ˈmarmo/", "m", "marmi"),
    ("legno", "madeira", "materiali", "Trave di legno.", "Viga de madeira.", "/ˈleɲɲo/", "m", "legni"),
    ("ferro", "ferro", "materiali", "Struttura in ferro.", "Estrutura de ferro.", "/ˈfɛrro/", "m", "ferri"),
    ("acciaio", "aço", "materiali", "Travi d'acciaio.", "Vigas de aço.", "/atˈtʃajo/", "m", "acciai"),
    ("vetro", "vidro", "materiali", "Una vetrata di vetro.", "Uma vidraça de vidro.", "/ˈvetro/", "m", "vetri"),
    ("plastica", "plástico", "materiali", "Tubi di plastica.", "Canos de plástico.", "/ˈplastika/", "f", "plastiche"),
    ("ceramica", "cerâmica", "materiali", "Piastrelle in ceramica.", "Azulejos de cerâmica.", "/tʃeˈramika/", "f", "ceramiche"),
    ("piastrella", "azulejo", "materiali", "Una piastrella rotta.", "Um azulejo quebrado.", "/pjasˈtrɛlla/", "f", "piastrelle"),
    ("intonaco", "reboco", "materiali", "Passare l'intonaco.", "Passar o reboco.", "/inˈtɔnako/", "m", "intonaci"),
    ("vernice", "tinta", "materiali", "Un barattolo di vernice.", "Uma lata de tinta.", "/verˈnitʃe/", "f", "vernici"),
    ("gesso", "gesso", "materiali", "Pareti in cartongesso.", "Paredes de gesso acartonado.", "/ˈdʒɛsso/", "m", "gessi"),
    ("asfalto", "asfalto", "materiali", "Strada asfaltata.", "Rua asfaltada.", "/asˈfalto/", "m", "asfalti"),
    ("tubo", "cano/tubo", "materiali", "Un tubo dell'acqua.", "Um cano de água.", "/ˈtubo/", "m", "tubi"),
    ("filo", "fio", "materiali", "Un filo elettrico.", "Um fio elétrico.", "/ˈfilo/", "m", "fili"),
    ("chiodo", "prego", "materiali", "Piantare un chiodo.", "Pregar um prego.", "/ˈkjɔdo/", "m", "chiodi"),
    ("vite", "parafuso", "materiali", "Stringere la vite.", "Apertar o parafuso.", "/ˈvite/", "f", "viti"),
    ("bullone", "porca/parafuso (bullone)", "materiali", "Un bullone di ferro.", "Um parafuso de ferro.", "/bulˈlone/", "m", "bulloni"),
    # Verbi
    ("costruire", "construir", "verbi", "Costruire una casa.", "Construir uma casa.", "/kostruˈire/", None, None),
    ("demolire", "demolir", "verbi", "Demolire un edificio.", "Demolir um edifício.", "/demoˈlire/", None, None),
    ("progettare", "projetare", "verbi", "Progettare un ponte.", "Projetar uma ponte.", "/prodʒetˈtare/", None, None),
    ("restaurare", "restaurar", "verbi", "Restaurare un palazzo.", "Restaurar um palácio.", "/restauˈrare/", None, None),
    ("riparare", "consertar/reparar", "verbi", "Riparare il tetto.", "Consertar o telhado.", "/ripaˈrare/", None, None),
    ("ristrutturare", "reformar", "verbi", "Ristrutturare l'appartamento.", "Reformar o apartamento.", "/ristruttuˈrare/", None, None),
    ("scavare", "escavar", "verbi", "Scavare una buca.", "Escavar um buraco.", "/skaˈvare/", None, None),
    ("misurare", "medir", "verbi", "Misurare la stanza.", "Medir o quarto.", "/mizuˈrare/", None, None),
    ("livellare", "nivelar", "verbi", "Livellare il terreno.", "Nivelar o terreno.", "/livelˈlare/", None, None),
    ("dipingere", "pintar", "verbi", "Dipingere la parete.", "Pintar a parede.", "/diˈpindʒere/", None, None),
    ("verniciare", "pintar (envernizar)", "verbi", "Verniciare il legno.", "Envernizar a madeira.", "/verniˈtʃare/", None, None),
    ("saldare", "soldar", "verbi", "Saldare i tubi.", "Soldar os canos.", "/salˈdare/", None, None),
    ("avvitare", "parafusar", "verbi", "Avvitare la mensola.", "Parafusar a prateleira.", "/avviˈtare/", None, None),
    ("svitare", "desparafusar", "verbi", "Svitare il bullone.", "Desparafusar a porca.", "/zviˈtare/", None, None),
    ("montare", "montar", "verbi", "Montare il mobile.", "Montar o móvel.", "/monˈtare/", None, None),
    ("smontare", "desmontar", "verbi", "Smontare l'impalcatura.", "Desmontar o andaime.", "/zmonˈtare/", None, None),
    ("installare", "instalar", "verbi", "Installare l'impianto.", "Instalar o sistema.", "/instalˈlare/", None, None),
    ("sigillare", "selar", "verbi", "Sigillare le fessure.", "Selar as rachaduras.", "/sidʒilˈlare/", None, None),
    ("isolare", "isolar", "verbi", "Isolare la casa dal freddo.", "Isolar a casa do frio.", "/izoˈlare/", None, None),
    # Aggettivi e descrittori
    ("civile", "civil (engenharia)", "aggettivi", "Ingegneria civile.", "Engenharia civil.", "/tʃiˈvile/", "m", "civili"),
    ("edile", "civil/da construção", "aggettivi", "Impresa edile.", "Empreiteira.", "/eˈdile/", "m", "edili"),
    ("strutturale", "estrutural", "aggettivi", "Un danno strutturale.", "Um dano estrutural.", "/struttuˈrale/", "m", "strutturali"),
    ("antisismico", "antissísmico", "aggettivi", "Edificio antisismico.", "Edifício antissísmico.", "/antiˈzizmiko/", "m", "antisismici"),
    ("solido", "sólido", "aggettivi", "Un muro solido.", "Um muro sólido.", "/ˈsɔlido/", "m", "solidi"),
    ("fragile", "frágil", "aggettivi", "Una struttura fragile.", "Uma estrutura frágil.", "/ˈfradʒile/", "m", "fragili"),
    ("portante", "estrutural (suporte)", "aggettivi", "Muro portante.", "Parede estrutural.", "/porˈtante/", "m", "portanti"),
    ("prefabbricato", "pré-fabricado", "aggettivi", "Casa prefabbricata.", "Casa pré-fabricada.", "/prefabbriˈkato/", "m", "prefabbricati"),
    ("grezzο", "bruto/sem acabamento", "aggettivi", "Lavoro al grezzo.", "Obra bruta.", "/ˈɡreddzo/", "m", "grezzi"),
    ("finito", "acabado/pronto", "aggettivi", "Un lavoro ben finito.", "Um trabalho bem acabado.", "/fiˈnito/", "m", "finiti"),
    ("moderno", "moderno", "aggettivi", "Design moderno.", "Design moderno.", "/moˈdɛrno/", "m", "moderni"),
    ("antico", "antigo", "aggettivi", "Un palazzo antico.", "Um palácio antigo.", "/anˈtiko/", "m", "antichi"),
    ("ristrutturato", "reformado", "aggettivi", "Appartamento ristrutturato.", "Apartamento reformado.", "/ristruttuˈrato/", "m", "ristrutturati"),
    ("pericolante", "em ruínas/perigoso", "aggettivi", "Muro pericolante.", "Muro em risco de cair.", "/perikoˈlante/", "m", "pericolanti")
]

# T46: I Sentimenti e le Emozioni Complesse (110 parole)
t46_data = [
    # Emozioni e Sentimenti
    ("amore", "amor", "emozioni", "Il vero amore.", "O verdadeiro amor.", "/aˈmore/", "m", "amori"),
    ("odio", "ódio", "emozioni", "Amore e odio.", "Amor e ódio.", "/ˈɔdjo/", "m", "odii"),
    ("affetto", "afeto/carinho", "emozioni", "Provare molto affetto.", "Sentir muito afeto.", "/afˈfɛtto/", "m", "affetti"),
    ("passione", "paixão", "emozioni", "Una passione travolgente.", "Uma paixão avassaladora.", "/pasˈsjone/", "f", "passioni"),
    ("tenerezza", "ternura", "emozioni", "Un gesto di tenerezza.", "Um gesto de ternura.", "/teneˈrettsa/", "f", "tenerezze"),
    ("dolcezza", "doçura", "emozioni", "Parla con dolcezza.", "Fala com doçura.", "/dolˈtʃettsa/", "f", "dolcezze"),
    ("nostalgia", "nostalgia/saudade", "emozioni", "Sentire nostalgia di casa.", "Sentir saudade de casa.", "/nostalˈdʒia/", "f", "nostalgie"),
    ("malinconia", "melancolia", "emozioni", "Una dolce malinconia.", "Uma doce melancolia.", "/malinkoˈnia/", "f", "malinconie"),
    ("gioia", "alegria", "emozioni", "Esplodere di gioia.", "Explodir de alegria.", "/ˈdʒɔja/", "f", "gioie"),
    ("euforia", "euforia", "emozioni", "Uno stato di euforia.", "Um estado de euforia.", "/eufoˈria/", "f", "euforie"),
    ("tristezza", "tristeza", "emozioni", "Una profonda tristezza.", "Uma profunda tristeza.", "/trisˈtettsa/", "f", "tristezze"),
    ("disperazione", "desespero", "emozioni", "Piangere dalla disperazione.", "Chorar de desespero.", "/disperatˈtsjone/", "f", "disperazioni"),
    ("paura", "medo", "emozioni", "Avere paura del buio.", "Ter medo do escuro.", "/paˈura/", "f", "paure"),
    ("terrore", "terror/pânico", "emozioni", "Gridare per il terrore.", "Gritar de terror.", "/terˈrore/", "m", "terrori"),
    ("spavento", "susto/espanto", "emozioni", "Che spavento mi hai fatto!", "Que susto você me deu!", "/spaˈvɛnto/", "m", "spaventi"),
    ("rabbia", "raiva", "emozioni", "Tremare di rabbia.", "Tremer de raiva.", "/ˈrabbja/", "f", "rabbie"),
    ("collera", "cólera/ira", "emozioni", "Un eccesso di collera.", "Um acesso de cólera.", "/ˈkɔllera/", "f", "collere"),
    ("furore", "furor/fúria", "emozioni", "In un impeto di furore.", "Num ímpeto de fúria.", "/fuˈrore/", "m", "furori"),
    ("risentimento", "ressentimento", "emozioni", "Covare risentimento.", "Nutrir ressentimento.", "/risentiˈmento/", "m", "risentimenti"),
    ("rancore", "rancor", "emozioni", "Non porto rancore.", "Não guardo rancor.", "/ranˈkore/", "m", "rancori"),
    ("invidia", "inveja", "emozioni", "Verde d'invidia.", "Verde de inveja.", "/inˈvidja/", "f", "invidie"),
    ("gelosia", "ciúme", "emozioni", "Pazzo di gelosia.", "Louco de ciúme.", "/dʒeloˈzia/", "f", "gelosie"),
    ("ammirazione", "admiração", "emozioni", "Provare ammirazione.", "Sentir admiração.", "/ammiratˈtsjone/", "f", "ammirazioni"),
    ("disprezzo", "desprezo", "emozioni", "Guardare con disprezzo.", "Olhar com desprezo.", "/disˈprɛttso/", "m", "disprezzi"),
    ("vergogna", "vergonha", "emozioni", "Arrossire di vergogna.", "Corar de vergonha.", "/verˈɡoɲɲa/", "f", "vergogne"),
    ("imbarazzo", "embaraço/constrangimento", "emozioni", "Un momento di imbarazzo.", "Um momento de constrangimento.", "/imbaˈrattso/", "m", "imbarazzi"),
    ("senso di colpa", "sentimento de culpa", "emozioni", "Avere sensi di colpa.", "Ter sentimentos de culpa.", "/ˈsɛnso di ˈkolpa/", "m", "sensi di colpa"),
    ("rimorso", "remorso", "emozioni", "Il rimorso della coscienza.", "O remorso da consciência.", "/riˈmɔrso/", "m", "rimorsi"),
    ("rimpianto", "arrependimento/saudade", "emozioni", "Non ho rimpianti.", "Não tenho arrependimentos.", "/rimˈpjanto/", "m", "rimpianti"),
    ("orgoglio", "orgulho", "emozioni", "Ferito nell'orgoglio.", "Ferido no orgulho.", "/orˈɡoʎʎo/", "m", "orgogli"),
    ("vanità", "vaidade", "emozioni", "Peccare di vanità.", "Pecar por vaidade.", "/vaniˈta/", "f", "vanità"),
    ("superbia", "soberba", "emozioni", "La superbia è un vizio.", "A soberba é um vício.", "/suˈpɛrbja/", "f", "superbie"),
    ("umiltà", "humildade", "emozioni", "Con grande umiltà.", "Com grande humildade.", "/umilˈta/", "f", "umiltà"),
    ("modestia", "modéstia", "emozioni", "Falsa modestia.", "Falsa modéstia.", "/moˈdɛstja/", "f", "modestie"),
    ("gratitudine", "gratidão", "emozioni", "Esprimere gratitudine.", "Expressar gratidão.", "/ɡratiˈtudine/", "f", "gratitudini"),
    ("riconoscenza", "reconhecimento/gratidão", "emozioni", "In segno di riconoscenza.", "Em sinal de reconhecimento.", "/rikonoʃˈʃɛntsa/", "f", "riconoscenze"),
    ("compassione", "compaixão", "emozioni", "Provare compassione.", "Sentir compaixão.", "/kompasˈsjone/", "f", "compassioni"),
    ("pietà", "piedade", "emozioni", "Avere pietà.", "Ter piedade.", "/pjeˈta/", "f", "pietà"),
    ("empatia", "empatia", "emozioni", "Mancanza di empatia.", "Falta de empatia.", "/empaˈtia/", "f", "empatie"),
    ("simpatia", "simpatia", "emozioni", "Provare simpatia.", "Sentir simpatia.", "/simpaˈtia/", "f", "simpatie"),
    ("antipatia", "antipatia", "emozioni", "Una pelle a pelle antipatia.", "Uma antipatia à primeira vista.", "/antipaˈtia/", "f", "antipatie"),
    ("noia", "tédio", "emozioni", "Morire di noia.", "Morrer de tédio.", "/ˈnɔja/", "f", "noie"),
    ("apatia", "apatia", "emozioni", "Uno stato di apatia.", "Um estado de apatia.", "/apaˈtia/", "f", "apatie"),
    ("sorpresa", "surpresa", "emozioni", "Una bella sorpresa.", "Uma bela surpresa.", "/sorˈpreza/", "f", "sorprese"),
    ("stupore", "espanto/estupor", "emozioni", "Restare con stupore.", "Ficar com espanto.", "/stuˈpore/", "m", "stupori"),
    ("meraviglia", "maravilha/deslumbramento", "emozioni", "Occhi pieni di meraviglia.", "Olhos cheios de deslumbramento.", "/meraˈviʎʎa/", "f", "meraviglie"),
    ("delusione", "decepção", "emozioni", "Una grande delusione.", "Uma grande decepção.", "/deluˈzjone/", "f", "delusioni"),
    ("speranza", "esperança", "emozioni", "La speranza è l'ultima a morire.", "A esperança é a última que morre.", "/speˈrantsa/", "f", "speranze"),
    ("fiducia", "confiança", "emozioni", "Avere fiducia in qualcuno.", "Ter confiança em alguém.", "/fiˈdutʃa/", "f", "fiducie"),
    ("diffidenza", "desconfiança", "emozioni", "Guardare con diffidenza.", "Olhar com desconfiança.", "/diffiˈdɛntsa/", "f", "diffidenze"),
    ("ansia", "ansiedade", "emozioni", "L'ansia per l'esame.", "A ansiedade pela prova.", "/ˈansja/", "f", "ansie"),
    ("angoscia", "angústia", "emozioni", "Un'angoscia terribile.", "Uma angústia terrível.", "/anˈɡɔʃʃa/", "f", "angosce"),
    ("sollievo", "alívio", "emozioni", "Tirare un sospiro di sollievo.", "Dar um suspiro de alívio.", "/solˈljɛvo/", "m", "sollievi"),
    ("pace", "paz", "emozioni", "Pace interiore.", "Paz interior.", "/ˈpatʃe/", "f", "paci"),
    ("serenità", "serenidade", "emozioni", "Vivere in serenità.", "Viver em serenidade.", "/sereniˈta/", "f", "serenità"),
    ("inquietudine", "inquietação", "emozioni", "Un senso di inquietudine.", "Um sentimento de inquietação.", "/inkwjeˈtudine/", "f", "inquietudini"),
    # Verbi
    ("amare", "amar", "verbi", "Amare alla follia.", "Amar loucamente.", "/aˈmare/", None, None),
    ("odiare", "odiar", "verbi", "Odiare con tutto il cuore.", "Odiar com todo o coração.", "/oˈdjare/", None, None),
    ("adorare", "adorar", "verbi", "Adorare i bambini.", "Adorar as crianças.", "/adoˈrare/", None, None),
    ("disprezzare", "desprezar", "verbi", "Disprezzare l'ignoranza.", "Desprezar a ignorância.", "/dispretˈtsare/", None, None),
    ("soffrire", "sofrer", "verbi", "Soffrire per amore.", "Sofrer por amor.", "/sofˈfrire/", None, None),
    ("gioire", "alegrar-se", "verbi", "Gioire per una vittoria.", "Alegrar-se por uma vitória.", "/dʒoˈire/", None, None),
    ("piangere", "chorar", "verbi", "Piangere a dirotto.", "Chorar copiosamente.", "/ˈpjandʒere/", None, None),
    ("ridere", "rir", "verbi", "Ridere di cuore.", "Rir de coração.", "/ˈridere/", None, None),
    ("sorridere", "sorrir", "verbi", "Sorridere alla vita.", "Sorrir para a vida.", "/sorˈridere/", None, None),
    ("spaventarsi", "assustar-se", "verbi", "Spaventarsi facilmente.", "Assustar-se facilmente.", "/spavenˈtarsi/", None, None),
    ("arrabbiarsi", "irritar-se/zangar-se", "verbi", "Arrabbiarsi per nulla.", "Irritar-se por nada.", "/arrabˈbjarsi/", None, None),
    ("calmarsi", "acalmar-se", "verbi", "Calmarsi dopo la tempesta.", "Acalmar-se depois da tempestade.", "/kalˈmarsi/", None, None),
    ("emozionarsi", "emocionar-se", "verbi", "Emozionarsi per un film.", "Emocionar-se com um filme.", "/emotsjoˈnarsi/", None, None),
    ("commuoversi", "comover-se", "verbi", "Commuoversi fino alle lacrime.", "Comover-se até às lágrimas.", "/komˈmwɔversi/", None, None),
    ("vergognarsi", "envergonhar-se", "verbi", "Vergognarsi dei propri errori.", "Envergonhar-se dos próprios erros.", "/verɡoˈɲɲarsi/", None, None),
    ("pentirsi", "arrepender-se", "verbi", "Pentirsi delle proprie azioni.", "Arrepender-se de suas ações.", "/penˈtirsi/", None, None),
    ("sperare", "ter esperança/esperar", "verbi", "Sperare in un futuro migliore.", "Esperar um futuro melhor.", "/speˈrare/", None, None),
    ("disperarsi", "desesperar-se", "verbi", "Disperarsi per la perdita.", "Desesperar-se pela perda.", "/dispeˈrarsi/", None, None),
    ("fidarsi", "confiar", "verbi", "Fidarsi ciecamente.", "Confiar cegamente.", "/fiˈdarsi/", None, None),
    ("dubitare", "duvidar", "verbi", "Dubitare di tutti.", "Duvidar de todos.", "/dubiˈtare/", None, None),
    ("perdonare", "perdoar", "verbi", "Perdonare un tradimento.", "Perdoar uma traição.", "/perdoˈnare/", None, None),
    ("consolare", "consolar", "verbi", "Consolare un amico triste.", "Consolar um amigo triste.", "/konsoˈlare/", None, None),
    ("incoraggiare", "encorajar", "verbi", "Incoraggiare a fare meglio.", "Encorajar a fazer melhor.", "/inkoradˈdʒare/", None, None),
    ("deludere", "decepcionar", "verbi", "Non deludere le aspettative.", "Não decepcionar as expectativas.", "/deˈludere/", None, None),
    # Aggettivi e Descrittori
    ("felice", "feliz", "aggettivi", "Sono molto felice.", "Estou muito feliz.", "/feˈlitʃe/", "m", "felici"),
    ("triste", "triste", "aggettivi", "Un viso triste.", "Um rosto triste.", "/ˈtriste/", "m", "tristi"),
    ("arrabbiato", "irritado/zangado", "aggettivi", "Un cane arrabbiato.", "Um cachorro bravo.", "/arrabˈbjato/", "m", "arrabbiati"),
    ("spaventato", "assustado", "aggettivi", "Un bambino spaventato.", "Um menino assustado.", "/spavenˈtato/", "m", "spaventati"),
    ("ansioso", "ansioso", "aggettivi", "Essere ansioso per i risultati.", "Estar ansioso pelos resultados.", "/anˈsjozo/", "m", "ansiosi"),
    ("sereno", "sereno", "aggettivi", "Un cielo sereno.", "Um céu sereno.", "/seˈreno/", "m", "sereni"),
    ("calmo", "calmo", "aggettivi", "Resta calmo.", "Fique calmo.", "/ˈkalmo/", "m", "calmi"),
    ("nervoso", "nervoso", "aggettivi", "Oggi sono nervoso.", "Hoje estou nervoso.", "/nerˈvozo/", "m", "nervosi"),
    ("depresso", "deprimido", "aggettivi", "Si sente depresso.", "Sente-se deprimido.", "/deˈprɛsso/", "m", "depressi"),
    ("entusiasta", "entusiasta/empolgado", "aggettivi", "Un pubblico entusiasta.", "Um público empolgado.", "/entuˈzjasta/", "m/f", "entusiasti"),
    ("apatico", "apático", "aggettivi", "Uno studente apatico.", "Um estudante apático.", "/aˈpatiko/", "m", "apatici"),
    ("ottimista", "otimista", "aggettivi", "Essere sempre ottimista.", "Ser sempre otimista.", "/ottiˈmista/", "m/f", "ottimisti"),
    ("pessimista", "pessimista", "aggettivi", "Vedere tutto nero, essere pessimista.", "Ver tudo negro, ser pessimista.", "/pessiˈmista/", "m/f", "pessimisti"),
    ("orgoglioso", "orgulhoso", "aggettivi", "Orgoglioso di te.", "Orgulhoso de você.", "/orɡoˈʎʎozo/", "m", "orgogliosi"),
    ("umile", "humilde", "aggettivi", "Di origini umili.", "De origens humildes.", "/ˈumile/", "m", "umili"),
    ("geloso", "ciumento", "aggettivi", "Un marito geloso.", "Um marido ciumento.", "/dʒeˈlozo/", "m", "gelosi"),
    ("invidioso", "invejoso", "aggettivi", "Sguardo invidioso.", "Olhar invejoso.", "/inviˈdjozo/", "m", "invidiosi"),
    ("grato", "grato", "aggettivi", "Ti sono molto grato.", "Te sou muito grato.", "/ˈɡrato/", "m", "grati"),
    ("indifferente", "indiferente", "aggettivi", "Rimase indifferente.", "Permaneceu indiferente.", "/indiffeˈrɛnte/", "m", "indifferenti"),
    ("appassionato", "apaixonado", "aggettivi", "Un bacio appassionato.", "Um beijo apaixonado.", "/appassjoˈnato/", "m", "appassionati"),
    ("tenero", "terno/macio", "aggettivi", "Un cuore tenero.", "Um coração terno.", "/ˈtɛnero/", "m", "teneri"),
    ("dolce", "doce", "aggettivi", "Una parola dolce.", "Uma palavra doce.", "/ˈdoltʃe/", "m", "dolci"),
    ("amaro", "amargo", "aggettivi", "Una delusione amara.", "Uma decepção amarga.", "/aˈmaro/", "m", "amari"),
    ("commosso", "comovido", "aggettivi", "Era visibilmente commosso.", "Estava visivelmente comovido.", "/komˈmɔsso/", "m", "commossi"),
    ("sorpreso", "surpreso", "aggettivi", "Una faccia sorpresa.", "Um rosto surpreso.", "/sorˈprezo/", "m", "sorpresi"),
    ("sconvolto", "chocado/perturbado", "aggettivi", "Sconvolto dalla notizia.", "Chocado com a notícia.", "/skonˈvɔlto/", "m", "sconvolti"),
    ("sollevato", "aliviado", "aggettivi", "Mi sento sollevato.", "Sinto-me aliviado.", "/solleˈvato/", "m", "sollevati"),
    ("colpevole", "culpado", "aggettivi", "Sguardo colpevole.", "Olhar culpado.", "/kolˈpevole/", "m", "colpevoli"),
    ("innocente", "inocente", "aggettivi", "Un sorriso innocente.", "Um sorriso inocente.", "/innoˈtʃɛnte/", "m", "innocenti")
]

# T47: I Verbi Idiomatici e i Modi di Dire (110 parole)
# Usiamo i verbi/espressioni comuni non dirette
t47_data = [
    # Modi di dire con FARE
    ("fare finta", "fingir", "espressioni", "Fare finta di niente.", "Fingir que não é nada.", "/ˈfare ˈfinta/", None, None),
    ("fare schifo", "dar nojo/ser ruim", "espressioni", "Questo cibo fa schifo.", "Esta comida é nojenta.", "/ˈfare ˈskifo/", None, None),
    ("fare una figuraccia", "passar vergonha/vexame", "espressioni", "Ho fatto una figuraccia.", "Passei um vexame.", "/ˈfare ˈuna fiɡuˈrattʃa/", None, None),
    ("fare il furbo", "dar uma de esperto", "espressioni", "Non fare il furbo con me.", "Não dê uma de esperto comigo.", "/ˈfare il ˈfurbo/", None, None),
    ("fare pena", "dar pena/ser patético", "espressioni", "Quel film fa pena.", "Aquele filme dá pena.", "/ˈfare ˈpena/", None, None),
    ("fare pace", "fazer as pazes", "espressioni", "Abbiamo fatto pace.", "Fizemos as pazes.", "/ˈfare ˈpatʃe/", None, None),
    ("fare caso", "prestar atenção", "espressioni", "Non ci ho fatto caso.", "Não prestei atenção nisso.", "/ˈfare ˈkazo/", None, None),
    ("fare gola", "dar água na boca", "espressioni", "Questo dolce mi fa gola.", "Este doce me dá água na boca.", "/ˈfare ˈɡola/", None, None),
    ("fare mente locale", "parar para pensar/recapitular", "espressioni", "Devo fare mente locale.", "Preciso recapitular as ideias.", "/ˈfare ˈmente loˈkale/", None, None),
    ("fare la fila", "fazer fila", "espressioni", "Dobbiamo fare la fila.", "Temos que fazer a fila.", "/ˈfare la ˈfila/", None, None),
    # Modi di dire con DARE
    ("dare fastidio", "incomodar", "espressioni", "Mi dà fastidio la luce.", "A luz me incomoda.", "/ˈdare fasˈtidjo/", None, None),
    ("dare una mano", "dar uma mão/ajudar", "espressioni", "Dammi una mano, per favore.", "Me dê uma mão, por favor.", "/ˈdare ˈuna ˈmano/", None, None),
    ("dare retta", "dar ouvidos", "espressioni", "Non dargli retta.", "Não dê ouvidos a ele.", "/ˈdare ˈrɛtta/", None, None),
    ("dare i numeri", "ficar louco/dizer absurdos", "espressioni", "Ma dai i numeri?", "Mas você tá doido?", "/ˈdare i ˈnumeri/", None, None),
    ("dare per scontato", "dar como certo", "espressioni", "Lo davo per scontato.", "Eu dava isso como certo.", "/ˈdare per skonˈtato/", None, None),
    ("dare all'occhio", "dar na vista/chamar atenção", "espressioni", "Questo colore dà all'occhio.", "Esta cor chama a atenção.", "/ˈdare allˈɔkkjo/", None, None),
    ("dare ragione", "dar razão", "espressioni", "Devo darti ragione.", "Tenho que te dar razão.", "/ˈdare raˈdʒone/", None, None),
    ("dare torto", "tirar a razão", "espressioni", "Non posso darti torto.", "Não posso te tirar a razão.", "/ˈdare ˈtɔrto/", None, None),
    ("dare buca", "dar o cano/bolo", "espressioni", "Mi ha dato buca.", "Ele me deu um bolo.", "/ˈdare ˈbuka/", None, None),
    ("dare un'occhiata", "dar uma olhada", "espressioni", "Vado a dare un'occhiata.", "Vou dar uma olhada.", "/ˈdare unokˈkjata/", None, None),
    # Modi di dire con ANDARE
    ("andare a ruba", "vender como água", "espressioni", "I biglietti sono andati a ruba.", "Os ingressos venderam como água.", "/anˈdare a ˈruba/", None, None),
    ("andare a gonfie vele", "ir de vento em popa", "espressioni", "Gli affari vanno a gonfie vele.", "Os negócios vão de vento em popa.", "/anˈdare a ˈɡonfje ˈvele/", None, None),
    ("andare in tilt", "dar pane/pifar", "espressioni", "Il computer è andato in tilt.", "O computador deu pane.", "/anˈdare in tilt/", None, None),
    ("andare d'accordo", "dar-se bem", "espressioni", "Vado d'accordo con lui.", "Me dou bem com ele.", "/anˈdare dakˈkɔrdo/", None, None),
    ("andare su tutte le furie", "ficar furioso", "espressioni", "È andato su tutte le furie.", "Ficou furioso.", "/anˈdare su ˈtutte le ˈfurje/", None, None),
    ("andarsene", "ir embora", "espressioni", "Voglio andarmene da qui.", "Quero ir embora daqui.", "/anˈdarsene/", None, None),
    ("andare a monte", "dar em nada/fracassar", "espressioni", "Il progetto è andato a monte.", "O projeto foi por água abaixo.", "/anˈdare a ˈmonte/", None, None),
    ("andare per le lunghe", "demorar demais", "espressioni", "La riunione sta andando per le lunghe.", "A reunião está demorando demais.", "/anˈdare ˈper le ˈlunɡe/", None, None),
    # Modi di dire con PRENDERE
    ("prendere in giro", "tirar sarro/zoar", "espressioni", "Smettila di prendermi in giro.", "Pare di tirar sarro de mim.", "/ˈprɛndere in ˈdʒiro/", None, None),
    ("prendere un granchio", "cometer um equívoco/dar mancada", "espressioni", "Ho preso un granchio.", "Dei uma mancada.", "/ˈprɛndere un ˈɡrankjo/", None, None),
    ("prendere fuoco", "pegar fogo", "espressioni", "Il legno ha preso fuoco.", "A madeira pegou fogo.", "/ˈprɛndere ˈfwɔko/", None, None),
    ("prendere a cuore", "levar a sério/importar-se", "espressioni", "Ho preso a cuore il problema.", "Levei o problema a sério.", "/ˈprɛndere a ˈkwɔre/", None, None),
    ("prendere due piccioni con una fava", "matar dois coelhos com uma cajadada", "espressioni", "Così prendiamo due piccioni con una fava.", "Assim matamos dois coelhos com uma cajadada.", "/ˈprɛndere ˈdue pitˈtʃoni kon ˈuna ˈfava/", None, None),
    ("prendersela", "levar a mal/ofender-se", "espressioni", "Non te la prendere.", "Não leve a mal.", "/ˈprɛndersela/", None, None),
    ("prendere il volo", "levantar voo/desaparecer", "espressioni", "I soldi hanno preso il volo.", "O dinheiro levantò voo (sumiu).", "/ˈprɛndere il ˈvolo/", None, None),
    # Altri Verbi
    ("essere in gamba", "ser bom (no que faz)", "espressioni", "È un ragazzo in gamba.", "É um rapaz muito bom.", "/ˈɛssere in ˈɡamba/", None, None),
    ("essere al verde", "estar sem dinheiro/liso", "espressioni", "Sono al verde questo mese.", "Estou liso este mês.", "/ˈɛssere al ˈverde/", None, None),
    ("avere un diavolo per capello", "estar muito irritado/furioso", "espressioni", "Oggi ho un diavolo per capello.", "Hoje estou furioso.", "/aˈvere un ˈdjavolo per kaˈpɛllo/", None, None),
    ("avere la puzza sotto il naso", "ser esnobe/nariz empinado", "espressioni", "Ha la puzza sotto il naso.", "É um nariz empinado.", "/aˈvere la ˈputtsa ˈsotto il ˈnazo/", None, None),
    ("avere le mani bucate", "ser gastador/mão aberta", "espressioni", "Tua moglie ha le mani bucate.", "Sua esposa é muito gastadora.", "/aˈvere le ˈmani buˈkate/", None, None),
    ("chiudere un occhio", "fazer vista grossa", "espressioni", "Questa volta chiudo un occhio.", "Desta vez farei vista grossa.", "/ˈkjudere un ˈɔkkjo/", None, None),
    ("costare un occhio della testa", "custar os olhos da cara", "espressioni", "Questo vestito costa un occhio della testa.", "Este vestido custa os olhos da cara.", "/kosˈtare un ˈɔkkjo ˈdella ˈtɛsta/", None, None),
    ("rimanerci male", "ficar chateado", "espressioni", "Ci sono rimasto male.", "Fiquei chateado com isso.", "/rimaˈnertʃi ˈmale/", None, None),
    ("farsene una ragione", "conformar-se", "espressioni", "Devi fartene una ragione.", "Você deve se conformar.", "/ˈfarsene ˈuna raˈdʒone/", None, None),
    ("perdere il filo", "perder o fio da meada", "espressioni", "Scusa, ho perso il filo del discorso.", "Desculpe, perdi o fio da meada.", "/ˈpɛrdere il ˈfilo/", None, None),
    ("mettere a fuoco", "focar", "espressioni", "Dobbiamo mettere a fuoco il problema.", "Devemos focar no problema.", "/ˈmettere a ˈfwɔko/", None, None),
    ("mettersi nei panni", "colocar-se no lugar", "espressioni", "Mettiti nei miei panni.", "Coloque-se no meu lugar.", "/ˈmettersi nei ˈpanni/", None, None),
    ("tagliare la corda", "fugir/cair fora", "espressioni", "Appena ha visto la polizia, ha tagliato la corda.", "Assim que viu a polícia, caiu fora.", "/taˈʎʎare la ˈkɔrda/", None, None),
    ("rompere il ghiaccio", "quebrar o gelo", "espressioni", "Ho raccontato una barzelletta per rompere il ghiaccio.", "Contei uma piada para quebrar o gelo.", "/ˈrompere il ˈɡjattʃo/", None, None),
    ("vuotare il sacco", "desembuchar/contar tudo", "espressioni", "È ora di vuotare il sacco.", "É hora de contar tudo.", "/vwoˈtare il ˈsakko/", None, None),
    ("salvare il salvabile", "salvar o que der", "espressioni", "Cerchiamo di salvare il salvabile.", "Vamos tentar salvar o que der.", "/salˈvare il salˈvabile/", None, None),
    ("tirare le cuoia", "esticar as canelas/morrer", "espressioni", "Alla fine ha tirato le cuoia.", "No final, ele esticou as canelas.", "/tiˈrare le ˈkwɔja/", None, None),
    ("alzare il gomito", "beber demais", "espressioni", "Ieri sera ha alzato il gomito.", "Ontem à noite ele bebeu demais.", "/alˈtsare il ˈɡomito/", None, None),
    ("arrampicarsi sugli specchi", "tentar se justificar sem argumentos", "espressioni", "Stai cercando di arrampicarti sugli specchi.", "Você está tentando se justificar sem ter como.", "/arrampiˈkarsi ˈsuʎʎi ˈspɛkki/", None, None),
    ("cavarsela", "safar-se/arranjar-se", "espressioni", "In inglese me la cavo.", "Em inglês eu me viro.", "/kaˈvarsela/", None, None),
    ("farcela", "conseguir", "espressioni", "Non ce la faccio più.", "Não aguento (consigo) mais.", "/ˈfartʃela/", None, None),
    ("aspettarsela", "esperar por isso", "espressioni", "Me l'aspettavo.", "Eu já esperava por isso.", "/aspetˈtarsela/", None, None),
    ("bersela", "engolir (mentira)/acreditar", "espressioni", "Se l'è bevuta tutta.", "Ele engoliu a história toda.", "/ˈbersela/", None, None),
    ("cercarsela", "procurar confusão/merecer", "espressioni", "Te la sei cercata.", "Você procurou por isso (mereceu).", "/tʃerˈkarsela/", None, None),
    ("godersela", "aproveitar (a vida)", "espressioni", "Se la sta godendo in vacanza.", "Está aproveitando as férias.", "/ɡoˈdersela/", None, None),
    ("legarsela al dito", "guardar rancor", "espressioni", "Me la sono legata al dito.", "Eu não vou esquecer isso (guardei rancor).", "/leˈɡarsela al ˈdito/", None, None),
    ("passarsela", "passar (bem/mal)", "espressioni", "Come te la passi?", "Como você está?", "/pasˈsarsela/", None, None),
    ("prendersela", "chatear-se", "espressioni", "Non te la prendere.", "Não fique chateado.", "/ˈprɛndersela/", None, None),
    ("sbrigarsela", "resolver/despachar", "espressioni", "Me la sbrigo io.", "Deixa que eu resolvo.", "/zbriˈɡarsela/", None, None),
    ("svignarsela", "cair fora de fininho", "espressioni", "Ce la siamo svignata di nascosto.", "Caímos fora de fininho.", "/zviˈɲɲarsela/", None, None),
    ("vedersela", "enfrentar/resolver-se", "espressioni", "Dovrai vedertela con me.", "Você terá que se resolver comigo.", "/veˈdersela/", None, None),
    # Esclamazioni / Parole Miste
    ("magari", "quem dera/talvez", "avverbi", "Magari fosse vero!", "Quem dera fosse verdade!", "/maˈɡari/", None, None),
    ("mica", "não (ênfase)/por acaso", "avverbi", "Non sono mica scemo.", "Não sou idiota.", "/ˈmika/", None, None),
    ("macché", "que nada!", "avverbi", "Macché! Non è vero.", "Que nada! Não é verdade.", "/makˈke/", None, None),
    ("figurati", "imagina/de nada", "espressioni", "Grazie! - Figurati!", "Obrigato! - Imagina!", "/fiˈɡurati/", None, None),
    ("meno male", "ainda bem", "espressioni", "Meno male che sei arrivato.", "Ainda bem que você chegou.", "/ˈmeno ˈmale/", None, None),
    ("peccato", "que pena", "espressioni", "Peccato che tu non venga.", "Que pena que você não vem.", "/pekˈkato/", None, None),
    ("anzi", "pelo contrário/aliás", "avverbi", "Non sono stanco, anzi.", "Não estou cansato, pelo contrário.", "/ˈantsi/", None, None),
    ("insomma", "enfim/mais ou menos", "avverbi", "Insomma, andiamo?", "Enfim, vamos?", "/inˈsomma/", None, None),
    ("infatti", "de fato", "avverbi", "È intelligente, e infatti studia molto.", "É inteligente, e de fato estuda muito.", "/inˈfatti/", None, None),
    ("addirittura", "até mesmo/nossa!", "avverbi", "Hai letto 10 libri? Addirittura!", "Você leu 10 livros? Nossa!", "/addiritˈtura/", None, None),
    ("ormai", "agora já/a esta altura", "avverbi", "Ormai è tardi.", "Agora já é tarde.", "/orˈmai/", None, None),
    ("allora", "então", "avverbi", "Allora, cosa facciamo?", "Então, o que fazemos?", "/alˈlora/", None, None),
    ("dunque", "portanto", "avverbi", "Penso, dunque sono.", "Penso, portanto sou.", "/ˈdunkwe/", None, None),
    ("pure", "também/até", "avverbi", "Vieni pure tu?", "Você vem também?", "/ˈpure/", None, None),
    ("casomai", "caso (aconteça)", "avverbi", "Casomai piovesse, porto l'ombrello.", "Caso chova, levo o guarda-chuva.", "/kazoˈmai/", None, None),
    ("apposta", "de propósito", "avverbi", "L'ha fatto apposta.", "Fez de propósito.", "/apˈpɔsta/", None, None),
    ("piuttosto", "em vez disso/bastante", "avverbi", "Piuttosto che uscire, leggo.", "Em vez de sair, leio.", "/pjutˈtɔsto/", None, None),
    ("cioè", "isto é/ou seja", "avverbi", "Torno tra poco, cioè domani.", "Volto em breve, isto é, amanhã.", "/tʃoˈɛ/", None, None),
    ("mica male", "nada mal", "espressioni", "Questa pizza non è mica male.", "Esta pizza não é nada mal.", "/ˈmika ˈmale/", None, None),
    ("roba da matti", "coisa de louco", "espressioni", "Pagare tanto è roba da matti.", "Pagar tanto é coisa de louco.", "/ˈrɔba da ˈmatti/", None, None),
    ("acqua in bocca", "bico calado", "espressioni", "Mi raccomando, acqua in bocca.", "Por favor, bico calado.", "/ˈakkwa in ˈbokka/", None, None),
    ("in bocca al lupo", "boa sorte", "espressioni", "In bocca al lupo per l'esame!", "Boa sorte na prova!", "/in ˈbokka al ˈlupo/", None, None),
    ("crepi", "obrigado (resp. boa sorte)", "espressioni", "Crepi il lupo!", "Que morra o lobo! (Obrigado)", "/ˈkrɛpi/", None, None),
    ("pelo nell'uovo", "pelo no ovo", "espressioni", "Cerchi sempre il pelo nell'uovo.", "Você sempre procura pelo em ovo.", "/ˈpelo nelˈlwɔvo/", None, None),
    ("un sacco", "um monte/muito", "espressioni", "Mi piace un sacco.", "Gosto pra caramba.", "/un ˈsakko/", None, None),
    ("alla mano", "acessível/simples", "espressioni", "È una persona molto alla mano.", "É uma pessoa muito acessível.", "/ˈalla ˈmano/", None, None),
    ("fuori di testa", "fora da casinha/louco", "espressioni", "Sei completamente fuori di testa.", "Você está completamente louco.", "/ˈfwɔri di ˈtɛsta/", None, None),
    ("a quattr'occhi", "a sós/particular", "espressioni", "Dobbiamo parlare a quattr'occhi.", "Temos que falar a sós.", "/a kwatˈtrɔkki/", None, None),
    ("su due piedi", "assim de repente/na lata", "espressioni", "Su due piedi non so risponderti.", "Assim de repente não sei te responder.", "/su ˈdue ˈpjɛdi/", None, None),
    ("di punto in bianco", "de repente/do nada", "espressioni", "Se n'è andato di punto in bianco.", "Foi embora do nada.", "/di ˈpunto im ˈbjanko/", None, None),
    ("in fin dei conti", "no fim das contas", "espressioni", "In fin dei conti, ha ragione lui.", "No fim das contas, ele tem razão.", "/in ˈfin dei ˈkonti/", None, None),
    ("per filo e per segno", "tintim por tintim/com detalhes", "espressioni", "Raccontami tutto per filo e per segno.", "Me conte tudo tintim por tintim.", "/per ˈfilo e per ˈseɲɲo/", None, None)
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
    append_to_existing(42, t42_add)
    append_to_existing(43, t43_add)
    append_to_existing(44, t44_add)
    
    create_new(45, "L'Ingegneria e le Costruzioni", "Milano", "C1", t45_data)
    create_new(46, "I Sentimenti e le Emozioni Complesse", "Verona", "B2", t46_data)
    create_new(47, "I Verbi Idiomatici e i Modi di Dire", "Roma", "C2", t47_data)
