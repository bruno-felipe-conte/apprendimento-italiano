import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

# =============================================================================
# Pool de frases reais por tema - 50 frases por tema (5 frases x 10 vols)
# Estrutura: (texto_completo, palavra_oculta, traducao, dica)
# =============================================================================

TEMAS = {
    "amore": [
        # Vol 1
        ("Ti amo con tutto il cuore, ogni giorno di più.", "cuore", "Eu te amo com todo o coração, cada dia mais.", "organo centrale / sinonimo: anima"),
        ("I tuoi occhi brillano come le stelle nel cielo.", "occhi", "Seus olhos brilham como as estrelas no céu.", "sostantivo plurale: gli organi della vista"),
        ("Quando sei lontana, mi manca la tua voce.", "manca", "Quando você está longe, sinto falta da sua voz.", "verbo mancare: essere assente"),
        ("L'amore è una fiamma che non si spegne mai.", "fiamma", "O amor é uma chama que nunca se apaga.", "sostantivo: sinonimo di fuoco"),
        # Vol 2
        ("Il mio cuore batte forte ogni volta che ti vedo.", "batte", "Meu coração bate forte cada vez que te vejo.", "verbo battere: pulsare"),
        ("Con te, ogni giorno diventa speciale e unico.", "speciale", "Com você, cada dia se torna especial e único.", "aggettivo: straordinario"),
        ("Il tuo sorriso illumina la mia giornata.", "sorriso", "Seu sorriso ilumina o meu dia.", "sostantivo: espressione di felicità"),
        ("Ti penso sempre, anche nei momenti più difficili.", "penso", "Penso em você sempre, mesmo nos momentos mais difíceis.", "verbo pensare: avere in mente"),
        # Vol 3
        ("Ogni notte sogno di stare tra le tue braccia.", "braccia", "Toda noite sonho em estar entre seus braços.", "sostantivo plurale di braccio"),
        ("La tua voce è la musica più dolce per me.", "dolce", "Sua voz é a música mais doce para mim.", "aggettivo: soave, piacevole"),
        ("Insieme siamo forti, separati siamo soli.", "forti", "Juntos somos fortes, separados estamos sós.", "aggettivo: robusti, potenti"),
        ("Ti aspetto ogni sera davanti alla finestra.", "aspetto", "Espero por você toda tarde diante da janela.", "verbo aspettare: attendere"),
        # Vol 4
        ("Il primo bacio che ci siamo dati non lo scorderò mai.", "bacio", "O primeiro beijo que nos demos nunca esquecerei.", "sostantivo: gesto d'amore"),
        ("Senza di te, la vita non ha più sapore.", "sapore", "Sem você, a vida não tem mais sabor.", "sostantivo: gusto, senso"),
        ("Mi hai insegnato il significato della parola amore.", "insegnato", "Você me ensinou o significado da palavra amor.", "participio passato di insegnare"),
        ("Il tempo vola quando sono con te.", "vola", "O tempo voa quando estou com você.", "verbo volare: passare velocemente"),
        # Vol 5
        ("La nostra storia è scritta nelle stelle.", "stelle", "Nossa história está escrita nas estrelas.", "sostantivo plurale di stella"),
        ("Ti cerco tra la folla ma non ti trovo.", "folla", "Procuro você na multidão mas não te encontro.", "sostantivo: gruppo grande di persone"),
        ("Hai cambiato la mia vita per sempre.", "cambiato", "Você mudou minha vida para sempre.", "participio passato di cambiare"),
        ("Il tuo profumo rimane con me tutto il giorno.", "profumo", "Seu perfume fica comigo o dia todo.", "sostantivo: fragranza"),
        # Vol 6
        ("Non ho parole per dirti quanto ti voglio bene.", "parole", "Não tenho palavras para dizer o quanto gosto de você.", "sostantivo plurale: termini, vocaboli"),
        ("Ogni volta che sorridi, il mondo diventa più bello.", "sorridi", "Cada vez que você sorri, o mundo fica mais bonito.", "verbo sorridere: mostrare gioia"),
        ("Mi fido di te con tutto me stesso.", "fido", "Confio em você com todo eu mesmo.", "verbo fidarsi: avere fiducia"),
        ("Sei il mio sole nelle giornate più buie.", "buie", "Você é o meu sol nos dias mais sombrios.", "aggettivo: scure, senza luce"),
        # Vol 7
        ("Vorrei fermare il tempo per stare sempre con te.", "fermare", "Eu queria parar o tempo para ficar sempre com você.", "infinito: bloccare, immobilizzare"),
        ("La tua risata è la mia canzone preferita.", "risata", "Sua risada é minha música favorita.", "sostantivo: atto del ridere"),
        ("Tu sei la ragione per cui sono felice.", "ragione", "Você é o motivo pelo qual sou feliz.", "sostantivo: causa, motivo"),
        ("Quando piangi, voglio asciugare le tue lacrime.", "lacrime", "Quando você chora, quero enxugar suas lágrimas.", "sostantivo plurale: gocce di pianto"),
        # Vol 8
        ("Il tuo abbraccio è il posto più sicuro del mondo.", "abbraccio", "Seu abraço é o lugar mais seguro do mundo.", "sostantivo: gesto di affetto"),
        ("Siamo diversi, ma ci completiamo a vicenda.", "completiamo", "Somos diferentes, mas nos completamos mutuamente.", "verbo completare: riempire"),
        ("Con ogni canzone penso a te, amore mio.", "canzone", "Com cada música penso em você, meu amor.", "sostantivo: composizione musicale"),
        ("Il nostro amore è come il vino, migliora col tempo.", "migliora", "Nosso amor é como o vinho, melhora com o tempo.", "verbo migliorare: diventare meglio"),
        # Vol 9
        ("Ti guardo negli occhi e vedo il mio futuro.", "futuro", "Olho nos seus olhos e vejo meu futuro.", "sostantivo: tempo che verrà"),
        ("Sarò sempre al tuo fianco, qualunque cosa accada.", "fianco", "Estarei sempre ao seu lado, aconteça o que acontecer.", "sostantivo: lato, parte laterale"),
        ("L'amore non si spiega, si sente nel petto.", "petto", "O amor não se explica, se sente no peito.", "sostantivo: parte anteriore del torso"),
        ("Ogni giorno che passa, ti amo di più.", "passa", "Cada dia que passa, te amo mais.", "verbo passare: trascorrere"),
        # Vol 10
        ("Il nostro primo incontro fu come un sogno.", "incontro", "Nosso primeiro encontro foi como um sonho.", "sostantivo: momento di ritrovarsi"),
        ("Con te ho imparato cos'è la felicità vera.", "felicità", "Com você aprendi o que é a felicidade verdadeira.", "sostantivo: stato di gioia"),
        ("Hai preso il mio cuore e non me lo restituisci.", "restituisci", "Você pegou meu coração e não me devolve.", "verbo restituire: ridare"),
        ("Innamorarsi di te è stata la mia migliore scelta.", "scelta", "Apaixonar-me por você foi minha melhor escolha.", "sostantivo: decisione, opzione"),
        # Extras (para vocabulario_chave)
        ("La nostra storia d'amore non finirà mai.", "storia", "Nossa história de amor nunca vai terminar.", "sostantivo: narrazione, vicenda"),
        ("L'amore che provo per te cresce ogni giorno.", "cresce", "O amor que sinto por você cresce cada dia.", "verbo crescere: aumentare"),
        ("Amarti è la cosa più bella che mi sia capitata.", "amarti", "Amar você é a coisa mais bonita que me aconteceu.", "infinito di amare + pronome"),
        ("Nei tuoi occhi vedo tutto il mondo.", "mondo", "Em seus olhos vejo o mundo inteiro.", "sostantivo: la terra, l'universo"),
        ("Il tuo nome è inciso nel mio cuore per sempre.", "inciso", "Seu nome está gravado no meu coração para sempre.", "participio passato di incidere"),
        ("Ogni bacio tuo è come il primo.", "primo", "Cada beijo seu é como o primeiro.", "aggettivo numerale ordinale"),
        ("Sei l'unica persona che capisce la mia anima.", "anima", "Você é a única pessoa que entende minha alma.", "sostantivo: spirito interiore"),
        ("Ti amo non solo per quello che sei, ma per quello che mi fai sentire.", "sentire", "Te amo não só pelo que você é, mas pelo que me faz sentir.", "verbo sentire: percepire"),
        ("La distanza non può separare i cuori che si amano.", "separare", "A distância não pode separar os corações que se amam.", "verbo: dividere, allontanare"),
        ("Ogni mattina mi sveglio pensando al tuo viso.", "viso", "Toda manhã acordo pensando no seu rosto.", "sostantivo: la faccia"),
    ],
    "estate": [
        # Vol 1
        ("Il sole brilla forte sulla spiaggia dorata.", "brilla", "O sol brilha forte na praia dourada.", "verbo brillare: splendere"),
        ("Il mare è azzurro e profondo come il cielo.", "azzurro", "O mar é azul e profundo como o céu.", "aggettivo: colore blu"),
        ("I bambini giocano sulla sabbia con grande gioia.", "sabbia", "As crianças brincam na areia com grande alegria.", "sostantivo: granuli minerali della spiaggia"),
        ("L'estate porta con sé calore e spensieratezza.", "calore", "O verão traz consigo calor e despreocupação.", "sostantivo: temperatura elevata"),
        # Vol 2
        ("Mangiamo il gelato seduti all'ombra degli alberi.", "gelato", "Comemos sorvete sentados à sombra das árvores.", "sostantivo: dolce freddo"),
        ("Le onde del mare ci accarezzano i piedi.", "onde", "As ondas do mar nos acariciam os pés.", "sostantivo plurale: movimento dell'acqua"),
        ("Di sera, facciamo lunghe passeggiate sul lungomare.", "lungomare", "À tarde, fazemos longas caminhadas à beira-mar.", "sostantivo: strada vicino al mare"),
        ("Il tramonto dipinge il cielo di rosso e arancione.", "tramonto", "O pôr do sol pinta o céu de vermelho e laranja.", "sostantivo: fine del giorno"),
        # Vol 3
        ("La brezza marina rinfresca le calde giornate estive.", "brezza", "A brisa marítima refresca os quentes dias de verão.", "sostantivo: vento leggero"),
        ("Facciamo il bagno nelle acque cristalline del mare.", "bagno", "Nos banhamos nas águas cristalinas do mar.", "sostantivo: immersione nell'acqua"),
        ("Il profumo del mare mi rilassa e mi fa sognare.", "rilassa", "O cheiro do mar me relaxa e me faz sonhar.", "verbo rilassare: calmare"),
        ("Quest'estate ho conosciuto persone meravigliose.", "meravigliose", "Neste verão conheci pessoas maravilhosas.", "aggettivo: straordinarie, stupende"),
        # Vol 4
        ("Gli ombrelloni colorati decorano la spiaggia.", "ombrelloni", "Os guarda-sóis coloridos decoram a praia.", "sostantivo plurale: grandi ombrelli da spiaggia"),
        ("La sera, seduti sul terrazzo, guardiamo le stelle.", "terrazzo", "À noite, sentados na varanda, olhamos as estrelas.", "sostantivo: spazio aperto sulla casa"),
        ("I bambini raccolgono conchiglie sulla riva del mare.", "conchiglie", "As crianças coletam conchas à beira do mar.", "sostantivo plurale: gusci di molluschi"),
        ("Beviamo limonata fresca sotto l'ombrellone.", "limonata", "Bebemos limonada fresca sob o guarda-sol.", "sostantivo: bevanda con limone"),
        # Vol 5
        ("Il sole tramonta lentamente dietro le montagne.", "tramonta", "O sol se põe lentamente atrás das montanhas.", "verbo tramontare: scendere all'orizzonte"),
        ("Ci sdraiamo sulla sabbia e guardiamo il cielo.", "sdraiamo", "Deitamo-nos na areia e olhamos o céu.", "verbo sdraiarsi: distendersi"),
        ("La frutta di stagione estiva è dolce e succosa.", "stagione", "A fruta da estação de verão é doce e suculenta.", "sostantivo: periodo dell'anno"),
        ("Il sole abbronza la pelle durante le lunghe giornate.", "abbronza", "O sol bronzeia a pele durante os longos dias.", "verbo abbronzare: scurire la pelle"),
        # Vol 6
        ("I gabbiani volano bassi sulla riva del mare.", "gabbiani", "As gaivotas voam baixas à beira do mar.", "sostantivo plurale: uccelli marini"),
        ("Mangiamo pesce fresco con il vino bianco freddo.", "pesce", "Comemos peixe fresco com vinho branco gelado.", "sostantivo: animale acquatico"),
        ("Costruiamo castelli di sabbia sulla spiaggia.", "castelli", "Construímos castelos de areia na praia.", "sostantivo plurale di castello"),
        ("Il cielo estivo è di un blu intenso e profondo.", "intenso", "O céu de verão é de um azul intenso e profundo.", "aggettivo: forte, concentrato"),
        # Vol 7
        ("Facciamo una gita in barca per vedere i fondali.", "fondali", "Fazemos um passeio de barco para ver o fundo do mar.", "sostantivo plurale: fondo del mare"),
        ("Sotto la luna d'agosto, tutto è silenzioso.", "silenzioso", "Sob a lua de agosto, tudo é silencioso.", "aggettivo: quieto, senza rumore"),
        ("L'acqua del mare è ancora fresca di mattina.", "fresca", "A água do mar ainda está fresca de manhã.", "aggettivo: con bassa temperatura"),
        ("Le cicale cantano senza sosta durante il pomeriggio.", "cicale", "As cigarras cantam sem parar durante a tarde.", "sostantivo plurale: insetti estivi rumorosi"),
        # Vol 8
        ("Il primo tuffo nell'acqua è sempre una gioia.", "tuffo", "O primeiro mergulho na água é sempre uma alegria.", "sostantivo: azione di immergersi"),
        ("Raccogliamo frutta fresca nei campi assolati.", "assolati", "Colhemos frutas frescas nos campos ensolarados.", "aggettivo: pieni di sole"),
        ("La pizzeria sul lungomare è sempre affollata.", "affollata", "A pizzaria à beira-mar está sempre cheia de gente.", "aggettivo: piena di persone"),
        ("Dormiamo con le finestre aperte per il caldo.", "finestre", "Dormimos com as janelas abertas por causa do calor.", "sostantivo plurale: aperture nel muro"),
        # Vol 9
        ("L'estate è la stagione dei concerti all'aperto.", "concerti", "O verão é a estação dos shows ao ar livre.", "sostantivo plurale: spettacoli musicali"),
        ("I colori dell'estate sono vivaci e luminosi.", "vivaci", "As cores do verão são vibrantes e luminosas.", "aggettivo: brillanti, intensi"),
        ("Andiamo a fare snorkeling nelle acque del golfo.", "golfo", "Vamos fazer snorkeling nas águas do golfo.", "sostantivo: insenatura del mare"),
        ("La spiaggia si riempie di turisti ad agosto.", "turisti", "A praia se enche de turistas em agosto.", "sostantivo plurale: visitatori"),
        # Vol 10
        ("Con la famiglia, ogni estate è un'avventura.", "avventura", "Com a família, todo verão é uma aventura.", "sostantivo: esperienza emozionante"),
        ("Il mare d'estate è pieno di barche a vela.", "vela", "O mar no verão está cheio de barcos à vela.", "sostantivo: tessuto che muove la barca"),
        ("Ogni estate mi porta ricordi bellissimi.", "ricordi", "Todo verão me traz lembranças belíssimas.", "sostantivo plurale: memorie"),
        ("La notte d'estate è calda e piena di suoni.", "suoni", "A noite de verão é quente e cheia de sons.", "sostantivo plurale: rumori, melodie"),
        # Extras
        ("Sotto il sole estivo, tutto sembra più luminoso.", "luminoso", "Sob o sol de verão, tudo parece mais luminoso.", "aggettivo: pieno di luce"),
        ("La brezza marina profuma di sale e libertà.", "profuma", "A brisa marítima cheira a sal e liberdade.", "verbo profumare: avere un profumo"),
        ("Nuotiamo per ore nelle acque tiepide del mare.", "tiepide", "Nadamos por horas nas águas mornas do mar.", "aggettivo: né calde né fredde"),
        ("Il sapore del gelato in estate è ineguagliabile.", "ineguagliabile", "O sabor do sorvete no verão é incomparável.", "aggettivo: che non ha pari"),
        ("Ogni sera il tramonto mi regala emozioni uniche.", "regala", "Toda tarde o pôr do sol me presenteia emoções únicas.", "verbo regalare: dare in dono"),
        ("L'estate finisce troppo presto per i miei gusti.", "gusti", "O verão termina cedo demais para o meu gosto.", "sostantivo plurale: preferenze"),
        ("Beviamo caffè freddo per combattere il caldo.", "combattere", "Bebemos café frio para combater o calor.", "verbo: lottare contro"),
        ("Il profumo della salsedine mi fa venire voglia di mare.", "salsedine", "O cheiro da maresia me dá vontade de mar.", "sostantivo: sale nell'aria marina"),
        ("Le notti estive sono perfette per le passeggiate.", "perfette", "As noites de verão são perfeitas para as caminhadas.", "aggettivo: ideali, senza difetti"),
        ("L'estate italiana è famosa in tutto il mondo.", "famosa", "O verão italiano é famoso no mundo inteiro.", "aggettivo: molto conosciuto"),
    ],
    "notte": [
        # Vol 1
        ("Le stelle brillano nel cielo notturno come diamanti.", "brillano", "As estrelas brilham no céu noturno como diamantes.", "verbo brillare: risplendere"),
        ("La luna piena illumina il paesaggio addormentato.", "illumina", "A lua cheia ilumina a paisagem adormecida.", "verbo illuminare: fare luce su"),
        ("Il silenzio della notte è profondo e misterioso.", "silenzio", "O silêncio da noite é profundo e misterioso.", "sostantivo: assenza di suono"),
        ("Conto le stelle e mi perdo nel loro numero infinito.", "infinito", "Conto as estrelas e me perco em seu número infinito.", "aggettivo: senza fine"),
        # Vol 2
        ("La Via Lattea attraversa il cielo come un fiume di luce.", "Lattea", "A Via Láctea atravessa o céu como um rio de luz.", "aggettivo: relativo al latte"),
        ("Di notte, i pensieri si fanno più profondi e sinceri.", "profondi", "À noite, os pensamentos ficam mais profundos e sinceros.", "aggettivo: intensi, non superficiali"),
        ("Il vento notturno porta con sé un profumo di fiori.", "notturno", "O vento noturno traz consigo um perfume de flores.", "aggettivo: della notte"),
        ("Osservo le costellazioni e penso all'universo infinito.", "costellazioni", "Observo as constelações e penso no universo infinito.", "sostantivo plurale: gruppi di stelle"),
        # Vol 3
        ("Le stelle cadenti portano fortuna a chi le vede.", "cadenti", "As estrelas cadentes trazem sorte a quem as vê.", "aggettivo: che cadono"),
        ("La notte stellata mi fa sentire piccolo ma libero.", "libero", "A noite estrelada me faz sentir pequeno mas livre.", "aggettivo: senza vincoli"),
        ("Il cielo notturno è una mappa dell'universo.", "mappa", "O céu noturno é um mapa do universo.", "sostantivo: rappresentazione geografica"),
        ("Sento il fruscio delle foglie nel buio della notte.", "fruscio", "Ouço o sussurro das folhas no escuro da noite.", "sostantivo: suono leggero delle foglie"),
        # Vol 4
        ("La luce delle stelle impiega anni per raggiungerci.", "raggiungerci", "A luz das estrelas leva anos para nos alcançar.", "verbo raggiungere + pronome"),
        ("Sotto le stelle, mi sento in pace con me stesso.", "pace", "Sob as estrelas, me sinto em paz comigo mesmo.", "sostantivo: tranquillità, armonia"),
        ("La notte porta con sé sogni e visioni meravigliose.", "sogni", "A noite traz consigo sonhos e visões maravilhosas.", "sostantivo plurale: visioni nel sonno"),
        ("I pianeti si muovono lentamente nel cielo notturno.", "pianeti", "Os planetas se movem lentamente no céu noturno.", "sostantivo plurale: corpi celesti"),
        # Vol 5
        ("Il telescopio mi permette di vedere le stelle da vicino.", "telescopio", "O telescópio me permite ver as estrelas de perto.", "sostantivo: strumento ottico"),
        ("Nell'oscurità più profonda, le stelle brillano di più.", "oscurità", "Na escuridão mais profunda, as estrelas brilham mais.", "sostantivo: assenza di luce"),
        ("Il cielo notturno cambia con le stagioni.", "stagioni", "O céu noturno muda com as estações.", "sostantivo plurale: periodi dell'anno"),
        ("Sento la voce del vento che mi chiama nel buio.", "buio", "Ouço a voz do vento que me chama no escuro.", "sostantivo: mancanza di luce"),
        # Vol 6
        ("Il chiaro di luna trasforma il paesaggio in argento.", "argento", "O luar transforma a paisagem em prata.", "sostantivo: metallo prezioso"),
        ("Aspetto l'alba seduto sotto il cielo stellato.", "alba", "Espero o amanhecer sentado sob o céu estrelado.", "sostantivo: inizio del giorno"),
        ("I sogni più belli nascono nelle notti stellate.", "nascono", "Os sonhos mais bonitos nascem nas noites estreladas.", "verbo nascere: venire al mondo"),
        ("La nebbia sale dalla valle e avvolge le stelle.", "nebbia", "A neblina sobe do vale e envolve as estrelas.", "sostantivo: vapore acqueo"),
        # Vol 7
        ("Guardare le stelle mi fa dimenticare i problemi.", "dimenticare", "Olhar as estrelas me faz esquecer os problemas.", "verbo: non ricordare più"),
        ("La Via Lattea è visibile solo lontano dalle città.", "visibile", "A Via Láctea é visível somente longe das cidades.", "aggettivo: che si può vedere"),
        ("Il cielo stellato è il più bel quadro naturale.", "quadro", "O céu estrelado é o mais belo quadro natural.", "sostantivo: opera visiva"),
        ("Ogni stella ha la sua storia scritta nel firmamento.", "firmamento", "Cada estrela tem sua história escrita no firmamento.", "sostantivo: volta celeste"),
        # Vol 8
        ("Il confine tra il cielo e la terra scompare di notte.", "scompare", "O limite entre o céu e a terra desaparece à noite.", "verbo scomparire: non essere più visibile"),
        ("Le lucciole danzano nell'oscurità come piccole stelle.", "lucciole", "Os vagalumes dançam na escuridão como pequenas estrelas.", "sostantivo plurale: insetti luminosi"),
        ("Sento la magia della notte stellata nella mia anima.", "magia", "Sinto a magia da noite estrelada em minha alma.", "sostantivo: potere misterioso"),
        ("L'astronomia mi ha insegnato a guardare il cielo.", "astronomia", "A astronomia me ensinou a olhar o céu.", "sostantivo: scienza dei corpi celesti"),
        # Vol 9
        ("Le stelle non mentono, riflettono la verità.", "verità", "As estrelas não mentem, refletem a verdade.", "sostantivo: realtà, opposto di bugia"),
        ("La luna nuova lascia il cielo completamente buio.", "nuova", "A lua nova deixa o céu completamente escuro.", "aggettivo: senza fase illuminata"),
        ("I filosofi guardavano le stelle per trovare risposte.", "filosofi", "Os filósofos olhavam as estrelas para encontrar respostas.", "sostantivo plurale: pensatori"),
        ("La bellezza del cielo notturno non ha confronti.", "confronti", "A beleza do céu noturno não tem comparação.", "sostantivo plurale: comparazioni"),
        # Vol 10
        ("Le notti senza luna sono perfette per osservare le stelle.", "perfette", "As noites sem lua são perfeitas para observar as estrelas.", "aggettivo: ideali, senza difetti"),
        ("Il mistero dello spazio mi affascina profondamente.", "affascina", "O mistério do espaço me fascina profundamente.", "verbo affascinare: attrarre con forza"),
        ("Ogni notte stellata è un dono della natura.", "dono", "Cada noite estrelada é um presente da natureza.", "sostantivo: regalo"),
        ("La notte è la madre di tutti i sogni e le speranze.", "speranze", "A noite é a mãe de todos os sonhos e esperanças.", "sostantivo plurale: desideri per il futuro"),
        # Extras
        ("Nel cuore della notte, tutto è possibile.", "possibile", "No coração da noite, tudo é possível.", "aggettivo: che può avvenire"),
        ("Le stelle mi guidano come antiche mappe del cielo.", "guidano", "As estrelas me guiam como antigas mapas do céu.", "verbo guidare: condurre"),
        ("Il freddo della notte mi sveglia dai miei pensieri.", "freddo", "O frio da noite me desperta dos meus pensamentos.", "sostantivo: bassa temperatura"),
        ("Giove e Saturno si vedono bene senza telescopio.", "Saturno", "Júpiter e Saturno se veem bem sem telescópio.", "pianeta: il sesto del sistema solare"),
        ("Il cielo notturno è un libro aperto per chi sa leggere.", "leggere", "O céu noturno é um livro aberto para quem sabe ler.", "verbo: interpretare la scrittura"),
        ("La notte silenziosa mi regala momenti di riflessione.", "riflessione", "A noite silenciosa me presenteia momentos de reflexão.", "sostantivo: pensiero profondo"),
        ("Le costellazioni raccontano storie antiche dell'umanità.", "raccontano", "As constelações contam histórias antigas da humanidade.", "verbo raccontare: narrare"),
        ("Il buio della notte non mi spaventa, mi affascina.", "spaventa", "O escuro da noite não me assusta, me fascina.", "verbo spaventare: fare paura"),
        ("Una stella cadente attraversa il cielo in un lampo.", "lampo", "Uma estrela cadente atravessa o céu num relâmpago.", "sostantivo: luce istantanea"),
        ("La notte porta silenzio e la mente si libera.", "libera", "A noite traz silêncio e a mente se liberta.", "verbo liberarsi: diventare libero"),
    ],
    "ballo": [
        # Vol 1
        ("La musica mi entra nel sangue e mi fa ballare.", "sangue", "A música entra no meu sangue e me faz dançar.", "sostantivo: liquido nel corpo"),
        ("Il ritmo della canzone mi trascina sulla pista.", "ritmo", "O ritmo da música me arrasta para a pista.", "sostantivo: cadenza musicale"),
        ("Quando ballo, dimentico tutti i problemi della giornata.", "dimentico", "Quando danço, esqueço todos os problemas do dia.", "verbo dimenticare: non ricordare"),
        ("La pista da ballo è piena di gente felice e spensierata.", "spensierata", "A pista de dança está cheia de gente feliz e despreocupada.", "aggettivo: senza preoccupazioni"),
        # Vol 2
        ("Il mio corpo si muove naturalmente seguendo la musica.", "naturalmente", "Meu corpo se move naturalmente seguindo a música.", "avverbio: in modo spontaneo"),
        ("Balliamo insieme tutta la notte senza fermarci mai.", "fermarci", "Dançamos juntos a noite toda sem nunca parar.", "verbo fermarsi: smettere di muoversi"),
        ("La musica alta mi fa sentire vivo e libero.", "libero", "A música alta me faz sentir vivo e livre.", "aggettivo: senza vincoli"),
        ("Il DJ mette le canzoni più belle della serata.", "serata", "O DJ coloca as músicas mais bonitas da noite.", "sostantivo: intera durata della notte"),
        # Vol 3
        ("Muovo i piedi al ritmo della musica incalzante.", "incalzante", "Movo os pés ao ritmo da música insistente.", "aggettivo: che incalza, pressante"),
        ("Con i miei amici, la discoteca diventa magica.", "discoteca", "Com meus amigos, a discoteca se torna mágica.", "sostantivo: locale da ballo"),
        ("Il ballo è il modo migliore per esprimere la gioia.", "esprimere", "A dança é o melhor jeito de expressar a alegria.", "verbo: manifestare, comunicare"),
        ("Mi piace ballare lento con la persona che amo.", "lento", "Gosto de dançar lento com a pessoa que amo.", "aggettivo: con poco ritmo"),
        # Vol 4
        ("Il ballo mi libera da ogni tensione e stanchezza.", "tensione", "A dança me liberta de toda tensão e cansaço.", "sostantivo: stato di stress"),
        ("Imparo un nuovo passo di danza ogni settimana.", "passo", "Aprendo um novo passo de dança toda semana.", "sostantivo: movimento nel ballo"),
        ("La musica salsa mi fa venire voglia di ballare.", "salsa", "A música salsa me dá vontade de dançar.", "sostantivo: genere musicale latino"),
        ("Danzo come se nessuno mi stesse guardando.", "guardando", "Danço como se ninguém estivesse me olhando.", "verbo guardare: osservare"),
        # Vol 5
        ("Il ballo è un linguaggio universale che tutti capiscono.", "linguaggio", "A dança é uma linguagem universal que todos entendem.", "sostantivo: sistema di comunicazione"),
        ("La festa finisce ma la voglia di ballare rimane.", "voglia", "A festa termina mas a vontade de dançar permanece.", "sostantivo: desiderio, volontà"),
        ("Balliamo sotto le stelle fino all'alba.", "alba", "Dançamos sob as estrelas até o amanhecer.", "sostantivo: inizio del giorno"),
        ("Il mio partner di ballo è il più bravo della scuola.", "partner", "Meu parceiro de dança é o melhor da escola.", "sostantivo: compagno/a"),
        # Vol 6
        ("Mi sono innamorato ballando con lei tutta la sera.", "innamorato", "Me apaixonei dançando com ela a noite toda.", "participio passato di innamorarsi"),
        ("La coreografia del gruppo è stata applaudita da tutti.", "coreografia", "A coreografia do grupo foi aplaudida por todos.", "sostantivo: sequenza di movimenti"),
        ("La musica del Sud Italia ha un ritmo inconfondibile.", "inconfondibile", "A música do sul da Itália tem um ritmo inconfundível.", "aggettivo: unico, riconoscibile"),
        ("Il ballo di coppia richiede sintonia e fiducia.", "sintonia", "A dança a dois exige sintonia e confiança.", "sostantivo: accordo, armonia"),
        # Vol 7
        ("Ogni movimento del corpo racconta una storia.", "racconta", "Cada movimento do corpo conta uma história.", "verbo raccontare: narrare"),
        ("La musica popolare italiana fa venire voglia di muoversi.", "popolare", "A música popular italiana dá vontade de se mover.", "aggettivo: del popolo, famoso"),
        ("Il ritmo incalzante del tamburello mi travolge.", "tamburello", "O ritmo insistente do pandeiro me arrasta.", "sostantivo: strumento a percussione"),
        ("Dopo una notte di ballo, mi sento leggero e felice.", "leggero", "Após uma noite de dança, me sinto leve e feliz.", "aggettivo: senza peso"),
        # Vol 8
        ("La danza classica richiede anni di allenamento.", "allenamento", "A dança clássica exige anos de treino.", "sostantivo: pratica, esercizio"),
        ("Ballo da quando avevo sei anni e non smetto più.", "smetto", "Danço desde que tinha seis anos e não paro mais.", "verbo smettere: interrompere"),
        ("Il teatro dell'opera è pieno di danzatori eleganti.", "danzatori", "O teatro de ópera está cheio de dançarinos elegantes.", "sostantivo plurale: chi danza professionalmente"),
        ("Nel ballo, il corpo parla meglio delle parole.", "parla", "Na dança, o corpo fala melhor do que as palavras.", "verbo parlare: comunicare"),
        # Vol 9
        ("La voglia di ballare nasce quando sento una bella canzone.", "nasce", "A vontade de dançar nasce quando ouço uma bela música.", "verbo nascere: avere origine"),
        ("Ballo il liscio con i miei nonni la domenica.", "liscio", "Danço o liscio com meus avós no domingo.", "sostantivo: tipo di ballo italiano"),
        ("I miei piedi si muovono da soli quando sento musica.", "muovono", "Meus pés se movem sozinhos quando ouço música.", "verbo muoversi: spostarsi"),
        ("La danza mi ha insegnato la disciplina e la pazienza.", "disciplina", "A dança me ensinou a disciplina e a paciência.", "sostantivo: autocontrollo"),
        # Vol 10
        ("La musica jazz mi fa improvvisare passi nuovi.", "improvvisare", "A música jazz me faz improvisar passos novos.", "verbo: creare sul momento"),
        ("Con il ballo, il tempo sembra fermarsi per un attimo.", "attimo", "Com a dança, o tempo parece parar por um instante.", "sostantivo: momento brevissimo"),
        ("La scuola di danza è il mio posto preferito in città.", "scuola", "A escola de dança é meu lugar favorito na cidade.", "sostantivo: luogo di apprendimento"),
        ("Danzo per gioia, per amore, per la vita.", "gioia", "Danço por alegria, por amor, pela vida.", "sostantivo: felicità intensa"),
        # Extras
        ("Il ballo è meditazione in movimento per me.", "meditazione", "A dança é meditação em movimento para mim.", "sostantivo: pratica contemplativa"),
        ("La musica e il ballo sono inseparabili come l'anima.", "inseparabili", "A música e a dança são inseparáveis como a alma.", "aggettivo: che non si possono dividere"),
        ("Invito tutti gli amici a ballare con me.", "invito", "Convido todos os amigos para dançar comigo.", "verbo invitare: chiamare qualcuno"),
        ("Sudate e stanche, le ballerine continuano a danzare.", "stanche", "Suadas e cansadas, as dançarinas continuam a dançar.", "aggettivo: affaticate"),
        ("Il ballo di gruppo crea un'energia speciale.", "energia", "A dança em grupo cria uma energia especial.", "sostantivo: forza vitale"),
        ("Quando ballo, il mondo esterno scompare.", "scompare", "Quando danço, o mundo externo desaparece.", "verbo scomparire: diventare invisibile"),
        ("La musica mi muove anche quando sono stanco.", "muove", "A música me move mesmo quando estou cansado.", "verbo muovere: mettere in movimento"),
        ("Il ballo esprime emozioni che le parole non sanno dire.", "esprime", "A dança expressa emoções que as palavras não sabem dizer.", "verbo esprimere: comunicare"),
        ("Ballare sotto la pioggia è la mia cosa preferita.", "pioggia", "Dançar embaixo da chuva é minha coisa favorita.", "sostantivo: acqua che cade dal cielo"),
        ("Il palcoscenico è il luogo dove mi sento libero.", "palcoscenico", "O palco é o lugar onde me sinto livre.", "sostantivo: area di spettacolo"),
    ],
    "tristezza": [
        # Vol 1
        ("La pioggia scende e porta con sé la malinconia.", "malinconia", "A chuva desce e traz consigo a melancolia.", "sostantivo: tristezza profonda"),
        ("Il silenzio della camera vuota mi pesa sul cuore.", "pesa", "O silêncio do quarto vazio pesa em meu coração.", "verbo pesare: gravare"),
        ("Le lacrime scorrono senza che io possa fermarle.", "scorrono", "As lágrimas escorrem sem que eu possa detê-las.", "verbo scorrere: fluire"),
        ("Mi manca la persona che amavo di più al mondo.", "manca", "Sinto falta da pessoa que mais amava no mundo.", "verbo mancare: essere assente"),
        # Vol 2
        ("Il dolore del distacco non si descrive a parole.", "distacco", "A dor da separação não se descreve em palavras.", "sostantivo: separazione"),
        ("Ogni luogo mi ricorda chi non c'è più con me.", "ricorda", "Cada lugar me lembra quem não está mais comigo.", "verbo ricordare: far tornare in mente"),
        ("La tristezza mi accompagna come un'ombra silenziosa.", "ombra", "A tristeza me acompanha como uma sombra silenciosa.", "sostantivo: oscurità proiettata"),
        ("Cerco la pace interiore ma non riesco a trovarla.", "interiore", "Procuro a paz interior mas não consigo encontrá-la.", "aggettivo: dentro di sé"),
        # Vol 3
        ("Mi siedo vicino alla finestra e guardo la pioggia.", "finestra", "Sento perto da janela e olho a chuva.", "sostantivo: apertura nel muro"),
        ("La solitudine pesa come una pietra sul petto.", "solitudine", "A solidão pesa como uma pedra no peito.", "sostantivo: stato di essere solo"),
        ("Ogni notte mi sveglio pensando a quello che ho perso.", "perso", "Toda noite acordo pensando no que perdi.", "participio passato di perdere"),
        ("Il tempo passa ma il dolore rimane sempre uguale.", "uguale", "O tempo passa mas a dor permanece sempre igual.", "aggettivo: identico, lo stesso"),
        # Vol 4
        ("Le parole non bastano per descrivere questo vuoto.", "vuoto", "As palavras não bastam para descrever esse vazio.", "sostantivo: spazio privo di contenuto"),
        ("Ho cercato la felicità ma ho trovato solo dolore.", "felicità", "Procurei a felicidade mas encontrei apenas dor.", "sostantivo: stato di gioia"),
        ("Sento un peso insopportabile nel mio cuore stanco.", "insopportabile", "Sinto um peso insuportável em meu coração cansado.", "aggettivo: intollerabile"),
        ("Il cielo grigio rispecchia il mio stato d'animo.", "rispecchia", "O céu cinza reflete meu estado de espírito.", "verbo rispecchiare: riflettere"),
        # Vol 5
        ("Le fotografie ingiallite raccontano tempi migliori.", "ingiallite", "As fotografias amareladas contam tempos melhores.", "aggettivo: diventate gialle"),
        ("La musica triste mi fa compagnia nelle notti lunghe.", "compagnia", "A música triste me faz companhia nas noites longas.", "sostantivo: presenza di qualcuno"),
        ("Cerco nel silenzio una risposta che non arriva.", "risposta", "Procuro no silêncio uma resposta que não chega.", "sostantivo: ciò che risponde"),
        ("Il cuore ferito guarisce lentamente con il tempo.", "ferito", "O coração ferido cura-se lentamente com o tempo.", "aggettivo: che ha ricevuto una ferita"),
        # Vol 6
        ("Le sere solitarie sembrano non finire mai.", "solitarie", "As tardes solitárias parecem não terminar nunca.", "aggettivo: prive di compagnia"),
        ("Il passato torna sempre nei sogni più bui.", "passato", "O passado sempre volta nos sonhos mais sombrios.", "sostantivo: ciò che è già accaduto"),
        ("Sento la mancanza di qualcosa che non posso nominare.", "mancanza", "Sinto a falta de algo que não consigo nomear.", "sostantivo: assenza, privazione"),
        ("Il grigio del cielo riflette la mia tristezza profonda.", "riflette", "O cinza do céu reflete minha tristeza profunda.", "verbo riflettere: riprodurre"),
        # Vol 7
        ("Non riesco a dormire quando il cuore è pesante.", "pesante", "Não consigo dormir quando o coração está pesado.", "aggettivo: di molto peso"),
        ("Scrivo lettere che non invierò mai a nessuno.", "invierò", "Escrevo cartas que nunca enviarei a ninguém.", "verbo inviare: futuro"),
        ("La nostalgia mi opprime come un cielo senza stelle.", "nostalgia", "A nostalgia me oprime como um céu sem estrelas.", "sostantivo: dolore per il passato"),
        ("Ogni addio lascia una cicatrice nell'anima.", "cicatrice", "Cada adeus deixa uma cicatriz na alma.", "sostantivo: segno di una ferita"),
        # Vol 8
        ("La tristezza è come la marea, sale e scende.", "marea", "A tristeza é como a maré, sobe e desce.", "sostantivo: movimento del mare"),
        ("Il peso del silenzio è a volte insostenibile.", "insostenibile", "O peso do silêncio é às vezes insustentável.", "aggettivo: non sopportabile"),
        ("Alcune ferite dell'anima non guariscono mai del tutto.", "ferite", "Algumas feridas da alma nunca curam completamente.", "sostantivo plurale: lesioni"),
        ("Vivo in un presente che sa solo di passato.", "presente", "Vivo em um presente que sabe apenas de passado.", "sostantivo: momento attuale"),
        # Vol 9
        ("Anche la bellezza del mondo non riesce a consolarmi.", "consolarmi", "Até a beleza do mundo não consegue me consolar.", "verbo consolare + pronome"),
        ("Ogni tramonto mi ricorda quanto sia breve la vita.", "breve", "Cada pôr do sol me lembra o quão breve é a vida.", "aggettivo: di corta durata"),
        ("Mi perdo nei pensieri e non trovo la via d'uscita.", "uscita", "Me perco nos pensamentos e não encontro a saída.", "sostantivo: punto di uscita"),
        ("Il tempo cura le ferite ma i ricordi restano.", "cura", "O tempo cura as feridas mas as memórias ficam.", "verbo curare: guarire"),
        # Vol 10
        ("L'amore perduto è il dolore più difficile da superare.", "superare", "O amor perdido é a dor mais difícil de superar.", "verbo: andare oltre, vincere"),
        ("Ogni lacrima porta con sé un pezzo di anima.", "lacrima", "Cada lágrima traz consigo um pedaço de alma.", "sostantivo: goccia dal pianto"),
        ("La tristezza infinita non conosce né fine né misura.", "misura", "A tristeza infinita não conhece nem fim nem medida.", "sostantivo: limite, dimensione"),
        ("Le parole dette nell'ira fanno male a lungo.", "ira", "As palavras ditas na raiva doem por muito tempo.", "sostantivo: rabbia intensa"),
        # Extras
        ("Anche sorridere mi costa fatica in certi giorni.", "fatica", "Até sorrir me custa esforço em certos dias.", "sostantivo: sforzo, stanchezza"),
        ("Mi chiedo se il dolore passerà mai completamente.", "completamente", "Me pergunto se a dor vai passar completamente.", "avverbio: in modo totale"),
        ("I momenti di gioia sembrano lontani e irraggiungibili.", "irraggiungibili", "Os momentos de alegria parecem distantes e inalcançáveis.", "aggettivo: impossibili da raggiungere"),
        ("Guardo vecchie fotografie e non riconosco me stesso.", "fotografie", "Olho fotos antigas e não me reconheço.", "sostantivo plurale: immagini"),
        ("Il dolore che provo è indescrivibile con le parole.", "indescrivibile", "A dor que sinto é indescritível com palavras.", "aggettivo: che non si può descrivere"),
        ("La notte porta con sé pensieri oscuri e dolorosi.", "oscuri", "A noite traz consigo pensamentos obscuros e dolorosos.", "aggettivo: privi di luce"),
        ("I ricordi belli fanno ancora più male in certi momenti.", "ricordi", "As boas lembranças doem ainda mais em certos momentos.", "sostantivo plurale: memorie"),
        ("Piango senza motivo e non riesco a smettere.", "smettere", "Choro sem motivo e não consigo parar.", "verbo: cessare di fare qualcosa"),
        ("La solitudine è compagna di molte notti insonni.", "insonni", "A solidão é companheira de muitas noites insones.", "aggettivo: senza sonno"),
        ("Ho smesso di sperare nel momento più difficile.", "sperare", "Parei de esperar no momento mais difícil.", "verbo: avere speranza"),
    ],
    "viaggio": [
        # Vol 1
        ("Il treno parte e mi porta verso terre sconosciute.", "sconosciute", "O trem parte e me leva para terras desconhecidas.", "aggettivo: non conosciute"),
        ("Ho preparato lo zaino con tutto l'essenziale.", "zaino", "Preparei a mochila com tudo o essencial.", "sostantivo: borsa da portare in spalla"),
        ("Il viaggio inizia sempre con un primo passo.", "inizia", "A viagem sempre começa com um primeiro passo.", "verbo iniziare: cominciare"),
        ("Guardo dal finestrino e vedo paesaggi meravigliosi.", "finestrino", "Olho pela janela e vejo paisagens maravilhosas.", "sostantivo: piccola finestra del treno"),
        # Vol 2
        ("Ogni città che visito mi insegna qualcosa di nuovo.", "insegna", "Cada cidade que visito me ensina algo novo.", "verbo insegnare: dare conoscenza"),
        ("Il passaporto è il mio biglietto per il mondo.", "passaporto", "O passaporte é meu bilhete para o mundo.", "sostantivo: documento di viaggio"),
        ("L'aeroporto è il luogo dove inizia ogni avventura.", "avventura", "O aeroporto é o lugar onde começa cada aventura.", "sostantivo: esperienza emozionante"),
        ("Il mare in lontananza mi chiama verso nuovi orizzonti.", "orizzonti", "O mar ao longe me chama para novos horizontes.", "sostantivo plurale: limite visivo"),
        # Vol 3
        ("Mi perdo nelle strade di città che non conosco.", "strade", "Me perco nas ruas de cidades que não conheço.", "sostantivo plurale: vie"),
        ("Ogni viaggio lascia un segno profondo nell'anima.", "segno", "Cada viagem deixa uma marca profunda na alma.", "sostantivo: traccia, impressione"),
        ("Ho incontrato persone straordinarie durante il cammino.", "straordinarie", "Encontrei pessoas extraordinárias durante o caminho.", "aggettivo: fuori dal comune"),
        ("Il cibo locale racconta la storia di ogni luogo.", "racconta", "A comida local conta a história de cada lugar.", "verbo raccontare: narrare"),
        # Vol 4
        ("La fotografia cattura i momenti del viaggio per sempre.", "cattura", "A fotografia captura os momentos da viagem para sempre.", "verbo catturare: prendere, fermare"),
        ("Il treno percorre chilometri di pianura silenziosa.", "pianura", "O trem percorre quilômetros de planície silenciosa.", "sostantivo: territorio piatto"),
        ("Dormo in ostelli e conosco viaggiatori da tutto il mondo.", "ostelli", "Durmo em albergues e conheço viajantes do mundo todo.", "sostantivo plurale: luoghi economici"),
        ("Ogni tramonto in viaggio è diverso dall'altro.", "tramonto", "Cada pôr do sol em viagem é diferente do outro.", "sostantivo: fine del giorno"),
        # Vol 5
        ("Tornare a casa dopo un lungo viaggio è sempre dolce.", "dolce", "Voltar para casa após uma longa viagem é sempre doce.", "aggettivo: piacevole, gradito"),
        ("Le montagne lontane mi attraggono come un magnete.", "attraggono", "As montanhas distantes me atraem como um ímã.", "verbo attrarre: esercitare attrazione"),
        ("Ogni idioma che imparo apre una nuova porta.", "idioma", "Cada idioma que aprendo abre uma nova porta.", "sostantivo: lingua"),
        ("Il silenzio della natura mi ricarica le energie.", "ricarica", "O silêncio da natureza recarrega minhas energias.", "verbo ricaricare: dare nuova energia"),
        # Vol 6
        ("Il profumo dei mercati locali mi conquista sempre.", "conquista", "O cheiro dos mercados locais sempre me conquista.", "verbo conquistare: vincere"),
        ("Ho camminato per ore sulle rive di un fiume antico.", "rive", "Caminhei por horas às margens de um rio antigo.", "sostantivo plurale: bordi del fiume"),
        ("Ogni viaggio è un capitolo nuovo della mia storia.", "capitolo", "Cada viagem é um capítulo novo da minha história.", "sostantivo: parte di un libro"),
        ("Visitare le rovine antiche è come viaggiare nel tempo.", "rovine", "Visitar as ruínas antigas é como viajar no tempo.", "sostantivo plurale: resti di edifici"),
        # Vol 7
        ("Ogni incontro con uno straniero arricchisce la mente.", "straniero", "Cada encontro com um estrangeiro enriquece a mente.", "sostantivo: persona di altro paese"),
        ("La bicicletta è il modo migliore per visitare le città.", "bicicletta", "A bicicleta é o melhor jeito de visitar as cidades.", "sostantivo: veicolo a due ruote"),
        ("Il treno notturno attraversa la penisola in silenzio.", "penisola", "O trem noturno atravessa a península em silêncio.", "sostantivo: terra circondata dal mare"),
        ("La lingua locale cambia, ma il sorriso è universale.", "universale", "A língua local muda, mas o sorriso é universal.", "aggettivo: di tutti, ovunque"),
        # Vol 8
        ("Ogni partenza è difficile, ma ne vale sempre la pena.", "partenza", "Cada partida é difícil, mas sempre vale a pena.", "sostantivo: azione del partire"),
        ("La cucina locale racconta la cultura del luogo.", "cucina", "A cozinha local conta a cultura do lugar.", "sostantivo: arte culinaria"),
        ("Viaggiare da soli insegna l'indipendenza e il coraggio.", "coraggio", "Viajar sozinho ensina a independência e a coragem.", "sostantivo: audacia, bravura"),
        ("Ogni villaggio nasconde tesori che non trovi nelle guide.", "tesori", "Cada vilarejo esconde tesouros que não se encontra nos guias.", "sostantivo plurale: cose preziose"),
        # Vol 9
        ("Il sole di mezzogiorno brucia ma non ci ferma.", "brucia", "O sol do meio-dia queima mas não nos para.", "verbo bruciare: essere molto caldo"),
        ("Le strade di Roma parlano di secoli di storia.", "secoli", "As ruas de Roma falam de séculos de história.", "sostantivo plurale: cento anni"),
        ("Il tramonto sul mare mi ricorda perché viaggio.", "ricorda", "O pôr do sol no mar me lembra por que viajo.", "verbo ricordare: far pensare"),
        ("La pioggia nel viaggio non è un ostacolo, è un'esperienza.", "ostacolo", "A chuva na viagem não é um obstáculo, é uma experiência.", "sostantivo: impedimento"),
        # Vol 10
        ("La nostalgia di casa cresce con la distanza.", "nostalgia", "A saudade de casa cresce com a distância.", "sostantivo: desiderio del passato"),
        ("Le stelle mi guidano quando mi perdo nella foresta.", "guidano", "As estrelas me guiam quando me perco na floresta.", "verbo guidare: indicare la via"),
        ("Il vento del nord porta odori di terre sconosciute.", "odori", "O vento do norte traz cheiros de terras desconhecidas.", "sostantivo plurale: fragranze"),
        ("Ho trovato un paese piccolo e meraviglioso fuori dalle mappe.", "mappe", "Encontrei uma cidadezinha maravilhosa fora dos mapas.", "sostantivo plurale: cartine geografiche"),
        # Extras
        ("Viaggio per scoprire me stesso e il mondo intorno.", "scoprire", "Viajo para descobrir a mim mesmo e o mundo ao redor.", "verbo: trovare, conoscere"),
        ("Viaggio leggero, con pochi oggetti ma tante esperienze.", "esperienze", "Viajo leve, com poucos objetos mas muitas experiências.", "sostantivo plurale: vissuti, conoscenze"),
        ("La mappa non basta per conoscere un paese davvero.", "mappa", "O mapa não basta para conhecer um país de verdade.", "sostantivo: rappresentazione geografica"),
        ("Il confine tra un paese e l'altro si passa in un attimo.", "confine", "A fronteira entre um país e outro se passa em um instante.", "sostantivo: limite territoriale"),
        ("Il vento marino mi sveglia all'alba con il suo odore.", "odore", "O vento marítimo me acorda ao amanhecer com seu cheiro.", "sostantivo: fragranza"),
        ("Ogni viaggio insegna qualcosa di nuovo sulla vita.", "insegna", "Cada viagem ensina algo novo sobre a vida.", "verbo insegnare: far imparare"),
        ("La libertà del viaggio è incomparabile con qualsiasi altra.", "libertà", "A liberdade da viagem é incomparável com qualquer outra.", "sostantivo: stato di essere liberi"),
        ("Cammino per le vie di Firenze e mi sento felice.", "Firenze", "Caminho pelas ruas de Florença e me sinto feliz.", "città italiana famosa per l'arte"),
        ("Il paesaggio montano mi toglie il fiato.", "paesaggio", "A paisagem montanhosa me tira o fôlego.", "sostantivo: vista panoramica"),
        ("Tornare a casa è bello, ma partire è ancora meglio.", "partire", "Voltar para casa é bom, mas partir é ainda melhor.", "verbo: lasciare un luogo"),
    ],
}

