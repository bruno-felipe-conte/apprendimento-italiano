import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def w(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {
        "id": tid, "italiano": it, "portugues": pt, "genero": gen, "plural": pl,
        "exemplo": ex_it, "exemplo_pt": ex_pt, "categoria": cat, "dificuldade": "medio", "audio_ipa": ipa
    }

# Fixes
t27_add = [
    ("acquerello", "aquarela", "strumenti", "Dipingere ad acquerello.", "Pintar em aquarela.", "/akkweˈrɛllo/", "m", "acquerelli"),
    ("pennarello", "canetinha", "strumenti", "Disegnare con il pennarello.", "Desenhar com a canetinha.", "/pennaˈrɛllo/", "m", "pennarelli"),
    ("carboncino", "carvão (desenho)", "strumenti", "Un ritratto a carboncino.", "Um retrato a carvão.", "/karbonˈtʃino/", "m", "carboncini"),
    ("cavalletto", "cavalete", "strumenti", "La tela sul cavalletto.", "A tela no cavalete.", "/kavalˈletto/", "m", "cavalletti"),
    ("argilla", "argila", "strumenti", "Vasi di argilla.", "Vasos de argila.", "/arˈdʒilla/", "f", "argille"),
    ("cera", "cera", "strumenti", "Statue di cera.", "Estátuas de cera.", "/ˈtʃera/", "f", "cere"),
    ("sfumatura", "nuance/tom", "stili", "Una sfumatura di blu.", "Uma nuance de azul.", "/sfumaˈtura/", "f", "sfumature"),
    ("chiaroscuro", "claro-escuro", "stili", "La tecnica del chiaroscuro.", "A técnica do claro-escuro.", "/kjaroˈskuro/", "m", "chiaroscuri"),
    ("prospettiva", "perspectiva", "stili", "Disegnare in prospettiva.", "Desenhar em perspectiva.", "/prospetˈtiva/", "f", "prospettive"),
    ("astrattismo", "abstracionismo", "stili", "L'arte dell'astrattismo.", "A arte do abstracionismo.", "/astratˈtizmo/", "m", "astrattismi"),
    ("cubismo", "cubismo", "stili", "Picasso e il cubismo.", "Picasso e o cubismo.", "/kuˈbizmo/", "m", "cubismi"),
    ("impressionismo", "impressionismo", "stili", "I pittori dell'impressionismo.", "Os pintores do impressionismo.", "/impressjoˈnizmo/", "m", "impressionismi"),
    ("espressionismo", "expressionismo", "stili", "L'espressionismo tedesco.", "O expressionismo alemão.", "/espressjoˈnizmo/", "m", "espressionismi"),
    ("surrealismo", "surrealismo", "stili", "Dalí e il surrealismo.", "Dalí e o surrealismo.", "/surreaˈlizmo/", "m", "surrealismi")
]

t28_add = [
    ("sintetizzatore", "sintetizador", "strumenti", "Suona il sintetizzatore.", "Toca o sintetizador.", "/sintetiddzaˈtore/", "m", "sintetizzatori")
]

t29_add = [
    ("ciak", "claquete", "elementi", "Azione, ciak si gira!", "Ação, gravando!", "/tʃak/", "m", "ciak"),
    ("provino", "teste (casting)", "elementi", "Oggi ho un provino.", "Hoje tenho um teste.", "/proˈvino/", "m", "provini"),
    ("casting", "elenco/casting", "elementi", "Fare un casting.", "Fazer um casting.", "/ˈkastiŋ/", "m", "casting"),
    ("botteghino", "bilheteria", "elementi", "Compra il biglietto al botteghino.", "Compre o ingresso na bilheteria.", "/botteˈɡino/", "m", "botteghini"),
    ("multisala", "cinema multiplex", "luoghi", "Un cinema multisala.", "Um cinema multiplex.", "/multiˈsala/", "f", "multisala"),
    ("poltronissima", "cadeira vip", "elementi", "Biglietto per la poltronissima.", "Ingresso para a cadeira vip.", "/poltroˈnissima/", "f", "poltronissime"),
    ("camerino", "camarim", "luoghi", "L'attore è nel camerino.", "O ator está no camarim.", "/kameˈrino/", "m", "camerini"),
    ("controfigura", "dublê", "persone", "L'attore usa una controfigura.", "O ator usa um dublê.", "/kontrofiˈɡura/", "f", "controfigure"),
    ("stuntman", "dublê de ação", "persone", "Uno stuntman coraggioso.", "Um dublê corajoso.", "/ˈstantmɛn/", "m", "stuntman"),
    ("faretto", "holofote", "elementi", "Il faretto illumina il palco.", "O holofote ilumina o palco.", "/faˈretto/", "m", "faretti"),
    ("inquadrare", "enquadrar", "verbi", "Inquadrare la scena perfetta.", "Enquadrar a cena perfeita.", "/inkwaˈdrare/", None, None),
    ("recitazione", "atuação", "elementi", "Ha studiato recitazione.", "Estudou atuação.", "/retʃitatˈtsjone/", "f", "recitazioni"),
    ("coprotagonista", "coprotagonista", "persone", "Il ruolo del coprotagonista.", "O papel do coprotagonista.", "/koprotaɡoˈnista/", "m/f", "coprotagonisti"),
    ("figurante", "figurante", "persone", "Lavora come figurante.", "Trabalha como figurante.", "/fiɡuˈrante/", "m/f", "figuranti"),
    ("drammaturgo", "dramaturgo", "persone", "Un famoso drammaturgo inglese.", "Um famoso dramaturgo inglês.", "/drammaˈturɡo/", "m", "drammaturghi"),
    ("scenografo", "cenógrafo", "persone", "Lo scenografo prepara la scena.", "O cenógrafo prepara a cena.", "/ʃeˈnɔɡrafo/", "m", "scenografi"),
    ("macchinista", "maquinista (teatro)", "persone", "Il macchinista teatrale.", "O maquinista teatral.", "/makkiˈnista/", "m", "macchinisti"),
    ("costumista", "figurinista", "persone", "Il costumista sceglie gli abiti.", "O figurinista escolhe as roupas.", "/kostuˈmista/", "m/f", "costumisti"),
    ("maschera", "lanterneirinho (teatro)", "persone", "Chiedi alla maschera in sala.", "Pergunte ao funcionário na sala.", "/ˈmaskera/", "f", "maschere")
]

# T30: La Letteratura e i Libri (110 parole)
t30_data = [
    ("libro", "livro", "oggetti", "Leggere un buon libro.", "Ler um bom livro.", "/ˈlibro/", "m", "libri"),
    ("romanzo", "romance (livro)", "generi", "Un romanzo d'avventura.", "Um romance de aventura.", "/roˈmandzo/", "m", "romanzi"),
    ("racconto", "conto", "generi", "Un racconto breve.", "Um conto curto.", "/rakˈkonto/", "m", "racconti"),
    ("poesia", "poesia", "generi", "Leggere una poesia.", "Ler uma poesia.", "/poeˈzia/", "f", "poesie"),
    ("saggio", "ensaio (livro)", "generi", "Un saggio filosofico.", "Um ensaio filosófico.", "/ˈsaddʒo/", "m", "saggi"),
    ("biografia", "biografia", "generi", "La biografia di un eroe.", "A biografia de um herói.", "/bjoɡraˈfia/", "f", "biografie"),
    ("autobiografia", "autobiografia", "generi", "Scrivere la propria autobiografia.", "Escrever a própria autobiografia.", "/autobjoɡraˈfia/", "f", "autobiografie"),
    ("giallo", "livro de mistério/policial", "generi", "Leggere un giallo appassionante.", "Ler um livro policial apaixonante.", "/ˈdʒallo/", "m", "gialli"),
    ("fantasy", "fantasia (gênero)", "generi", "Un libro fantasy.", "Um livro de fantasia.", "/ˈfɛntazi/", "m", "fantasy"),
    ("fumetto", "história em quadrinhos", "generi", "I bambini leggono il fumetto.", "As crianças leem histórias em quadrinhos.", "/fuˈmetto/", "m", "fumetti"),
    ("fiaba", "conto de fadas", "generi", "Una fiaba per bambini.", "Um conto de fadas para crianças.", "/ˈfjaba/", "f", "fiabe"),
    ("favola", "fábula", "generi", "La favola della volpe.", "A fábula da raposa.", "/ˈfavola/", "f", "favole"),
    ("autore", "autor", "persone", "L'autore del libro.", "O autor do livro.", "/auˈtore/", "m", "autori"),
    ("scrittore", "escritor", "persone", "Un famoso scrittore.", "Um escritor famoso.", "/skritˈtore/", "m", "scrittori"),
    ("poeta", "poeta", "persone", "Il poeta cerca ispirazione.", "O poeta busca inspiração.", "/poˈɛta/", "m", "poeti"),
    ("editore", "editor/editora", "persone", "L'editore pubblica il romanzo.", "A editora publica o romance.", "/ediˈtore/", "m", "editori"),
    ("lettore", "leitor", "persone", "Un lettore accanito.", "Um leitor assíduo.", "/letˈtore/", "m", "lettori"),
    ("protagonista", "protagonista", "persone", "Il protagonista muore alla fine.", "O protagonista morre no fim.", "/protaɡoˈnista/", "m/f", "protagonisti"),
    ("pagina", "página", "oggetti", "Gira la pagina.", "Vire a página.", "/ˈpadʒina/", "f", "pagine"),
    ("capitolo", "capítulo", "oggetti", "Il primo capitolo.", "O primeiro capítulo.", "/kaˈpitolo/", "m", "capitoli"),
    ("copertina", "capa (livro)", "oggetti", "Il libro ha una bella copertina.", "O livro tem uma bela capa.", "/koperˈtina/", "f", "copertine"),
    ("titolo", "título", "oggetti", "Il titolo dell'opera.", "O título da obra.", "/ˈtitolo/", "m", "titoli"),
    ("indice", "índice", "oggetti", "Cerca nell'indice.", "Procure no índice.", "/ˈinditʃe/", "m", "indici"),
    ("prefazione", "prefácio", "oggetti", "Leggere la prefazione.", "Ler o prefácio.", "/prefatˈtsjone/", "f", "prefazioni"),
    ("trama", "enredo", "oggetti", "La trama è complessa.", "O enredo é complexo.", "/ˈtrama/", "f", "trame"),
    ("biblioteca", "biblioteca", "luoghi", "Studiare in biblioteca.", "Estudar na biblioteca.", "/bibljoˈtɛka/", "f", "biblioteche"),
    ("libreria", "livraria", "luoghi", "Comprare un libro in libreria.", "Comprar um livro na livraria.", "/libreˈria/", "f", "librerie"),
    ("scaffale", "prateleira", "luoghi", "I libri sullo scaffale.", "Os livros na prateleira.", "/skafˈfale/", "m", "scaffali"),
    ("edizione", "edição", "oggetti", "La prima edizione.", "A primeira edição.", "/editˈtsjone/", "f", "edizioni"),
    ("pubblicazione", "publicação", "oggetti", "Data di pubblicazione.", "Data de publicação.", "/pubblikatˈtsjone/", "f", "pubblicazioni"),
    ("leggere", "ler", "verbi", "Amo leggere la sera.", "Amo ler à noite.", "/ˈlɛddʒere/", None, None),
    ("scrivere", "escrever", "verbi", "Scrivere un libro.", "Escrever um livro.", "/ˈskrivere/", None, None),
    ("pubblicare", "publicar", "verbi", "Pubblicare un articolo.", "Publicar um artigo.", "/pubbliˈkare/", None, None),
    ("sfogliare", "folhear", "verbi", "Sfogliare una rivista.", "Folhear uma revista.", "/sfoˈʎʎare/", None, None),
    ("stampare", "imprimir", "verbi", "Stampare il manoscritto.", "Imprimir o manuscrito.", "/stamˈpare/", None, None),
    ("tradurre", "traduzir", "verbi", "Tradurre dall'italiano.", "Traduzir do italiano.", "/traˈdurre/", None, None),
    ("raccontare", "contar", "verbi", "Raccontare una storia.", "Contar uma história.", "/rakkonˈtare/", None, None),
    ("recensire", "fazer resenha", "verbi", "Recensire l'ultimo libro.", "Fazer resenha do último livro.", "/retʃenˈsire/", None, None),
    ("citare", "citar", "verbi", "Citare un famoso autore.", "Citar um famoso autor.", "/tʃiˈtare/", None, None),
    ("dedicare", "dedicar", "verbi", "Dedicare il libro alla moglie.", "Dedicar o livro à esposa.", "/dediˈkare/", None, None),
    ("riassumere", "resumir", "verbi", "Riassumere il capitolo.", "Resumir o capítulo.", "/rjasˈsumere/", None, None),
    ("sottolineare", "sublinhar", "verbi", "Sottolineare le frasi importanti.", "Sublinhar as frases importantes.", "/sottolineˈare/", None, None),
    ("immaginare", "imaginar", "verbi", "Immaginare un mondo nuovo.", "Imaginar um mundo novo.", "/immadʒiˈnare/", None, None),
    ("appassionante", "apaixonante", "aggettivi", "Una storia appassionante.", "Uma história apaixonante.", "/appassjoˈnante/", "m", "appassionanti"),
    ("noioso", "chato", "aggettivi", "Un libro noioso.", "Um livro chato.", "/noˈjozo/", "m", "noiosi"),
    ("lungo", "longo", "aggettivi", "Un romanzo molto lungo.", "Um romance muito longo.", "/ˈlunɡo/", "m", "lunghi"),
    ("breve", "curto/breve", "aggettivi", "Un racconto breve.", "Um conto curto.", "/ˈbreve/", "m", "brevi"),
    ("inedito", "inédito", "aggettivi", "Un manoscritto inedito.", "Um manuscrito inédito.", "/iˈnɛdito/", "m", "inediti"),
    ("classico", "clássico", "aggettivi", "Un classico della letteratura.", "Um clássico da literatura.", "/ˈklassiko/", "m", "classici"),
    ("moderno", "moderno", "aggettivi", "Letteratura moderna.", "Literatura moderna.", "/moˈdɛrno/", "m", "moderni"),
    ("contemporaneo", "contemporâneo", "aggettivi", "Un autore contemporaneo.", "Um autor contemporâneo.", "/kontempoˈranɛo/", "m", "contemporanei"),
    ("epico", "épico", "aggettivi", "Un poema epico.", "Um poema épico.", "/ˈɛpiko/", "m", "epici"),
    ("lirico", "lírico", "aggettivi", "Un componimento lirico.", "Uma composição lírica.", "/ˈliriko/", "m", "lirici"),
    ("famoso", "famoso", "aggettivi", "Uno scrittore famoso.", "Um escritor famoso.", "/faˈmozo/", "m", "famosi"),
    ("scolastico", "escolar", "aggettivi", "Un libro scolastico.", "Um livro escolar.", "/skoˈlastiko/", "m", "scolastici"),
    ("illustrato", "ilustrado", "aggettivi", "Un libro illustrato.", "Um livro ilustrado.", "/illusˈtrato/", "m", "illustrati"),
    ("brossura", "brochura", "oggetti", "Un'edizione in brossura.", "Uma edição em brochura.", "/brosˈsura/", "f", "brossure"),
    ("rilegatura", "encadernação", "oggetti", "Una bella rilegatura.", "Uma bela encadernação.", "/rileɡaˈtura/", "f", "rilegature"),
    ("carta", "papel", "oggetti", "Stampato su carta.", "Impresso em papel.", "/ˈkarta/", "f", "carte"),
    ("inchiostro", "tinta (caneta)", "oggetti", "Scrivere con l'inchiostro.", "Escrever com tinta.", "/inˈkjɔstro/", "m", "inchiostri"),
    ("penna", "caneta", "oggetti", "Prendi una penna.", "Pegue uma caneta.", "/ˈpenna/", "f", "penne"),
    ("matita", "lápis", "oggetti", "Scrivi a matita.", "Escreva a lápis.", "/maˈtita/", "f", "matite"),
    ("segnalibro", "marcador de página", "oggetti", "Usa un segnalibro.", "Use um marcador de página.", "/seɲɲaˈlibro/", "m", "segnalibri"),
    ("dizionario", "dicionário", "oggetti", "Cerca nel dizionario.", "Procure no dicionário.", "/ditsjoˈnarjo/", "m", "dizionari"),
    ("enciclopedia", "enciclopédia", "oggetti", "L'enciclopedia italiana.", "A enciclopédia italiana.", "/entʃiklopeˈdia/", "f", "enciclopedie"),
    ("rivista", "revista", "oggetti", "Una rivista di moda.", "Uma revista de moda.", "/riˈvista/", "f", "riviste"),
    ("giornale", "jornal", "oggetti", "Leggi il giornale quotidiano.", "Leia o jornal diário.", "/dʒorˈnale/", "m", "giornali"),
    ("quotidiano", "diário (jornal)", "oggetti", "Un quotidiano nazionale.", "Um diário nacional.", "/kwotiˈdjano/", "m", "quotidiani"),
    ("periodico", "periódico", "oggetti", "Una rivista periodica.", "Uma revista periódica.", "/peˈrjɔdiko/", "m", "periodici"),
    ("articolo", "artigo", "oggetti", "Un articolo interessante.", "Um artigo interessante.", "/arˈtikolo/", "m", "articoli"),
    ("manoscritto", "manuscrito", "oggetti", "Un antico manoscritto.", "Um antigo manuscrito.", "/manosˈkritto/", "m", "manoscritti"),
    ("bozza", "rascunho/esboço", "oggetti", "La prima bozza del testo.", "O primeiro rascunho do texto.", "/ˈbɔttsa/", "f", "bozze"),
    ("stampa", "imprensa/impressão", "oggetti", "Andare in stampa.", "Ir para a impressão.", "/ˈstampa/", "f", "stampe"),
    ("tiratura", "tiragem", "oggetti", "Una tiratura limitata.", "Uma tiragem limitada.", "/tiraˈtura/", "f", "tirature"),
    ("prosa", "prosa", "generi", "Scrivere in prosa.", "Escrever em prosa.", "/ˈprɔza/", "f", "prose"),
    ("verso", "verso", "generi", "Scrivere in versi.", "Escrever em versos.", "/ˈvɛrso/", "m", "versi"),
    ("rima", "rima", "generi", "Una poesia in rima.", "Uma poesia com rima.", "/ˈrima/", "f", "rime"),
    ("sillaba", "sílaba", "generi", "Contare le sillabe.", "Contar as sílabas.", "/ˈsillaba/", "f", "sillabe"),
    ("frase", "frase", "generi", "Una frase lunga.", "Uma frase longa.", "/ˈfraze/", "f", "frasi"),
    ("parola", "palavra", "generi", "Non trovo la parola.", "Não encontro a palavra.", "/paˈrɔla/", "f", "parole"),
    ("vocabolario", "vocabulário", "oggetti", "Ampliare il vocabolario.", "Ampliar o vocabulário.", "/vokaboˈlarjo/", "m", "vocabolari"),
    ("traduttore", "tradutor", "persone", "Il traduttore del romanzo.", "O tradutor do romance.", "/tradutˈtore/", "m", "traduttori"),
    ("illustratore", "ilustrador", "persone", "L'illustratore del libro.", "O ilustrador do livro.", "/illusˈtratore/", "m", "illustratori"),
    ("rilegatore", "encadernador", "persone", "Il rilegatore artigiano.", "O encadernador artesão.", "/rileɡaˈtore/", "m", "rilegatori"),
    ("critica", "crítica", "concetti", "Una critica letteraria.", "Uma crítica literária.", "/ˈkritika/", "f", "critiche"),
    ("ispirazione", "inspiração", "concetti", "Cercare l'ispirazione.", "Buscar a inspiração.", "/ispiratˈtsjone/", "f", "ispirazioni"),
    ("stile", "estilo", "concetti", "Lo stile dell'autore.", "O estilo do autor.", "/ˈstile/", "m", "stili"),
    ("corrente", "corrente (literária)", "concetti", "Una corrente letteraria.", "Uma corrente literária.", "/korˈrɛnte/", "f", "correnti"),
    ("movimento", "movimento (cultural)", "concetti", "Il movimento romantico.", "O movimento romântico.", "/moviˈmento/", "m", "movimenti"),
    ("capolavoro", "obra-prima", "oggetti", "Il capolavoro di Dante.", "A obra-prima de Dante.", "/kapolaˈvoro/", "m", "capolavori"),
    ("best seller", "best seller", "oggetti", "È diventato un best seller.", "Tornou-se um best seller.", "/bɛst ˈsɛller/", "m", "best seller"),
    ("pseudonimo", "pseudônimo", "concetti", "Scrive con uno pseudonimo.", "Escreve com um pseudônimo.", "/pseuˈdɔnimo/", "m", "pseudonimi"),
    ("dedica", "dedicatória", "concetti", "Una dedica speciale.", "Uma dedicatória especial.", "/ˈdɛdika/", "f", "dediche"),
    ("epilogo", "epílogo", "concetti", "L'epilogo della storia.", "O epílogo da história.", "/eˈpiloɡo/", "m", "epiloghi"),
    ("prologo", "prólogo", "concetti", "Il prologo è misterioso.", "O prólogo é misterioso.", "/ˈprɔloɡo/", "m", "prologhi"),
    ("dialogo", "diálogo", "concetti", "Un dialogo brillante.", "Um diálogo brilhante.", "/diˈaloɡo/", "m", "dialoghi"),
    ("monologo", "monólogo", "concetti", "Il monologo interiore.", "O monólogo interior.", "/moˈnɔloɡo/", "m", "monologhi"),
    ("metafora", "metáfora", "concetti", "Usare una metafora.", "Usar uma metáfora.", "/meˈtafora/", "f", "metafore"),
    ("ironia", "ironia", "concetti", "Una sottile ironia.", "Uma sutil ironia.", "/iroˈnia/", "f", "ironie"),
    ("suspense", "suspense", "concetti", "Un momento di grande suspense.", "Um momento de grande suspense.", "/ˈsaspɛns/", "f", "suspense"),
    ("finale", "final", "concetti", "Il finale a sorpresa.", "O final surpreendente.", "/fiˈnale/", "m", "finali")
]

# T31: La Scienza e la Ricerca (110 parole)
t31_data = [
    ("scienza", "ciência", "concetti", "La scienza fa progressi.", "A ciência faz progressi.", "/ˈʃɛntsa/", "f", "scienze"),
    ("ricerca", "pesquisa", "concetti", "La ricerca scientifica.", "A pesquisa científica.", "/riˈtʃerka/", "f", "ricerche"),
    ("scienziato", "cientista", "persone", "Un famoso scienziato.", "Um famoso cientista.", "/ʃenˈtsjato/", "m", "scienziati"),
    ("ricercatore", "pesquisador", "persone", "Il ricercatore lavora in laboratorio.", "O pesquisador trabalha no laboratório.", "/ritʃerkaˈtore/", "m", "ricercatori"),
    ("laboratorio", "laboratório", "luoghi", "Un laboratorio chimico.", "Um laboratório químico.", "/laboraˈtɔrjo/", "m", "laboratori"),
    ("esperimento", "experimento", "concetti", "Fare un esperimento.", "Fazer um experimento.", "/esperiˈmento/", "m", "esperimenti"),
    ("teoria", "teoria", "concetti", "La teoria della relatività.", "A teoria da relatividade.", "/teoˈria/", "f", "teorie"),
    ("ipotesi", "hipótese", "concetti", "Formulare un'ipotesi.", "Formular uma hipótese.", "/iˈpɔtezi/", "f", "ipotesi"),
    ("scoperta", "descoberta", "concetti", "Una scoperta sensazionale.", "Uma descoberta sensacional.", "/skoˈpɛrta/", "f", "scoperte"),
    ("invenzione", "invenção", "concetti", "L'invenzione del telefono.", "A invenção do telefone.", "/inventˈtsjone/", "f", "invenzioni"),
    ("fisica", "física", "discipline", "Studiare la fisica.", "Estudar a física.", "/ˈfizika/", "f", "fisiche"),
    ("chimica", "química", "discipline", "La chimica organica.", "A química orgânica.", "/ˈkimika/", "f", "chimiche"),
    ("biologia", "biologia", "discipline", "La biologia marina.", "A biologia marinha.", "/bjoloˈdʒia/", "f", "biologie"),
    ("astronomia", "astronomia", "discipline", "L'astronomia osserva le stelle.", "A astronomia observa as estrelas.", "/astronoˈmia/", "f", "astronomie"),
    ("matematica", "matemática", "discipline", "Un problema di matematica.", "Um problema de matemática.", "/mateˈmatika/", "f", "matematiche"),
    ("medicina", "medicina", "discipline", "La facoltà di medicina.", "A faculdade de medicina.", "/mediˈtʃina/", "f", "medicine"),
    ("genetica", "genética", "discipline", "La genetica studia il DNA.", "A genética estuda o DNA.", "/dʒeˈnɛtika/", "f", "genetiche"),
    ("tecnologia", "tecnologia", "discipline", "La nuova tecnologia.", "A nova tecnologia.", "/teknoloˈdʒia/", "f", "tecnologie"),
    ("ingegneria", "engenharia", "discipline", "L'ingegneria civile.", "A engenharia civil.", "/indʒeɲɲeˈria/", "f", "ingegnerie"),
    ("microscopio", "microscópio", "strumenti", "Guardare al microscopio.", "Olhar no microscópio.", "/mikroˈskɔpjo/", "m", "microscopi"),
    ("telescopio", "telescópio", "strumenti", "Il telescopio spaziale.", "O telescópio espacial.", "/telesˈkɔpjo/", "m", "telescopi"),
    ("atomo", "átomo", "elementi", "L'atomo è minuscolo.", "O átomo é minúsculo.", "/ˈatomo/", "m", "atomi"),
    ("molecola", "molécula", "elementi", "Una molecola d'acqua.", "Uma molécula de água.", "/moˈlɛkola/", "f", "molecole"),
    ("cellula", "célula", "elementi", "Una cellula animale.", "Uma célula animal.", "/ˈtʃɛllula/", "f", "cellule"),
    ("pianeta", "planeta", "elementi", "Il pianeta Marte.", "O planeta Marte.", "/pjaˈneta/", "m", "pianeti"),
    ("stella", "estrela", "elementi", "Una stella luminosa.", "Uma estrela luminosa.", "/ˈstella/", "f", "stelle"),
    ("galassia", "galáxia", "elementi", "La nostra galassia.", "A nossa galáxia.", "/ɡaˈlassja/", "f", "galassie"),
    ("gravità", "gravidade", "elementi", "La forza di gravità.", "A força da gravidade.", "/ɡraviˈta/", "f", "gravità"),
    ("energia", "energia", "elementi", "L'energia solare.", "A energia solar.", "/enerˈdʒia/", "f", "energie"),
    ("velocità", "velocidade", "elementi", "La velocità della luce.", "A velocidade da luz.", "/velotʃiˈta/", "f", "velocità"),
    ("massa", "massa", "elementi", "Massa ed energia.", "Massa e energia.", "/ˈmassa/", "f", "masse"),
    ("volume", "volume", "elementi", "Misurare il volume.", "Medir o volume.", "/voˈlume/", "m", "volumi"),
    ("temperatura", "temperatura", "elementi", "La temperatura sale.", "A temperatura sobe.", "/temperaˈtura/", "f", "temperature"),
    ("pressione", "pressão", "elementi", "La pressione atmosferica.", "A pressão atmosférica.", "/presˈsjone/", "f", "pressioni"),
    ("formula", "fórmula", "concetti", "La formula chimica.", "A fórmula química.", "/ˈfɔrmula/", "f", "formule"),
    ("equazione", "equação", "concetti", "Risolvere un'equazione.", "Resolver uma equação.", "/ekwatˈtsjone/", "f", "equazioni"),
    ("teorema", "teorema", "concetti", "Il teorema di Pitagora.", "O teorema de Pitágoras.", "/teoˈrɛma/", "m", "teoremi"),
    ("dati", "dados", "concetti", "Raccogliere i dati.", "Coletar os dados.", "/ˈdati/", "m", "dati"),
    ("risultato", "resultado", "concetti", "Il risultato dell'analisi.", "O resultado da análise.", "/rizulˈtato/", "m", "risultati"),
    ("analisi", "análise", "concetti", "Un'analisi dettagliata.", "Uma análise detalhada.", "/aˈnalizi/", "f", "analisi"),
    ("osservazione", "observação", "concetti", "L'osservazione dei fenomeni.", "A observação dos fenômenos.", "/osservatˈtsjone/", "f", "osservazioni"),
    ("fenomeno", "fenômeno", "concetti", "Un fenomeno naturale.", "Um fenômeno natural.", "/feˈnɔmeno/", "m", "fenomeni"),
    ("batterio", "bactéria", "elementi", "Un batterio resistente.", "Uma bactéria resistente.", "/batˈtɛrjo/", "m", "batteri"),
    ("virus", "vírus", "elementi", "Il virus influenzale.", "O vírus da gripe.", "/ˈvirus/", "m", "virus"),
    ("vaccino", "vacina", "elementi", "Un nuovo vaccino.", "Uma nova vacina.", "/vatˈtʃino/", "m", "vaccini"),
    ("malattia", "doença", "elementi", "Curare una malattia.", "Curar uma doença.", "/malatˈtia/", "f", "malattie"),
    ("cura", "cura/tratamento", "concetti", "Cercare una cura.", "Buscar uma cura.", "/ˈkura/", "f", "cure"),
    ("medicina", "remédio", "elementi", "Prendi la medicina.", "Tome o remédio.", "/mediˈtʃina/", "f", "medicine"),
    ("genio", "gênio", "persone", "Un genio della matematica.", "Um gênio da matemática.", "/ˈdʒɛnjo/", "m", "geni"),
    ("evoluzione", "evolução", "concetti", "La teoria dell'evoluzione.", "A teoria da evolução.", "/evolutˈtsjone/", "f", "evoluzioni"),
    ("specie", "espécie", "elementi", "Una specie in via di estinzione.", "Uma espécie em vias de extinção.", "/ˈspɛtʃe/", "f", "specie"),
    ("ambiente", "meio ambiente", "elementi", "Proteggere l'ambiente.", "Proteger o meio ambiente.", "/amˈbjɛnte/", "m", "ambienti"),
    ("clima", "clima", "elementi", "Il cambiamento del clima.", "A mudança climática.", "/ˈklima/", "m", "climi"),
    ("spazio", "espaço", "elementi", "Viaggio nello spazio.", "Viagem no espaço.", "/ˈspattsjo/", "m", "spazi"),
    ("orbita", "órbita", "elementi", "Entrare in orbita.", "Entrar em órbita.", "/ˈɔrbita/", "f", "orbite"),
    ("satellite", "satélite", "elementi", "Il satellite artificiale.", "O satélite artificial.", "/saˈtɛllite/", "m", "satelliti"),
    ("razzo", "foguete", "elementi", "Il razzo decolla.", "O foguete decola.", "/ˈraddzo/", "m", "razzi"),
    ("astronauta", "astronauta", "persone", "L'astronauta sulla luna.", "O astronauta na lua.", "/astroˈnauta/", "m/f", "astronauti"),
    ("calcolo", "cálculo", "concetti", "Un calcolo esatto.", "Um cálculo exato.", "/ˈkalkolo/", "m", "calcoli"),
    ("misura", "medida", "concetti", "Prendere le misure.", "Tirar as medidas.", "/miˈzura/", "f", "misure"),
    ("peso", "peso", "elementi", "Il peso della materia.", "O peso da matéria.", "/ˈpezo/", "m", "pesi"),
    ("lunghezza", "comprimento", "elementi", "La lunghezza d'onda.", "O comprimento de onda.", "/lunˈɡhettsa/", "f", "lunghezze"),
    ("distanza", "distância", "elementi", "La distanza tra i pianeti.", "A distância entre os planetas.", "/disˈtantsa/", "f", "distanze"),
    ("ricercare", "pesquisar", "verbi", "Ricercare nuove soluzioni.", "Pesquisar novas soluções.", "/ritʃerˈkare/", None, None),
    ("scoprire", "descobrir", "verbi", "Scoprire un pianeta.", "Descobrir um planeta.", "/skoˈprire/", None, None),
    ("inventare", "inventar", "verbi", "Inventare una macchina.", "Inventar uma máquina.", "/invenˈtare/", None, None),
    ("osservare", "observar", "verbi", "Osservare le stelle.", "Observar as estrelas.", "/osserˈvare/", None, None),
    ("analizzare", "analisar", "verbi", "Analizzare i dati.", "Analisar os dados.", "/analidˈdzare/", None, None),
    ("dimostrare", "demonstrar", "verbi", "Dimostrare il teorema.", "Demonstrar o teorema.", "/dimosˈtrare/", None, None),
    ("calcolare", "calcular", "verbi", "Calcolare l'area.", "Calcular a área.", "/kalkoˈlare/", None, None),
    ("misurare", "medir", "verbi", "Misurare la temperatura.", "Medir a temperatura.", "/mizuˈrare/", None, None),
    ("pubblicare", "publicar", "verbi", "Pubblicare i risultati.", "Publicar os resultados.", "/pubbliˈkare/", None, None),
    ("sperimentare", "experimentar", "verbi", "Sperimentare in laboratorio.", "Experimentar no laboratório.", "/sperimenˈtare/", None, None),
    ("sviluppare", "desenvolver", "verbi", "Sviluppare un software.", "Desenvolver um software.", "/zvilupˈpare/", None, None),
    ("brevettare", "patentear", "verbi", "Brevettare un'idea.", "Patentear uma ideia.", "/brevetˈtare/", None, None),
    ("guarire", "curar", "verbi", "Guarire dalla malattia.", "Curar-se da doença.", "/ɡwaˈrire/", None, None),
    ("inquinare", "poluir", "verbi", "Inquinare l'aria.", "Poluir o ar.", "/inkwiˈnare/", None, None),
    ("proteggere", "proteger", "verbi", "Proteggere la natura.", "Proteger a natureza.", "/proˈtɛddʒere/", None, None),
    ("scientifico", "científico", "aggettivi", "Il metodo scientifico.", "O método científico.", "/ʃenˈtifiko/", "m", "scientifici"),
    ("tecnologico", "tecnológico", "aggettivi", "Progresso tecnologico.", "Progresso tecnológico.", "/teknoˈlɔdʒiko/", "m", "tecnologici"),
    ("chimico", "químico", "aggettivi", "Reazione chimica.", "Reação química.", "/ˈkimiko/", "m", "chimici"),
    ("fisico", "físico", "aggettivi", "Stato fisico.", "Estado físico.", "/ˈfiziko/", "m", "fisici"),
    ("biologico", "biológico", "aggettivi", "Cibo biologico.", "Comida orgânica.", "/bjoˈlɔdʒiko/", "m", "biologici"),
    ("genetico", "genético", "aggettivi", "Patrimonio genetico.", "Patrimônio genético.", "/dʒeˈnɛtiko/", "m", "genetici"),
    ("esatto", "exato", "aggettivi", "Un calcolo esatto.", "Um cálculo exato.", "/eˈzatto/", "m", "esatti"),
    ("preciso", "preciso", "aggettivi", "Uno strumento preciso.", "Um instrumento preciso.", "/preˈtʃizo/", "m", "precisi"),
    ("sbagliato", "errado", "aggettivi", "Il risultato è sbagliato.", "O resultado está errado.", "/zbaˈʎʎato/", "m", "sbagliati"),
    ("vero", "verdadeiro", "aggettivi", "Questo è vero.", "Isto é verdadeiro.", "/ˈvero/", "m", "veri"),
    ("falso", "falso", "aggettivi", "Un mito falso.", "Um mito falso.", "/ˈfalso/", "m", "falsi"),
    ("naturale", "natural", "aggettivi", "Un fenomeno naturale.", "Um fenômeno natural.", "/natuˈrale/", "m", "naturali"),
    ("artificiale", "artificial", "aggettivi", "Intelligenza artificiale.", "Inteligência artificial.", "/artifiˈtʃale/", "m", "artificiali"),
    ("complesso", "complexo", "aggettivi", "Un sistema complesso.", "Um sistema complexo.", "/komˈplɛsso/", "m", "complessi"),
    ("semplice", "simples", "aggettivi", "Una spiegazione semplice.", "Uma explicação simples.", "/ˈsemplitʃe/", "m", "semplici"),
    ("moderno", "moderno", "aggettivi", "Un laboratorio moderno.", "Um laboratório moderno.", "/moˈdɛrno/", "m", "moderni"),
    ("avanzato", "avançado", "aggettivi", "Stato avanzato di ricerca.", "Estado avançado de pesquisa.", "/avanˈtsato/", "m", "avanzati"),
    ("empirico", "empírico", "aggettivi", "Un dato empirico.", "Um dado empírico.", "/emˈpiriko/", "m", "empirici"),
    ("teorico", "teórico", "aggettivi", "Un approccio teorico.", "Uma abordagem teórica.", "/teˈɔriko/", "m", "teorici"),
    ("pratico", "prático", "aggettivi", "Un esempio pratico.", "Um exemplo prático.", "/ˈpratiko/", "m", "pratici"),
    ("universale", "universal", "aggettivi", "Legge universale.", "Lei universal.", "/univerˈsale/", "m", "universali"),
    ("oggettivo", "objetivo", "aggettivi", "Un dato oggettivo.", "Um dado objetivo.", "/oddʒetˈtivo/", "m", "oggettivi"),
    ("soggettivo", "subjetivo", "aggettivi", "Un parere soggettivo.", "Uma opinião subjetiva.", "/soddʒetˈtivo/", "m", "soggettivi")
]

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
    # Append words to previous temples
    append_to_existing(27, t27_add)
    append_to_existing(28, t28_add)
    append_to_existing(29, t29_add)
    
    # Create new temples T30 and T31
    create_new(30, "La Letteratura e i Libri", "Bologna", "B2", t30_data)
    create_new(31, "La Scienza e la Ricerca", "Pisa", "B2", t31_data)
