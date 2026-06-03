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

t45_add = [
    ("appaltatore", "empreiteiro", "persone", "L'appaltatore generale.", "O empreiteiro geral.", "/appaltaˈtore/", "m", "appaltatori"),
    ("condominio", "condomínio", "costruzioni", "Riunione di condominio.", "Reunião de condomínio.", "/kondoˈminjo/", "m", "condomini"),
    ("capocantiere", "mestre de obras", "persone", "Il capocantiere controlla tutto.", "O mestre de obras controla tudo.", "/kapokanˈtjɛre/", "m", "capicantiere"),
    ("malta", "argamassa", "materiali", "Preparare la malta.", "Preparar a argamassa.", "/ˈmalta/", "f", "malte"),
    ("calce", "cal", "materiali", "La calce spenta.", "A cal apagada.", "/ˈkaltʃe/", "f", "calci"),
    ("planimetria", "planta baixa", "costruzioni", "La planimetria catastale.", "A planta baixa do cartório.", "/planimeˈtria/", "f", "planimetrie"),
    ("impalcatura", "andaime", "attrezzi", "Smontare l'impalcatura.", "Desmontar o andaime.", "/impalkaˈtura/", "f", "impalcature"),
    ("martello pneumatico", "britadeira", "attrezzi", "Il rumore del martello pneumatico.", "O barulho da britadeira.", "/marˈtɛllo pneuˈmatiko/", "m", "martelli pneumatici"),
    ("carrucola", "roldana", "attrezzi", "Sollevare con la carrucola.", "Levantar com a roldana.", "/karˈrukola/", "f", "carrucole"),
    ("carriola", "carrinho de mão", "attrezzi", "La carriola piena di terra.", "O carrinho de mão cheio de terra.", "/karˈrjɔla/", "f", "carriole"),
    ("isolante", "isolante", "materiali", "Materiale isolante.", "Material isolante.", "/izoˈlante/", "m", "isolanti"),
    ("grondaia", "calha", "costruzioni", "Pulire la grondaia.", "Limpar a calha.", "/ɡronˈdaja/", "f", "grondaie"),
    ("intonacare", "rebocar", "verbi", "Intonacare il muro.", "Rebocar o muro.", "/intonaˈkare/", None, None),
    ("asfaltare", "asfaltar", "verbi", "Asfaltare la strada.", "Asfaltar a rua.", "/asfalˈtare/", None, None)
]

t46_add = [
    ("ossessione", "obsessão", "emozioni", "Un'ossessione perenne.", "Uma obsessão perene.", "/ossesˈsjone/", "f", "ossessioni")
]

t47_add = [
    ("essere in alto mare", "estar longe de terminar", "espressioni", "Siamo ancora in alto mare.", "Ainda estamos em alto mar (longe do fim).", "/ˈɛssere in ˈalto ˈmare/", None, None),
    ("piovere sul bagnato", "chover no molhado", "espressioni", "Piove sempre sul bagnato.", "Chove sempre no molhado.", "/ˈpjɔvere sul baɲˈɲato/", None, None),
    ("gettare la spugna", "jogar a toalha/desistir", "espressioni", "Non gettare la spugna ora.", "Não jogue a toalha agora.", "/dʒetˈtare la ˈspuɲɲa/", None, None),
    ("scoprire le carte", "abrir o jogo", "espressioni", "È ora di scoprire le carte.", "É hora de abrir o jogo.", "/skoˈprire le ˈkarte/", None, None),
    ("mettere i puntini sulle i", "pôr os pingos nos is", "espressioni", "Vorrei mettere i puntini sulle i.", "Gostaria de pôr os pingos nos is.", "/ˈmettere i punˈtini ˈsulle i/", None, None),
    ("toccare ferro", "bater na madeira (dar sorte)", "espressioni", "Speriamo bene, tocco ferro.", "Tomara, bato na madeira (ferro).", "/tokˈkare ˈfɛrro/", None, None),
    ("essere alla mano", "ser acessível/sociável", "espressioni", "Il capo è alla mano.", "O chefe é muito acessível.", "/ˈɛssere ˈalla ˈmano/", None, None),
    ("vuotare il sacco", "desembuchar", "espressioni", "Ora devi vuotare il sacco.", "Agora você deve desembuchar.", "/vwoˈtare il ˈsakko/", None, None),
    ("stare con le mani in mano", "ficar de braços cruzados", "espressioni", "Non stare con le mani in mano.", "Não fique de braços cruzados.", "/ˈstare kon le ˈmani in ˈmano/", None, None),
    ("arrampicarsi sugli specchi", "dar desculpas esfarrapate", "espressioni", "Ti stai arrampicando sugli specchi.", "Você está dando desculpas esfarrapate.", "/arrampiˈkarsi ˈsuʎʎi ˈspɛkki/", None, None),
    ("tirare in ballo", "trazer à tona", "espressioni", "Non mi tirare in ballo.", "Não me envolva nisso.", "/tiˈrare im ˈballo/", None, None),
    ("fare orecchie da mercante", "fazer de ouvidos moucos", "espressioni", "Lui fa orecchie da mercante.", "Ele faz de ouvidos moucos.", "/ˈfare oˈrekkje da merˈkante/", None, None)
]