# Mappa temi italiani -> chiave interna
TEMA_MAP = {
    "amore": "amore",
    "estate": "estate",
    "notte": "notte",
    "ballo": "ballo",
    "tristezza": "tristezza",
    "viaggio": "viaggio",
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
        if "Questo è un verso" in e.get("texto_completo", ""):
            return True
    return False

# Load
with open("data/canzoni.json", "r", encoding="utf-8") as f:
    data = json.load(f)

songs = data["canzoni"]
fixed = 0
skipped = 0
unknown_tema = []

# Track usage per tema (to cycle through 50 frases across 10 vols)
tema_usage = {t: 0 for t in TEMAS}

for song in songs:
    sid = song["id"]
    num_match = re.match(r"can_(\d+)", sid)
    if not num_match:
        continue
    num = int(num_match.group(1))
    if not (51 <= num <= 150):
        continue

    tema = song.get("tema", "")
    tema_key = TEMA_MAP.get(tema)
    
    if not tema_key:
        unknown_tema.append((sid, tema))
        continue

    if not is_generic(song.get("estrofes", [])):
        skipped += 1
        continue

    pool = TEMAS[tema_key]
    start = tema_usage[tema_key]
    
    # Take 4 frases from pool (cycling if needed)
    frases = []
    for i in range(4):
        frases.append(pool[(start + i) % len(pool)])
    tema_usage[tema_key] += 4

    # Build new estrofes
    new_estrofes = [make_estrofa(i+1, frases[i]) for i in range(4)]
    new_vocab = [f[1] for f in frases]  # palavras ocultas

    song["estrofes"] = new_estrofes
    song["vocabulario_chave"] = new_vocab
    fixed += 1

print(f"Fixed: {fixed}")
print(f"Skipped (already real): {skipped}")
if unknown_tema:
    print(f"Unknown tema: {unknown_tema}")

# Save
with open("data/canzoni.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved data/canzoni.json")

# Verify
print("\nVerification of first 3 fixed songs:")
songs2 = data["canzoni"]
count = 0
for s in songs2:
    sid = s["id"]
    nm = re.match(r"can_(\d+)", sid)
    if not nm:
        continue
    num = int(nm.group(1))
    if 51 <= num <= 53:
        print(f"\n{sid} ({s['titulo']}):")
        for e in s["estrofes"][:2]:
            print(f"  [{e['id']}] {e['texto_completo']}")
            print(f"       -> oculta: {e['palavra_oculta']}")
        count += 1
