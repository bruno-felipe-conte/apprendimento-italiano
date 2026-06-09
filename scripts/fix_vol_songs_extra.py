import json, re, sys

# Fix remaining 40 songs with themes: amicizia, ribellione, nostalgia, vita
TEMAS_EXTRA = {
    "amicizia": [
        # Vol 1
        ("Gli amici veri restano accanto a te nei momenti difficili.", "veri", "Os amigos verdadeiros ficam do seu lado nos momentos difíceis.", "aggettivo: autentici, sinceri"),
        ("Con i miei amici mi sento sempre a casa.", "amici", "Com meus amigos sempre me sinto em casa.", "sostantivo plurale: persone care"),
        ("L'amicizia è il dono più prezioso della vita.", "dono", "A amizade é o presente mais precioso da vida.", "sostantivo: regalo"),
        ("Ridiamo insieme fino alle lacrime ogni volta.", "lacrime", "Rimos juntos até as lágrimas cada vez.", "sostantivo plurale: gocce dal pianto"),
        # Vol 2
        ("Un amico sincero vale più di mille conoscenti.", "sincero", "Um amigo sincero vale mais que mil conhecidos.", "aggettivo: onesto, genuino"),
        ("Ci siamo incontrati per caso e non ci siamo più lasciati.", "lasciati", "Nos conhecemos por acaso e nunca mais nos separamos.", "participio passato di lasciarsi"),
        ("La distanza non spezza l'amicizia vera.", "spezza", "A distância não quebra a amizade verdadeira.", "verbo spezzare: rompere"),
        ("Con te posso essere me stesso senza maschere.", "maschere", "Com você posso ser eu mesmo sem máscaras.", "sostantivo plurale: travestimenti"),
        # Vol 3
        ("Gli amici di infanzia sono i più difficili da dimenticare.", "infanzia", "Os amigos de infância são os mais difíceis de esquecer.", "sostantivo: periodo dell'età giovane"),
        ("Ti ascolto sempre quando hai bisogno di parlare.", "bisogno", "Sempre te escuto quando você precisa falar.", "sostantivo: necessità"),
        ("Condividere i problemi con un amico li rende più leggeri.", "condividere", "Compartilhar os problemas com um amigo os torna mais leves.", "verbo: dividere con altri"),
        ("La nostra amicizia è nata un pomeriggio d'estate.", "nata", "Nossa amizade nasceu numa tarde de verão.", "participio passato di nascere"),
        # Vol 4
        ("Un vero amico sa cosa pensi anche senza parlare.", "pensa", "Um amigo verdadeiro sabe o que você pensa sem falar.", "verbo pensare: avere in mente"),
        ("Con te ogni giornata diventa più bella e speciale.", "speciale", "Com você cada dia se torna mais bonito e especial.", "aggettivo: fuori dal comune"),
        ("Gli amici sono la famiglia che scegliamo noi stessi.", "famiglia", "Os amigos são a família que escolhemos nós mesmos.", "sostantivo: gruppo di persone care"),
        ("Festeggiamo insieme ogni piccola vittoria della vita.", "vittoria", "Celebramos juntos cada pequena vitória da vida.", "sostantivo: successo ottenuto"),
        # Vol 5
        ("Mi fido ciecamente di te come di un fratello.", "fratello", "Confio cegamente em você como em um irmão.", "sostantivo: figlio degli stessi genitori"),
        ("L'amicizia vera cresce con il tempo e le esperienze.", "cresce", "A amizade verdadeira cresce com o tempo e as experiências.", "verbo crescere: aumentare"),
        ("Ci aiutiamo a vicenda senza aspettarci nulla.", "aiutiamo", "Nos ajudamos mutuamente sem esperar nada em troca.", "verbo aiutarsi: sostenersi"),
        ("Il tuo sorriso mi dà forza quando sono giù di morale.", "morale", "Seu sorriso me dá força quando estou pra baixo.", "sostantivo: stato d'animo"),
        # Vol 6
        ("Abbiamo condiviso migliaia di risate e qualche lacrima.", "risate", "Compartilhamos milhares de risadas e algumas lágrimas.", "sostantivo plurale: atti del ridere"),
        ("Sei la persona con cui voglio celebrare ogni successo.", "celebrare", "Você é a pessoa com quem quero celebrar cada sucesso.", "verbo: festeggiare"),
        ("Ogni viaggio è più bello se lo faccio con te.", "viaggio", "Cada viagem é mais bonita se a faço com você.", "sostantivo: spostamento"),
        ("La nostra amicizia resiste a tutte le tempeste.", "tempeste", "Nossa amizade resiste a todas as tempestades.", "sostantivo plurale: difficoltà"),
        # Vol 7
        ("Ci capiamo senza bisogno di spiegare troppo.", "capiamo", "Nos entendemos sem precisar explicar muito.", "verbo capirsi: comprendersi"),
        ("Sei il primo a cui telefono quando ho una buona notizia.", "notizia", "Você é o primeiro a quem ligo quando tenho uma boa notícia.", "sostantivo: informazione"),
        ("Gli anni passano ma la nostra amicizia non invecchia.", "invecchia", "Os anos passam mas nossa amizade não envelhece.", "verbo invecchiare: diventare vecchio"),
        ("Con te non ho bisogno di fare finta di stare bene.", "finta", "Com você não preciso fingir estar bem.", "sostantivo: finzione"),
        # Vol 8
        ("Ti conosco così bene che so quando stai soffrendo.", "soffrendo", "Te conheço tão bem que sei quando você está sofrendo.", "gerundio di soffrire"),
        ("Siamo diversi ma questo è il segreto della nostra amicizia.", "segreto", "Somos diferentes mas este é o segredo da nossa amizade.", "sostantivo: cosa nascosta"),
        ("Ho imparato tanto da te negli anni che siamo amici.", "amici", "Aprendi muito com você nos anos em que somos amigos.", "sostantivo plurale: persone care"),
        ("Ogni momento trascorso insieme è un regalo.", "regalo", "Cada momento passado junto é um presente.", "sostantivo: dono, regalare"),
        # Vol 9
        ("Il tuo supporto mi ha dato il coraggio di andare avanti.", "coraggio", "Seu apoio me deu a coragem de seguir em frente.", "sostantivo: audacia, bravura"),
        ("Con gli amici il tempo non si misura in ore ma in emozioni.", "emozioni", "Com amigos o tempo não se mede em horas mas em emoções.", "sostantivo plurale: sentimenti"),
        ("Sei la prova vivente che l'amicizia può durare per sempre.", "vivente", "Você é a prova viva de que a amizade pode durar para sempre.", "aggettivo: che è in vita"),
        ("Quando sono con te, tutti i problemi sembrano piccoli.", "piccoli", "Quando estou com você, todos os problemas parecem pequenos.", "aggettivo: di dimensioni ridotte"),
        # Vol 10
        ("Grazie per esserci sempre, anche nelle notti più buie.", "buie", "Obrigado por estar sempre, mesmo nas noites mais sombrias.", "aggettivo: senza luce"),
        ("La vera amicizia non si conta in anni ma in qualità.", "qualità", "A verdadeira amizade não se conta em anos mas em qualidade.", "sostantivo: valore, caratteristica"),
        ("Insieme abbiamo superato tutto, e continueremo così.", "superato", "Juntos superamos tudo, e continuaremos assim.", "participio passato di superare"),
        ("Sei l'amico che tutti vorrebbero avere nella vita.", "vorrebbero", "Você é o amigo que todos gostariam de ter na vida.", "condizionale di volere"),
    ],
    "ribellione": [
        # Vol 1
        ("Non seguo le regole che gli altri hanno scritto per me.", "regole", "Não sigo as regras que os outros escreveram para mim.", "sostantivo plurale: norme, leggi"),
        ("Mi ribello contro ogni forma di ingiustizia.", "ribello", "Me rebelo contra toda forma de injustiça.", "verbo ribellarsi: opporsi"),
        ("La libertà non si chiede, si prende con forza.", "libertà", "A liberdade não se pede, se toma com força.", "sostantivo: stato di essere liberi"),
        ("Ho detto no quando tutti gli altri dicevano sì.", "dicevano", "Disse não quando todos os outros diziam sim.", "verbo dire: imperfetto plurale"),
        # Vol 2
        ("Non accetto di vivere nella gabbia che la società costruisce.", "gabbia", "Não aceito viver na gaiola que a sociedade constrói.", "sostantivo: prigione per uccelli"),
        ("Mi alzo e grido: non siamo schiavi del sistema.", "schiavi", "Me levanto e grito: não somos escravos do sistema.", "sostantivo plurale: persone non libere"),
        ("La mia voce non si spegne neanche quando mi chiedono il silenzio.", "neanche", "Minha voz não se apaga nem quando me pedem silêncio.", "congiunzione: nemmeno"),
        ("Ogni regola ingiusta merita di essere contestata.", "contestata", "Cada regra injusta merece ser contestada.", "participio passato di contestare"),
        # Vol 3
        ("Rompo le catene che tengono la mia mente prigioniera.", "catene", "Quebre as correntes que mantêm minha mente prisioneira.", "sostantivo plurale: legami di metallo"),
        ("Non temo le conseguenze di dire quello che penso.", "penso", "Não temo as consequências de dizer o que penso.", "verbo pensare: avere in mente"),
        ("La ribellione nasce quando l'ingiustizia diventa insopportabile.", "insopportabile", "A rebelião nasce quando a injustiça se torna insuportável.", "aggettivo: intollerabile"),
        ("Cammino controcorrente anche quando è difficile farlo.", "controcorrente", "Caminho contra a corrente mesmo quando é difícil.", "avverbio: nel senso contrario"),
        # Vol 4
        ("Non mi fermo davanti ai muri che cercano di bloccarmi.", "bloccarmi", "Não me paro diante dos muros que tentam me bloquear.", "verbo bloccare + pronome"),
        ("Il silenzio è complicità, e io non voglio essere complice.", "complicità", "O silêncio é cumplicidade, e eu não quero ser cúmplice.", "sostantivo: partecipazione passiva"),
        ("Grido la verità anche quando fa paura ascoltarla.", "verità", "Grito a verdade mesmo quando dá medo ouvi-la.", "sostantivo: realtà, contrario di bugia"),
        ("Mi rifiuto di obbedire a ordini che vanno contro la coscienza.", "coscienza", "Me recuso a obedecer a ordens que vão contra a consciência.", "sostantivo: senso morale"),
        # Vol 5
        ("La generazione che sfida il passato costruisce il futuro.", "sfida", "A geração que desafia o passado constrói o futuro.", "verbo sfidare: affrontare con coraggio"),
        ("Non ho paura di essere diverso dalla massa.", "massa", "Não tenho medo de ser diferente da massa.", "sostantivo: insieme indistinto di persone"),
        ("La rivoluzione inizia dentro di noi prima che fuori.", "rivoluzione", "A revolução começa dentro de nós antes que fora.", "sostantivo: cambiamento radicale"),
        ("Lottiamo per un mondo più giusto e libero per tutti.", "giusto", "Lutamos por um mundo mais justo e livre para todos.", "aggettivo: equo, corretto"),
        # Vol 6
        ("Non lascio che la paura del giudizio mi metta a tacere.", "giudizio", "Não deixo que o medo do julgamento me faça calar.", "sostantivo: opinione, valutazione"),
        ("Ogni forma d'arte può essere un atto di ribellione.", "ribellione", "Toda forma de arte pode ser um ato de rebelião.", "sostantivo: azione di opporsi"),
        ("Mi vesto come voglio e non mi importa cosa pensano gli altri.", "importa", "Me visto como quero e não me importa o que os outros pensam.", "verbo importare: avere importanza"),
        ("Non si può fermare chi crede nella propria causa.", "causa", "Não se pode parar quem acredita na própria causa.", "sostantivo: ragione per cui si lotta"),
        # Vol 7
        ("Ho deciso di seguire il mio cuore invece delle convenzioni.", "convenzioni", "Decidi seguir meu coração em vez das convenções.", "sostantivo plurale: regole sociali"),
        ("La gioventù ha sempre il diritto di mettere in discussione tutto.", "discussione", "A juventude sempre tem o direito de questionar tudo.", "sostantivo: dibattito, confronto"),
        ("Non accetto compromessi quando si tratta di dignità.", "dignità", "Não aceito compromissos quando se trata de dignidade.", "sostantivo: valore personale"),
        ("Mi alzo ogni giorno con la volontà di cambiare qualcosa.", "volontà", "Me levanto todo dia com a vontade de mudar algo.", "sostantivo: desiderio forte"),
        # Vol 8
        ("Il potere teme chi non ha paura di parlare chiaramente.", "chiaramente", "O poder teme quem não tem medo de falar claramente.", "avverbio: in modo chiaro"),
        ("Rompere gli schemi è l'unico modo per progredire.", "schemi", "Quebrar os esquemas é o único jeito de progredir.", "sostantivo plurale: modelli, sistemi"),
        ("Non mi piace l'omologazione, preferisco la differenza.", "omologazione", "Não gosto da homologação, prefiro a diferença.", "sostantivo: uniformità imposta"),
        ("Chi resiste all'ingiustizia è già un eroe per me.", "resiste", "Quem resiste à injustiça já é um herói para mim.", "verbo resistere: opporsi"),
        # Vol 9
        ("La musica ribelle è la colonna sonora della mia vita.", "colonna", "A música rebelde é a trilha sonora da minha vida.", "sostantivo: struttura portante"),
        ("Non voglio adattarmi, voglio che il mondo si adatti a me.", "adattarmi", "Não quero me adaptar, quero que o mundo se adapte a mim.", "verbo adattarsi + pronome"),
        ("Ogni piccola protesta è un passo verso la libertà.", "protesta", "Cada pequeno protesto é um passo em direção à liberdade.", "sostantivo: manifestazione di disaccordo"),
        ("Chi non si ribella accetta implicitamente l'ingiustizia.", "implicitamente", "Quem não se rebela aceita implicitamente a injustiça.", "avverbio: in modo non esplicito"),
        # Vol 10
        ("La mia ribellione è pacifica ma decisa e coerente.", "coerente", "Minha rebelião é pacífica mas decidida e coerente.", "aggettivo: in accordo con i propri valori"),
        ("Ho smesso di chiedere permesso per essere me stesso.", "permesso", "Parei de pedir permissão para ser eu mesmo.", "sostantivo: autorizzazione"),
        ("L'arte è il mezzo più potente di ribellione contro il sistema.", "potente", "A arte é o meio mais poderoso de rebelião contra o sistema.", "aggettivo: forte, efficace"),
        ("Viviamo in un'epoca in cui il coraggio fa la differenza.", "differenza", "Vivemos em uma época em que a coragem faz a diferença.", "sostantivo: distinzione, cambiamento"),
    ],
    "nostalgia": [
        # Vol 1
        ("Chiudo gli occhi e rivedo i giorni della mia infanzia.", "infanzia", "Fecho os olhos e revejo os dias da minha infância.", "sostantivo: periodo dell'età giovane"),
        ("Il profumo del pane appena sfornato mi riporta a casa.", "sfornato", "O cheiro do pão recém-assado me leva de volta para casa.", "participio passato di sfornare"),
        ("Guardo le vecchie fotografie e sento il cuore stringersi.", "fotografie", "Olho as fotos antigas e sinto o coração apertar.", "sostantivo plurale: immagini del passato"),
        ("La canzone che suonava mia madre mi fa sempre piangere.", "suonava", "A música que minha mãe tocava sempre me faz chorar.", "verbo suonare: imperfetto"),
        # Vol 2
        ("Vorrei tornare ai pomeriggi d'estate della mia giovinezza.", "giovinezza", "Eu queria voltar às tardes de verão da minha juventude.", "sostantivo: periodo della vita giovane"),
        ("I sapori della cucina di casa mi mancano ogni giorno.", "sapori", "Os sabores da cozinha de casa me fazem falta todo dia.", "sostantivo plurale: gusti"),
        ("Penso spesso al paese dove sono cresciuto.", "cresciuto", "Penso frequentemente na cidade onde cresci.", "participio passato di crescere"),
        ("Le serate in famiglia avevano un calore speciale.", "calore", "As noitadas em família tinham um calor especial.", "sostantivo: tepore, affetto"),
        # Vol 3
        ("Mi manca la semplicità dei tempi andati.", "semplicità", "Sinto falta da simplicidade dos tempos passados.", "sostantivo: qualità di essere semplice"),
        ("Il passato è un paese straniero dove non si può tornare.", "straniero", "O passado é um país estrangeiro onde não se pode voltar.", "aggettivo: di altro paese"),
        ("Sento ancora la voce di mio nonno che mi racconta storie.", "racconta", "Ainda ouço a voz do meu avô me contando histórias.", "verbo raccontare: narrare"),
        ("Ogni cosa vecchia porta con sé un ricordo perduto.", "perduto", "Cada coisa velha traz consigo uma memória perdida.", "aggettivo: smarrito"),
        # Vol 4
        ("Quando sento quella melodia, torno bambino per un istante.", "melodia", "Quando ouço aquela melodia, volto a ser criança por um instante.", "sostantivo: sequenza di note musicali"),
        ("La nostalgia è un dolore dolce che non vuoi lasciare andare.", "dolce", "A nostalgia é uma dor doce que não quer deixar ir.", "aggettivo: piacevole ma triste"),
        ("I giochi dell'infanzia mi sembrano ora un sogno lontano.", "giochi", "As brincadeiras da infância me parecem agora um sonho distante.", "sostantivo plurale: attività per bambini"),
        ("Riconosco ancora la strada dove andavo a scuola da piccolo.", "riconosco", "Ainda reconheço a rua onde ia para a escola quando pequeno.", "verbo riconoscere: identificare"),
        # Vol 5
        ("Ogni vecchia canzone è una macchina del tempo.", "macchina", "Cada música antiga é uma máquina do tempo.", "sostantivo: veicolo, strumento"),
        ("Gli amici di scuola sono dispersi in tutto il mondo.", "dispersi", "Os amigos da escola estão espalhados pelo mundo inteiro.", "aggettivo: separati, lontani"),
        ("Il sapore di certe pietanze mi fa tornare indietro di anni.", "pietanze", "O sabor de certos pratos me faz voltar anos atrás.", "sostantivo plurale: piatti di cibo"),
        ("Sento nostalgia per le domeniche in famiglia d'un tempo.", "domeniche", "Sinto nostalgia pelos domingos em família de antigamente.", "sostantivo plurale: settimo giorno"),
        # Vol 6
        ("Il quartiere dove sono nato è cambiato ma non nella memoria.", "memoria", "O bairro onde nasci mudou mas não na memória.", "sostantivo: capacità di ricordare"),
        ("Certe parole mi ricordano conversazioni dimenticate.", "conversazioni", "Certas palavras me lembram conversas esquecidas.", "sostantivo plurale: dialoghi"),
        ("I vecchi giocattoli conservati in soffitta hanno un'anima.", "soffitta", "Os brinquedos velhos guardados no sótão têm uma alma.", "sostantivo: ultimo piano di una casa"),
        ("Rivedo nei sogni i luoghi dove ho vissuto da giovane.", "vissuto", "Revejo nos sonhos os lugares onde vivi quando jovem.", "participio passato di vivere"),
        # Vol 7
        ("Ogni anniversario mi porta un misto di gioia e malinconia.", "anniversario", "Cada aniversário me traz uma mistura de alegria e melancolia.", "sostantivo: ricorrenza annuale"),
        ("Le lettere scritte a mano hanno un valore inestimabile.", "inestimabile", "As cartas escritas à mão têm um valor inestimável.", "aggettivo: che non si può calcolare"),
        ("Mi mancano le risate spenserate di quando ero ragazzo.", "spenserate", "Sinto falta das risadas despreocupadas de quando era jovem.", "aggettivo: senza pensieri"),
        ("La casa della mia infanzia esiste solo nei miei ricordi.", "infanzia", "A casa da minha infância existe só nas minhas memórias.", "sostantivo: periodo della vita giovane"),
        # Vol 8
        ("Ogni tramonto mi riporta a quei momenti irripetibili.", "irripetibili", "Cada pôr do sol me leva de volta àqueles momentos irrepetíveis.", "aggettivo: che non si possono ripetere"),
        ("La nostalgia non è malattia, è il segno di aver amato.", "malattia", "A nostalgia não é doença, é o sinal de ter amado.", "sostantivo: condizione patologica"),
        ("Sento il profumo della pioggia e torno alla mia infanzia.", "pioggia", "Sinto o cheiro da chuva e volto à minha infância.", "sostantivo: acqua che cade dal cielo"),
        ("I film vecchi mi fanno rivivere emozioni perdute.", "rivivere", "Os filmes antigos me fazem reviver emoções perdidas.", "verbo: vivere di nuovo"),
        # Vol 9
        ("Conservo ogni biglietto e fotografia come un tesoro.", "conservo", "Guardo cada bilhete e fotografia como um tesouro.", "verbo conservare: tenere con cura"),
        ("Il tempo non si ferma ma la memoria sì.", "ferma", "O tempo não para mas a memória sim.", "verbo fermarsi: cessare"),
        ("La storia della mia famiglia è incisa nel mio cuore.", "incisa", "A história da minha família está gravada no meu coração.", "participio passato di incidere"),
        ("Certe emozioni non si spiegano, si sentono soltanto.", "soltanto", "Certas emoções não se explicam, se sentem somente.", "avverbio: solo, solamente"),
        # Vol 10
        ("Ogni vecchia fotografia vale più di mille parole.", "fotografia", "Cada foto antiga vale mais que mil palavras.", "sostantivo: immagine impressa"),
        ("La nostalgia mi insegna ad apprezzare il presente.", "insegna", "A nostalgia me ensina a apreciar o presente.", "verbo insegnare: far imparare"),
        ("Rivivo il passato nei sogni e mi sveglio con il sorriso.", "rivivo", "Revivo o passado nos sonhos e acordo com o sorriso.", "verbo rivivere: vivere di nuovo"),
        ("I migliori ricordi sono quelli che non svaniscono mai.", "svaniscono", "As melhores lembranças são aquelas que nunca desaparecem.", "verbo svanire: sparire"),
    ],
    "vita": [
        # Vol 1
        ("La vita è troppo breve per rimpianti e paure inutili.", "rimpianti", "A vida é curta demais para arrependimentos e medos inúteis.", "sostantivo plurale: dispiaceri"),
        ("Ogni mattina è una nuova possibilità di iniziare.", "possibilità", "Cada manhã é uma nova possibilidade de começar.", "sostantivo: opportunità"),
        ("Vivo il presente perché il futuro è incerto.", "incerto", "Vivo o presente porque o futuro é incerto.", "aggettivo: non sicuro"),
        ("La vita mi ha insegnato che niente è per sempre.", "insegnato", "A vida me ensinou que nada é para sempre.", "participio passato di insegnare"),
        # Vol 2
        ("Ogni esperienza, buona o cattiva, mi ha reso più forte.", "esperienza", "Cada experiência, boa ou ruim, me tornou mais forte.", "sostantivo: vissuto, conoscenza"),
        ("Il tempo è il bene più prezioso che abbiamo.", "prezioso", "O tempo é o bem mais precioso que temos.", "aggettivo: di grande valore"),
        ("Bisogna saper cogliere le occasioni prima che svaniscano.", "cogliere", "É preciso saber aproveitar as oportunidades antes que desapareçam.", "verbo: prendere al momento giusto"),
        ("La vita è bella soprattutto nei dettagli più piccoli.", "dettagli", "A vida é bonita especialmente nos detalhes mais pequenos.", "sostantivo plurale: particolari"),
        # Vol 3
        ("Ogni giorno che passa è un regalo da non sprecare.", "sprecare", "Cada dia que passa é um presente a não desperdiçar.", "verbo: usare male, gettare via"),
        ("Le difficoltà della vita ci rendono più resilienti.", "resilienti", "As dificuldades da vida nos tornam mais resilientes.", "aggettivo: capaci di riprendersi"),
        ("Ho imparato a sorridere anche quando fa male.", "sorridere", "Aprendi a sorrir mesmo quando dói.", "verbo: mostrare gioia col viso"),
        ("La felicità non si trova, si costruisce giorno dopo giorno.", "costruisce", "A felicidade não se encontra, se constrói dia após dia.", "verbo costruire: edificare"),
        # Vol 4
        ("Non sprecare energie su chi non merita la tua attenzione.", "merita", "Não desperdice energias em quem não merece sua atenção.", "verbo meritare: essere degno"),
        ("La vita scorre veloce, quindi dobbiamo assaporarla.", "assaporarla", "A vida corre rápido, então devemos saboreá-la.", "verbo assaporare + pronome"),
        ("Ho scelto di circondarmi di persone positive e sincere.", "positiva", "Escolhi me cercar de pessoas positivas e sinceras.", "aggettivo: ottimista"),
        ("Ogni fallimento è una lezione travestita da sconfitta.", "lezione", "Cada fracasso é uma lição disfarçada de derrota.", "sostantivo: insegnamento"),
        # Vol 5
        ("La vita non è sempre giusta, ma è sempre istruttiva.", "istruttiva", "A vida nem sempre é justa, mas sempre é instrutiva.", "aggettivo: che insegna qualcosa"),
        ("Vivo senza rimpianti perché ho dato il massimo.", "rimpianti", "Vivo sem arrependimentos porque dei o máximo.", "sostantivo plurale: dispiaceri"),
        ("Le scelte difficili ci definiscono come persone.", "definiscono", "As escolhas difíceis nos definem como pessoas.", "verbo definire: determinare"),
        ("Il coraggio non è assenza di paura, ma agire nonostante essa.", "nonostante", "A coragem não é ausência de medo, mas agir apesar dele.", "preposizione: malgrado"),
        # Vol 6
        ("Nella vita contano le relazioni, non le cose materiali.", "materiali", "Na vida contam os relacionamentos, não as coisas materiais.", "aggettivo: fisico, tangibile"),
        ("Ho capito che la salute è il vero lusso della vita.", "lusso", "Entendi que a saúde é o verdadeiro luxo da vida.", "sostantivo: bene raro e costoso"),
        ("Ogni persona che incontro mi arricchisce in qualche modo.", "arricchisce", "Cada pessoa que encontro me enriquece de alguma forma.", "verbo arricchire: rendere più ricco"),
        ("Scegliere la felicità è un atto di coraggio quotidiano.", "quotidiano", "Escolher a felicidade é um ato de coragem diário.", "aggettivo: di ogni giorno"),
        # Vol 7
        ("La vita è un viaggio e non una destinazione.", "destinazione", "A vida é uma viagem e não um destino.", "sostantivo: luogo di arrivo"),
        ("Non rimando mai a domani ciò che posso fare oggi.", "rimando", "Nunca adio para amanhã o que posso fazer hoje.", "verbo rimandare: posticipare"),
        ("I momenti semplici sono spesso i più belli.", "semplici", "Os momentos simples são muitas vezes os mais bonitos.", "aggettivo: non complicati"),
        ("La vita cambia direzione quando meno ce lo aspettiamo.", "aspettiamo", "A vida muda de direção quando menos esperamos.", "verbo aspettarsi: prevedere"),
        # Vol 8
        ("Ho imparato a lasciar andare ciò che non posso controllare.", "controllare", "Aprendi a deixar ir o que não posso controlar.", "verbo: governare, gestire"),
        ("Vivere con gratitudine trasforma ogni giorno.", "gratitudine", "Viver com gratidão transforma cada dia.", "sostantivo: sentimento di riconoscenza"),
        ("La vita è il risultato delle scelte che facciamo ogni giorno.", "risultato", "A vida é o resultado das escolhas que fazemos todo dia.", "sostantivo: conseguenza, esito"),
        ("Non esistono strade perfette, solo strade percorse.", "percorse", "Não existem estradas perfeitas, apenas estradas percorridas.", "participio passato di percorrere"),
        # Vol 9
        ("Il senso della vita si trova nelle piccole cose.", "senso", "O sentido da vida se encontra nas pequenas coisas.", "sostantivo: significato, scopo"),
        ("Cambiare idea non è debolezza, è saggezza.", "saggezza", "Mudar de ideia não é fraqueza, é sabedoria.", "sostantivo: qualità di chi è saggio"),
        ("La vita mi ha dato tutto ciò di cui avevo bisogno.", "bisogno", "A vida me deu tudo o que eu precisava.", "sostantivo: necessità"),
        ("Non smettere mai di imparare è il segreto della giovinezza.", "giovinezza", "Nunca parar de aprender é o segredo da juventude.", "sostantivo: periodo della vita giovane"),
        # Vol 10
        ("Ogni tramonto è una promessa di un nuovo domani.", "promessa", "Cada pôr do sol é uma promessa de um novo amanhã.", "sostantivo: impegno preso"),
        ("Ho scelto di costruire ponti invece di muri.", "ponti", "Escolhi construir pontes em vez de muros.", "sostantivo plurale: strutture di collegamento"),
        ("La vita è più bella quando la condividi con gli altri.", "condividi", "A vida é mais bonita quando a compartilhas com os outros.", "verbo condividere: dividere con altri"),
        ("Ogni respiro è un invito a vivere pienamente.", "rispiro", "Cada respiração é um convite a viver plenamente.", "sostantivo: azione del respirare"),
    ],
}