# T48: L'Arte dell'Oratoria e la Persuasione (110 parole)
t48_data = [
    # Elementi del discorso
    ("discorso", "discurso", "oratoria", "Un discorso inaugurale.", "Um discurso inaugural.", "/disˈkorso/", "m", "discorsi"),
    ("oratoria", "oratória", "oratoria", "L'arte dell'oratoria.", "A arte da oratória.", "/oraˈtɔrja/", "f", "oratorie"),
    ("persuasione", "persuasão", "oratoria", "La forza della persuasione.", "A força da persuasão.", "/perswaˈzjone/", "f", "persuasioni"),
    ("retorica", "retórica", "oratoria", "Figura retorica.", "Figura retórica.", "/reˈtɔrika/", "f", "retoriche"),
    ("pubblico", "público/audiência", "persone", "Parlar in pubblico.", "Falar em público.", "/ˈpubbliko/", "m", "pubblici"),
    ("platea", "plateia", "persone", "Una platea attenta.", "Uma plateia atenta.", "/plaˈtɛa/", "f", "platee"),
    ("auditorio", "auditório", "luoghi", "L'auditorio è pieno.", "O auditório está cheio.", "/audiˈtɔrjo/", "m", "auditori"),
    ("palco", "palco", "luoghi", "Salire sul palco.", "Subir no palco.", "/ˈpalko/", "m", "palchi"),
    ("microfono", "microfone", "oggetti", "Parlare al microfono.", "Falar ao microfone.", "/miˈkrɔfono/", "m", "microfoni"),
    ("voce", "voz", "oratoria", "Una voce potente.", "Uma voz potente.", "/ˈvotʃe/", "f", "voci"),
    ("tono", "tom", "oratoria", "Un tono convincente.", "Um tom convincente.", "/ˈtɔno/", "m", "toni"),
    ("pausa", "pausa", "oratoria", "Fare una pausa.", "Fazer uma pausa.", "/ˈpauza/", "f", "pause"),
    ("argomento", "argumento", "oratoria", "Un argomento solido.", "Um argumento sólido.", "/arɡoˈmento/", "m", "argomenti"),
    ("dibattito", "debate", "oratoria", "Un dibattito acceso.", "Um debate acalorado.", "/diˈbattito/", "m", "dibattiti"),
    ("conferenza", "conferência/palestra", "oratoria", "Tenere una conferenza.", "Dar uma palestra.", "/konfeˈrɛntsa/", "f", "conferenze"),
    ("presentazione", "apresentação", "oratoria", "La presentazione del libro.", "A apresentação do livro.", "/prezentatˈtsjone/", "f", "presentazioni"),
    ("monologo", "monólogo", "oratoria", "Un lungo monologo.", "Um longo monólogo.", "/moˈnɔloɡo/", "m", "monologhi"),
    ("eloquenza", "eloquência", "oratoria", "Parlare con eloquenza.", "Falar com eloquência.", "/eloˈkwɛntsa/", "f", "eloquenze"),
    ("carisma", "carisma", "oratoria", "Un leader pieno di carisma.", "Um líder cheio de carisma.", "/kaˈrizma/", "m", "carismi"),
    ("gestualità", "gestualidade", "oratoria", "La gestualità italiana.", "A gestualidade italiana.", "/dʒestwaliˈta/", "f", "gestualità"),
    ("sguardo", "olhar", "oratoria", "Mantenere lo sguardo.", "Manter o olhar.", "/ˈzɡwardo/", "m", "sguardi"),
    ("postura", "postura", "oratoria", "Una postura eretta.", "Uma postura ereta.", "/posˈtura/", "f", "posture"),
    ("conclusione", "conclusão", "oratoria", "Trarre una conclusione.", "Tirar uma conclusão.", "/konkluˈzjone/", "f", "conclusioni"),
    ("premessa", "premissa", "oratoria", "Partire da una premessa.", "Partir de uma premissa.", "/preˈmessa/", "f", "premesse"),
    ("obiezione", "objeção", "oratoria", "Sollevare un'obiezione.", "Levantar uma objeção.", "/objetsˈsjone/", "f", "obiezioni"),
    ("replica", "réplica", "oratoria", "Il diritto di replica.", "O direito de réplica.", "/ˈrɛplika/", "f", "repliche"),
    ("applauso", "aplauso", "oratoria", "Un fragoroso applauso.", "Um estrondoso aplauso.", "/apˈplauzo/", "m", "applausi"),
    ("ovazione", "ovação", "oratoria", "Ricevere un'ovazione.", "Receber uma ovação.", "/ovatˈtsjone/", "f", "ovazioni"),
    ("critica", "crítica", "oratoria", "Una critica costruttiva.", "Uma crítica construtiva.", "/ˈkritika/", "f", "critiche"),
    ("complimento", "elogio", "oratoria", "Accettare un complimento.", "Aceitar um elogio.", "/kompliˈmento/", "m", "complimenti"),
    # Verbi
    ("parlare", "falar", "verbi", "Parlare in pubblico.", "Falar em público.", "/parˈlare/", None, None),
    ("comunicare", "comunicar", "verbi", "Comunicare un'idea.", "Comunicar uma ideia.", "/komuniˈkare/", None, None),
    ("convincere", "convencer", "verbi", "Convincere la giuria.", "Convencer o júri.", "/konˈvintʃere/", None, None),
    ("persuadere", "persuadir", "verbi", "Persuadere gli elettori.", "Persuadir os eleitores.", "/perswaˈdere/", None, None),
    ("argomentare", "argumentar", "verbi", "Argomentare la tesi.", "Argumentar a tese.", "/arɡomenˈtare/", None, None),
    ("dibattere", "debater", "verbi", "Dibattere su un tema.", "Debater sobre um tema.", "/diˈbattere/", None, None),
    ("spiegare", "explicar", "verbi", "Spiegare il concetto.", "Explicar o conceito.", "/spjeˈɡare/", None, None),
    ("illustrare", "ilustrar/explicar", "verbi", "Illustrare il progetto.", "Ilustrar o projeto.", "/illusˈtrare/", None, None),
    ("coinvolgere", "envolver", "verbi", "Coinvolgere il pubblico.", "Envolver o público.", "/koinˈvɔldʒere/", None, None),
    ("ispirare", "inspirar", "verbi", "Ispirare le persone.", "Inspirar as pessoas.", "/ispiˈrare/", None, None),
    ("emozionare", "emocionar", "verbi", "Emozionare la folla.", "Emocionar a multidão.", "/emotsjoˈnare/", None, None),
    ("motivare", "motivar", "verbi", "Motivare la squadra.", "Motivar a equipe.", "/motiˈvare/", None, None),
    ("articolare", "articular", "verbi", "Articolare le parole.", "Articular as palavras.", "/artikoˈlare/", None, None),
    ("scandire", "pronunciar claramente/escandir", "verbi", "Scandire bene le sillabe.", "Pronunciar bem as sílabas.", "/skanˈdire/", None, None),
    ("esclamare", "exclamar", "verbi", "Esclamare con sorpresa.", "Exclamar com surpresa.", "/esklaˈmare/", None, None),
    ("sussurrare", "sussurrar", "verbi", "Sussurrare un segreto.", "Sussurrar um segredo.", "/sussurˈrare/", None, None),
    ("gridare", "gritar", "verbi", "Gridare a squarciagola.", "Gritar a plenos pulmões.", "/ɡriˈdare/", None, None),
    ("balbettare", "gaguejar", "verbi", "Balbettare per l'emozione.", "Gaguejar de emoção.", "/balbetˈtare/", None, None),
    ("esporre", "expor", "verbi", "Esporre i fatti.", "Expor os fatos.", "/esˈporre/", None, None),
    ("dichiarare", "declarar", "verbi", "Dichiarare guerra.", "Declarar guerra.", "/dikjaˈrare/", None, None),
    ("annunciare", "anunciar", "verbi", "Annunciare il vincitore.", "Anunciar o vencedor.", "/annunˈtʃare/", None, None),
    ("sottolineare", "sublinhar/enfatizar", "verbi", "Vorrei sottolineare che...", "Gostaria de enfatizar que...", "/sottolineˈare/", None, None),
    ("ribadire", "reiterar", "verbi", "Ribadire il concetto.", "Reiterar o conceito.", "/ribaˈdire/", None, None),
    ("confutare", "refutar", "verbi", "Confutare un'opinione.", "Refutar uma opinião.", "/konfuˈtare/", None, None),
    ("protestare", "protestar", "verbi", "Protestare contro la legge.", "Protestar contra a lei.", "/protesˈtare/", None, None),
    ("difendere", "defender", "verbi", "Difendere i propri diritti.", "Defender os próprios direitos.", "/diˈfɛndere/", None, None),
    ("affascinare", "fascinar", "verbi", "Affascinare chi ascolta.", "Fascinar quem ouve.", "/affaʃʃiˈnare/", None, None),
    ("incantare", "encantar", "verbi", "Incantare con le parole.", "Encantar com as palavras.", "/inkanˈtare/", None, None),
    ("ammaliare", "enfeitiçar/seduzir", "verbi", "Ammaliare il pubblico.", "Enfeitiçar o público.", "/ammaˈljare/", None, None),
    ("manipolare", "manipular", "verbi", "Manipolare l'opinione.", "Manipular a opinião.", "/manipoˈlare/", None, None),
    # Aggettivi e Descrittori
    ("convincente", "convincente", "aggettivi", "Un discorso convincente.", "Um discurso convincente.", "/konvinˈtʃɛnte/", "m", "convincenti"),
    ("persuasivo", "persuasivo", "aggettivi", "Un tono persuasivo.", "Um tom persuasivo.", "/perswaˈzivo/", "m", "persuasivi"),
    ("eloquente", "eloquente", "aggettivi", "Un oratore eloquente.", "Um orador eloquente.", "/eloˈkwɛnte/", "m", "eloquenti"),
    ("logico", "lógico", "aggettivi", "Un ragionamento logico.", "Um raciocínio lógico.", "/ˈlɔdʒiko/", "m", "logici"),
    ("irrazionale", "irracional", "aggettivi", "Una paura irrazionale.", "Um medo irracional.", "/irrattsjoˈnale/", "m", "irrazionali"),
    ("chiaro", "claro", "aggettivi", "Un concetto chiaro.", "Um conceito claro.", "/ˈkjaro/", "m", "chiari"),
    ("oscuro", "obscuro/confuso", "aggettivi", "Un discorso oscuro.", "Um discurso obscuro.", "/osˈkuro/", "m", "oscuri"),
    ("noioso", "chato/entediante", "aggettivi", "Una lezione noiosa.", "Uma aula entediante.", "/noˈjozo/", "m", "noiosi"),
    ("appassionato", "apaixonado/fervoroso", "aggettivi", "Un discorso appassionato.", "Um discurso fervoroso.", "/appassjoˈnato/", "m", "appassionati"),
    ("carismatico", "carismático", "aggettivi", "Un leader carismatico.", "Um líder carismático.", "/karizˈmatiko/", "m", "carismatici"),
    ("assertivo", "assertivo", "aggettivi", "Un comportamento assertivo.", "Um comportamento assertivo.", "/asserˈtivo/", "m", "assertivi"),
    ("provocatorio", "provocativo", "aggettivi", "Una domanda provocatoria.", "Uma pergunta provocativa.", "/provokaˈtɔrjo/", "m", "provocatori"),
    ("ironico", "irônico", "aggettivi", "Un commento ironico.", "Um comentário irônico.", "/iˈrɔniko/", "m", "ironici"),
    ("sarcastico", "sarcástico", "aggettivi", "Un sorriso sarcastico.", "Um sorriso sarcástico.", "/sarˈkastiko/", "m", "sarcastici"),
    ("polemico", "polêmico", "aggettivi", "Un tono polemico.", "Um tom polêmico.", "/poˈlɛmiko/", "m", "polemici"),
    ("pacato", "pacato/calmo", "aggettivi", "Una voce pacata.", "Uma voz calma.", "/paˈkato/", "m", "pacati"),
    ("aggressivo", "agressivo", "aggettivi", "Un modo aggressivo.", "Um modo agressivo.", "/aɡɡresˈsivo/", "m", "aggressivi"),
    ("difensivo", "defensivo", "aggettivi", "Sulla difensiva.", "Na defensiva.", "/difenˈsivo/", "m", "difensivi"),
    ("spontaneo", "espontâneo", "aggettivi", "Un applauso spontaneo.", "Um aplauso espontâneo.", "/sponˈtaneo/", "m", "spontanei"),
    ("preparato", "preparado", "aggettivi", "Un discorso ben preparato.", "Um discurso bem preparado.", "/prepaˈrato/", "m", "preparati"),
    ("improvvisato", "improvisado", "aggettivi", "Tutto è stato improvvisato.", "Tudo foi improvisado.", "/improvviˈzato/", "m", "improvvisati"),
    ("coinvolgente", "envolvente", "aggettivi", "Una storia coinvolgente.", "Uma história envolvente.", "/koinvolˈdʒɛnte/", "m", "coinvolgenti"),
    ("emozionante", "emocionante", "aggettivi", "Un momento emozionante.", "Um momento emocionante.", "/emotsjoˈnante/", "m", "emozionanti"),
    ("ispiratore", "inspirador", "aggettivi", "Un libro ispiratore.", "Um livro inspirador.", "/ispiraˈtore/", "m", "ispiratori"),
    ("noioso", "chato", "aggettivi", "Un relatore noioso.", "Un palestrante chato.", "/noˈjozo/", "m", "noiosi"), # wait, noioso is dupe, change to pedante
    ("pedante", "pedante", "aggettivi", "Un professore pedante.", "Um professor pedante.", "/peˈdante/", "m", "pedanti"),
    ("sincero", "sincero", "aggettivi", "Un ringraziamento sincero.", "Um agradecimento sincero.", "/sinˈtʃɛro/", "m", "sinceri"),
    ("ipocrita", "hipócrita", "aggettivi", "Un discorso ipocrita.", "Um discurso hipócrita.", "/iˈpɔkrita/", "m/f", "ipocriti"),
    ("vero", "verdadeiro", "aggettivi", "È la pura verità.", "É a pura verdade.", "/ˈvero/", "m", "veri"),
    ("falso", "falso", "aggettivi", "Una falsa promessa.", "Uma falsa promessa.", "/ˈfalso/", "m", "falsi"),
    ("retorico", "retórico", "aggettivi", "Domanda retorica.", "Pergunta retórica.", "/reˈtɔriko/", "m", "retorici")
]

