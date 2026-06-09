#!/usr/bin/env python3
"""Expand songs can_151 through can_200 from 2 to 5-6 estrofes each."""

import json

EXPANSIONS = {
    "can_151": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Il mondo è grigio, il mondo è azzurro, il mondo è tristezza e bugie.",
                "texto_lacuna": "Il mondo è grigio, il mondo è ___, il mondo è tristezza e bugie.",
                "palavra_oculta": "azzurro",
                "traducao": "O mundo é cinza, o mundo é azul, o mundo é tristeza e mentiras.",
                "dica": "colore del cielo"
            },
            {
                "id": 2,
                "texto_completo": "E il cuore ha paura di amare ma poi si innamora.",
                "texto_lacuna": "E il cuore ha paura di ___ ma poi si innamora.",
                "palavra_oculta": "amare",
                "traducao": "E o coração tem medo de amar mas depois se apaixona.",
                "dica": "infinito di 'amore'"
            },
            {
                "id": 3,
                "texto_completo": "Gira il mondo, gira, e la vita non si ferma mai.",
                "texto_lacuna": "Gira il mondo, gira, e la vita non si ___ mai.",
                "palavra_oculta": "ferma",
                "traducao": "O mundo gira, gira, e a vida nunca para.",
                "dica": "si ferma = para (riflessivo di 'fermare')"
            },
            {
                "id": 4,
                "texto_completo": "Il sole sorge e tramonta ogni giorno senza sosta.",
                "texto_lacuna": "Il sole sorge e ___ ogni giorno senza sosta.",
                "palavra_oculta": "tramonta",
                "traducao": "O sol nasce e se põe todo dia sem parar.",
                "dica": "opposto di 'sorge'"
            },
            {
                "id": 5,
                "texto_completo": "E intanto il tempo passa e porta via i sogni.",
                "texto_lacuna": "E intanto il ___ passa e porta via i sogni.",
                "palavra_oculta": "tempo",
                "traducao": "E enquanto isso o tempo passa e leva os sonhos.",
                "dica": "sinonimo: 'ora', 'momento'"
            },
            {
                "id": 6,
                "texto_completo": "Ma il cuore resta e continua ad amare.",
                "texto_lacuna": "Ma il cuore ___ e continua ad amare.",
                "palavra_oculta": "resta",
                "traducao": "Mas o coração fica e continua a amar.",
                "dica": "sinonimo: 'rimane'"
            }
        ]
    },
    "can_152": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Non ho l'età, per amarti, non ho l'età per vivere.",
                "texto_lacuna": "Non ho l'età, per ___, non ho l'età per vivere.",
                "palavra_oculta": "amarti",
                "traducao": "Não tenho a idade para te amar, não tenho a idade para viver.",
                "dica": "infinito 'amare' + ti"
            },
            {
                "id": 2,
                "texto_completo": "Sarai il mio primo amore, il primo pensiero al mattino.",
                "texto_lacuna": "Sarai il mio ___ amore, il primo pensiero al mattino.",
                "palavra_oculta": "primo",
                "traducao": "Você será meu primeiro amor, o primeiro pensamento de manhã.",
                "dica": "numero ordinale: 1°"
            },
            {
                "id": 3,
                "texto_completo": "Non ho l'età ma ti amo con tutto il mio cuore.",
                "texto_lacuna": "Non ho l'età ma ti ___ con tutto il mio cuore.",
                "palavra_oculta": "amo",
                "traducao": "Não tenho a idade mas te amo com todo o meu coração.",
                "dica": "prima persona di 'amare'"
            },
            {
                "id": 4,
                "texto_completo": "Sei troppo grande per me, eppure ti seguo ovunque.",
                "texto_lacuna": "Sei troppo ___ per me, eppure ti seguo ovunque.",
                "palavra_oculta": "grande",
                "traducao": "Você é muito grande para mim, mesmo assim te sigo por toda parte.",
                "dica": "opposto di 'piccolo'"
            },
            {
                "id": 5,
                "texto_completo": "Aspetterò il giorno in cui potrò dirti sì.",
                "texto_lacuna": "___ il giorno in cui potrò dirti sì.",
                "palavra_oculta": "Aspetterò",
                "traducao": "Esperarei o dia em que poderei te dizer sim.",
                "dica": "futuro di 'aspettare'"
            }
        ]
    },
    "can_153": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Dimmi quando tu verrai, dimmi quando quando quando.",
                "texto_lacuna": "Dimmi quando tu ___, dimmi quando quando quando.",
                "palavra_oculta": "verrai",
                "traducao": "Me diga quando você virá, me diga quando quando quando.",
                "dica": "futuro di 'venire'"
            },
            {
                "id": 2,
                "texto_completo": "L'anno, il giorno, l'ora in cui forse tu mi bacerai.",
                "texto_lacuna": "L'anno, il giorno, l'ora in cui forse tu mi ___.",
                "palavra_oculta": "bacerai",
                "traducao": "O ano, o dia, a hora em que talvez você me beijará.",
                "dica": "futuro di 'baciare'"
            },
            {
                "id": 3,
                "texto_completo": "Ogni ora che passa senza di te sembra un'eternità.",
                "texto_lacuna": "Ogni ora che passa senza di te sembra un'___.",
                "palavra_oculta": "eternità",
                "traducao": "Cada hora que passa sem você parece uma eternidade.",
                "dica": "tempo infinito"
            },
            {
                "id": 4,
                "texto_completo": "Ti aspetto con il cuore che batte forte.",
                "texto_lacuna": "Ti ___ con il cuore che batte forte.",
                "palavra_oculta": "aspetto",
                "traducao": "Espero por você com o coração batendo forte.",
                "dica": "prima persona di 'aspettare'"
            },
            {
                "id": 5,
                "texto_completo": "Il tuo sorriso è la cosa più bella che conosca.",
                "texto_lacuna": "Il tuo ___ è la cosa più bella che conosca.",
                "palavra_oculta": "sorriso",
                "traducao": "Seu sorriso é a coisa mais bonita que eu conheça.",
                "dica": "da 'sorridere'"
            },
            {
                "id": 6,
                "texto_completo": "Dimmi soltanto che tornerai presto da me.",
                "texto_lacuna": "Dimmi soltanto che ___ presto da me.",
                "palavra_oculta": "tornerai",
                "traducao": "Me diga apenas que voltará logo para mim.",
                "dica": "futuro di 'tornare'"
            }
        ]
    },
    "can_154": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Io vagabondo non ho paura, cammino libero per il mondo.",
                "texto_lacuna": "Io ___ non ho paura, cammino libero per il mondo.",
                "palavra_oculta": "vagabondo",
                "traducao": "Eu vagabundo não tenho medo, caminho livre pelo mundo.",
                "dica": "chi vaga senza meta"
            },
            {
                "id": 2,
                "texto_completo": "La strada è la mia casa, il vento il mio compagno.",
                "texto_lacuna": "La strada è la mia casa, il ___ il mio compagno.",
                "palavra_oculta": "vento",
                "traducao": "A estrada é minha casa, o vento meu companheiro.",
                "dica": "aria in movimento"
            },
            {
                "id": 3,
                "texto_completo": "Non cerco ricchezze, cerco la libertà.",
                "texto_lacuna": "Non cerco ricchezze, cerco la ___.",
                "palavra_oculta": "libertà",
                "traducao": "Não busco riquezas, busco a liberdade.",
                "dica": "sinonimo: 'indipendenza'"
            },
            {
                "id": 4,
                "texto_completo": "Ogni città è mia, ogni paese è mio.",
                "texto_lacuna": "Ogni città è mia, ogni ___ è mio.",
                "palavra_oculta": "paese",
                "traducao": "Cada cidade é minha, cada aldeia é minha.",
                "dica": "piccola città"
            },
            {
                "id": 5,
                "texto_completo": "Sotto le stelle dormo e sogno nuovi orizzonti.",
                "texto_lacuna": "Sotto le stelle ___ e sogno nuovi orizzonti.",
                "palavra_oculta": "dormo",
                "traducao": "Sob as estrelas durmo e sonho novos horizontes.",
                "dica": "prima persona di 'dormire'"
            }
        ]
    },
    "can_155": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Tanti auguri a te, tanti auguri a te!",
                "texto_lacuna": "___ auguri a te, tanti auguri a te!",
                "palavra_oculta": "Tanti",
                "traducao": "Muitos parabéns a você, muitos parabéns a você!",
                "dica": "molti, numerosi"
            },
            {
                "id": 2,
                "texto_completo": "Tanti auguri, cara amica, tanti auguri a te!",
                "texto_lacuna": "Tanti auguri, cara ___, tanti auguri a te!",
                "palavra_oculta": "amica",
                "traducao": "Muitos parabéns, querida amiga, muitos parabéns a você!",
                "dica": "femminile di 'amico'"
            },
            {
                "id": 3,
                "texto_completo": "Che la vita ti sorrida sempre con gioia.",
                "texto_lacuna": "Che la vita ti ___ sempre con gioia.",
                "palavra_oculta": "sorrida",
                "traducao": "Que a vida sempre te sorria com alegria.",
                "dica": "congiuntivo di 'sorridere'"
            },
            {
                "id": 4,
                "texto_completo": "Festeggiamo insieme questo giorno speciale.",
                "texto_lacuna": "___ insieme questo giorno speciale.",
                "palavra_oculta": "Festeggiamo",
                "traducao": "Comemoramos juntos este dia especial.",
                "dica": "da 'festeggiare', prima persona plurale"
            },
            {
                "id": 5,
                "texto_completo": "Un grande abbraccio e mille baci per te.",
                "texto_lacuna": "Un grande ___ e mille baci per te.",
                "palavra_oculta": "abbraccio",
                "traducao": "Um grande abraço e mil beijos para você.",
                "dica": "da 'abbracciare'"
            },
            {
                "id": 6,
                "texto_completo": "Che i tuoi sogni si realizzino oggi e sempre.",
                "texto_lacuna": "Che i tuoi sogni si ___ oggi e sempre.",
                "palavra_oculta": "realizzino",
                "traducao": "Que seus sonhos se realizem hoje e sempre.",
                "dica": "congiuntivo di 'realizzarsi'"
            }
        ]
    },
    "can_156": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Luce dei miei occhi, tu sei la mia luce.",
                "texto_lacuna": "___ dei miei occhi, tu sei la mia luce.",
                "palavra_oculta": "Luce",
                "traducao": "Luz dos meus olhos, você é a minha luz.",
                "dica": "contrario di 'buio'"
            },
            {
                "id": 2,
                "texto_completo": "Tramonti a nord est, colori nell'aria.",
                "texto_lacuna": "___ a nord est, colori nell'aria.",
                "palavra_oculta": "Tramonti",
                "traducao": "Pôr do sol a nordeste, cores no ar.",
                "dica": "plurale di 'tramonto'"
            },
            {
                "id": 3,
                "texto_completo": "Il cielo si tinge di rosso e arancione.",
                "texto_lacuna": "Il cielo si ___ di rosso e arancione.",
                "palavra_oculta": "tinge",
                "traducao": "O céu se pinta de vermelho e laranja.",
                "dica": "si colora"
            },
            {
                "id": 4,
                "texto_completo": "Tu illumini la mia vita come il sole illumina il giorno.",
                "texto_lacuna": "Tu ___ la mia vita come il sole illumina il giorno.",
                "palavra_oculta": "illumini",
                "traducao": "Você ilumina minha vida como o sol ilumina o dia.",
                "dica": "da 'illuminare', seconda persona"
            },
            {
                "id": 5,
                "texto_completo": "Senza di te sarei persa nel buio.",
                "texto_lacuna": "Senza di te sarei ___ nel buio.",
                "palavra_oculta": "persa",
                "traducao": "Sem você eu estaria perdida na escuridão.",
                "dica": "participio di 'perdere', femminile"
            }
        ]
    },
    "can_157": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Come saprei amarti, come vorrei tenerti.",
                "texto_lacuna": "Come ___ amarti, come vorrei tenerti.",
                "palavra_oculta": "saprei",
                "traducao": "Como eu saberia te amar, como gostaria de te ter.",
                "dica": "condizionale di 'sapere'"
            },
            {
                "id": 2,
                "texto_completo": "Se tu fossi ancora qui, non ti lascerei mai andare.",
                "texto_lacuna": "Se tu fossi ancora qui, non ti ___ mai andare.",
                "palavra_oculta": "lascerei",
                "traducao": "Se você ainda estivesse aqui, nunca te deixaria ir.",
                "dica": "condizionale di 'lasciare'"
            },
            {
                "id": 3,
                "texto_completo": "Il tuo profumo è ancora nell'aria e nel mio cuore.",
                "texto_lacuna": "Il tuo ___ è ancora nell'aria e nel mio cuore.",
                "palavra_oculta": "profumo",
                "traducao": "Seu perfume ainda está no ar e no meu coração.",
                "dica": "aroma, fragranza"
            },
            {
                "id": 4,
                "texto_completo": "Cerco il tuo viso in ogni volto che incontro.",
                "texto_lacuna": "Cerco il tuo ___ in ogni volto che incontro.",
                "palavra_oculta": "viso",
                "traducao": "Procuro seu rosto em cada rosto que encontro.",
                "dica": "sinonimo: 'faccia', 'volto'"
            },
            {
                "id": 5,
                "texto_completo": "Ogni notte sogno di riabbracciarti ancora.",
                "texto_lacuna": "Ogni notte ___ di riabbracciarti ancora.",
                "palavra_oculta": "sogno",
                "traducao": "Toda noite sonho em te abraçar de novo.",
                "dica": "prima persona di 'sognare'"
            },
            {
                "id": 6,
                "texto_completo": "Come saprei dirti quanto mi manchi.",
                "texto_lacuna": "Come saprei dirti quanto mi ___.",
                "palavra_oculta": "manchi",
                "traducao": "Como eu saberia te dizer o quanto sinto sua falta.",
                "dica": "da 'mancare', seconda persona"
            }
        ]
    },
    "can_158": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Nessuno mi può giudicare, neanche tu.",
                "texto_lacuna": "Nessuno mi può ___, neanche tu.",
                "palavra_oculta": "giudicare",
                "traducao": "Ninguém pode me julgar, nem você.",
                "dica": "dare un giudizio"
            },
            {
                "id": 2,
                "texto_completo": "Sono libera di fare quello che voglio.",
                "texto_lacuna": "Sono ___ di fare quello che voglio.",
                "palavra_oculta": "libera",
                "traducao": "Sou livre para fazer o que quero.",
                "dica": "femminile di 'libero'"
            },
            {
                "id": 3,
                "texto_completo": "La mia vita è mia e la vivo a modo mio.",
                "texto_lacuna": "La mia vita è mia e la ___ a modo mio.",
                "palavra_oculta": "vivo",
                "traducao": "Minha vida é minha e a vivo do meu jeito.",
                "dica": "prima persona di 'vivere'"
            },
            {
                "id": 4,
                "texto_completo": "Non mi importa di cosa pensano gli altri.",
                "texto_lacuna": "Non mi importa di cosa ___ gli altri.",
                "palavra_oculta": "pensano",
                "traducao": "Não me importa o que os outros pensam.",
                "dica": "terza persona plurale di 'pensare'"
            },
            {
                "id": 5,
                "texto_completo": "Cammino per la mia strada con la testa alta.",
                "texto_lacuna": "Cammino per la mia strada con la testa ___.",
                "palavra_oculta": "alta",
                "traducao": "Caminho pelo meu caminho com a cabeça erguida.",
                "dica": "opposto di 'bassa'"
            }
        ]
    },
    "can_159": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "La bambola non vuole più giocare.",
                "texto_lacuna": "La ___ non vuole più giocare.",
                "palavra_oculta": "bambola",
                "traducao": "A boneca não quer mais brincar.",
                "dica": "giocattolo femminile"
            },
            {
                "id": 2,
                "texto_completo": "Ha gli occhi di vetro e un sorriso dipinto.",
                "texto_lacuna": "Ha gli occhi di ___ e un sorriso dipinto.",
                "palavra_oculta": "vetro",
                "traducao": "Tem olhos de vidro e um sorriso pintado.",
                "dica": "materiale trasparente"
            },
            {
                "id": 3,
                "texto_completo": "Ma dentro si nasconde un'anima vera.",
                "texto_lacuna": "Ma dentro si ___ un'anima vera.",
                "palavra_oculta": "nasconde",
                "traducao": "Mas dentro se esconde uma alma verdadeira.",
                "dica": "si cela, non si mostra"
            },
            {
                "id": 4,
                "texto_completo": "Nessuno capisce il suo dolore silenzioso.",
                "texto_lacuna": "Nessuno capisce il suo ___ silenzioso.",
                "palavra_oculta": "dolore",
                "traducao": "Ninguém entende sua dor silenciosa.",
                "dica": "sofferenza, pena"
            },
            {
                "id": 5,
                "texto_completo": "Lei aspetta qualcuno che la sappia amare davvero.",
                "texto_lacuna": "Lei ___ qualcuno che la sappia amare davvero.",
                "palavra_oculta": "aspetta",
                "traducao": "Ela espera alguém que saiba amá-la de verdade.",
                "dica": "terza persona di 'aspettare'"
            }
        ]
    },
    "can_160": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Sei nell'anima mia, ci sei nell'anima.",
                "texto_lacuna": "___ nell'anima mia, ci sei nell'anima.",
                "palavra_oculta": "Sei",
                "traducao": "Você está na minha alma, está na alma.",
                "dica": "seconda persona di 'essere'"
            },
            {
                "id": 2,
                "texto_completo": "Ogni respiro che faccio è pieno di te.",
                "texto_lacuna": "Ogni ___ che faccio è pieno di te.",
                "palavra_oculta": "respiro",
                "traducao": "Cada respiração que faço está cheia de você.",
                "dica": "da 'respirare'"
            },
            {
                "id": 3,
                "texto_completo": "Non riesco a dimenticarti, sei troppo dentro di me.",
                "texto_lacuna": "Non riesco a ___, sei troppo dentro di me.",
                "palavra_oculta": "dimenticarti",
                "traducao": "Não consigo te esquecer, você está muito dentro de mim.",
                "dica": "infinito di 'dimenticare' + ti"
            },
            {
                "id": 4,
                "texto_completo": "Mi hai lasciato un segno indelebile nell'anima.",
                "texto_lacuna": "Mi hai lasciato un segno ___ nell'anima.",
                "palavra_oculta": "indelebile",
                "traducao": "Você deixou uma marca indelével na minha alma.",
                "dica": "che non si cancella"
            },
            {
                "id": 5,
                "texto_completo": "La tua voce risuona ancora nei miei pensieri.",
                "texto_lacuna": "La tua voce ___ ancora nei miei pensieri.",
                "palavra_oculta": "risuona",
                "traducao": "Sua voz ainda ressoa nos meus pensamentos.",
                "dica": "echeggia, si sente ancora"
            }
        ]
    },
    "can_161": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "America, America, terra di sogni e di speranza.",
                "texto_lacuna": "___, America, terra di sogni e di speranza.",
                "palavra_oculta": "America",
                "traducao": "América, América, terra de sonhos e esperança.",
                "dica": "continente o nazione"
            },
            {
                "id": 2,
                "texto_completo": "Partii con una valigia piena di illusioni.",
                "texto_lacuna": "Partii con una ___ piena di illusioni.",
                "palavra_oculta": "valigia",
                "traducao": "Parti com uma mala cheia de ilusões.",
                "dica": "borsa da viaggio"
            },
            {
                "id": 3,
                "texto_completo": "Cercavo fortuna in una terra straniera.",
                "texto_lacuna": "Cercavo ___ in una terra straniera.",
                "palavra_oculta": "fortuna",
                "traducao": "Buscava sorte numa terra estrangeira.",
                "dica": "buona sorte, successo"
            },
            {
                "id": 4,
                "texto_completo": "Ma il cuore è rimasto nella mia terra natia.",
                "texto_lacuna": "Ma il cuore è rimasto nella mia terra ___.",
                "palavra_oculta": "natia",
                "traducao": "Mas o coração ficou na minha terra natal.",
                "dica": "dove si è nati"
            },
            {
                "id": 5,
                "texto_completo": "L'emigrante porta con sé i ricordi di casa.",
                "texto_lacuna": "L'___ porta con sé i ricordi di casa.",
                "palavra_oculta": "emigrante",
                "traducao": "O emigrante carrega consigo as memórias de casa.",
                "dica": "chi lascia il proprio paese"
            }
        ]
    },
    "can_162": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Via del Campo c'è una graziosa, gli occhi grandi color di foglia.",
                "texto_lacuna": "Via del Campo c'è una ___, gli occhi grandi color di foglia.",
                "palavra_oculta": "graziosa",
                "traducao": "Via del Campo tem uma graciosa, olhos grandes cor de folha.",
                "dica": "bella, piacevole"
            },
            {
                "id": 2,
                "texto_completo": "Che traffica senza speranza nel mondo dei sogni infranti.",
                "texto_lacuna": "Che traffica senza ___ nel mondo dei sogni infranti.",
                "palavra_oculta": "speranza",
                "traducao": "Que trafega sem esperança no mundo dos sonhos destruídos.",
                "dica": "ottimismo, fiducia nel futuro"
            },
            {
                "id": 3,
                "texto_completo": "Se sei gentile le puoi chiedere il cielo.",
                "texto_lacuna": "Se sei ___ le puoi chiedere il cielo.",
                "palavra_oculta": "gentile",
                "traducao": "Se você for gentil pode pedir a ela o céu.",
                "dica": "cortese, educato"
            },
            {
                "id": 4,
                "texto_completo": "Via del Campo ci vuole andare la sera.",
                "texto_lacuna": "Via del Campo ci vuole ___ la sera.",
                "palavra_oculta": "andare",
                "traducao": "Via del Campo é preciso ir à noite.",
                "dica": "infinito di movimento"
            },
            {
                "id": 5,
                "texto_completo": "Dai diamanti non nasce niente, dal letame nascono i fior.",
                "texto_lacuna": "Dai ___ non nasce niente, dal letame nascono i fior.",
                "palavra_oculta": "diamanti",
                "traducao": "Dos diamantes não nasce nada, do esterco nascem as flores.",
                "dica": "pietre preziose"
            }
        ]
    },
    "can_163": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Era bella come una rosa, Marinella sul fiume.",
                "texto_lacuna": "Era bella come una ___, Marinella sul fiume.",
                "palavra_oculta": "rosa",
                "traducao": "Era bonita como uma rosa, Marinella no rio.",
                "dica": "fiore profumato"
            },
            {
                "id": 2,
                "texto_completo": "Il vento cantava nel bosco la sua canzone.",
                "texto_lacuna": "Il vento ___ nel bosco la sua canzone.",
                "palavra_oculta": "cantava",
                "traducao": "O vento cantava no bosque sua canção.",
                "dica": "imperfetto di 'cantare'"
            },
            {
                "id": 3,
                "texto_completo": "Marinella, il mare ti ha portata via per sempre.",
                "texto_lacuna": "Marinella, il mare ti ha ___ via per sempre.",
                "palavra_oculta": "portata",
                "traducao": "Marinella, o mar te levou para sempre.",
                "dica": "participio di 'portare', femminile"
            },
            {
                "id": 4,
                "texto_completo": "Le stelle del cielo sono le lacrime degli angeli.",
                "texto_lacuna": "Le stelle del cielo sono le ___ degli angeli.",
                "palavra_oculta": "lacrime",
                "traducao": "As estrelas do céu são as lágrimas dos anjos.",
                "dica": "pianto, gocce dagli occhi"
            },
            {
                "id": 5,
                "texto_completo": "La storia di Marinella è una storia d'amore e dolore.",
                "texto_lacuna": "La storia di Marinella è una storia d'amore e ___.",
                "palavra_oculta": "dolore",
                "traducao": "A história de Marinella é uma história de amor e dor.",
                "dica": "sofferenza, pena"
            }
        ]
    },
    "can_164": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Bocca di Rosa mise l'amore sopra ogni cosa.",
                "texto_lacuna": "Bocca di Rosa mise l'___ sopra ogni cosa.",
                "palavra_oculta": "amore",
                "traducao": "Bocca di Rosa colocou o amor acima de tudo.",
                "dica": "sentimento profondo"
            },
            {
                "id": 2,
                "texto_completo": "Arrivò a Sant'Ilario con il cuore libero.",
                "texto_lacuna": "Arrivò a Sant'Ilario con il cuore ___.",
                "palavra_oculta": "libero",
                "traducao": "Chegou a Sant'Ilario com o coração livre.",
                "dica": "opposto di 'prigioniero'"
            },
            {
                "id": 3,
                "texto_completo": "Le donne del paese la guardavano con invidia.",
                "texto_lacuna": "Le donne del paese la guardavano con ___.",
                "palavra_oculta": "invidia",
                "traducao": "As mulheres do vilarejo a olhavam com inveja.",
                "dica": "gelosia per i successi altrui"
            },
            {
                "id": 4,
                "texto_completo": "Ma Bocca di Rosa amava senza chiedere niente in cambio.",
                "texto_lacuna": "Ma Bocca di Rosa amava senza chiedere niente in ___.",
                "palavra_oculta": "cambio",
                "traducao": "Mas Bocca di Rosa amava sem pedir nada em troca.",
                "dica": "in cambio = em troca"
            },
            {
                "id": 5,
                "texto_completo": "La misero sul treno mentre il paese la fischiava.",
                "texto_lacuna": "La misero sul ___ mentre il paese la fischiava.",
                "palavra_oculta": "treno",
                "traducao": "Colocaram-na no trem enquanto o vilarejo a vaiava.",
                "dica": "mezzo di trasporto su rotaie"
            },
            {
                "id": 6,
                "texto_completo": "Una rosa che nasce in mezzo alla spazzatura.",
                "texto_lacuna": "Una rosa che nasce in mezzo alla ___.",
                "palavra_oculta": "spazzatura",
                "traducao": "Uma rosa que nasce no meio do lixo.",
                "dica": "rifiuti, immondizia"
            }
        ]
    },
    "can_165": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "All'ombra dell'ultimo sole un pescatore tornava.",
                "texto_lacuna": "All'ombra dell'ultimo sole un ___ tornava.",
                "palavra_oculta": "pescatore",
                "traducao": "À sombra do último sol um pescador voltava.",
                "dica": "chi pesca il pesce"
            },
            {
                "id": 2,
                "texto_completo": "Con le reti vuote e il cuore stanco.",
                "texto_lacuna": "Con le reti ___ e il cuore stanco.",
                "palavra_oculta": "vuote",
                "traducao": "Com as redes vazias e o coração cansado.",
                "dica": "senza contenuto, contrario di 'piene'"
            },
            {
                "id": 3,
                "texto_completo": "Incontrò un assassino in fuga dalla legge.",
                "texto_lacuna": "Incontrò un ___ in fuga dalla legge.",
                "palavra_oculta": "assassino",
                "traducao": "Encontrou um assassino em fuga da lei.",
                "dica": "chi ha ucciso qualcuno"
            },
            {
                "id": 4,
                "texto_completo": "Lo portò a casa e lo sfamò con pane e vino.",
                "texto_lacuna": "Lo portò a casa e lo ___ con pane e vino.",
                "palavra_oculta": "sfamò",
                "traducao": "Levou-o para casa e o alimentou com pão e vinho.",
                "dica": "diede da mangiare"
            },
            {
                "id": 5,
                "texto_completo": "Il pescatore non chiede il nome né la storia.",
                "texto_lacuna": "Il pescatore non chiede il ___ né la storia.",
                "palavra_oculta": "nome",
                "traducao": "O pescador não pergunta o nome nem a história.",
                "dica": "come si chiama una persona"
            }
        ]
    },
    "can_166": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Napule è mille culure, Napule è mille paure.",
                "texto_lacuna": "Napule è mille ___, Napule è mille paure.",
                "palavra_oculta": "culure",
                "traducao": "Nápoles tem mil cores, Nápoles tem mil medos.",
                "dica": "dialetto napoletano per 'colori'"
            },
            {
                "id": 2,
                "texto_completo": "Napule è 'a voce d'e creature, Napule è nù sole amaro.",
                "texto_lacuna": "Napule è 'a voce d'e ___, Napule è nù sole amaro.",
                "palavra_oculta": "creature",
                "traducao": "Nápoles é a voz das criaturas, Nápoles é um sol amargo.",
                "dica": "esseri viventi"
            },
            {
                "id": 3,
                "texto_completo": "Napule è nu paese curioso, è miezo malo e miezo bello.",
                "texto_lacuna": "Napule è nu paese ___, è miezo malo e miezo bello.",
                "palavra_oculta": "curioso",
                "traducao": "Nápoles é um lugar curioso, é meio feio e meio bonito.",
                "dica": "strano, interessante"
            },
            {
                "id": 4,
                "texto_completo": "Napule è nu cardillo 'addunato, è na' chitarra stonata.",
                "texto_lacuna": "Napule è nu ___ 'addunato, è na' chitarra stonata.",
                "palavra_oculta": "cardillo",
                "traducao": "Nápoles é um pintassilgo adormecido, é um violão desafinado.",
                "dica": "piccolo uccello canoro"
            },
            {
                "id": 5,
                "texto_completo": "Napule è tutto, e Napule non è niente.",
                "texto_lacuna": "Napule è ___, e Napule non è niente.",
                "palavra_oculta": "tutto",
                "traducao": "Nápoles é tudo, e Nápoles não é nada.",
                "dica": "l'insieme di ogni cosa"
            }
        ]
    },
    "can_167": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Ma il cielo è sempre più blu, la gente è sempre più giù.",
                "texto_lacuna": "Ma il ___ è sempre più blu, la gente è sempre più giù.",
                "palavra_oculta": "cielo",
                "traducao": "Mas o céu está cada vez mais azul, o povo está cada vez mais para baixo.",
                "dica": "volta celeste sopra di noi"
            },
            {
                "id": 2,
                "texto_completo": "Ma il cielo è sempre più blu, su in alto, sempre più su.",
                "texto_lacuna": "Ma il cielo è sempre più ___, su in alto, sempre più su.",
                "palavra_oculta": "blu",
                "traducao": "Mas o céu está cada vez mais azul, lá em cima, cada vez mais para cima.",
                "dica": "colore del mare e del cielo"
            },
            {
                "id": 3,
                "texto_completo": "C'è chi lavora tutto il giorno e non ha tempo di respirare.",
                "texto_lacuna": "C'è chi ___ tutto il giorno e non ha tempo di respirare.",
                "palavra_oculta": "lavora",
                "traducao": "Há quem trabalhe o dia todo e não tenha tempo de respirar.",
                "dica": "terza persona di 'lavorare'"
            },
            {
                "id": 4,
                "texto_completo": "C'è chi ha troppo e chi non ha abbastanza.",
                "texto_lacuna": "C'è chi ha troppo e chi non ha ___.",
                "palavra_oculta": "abbastanza",
                "traducao": "Há quem tenha demais e quem não tenha o suficiente.",
                "dica": "sufficiente, in quantità sufficiente"
            },
            {
                "id": 5,
                "texto_completo": "La vita continua e il cielo rimane azzurro sopra di noi.",
                "texto_lacuna": "La vita ___ e il cielo rimane azzurro sopra di noi.",
                "palavra_oculta": "continua",
                "traducao": "A vida continua e o céu permanece azul sobre nós.",
                "dica": "terza persona di 'continuare'"
            }
        ]
    },
    "can_168": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Un'emozione per sempre, che non finirà.",
                "texto_lacuna": "Un'emozione per sempre, che non ___.",
                "palavra_oculta": "finirà",
                "traducao": "Uma emoção para sempre, que não terminará.",
                "dica": "futuro di 'finire'"
            },
            {
                "id": 2,
                "texto_completo": "Ogni volta che ti guardo sento il cuore tremare.",
                "texto_lacuna": "Ogni volta che ti guardo sento il cuore ___.",
                "palavra_oculta": "tremare",
                "traducao": "Cada vez que te olho sinto o coração tremer.",
                "dica": "vibrare, fremere"
            },
            {
                "id": 3,
                "texto_completo": "Sei la luce nei miei occhi, sei il sole nella mia vita.",
                "texto_lacuna": "Sei la luce nei miei ___, sei il sole nella mia vita.",
                "palavra_oculta": "occhi",
                "traducao": "Você é a luz nos meus olhos, você é o sol na minha vida.",
                "dica": "plurale di 'occhio'"
            },
            {
                "id": 4,
                "texto_completo": "Con te ogni momento è indimenticabile.",
                "texto_lacuna": "Con te ogni momento è ___.",
                "palavra_oculta": "indimenticabile",
                "traducao": "Com você cada momento é inesquecível.",
                "dica": "che non si dimentica"
            },
            {
                "id": 5,
                "texto_completo": "Ti amo con tutta la forza che ho dentro.",
                "texto_lacuna": "Ti amo con tutta la ___ che ho dentro.",
                "palavra_oculta": "forza",
                "traducao": "Te amo com toda a força que tenho dentro.",
                "dica": "energia, potenza"
            }
        ]
    },
    "can_169": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Com'è profondo il mare, com'è profondo.",
                "texto_lacuna": "Com'è ___ il mare, com'è profondo.",
                "palavra_oculta": "profondo",
                "traducao": "Como é profundo o mar, como é profundo.",
                "dica": "opposto di 'superficiale'"
            },
            {
                "id": 2,
                "texto_completo": "Nelle sue acque si nascondono mille segreti.",
                "texto_lacuna": "Nelle sue acque si nascondono mille ___.",
                "palavra_oculta": "segreti",
                "traducao": "Em suas águas se escondem mil segredos.",
                "dica": "cose nascoste, misteri"
            },
            {
                "id": 3,
                "texto_completo": "Come i pensieri che non riesco a esprimere.",
                "texto_lacuna": "Come i pensieri che non riesco a ___.",
                "palavra_oculta": "esprimere",
                "traducao": "Como os pensamentos que não consigo expressar.",
                "dica": "comunicare, dire"
            },
            {
                "id": 4,
                "texto_completo": "Il mare conosce le mie lacrime, le ha già viste.",
                "texto_lacuna": "Il mare ___ le mie lacrime, le ha già viste.",
                "palavra_oculta": "conosce",
                "traducao": "O mar conhece minhas lágrimas, já as viu.",
                "dica": "terza persona di 'conoscere'"
            },
            {
                "id": 5,
                "texto_completo": "Ci sono pesci che nuotano nell'oscurità assoluta.",
                "texto_lacuna": "Ci sono pesci che ___ nell'oscurità assoluta.",
                "palavra_oculta": "nuotano",
                "traducao": "Há peixes que nadam na escuridão absoluta.",
                "dica": "si muovono nell'acqua"
            }
        ]
    },
    "can_170": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Questa canzone è per te che sei lontano.",
                "texto_lacuna": "Questa ___ è per te che sei lontano.",
                "palavra_oculta": "canzone",
                "traducao": "Esta canção é para você que está longe.",
                "dica": "composizione musicale"
            },
            {
                "id": 2,
                "texto_completo": "Ti mando la mia voce attraverso le onde.",
                "texto_lacuna": "Ti mando la mia ___ attraverso le onde.",
                "palavra_oculta": "voce",
                "traducao": "Mando minha voz através das ondas.",
                "dica": "suono prodotto dalla gola"
            },
            {
                "id": 3,
                "texto_completo": "Le parole volano nell'aria verso di te.",
                "texto_lacuna": "Le parole ___ nell'aria verso di te.",
                "palavra_oculta": "volano",
                "traducao": "As palavras voam no ar em direção a você.",
                "dica": "si muovono nell'aria come gli uccelli"
            },
            {
                "id": 4,
                "texto_completo": "Spero che questa melodia ti raggiunga.",
                "texto_lacuna": "Spero che questa ___ ti raggiunga.",
                "palavra_oculta": "melodia",
                "traducao": "Espero que esta melodia te alcance.",
                "dica": "sequenza di note musicali"
            },
            {
                "id": 5,
                "texto_completo": "La musica unisce chi è separato dalla distanza.",
                "texto_lacuna": "La musica ___ chi è separato dalla distanza.",
                "palavra_oculta": "unisce",
                "traducao": "A música une quem está separado pela distância.",
                "dica": "mette insieme, connette"
            }
        ]
    },
    "can_171": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Amarsi un po' per poi lasciarsi andare.",
                "texto_lacuna": "___ un po' per poi lasciarsi andare.",
                "palavra_oculta": "Amarsi",
                "traducao": "Amar-se um pouco para depois se deixar ir.",
                "dica": "riflessivo di 'amare'"
            },
            {
                "id": 2,
                "texto_completo": "È difficile capire dove finisce l'amore.",
                "texto_lacuna": "È ___ capire dove finisce l'amore.",
                "palavra_oculta": "difficile",
                "traducao": "É difícil entender onde o amor termina.",
                "dica": "non facile"
            },
            {
                "id": 3,
                "texto_completo": "Ci siamo amati con tutta la nostra forza.",
                "texto_lacuna": "Ci siamo ___ con tutta la nostra forza.",
                "palavra_oculta": "amati",
                "traducao": "Nos amamos com toda a nossa força.",
                "dica": "participio di 'amare', plurale"
            },
            {
                "id": 4,
                "texto_completo": "Poi qualcosa è cambiato senza che ce ne accorgessimo.",
                "texto_lacuna": "Poi qualcosa è ___ senza che ce ne accorgessimo.",
                "palavra_oculta": "cambiato",
                "traducao": "Depois algo mudou sem que nos déssemos conta.",
                "dica": "participio di 'cambiare'"
            },
            {
                "id": 5,
                "texto_completo": "L'amore non è eterno, ma i ricordi lo sono.",
                "texto_lacuna": "L'amore non è eterno, ma i ___ lo sono.",
                "palavra_oculta": "ricordi",
                "traducao": "O amor não é eterno, mas as memórias são.",
                "dica": "memorie, ciò che si ricorda"
            }
        ]
    },
    "can_172": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Ancora, ancora, ancora ti voglio amare.",
                "texto_lacuna": "___, ancora, ancora ti voglio amare.",
                "palavra_oculta": "Ancora",
                "traducao": "Ainda, ainda, ainda quero te amar.",
                "dica": "di nuovo, un'altra volta"
            },
            {
                "id": 2,
                "texto_completo": "Non mi stanco mai di stare tra le tue braccia.",
                "texto_lacuna": "Non mi ___ mai di stare tra le tue braccia.",
                "palavra_oculta": "stanco",
                "traducao": "Nunca me canso de estar nos seus braços.",
                "dica": "mi stanco = fico cansado"
            },
            {
                "id": 3,
                "texto_completo": "Ogni giorno che passa ti amo di più.",
                "texto_lacuna": "Ogni giorno che passa ti amo di ___.",
                "palavra_oculta": "più",
                "traducao": "Cada dia que passa te amo mais.",
                "dica": "in maggiore quantità"
            },
            {
                "id": 4,
                "texto_completo": "Il tuo calore mi scalda anche nelle notti fredde.",
                "texto_lacuna": "Il tuo ___ mi scalda anche nelle notti fredde.",
                "palavra_oculta": "calore",
                "traducao": "Seu calor me aquece mesmo nas noites frias.",
                "dica": "tepore, temperatura alta"
            },
            {
                "id": 5,
                "texto_completo": "Con te vorrei trascorrere ogni istante della mia vita.",
                "texto_lacuna": "Con te vorrei ___ ogni istante della mia vita.",
                "palavra_oculta": "trascorrere",
                "traducao": "Com você gostaria de passar cada instante da minha vida.",
                "dica": "passare il tempo"
            }
        ]
    },
    "can_173": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Parole, parole, parole, soltanto parole tra noi.",
                "texto_lacuna": "___, parole, parole, soltanto parole tra noi.",
                "palavra_oculta": "Parole",
                "traducao": "Palavras, palavras, palavras, somente palavras entre nós.",
                "dica": "plurale di 'parola'"
            },
            {
                "id": 2,
                "texto_completo": "Mi dici che mi ami ma le parole son vuote.",
                "texto_lacuna": "Mi dici che mi ami ma le parole son ___.",
                "palavra_oculta": "vuote",
                "traducao": "Me diz que me ama mas as palavras são vazias.",
                "dica": "senza contenuto, non sincere"
            },
            {
                "id": 3,
                "texto_completo": "Basta promesse, voglio fatti concreti.",
                "texto_lacuna": "Basta ___, voglio fatti concreti.",
                "palavra_oculta": "promesse",
                "traducao": "Chega de promessas, quero fatos concretos.",
                "dica": "plurale di 'promessa'"
            },
            {
                "id": 4,
                "texto_completo": "Le tue bugie mi hanno ferita profondamente.",
                "texto_lacuna": "Le tue ___ mi hanno ferita profondamente.",
                "palavra_oculta": "bugie",
                "traducao": "Suas mentiras me feriram profundamente.",
                "dica": "menzogne, falsità"
            },
            {
                "id": 5,
                "texto_completo": "Non ci credo più alle tue dolci dichiarazioni.",
                "texto_lacuna": "Non ci credo più alle tue dolci ___.",
                "palavra_oculta": "dichiarazioni",
                "traducao": "Não acredito mais nas suas doces declarações.",
                "dica": "affermazioni, ciò che si dichiara"
            }
        ]
    },
    "can_174": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "L'emozione non ha voce, non sa parlare.",
                "texto_lacuna": "L'___ non ha voce, non sa parlare.",
                "palavra_oculta": "emozione",
                "traducao": "A emoção não tem voz, não sabe falar.",
                "dica": "sentimento intenso"
            },
            {
                "id": 2,
                "texto_completo": "Si esprime con gli occhi, con le mani, col cuore.",
                "texto_lacuna": "Si esprime con gli occhi, con le ___, col cuore.",
                "palavra_oculta": "mani",
                "traducao": "Se expressa com os olhos, com as mãos, com o coração.",
                "dica": "plurale di 'mano'"
            },
            {
                "id": 3,
                "texto_completo": "Quando ti vedo non riesco a dire nemmeno una parola.",
                "texto_lacuna": "Quando ti vedo non riesco a dire nemmeno una ___.",
                "palavra_oculta": "parola",
                "traducao": "Quando te vejo não consigo dizer nem uma palavra.",
                "dica": "termine, vocabolo"
            },
            {
                "id": 4,
                "texto_completo": "Il silenzio tra noi dice più di mille parole.",
                "texto_lacuna": "Il ___ tra noi dice più di mille parole.",
                "palavra_oculta": "silenzio",
                "traducao": "O silêncio entre nós diz mais que mil palavras.",
                "dica": "assenza di suono"
            },
            {
                "id": 5,
                "texto_completo": "Ti guardo e capisco tutto senza bisogno di spiegazioni.",
                "texto_lacuna": "Ti ___ e capisco tutto senza bisogno di spiegazioni.",
                "palavra_oculta": "guardo",
                "traducao": "Te olho e entendo tudo sem precisar de explicações.",
                "dica": "prima persona di 'guardare'"
            }
        ]
    },
    "can_175": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Sono solo canzonette, non prendertela a cuore.",
                "texto_lacuna": "Sono solo ___, non prendertela a cuore.",
                "palavra_oculta": "canzonette",
                "traducao": "São apenas cançõezinhas, não leve a sério.",
                "dica": "diminutivo di 'canzoni'"
            },
            {
                "id": 2,
                "texto_completo": "La musica non cambia il mondo, dicono i potenti.",
                "texto_lacuna": "La musica non ___ il mondo, dicono i potenti.",
                "palavra_oculta": "cambia",
                "traducao": "A música não muda o mundo, dizem os poderosos.",
                "dica": "terza persona di 'cambiare'"
            },
            {
                "id": 3,
                "texto_completo": "Ma una canzone può far piangere, ridere, sperare.",
                "texto_lacuna": "Ma una canzone può far ___, ridere, sperare.",
                "palavra_oculta": "piangere",
                "traducao": "Mas uma canção pode fazer chorar, rir, esperar.",
                "dica": "versare lacrime"
            },
            {
                "id": 4,
                "texto_completo": "Le parole delle canzoni restano nell'anima per sempre.",
                "texto_lacuna": "Le parole delle canzoni ___ nell'anima per sempre.",
                "palavra_oculta": "restano",
                "traducao": "As palavras das canções ficam na alma para sempre.",
                "dica": "rimangono, non se ne vanno"
            },
            {
                "id": 5,
                "texto_completo": "Cantare è resistere, è un atto di libertà.",
                "texto_lacuna": "Cantare è ___, è un atto di libertà.",
                "palavra_oculta": "resistere",
                "traducao": "Cantar é resistir, é um ato de liberdade.",
                "dica": "opporsi, non cedere"
            }
        ]
    },
    "can_176": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Sei bellissima quando sorridi così.",
                "texto_lacuna": "Sei ___ quando sorridi così.",
                "palavra_oculta": "bellissima",
                "traducao": "Você é lindíssima quando sorri assim.",
                "dica": "superlativo di 'bella'"
            },
            {
                "id": 2,
                "texto_completo": "I tuoi capelli brillano come l'oro al sole.",
                "texto_lacuna": "I tuoi capelli ___ come l'oro al sole.",
                "palavra_oculta": "brillano",
                "traducao": "Seu cabelo brilha como ouro ao sol.",
                "dica": "luccicano, emanano luce"
            },
            {
                "id": 3,
                "texto_completo": "Ogni volta che entri in una stanza tutti si girano.",
                "texto_lacuna": "Ogni volta che entri in una stanza tutti si ___.",
                "palavra_oculta": "girano",
                "traducao": "Toda vez que você entra numa sala todos se viram.",
                "dica": "si voltano, si rivolgono"
            },
            {
                "id": 4,
                "texto_completo": "La tua bellezza è naturale, senza artifici.",
                "texto_lacuna": "La tua ___ è naturale, senza artifici.",
                "palavra_oculta": "bellezza",
                "traducao": "Sua beleza é natural, sem artifícios.",
                "dica": "qualità di chi è bello"
            },
            {
                "id": 5,
                "texto_completo": "Sei bellissima, sei bellissima davvero.",
                "texto_lacuna": "Sei bellissima, sei bellissima ___.",
                "palavra_oculta": "davvero",
                "traducao": "Você é lindíssima, você é lindíssima de verdade.",
                "dica": "veramente, in modo sincero"
            }
        ]
    },
    "can_177": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Romagna mia, Romagna soave, terra e sole e canti.",
                "texto_lacuna": "Romagna mia, Romagna ___, terra e sole e canti.",
                "palavra_oculta": "soave",
                "traducao": "Romanha minha, Romanha suave, terra e sol e cantos.",
                "dica": "dolce, delicata"
            },
            {
                "id": 2,
                "texto_completo": "Nelle colline verdi cresce l'uva e il grano.",
                "texto_lacuna": "Nelle colline verdi cresce l'___ e il grano.",
                "palavra_oculta": "uva",
                "traducao": "Nas colinas verdes cresce a uva e o trigo.",
                "dica": "frutto per fare il vino"
            },
            {
                "id": 3,
                "texto_completo": "Il mare Adriatico bagna le coste della Romagna.",
                "texto_lacuna": "Il mare ___ bagna le coste della Romagna.",
                "palavra_oculta": "Adriatico",
                "traducao": "O mar Adriático banha as costas da Romanha.",
                "dica": "mare tra Italia e Balcani"
            },
            {
                "id": 4,
                "texto_completo": "La gente romagnola balla il liscio con passione.",
                "texto_lacuna": "La gente romagnola ___ il liscio con passione.",
                "palavra_oculta": "balla",
                "traducao": "O povo romagnolo dança o liscio com paixão.",
                "dica": "terza persona di 'ballare'"
            },
            {
                "id": 5,
                "texto_completo": "Questa terra è nel mio cuore per sempre.",
                "texto_lacuna": "Questa ___ è nel mio cuore per sempre.",
                "palavra_oculta": "terra",
                "traducao": "Esta terra está no meu coração para sempre.",
                "dica": "suolo, regione, paese"
            }
        ]
    },
    "can_178": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "La donna dei sogni esiste soltanto nei sogni.",
                "texto_lacuna": "La donna dei ___ esiste soltanto nei sogni.",
                "palavra_oculta": "sogni",
                "traducao": "A mulher dos sonhos existe somente nos sonhos.",
                "dica": "plurale di 'sogno'"
            },
            {
                "id": 2,
                "texto_completo": "La cerco ogni notte e la trovo nell'alba.",
                "texto_lacuna": "La cerco ogni notte e la trovo nell'___.",
                "palavra_oculta": "alba",
                "traducao": "A procuro cada noite e a encontro no amanhecer.",
                "dica": "momento prima del sorgere del sole"
            },
            {
                "id": 3,
                "texto_completo": "Ha gli occhi che brillano come stelle lontane.",
                "texto_lacuna": "Ha gli occhi che ___ come stelle lontane.",
                "palavra_oculta": "brillano",
                "traducao": "Tem olhos que brilham como estrelas distantes.",
                "dica": "luccicano, risplendono"
            },
            {
                "id": 4,
                "texto_completo": "Ma quando mi sveglio lei svanisce nell'aria.",
                "texto_lacuna": "Ma quando mi sveglio lei ___ nell'aria.",
                "palavra_oculta": "svanisce",
                "traducao": "Mas quando acordo ela desvanece no ar.",
                "dica": "sparisce, si dissolve"
            },
            {
                "id": 5,
                "texto_completo": "Forse un giorno troverò la donna dei miei sogni.",
                "texto_lacuna": "Forse un giorno ___ la donna dei miei sogni.",
                "palavra_oculta": "troverò",
                "traducao": "Talvez um dia encontrarei a mulher dos meus sonhos.",
                "dica": "futuro di 'trovare'"
            }
        ]
    },
    "can_179": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Come musica nella notte, tu arrivi e illumini tutto.",
                "texto_lacuna": "Come ___ nella notte, tu arrivi e illumini tutto.",
                "palavra_oculta": "musica",
                "traducao": "Como música na noite, você chega e ilumina tudo.",
                "dica": "arte dei suoni"
            },
            {
                "id": 2,
                "texto_completo": "La tua presenza riempie ogni silenzio.",
                "texto_lacuna": "La tua ___ riempie ogni silenzio.",
                "palavra_oculta": "presenza",
                "traducao": "Sua presença preenche cada silêncio.",
                "dica": "essere presente, esserci"
            },
            {
                "id": 3,
                "texto_completo": "Come una melodia che non riesco a dimenticare.",
                "texto_lacuna": "Come una ___ che non riesco a dimenticare.",
                "palavra_oculta": "melodia",
                "traducao": "Como uma melodia que não consigo esquecer.",
                "dica": "sequenza armoniosa di note"
            },
            {
                "id": 4,
                "texto_completo": "Tu sei il ritmo del mio cuore, la mia canzone.",
                "texto_lacuna": "Tu sei il ___ del mio cuore, la mia canzone.",
                "palavra_oculta": "ritmo",
                "traducao": "Você é o ritmo do meu coração, minha canção.",
                "dica": "cadenza, battito regolare"
            },
            {
                "id": 5,
                "texto_completo": "Senza di te la vita sarebbe silenziosa e vuota.",
                "texto_lacuna": "Senza di te la vita sarebbe ___ e vuota.",
                "palavra_oculta": "silenziosa",
                "traducao": "Sem você a vida seria silenciosa e vazia.",
                "dica": "priva di suoni"
            }
        ]
    },
    "can_180": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Sogno e son desto, non so se dormo o veglio.",
                "texto_lacuna": "Sogno e son ___, non so se dormo o veglio.",
                "palavra_oculta": "desto",
                "traducao": "Sonho e estou acordado, não sei se durmo ou vigio.",
                "dica": "sveglio, non addormentato"
            },
            {
                "id": 2,
                "texto_completo": "La realtà e il sogno si confondono nella mia mente.",
                "texto_lacuna": "La realtà e il sogno si ___ nella mia mente.",
                "palavra_oculta": "confondono",
                "traducao": "A realidade e o sonho se confundem na minha mente.",
                "dica": "si mescolano, non si distinguono"
            },
            {
                "id": 3,
                "texto_completo": "Vivo in un mondo tra il reale e l'immaginario.",
                "texto_lacuna": "Vivo in un mondo tra il reale e l'___.",
                "palavra_oculta": "immaginario",
                "traducao": "Vivo num mundo entre o real e o imaginário.",
                "dica": "frutto dell'immaginazione"
            },
            {
                "id": 4,
                "texto_completo": "Napoli, la mia città, è un sogno ad occhi aperti.",
                "texto_lacuna": "Napoli, la mia ___, è un sogno ad occhi aperti.",
                "palavra_oculta": "città",
                "traducao": "Nápoles, minha cidade, é um sonho a olhos abertos.",
                "dica": "centro urbano, metropoli"
            },
            {
                "id": 5,
                "texto_completo": "Canto per non dimenticare chi ero e chi sono.",
                "texto_lacuna": "___ per non dimenticare chi ero e chi sono.",
                "palavra_oculta": "Canto",
                "traducao": "Canto para não esquecer quem era e quem sou.",
                "dica": "prima persona di 'cantare'"
            }
        ]
    },
    "can_181": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Nessun dorma! Nessun dorma! Tu pure, o Principessa.",
                "texto_lacuna": "Nessun dorma! Nessun dorma! Tu pure, o ___.",
                "palavra_oculta": "Principessa",
                "traducao": "Ninguém durma! Ninguém durma! Você também, ó Princesa.",
                "dica": "figlia di re e regina"
            },
            {
                "id": 2,
                "texto_completo": "Nella tua fredda stanza guardi le stelle che tremano.",
                "texto_lacuna": "Nella tua fredda ___ guardi le stelle che tremano.",
                "palavra_oculta": "stanza",
                "traducao": "Em seu frio quarto você olha as estrelas que tremem.",
                "dica": "camera, locale"
            },
            {
                "id": 3,
                "texto_completo": "Ma il mio mistero è chiuso in me, nessuno saprà il mio nome.",
                "texto_lacuna": "Ma il mio ___ è chiuso in me, nessuno saprà il mio nome.",
                "palavra_oculta": "mistero",
                "traducao": "Mas o meu mistério está fechado em mim, ninguém saberá o meu nome.",
                "dica": "segreto, enigma"
            },
            {
                "id": 4,
                "texto_completo": "All'alba vincerò, vincerò, vincerò!",
                "texto_lacuna": "All'alba ___, vincerò, vincerò!",
                "palavra_oculta": "vincerò",
                "traducao": "Ao amanhecer vencerei, vencerei, vencerei!",
                "dica": "futuro di 'vincere'"
            },
            {
                "id": 5,
                "texto_completo": "Tramontate, stelle! All'alba vincerò!",
                "texto_lacuna": "___, stelle! All'alba vincerò!",
                "palavra_oculta": "Tramontate",
                "traducao": "Ponde-se, estrelas! Ao amanhecer vencerei!",
                "dica": "imperativo di 'tramontare'"
            }
        ]
    },
    "can_182": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "O mio babbino caro, mi piace, è bello bello.",
                "texto_lacuna": "O mio ___ caro, mi piace, è bello bello.",
                "palavra_oculta": "babbino",
                "traducao": "Ó meu querido papai, eu gosto, ele é muito bonito.",
                "dica": "termine affettuoso per il padre"
            },
            {
                "id": 2,
                "texto_completo": "Vo' andare in Porta Rossa a comperar l'anello!",
                "texto_lacuna": "Vo' andare in Porta Rossa a ___ l'anello!",
                "palavra_oculta": "comperar",
                "traducao": "Vou à Porta Rossa comprar o anel!",
                "dica": "comperare, acquistare"
            },
            {
                "id": 3,
                "texto_completo": "Se l'amassi indarno, andrei sul Ponte Vecchio.",
                "texto_lacuna": "Se l'amassi indarno, andrei sul ___ Vecchio.",
                "palavra_oculta": "Ponte",
                "traducao": "Se o amasse em vão, iria para o Ponte Vecchio.",
                "dica": "struttura che attraversa un fiume"
            },
            {
                "id": 4,
                "texto_completo": "Mi butterrei nell'Arno! Mi butterrei!",
                "texto_lacuna": "Mi ___ nell'Arno! Mi butterrei!",
                "palavra_oculta": "butterrei",
                "traducao": "Me jogaria no Arno! Me jogaria!",
                "dica": "condizionale di 'buttarsi'"
            },
            {
                "id": 5,
                "texto_completo": "Babbo, pietà, pietà! Ho il cuore affannato.",
                "texto_lacuna": "Babbo, ___, pietà! Ho il cuore affannato.",
                "palavra_oculta": "pietà",
                "traducao": "Papai, piedade, piedade! Tenho o coração angustiado.",
                "dica": "compassione, misericordia"
            }
        ]
    },
    "can_183": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Una furtiva lagrima negli occhi suoi spuntò.",
                "texto_lacuna": "Una furtiva ___ negli occhi suoi spuntò.",
                "palavra_oculta": "lagrima",
                "traducao": "Uma furtiva lágrima em seus olhos brotou.",
                "dica": "goccia di pianto"
            },
            {
                "id": 2,
                "texto_completo": "Quelle festose giovani invidiar sembrò.",
                "texto_lacuna": "Quelle festose giovani ___ sembrò.",
                "palavra_oculta": "invidiar",
                "traducao": "Pareceu invejar aquelas jovens festivas.",
                "dica": "desiderare ciò che altri hanno"
            },
            {
                "id": 3,
                "texto_completo": "Che più cercando io vo'? Che più cercando io vo'?",
                "texto_lacuna": "Che più ___ io vo'? Che più cercando io vo'?",
                "palavra_oculta": "cercando",
                "traducao": "Que mais estou procurando? Que mais estou procurando?",
                "dica": "gerundio di 'cercare'"
            },
            {
                "id": 4,
                "texto_completo": "M'ama, lo vedo. Un solo istante i palpiti.",
                "texto_lacuna": "M'ama, lo vedo. Un solo ___ i palpiti.",
                "palavra_oculta": "istante",
                "traducao": "Ela me ama, eu vejo. Um único instante as palpitações.",
                "dica": "momento brevissimo"
            },
            {
                "id": 5,
                "texto_completo": "Del suo bel cor sentire, de' suoi sospir mischiar.",
                "texto_lacuna": "Del suo bel cor ___, de' suoi sospir mischiar.",
                "palavra_oculta": "sentire",
                "traducao": "Sentir seu belo coração, misturar com seus suspiros.",
                "dica": "percepire, udire"
            }
        ]
    },
    "can_184": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "L'aurora dipinge il cielo di mille colori.",
                "texto_lacuna": "L'___ dipinge il cielo di mille colori.",
                "palavra_oculta": "aurora",
                "traducao": "A aurora pinta o céu de mil cores.",
                "dica": "alba, primo chiarore del giorno"
            },
            {
                "id": 2,
                "texto_completo": "Un nuovo giorno comincia con speranza.",
                "texto_lacuna": "Un nuovo giorno ___ con speranza.",
                "palavra_oculta": "comincia",
                "traducao": "Um novo dia começa com esperança.",
                "dica": "inizia, ha inizio"
            },
            {
                "id": 3,
                "texto_completo": "Ti aspetto come si aspetta l'alba dopo una lunga notte.",
                "texto_lacuna": "Ti ___ come si aspetta l'alba dopo una lunga notte.",
                "palavra_oculta": "aspetto",
                "traducao": "Espero por você como se espera o amanhecer após uma longa noite.",
                "dica": "prima persona di 'aspettare'"
            },
            {
                "id": 4,
                "texto_completo": "Il sole nascente illumina la strada davanti a noi.",
                "texto_lacuna": "Il sole ___ illumina la strada davanti a noi.",
                "palavra_oculta": "nascente",
                "traducao": "O sol nascente ilumina o caminho à nossa frente.",
                "dica": "che sta nascendo, sorgente"
            },
            {
                "id": 5,
                "texto_completo": "Con te ogni aurora è più bella e più dolce.",
                "texto_lacuna": "Con te ogni aurora è più ___ e più dolce.",
                "palavra_oculta": "bella",
                "traducao": "Com você cada aurora é mais bonita e mais doce.",
                "dica": "esteticamente piacevole"
            }
        ]
    },
    "can_185": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Inevitabile, era inevitabile amarti così.",
                "texto_lacuna": "___, era inevitabile amarti così.",
                "palavra_oculta": "Inevitabile",
                "traducao": "Inevitável, era inevitável te amar assim.",
                "dica": "che non si può evitare"
            },
            {
                "id": 2,
                "texto_completo": "Sapevo che sarebbe finita con il cuore spezzato.",
                "texto_lacuna": "Sapevo che sarebbe finita con il cuore ___.",
                "palavra_oculta": "spezzato",
                "traducao": "Sabia que terminaria com o coração partido.",
                "dica": "rotto, in pezzi"
            },
            {
                "id": 3,
                "texto_completo": "Eppure non potevo fare a meno di te.",
                "texto_lacuna": "Eppure non potevo ___ a meno di te.",
                "palavra_oculta": "fare",
                "traducao": "Mesmo assim não conseguia viver sem você.",
                "dica": "fare a meno = prescindir"
            },
            {
                "id": 4,
                "texto_completo": "L'amore è così, ti prende e non ti lascia andare.",
                "texto_lacuna": "L'amore è così, ti ___ e non ti lascia andare.",
                "palavra_oculta": "prende",
                "traducao": "O amor é assim, te pega e não te deixa ir.",
                "dica": "afferra, cattura"
            },
            {
                "id": 5,
                "texto_completo": "Anche sapendo il finale, lo farei ancora.",
                "texto_lacuna": "Anche sapendo il ___, lo farei ancora.",
                "palavra_oculta": "finale",
                "traducao": "Mesmo sabendo o final, faria de novo.",
                "dica": "la fine, la conclusione"
            }
        ]
    },
    "can_186": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Io canto, canto, canto per non sentire il vuoto.",
                "texto_lacuna": "Io ___, canto, canto per non sentire il vuoto.",
                "palavra_oculta": "canto",
                "traducao": "Eu canto, canto, canto para não sentir o vazio.",
                "dica": "prima persona di 'cantare'"
            },
            {
                "id": 2,
                "texto_completo": "La musica è la mia salvezza nei momenti bui.",
                "texto_lacuna": "La musica è la mia ___ nei momenti bui.",
                "palavra_oculta": "salvezza",
                "traducao": "A música é minha salvação nos momentos sombrios.",
                "dica": "salvare, liberarsi dal pericolo"
            },
            {
                "id": 3,
                "texto_completo": "Canto quando sono triste, canto quando sono felice.",
                "texto_lacuna": "Canto quando sono ___, canto quando sono felice.",
                "palavra_oculta": "triste",
                "traducao": "Canto quando estou triste, canto quando estou feliz.",
                "dica": "contrario di 'felice'"
            },
            {
                "id": 4,
                "texto_completo": "Ogni nota è un pezzo del mio cuore.",
                "texto_lacuna": "Ogni ___ è un pezzo del mio cuore.",
                "palavra_oculta": "nota",
                "traducao": "Cada nota é um pedaço do meu coração.",
                "dica": "suono musicale"
            },
            {
                "id": 5,
                "texto_completo": "Cantare mi fa sentire viva, reale, presente.",
                "texto_lacuna": "Cantare mi fa sentire ___, reale, presente.",
                "palavra_oculta": "viva",
                "traducao": "Cantar me faz sentir viva, real, presente.",
                "dica": "femminile di 'vivo'"
            }
        ]
    },
    "can_187": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Invece no, invece no, non è così che va.",
                "texto_lacuna": "Invece no, invece no, non è ___ che va.",
                "palavra_oculta": "così",
                "traducao": "Ao contrário não, ao contrário não, não é assim que vai.",
                "dica": "in questo modo"
            },
            {
                "id": 2,
                "texto_completo": "Mi aspettavo di più, mi aspettavo altro.",
                "texto_lacuna": "Mi ___ di più, mi aspettavo altro.",
                "palavra_oculta": "aspettavo",
                "traducao": "Esperava mais, esperava outra coisa.",
                "dica": "imperfetto di 'aspettarsi'"
            },
            {
                "id": 3,
                "texto_completo": "Le promesse fatte nell'amore non si mantengono.",
                "texto_lacuna": "Le promesse fatte nell'amore non si ___.",
                "palavra_oculta": "mantengono",
                "traducao": "As promessas feitas no amor não se mantêm.",
                "dica": "terza persona di 'mantenere'"
            },
            {
                "id": 4,
                "texto_completo": "Il cuore ingannato impara a non fidarsi più.",
                "texto_lacuna": "Il cuore ___ impara a non fidarsi più.",
                "palavra_oculta": "ingannato",
                "traducao": "O coração enganado aprende a não mais confiar.",
                "dica": "tradito, deluso"
            },
            {
                "id": 5,
                "texto_completo": "Invece no, la vita non è una favola.",
                "texto_lacuna": "Invece no, la vita non è una ___.",
                "palavra_oculta": "favola",
                "traducao": "Ao contrário não, a vida não é um conto de fadas.",
                "dica": "racconto fantastico"
            }
        ]
    },
    "can_188": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Benvenuto a questo mondo che non ti aspettava.",
                "texto_lacuna": "___ a questo mondo che non ti aspettava.",
                "palavra_oculta": "Benvenuto",
                "traducao": "Bem-vindo a este mundo que não te esperava.",
                "dica": "saluto di accoglienza"
            },
            {
                "id": 2,
                "texto_completo": "Ogni giorno è una nuova battaglia da combattere.",
                "texto_lacuna": "Ogni giorno è una nuova ___ da combattere.",
                "palavra_oculta": "battaglia",
                "traducao": "Cada dia é uma nova batalha a combater.",
                "dica": "conflitto, scontro"
            },
            {
                "id": 3,
                "texto_completo": "Le città moderne ci inghiottono e ci sperdono.",
                "texto_lacuna": "Le città moderne ci ___ e ci sperdono.",
                "palavra_oculta": "inghiottono",
                "traducao": "As cidades modernas nos engolindo e nos perdem.",
                "dica": "assorbono, inglobano"
            },
            {
                "id": 4,
                "texto_completo": "Cerco la mia identità tra le macerie del presente.",
                "texto_lacuna": "Cerco la mia ___ tra le macerie del presente.",
                "palavra_oculta": "identità",
                "traducao": "Procuro minha identidade entre os escombros do presente.",
                "dica": "chi si è, la propria essenza"
            },
            {
                "id": 5,
                "texto_completo": "Resistiamo insieme, siamo la stessa razza.",
                "texto_lacuna": "___ insieme, siamo la stessa razza.",
                "palavra_oculta": "Resistiamo",
                "traducao": "Resistimos juntos, somos a mesma raça.",
                "dica": "prima persona plurale di 'resistere'"
            }
        ]
    },
    "can_189": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Quello che le donne non dicono si legge negli occhi.",
                "texto_lacuna": "Quello che le donne non ___ si legge negli occhi.",
                "palavra_oculta": "dicono",
                "traducao": "O que as mulheres não dizem se lê nos olhos.",
                "dica": "terza persona plurale di 'dire'"
            },
            {
                "id": 2,
                "texto_completo": "Un sorriso può nascondere mille silenzi.",
                "texto_lacuna": "Un sorriso può ___ mille silenzi.",
                "palavra_oculta": "nascondere",
                "traducao": "Um sorriso pode esconder mil silêncios.",
                "dica": "celare, non mostrare"
            },
            {
                "id": 3,
                "texto_completo": "Le parole non dette pesano come macigni.",
                "texto_lacuna": "Le parole non dette ___ come macigni.",
                "palavra_oculta": "pesano",
                "traducao": "As palavras não ditas pesam como pedras.",
                "dica": "hanno peso, gravano"
            },
            {
                "id": 4,
                "texto_completo": "Una donna porta dentro mille mondi segreti.",
                "texto_lacuna": "Una donna porta dentro mille mondi ___.",
                "palavra_oculta": "segreti",
                "traducao": "Uma mulher carrega dentro mil mundos secretos.",
                "dica": "nascosti, riservati"
            },
            {
                "id": 5,
                "texto_completo": "Ascoltala bene, non solo le parole ma l'anima.",
                "texto_lacuna": "Ascoltala bene, non solo le ___ ma l'anima.",
                "palavra_oculta": "parole",
                "traducao": "Ouça-a bem, não apenas as palavras mas a alma.",
                "dica": "ciò che si dice"
            }
        ]
    },
    "can_190": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Al caffè del mattino inizio ogni giornata.",
                "texto_lacuna": "Al ___ del mattino inizio ogni giornata.",
                "palavra_oculta": "caffè",
                "traducao": "No café da manhã começo cada dia.",
                "dica": "bevanda calda nera"
            },
            {
                "id": 2,
                "texto_completo": "L'aroma del caffè risveglia i ricordi più dolci.",
                "texto_lacuna": "L'___ del caffè risveglia i ricordi più dolci.",
                "palavra_oculta": "aroma",
                "traducao": "O aroma do café desperta as memórias mais doces.",
                "dica": "profumo, odore piacevole"
            },
            {
                "id": 3,
                "texto_completo": "Sorseggio lentamente guardando il mondo svegliarsi.",
                "texto_lacuna": "___ lentamente guardando il mondo svegliarsi.",
                "palavra_oculta": "Sorseggio",
                "traducao": "Sorvo lentamente observando o mundo acordar.",
                "dica": "bevo a piccoli sorsi"
            },
            {
                "id": 4,
                "texto_completo": "Il mattino ha l'oro in bocca, si dice.",
                "texto_lacuna": "Il ___ ha l'oro in bocca, si dice.",
                "palavra_oculta": "mattino",
                "traducao": "A manhã tem ouro na boca, dizem.",
                "dica": "prima parte del giorno"
            },
            {
                "id": 5,
                "texto_completo": "La vita è più bella con una tazza di caffè caldo.",
                "texto_lacuna": "La vita è più bella con una ___ di caffè caldo.",
                "palavra_oculta": "tazza",
                "traducao": "A vida é mais bonita com uma xícara de café quente.",
                "dica": "recipiente per bevande calde"
            }
        ]
    },
    "can_191": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Almeno tu nell'universo, sei la cosa più gentile.",
                "texto_lacuna": "Almeno tu nell'universo, sei la cosa più ___.",
                "palavra_oculta": "gentile",
                "traducao": "Pelo menos você no universo, é a coisa mais gentil.",
                "dica": "cortese, educato, buono"
            },
            {
                "id": 2,
                "texto_completo": "Il tuo sorriso è la mia ancora di salvezza.",
                "texto_lacuna": "Il tuo sorriso è la mia ___ di salvezza.",
                "palavra_oculta": "ancora",
                "traducao": "Seu sorriso é minha âncora de salvação.",
                "dica": "oggetto che tiene ferma la nave"
            },
            {
                "id": 3,
                "texto_completo": "Nel caos del mondo tu sei il mio punto fermo.",
                "texto_lacuna": "Nel caos del mondo tu sei il mio punto ___.",
                "palavra_oculta": "fermo",
                "traducao": "No caos do mundo você é meu ponto fixo.",
                "dica": "stabile, che non si muove"
            },
            {
                "id": 4,
                "texto_completo": "Senza di te sarei perduto nell'oscurità.",
                "texto_lacuna": "Senza di te sarei ___ nell'oscurità.",
                "palavra_oculta": "perduto",
                "traducao": "Sem você estaria perdido na escuridão.",
                "dica": "participio di 'perdere'"
            },
            {
                "id": 5,
                "texto_completo": "Almeno tu, tra tante delusioni, sei rimasto vero.",
                "texto_lacuna": "Almeno tu, tra tante ___, sei rimasto vero.",
                "palavra_oculta": "delusioni",
                "traducao": "Pelo menos você, entre tantas decepções, ficou verdadeiro.",
                "dica": "disppuntamenti, frustrazioni"
            }
        ]
    },
    "can_192": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Vedrai, vedrai, vedrai che non è finita.",
                "texto_lacuna": "___, vedrai, vedrai che non è finita.",
                "palavra_oculta": "Vedrai",
                "traducao": "Verá, verá, verá que não acabou.",
                "dica": "futuro di 'vedere'"
            },
            {
                "id": 2,
                "texto_completo": "L'amore che sembra spento può ancora accendersi.",
                "texto_lacuna": "L'amore che sembra spento può ancora ___.",
                "palavra_oculta": "accendersi",
                "traducao": "O amor que parece apagado ainda pode se acender.",
                "dica": "riflessivo di 'accendere'"
            },
            {
                "id": 3,
                "texto_completo": "Vedrai che torneranno i giorni sereni.",
                "texto_lacuna": "Vedrai che ___ i giorni sereni.",
                "palavra_oculta": "torneranno",
                "traducao": "Verá que voltarão os dias serenos.",
                "dica": "futuro di 'tornare', plurale"
            },
            {
                "id": 4,
                "texto_completo": "Ogni notte oscura è seguita dall'alba.",
                "texto_lacuna": "Ogni notte oscura è ___ dall'alba.",
                "palavra_oculta": "seguita",
                "traducao": "Cada noite escura é seguida pelo amanhecer.",
                "dica": "participio di 'seguire', femminile"
            },
            {
                "id": 5,
                "texto_completo": "Abbi fede, il meglio deve ancora venire.",
                "texto_lacuna": "Abbi ___, il meglio deve ancora venire.",
                "palavra_oculta": "fede",
                "traducao": "Tenha fé, o melhor ainda está por vir.",
                "dica": "fiducia, credenza"
            }
        ]
    },
    "can_193": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Ciao amore, ciao, me ne vado lontano.",
                "texto_lacuna": "Ciao ___, ciao, me ne vado lontano.",
                "palavra_oculta": "amore",
                "traducao": "Tchau amor, tchau, vou embora para longe.",
                "dica": "sentimento, persona amata"
            },
            {
                "id": 2,
                "texto_completo": "Non so se tornerò, non so se rivedrò questo cielo.",
                "texto_lacuna": "Non so se ___, non so se rivedrò questo cielo.",
                "palavra_oculta": "tornerò",
                "traducao": "Não sei se voltarei, não sei se verei este céu novamente.",
                "dica": "futuro di 'tornare'"
            },
            {
                "id": 3,
                "texto_completo": "Porto con me il tuo sorriso come un talismano.",
                "texto_lacuna": "Porto con me il tuo ___ come un talismano.",
                "palavra_oculta": "sorriso",
                "traducao": "Levo comigo seu sorriso como um talismã.",
                "dica": "espressione del viso felice"
            },
            {
                "id": 4,
                "texto_completo": "La distanza non spegnerà mai il mio amore per te.",
                "texto_lacuna": "La ___ non spegnerà mai il mio amore per te.",
                "palavra_oculta": "distanza",
                "traducao": "A distância nunca apagará meu amor por você.",
                "dica": "spazio tra due persone"
            },
            {
                "id": 5,
                "texto_completo": "Ciao amore, ti ricorderò in ogni momento.",
                "texto_lacuna": "Ciao amore, ti ___ in ogni momento.",
                "palavra_oculta": "ricorderò",
                "traducao": "Tchau amor, vou me lembrar de você em cada momento.",
                "dica": "futuro di 'ricordare'"
            }
        ]
    },
    "can_194": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Il cielo in una stanza, quando sei qui con me.",
                "texto_lacuna": "Il cielo in una ___, quando sei qui con me.",
                "palavra_oculta": "stanza",
                "traducao": "O céu num quarto, quando você está aqui comigo.",
                "dica": "camera, locale interno"
            },
            {
                "id": 2,
                "texto_completo": "Le pareti scompaiono e vedo il cielo sopra di noi.",
                "texto_lacuna": "Le ___ scompaiono e vedo il cielo sopra di noi.",
                "palavra_oculta": "pareti",
                "traducao": "As paredes desaparecem e vejo o céu acima de nós.",
                "dica": "muri interni di una stanza"
            },
            {
                "id": 3,
                "texto_completo": "Con te il mondo diventa infinito e meraviglioso.",
                "texto_lacuna": "Con te il mondo diventa ___ e meraviglioso.",
                "palavra_oculta": "infinito",
                "traducao": "Com você o mundo se torna infinito e maravilhoso.",
                "dica": "senza fine, illimitato"
            },
            {
                "id": 4,
                "texto_completo": "Il tuo abbraccio è il posto più sicuro del mondo.",
                "texto_lacuna": "Il tuo abbraccio è il posto più ___ del mondo.",
                "palavra_oculta": "sicuro",
                "traducao": "Seu abraço é o lugar mais seguro do mundo.",
                "dica": "protetto, senza pericoli"
            },
            {
                "id": 5,
                "texto_completo": "Restiamo qui, sospesi tra la terra e il cielo.",
                "texto_lacuna": "___ qui, sospesi tra la terra e il cielo.",
                "palavra_oculta": "Restiamo",
                "traducao": "Ficamos aqui, suspensos entre a terra e o céu.",
                "dica": "prima persona plurale di 'restare'"
            }
        ]
    },
    "can_195": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Pensieri e parole, mille immagini dentro di me.",
                "texto_lacuna": "___ e parole, mille immagini dentro di me.",
                "palavra_oculta": "Pensieri",
                "traducao": "Pensamentos e palavras, mil imagens dentro de mim.",
                "dica": "plurale di 'pensiero'"
            },
            {
                "id": 2,
                "texto_completo": "La mente non si ferma mai, corre sempre.",
                "texto_lacuna": "La mente non si ferma mai, ___ sempre.",
                "palavra_oculta": "corre",
                "traducao": "A mente nunca para, corre sempre.",
                "dica": "si muove velocemente"
            },
            {
                "id": 3,
                "texto_completo": "Vorrei mettere ordine nei miei sentimenti.",
                "texto_lacuna": "Vorrei mettere ___ nei miei sentimenti.",
                "palavra_oculta": "ordine",
                "traducao": "Gostaria de colocar ordem nos meus sentimentos.",
                "dica": "organizzazione, sistemazione"
            },
            {
                "id": 4,
                "texto_completo": "Ma le emozioni non obbediscono alla ragione.",
                "texto_lacuna": "Ma le emozioni non ___ alla ragione.",
                "palavra_oculta": "obbediscono",
                "traducao": "Mas as emoções não obedecem à razão.",
                "dica": "si sottomettono, seguono le regole"
            },
            {
                "id": 5,
                "texto_completo": "I pensieri volano liberi e le parole restano.",
                "texto_lacuna": "I pensieri volano ___ e le parole restano.",
                "palavra_oculta": "liberi",
                "traducao": "Os pensamentos voam livres e as palavras ficam.",
                "dica": "senza vincoli, non prigionieri"
            }
        ]
    },
    "can_196": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Perduto amor, ho perso il senso della realtà.",
                "texto_lacuna": "___ amor, ho perso il senso della realtà.",
                "palavra_oculta": "Perduto",
                "traducao": "Amor perdido, perdi o senso da realidade.",
                "dica": "participio di 'perdere'"
            },
            {
                "id": 2,
                "texto_completo": "Il tuo ricordo è una ferita ancora aperta.",
                "texto_lacuna": "Il tuo ricordo è una ___ ancora aperta.",
                "palavra_oculta": "ferita",
                "traducao": "Sua memória é uma ferida ainda aberta.",
                "dica": "lesione, danno fisico o emotivo"
            },
            {
                "id": 3,
                "texto_completo": "Cerco di dimenticare ma non ci riesco.",
                "texto_lacuna": "Cerco di ___ ma non ci riesco.",
                "palavra_oculta": "dimenticare",
                "traducao": "Tento esquecer mas não consigo.",
                "dica": "non ricordare più"
            },
            {
                "id": 4,
                "texto_completo": "L'amore perduto lascia un vuoto incolmabile.",
                "texto_lacuna": "L'amore perduto lascia un vuoto ___.",
                "palavra_oculta": "incolmabile",
                "traducao": "O amor perdido deixa um vazio inpreenchível.",
                "dica": "che non si può riempire"
            },
            {
                "id": 5,
                "texto_completo": "Forse un giorno troverò la pace in questo dolore.",
                "texto_lacuna": "Forse un giorno troverò la ___ in questo dolore.",
                "palavra_oculta": "pace",
                "traducao": "Talvez um dia encontrarei a paz nesta dor.",
                "dica": "quiete, assenza di conflitto"
            }
        ]
    },
    "can_197": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "La luna e il sole, opposti che si amano.",
                "texto_lacuna": "La ___ e il sole, opposti che si amano.",
                "palavra_oculta": "luna",
                "traducao": "A lua e o sol, opostos que se amam.",
                "dica": "satellite naturale della Terra"
            },
            {
                "id": 2,
                "texto_completo": "Il giorno e la notte si inseguono senza sosta.",
                "texto_lacuna": "Il giorno e la notte si ___ senza sosta.",
                "palavra_oculta": "inseguono",
                "traducao": "O dia e a noite se perseguem sem parar.",
                "dica": "corrono l'uno dietro l'altro"
            },
            {
                "id": 3,
                "texto_completo": "Come noi due, diversi ma inseparabili.",
                "texto_lacuna": "Come noi due, diversi ma ___.",
                "palavra_oculta": "inseparabili",
                "traducao": "Como nós dois, diferentes mas inseparáveis.",
                "dica": "che non si possono separare"
            },
            {
                "id": 4,
                "texto_completo": "La luna aspetta il sole ogni mattino.",
                "texto_lacuna": "La luna ___ il sole ogni mattino.",
                "palavra_oculta": "aspetta",
                "traducao": "A lua espera o sol toda manhã.",
                "dica": "terza persona di 'aspettare'"
            },
            {
                "id": 5,
                "texto_completo": "E il sole rimpiange la luna ogni sera.",
                "texto_lacuna": "E il sole ___ la luna ogni sera.",
                "palavra_oculta": "rimpiange",
                "traducao": "E o sol sente saudade da lua toda tarde.",
                "dica": "sente la mancanza, desidera il passato"
            }
        ]
    },
    "can_198": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Profumo di donna, dolce e misterioso.",
                "texto_lacuna": "___ di donna, dolce e misterioso.",
                "palavra_oculta": "Profumo",
                "traducao": "Perfume de mulher, doce e misterioso.",
                "dica": "fragranza, aroma"
            },
            {
                "id": 2,
                "texto_completo": "Un profumo che rimane nell'aria dopo la sua partenza.",
                "texto_lacuna": "Un profumo che ___ nell'aria dopo la sua partenza.",
                "palavra_oculta": "rimane",
                "traducao": "Um perfume que fica no ar após sua partida.",
                "dica": "resta, non scompare"
            },
            {
                "id": 3,
                "texto_completo": "Ogni fragranza racconta una storia d'amore.",
                "texto_lacuna": "Ogni ___ racconta una storia d'amore.",
                "palavra_oculta": "fragranza",
                "traducao": "Cada fragrância conta uma história de amor.",
                "dica": "sinonimo di 'profumo'"
            },
            {
                "id": 4,
                "texto_completo": "Il suo profumo mi fa impazzire, mi conquista.",
                "texto_lacuna": "Il suo profumo mi fa ___, mi conquista.",
                "palavra_oculta": "impazzire",
                "traducao": "Seu perfume me enlouquece, me conquista.",
                "dica": "diventare matto"
            },
            {
                "id": 5,
                "texto_completo": "Chiudo gli occhi e la rivedo attraverso il profumo.",
                "texto_lacuna": "Chiudo gli occhi e la ___ attraverso il profumo.",
                "palavra_oculta": "rivedo",
                "traducao": "Fecho os olhos e a revejo através do perfume.",
                "dica": "vedo di nuovo"
            }
        ]
    },
    "can_199": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Come prima, più di prima, ti amerò.",
                "texto_lacuna": "Come ___, più di prima, ti amerò.",
                "palavra_oculta": "prima",
                "traducao": "Como antes, mais do que antes, te amarei.",
                "dica": "nel passato, in precedenza"
            },
            {
                "id": 2,
                "texto_completo": "Per la vita la mia vita darò a te.",
                "texto_lacuna": "Per la vita la mia vita ___ a te.",
                "palavra_oculta": "darò",
                "traducao": "Para a vida darei minha vida a você.",
                "dica": "futuro di 'dare'"
            },
            {
                "id": 3,
                "texto_completo": "Ritorno a te, mio grande amore perduto.",
                "texto_lacuna": "___ a te, mio grande amore perduto.",
                "palavra_oculta": "Ritorno",
                "traducao": "Volto a você, meu grande amor perdido.",
                "dica": "prima persona di 'ritornare'"
            },
            {
                "id": 4,
                "texto_completo": "Gli anni non hanno cambiato il mio sentimento.",
                "texto_lacuna": "Gli anni non hanno ___ il mio sentimento.",
                "palavra_oculta": "cambiato",
                "traducao": "Os anos não mudaram meu sentimento.",
                "dica": "participio di 'cambiare'"
            },
            {
                "id": 5,
                "texto_completo": "Ti amo come allora, anzi di più.",
                "texto_lacuna": "Ti amo come allora, anzi di ___.",
                "palavra_oculta": "più",
                "traducao": "Te amo como então, aliás mais.",
                "dica": "in maggiore quantità, maggiormente"
            }
        ]
    },
    "can_200": {
        "estrofes": [
            {
                "id": 1,
                "texto_completo": "Lavandaie del Vomero, cantate insieme a noi.",
                "texto_lacuna": "___ del Vomero, cantate insieme a noi.",
                "palavra_oculta": "Lavandaie",
                "traducao": "Lavadeiras do Vomero, cantai conosco.",
                "dica": "donne che lavano i panni"
            },
            {
                "id": 2,
                "texto_completo": "Le mani nell'acqua fresca del mattino.",
                "texto_lacuna": "Le mani nell'___ fresca del mattino.",
                "palavra_oculta": "acqua",
                "traducao": "As mãos na água fresca da manhã.",
                "dica": "liquido trasparente, H2O"
            },
            {
                "id": 3,
                "texto_completo": "Il canto sale dal vicolo verso il cielo.",
                "texto_lacuna": "Il canto ___ dal vicolo verso il cielo.",
                "palavra_oculta": "sale",
                "traducao": "O canto sobe do beco em direção ao céu.",
                "dica": "si alza, va in alto"
            },
            {
                "id": 4,
                "texto_completo": "Napoli antica vive nei suoi canti popolari.",
                "texto_lacuna": "Napoli ___ vive nei suoi canti popolari.",
                "palavra_oculta": "antica",
                "traducao": "A antiga Nápoles vive em seus cantos populares.",
                "dica": "di lungo tempo fa, storica"
            },
            {
                "id": 5,
                "texto_completo": "La tradizione si tramanda di voce in voce.",
                "texto_lacuna": "La tradizione si ___ di voce in voce.",
                "palavra_oculta": "tramanda",
                "traducao": "A tradição é transmitida de voz em voz.",
                "dica": "si passa di generazione in generazione"
            },
            {
                "id": 6,
                "texto_completo": "Il popolo canta e la sua storia non muore mai.",
                "texto_lacuna": "Il ___ canta e la sua storia non muore mai.",
                "palavra_oculta": "popolo",
                "traducao": "O povo canta e sua história nunca morre.",
                "dica": "insieme di persone di una nazione"
            }
        ]
    }
}

def main():
    json_path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\canzoni.json"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for song in data["canzoni"]:
        song_id = song["id"]
        if song_id in EXPANSIONS:
            song["estrofes"] = EXPANSIONS[song_id]["estrofes"]
            # Update xp_recompensa based on number of estrofes
            num_estrofes = len(EXPANSIONS[song_id]["estrofes"])
            song["xp_recompensa"] = num_estrofes * 10
            updated += 1

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated} songs successfully.")

if __name__ == "__main__":
    main()
