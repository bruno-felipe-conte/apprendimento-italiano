#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def w(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {
        "id": tid, "italiano": it, "portugues": pt, "genero": gen, "plural": pl,
        "exemplo": ex_it, "exemplo_pt": ex_pt, "categoria": cat, "dificuldade": "medio", "audio_ipa": ipa
    }

t19_add = [
    ("bigliettaio", "bilheteiro", "viaggio", "Il bigliettaio controlla i biglietti.", "O bilheteiro verifica as passagens.", "/biʎʎetˈtajo/", "m", "bigliettai"),
    ("conducente", "condutor", "viaggio", "Parla con il conducente.", "Fale com o condutor.", "/konduˈtʃɛnte/", "m", "conducenti"),
    ("autista", "motorista", "viaggio", "L'autista dell'autobus.", "O motorista do ônibus.", "/auˈtista/", "m", "autisti"),
    ("pilota", "piloto", "viaggio", "Il pilota guida l'aereo.", "O piloto guia o avião.", "/piˈlɔta/", "m", "piloti"),
    ("passeggera", "passageira", "viaggio", "Una passeggera è scesa.", "Uma passageira desceu.", "/passeidˈdʒɛra/", "f", "passeggere"),
    ("cabina", "cabine", "veicoli", "La cabina di pilotaggio.", "A cabine de pilotagem.", "/kaˈbina/", "f", "cabine"),
    ("vagone", "vagão", "veicoli", "Il terzo vagone del treno.", "O terceiro vagão do trem.", "/vaˈɡone/", "m", "vagoni"),
    ("locomotiva", "locomotiva", "veicoli", "La vecchia locomotiva a vapore.", "A velha locomotiva a vapor.", "/lokomoˈtiva/", "f", "locomotive"),
    ("capotreno", "chefe de trem", "viaggio", "Il capotreno fischia.", "O chefe do trem apita.", "/kapoˈtrɛno/", "m", "capitreno"),
    ("hostess", "aeromoça", "viaggio", "L'hostess serve le bevande.", "A aeromoça serve as bebidas.", "/ˈɔstess/", "f", "hostess"),
    ("steward", "comissário", "viaggio", "Lo steward aiuta i passeggeri.", "O comissário ajuda os passageiros.", "/ˈstjuard/", "m", "steward")
]

t20_add = [
    ("polpaccio", "panturrilha", "inferiori", "Un crampo al polpaccio.", "Uma cãibra na panturrilha.", "/polˈpattʃo/", "m", "polpacci"),
    ("natica", "nádega", "tronco", "Un dolore alla natica.", "Uma dor na nádega.", "/ˈnatika/", "f", "natiche"),
    ("sedere", "traseiro", "tronco", "Cadere sul sedere.", "Cair de traseiro.", "/seˈdere/", "m", "sederi"),
    ("anca", "quadril", "tronco", "Frattura dell'anca.", "Fratura do quadril.", "/ˈanka/", "f", "anche"),
    ("costola", "costela", "interni", "Una costola rotta.", "Uma costela quebrata.", "/ˈkɔstola/", "f", "costole"),
    ("spina dorsale", "coluna vertebral", "interni", "Un problema alla spina dorsale.", "Um problema na coluna vertebral.", "/ˈspina dorˈsale/", "f", "spine dorsali"),
    ("teschio", "crânio", "interni", "Il teschio protegge il cervello.", "O crânio protege o cérebro.", "/ˈteskjo/", "m", "teschi"),
    ("palato", "palato", "testa", "Il palato superiore.", "O palato superior.", "/paˈlato/", "m", "palati"),
    ("gengiva", "gengiva", "testa", "Una gengiva infiammata.", "Uma gengiva inflamata.", "/dʒenˈdʒiva/", "f", "gengive"),
    ("narice", "narina", "testa", "Respirare da una narice.", "Respirar por uma narina.", "/naˈritʃe/", "f", "narici"),
    ("pupilla", "pupila", "testa", "La pupilla si dilata.", "A pupila se dilata.", "/puˈpilla/", "f", "pupille"),
    ("palpebra", "pálpebra", "testa", "Una palpebra gonfia.", "Uma pálpebra inchada.", "/ˈpalpebra/", "f", "palpebre"),
    ("iride", "íris", "testa", "L'iride verde dell'occhio.", "A íris verde do olho.", "/ˈiride/", "f", "iridi"),
    ("midollo", "medula", "interni", "Il midollo osseo.", "A medula óssea.", "/miˈdollo/", "m", "midolli"),
    ("arteria", "artéria", "interni", "Un'arteria principale.", "Uma artéria principal.", "/arˈtɛrja/", "f", "arterie"),
    ("ghiandola", "glândula", "interni", "Una ghiandola ingrossata.", "Uma glândula aumentada.", "/ˈɡjandola/", "f", "ghiandole"),
    ("sudorazione", "sudorese", "condizioni", "Forte sudorazione notturna.", "Forte sudorese noturna.", "/sudoratˈtsjone/", "f", "sudorazioni"),
    ("digestione", "digestão", "condizioni", "Una digestione lenta.", "Uma digestão lenta.", "/didʒesˈtjone/", "f", "digestioni"),
    ("circolazione", "circulação", "condizioni", "La circolazione sanguigna.", "A circulação sanguínea.", "/tʃirkolatˈtsjone/", "f", "circolazioni"),
    ("ormone", "hormônio", "interni", "Un ormone della crescita.", "Um hormônio do crescimento.", "/orˈmone/", "m", "ormoni"),
    ("cartilagine", "cartilagem", "interni", "La cartilagine del ginocchio.", "A cartilagem do joelho.", "/kartiˈladʒine/", "f", "cartilagini"),
    ("metabolismo", "metabolismo", "condizioni", "Avere un metabolismo veloce.", "Ter um metabolismo rápido.", "/metaboˈlizmo/", "m", "metabolismi")
]