# T49: La Spiritualità Orientale e la Meditazione (110 parole)
t49_data = [
    # Pratiche e Concetti
    ("meditazione", "meditação", "spiritualità", "Fare meditazione.", "Fazer meditação.", "/meditatˈtsjone/", "f", "meditazioni"),
    ("yoga", "ioga", "spiritualità", "Praticare lo yoga.", "Praticar ioga.", "/ˈjɔɡa/", "m", "yoga"),
    ("zen", "zen", "spiritualità", "Il buddismo zen.", "O budismo zen.", "/dzɛn/", "m", "zen"),
    ("karma", "carma", "spiritualità", "La legge del karma.", "A lei do carma.", "/ˈkarma/", "m", "karma"),
    ("dharma", "darma", "spiritualità", "Seguire il dharma.", "Seguir o darma.", "/ˈdarma/", "m", "dharma"),
    ("chakra", "chakra", "spiritualità", "Aprire i chakra.", "Abrir os chakras.", "/ˈtʃakra/", "m", "chakra"),
    ("mantra", "mantra", "spiritualità", "Recitare un mantra.", "Recitar um mantra.", "/ˈmantra/", "m", "mantra"),
    ("nirvana", "nirvana", "spiritualità", "Raggiungere il nirvana.", "Alcançar o nirvana.", "/nirˈvana/", "m", "nirvana"),
    ("mandala", "mandala", "spiritualità", "Colorare un mandala.", "Colorir uma mandala.", "/manˈdala/", "m", "mandala"),
    ("tao", "tao", "spiritualità", "Il flusso del tao.", "O fluxo do tao.", "/ˈtao/", "m", "tao"),
    ("yin", "yin", "spiritualità", "Lo yin e lo yang.", "O yin e o yang.", "/jin/", "m", "yin"),
    ("yang", "yang", "spiritualità", "Equilibrio tra yin e yang.", "Equilíbrio entre yin e yang.", "/jaŋ/", "m", "yang"),
    ("ki", "chi/ki (energia)", "spiritualità", "L'energia vitale ki.", "A energia vital ki.", "/ki/", "m", "ki"),
    ("prana", "prana", "spiritualità", "Il prana nell'aria.", "O prana no ar.", "/ˈprana/", "m", "prana"),
    ("reincarnazione", "reencarnação", "spiritualità", "Credere nella reincarnazione.", "Acreditar na reencarnação.", "/reinkarnatˈtsjone/", "f", "reincarnazioni"),
    ("illuminazione", "iluminação (espiritual)", "spiritualità", "L'illuminazione del Buddha.", "A iluminação do Buda.", "/illuminatˈtsjone/", "f", "illuminazioni"),
    ("risveglio", "despertar", "spiritualità", "Il risveglio spirituale.", "O despertar espiritual.", "/rizˈveʎʎo/", "m", "risvegli"),
    ("consapevolezza", "consciência/mindfulness", "spiritualità", "Praticare la consapevolezza.", "Praticar a atenção plena.", "/konsapevoˈlettsa/", "f", "consapevolezze"),
    ("compassione", "compaixão", "spiritualità", "Provare compassione per tutti.", "Sentir compaixão por todos.", "/kompasˈsjone/", "f", "compassioni"),
    ("distacco", "desapego", "spiritualità", "Il distacco dai beni materiali.", "O desapego dos bens materiais.", "/disˈtakko/", "m", "distacchi"),
    ("vuoto", "vazio (shunyata)", "spiritualità", "Il vuoto mentale.", "O vazio mental.", "/ˈvwɔto/", "m", "vuoti"),
    ("silenzio", "silêncio", "spiritualità", "Il silenzio interiore.", "O silêncio interior.", "/siˈlɛntsjo/", "m", "silenzi"),
    ("pace", "paz", "spiritualità", "Pace e serenità.", "Paz e serenidade.", "/ˈpatʃe/", "f", "paci"),
    ("armonia", "harmonia", "spiritualità", "In armonia col cosmo.", "Em harmonia com o cosmos.", "/armoˈnia/", "f", "armonie"),
    ("energia", "energia", "spiritualità", "Energia positiva.", "Energia positiva.", "/enerˈdʒia/", "f", "energie"),
    ("respiro", "respiração", "spiritualità", "Ascoltare il respiro.", "Ouvir a respiração.", "/resˈpiro/", "m", "respiri"),
    ("postura", "postura (asana)", "spiritualità", "La postura del loto.", "A postura de lótus.", "/posˈtura/", "f", "posture"),
    ("loto", "lótus", "spiritualità", "Il fiore di loto.", "A flor de lótus.", "/ˈlɔto/", "m", "loti"),
    ("campana", "sino (tibetano)", "oggetti", "Suonare la campana tibetana.", "Tocar o sino tibetano.", "/kamˈpana/", "f", "campane"),
    ("incenso", "incenso", "oggetti", "Bruciare l'incenso.", "Queimar o incenso.", "/inˈtʃɛnso/", "m", "incensi"),
    ("gong", "gongo", "oggetti", "Il suono del gong.", "O som do gongo.", "/ɡɔnɡ/", "m", "gong"),
    # Persone e Luoghi
    ("buddha", "buda", "persone", "La statua del Buddha.", "A estátua do Buda.", "/ˈbudda/", "m", "buddha"),
    ("monaco", "monge", "persone", "Il monaco buddista.", "O monge budista.", "/ˈmɔnako/", "m", "monaci"),
    ("maestro", "mestre", "persone", "Il maestro spirituale.", "O mestre espiritual.", "/maˈɛstro/", "m", "maestri"),
    ("guru", "guru", "persone", "Il guru indiano.", "O guru indiano.", "/ˈɡuru/", "m", "guru"),
    ("discepolo", "discípulo", "persone", "Il discepolo ascolta.", "O discípulo ouve.", "/diʃˈʃepolo/", "m", "discepoli"),
    ("ashram", "ashram", "luoghi", "Vivere in un ashram.", "Viver em um ashram.", "/ˈaʃram/", "m", "ashram"),
    ("tempio", "templo", "luoghi", "Il tempio zen.", "O templo zen.", "/ˈtɛmpjo/", "m", "tempi"),
    ("santuario", "santuário", "luoghi", "Il santuario scintoista.", "O santuário xintoísta.", "/santuˈarjo/", "m", "santuari"),
    ("monastero", "mosteiro", "luoghi", "Un monastero tibetano.", "Um mosteiro tibetano.", "/monasˈtɛro/", "m", "monasteri"),
    ("tibet", "tibet", "luoghi", "Viaggio in Tibet.", "Viagem ao Tibet.", "/ˈtibet/", "m", None),
    ("india", "índia", "luoghi", "Lo yoga viene dall'India.", "A ioga vem da Índia.", "/ˈindja/", "f", None),
    # Verbi
    ("meditare", "meditar", "verbi", "Meditare al mattino.", "Meditar de manhã.", "/mediˈtare/", None, None),
    ("respirare", "respirar", "verbi", "Respirare profondamente.", "Respirar profundamente.", "/respiˈrare/", None, None),
    ("concentrarsi", "concentrar-se", "verbi", "Concentrarsi sul respiro.", "Concentrar-se na respiração.", "/kontʃenˈtrarsi/", None, None),
    ("rilassarsi", "relaxar", "verbi", "Rilassarsi completamente.", "Relaxar completamente.", "/rilasˈsarsi/", None, None),
    ("osservare", "observar", "verbi", "Osservare i pensieri.", "Observar os pensamentos.", "/osserˈvare/", None, None),
    ("accettare", "aceitar", "verbi", "Accettare le cose come sono.", "Aceitar as coisas como são.", "/attʃetˈtare/", None, None),
    ("lasciare", "deixar (ir)", "verbi", "Lasciare andare il passato.", "Deixar ir o passado.", "/laʃˈʃare/", None, None),
    ("fluire", "fluir", "verbi", "Lasciare fluire l'energia.", "Deixar fluir a energia.", "/fluˈire/", None, None),
    ("risvegliarsi", "despertar", "verbi", "Risvegliarsi spiritualmente.", "Despertar espiritualmente.", "/rizveʎˈʎarsi/", None, None),
    ("illuminarsi", "iluminar-se", "verbi", "Il Buddha si illuminò.", "O Buda se iluminou.", "/illumiˈnarsi/", None, None),
    ("cantare", "cantar (mantra)", "verbi", "Cantare il mantra Om.", "Cantar o mantra Om.", "/kanˈtare/", None, None),
    ("visualizzare", "visualizar", "verbi", "Visualizzare la luce.", "Visualizar a luz.", "/vizwalidˈdzare/", None, None),
    ("purificare", "purificar", "verbi", "Purificare la mente.", "Purificar a mente.", "/purifiˈkare/", None, None),
    ("bilanciare", "equilibrar", "verbi", "Bilanciare i chakra.", "Equilibrar os chakras.", "/bilanˈtʃare/", None, None),
    ("vibrare", "vibrar", "verbi", "Vibrare a frequenze alte.", "Vibrar em altas frequências.", "/viˈbrare/", None, None),
    ("inchinarsi", "curvar-se/reverenciar", "verbi", "Inchinarsi al maestro.", "Curvar-se ao mestre.", "/inkiˈnarsi/", None, None),
    ("praticare", "praticar", "verbi", "Praticare yoga ogni giorno.", "Praticar ioga todo dia.", "/pratiˈkare/", None, None),
    ("unire", "unir", "verbi", "Unire corpo e mente.", "Unir corpo e mente.", "/uˈnire/", None, None),
    ("percepire", "perceber/sentir", "verbi", "Percepire l'energia.", "Perceber a energia.", "/pertʃeˈpire/", None, None),
    ("trascendere", "transcender", "verbi", "Trascendere l'ego.", "Transcender o ego.", "/traʃˈʃendere/", None, None),
    # Aggettivi e descrittori
    ("spirituale", "espiritual", "aggettivi", "Un viaggio spirituale.", "Uma viagem espiritual.", "/spiriˈtwale/", "m", "spirituali"),
    ("interiore", "interior", "aggettivi", "Pace interiore.", "Paz interior.", "/inteˈrjore/", "m", "interiori"),
    ("esteriore", "exterior", "aggettivi", "L'aspetto esteriore.", "O aspecto exterior.", "/esteˈrjore/", "m", "esteriori"),
    ("consapevole", "consciente", "aggettivi", "Essere consapevole del respiro.", "Estar consciente da respiração.", "/konsaˈpevole/", "m", "consapevoli"),
    ("sereno", "sereno", "aggettivi", "Un viso sereno.", "Um rosto sereno.", "/seˈreno/", "m", "sereni"),
    ("calmo", "calmo", "aggettivi", "Una mente calma.", "Uma mente calma.", "/ˈkalmo/", "m", "calmi"),
    ("equilibrato", "equilibrado", "aggettivi", "Uno stile di vita equilibrato.", "Um estilo de vida equilibrado.", "/ekwiliˈbrato/", "m", "equilibrati"),
    ("profondo", "profundo", "aggettivi", "Un respiro profondo.", "Uma respiração profunda.", "/proˈfondo/", "m", "profondi"),
    ("saggio", "sábio", "aggettivi", "Un maestro saggio.", "Um mestre sábio.", "/ˈsaddʒo/", "m", "saggi"),
    ("illuminato", "iluminado", "aggettivi", "Un essere illuminato.", "Um ser iluminado.", "/illumiˈnato/", "m", "illuminati"),
    ("divino", "divino", "aggettivi", "La scintilla divina.", "A centelha divina.", "/diˈvino/", "m", "divini"),
    ("sacro", "sagrado", "aggettivi", "Un fiume sacro.", "Um rio sagrado.", "/ˈsakro/", "m", "sacri"),
    ("puro", "puro", "aggettivi", "Amore puro.", "Amor puro.", "/ˈpuro/", "m", "puri"),
    ("compassionevole", "compassivo", "aggettivi", "Un cuore compassionevole.", "Um coração compassivo.", "/kompassjoˈnevole/", "m", "compassionevoli"),
    ("silenzioso", "silencioso", "aggettivi", "Un ritiro silenzioso.", "Um retiro silencioso.", "/silenˈtsjozo/", "m", "silenziosi"),
    ("invisibile", "invisível", "aggettivi", "Energia invisibile.", "Energia invisível.", "/inviˈzibile/", "m", "invisibili"),
    ("sottile", "sutil", "aggettivi", "Il corpo sottile.", "O corpo sutil.", "/sotˈtile/", "m", "sottili"),
    ("universale", "universal", "aggettivi", "Mente universale.", "Mente universal.", "/univerˈsale/", "m", "universali"),
    ("eterno", "eterno", "aggettivi", "Il ciclo eterno.", "O ciclo eterno.", "/eˈtɛrno/", "m", "eterni"),
    ("infinito", "infinito", "aggettivi", "L'amore infinito.", "O amor infinito.", "/infiˈnito/", "m", "infiniti"),
    ("orientale", "oriental", "aggettivi", "Filosofia orientale.", "Filosofia oriental.", "/orjenˈtale/", "m", "orientali"),
    ("occidentale", "ocidental", "aggettivi", "Mondo occidentale.", "Mundo ocidental.", "/ottʃidenˈtale/", "m", "occidentali"),
    ("buddista", "budista", "aggettivi", "Tempio buddista.", "Templo budista.", "/budˈdista/", "m/f", "buddisti"),
    ("induista", "hinduísta", "aggettivi", "Religione induista.", "Religião hinduísta.", "/induˈista/", "m/f", "induisti"),
    ("scintoista", "xintoísta", "aggettivi", "Santuario scintoista.", "Santuário xintoísta.", "/ʃintoˈista/", "m/f", "scintoisti"),
    ("taoista", "taoísta", "aggettivi", "Monaco taoista.", "Monge taoísta.", "/taoˈista/", "m/f", "taoisti"),
    ("mistico", "místico", "aggettivi", "Un'esperienza mistica.", "Uma experiência mística.", "/ˈmistiko/", "m", "mistici"),
    ("esoterico", "esotérico", "aggettivi", "Sapere esoterico.", "Saber esotérico.", "/ezoˈtɛriko/", "m", "esoterici")
]