TEMA_MAP_EXTRA = {
    "amicizia": "amicizia",
    "ribellione": "ribellione",
    "nostalgia": "nostalgia",
    "vita": "vita",
}

def make_estrofa(idx, frase_tuple):
    testo, parola, traducao, dica = frase_tuple
    lacuna = testo.replace(parola, "___", 1)
    return {
        "id": idx,
        "texto_completo": testo,
        "texto_lacuna": lacuna,
        "palavra_oculta": parola,
        "traducao": traducao,
        "dica": dica
    }

def is_generic(estrofe_list):
    for e in estrofe_list:
        if "Questo e un verso" in e.get("texto_completo", "").replace("è", "e"):
            return True
    return False

# Load
with open("data/canzoni.json", "r", encoding="utf-8") as f:
    data = json.load(f)

songs = data["canzoni"]
fixed = 0
skipped = 0

tema_usage = {t: 0 for t in TEMAS_EXTRA}

for song in songs:
    sid = song["id"]
    num_match = re.match(r"can_(\d+)", sid)
    if not num_match:
        continue
    num = int(num_match.group(1))
    if not (51 <= num <= 150):
        continue

    tema = song.get("tema", "")
    tema_key = TEMA_MAP_EXTRA.get(tema)

    if not tema_key:
        continue  # already fixed by previous script

    if not is_generic(song.get("estrofes", [])):
        skipped += 1
        continue

    pool = TEMAS_EXTRA[tema_key]
    start = tema_usage[tema_key]

    frases = []
    for i in range(4):
        frases.append(pool[(start + i) % len(pool)])
    tema_usage[tema_key] += 4

    new_estrofes = [make_estrofa(i+1, frases[i]) for i in range(4)]
    new_vocab = [f[1] for f in frases]

    song["estrofes"] = new_estrofes
    song["vocabulario_chave"] = new_vocab
    fixed += 1

print("Fixed extra: " + str(fixed))
print("Skipped: " + str(skipped))

# Save
output = json.dumps(data, ensure_ascii=False, indent=2)
with open("data/canzoni.json", "w", encoding="utf-8", newline="\n") as f:
    f.write(output)

print("Saved data/canzoni.json")

# Quick verify
print("\nSample check:")
for s in data["canzoni"]:
    if s["id"] in ("can_057", "can_058", "can_059", "can_060"):
        print(s["id"] + " - " + s["titulo"])
        if s["estrofes"]:
            e = s["estrofes"][0]
            print("  Estrofe 1: " + e["texto_completo"])
            print("  Oculta: " + e["palavra_oculta"])