t21_add = [
    ("antipatia", "antipatia", "negative", "Provo antipatia per lui.", "Sinto antipatia por ele.", "/antipaˈtia/", "f", "antipatie"),
    ("empatia", "empatia", "positive", "Ha una grande empatia.", "Tem uma grande empatia.", "/empaˈtia/", "f", "empatie"),
    ("apatia", "apatia", "negative", "Uno stato di completa apatia.", "Um estado de completa apatia.", "/apaˈtia/", "f", "apatie"),
    ("esaltazione", "exaltação", "positive", "L'esaltazione della vittoria.", "A exaltação da vitória.", "/ezaltatˈtsjone/", "f", "esaltazioni"),
    ("euforia", "euforia", "positive", "Un senso di euforia.", "Uma sensação de euforia.", "/eufoˈria/", "f", "euforie"),
    ("estasi", "êxtase", "positive", "Ascoltare in estasi.", "Escutar em êxtase.", "/ˈɛstazi/", "f", "estasi"),
    ("ottimismo", "otimismo", "positive", "Affrontare con ottimismo.", "Enfrentar com otimismo.", "/ottiˈmizmo/", "m", "ottimismi"),
    ("pessimismo", "pessimismo", "negative", "Un generale pessimismo.", "Um pessimismo geral.", "/pessiˈmizmo/", "m", "pessimismi"),
    ("compassione", "compaixão", "positive", "Provare compassione per i deboli.", "Sentir compaixão pelos fracos.", "/kompasˈsjone/", "f", "compassioni"),
    ("pietà", "piedade", "positive", "Abbi pietà di noi.", "Tenha piedade de nós.", "/pjeˈta/", "f", "pietà"),
    ("afflizione", "aflição", "negative", "Causa grande afflizione.", "Causa grande aflição.", "/afflitˈtsjone/", "f", "afflizioni"),
    ("tormento", "tormento", "negative", "Un tormento continuo.", "Um tormento contínuo.", "/torˈmento/", "m", "tormenti"),
    ("inquietudine", "inquietação", "negative", "Sento un'inquietudine profonda.", "Sinto uma inquietação profunda.", "/inkwjeˈtudine/", "f", "inquietudini"),
    ("spavento", "susto", "negative", "Che grande spavento!", "Que grande susto!", "/spaˈvɛnto/", "m", "spaventi"),
    ("orrore", "horror", "negative", "Film dell'orrore.", "Filme de horror.", "/orˈrore/", "m", "orrori"),
    ("disgusto", "desgosto", "negative", "Guardare con disgusto.", "Olhar com desgosto.", "/dizˈɡusto/", "m", "disgusti"),
    ("ripugnanza", "repugnância", "negative", "Una forte ripugnanza.", "Uma forte repugnância.", "/ripuɲˈɲantsa/", "f", "ripugnanze"),
    ("disprezzo", "desprezo", "negative", "Mostrare disprezzo.", "Mostrar desprezo.", "/disˈprɛttso/", "m", "disprezzi"),
    ("stima", "estima", "positive", "Ho molta stima di te.", "Tenho muita estima por você.", "/ˈstima/", "f", "stime"),
    ("ammirazione", "admiração", "positive", "Guarda con ammirazione.", "Olha com admiração.", "/ammiratˈtsjone/", "f", "ammirazioni"),
    ("indifferenza", "indiferença", "negative", "L'indifferenza totale.", "A indiferença total.", "/indiffeˈrɛntsa/", "f", "indifferenze"),
    ("esitazione", "hesitação", "negative", "Parlare senza esitazione.", "Falar sem hesitação.", "/ezitatˈtsjone/", "f", "esitazioni"),
    ("dubbio", "dúvida", "negative", "Ho un piccolo dubbio.", "Tenho uma pequena dúvida.", "/ˈdubbjo/", "m", "dubbi"),
    ("certezza", "certeza", "positive", "Avere la certezza assoluta.", "Ter a certeza absoluta.", "/tʃerˈtettsa/", "f", "certezze"),
    ("audacia", "audácia", "positive", "Mostrare grande audacia.", "Mostrar grande audácia.", "/auˈdatʃa/", "f", "audacie"),
    ("viltà", "covardia", "negative", "Un atto di viltà.", "Um ato de covardia.", "/vilˈta/", "f", "viltà"),
    ("codardia", "covardia", "negative", "Accusato di codardia.", "Acusado de covardia.", "/kodarˈdia/", "f", "codardie"),
    ("smarrimento", "perplexidade", "negative", "Un senso di smarrimento.", "Uma sensação de perplexidade.", "/zmarriˈmento/", "m", "smarrimenti"),
    ("perplessità", "perplexidade", "negative", "Esprimo la mia perplessità.", "Expresso a minha perplexidade.", "/perplessiˈta/", "f", "perplessità"),
    ("fascinazione", "fascinação", "positive", "Una forte fascinazione.", "Uma forte fascinação.", "/faʃʃinatˈtsjone/", "f", "fascinazioni"),
    ("soggezione", "sujeição", "negative", "Mettere in soggezione.", "Deixar intimidado.", "/soddʒetˈtsjone/", "f", "soggezioni")
]