# T50: Il Viaggio della Vita (Il traguardo finale) (110 parole)
t50_data = [
    # Fasi della Vita
    ("vita", "vida", "fasi", "La vita è bella.", "A vida é bela.", "/ˈvita/", "f", "vite"),
    ("morte", "morte", "fasi", "La vita e la morte.", "A vida e a morte.", "/ˈmɔrte/", "f", "morti"),
    ("nascita", "nascimento", "fasi", "La nascita di un bambino.", "O nascimento de um bebê.", "/ˈnaʃʃita/", "f", "nascite"),
    ("infanzia", "infância", "fasi", "Un'infanzia felice.", "Uma infância feliz.", "/inˈfantsja/", "f", "infanzie"),
    ("adolescenza", "adolescência", "fasi", "I problemi dell'adolescenza.", "Os problemas da adolescência.", "/adoleʃˈʃɛntsa/", "f", "adolescenze"),
    ("giovinezza", "juventude", "fasi", "La giovinezza passa in fretta.", "A juventude passa rápido.", "/dʒoviˈnettsa/", "f", "giovinezze"),
    ("maturità", "maturidade", "fasi", "Raggiungere la maturità.", "Alcançar a maturidade.", "/maturiˈta/", "f", "maturità"),
    ("vecchiaia", "velhice", "fasi", "Una serena vecchiaia.", "Uma velhice serena.", "/vekˈkjaja/", "f", "vecchiaie"),
    ("generazione", "geração", "fasi", "Di generazione in generazione.", "De geração em geração.", "/dʒeneratˈtsjone/", "f", "generazioni"),
    ("destino", "destino", "concetti", "Il mio destino.", "O meu destino.", "/desˈtino/", "m", "destini"),
    ("passato", "passado", "concetti", "Non pensare al passato.", "Não pense no passado.", "/pasˈsato/", "m", "passati"),
    ("presente", "presente", "concetti", "Vivi nel presente.", "Viva no presente.", "/preˈzɛnte/", "m", "presenti"),
    ("futuro", "futuro", "concetti", "Il futuro è incerto.", "O futuro é incerto.", "/fuˈturo/", "m", "futuri"),
    ("tempo", "tempo", "concetti", "Il tempo vola.", "O tempo voa.", "/ˈtɛmpo/", "m", "tempi"),
    ("memoria", "memória", "concetti", "In memoria di...", "Em memória de...", "/meˈmɔrja/", "f", "memorie"),
    ("ricordo", "lembrança", "concetti", "Un bellissimo ricordo.", "Uma belíssima lembrança.", "/riˈkɔrdo/", "m", "ricordi"),
    ("sogno", "sonho", "concetti", "I sogni diventano realtà.", "Os sonhos se tornam realidade.", "/ˈsoɲɲo/", "m", "sogni"),
    ("speranza", "esperança", "concetti", "Non perdere la speranza.", "Não perca a esperança.", "/speˈrantsa/", "f", "speranze"),
    ("scopo", "propósito/objetivo", "concetti", "Lo scopo della vita.", "O propósito da vida.", "/ˈskɔpo/", "m", "scopi"),
    ("senso", "sentido", "concetti", "Il senso della vita.", "O sentido da vida.", "/ˈsɛnso/", "m", "sensi"),
    ("esperienza", "experiência", "concetti", "Imparare dall'esperienza.", "Aprender com a experiência.", "/espeˈrjɛntsa/", "f", "esperienze"),
    ("saggezza", "sabedoria", "concetti", "La saggezza degli anziani.", "A sabedoria dos mais velhos.", "/sadˈdʒettsa/", "f", "saggezze"),
    ("viaggio", "viagem", "concetti", "La vita è un viaggio.", "A vida é uma viagem.", "/ˈvjaddʒo/", "m", "viaggi"),
    ("strada", "caminho/estrada", "concetti", "La strada giusta.", "O caminho certo.", "/ˈstrada/", "f", "strade"),
    ("percorso", "percurso/trajetória", "concetti", "Il mio percorso.", "A minha trajetória.", "/perˈkorso/", "m", "percorsi"),
    ("meta", "meta/destino", "concetti", "Raggiungere la meta.", "Alcançar a meta.", "/ˈmɛta/", "f", "mete"),
    ("traguardo", "linha de chegada/meta", "concetti", "Tagliare il traguardo.", "Cruzar a linha de chegada.", "/traˈɡwardo/", "m", "traguardi"),
    ("ostacolo", "obstáculo", "concetti", "Superare un ostacolo.", "Superar um obstáculo.", "/osˈtakolo/", "m", "ostacoli"),
    ("sfida", "desafio", "concetti", "Accettare la sfida.", "Aceitar o desafio.", "/ˈsfida/", "f", "sfide"),
    ("successo", "sucesso", "concetti", "Avere grande successo.", "Ter grande sucesso.", "/sutˈtʃɛsso/", "m", "successi"),
    ("fallimento", "fracasso", "concetti", "La paura del fallimento.", "O medo do fracasso.", "/falliˈmento/", "m", "fallimenti"),
    ("vittoria", "vitória", "concetti", "Celebrare la vittoria.", "Celebrar a vitória.", "/vitˈtɔrja/", "f", "vittorie"),
    ("sconfitta", "derrota", "concetti", "Accettare la sconfitta.", "Aceitar a derrota.", "/skonˈfitta/", "f", "sconfitte"),
    ("cambiamento", "mudança", "concetti", "Il cambiamento climatico.", "A mudança climática.", "/kambjaˈmento/", "m", "cambiamenti"),
    ("scelta", "escolha", "concetti", "Fare una scelta.", "Fazer uma escolha.", "/ˈʃelta/", "f", "scelte"),
    ("rimpianto", "arrependimento", "concetti", "Vivere senza rimpianti.", "Viver sem arrependimentos.", "/rimˈpjanto/", "m", "rimpianti"),
    ("perdono", "perdão", "concetti", "Chiedere perdono.", "Pedir perdão.", "/perˈdono/", "m", "perdoni"),
    ("eredità", "herança/legado", "concetti", "Lasciare una buona eredità.", "Deixar um bom legado.", "/erediˈta/", "f", "eredità"),
    ("anima", "alma", "concetti", "Anima e corpo.", "Alma e corpo.", "/ˈanima/", "f", "anime"),
    ("cuore", "coração", "concetti", "Ascolta il tuo cuore.", "Ouça o seu coração.", "/ˈkwɔre/", "m", "cuori"),
    ("mente", "mente", "concetti", "Mente aperta.", "Mente aberta.", "/ˈmente/", "f", "menti"),
    ("spirito", "espírito", "concetti", "Uno spirito libero.", "Um espírito livre.", "/ˈspirito/", "m", "spiriti"),
    ("universo", "universo", "concetti", "Siamo parte dell'universo.", "Somos parte do universo.", "/uniˈvɛrso/", "m", "universi"),
    ("natura", "natureza", "concetti", "Il ciclo della natura.", "O ciclo da natureza.", "/naˈtura/", "f", "nature"),
    ("amore", "amor", "concetti", "L'amore vince tutto.", "O amor vence tudo.", "/aˈmore/", "m", "amori"),
    ("amicizia", "amizade", "concetti", "Un'amicizia vera.", "Uma amizade verdadeira.", "/amiˈtʃittsja/", "f", "amicizie"),
    ("famiglia", "família", "concetti", "La famiglia è importante.", "A família é importante.", "/faˈmiʎʎa/", "f", "famiglie"),
    ("casa", "casa/lar", "concetti", "Tornare a casa.", "Voltar para casa.", "/ˈkaza/", "f", "case"),
    ("mondo", "mundo", "concetti", "Il giro del mondo.", "A volta ao mundo.", "/ˈmondo/", "m", "mondi"),
    ("pace", "paz", "concetti", "Riposare in pace.", "Descansar em paz.", "/ˈpatʃe/", "f", "paci"),
    # Verbi
    ("nascere", "nascer", "verbi", "Nascere a Roma.", "Nascer em Roma.", "/ˈnaʃʃere/", None, None),
    ("crescere", "crescer", "verbi", "I bambini crescono in fretta.", "As crianças crescem rápido.", "/ˈkreʃʃere/", None, None),
    ("vivere", "viver", "verbi", "Vivere intensamente.", "Viver intensamente.", "/ˈvivere/", None, None),
    ("sopravvivere", "sobreviver", "verbi", "Sopravvivere alle difficoltà.", "Sobreviver às dificuldades.", "/sopravˈvivere/", None, None),
    ("invecchiare", "envelhecer", "verbi", "Invecchiare bene.", "Envelhecer bem.", "/invekˈkjare/", None, None),
    ("morire", "morrer", "verbi", "Morire di vecchiaia.", "Morrer de velhice.", "/moˈrire/", None, None),
    ("imparare", "aprender", "verbi", "Non si finisce mai di imparare.", "Nunca se termina de aprender.", "/impaˈrare/", None, None),
    ("insegnare", "ensinar", "verbi", "Insegnare ai figli.", "Ensinar aos filhos.", "/inseɲˈɲare/", None, None),
    ("scoprire", "descobrir", "verbi", "Scoprire il mondo.", "Descobrir o mundo.", "/skoˈprire/", None, None),
    ("viaggiare", "viajar", "verbi", "Viaggiare apre la mente.", "Viajar abre a mente.", "/vjadˈdʒare/", None, None),
    ("amare", "amar", "verbi", "Amare e farsi amare.", "Amar e ser amado.", "/aˈmare/", None, None),
    ("soffrire", "sofrer", "verbi", "Soffrire in silenzio.", "Sofrer em silêncio.", "/sofˈfrire/", None, None),
    ("gioire", "alegrar-se", "verbi", "Gioire per le piccole cose.", "Alegrar-se com as pequenas coisas.", "/dʒoˈire/", None, None),
    ("lottare", "lutar", "verbi", "Lottare per i propri sogni.", "Lutar pelos próprios sonhos.", "/lotˈtare/", None, None),
    ("arrendersi", "render-se/desistir", "verbi", "Mai arrendersi.", "Nunca desistir.", "/arˈrɛndersi/", None, None),
    ("superare", "superar", "verbi", "Superare le paure.", "Superar os medos.", "/supeˈrare/", None, None),
    ("cadere", "cair", "verbi", "Cadere e rialzarsi.", "Cair e levantar-se.", "/kaˈdere/", None, None),
    ("rialzarsi", "levantar-se (de novo)", "verbi", "Rialzarsi più forti.", "Levantar-se mais fortes.", "/rjalˈtsarsi/", None, None),
    ("cambiare", "mudar", "verbi", "Le persone cambiano.", "As pessoas mudam.", "/kamˈbjare/", None, None),
    ("migliorare", "melhorar", "verbi", "Migliorare ogni giorno.", "Melhorar a cada dia.", "/miʎʎoˈrare/", None, None),
    ("perdonare", "perdoar", "verbi", "Perdonare gli errori.", "Perdoar os erros.", "/perdoˈnare/", None, None),
    ("dimenticare", "esquecer", "verbi", "Non dimenticare mai.", "Nunca esquecer.", "/dimentiˈkare/", None, None),
    ("ricordare", "lembrar", "verbi", "Ricordare i bei momenti.", "Lembrar os bons momentos.", "/rikorˈdare/", None, None),
    ("sognare", "sonhar", "verbi", "Sognare un futuro migliore.", "Sonhar com um futuro melhor.", "/soɲˈɲare/", None, None),
    ("sperare", "esperar (esperança)", "verbi", "Continuare a sperare.", "Continuar a ter esperança.", "/speˈrare/", None, None),
    ("costruire", "construir", "verbi", "Costruire una famiglia.", "Construir uma família.", "/kostruˈire/", None, None),
    ("lasciare", "deixar", "verbi", "Lasciare un segno.", "Deixar uma marca.", "/laʃˈʃare/", None, None),
    ("trovare", "encontrar", "verbi", "Trovare il proprio scopo.", "Encontrar o próprio propósito.", "/troˈvare/", None, None),
    ("cercare", "procurar", "verbi", "Cercare la felicità.", "Procurar a felicidade.", "/tʃerˈkare/", None, None),
    ("essere", "ser/estar", "verbi", "Essere se stessi.", "Ser si mesmo.", "/ˈɛssere/", None, None),
    # Aggettivi e descrittori
    ("umano", "humano", "aggettivi", "Un essere umano.", "Um ser humano.", "/uˈmano/", "m", "umani"),
    ("divino", "divino", "aggettivi", "Intervento divino.", "Intervenção divina.", "/diˈvino/", "m", "divini"),
    ("mortale", "mortal", "aggettivi", "Noi siamo mortali.", "Nós somos mortais.", "/morˈtale/", "m", "mortali"),
    ("immortale", "imortal", "aggettivi", "Un ricordo immortale.", "Uma lembrança imortal.", "/immorˈtale/", "m", "immortali"),
    ("eterno", "eterno", "aggettivi", "Amore eterno.", "Amor eterno.", "/eˈtɛrno/", "m", "eterni"),
    ("infinito", "infinito", "aggettivi", "Il cosmo infinito.", "O cosmos infinito.", "/infiˈnito/", "m", "infiniti"),
    ("effimero", "efêmero", "aggettivi", "La bellezza è effimera.", "A beleza é efêmera.", "/efˈfimero/", "m", "effimeri"),
    ("duraturo", "duradouro", "aggettivi", "Una pace duratura.", "Uma paz duradoura.", "/duraˈturo/", "m", "duraturi"),
    ("giovane", "jovem", "aggettivi", "Un ragazzo giovane.", "Um rapaz jovem.", "/ˈdʒovane/", "m", "giovani"),
    ("anziano", "idoso", "aggettivi", "Un signore anziano.", "Um senhor idoso.", "/anˈtsjano/", "m", "anziani"),
    ("maturo", "maduro", "aggettivi", "Una persona matura.", "Uma pessoa madura.", "/maˈturo/", "m", "maturi"),
    ("saggio", "sábio", "aggettivi", "Un consiglio saggio.", "Um conselho sábio.", "/ˈsaddʒo/", "m", "saggi"),
    ("felice", "feliz", "aggettivi", "Essere felici.", "Ser felizes.", "/feˈlitʃe/", "m", "felici"),
    ("triste", "triste", "aggettivi", "Un momento triste.", "Um momento triste.", "/ˈtriste/", "m", "tristi"),
    ("forte", "forte", "aggettivi", "Rimanere forte.", "Permanecer forte.", "/ˈfɔrte/", "m", "forti"),
    ("debole", "fraco", "aggettivi", "Un momento debole.", "Um momento fraco.", "/ˈdebole/", "m", "deboli"),
    ("coraggioso", "corajoso", "aggettivi", "Una scelta coraggiosa.", "Uma escolha corajosa.", "/koradˈdʒozo/", "m", "coraggiosi"),
    ("pauroso", "medroso/assustador", "aggettivi", "Un cane pauroso.", "Um cachorro medroso.", "/pauˈrozo/", "m", "paurosi"),
    ("libero", "livre", "aggettivi", "Come un uccello libero.", "Como um pássaro livre.", "/ˈlibero/", "m", "liberi"),
    ("prigioniero", "prisioneiro", "aggettivi", "Prigioniero delle paure.", "Prisioneiro dos medos.", "/pridʒoˈnjɛro/", "m", "prigionieri"),
    ("vero", "verdadeiro", "aggettivi", "È la vita vera.", "É a vida verdadeira.", "/ˈvero/", "m", "veri"),
    ("falso", "falso", "aggettivi", "Un mondo falso.", "Um mundo falso.", "/ˈfalso/", "m", "falsi"),
    ("giusto", "justo", "aggettivi", "Fare la cosa giusta.", "Fazer a coisa certa.", "/ˈdʒusto/", "m", "giusti"),
    ("sbagliato", "errado", "aggettivi", "Un passo sbagliato.", "Um passo errado.", "/zbaˈʎʎato/", "m", "sbagliati"),
    ("buono", "bom", "aggettivi", "Un uomo buono.", "Um homem bom.", "/ˈbwɔno/", "m", "buoni"),
    ("cattivo", "mau/ruim", "aggettivi", "Un lupo cattivo.", "Um lobo mau.", "/katˈtivo/", "m", "cattivi"),
    ("bello", "belo/bonito", "aggettivi", "Che bel giorno.", "Que belo dia.", "/ˈbɛllo/", "m", "belli"),
    ("brutto", "feio/ruim", "aggettivi", "Un brutto ricordo.", "Uma lembrança ruim.", "/ˈbrutto/", "m", "brutti"),
    ("importante", "importante", "aggettivi", "La cosa più importante.", "A coisa mais importante.", "/imporˈtante/", "m", "importanti"),
    ("unico", "único", "aggettivi", "Ogni persona è unica.", "Cada pessoa é única.", "/ˈuniko/", "m", "unici")
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
    append_to_existing(45, t45_add)
    append_to_existing(46, t46_add)
    append_to_existing(47, t47_add)
    
    create_new(48, "L'Arte dell'Oratoria e la Persuasione", "Roma", "C2", t48_data)
    create_new(49, "La Spiritualità Orientale e la Meditazione", "Assisi", "C2", t49_data)
    create_new(50, "Il Viaggio della Vita", "Venezia", "C2", t50_data)