# T22: La Natura e le Stagioni (110 words)
t22_data = [
    # Stagioni e Tempo
    ("primavera", "primavera", "stagioni", "La primavera porta i fiori.", "A primavera traz as flores.", "/primaˈvɛra/", "f", "primavere"),
    ("estate", "verão", "stagioni", "In estate fa caldo.", "No verão faz calor.", "/esˈtate/", "f", "estati"),
    ("autunno", "outono", "stagioni", "In autunno cadono le foglie.", "No outono as folhas caem.", "/auˈtunno/", "m", "autunni"),
    ("inverno", "inverno", "stagioni", "L'inverno è molto freddo.", "O inverno é muito frio.", "/inˈvɛrno/", "m", "inverni"),
    ("clima", "clima", "tempo", "Il clima mediterraneo.", "O clima mediterrâneo.", "/ˈklima/", "m", "climi"),
    ("tempo", "tempo/clima", "tempo", "Che tempo fa oggi?", "Como está o tempo hoje?", "/ˈtɛmpo/", "m", "tempi"),
    ("caldo", "calor", "tempo", "Oggi fa un caldo terribile.", "Hoje faz um calor terrível.", "/ˈkaldo/", "m", "caldi"),
    ("freddo", "frio", "tempo", "Fa troppo freddo per uscire.", "Faz muito frio para sair.", "/ˈfreddo/", "m", "freddi"),
    ("pioggia", "chuva", "tempo", "La pioggia non smette.", "A chuva não para.", "/ˈpjɔddʒa/", "f", "piogge"),
    ("neve", "neve", "tempo", "I bambini giocano con la neve.", "As crianças brincam com a neve.", "/ˈneve/", "f", "nevi"),
    ("vento", "vento", "tempo", "C'è un vento forte.", "Há um vento forte.", "/ˈvɛnto/", "m", "venti"),
    ("nebbia", "névoa", "tempo", "A Milano c'è spesso la nebbia.", "Em Milão há frequentemente névoa.", "/ˈnebbja/", "f", "nebbie"),
    ("tempesta", "tempestade", "tempo", "Una forte tempesta in mare.", "Uma forte tempestade no mar.", "/temˈpɛsta/", "f", "tempeste"),
    ("fulmine", "raio", "tempo", "Ho visto un fulmine.", "Vi um raio.", "/ˈfulmine/", "m", "fulmini"),
    ("tuono", "trovão", "tempo", "Il rumore del tuono.", "O barulho do trovão.", "/ˈtwɔno/", "m", "tuoni"),
    ("nuvola", "nuvem", "tempo", "Una nuvola bianca nel cielo.", "Uma nuvem branca no céu.", "/ˈnuvola/", "f", "nuvole"),
    ("sole", "sol", "tempo", "Il sole splende oggi.", "O sol brilha hoje.", "/ˈsole/", "m", "soli"),
    ("luna", "lua", "tempo", "La luna piena stanotte.", "A lua cheia esta noite.", "/ˈluna/", "f", "lune"),
    ("stella", "estrela", "tempo", "Una stella cadente.", "Uma estrela cadente.", "/ˈstella/", "f", "stelle"),
    ("cielo", "céu", "tempo", "Il cielo è azzurro.", "O céu é azul.", "/ˈtʃɛlo/", "m", "cieli"),
    
    # Paesaggio e Geografia
    ("natura", "natureza", "paesaggio", "Amo stare in mezzo alla natura.", "Amo ficar no meio da natureza.", "/naˈtura/", "f", "nature"),
    ("albero", "árvore", "paesaggio", "Un grande albero nel parco.", "Una grande árvore no parque.", "/ˈalbero/", "m", "alberi"),
    ("fiore", "flor", "paesaggio", "Un fiore rosso profumato.", "Uma flor vermelha perfumada.", "/ˈfjore/", "m", "fiori"),
    ("foglia", "folha", "paesaggio", "Una foglia secca.", "Uma folha seca.", "/ˈfɔʎʎa/", "f", "foglie"),
    ("fiume", "rio", "paesaggio", "Il fiume scorre veloce.", "O rio corre rápido.", "/ˈfjume/", "m", "fiumi"),
    ("lago", "lago", "paesaggio", "Andiamo in vacanza al lago.", "Vamos passar férias no lago.", "/ˈlaɡo/", "m", "laghi"),
    ("mare", "mar", "paesaggio", "Nuotare nel mare.", "Nadar no mar.", "/ˈmare/", "m", "mari"),
    ("oceano", "oceano", "paesaggio", "L'Oceano Atlantico.", "O Oceano Atlântico.", "/oˈtʃɛano/", "m", "oceani"),
    ("spiaggia", "praia", "paesaggio", "Prendere il sole in spiaggia.", "Tomar sol na praia.", "/ˈspjaddʒa/", "f", "spiagge"),
    ("sabbia", "areia", "paesaggio", "Costruire castelli di sabbia.", "Construir castelos de areia.", "/ˈsabbja/", "f", "sabbie"),
    ("montagna", "montanha", "paesaggio", "Scalare la montagna.", "Escalar a montanha.", "/monˈtaɲɲa/", "f", "montagne"),
    ("collina", "colina", "paesaggio", "Una verde collina.", "Uma verde colina.", "/kolˈlina/", "f", "colline"),
    ("valle", "vale", "paesaggio", "La valle è profonda.", "O vale é profundo.", "/ˈvalle/", "f", "valli"),
    ("bosco", "bosque", "paesaggio", "Passeggiare nel bosco.", "Passear no bosque.", "/ˈbɔsko/", "m", "boschi"),
    ("foresta", "floresta", "paesaggio", "Gli animali della foresta.", "Os animais da floresta.", "/foˈrɛsta/", "f", "foreste"),
    ("prato", "prado", "paesaggio", "Correre sul prato verde.", "Correr no prado verde.", "/ˈprato/", "m", "prati"),
    ("erba", "grama", "paesaggio", "L'erba è ancora bagnata.", "A grama ainda está molhada.", "/ˈɛrba/", "f", "erbe"),
    ("pianta", "planta", "paesaggio", "Annaffiare le piante.", "Regar as plantas.", "/ˈpjanta/", "f", "piante"),
    ("radice", "raiz", "paesaggio", "Le radici dell'albero.", "As raízes da árvore.", "/raˈditʃe/", "f", "radici"),
    ("tronco", "tronco", "paesaggio", "Il tronco è molto spesso.", "O tronco é muito grosso.", "/ˈtronko/", "m", "tronchi"),
    ("ramo", "ramo", "paesaggio", "Un uccello sul ramo.", "Um pássaro no ramo.", "/ˈramo/", "m", "rami"),
    ("sasso", "pedra", "paesaggio", "Lanciare un sasso nell'acqua.", "Jogar uma pedra na água.", "/ˈsasso/", "m", "sassi"),
    ("roccia", "rocha", "paesaggio", "Arrampicarsi sulla roccia.", "Escalar na rocha.", "/ˈrɔttʃa/", "f", "rocce"),
    ("terra", "terra", "paesaggio", "La terra è fertile.", "A terra é fértil.", "/ˈtɛrra/", "f", "terre"),
    ("isola", "ilha", "paesaggio", "Un'isola deserta.", "Uma ilha deserta.", "/ˈizola/", "f", "isole"),
    ("costa", "litoral", "paesaggio", "La costa italiana.", "O litoral italiano.", "/ˈkɔsta/", "f", "coste"),
    ("onda", "onda", "paesaggio", "Le onde sono alte.", "As ondas estão altas.", "/ˈonda/", "f", "onde"),
    ("deserto", "deserto", "paesaggio", "Un cammello nel deserto.", "Um camelo no deserto.", "/deˈzɛrto/", "m", "deserti"),
    ("giungla", "selva", "paesaggio", "La giungla amazzonica.", "A selva amazônica.", "/ˈdʒunɡla/", "f", "giungle"),
    ("pianura", "planície", "paesaggio", "La pianura padana.", "A planície padana.", "/pjaˈnura/", "f", "pianure"),
    
    # Azioni ed espressioni (20)
    ("sbocciare", "desabrochar", "verbi", "I fiori sbocciano in primavera.", "As flores desabrocham na primavera.", "/zbotˈtʃare/", None, None),
    ("appassire", "murchar", "verbi", "Il fiore sta appassendo.", "A flor está murchando.", "/appasˈsire/", None, None),
    ("crescere", "crescer", "verbi", "L'albero cresce in fretta.", "A árvore cresce rápido.", "/ˈkreʃʃere/", None, None),
    ("piantare", "plantar", "verbi", "Piantare un seme.", "Plantar uma semente.", "/pjanˈtare/", None, None),
    ("raccogliere", "colher", "verbi", "Raccogliere i frutti.", "Colher os frutos.", "/rakˈkɔʎʎere/", None, None),
    ("innaffiare", "regar", "verbi", "Innaffiare le rose.", "Regar as rosas.", "/innafˈfjare/", None, None),
    ("piovere", "chover", "verbi", "Oggi piove molto.", "Hoje chove muito.", "/ˈpjɔvere/", None, None),
    ("nevicare", "nevar", "verbi", "In montagna nevica.", "Na montanha neva.", "/neviˈkare/", None, None),
    ("soffiare", "soprar", "verbi", "Il vento soffia forte.", "O vento sopra forte.", "/sofˈfjare/", None, None),
    ("gelare", "gelar", "verbi", "L'acqua del lago è gelata.", "A água do lago congelou.", "/dʒeˈlare/", None, None),
    ("scongelare", "descongelar", "verbi", "Il ghiaccio si scongela.", "O gelo se descongela.", "/skondʒeˈlare/", None, None),
    ("scorrere", "correr (água)", "verbi", "L'acqua scorre veloce.", "A água corre rápido.", "/ˈskorrere/", None, None),
    ("tramontare", "pôr-se", "verbi", "Il sole tramonta tardi.", "O sol se põe tarde.", "/tramonˈtare/", None, None),
    ("sorgere", "surgir/nascer", "verbi", "Il sole sorge all'alba.", "O sol nasce ao amanhecer.", "/ˈsordʒere/", None, None),
    ("splendere", "brilhar", "verbi", "Il sole splende nel cielo.", "O sol brilha no céu.", "/ˈsplɛndere/", None, None),
    ("nuotare", "nadar", "verbi", "Nuotare nel fiume.", "Nadar no rio.", "/nwoˈtare/", None, None),
    ("passeggiare", "passear", "verbi", "Passeggiare nel bosco.", "Passear no bosque.", "/passedˈdʒare/", None, None),
    ("arrampicare", "escalar", "verbi", "Arrampicare sulla roccia.", "Escalar a rocha.", "/arrampiˈkare/", None, None),
    ("respirare", "respirar", "verbi", "Respirare aria pulita.", "Respirar ar limpo.", "/respiˈrare/", None, None),
    ("godere", "desfrutar", "verbi", "Godere del bel tempo.", "Desfrutar do bom tempo.", "/ɡoˈdere/", None, None),
    
    # Aggettivi e altri fenomeni
    ("sereno", "sereno", "aggettivi", "Il cielo oggi è sereno.", "O céu hoje está sereno.", "/seˈreno/", "m", "sereni"),
    ("nuvoloso", "nublado", "aggettivi", "Il tempo è nuvoloso.", "O tempo está nublado.", "/nuvoˈlozo/", "m", "nuvolosi"),
    ("piovoso", "chuvoso", "aggettivi", "Un giorno molto piovoso.", "Um dia muito chuvoso.", "/pjoˈvozo/", "m", "piovosi"),
    ("secco", "seco", "aggettivi", "Un clima arido e secco.", "Um clima árido e seco.", "/ˈsekko/", "m", "secchi"),
    ("umido", "úmido", "aggettivi", "Fa caldo e molto umido.", "Faz calor e é muito úmido.", "/ˈumido/", "m", "umidi"),
    ("soleggiato", "ensolarado", "aggettivi", "Un pomeriggio soleggiato.", "Uma tarde ensolarada.", "/soledˈdʒato/", "m", "soleggiati"),
    ("selvaggio", "selvagem", "aggettivi", "La natura selvaggia.", "A natureza selvagem.", "/selˈvaddʒo/", "m", "selvaggi"),
    ("naturale", "natural", "aggettivi", "Un parco naturale.", "Um parque natural.", "/natuˈrale/", "m", "naturali"),
    ("artificiale", "artificial", "aggettivi", "Un lago artificiale.", "Um lago artificial.", "/artifiˈtʃale/", "m", "artificiali"),
    ("incontaminato", "intocado", "aggettivi", "Un bosco incontaminato.", "Um bosque intocado.", "/inkontamiˈnato/", "m", "incontaminati"),
    ("alba", "amanhecer", "tempo", "Alzarsi all'alba.", "Levantar ao amanhecer.", "/ˈalba/", "f", "albe"),
    ("tramonto", "pôr do sol", "tempo", "Un bellissimo tramonto.", "Um belíssimo pôr do sol.", "/traˈmonto/", "m", "tramonti"),
    ("crepuscolo", "crepúsculo", "tempo", "La luce del crepuscolo.", "A luz do crepúsculo.", "/kreˈpuskolo/", "m", "crepuscoli"),
    ("terremoto", "terremoto", "fenomeni", "Un forte terremoto.", "Um forte terremoto.", "/terreˈmɔto/", "m", "terremoti"),
    ("vulcano", "vulcão", "paesaggio", "Il vulcano è attivo.", "O vulcão está ativo.", "/vulˈkano/", "m", "vulcani"),
    ("eruzione", "erupção", "fenomeni", "Un'eruzione vulcanica.", "Uma erupção vulcânica.", "/erutˈtsjone/", "f", "eruzioni"),
    ("ghiacciaio", "geleira", "paesaggio", "Il ghiacciaio si sta sciogliendo.", "A geleira está derretendo.", "/ɡjatˈtʃajo/", "m", "ghiacciai"),
    ("cascata", "cachoeira", "paesaggio", "Una cascata altissima.", "Uma cachoeira altíssima.", "/kasˈkata/", "f", "cascate"),
    ("grotta", "caverna", "paesaggio", "Esplorare una grotta.", "Explorar uma caverna.", "/ˈɡrɔtta/", "f", "grotte"),
    ("canyon", "cânion", "paesaggio", "Un canyon profondo.", "Um cânion profundo.", "/ˈkɛnjon/", "m", "canyon"),
    ("rugiada", "orvalho", "fenomeni", "La rugiada del mattino.", "O orvalho da manhã.", "/ruˈdʒada/", "f", "rugiade"),
    ("brina", "geada", "fenomeni", "I campi coperti di brina.", "Os campos cobertos de geada.", "/ˈbrina/", "f", "brine"),
    ("grandine", "granizo", "fenomeni", "È caduta molta grandine.", "Caiu muito granizo.", "/ˈɡrandine/", "f", "grandini"),
    ("arcobaleno", "arco-íris", "fenomeni", "Un arcobaleno nel cielo.", "Um arco-íris no céu.", "/arkobaˈleno/", "m", "arcobaleni"),
    ("orizzonte", "horizonte", "paesaggio", "Guardare verso l'orizzonte.", "Olhar para o horizonte.", "/oridˈdzonte/", "m", "orizzonti"),
    ("profumo", "perfume", "natura", "Il profumo dei fiori.", "O perfume das flores.", "/proˈfumo/", "m", "profumi"),
    ("ombra", "sombra", "natura", "Riposare all'ombra.", "Descansar na sombra.", "/ˈombra/", "f", "ombre"),
    ("rifugio", "refúgio", "paesaggio", "Un rifugio in montagna.", "Um refúgio na montanha.", "/riˈfudʒo/", "m", "rifugi"),
    ("sentiero", "trilha", "paesaggio", "Seguire il sentiero.", "Seguir a trilha.", "/senˈtjɛro/", "m", "sentieri"),
    ("cima", "cume", "paesaggio", "Raggiungere la cima.", "Alcançar o cume.", "/ˈtʃima/", "f", "cime"),
    ("valanga", "avalanche", "fenomeni", "Pericolo di valanga.", "Perigo de avalanche.", "/vaˈlanɡa/", "f", "valanghe"),
    ("frana", "deslizamento", "fenomeni", "Una frana ha bloccato la strada.", "Um deslizamento bloqueou a rua.", "/ˈfrana/", "f", "frane"),
    ("pianeta", "planeta", "natura", "Il pianeta Terra.", "O planeta Terra.", "/pjaˈneta/", "m", "pianeti"),
    ("universo", "universo", "natura", "L'universo è immenso.", "O universo é imenso.", "/uniˈvɛrso/", "m", "universi"),
    ("ambiente", "meio ambiente", "natura", "Rispettiamo l'ambiente.", "Respeitamos o meio ambiente.", "/amˈbjɛnte/", "m", "ambienti"),
    ("ecologia", "ecologia", "natura", "Studia l'ecologia.", "Estuda ecologia.", "/ekoloˈdʒia/", "f", "ecologie"),
    ("inquinamento", "poluição", "natura", "Combattere l'inquinamento.", "Combater a poluição.", "/inkwinaˈmento/", "m", "inquinamenti"),
    ("sostenibile", "sustentável", "aggettivi", "Energia sostenibile.", "Energia sustentável.", "/sosteˈnibile/", "m", "sostenibili"),
    ("riciclo", "reciclagem", "natura", "Il riciclo della plastica.", "A reciclagem do plástico.", "/riˈtʃiklo/", "m", "ricicli"),
    ("risparmio", "economia", "natura", "Il risparmio energetico.", "A economia de energia.", "/riˈsparmjo/", "m", "risparmi")
]

# T23: Gli Animali (110 words)
t23_data = [
    # Domestici
    ("cane", "cachorro", "domestici", "Il mio cane abbaia spesso.", "O meu cachorro late frequentemente.", "/ˈkane/", "m", "cani"),
    ("gatto", "gato", "domestici", "Il gatto dorme sul divano.", "O gato dorme no sofá.", "/ˈɡatto/", "m", "gatti"),
    ("cavallo", "cavalo", "domestici", "Cavalcare un bel cavallo.", "Cavalgar um belo cavalo.", "/kaˈvallo/", "m", "cavalli"),
    ("mucca", "vaca", "fattoria", "La mucca produce latte.", "A vaca produz leite.", "/ˈmukka/", "f", "mucche"),
    ("pecora", "ovelha", "fattoria", "Il gregge di pecore.", "O rebanho de ovelhas.", "/ˈpɛkora/", "f", "pecore"),
    ("maiale", "porco", "fattoria", "Il maiale mangia molto.", "O porco come muito.", "/maˈjale/", "m", "maiali"),
    ("gallina", "galinha", "fattoria", "La gallina fa le uova.", "A galinha põe ovos.", "/ɡalˈlina/", "f", "galline"),
    ("pollo", "frango", "fattoria", "Il pollo ruspante.", "O frango caipira.", "/ˈpollo/", "m", "polli"),
    ("gallo", "galo", "fattoria", "Il gallo canta all'alba.", "O galo canta ao amanhecer.", "/ˈɡallo/", "m", "galli"),
    ("anatra", "pato", "fattoria", "L'anatra nuota nel lago.", "O pato nada no lago.", "/ˈanatra/", "f", "anatre"),
    ("oca", "ganso", "fattoria", "Un'oca bianca.", "Um ganso branco.", "/ˈɔka/", "f", "oche"),
    ("coniglio", "coelho", "domestici", "Il coniglio mangia la carota.", "O coelho come a cenoura.", "/koˈniʎʎo/", "m", "conigli"),
    ("asino", "burro", "fattoria", "L'asino è testardo.", "O burro é teimoso.", "/ˈazino/", "m", "asini"),
    ("capra", "cabra", "fattoria", "La capra salta sulle rocce.", "A cabra salta nas pedras.", "/ˈkapra/", "f", "capre"),
    
    # Uccelli
    ("uccello", "pássaro", "uccelli", "L'uccello vola nel cielo.", "O pássaro voa no céu.", "/utˈtʃɛllo/", "m", "uccelli"),
    ("piccione", "pombo", "uccelli", "Un piccione in piazza.", "Um pombo na praça.", "/pitˈtʃone/", "m", "piccioni"),
    ("aquila", "águia", "uccelli", "L'aquila vola in alto.", "A águia voa alto.", "/ˈakwila/", "f", "aquile"),
    ("falco", "falcão", "uccelli", "Il falco caccia la preda.", "O falcão caça a presa.", "/ˈfalko/", "m", "falchi"),
    ("gufo", "coruja", "uccelli", "Il gufo è un animale notturno.", "A coruja é um animal noturno.", "/ˈɡufo/", "m", "gufi"),
    ("rondine", "andorinha", "uccelli", "Una rondine non fa primavera.", "Uma andorinha só não faz primavera.", "/ˈrondine/", "f", "rondini"),
    ("gabbiano", "gaivota", "uccelli", "Il gabbiano sul mare.", "A gaivota sobre o mar.", "/ɡabˈbjano/", "m", "gabbiani"),
    ("pappagallo", "papagaio", "uccelli", "Il pappagallo colorato.", "O papagaio colorido.", "/pappaˈɡallo/", "m", "pappagalli"),
    ("pavone", "pavão", "uccelli", "Il pavone fa la ruota.", "O pavão abre a cauda.", "/paˈvone/", "m", "pavoni"),
    ("pinguino", "pinguim", "uccelli", "Il pinguino vive al freddo.", "O pinguim vive no frio.", "/pinˈɡwino/", "m", "pinguini"),
    ("struzzo", "avestruz", "uccelli", "Lo struzzo corre veloce.", "O avestruz corre rápido.", "/ˈstruttso/", "m", "struzzi"),
    
    # Selvatici
    ("leone", "leão", "selvatici", "Il leone è il re della foresta.", "O leão é o rei da selva.", "/leˈone/", "m", "leoni"),
    ("tigre", "tigre", "selvatici", "La tigre ha le strisce.", "O tigre tem listras.", "/ˈtiɡre/", "f", "tigri"),
    ("orso", "urso", "selvatici", "L'orso dorme in inverno.", "O urso dorme no inverno.", "/ˈorso/", "m", "orsi"),
    ("lupo", "lobo", "selvatici", "Il lupo ulula alla luna.", "O lobo uiva para a lua.", "/ˈlupo/", "m", "lupi"),
    ("elefante", "elefante", "selvatici", "L'elefante ha una grande proboscide.", "O elefante tem uma grande tromba.", "/eleˈfante/", "m", "elefanti"),
    ("scimmia", "macaco", "selvatici", "La scimmia mangia la banana.", "O macaco come a banana.", "/ˈʃimmja/", "f", "scimmie"),
    ("giraffa", "girafa", "selvatici", "La giraffa ha un collo lungo.", "A girafa tem um pescoço longo.", "/dʒiˈraffa/", "f", "giraffe"),
    ("zebra", "zebra", "selvatici", "La zebra è bianca e nera.", "A zebra é branca e preta.", "/ˈdzɛbra/", "f", "zebre"),
    ("ippopotamo", "hipopótamo", "selvatici", "L'ippopotamo vive nell'acqua.", "O hipopótamo vive na água.", "/ippoˈpɔtamo/", "m", "ippopotami"),
    ("rinoceronte", "rinoceronte", "selvatici", "Il rinoceronte ha un corno.", "O rinoceronte tem um chifre.", "/rinotʃeˈronte/", "m", "rinoceronti"),
    ("canguro", "canguru", "selvatici", "Il canguro salta molto in alto.", "O canguru salta muito alto.", "/kanˈɡuro/", "m", "canguri"),
    ("cammello", "camelo", "selvatici", "Il cammello nel deserto.", "O camelo no deserto.", "/kamˈmɛllo/", "m", "cammelli"),
    ("cervo", "cervo", "selvatici", "Il cervo nel bosco.", "O cervo no bosque.", "/ˈtʃɛrvo/", "m", "cervi"),
    ("volpe", "raposa", "selvatici", "La volpe è furba.", "A raposa é esperta.", "/ˈvolpe/", "f", "volpi"),
    ("scoiattolo", "esquilo", "selvatici", "Lo scoiattolo mangia le noci.", "O esquilo come as nozes.", "/skoiˈjattolo/", "m", "scoiattoli"),
    ("tartaruga", "tartaruga", "selvatici", "La tartaruga è molto lenta.", "A tartaruga é muito lenta.", "/tartaˈruɡa/", "f", "tartarughe"),
    ("rana", "sapo/rã", "selvatici", "La rana salta nello stagno.", "A rã salta no lago.", "/ˈrana/", "f", "rane"),
    ("serpente", "cobra", "selvatici", "Il serpente velenoso.", "A cobra venenosa.", "/serˈpɛnte/", "m", "serpenti"),
    ("lucertola", "lagartixa", "selvatici", "La lucertola al sole.", "A lagartixa ao sol.", "/luˈtʃɛrtola/", "f", "lucertole"),
    ("coccodrillo", "crocodilo", "selvatici", "Il coccodrillo nel fiume.", "O crocodilo no rio.", "/kokkoˈdrillo/", "m", "coccodrilli"),
    ("pipistrello", "morcego", "selvatici", "Il pipistrello vola di notte.", "O morcego voa de noite.", "/pipisˈtrɛllo/", "m", "pipistrelli"),
    ("topo", "rato", "selvatici", "Il topo scappa dal gatto.", "O rato foge do gato.", "/ˈtɔpo/", "m", "topi"),
    
    # Insetti e Piccoli
    ("insetto", "inseto", "insetti", "Un insetto fastidioso.", "Um inseto chato.", "/inˈsɛtto/", "m", "insetti"),
    ("mosca", "mosca", "insetti", "Una mosca vola in cucina.", "Uma mosca voa na cozinha.", "/ˈmoska/", "f", "mosche"),
    ("zanzara", "mosquito", "insetti", "La zanzara punge di notte.", "O mosquito pica de noite.", "/dzanˈdzara/", "f", "zanzare"),
    ("ape", "abelha", "insetti", "L'ape produce il miele.", "A abelha produz o mel.", "/ˈape/", "f", "api"),
    ("formica", "formiga", "insetti", "La formica lavora molto.", "A formiga trabalha muito.", "/forˈmika/", "f", "formiche"),
    ("farfalla", "borboleta", "insetti", "Una bellissima farfalla.", "Uma belíssima borboleta.", "/farˈfalla/", "f", "farfalle"),
    ("ragno", "aranha", "insetti", "Il ragno fa la ragnatela.", "A aranha faz a teia.", "/ˈraɲɲo/", "m", "ragni"),
    ("scorpione", "escorpião", "insetti", "Lo scorpione nel deserto.", "O escorpião no deserto.", "/skorˈpjone/", "m", "scorpioni"),
    ("lumaca", "caracol", "insetti", "La lumaca lascia la scia.", "O caracol deixa um rastro.", "/luˈmaka/", "f", "lumache"),
    ("verme", "verme", "insetti", "Il verme nella terra.", "O verme na terra.", "/ˈvɛrme/", "m", "vermi"),
    ("bruco", "lagarta", "insetti", "Il bruco diventa farfalla.", "A lagarta vira borboleta.", "/ˈbruko/", "m", "bruchi"),
    ("grillo", "grilo", "insetti", "Il grillo canta d'estate.", "O grilo canta no verão.", "/ˈɡrillo/", "m", "grilli"),
    ("scarabeo", "besouro", "insetti", "Uno scarabeo verde.", "Um besouro verde.", "/skaraˈbɛo/", "m", "scarabei"),
    ("coccinella", "joaninha", "insetti", "La coccinella porta fortuna.", "A joaninha traz sorte.", "/kottʃiˈnɛlla/", "f", "coccinelle"),
    
    # Marini
    ("pesce", "peixe", "marini", "Il pesce nuota nell'acqua.", "O peixe nada na água.", "/ˈpeʃʃe/", "m", "pesci"),
    ("squalo", "tubarão", "marini", "Lo squalo è pericoloso.", "O tubarão é perigoso.", "/ˈskwalo/", "m", "squali"),
    ("delfino", "golfinho", "marini", "Il delfino salta tra le onde.", "O golfinho salta nas ondas.", "/delˈfino/", "m", "delfini"),
    ("balena", "baleia", "marini", "La balena è enorme.", "A baleia é enorme.", "/baˈlena/", "f", "balene"),
    ("granchio", "caranguejo", "marini", "Il granchio cammina di lato.", "O caranguejo anda de lado.", "/ˈɡrankjo/", "m", "granchi"),
    ("polpo", "polvo", "marini", "Il polpo ha otto tentacoli.", "O polvo tem oito tentáculos.", "/ˈpolpo/", "m", "polpi"),
    ("medusa", "água-viva", "marini", "Attento alla medusa.", "Cuidado com a água-viva.", "/meˈduza/", "f", "meduse"),
    ("stella marina", "estrela-do-mar", "marini", "Una stella marina sulla spiaggia.", "Uma estrela-do-mar na praia.", "/ˈstella maˈrina/", "f", "stelle marine"),
    ("cavalluccio marino", "cavalo-marinho", "marini", "Un piccolo cavalluccio marino.", "Um pequeno cavalo-marinho.", "/kavalˈluttʃo maˈrino/", "m", "cavallucci marini"),
    ("foca", "foca", "marini", "La foca gioca con la palla.", "A foca brinca com a bola.", "/ˈfɔka/", "f", "foche"),
    
    # Corpo Animale e Verbi
    ("zampa", "pata", "anatomia", "Il cane ha quattro zampe.", "O cachorro tem quatro patas.", "/ˈtsampa/", "f", "zampe"),
    ("coda", "cauda/rabo", "anatomia", "Il gatto muove la coda.", "O gato mexe o rabo.", "/ˈkoda/", "f", "code"),
    ("pelo", "pelo", "anatomia", "Il pelo del cane è morbido.", "O pelo do cachorro é macio.", "/ˈpelo/", "m", "peli"),
    ("ala", "asa", "anatomia", "L'uccello apre le ali.", "O pássaro abre as asas.", "/ˈala/", "f", "ali"),
    ("piuma", "pena", "anatomia", "Un cuscino di piume.", "Um travesseiro de penas.", "/ˈpjuma/", "f", "piume"),
    ("becco", "bico", "anatomia", "Il becco dell'uccello.", "O bico do pássaro.", "/ˈbekko/", "m", "becchi"),
    ("corno", "chifre", "anatomia", "Il toro ha le corna.", "O touro tem chifres.", "/ˈkɔrno/", "m", "corna"),
    ("artiglio", "garra", "anatomia", "L'aquila ha artigli affilati.", "A águia tem garras afiadas.", "/arˈtiʎʎo/", "m", "artigli"),
    ("squama", "escama", "anatomia", "Le squame del pesce.", "As escamas do peixe.", "/ˈskwama/", "f", "squame"),
    ("cucciolo", "filhote", "anatomia", "Un cucciolo di leone.", "Um filhote de leão.", "/ˈkuttʃolo/", "m", "cuccioli"),
    ("nido", "ninho", "anatomia", "L'uccello fa il nido.", "O pássaro faz o ninho.", "/ˈnido/", "m", "nidi"),
    ("tana", "toca", "anatomia", "La volpe nella tana.", "A raposa na toca.", "/ˈtana/", "f", "tane"),
    ("gabbia", "gaiola", "anatomia", "Il pappagallo è in gabbia.", "O papagaio está na gaiola.", "/ˈɡabbja/", "f", "gabbie"),
    ("abbaiare", "latir", "verbi", "Il cane abbaia forte.", "O cachorro late alto.", "/abbajˈjare/", None, None),
    ("miagolare", "miar", "verbi", "Il gatto miagola per la fame.", "O gato mia de fome.", "/mjaɡoˈlare/", None, None),
    ("mordere", "morder", "verbi", "Attento, il cane può mordere.", "Cuidado, o cachorro pode morder.", "/ˈmɔrdere/", None, None),
    ("graffiare", "arranhar", "verbi", "Il gatto mi ha graffiato.", "O gato me arranhou.", "/ɡrafˈfjare/", None, None),
    ("volare", "voar", "verbi", "L'aquila vola nel cielo.", "A águia voa no céu.", "/voˈlare/", None, None),
    ("strisciare", "rastejar", "verbi", "Il serpente striscia a terra.", "A cobra rasteja no chão.", "/striʃˈʃare/", None, None),
    ("nuotare", "nadar", "verbi", "Il pesce nuota nel mare.", "O peixe nada no mar.", "/nwoˈtare/", None, None),
    ("galoppare", "galopar", "verbi", "Il cavallo galoppa nel prato.", "O cavalo galopa no prado.", "/ɡalopˈpare/", None, None),
    ("addestrare", "adestrar", "verbi", "Addestrare un cane.", "Adestrar um cachorro.", "/addesˈtrare/", None, None),
    ("cacciare", "caçar", "verbi", "Il leone caccia la preda.", "O leão caça a presa.", "/katˈtʃare/", None, None)
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
    # 1. Append missing words to T19, T20, T21 to reach ~110
    append_to_existing(19, t19_add)
    append_to_existing(20, t20_add)
    append_to_existing(21, t21_add)
    
    # 2. Create T22 and T23 entirely
    create_new(22, "La Natura e le Stagioni", "Torino", "A2", t22_data)
    create_new(23, "Gli Animali", "Palermo", "A2", t23_data)
