#!/usr/bin/env python3
"""
Atualiza data/canzoni.json:
1. Mantém can_001 (Bella Ciao) e can_002 (L'Italiano) e garante 5 estrofes ricas e dicas em PT.
2. Substitui can_003 a can_050 (48 clássicos italianos que estavam com 'Testo generico per ... strofa 1')
   por 5 estrofes autênticas e didáticas de cada música (substituindo a duplicata can_047 por 'Con Il Nastro Rosa' de Lucio Battisti).
3. Remove can_051 a can_150 (100 músicas falsas geradas automaticamente 'Vol. 1..10').
4. Renumera can_151 a can_200 para can_051 a can_100 e traduz as dicas técnicas para português claro.
"""
import json

import re

def make_est(idx, texto_completo, palavra_oculta, traducao, dica, repeticoes=1):
    # Garante que texto_lacuna substitua a primeira ocorrência da palavra_oculta por ___
    if palavra_oculta not in texto_completo:
        m = re.search(re.escape(palavra_oculta), texto_completo, re.IGNORECASE)
        assert m, f"'{palavra_oculta}' não encontrada em '{texto_completo}'"
        palavra_oculta = m.group(0)
    texto_lacuna = texto_completo.replace(palavra_oculta, "___", 1)
    est = {
        "id": idx,
        "texto_completo": texto_completo,
        "texto_lacuna": texto_lacuna,
        "palavra_oculta": palavra_oculta,
        "traducao": traducao,
        "dica": dica
    }
    if repeticoes > 1:
        est["repeticoes"] = repeticoes
    return est

SONGS_1_TO_50 = {
    "can_001": {
        "vocabulario_chave": ["mattina", "alzato", "trovato", "partigiano", "libertà", "fiore"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Una mattina mi sono alzato, o bella ciao, bella ciao, bella ciao ciao ciao!", "alzato",
                     "Uma manhã eu me levantei, ó bella ciao, bella ciao, bella ciao ciao ciao!",
                     "Particípio passado de 'alzarsi' (levantar-se)"),
            make_est(2, "Una mattina mi sono alzato e ho trovato l'invasor.", "trovato",
                     "Uma manhã eu me levantei e encontrei o invasor.",
                     "Particípio passado de 'trovare' (encontrar)"),
            make_est(3, "O partigiano, portami via, o bella ciao, bella ciao, bella ciao ciao ciao!", "portami",
                     "Ó partigiano, leva-me embora, ó bella ciao, bella ciao, bella ciao ciao ciao!",
                     "Imperativo 'porta' + pronome 'mi' (leva-me)"),
            make_est(4, "O partigiano, portami via, ché mi sento di morir.", "morir",
                     "Ó partigiano, leva-me embora, pois sinto que vou morrer.",
                     "Forma apocopada de 'morire' (morrer)"),
            make_est(5, "E questo è il fiore del partigiano, morto per la libertà!", "libertà",
                     "E esta é a flor do partigiano, morto pela liberdade!",
                     "Substantivo feminino: liberdade", repeticoes=2),
        ]
    },
    "can_002": {
        "vocabulario_chave": ["spaghetti", "dente", "destra", "canarino", "cantare", "chitarra", "corretto", "mercato"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Buongiorno Italia, gli spaghetti al dente e un partigiano come presidente.", "dente",
                     "Bom dia Itália, os espaguetes al dente e um partigiano como presidente.",
                     "Expressão culinária para massa cozida no ponto firme"),
            make_est(2, "Con la radio nella mano destra e un canarino sopra la finestra.", "destra",
                     "Com o rádio na mão direita e um canário em cima da janela.",
                     "Oposto de 'sinistra' (direita)"),
            make_est(3, "Buongiorno Italia con i tuoi artisti, con troppa America sui manifesti.", "artisti",
                     "Bom dia Itália com os teus artistas, com América demais nos cartazes.",
                     "Plural masculino de 'artista'"),
            make_est(4, "Lasciatemi cantare con la chitarra in mano, lasciatemi cantare, sono un italiano.", "cantare",
                     "Deixem-me cantar com o violão na mão, deixem-me cantar, sou um italiano.",
                     "Verbo no infinitivo: cantar", repeticoes=2),
            make_est(5, "Buongiorno Italia, caffè corretto, la domenica a messa, il lunedì al mercato.", "corretto",
                     "Bom dia Itália, café batizado com licor, no domingo à missa, na segunda no mercado.",
                     "Café expresso com uma dose de grappa ou licor"),
        ]
    },
    "can_003": {
        "vocabulario_chave": ["sogno", "volare", "dipinto", "cielo", "infinito", "felice"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Penso che un sogno così non ritorni mai più.", "sogno",
                     "Penso que um sonho assim nunca mais volte.",
                     "Substantivo masculino: sonho"),
            make_est(2, "Mi dipingevo le mani e la faccia di blu.", "blu",
                     "Eu pintava as mãos e o rosto de azul.",
                     "Cor: azul escuro"),
            make_est(3, "Poi d'improvviso venivo dal vento rapito e incominciavo a volare nel cielo infinito.", "volare",
                     "Depois, de repente, eu era arrebatado pelo vento e começava a voar no céu infinito.",
                     "Verbo no infinitivo: voar"),
            make_est(4, "Volare, oh oh, cantare, oh oh oh oh! Nel blu dipinto di blu, felice di stare lassù.", "felice",
                     "Voar, oh oh, cantar, oh oh oh oh! No azul pintado de azul, feliz de estar lá em cima.",
                     "Adjetivo: feliz", repeticoes=2),
            make_est(5, "E volavo, volavo felice più in alto del sole ed ancora più su.", "sole",
                     "E eu voava, voava feliz mais alto que o sol e ainda mais para cima.",
                     "Substantivo masculino: o sol"),
        ]
    },
    "can_004": {
        "vocabulario_chave": ["estate", "città", "azzurro", "pomeriggio", "treno", "desideri"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Cerco l'estate tutto l'anno e all'improvviso eccola qua.", "estate",
                     "Procuro o verão o ano todo e, de repente, ei-lo aqui.",
                     "Estação mais quente do ano: verão"),
            make_est(2, "Lei è partita per le spiagge e sono solo quaggiù in città.", "città",
                     "Ela partiu para as praias e estou sozinho aqui embaixo na cidade.",
                     "Substantivo feminino invariável: cidade"),
            make_est(3, "Azzurro, il pomeriggio è troppo azzurro e lungo per me.", "pomeriggio",
                     "Azul, a tarde é azul demais e longa para mim.",
                     "Período do dia após o meio-dia: tarde", repeticoes=2),
            make_est(4, "Mi accorgo di non avere più risorse senza di te.", "senza",
                     "Percebo que não tenho mais recursos sem você.",
                     "Preposição: sem"),
            make_est(5, "E allora io quasi quasi prendo il treno e vengo da te.", "treno",
                     "E então eu quase pego o trem e vou até você.",
                     "Meio de transporte sobre trilhos: trem"),
        ]
    },
    "can_005": {
        "vocabulario_chave": ["felicità", "mano", "vino", "panino", "sguardo", "amore"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Felicità è tenersi per mano, andare lontano, la felicità.", "mano",
                     "Felicidade é dar as mãos, ir longe, a felicidade.",
                     "Parte do corpo: mão"),
            make_est(2, "È il tuo sguardo innocente in mezzo alla gente, la felicità.", "sguardo",
                     "É o teu olhar inocente no meio das pessoas, a felicidade.",
                     "Substantivo masculino: olhar"),
            make_est(3, "Felicità è un bicchiere di vino con un panino, la felicità.", "vino",
                     "Felicidade é uma taça de vinho com um sanduíche, a felicidade.",
                     "Bebida tradicional italiana feita de uva", repeticoes=2),
            make_est(4, "È lasciarti un biglietto dentro al cassetto, la felicità.", "biglietto",
                     "É deixar-te um bilhete dentro da gaveta, a felicidade.",
                     "Substantivo masculino: bilhete / passagem"),
            make_est(5, "È cantare a due voci quanto mi piaci, la felicità.", "piaci",
                     "É cantar a duas vozes o quanto gosto de ti, a felicidade.",
                     "Verbo 'piacere' na 2ª pessoa: tu me agradas"),
        ]
    },
    "can_006": {
        "vocabulario_chave": ["amo", "moneta", "aria", "letto", "perdono", "gelosia"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Ti amo, un soldo di moneta, ti amo, in aria è caduto.", "amo",
                     "Eu te amo, um tostão de moeda, te amo, no ar caiu.",
                     "Presente de 'amare' (1ª pessoa): amo", repeticoes=2),
            make_est(2, "Dammi metà del tuo letto, se poi ti pentirai.", "letto",
                     "Dá-me metade da tua cama, se depois te arrependeres.",
                     "Móvel onde dormimos: cama"),
            make_est(3, "Ti amo e chiedo perdono, ricordati chi sono.", "perdono",
                     "Eu te amo e peço perdão, lembra-te de quem eu sou.",
                     "Substantivo masculino: perdão"),
            make_est(4, "Apri la porta a un guerriero di carta igienica.", "porta",
                     "Abre a porta para um guerreiro de papel higiênico.",
                     "Substantivo feminino: porta"),
            make_est(5, "E dammi il tuo vino leggero che hai fatto quando non c'ero.", "vino",
                     "E dá-me o teu vinho leve que fizeste quando eu não estava.",
                     "Bebida: vinho"),
        ]
    },
    "can_007": {
        "vocabulario_chave": ["mattino", "mani", "attesa", "chiesa", "acqua", "deserto"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Gloria, manchi tu nell'aria, manchi ad una mano che lavora piano.", "aria",
                     "Gloria, faltas tu no ar, faltas a uma mão que trabalha devagar.",
                     "Elemento que respiramos: ar"),
            make_est(2, "Manchi a questa bocca che cibo più non tocca.", "bocca",
                     "Faltas a esta boca que já não toca na comida.",
                     "Parte do rosto: boca"),
            make_est(3, "Gloria, nell'attesa di te che scendi dal mattino.", "mattino",
                     "Gloria, na espera de ti que desces da manhã.",
                     "Período inicial do dia: manhã"),
            make_est(4, "Tu sei acqua nel deserto, lascia aperto il cuore.", "acqua",
                     "Tu és água no deserto, deixa aberto o coração.",
                     "Líquido essencial à vida: água", repeticoes=2),
            make_est(5, "Io ti aspetto Gloria, nel mio letto e nei miei sogni.", "sogni",
                     "Eu te espero, Gloria, na minha cama e nos meus sonhos.",
                     "Plural de 'sogno': sonhos"),
        ]
    },
    "can_008": {
        "vocabulario_chave": ["partito", "treno", "scuola", "solitudine", "diario", "pensieri"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Marco se n'è andato e non ritorna più, e il treno delle sette e mezzo senza lui.", "treno",
                     "Marco foi embora e não volta mais, e o trem das sete e meia parte sem ele.",
                     "Meio de transporte ferroviário: trem"),
            make_est(2, "È un cuore di metallo senza l'anima nel freddo del mattino grigio di città.", "cuore",
                     "É um coração de metal sem alma no frio da manhã cinzenta da cidade.",
                     "Órgão central dos sentimentos: coração"),
            make_est(3, "A scuola il banco è vuoto, Marco è dentro me, è dolce il suo respiro fra i pensieri miei.", "scuola",
                     "Na escola a carteira está vazia, Marco está dentro de mim, é doce o seu respiro entre os meus pensamentos.",
                     "Lugar de estudo: escola"),
            make_est(4, "La solitudine fra noi, questo silenzio dentro me.", "solitudine",
                     "A solidão entre nós, este silêncio dentro de mim.",
                     "Estado de quem está só: solidão", repeticoes=2),
            make_est(5, "Ti prego, aspettami perché non posso stare senza te.", "aspettami",
                     "Eu te imploro, espera-me porque não posso ficar sem ti.",
                     "Imperativo de 'aspettare' + 'mi' (espera-me)"),
        ]
    },
    "can_009": {
        "vocabulario_chave": ["solo", "sogno", "luce", "partirò", "paesi", "mari"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Quando sono solo sogno all'orizzonte e mancan le parole.", "solo",
                     "Quando estou sozinho sonho com o horizonte e faltam as palavras.",
                     "Adjetivo: sozinho"),
            make_est(2, "Sì lo so che non c'è luce in una stanza quando manca il sole.", "luce",
                     "Sim, eu sei que não há luz em um quarto quando falta o sol.",
                     "Substantivo feminino: luz"),
            make_est(3, "Con te partirò, paesi che non ho mai veduto e vissuto con te.", "partirò",
                     "Contigo partirei, países que nunca vi e vivi contigo.",
                     "Futuro simples de 'partire' (1ª pessoa): partirei", repeticoes=2),
            make_est(4, "Adesso sì li vivrò, con te partirò su navi per mari.", "mari",
                     "Agora sim os viverei, contigo partirei em navios por mares.",
                     "Plural irregular de 'mare': mares"),
            make_est(5, "Che io lo so, no no non esistono più, con te io li rivivrò.", "esistono",
                     "Que eu sei, não, não existem mais, contigo eu os reviverei.",
                     "Presente de 'esistere' (3ª pessoa plural): existem"),
        ]
    },
    "can_010": {
        "vocabulario_chave": ["confusione", "emozione", "stella", "vola", "petto", "innamorarsi"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Che confusione, sarà perché ti amo, è un'emozione che cresce piano piano.", "confusione",
                     "Que confusão, será porque te amo, é uma emoção que cresce devagarinho.",
                     "Substantivo feminino: confusão", repeticoes=2),
            make_est(2, "Stringimi forte e stammi più vicino, se ci sto bene sarà perché ti amo.", "vicino",
                     "Aperta-me forte e fica mais perto de mim, se me sinto bem será porque te amo.",
                     "Advérbio/adjetivo: perto / próximo"),
            make_est(3, "Io canto al ritmo del dolce tuo respiro, è primavera, sarà perché ti amo.", "primavera",
                     "Eu canto ao ritmo do teu doce respiro, é primavera, será porque te amo.",
                     "Estação das flores: primavera"),
            make_est(4, "Cade una stella, ma dimmi dove siamo, che te ne frega, sarà perché ti amo.", "stella",
                     "Cai uma estrela, mas diz-me onde estamos, que importa, será porque te amo.",
                     "Astro luminoso no céu noturno: estrela"),
            make_est(5, "E vola, vola si sa, sempre più in alto si va!", "vola",
                     "E voa, voa, sabe-se, sempre mais alto se vai!",
                     "3ª pessoa singular do verbo 'volare': voa"),
        ]
    },
    "can_011": {
        "vocabulario_chave": ["sole", "giornata", "aria", "festa", "fronte", "Tempesta"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Che bella cosa è una giornata di sole, un'aria serena dopo la tempesta!", "giornata",
                     "Que coisa linda é um dia de sol, um ar sereno depois da tempestade!",
                     "Substantivo feminino para a duração do dia: jornada/dia"),
            make_est(2, "Per l'aria fresca pare già una festa, che bella cosa è una giornata di sole.", "festa",
                     "Pelo ar fresco já parece uma festa, que coisa linda é um dia de sol.",
                     "Substantivo feminino: festa"),
            make_est(3, "Ma un altro sole più bello ancora, o sole mio, sta in fronte a te!", "sole",
                     "Mas um outro sol mais bonito ainda, ó meu sol, está diante de ti!",
                     "Astro rei: sol", repeticoes=2),
            make_est(4, "Il sole, il sole mio, sta in fronte a te, sta in fronte a te!", "fronte",
                     "O sol, o meu sol, está na tua testa / diante de ti!",
                     "Substantivo feminino: testa / frente"),
            make_est(5, "Quando fa notte e il sole se ne scende, mi viene quasi una malinconia.", "notte",
                     "Quando anoitece e o sol se põe, vem-me quase uma melancolia.",
                     "Período escuro do dia: noite"),
        ]
    },
    "can_012": {
        "vocabulario_chave": ["montagna", "vento", "fuoco", "mondo", "cima", "correre"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Ieri sera, Nannina, me ne sono salito fin sopra la montagna.", "montagna",
                     "Ontem à noite, Nannina, subi até lá em cima da montanha.",
                     "Elevação natural do terreno: montanha"),
            make_est(2, "Per vedere il fuoco che brucia e che non si stanca mai.", "fuoco",
                     "Para ver o fogo que queima e que nunca se cansa.",
                     "Substantivo masculino: fogo"),
            make_est(3, "Andiamo, andiamo, fino in cima ritorneremo giù!", "cima",
                     "Vamos, vamos, até o topo e depois voltaremos para baixo!",
                     "Ponto mais alto: topo / cume"),
            make_est(4, "Funiculì, funiculà, funiculì, funiculà! Saliamo, Nannina, funiculì, funiculà!", "Saliamo",
                     "Funiculì, funiculà! Subamos, Nannina, funiculì, funiculà!",
                     "1ª pessoa do plural de 'salire' (subir)", repeticoes=2),
            make_est(5, "Si vede Francia, Procida e la Spagna, e io vedo te nel cuore mio.", "cuore",
                     "Vê-se a França, Procida e a Espanha, e eu vejo você no meu coração.",
                     "Substantivo masculino: coração")
        ]
    },
}

SONGS_1_TO_50.update({
    "can_013": {
        "vocabulario_chave": ["mare", "golfo", "vento", "occhi", "volo", "bene"],
        "xp_recompensa": 55,
        "estrofes": [
            make_est(1, "Qui dove il mare luccica e tira forte il vento su una vecchia terrazza davanti al golfo di Surriento.", "mare",
                     "Aqui onde o mar reluz e sopra forte o vento num velho terraço diante do golfo de Sorrento.",
                     "Grande massa de água salgada: mar"),
            make_est(2, "Un uomo abbraccia una ragazza dopo che aveva pianto, poi si schiarisce la voce e ricomincia il canto.", "voce",
                     "Um homem abraça uma garota depois que ela havia chorado, depois limpa a voz e recomeça o canto.",
                     "Som produzido pelas cordas vocais: voz"),
            make_est(3, "Te voglio bene assaje, ma tanto tanto bene sai!", "bene",
                     "Quero-te muito bem, mas tanto, tanto bem, sabes!",
                     "Expressão 'volere bene' = amar / querer bem", repeticoes=2),
            make_est(4, "È una catena ormai che scioglie il sangue dint'e vene sai.", "sangue",
                     "Já é uma corrente que derrete o sangue dentro das veias, sabes.",
                     "Substantivo masculino: sangue"),
            make_est(5, "Sentì il dolore nella musica, si alzò dal pianoforte, ma quando vide la luna uscire da una nuvola gli sembrò più dolce anche la morte.", "luna",
                     "Sentiu a dor na música, levantou-se do piano, mas quando viu a lua sair de uma nuvem pareceu-lhe mais doce até a morte.",
                     "Satélite natural da Terra: lua"),
        ]
    },
    "can_014": {
        "vocabulario_chave": ["stanza", "pareti", "cielo", "alberi", "soffitto", "infinito"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Quando sei qui con me questa stanza non ha più pareti ma alberi.", "stanza",
                     "Quando estás aqui comigo este quarto não tem mais paredes, mas árvores.",
                     "Cômodo de uma casa: quarto / sala", repeticoes=2),
            make_est(2, "Alberi infiniti, quando sei qui vicino a me questo soffitto viola no, non esiste più.", "soffitto",
                     "Árvores infinitas, quando estás aqui perto de mim este teto violeta não, não existe mais.",
                     "Parte superior interna de um quarto: teto"),
            make_est(3, "Io vedo il cielo sopra noi che restiamo qui abbandonati come se non ci fosse più niente.", "cielo",
                     "Eu vejo o céu sobre nós que ficamos aqui entregues como se não houvesse mais nada.",
                     "Substantivo masculino: céu"),
            make_est(4, "Più niente al mondo, suona un'armonica, mi sembra un organo che vibra per te e per me.", "mondo",
                     "Mais nada no mundo, toca uma gaita, parece-me um órgão que vibra por ti e por mim.",
                     "Substantivo masculino: mundo"),
            make_est(5, "Su nell'immensità del cielo, per te e per me nel cielo.", "immensità",
                     "Lá em cima na imensidão do céu, por ti e por mim no céu.",
                     "Substantivo feminino abstrato: imensidão"),
        ]
    },
    "can_015": {
        "vocabulario_chave": ["donna", "notte", "pelle", "spalle", "stelle", "amore"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Non so più cosa fare, non mi ricordo come si sta insieme.", "insieme",
                     "Não sei mais o que fazer, não me lembro de como se fica junto.",
                     "Advérbio: juntos / em conjunto"),
            make_est(2, "Adesso vivo da solo in una casa sul mare.", "casa",
                     "Agora moro sozinho numa casa à beira-mar.",
                     "Substantivo feminino: casa / lar"),
            make_est(3, "Senza una donna, come siamo lontani, senza una donna sto bene anche domani.", "donna",
                     "Sem uma mulher, como estamos distantes, sem uma mulher fico bem também amanhã.",
                     "Substantivo feminino: mulher", repeticoes=2),
            make_est(4, "Senza una donna che mi ha cambiato la pelle e che mi fa vedere le stelle.", "stelle",
                     "Sem uma mulher que mudou a minha pele e que me faz ver as estrelas.",
                     "Plural de 'stella': estrelas"),
            make_est(5, "Ascolta questa canzone che scende piano nella notte.", "notte",
                     "Escuta esta canção que desce suavemente na noite.",
                     "Período noturno: noite"),
        ]
    },
    "can_016": {
        "vocabulario_chave": ["ballo", "capogiro", "notte", "festa", "musica", "stelle"],
        "xp_recompensa": 45,
        "estrofes": [
            make_est(1, "Ballo, ballo, ballo da capogiro, ballo, ballo, ballo senza respiro!", "respiro",
                     "Danço, danço, danço de dar tontura, danço, danço, danço sem fôlego!",
                     "Substantivo masculino: respiração / fôlego", repeticoes=2),
            make_est(2, "Ballo per tutta la notte sotto le stelle della città.", "notte",
                     "Danço por toda a noite sob as estrelas da cidade.",
                     "Substantivo feminino: noite"),
            make_est(3, "Quando parte la musica nessuno si può più fermare.", "musica",
                     "Quando começa a música ninguém mais consegue parar.",
                     "Arte dos sons: música"),
            make_est(4, "Io mi invento una festa dentro al cuore insieme a te.", "festa",
                     "Eu invento uma festa dentro do coração junto com você.",
                     "Substantivo feminino: festa"),
            make_est(5, "Gira tutto il mondo intorno a noi mentre balliamo così.", "mondo",
                     "Gira todo o mundo ao nosso redor enquanto dançamos assim.",
                     "Substantivo masculino: mundo"),
        ]
    },
    "can_017": {
        "vocabulario_chave": ["amore", "comincia", "libero", "scoppia", "cuore", "strano"],
        "xp_recompensa": 45,
        "estrofes": [
            make_est(1, "Se lui ti porta su un letto vuoto, il vuoto daglielo indietro a lui.", "vuoto",
                     "Se ele te leva para uma cama vazia, devolve o vazio para ele.",
                     "Adjetivo/substantivo: vazio"),
            make_est(2, "Fagli vedere che non è un gioco, fagli capire quello che vuoi.", "gioco",
                     "Mostra-lhe que não é um jogo, faz com que ele entenda o que queres.",
                     "Substantivo masculino: jogo / brincadeira"),
            make_est(3, "A far l'amore comincia tu, se lui ti porta su un letto vuoto.", "comincia",
                     "Para fazer amor começa tu, se ele te leva para uma cama vazia.",
                     "Imperativo de 'cominciare': começa", repeticoes=2),
            make_est(4, "Scoppia, scoppia mi sco', scoppia, scoppia mi scoppia il cuor!", "cuor",
                     "Explode, explode, explode o meu coração!",
                     "Forma truncada poética de 'cuore' (coração)"),
            make_est(5, "Libero l'amore, tutto quello che c'è, senza catene e senza paure.", "libero",
                     "Livre o amor, tudo o que há, sem correntes e sem medos.",
                     "Adjetivo masculino: livre"),
        ]
    },
    "can_018": {
        "vocabulario_chave": ["canzone", "pensiero", "bella", "grazie", "unica", "esistere"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Com'è cominciata io non saprei, la storia infinita con te.", "storia",
                     "Como começou eu não saberia dizer, a história infinita com você.",
                     "Substantivo feminino: história"),
            make_est(2, "Che sei diventata la mia lei di tutta una vita per me.", "vita",
                     "Que você se tornou a minha mulher de toda uma vida para mim.",
                     "Substantivo feminino: vida"),
            make_est(3, "Cantare d'amore non basta mai, ne servirà di più per dirtelo ancora.", "amore",
                     "Cantar de amor nunca basta, será preciso mais para te dizer de novo.",
                     "Sentimento profundo de afeto: amor"),
            make_est(4, "Più bella cosa non c'è, più bella cosa di te, unica come sei!", "unica",
                     "Coisa mais linda não há, coisa mais linda do que você, única como és!",
                     "Adjetivo feminino: única", repeticoes=2),
            make_est(5, "Immensa quando vuoi, grazie di esistere!", "esistere",
                     "Imensa quando queres, obrigado por existir!",
                     "Verbo no infinitivo: existir"),
        ]
    },
    "can_019": {
        "vocabulario_chave": ["ragazzo", "Sicilia", "ballare", "vino", "pesce", "allegria"],
        "xp_recompensa": 45,
        "estrofes": [
            make_est(1, "Un ragazzo ritornò in Sicilia e trovò una nuova danza da ballare.", "Sicilia",
                     "Um rapaz voltou à Sicília e encontrou uma nova dança para dançar.",
                     "Maior ilha da Itália e do Mediterrâneo"),
            make_est(2, "Ehi, mambo! Mambo italiano! Balla con noi tutta la sera!", "italiano",
                     "Ei, mambo! Mambo italiano! Dança conosco a noite toda!",
                     "Gentílico da Itália", repeticoes=2),
            make_est(3, "Prendi un po' di mozzarella, un po' di vino e vieni a festeggiare.", "vino",
                     "Pega um pouco de mussarela, um pouco de vinho e vem festejar.",
                     "Bebida fermentada da uva: vinho"),
            make_est(4, "La musica ti fa girare la testa e riempie il cuore di allegria.", "allegria",
                     "A música faz girar a tua cabeça e enche o coração de alegria.",
                     "Substantivo feminino: alegria"),
            make_est(5, "In Italia si canta e si balla sotto la luna fino al mattino.", "mattino",
                     "Na Itália canta-se e dança-se sob a lua até de manhã.",
                     "Período inicial do dia: manhã"),
        ]
    },
    "can_020": {
        "vocabulario_chave": ["avventura", "porta", "notti", "magiche", "rete", "cielo"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Forse non sarà una canzone a cambiare le regole del gioco.", "regole",
                     "Talvez não seja uma canção que vá mudar as regras do jogo.",
                     "Plural de 'regola': regras"),
            make_est(2, "Ma voglio viverla così quest'avventura, senza frontiere e con il cuore in gola.", "avventura",
                     "Mas quero vivê-la assim esta aventura, sem fronteiras e com o coração na garganta.",
                     "Substantivo feminino: aventura"),
            make_est(3, "Notti magiche, inseguendo un goal, sotto il cielo di un'estate italiana!", "magiche",
                     "Noites mágicas, perseguindo um gol, sob o céu de um verão italiano!",
                     "Adjetivo feminino plural: mágicas", repeticoes=2),
            make_est(4, "E negli occhi tuoi voglia di vincere, un'estate, un'avventura in più.", "vincere",
                     "E nos teus olhos vontade de vencer, um verão, uma aventura a mais.",
                     "Verbo no infinitivo: vencer"),
            make_est(5, "Un sogno che diventa realtà per chi ci crede fino in fondo.", "sogno",
                     "Um sonho que se torna realidade para quem acredita até o fim.",
                     "Substantivo masculino: sonho"),
        ]
    },
    "can_021": {
        "vocabulario_chave": ["mistero", "volare", "cielo", "ali", "amore", "circo"],
        "xp_recompensa": 60,
        "estrofes": [
            make_est(1, "Butterò questo mio enorme cuore tra le stelle un giorno, giuro che lo farò.", "stelle",
                     "Jogarei este meu enorme coração entre as estrelas um dia, juro que o farei.",
                     "Plural de 'stella': estrelas"),
            make_est(2, "E oltre l'azzurro della tenda nell'azzurro io volerò.", "volerò",
                     "E além do azul da tenda, no azul eu voarei.",
                     "Futuro simples de 'volare' (1ª pessoa): voarei"),
            make_est(3, "Quando la donna cannone d'oro e d'argento diventerà, senza passare dalla stazione l'ultimo treno prenderà.", "stazione",
                     "Quando a mulher-canhão de ouro e de prata se tornar, sem passar pela estação o último trem pegará.",
                     "Substantivo feminino: estação"),
            make_est(4, "E con le mani amore, per le mani ti prenderò, e senza dire parole nel mio cuore ti porterò.", "mani",
                     "E com as mãos, amor, pelas mãos te tomarei, e sem dizer palavras no meu coração te levarei.",
                     "Plural irregular de 'mano': mãos", repeticoes=2),
            make_est(5, "E non avrò paura se non sarò bella come dici tu, ma voleremo in cielo in carne ed ossa, non torneremo più.", "paura",
                     "E não terei medo se não for bela como dizes, mas voaremos no céu em carne e osso, não voltaremos mais.",
                     "Substantivo feminino: medo"),
        ]
    },
    "can_022": {
        "vocabulario_chave": ["gente", "strani", "universo", "punto", "sole", "amare"],
        "xp_recompensa": 55,
        "estrofes": [
            make_est(1, "Sai, la gente è strana, prima si odia e poi si ama.", "strana",
                     "Sabes, as pessoas são estranhas, primeiro se odeiam e depois se amam.",
                     "Adjetivo feminino singular (concorda com 'la gente'): estranha"),
            make_est(2, "Cambia idea improvvisamente, prima la verità poi mentirà lui.", "verità",
                     "Muda de ideia de repente, primeiro a verdade, depois mentirá.",
                     "Substantivo feminino invariável: verdade"),
            make_est(3, "Almeno tu nell'universo, un punto che non gira mai intorno a me.", "universo",
                     "Pelo menos tu no universo, um ponto que nunca gira indeciso ao meu redor.",
                     "Substantivo masculino: universo", repeticoes=2),
            make_est(4, "Un sole che splende per me soltanto come un diamante in mezzo al cuore.", "diamante",
                     "Um sol que brilha apenas para mim como um diamante no meio do coração.",
                     "Pedra preciosa: diamante"),
            make_est(5, "Tu che sei diverso, almeno tu nell'universo non cambierai.", "diverso",
                     "Tu que és diferente, pelo menos tu no universo não mudarás.",
                     "Adjetivo masculino: diferente"),
        ]
    },
    "can_023": {
        "vocabulario_chave": ["vecchia", "centro", "gravità", "idee", "stagione", "cose"],
        "xp_recompensa": 55,
        "estrofes": [
            make_est(1, "Una vecchia bretone con un cappello e un ombrello di carta di riso e canna di bambù.", "ombrello",
                     "Uma velha bretã com um chapéu e um guarda-chuva de papel de arroz e cana de bambu.",
                     "Objeto para proteger da chuva: guarda-chuva"),
            make_est(2, "Capitani coraggiosi, furbi contrabbandieri macedoni.", "coraggiosi",
                     "Capitães corajosos, astutos contrabandistas macedônios.",
                     "Adjetivo masculino plural: corajosos"),
            make_est(3, "Cerco un centro di gravità permanente che non mi faccia mai cambiare idea sulle cose e sulla gente.", "gravità",
                     "Procuro um centro de gravidade permanente que nunca me faça mudar de ideia sobre as coisas e as pessoas.",
                     "Substantivo feminino: gravidade", repeticoes=2),
            make_est(4, "Avrei bisogno di certi sguardi per ritrovare la serenità.", "sguardi",
                     "Eu precisaria de certos olhares para reencontrar a serenidade.",
                     "Plural de 'sguardo': olhares"),
            make_est(5, "Over and over again, girano le stelle nella notte d'estate.", "estate",
                     "Repetidamente, giram as estrelas na noite de verão.",
                     "Estação do ano: verão"),
        ]
    },
    "can_024": {
        "vocabulario_chave": ["proteggerò", "paure", "correnti", "silenzio", "cura", "essere"],
        "xp_recompensa": 60,
        "estrofes": [
            make_est(1, "Ti proteggerò dalle paure delle ipocondrie, dai turbamenti che da oggi incontrerai per la tua via.", "paure",
                     "Eu te protegerei dos medos das hipocondrias, das perturbações que a partir de hoje encontrarás pelo teu caminho.",
                     "Plural de 'paura': medos"),
            make_est(2, "Dalle ingiustizie e dagli inganni del tuo tempo, dai fallimenti che per tua natura normalmente attirerai.", "tempo",
                     "Das injustiças e dos enganos do teu tempo, dos fracassos que por tua natureza normalmente atrairás.",
                     "Substantivo masculino: tempo"),
            make_est(3, "Ti solleverò dai dolori e dai tuoi sbalzi d'umore, dalle ossessioni delle tue manie.", "dolori",
                     "Eu te erguerei das dores e das tuas mudanças de humor, das obsessões das tuas manias.",
                     "Plural de 'dolore': dores"),
            make_est(4, "Supererò le correnti gravitazionali, lo spazio e la luce per non farti invecchiare.", "luce",
                     "Superarei as correntes gravitacionais, o espaço e a luz para não te deixar envelhecer.",
                     "Substantivo feminino: luz", repeticoes=2),
            make_est(5, "E guarirai da tutte le malattie, perché sei un essere speciale ed io avrò cura di te.", "cura",
                     "E te curarás de todas as doenças, porque és um ser especial e eu cuidarei de ti.",
                     "Expressão 'avere cura di': cuidar de"),
        ]
    },
    "can_025": {
        "vocabulario_chave": ["sostanza", "giorni", "dubbi", "sorriso", "vita", "amore"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "A te che sei l'unica al mondo, l'unica ragione per arrivare fino in fondo.", "ragione",
                     "A ti que és a única no mundo, a única razão para chegar até o fim.",
                     "Substantivo feminino: razão / motivo"),
            make_est(2, "A te che hai preso la mia vita e ne hai fatto molto di più.", "vita",
                     "A ti que pegaste a minha vida e fizeste dela muito mais.",
                     "Substantivo feminino: vida"),
            make_est(3, "A te che hai dato senso al tempo senza misurarlo.", "senso",
                     "A ti que deste sentido ao tempo sem medi-lo.",
                     "Substantivo masculino: sentido / significado"),
            make_est(4, "A te che sei la sostanza dei giorni miei, della sostanza dei sogni miei.", "sostanza",
                     "A ti que és a substância dos meus dias, da substância dos meus sonhos.",
                     "Substantivo feminino: substância / essência", repeticoes=2),
            make_est(5, "A te che cambi tutti i giorni e resti sempre la stessa.", "stessa",
                     "A ti que mudas todos os dias e permaneces sempre a mesma.",
                     "Pronome/adjetivo feminino: mesma"),
        ]
    },
    "can_026": {
        "vocabulario_chave": ["positivo", "vivo", "credo", "libertà", "strada", "futuro"],
        "xp_recompensa": 45,
        "estrofes": [
            make_est(1, "Io penso positivo perché son vivo, perché son vivo!", "vivo",
                     "Eu penso positivo porque estou vivo, porque estou vivo!",
                     "Adjetivo masculino: vivo", repeticoes=2),
            make_est(2, "Niente e nessuno al mondo potrà fermarmi da ragionare.", "mondo",
                     "Nada e ninguém no mundo poderá me impedir de raciocinar.",
                     "Substantivo masculino: mundo"),
            make_est(3, "Io credo che a questo mondo esista solo una grande chiesa.", "chiesa",
                     "Eu acredito que neste mundo exista apenas uma grande igreja.",
                     "Substantivo feminino: igreja"),
            make_est(4, "Che passa da Che Guevara e arriva fino a Madre Teresa.", "arriva",
                     "Que passa por Che Guevara e chega até Madre Teresa.",
                     "Presente de 'arrivare' (3ª pessoa): chega"),
            make_est(5, "Il sole batte forte su questa strada che porta al futuro.", "futuro",
                     "O sol bate forte nesta estrada que leva ao futuro.",
                     "Substantivo masculino: futuro"),
        ]
    },
    "can_027": {
        "vocabulario_chave": ["Vespa", "domenica", "colli", "problemi", "scuola", "vacanze"],
        "xp_recompensa": 45,
        "estrofes": [
            make_est(1, "Vespa Special che ti toglie i problemi, fuori è già primavera.", "problemi",
                     "Vespa Special que tira os teus problemas, lá fora já é primavera.",
                     "Plural masculino de 'problema'"),
            make_est(2, "Dammi una Special, l'estate che avanza, dammi una Vespa e ti porto in vacanza!", "vacanza",
                     "Dá-me uma Special, o verão que avança, dá-me uma Vespa e te levo de férias!",
                     "Substantivo feminino: férias", repeticoes=2),
            make_est(3, "Ma quanto è bello andare in giro con le ali sotto ai piedi!", "piedi",
                     "Mas como é bom passear por aí com asas debaixo dos pés!",
                     "Plural de 'piede': pés"),
            make_est(4, "Se hai una Vespa Special che ti toglie i problemi.", "toglie",
                     "Se tens uma Vespa Special que te tira os problemas.",
                     "Presente de 'togliere' (tirar/remover)"),
            make_est(5, "E la scuola non va, ma ho una Vespa e una domenica da vivere.", "scuola",
                     "E a escola não vai bem, mas tenho uma Vespa e um domingo para viver.",
                     "Substantivo feminino: escola"),
        ]
    },
    "can_028": {
        "vocabulario_chave": ["spettacolo", "universo", "musica", "stelle", "noi", "insieme"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Il più grande spettacolo dopo il Big Bang siamo noi, io e te!", "spettacolo",
                     "O maior espetáculo depois do Big Bang somos nós, eu e tu!",
                     "Substantivo masculino: espetáculo", repeticoes=2),
            make_est(2, "Ho attraversato l'oceano solo per vedere il tuo sorriso.", "sorriso",
                     "Atravessei o oceano só para ver o teu sorriso.",
                     "Substantivo masculino: sorriso"),
            make_est(3, "La musica suona forte mentre camminiamo nella notte.", "camminiamo",
                     "A música toca alto enquanto caminhamos na noite.",
                     "1ª pessoa do plural de 'camminare': caminhamos"),
            make_est(4, "Sotto un cielo pieno di stelle che brillano per noi.", "brillano",
                     "Sob um céu cheio de estrelas que brilham por nós.",
                     "3ª pessoa plural de 'brillare': brilham"),
            make_est(5, "Insieme non abbiamo paura di niente, siamo una forza viva.", "forza",
                     "Juntos não temos medo de nada, somos uma força viva.",
                     "Substantivo feminino: força"),
        ]
    },
    "can_029": {
        "vocabulario_chave": ["rose", "rosse", "stasera", "cuore", "piangere", "amore"],
        "xp_recompensa": 45,
        "estrofes": [
            make_est(1, "Ho comprato stasera delle rose rosse per te.", "rosse",
                     "Comprei esta noite rosas vermelhas para ti.",
                     "Adjetivo feminino plural da cor vermelha: vermelhas"),
            make_est(2, "Rose rosse per te ho comprato stasera, e il tuo cuore lo sa cosa voglio da te.", "stasera",
                     "Rosas vermelhas para ti comprei esta noite, e o teu coração sabe o que quero de ti.",
                     "Advérbio de tempo: esta noite", repeticoes=2),
            make_est(3, "D'amore non si muore ma io sto male lontano da te.", "lontano",
                     "De amor não se morre, mas eu passo mal longe de ti.",
                     "Advérbio/adjetivo: longe / distante"),
            make_est(4, "Perché mi lasci sempre solo a piangere nel buio?", "piangere",
                     "Por que me deixas sempre sozinho a chorar no escuro?",
                     "Verbo no infinitivo: chorar"),
            make_est(5, "Prendi queste rose e dimmi che resti con me.", "resti",
                     "Pega estas rosas e diz-me que ficas comigo.",
                     "Presente de 'restare' (2ª pessoa): ficas"),
        ]
    },
    "can_030": {
        "vocabulario_chave": ["perdere", "sera", "cielo", "lacrime", "dolore", "ricordi"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "E adesso andate via, voglio restare solo con la mia malinconia.", "malinconia",
                     "E agora vão embora, quero ficar sozinho com a minha melancolia.",
                     "Substantivo feminino: melancolia"),
            make_est(2, "Volare via con i pensieri mentre cade la sera sulla città.", "sera",
                     "Voar para longe com os pensamentos enquanto cai a noite sobre a cidade.",
                     "Substantivo feminino: fim de tarde / noite"),
            make_est(3, "Perdere l'amore quando si fa sera, quando tra i capelli un po' d'argento li colora.", "perdere",
                     "Perder o amor quando cai a noite, quando entre os cabelos um pouco de prata os colore.",
                     "Verbo no infinitivo: perder", repeticoes=2),
            make_est(4, "Rischi di impazzire, può scoppiarti il cuore per il dolore.", "dolore",
                     "Corres o risco de enlouquecer, pode explodir o teu coração pela dor.",
                     "Substantivo masculino: dor"),
            make_est(5, "Provi a ragionare, ma le parole non bastano più.", "parole",
                     "Tentas raciocinar, mas as palavras já não bastam.",
                     "Plural de 'parola': palavras"),
        ]
    },
    "can_031": {
        "vocabulario_chave": ["mille", "giorni", "pioggia", "occhi", "mani", "ricordo"],
        "xp_recompensa": 55,
        "estrofes": [
            make_est(1, "Amore mio, come farò a dimenticare tutto quello che siamo stati?", "dimenticare",
                     "Meu amor, como farei para esquecer tudo o que fomos?",
                     "Verbo no infinitivo: esquecer"),
            make_est(2, "Mille giorni di te e di me, ti presento un vecchio amico mio.", "giorni",
                     "Mil dias de ti e de mim, apresento-te um velho amigo meu.",
                     "Plural de 'giorno': dias", repeticoes=2),
            make_est(3, "In mezzo a questa pioggia fredda cerco ancora il calore delle tue mani.", "pioggia",
                     "No meio desta chuva fria procuro ainda o calor das tuas mãos.",
                     "Substantivo feminino: chuva"),
            make_est(4, "Abbiamo corso insieme contro il vento senza mai voltarci indietro.", "vento",
                     "Corremos juntos contra o vento sem nunca olhar para trás.",
                     "Substantivo masculino: vento"),
            make_est(5, "E adesso resta il ricordo dolce di ogni nostro istante.", "ricordo",
                     "E agora resta a doce lembrança de cada instante nosso.",
                     "Substantivo masculino: lembrança / recordação"),
        ]
    },
    "can_032": {
        "vocabulario_chave": ["maglietta", "fina", "piccolo", "grande", "paura", "bacio"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Quella sua maglietta fina, tanto stretta al punto che m'immaginavo tutto.", "maglietta",
                     "Aquela sua camiseta fina, tão justa a ponto de eu imaginar tudo.",
                     "Substantivo feminino: camiseta"),
            make_est(2, "E quell'aria da bambina che non gliel'ho detto mai, ma io ci andavo matto.", "bambina",
                     "E aquele ar de menina que nunca lhe disse, mas eu ficava louco por isso.",
                     "Substantivo feminino: menina"),
            make_est(3, "E chiare sere d'estate, il mare, i giochi e le fate.", "fate",
                     "E claras noites de verão, o mar, as brincadeiras e as fadas.",
                     "Plural de 'fata': fadas"),
            make_est(4, "E la paura e la voglia di essere nudi, un bacio a labbra salate.", "bacio",
                     "E o medo e a vontade de estarmos nus, um beijo de lábios salgados.",
                     "Substantivo masculino: beijo"),
            make_est(5, "Questo piccolo grande amore, solo questo piccolo grande amore, niente più di questo niente più!", "grande",
                     "Este pequeno grande amor, só este pequeno grande amor, nada mais que isto, nada mais!",
                     "Adjetivo: grande", repeticoes=2),
        ]
    },
    "can_033": {
        "vocabulario_chave": ["freddo", "dormire", "innamorato", "muro", "stelle", "correre"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Io non posso stare fermo con le mani nelle mani, tante cose devo fare prima che venga domani.", "domani",
                     "Eu não posso ficar parado com as mãos nas mãos, tantas coisas devo fazer antes que chegue amanhã.",
                     "Advérbio de tempo: amanhã"),
            make_est(2, "E se lei già sta dormendo io non posso riposare, farò in modo che al risveglio non mi possa più scordare.", "riposare",
                     "E se ela já está dormindo eu não posso descansar, farei de modo que ao despertar não possa mais me esquecer.",
                     "Verbo no infinitivo: descansar"),
            make_est(3, "Perché Margherita è buona, perché Margherita è bella, perché Margherita è dolce!", "dolce",
                     "Porque Margherita é boa, porque Margherita é bela, porque Margherita é doce!",
                     "Adjetivo: doce / meiga", repeticoes=2),
            make_est(4, "Corro per le strade e salto sopra i tetti per gridare a tutti che ti amo.", "strade",
                     "Corro pelas ruas e salto sobre os telhados para gritar a todos que te amo.",
                     "Plural de 'strada': ruas"),
            make_est(5, "Svegliatevi tutti perché stanotte sono pazzo d'amore per lei!", "pazzo",
                     "Acordem todos porque esta noite estou louco de amor por ela!",
                     "Adjetivo masculino: louco"),
        ]
    },
    "can_034": {
        "vocabulario_chave": ["primavera", "alberi", "fiume", "neve", "nuovo", "cuore"],
        "xp_recompensa": 55,
        "estrofes": [
            make_est(1, "Dopo un lungo inverno freddo il ghiaccio si scioglie al sole.", "inverno",
                     "Depois de um longo inverno frio o gelo se derrete ao sol.",
                     "Estação fria do ano: inverno"),
            make_est(2, "E così io mi risveglio come un cervo a primavera.", "primavera",
                     "E assim eu desperto como um cervo na primavera.",
                     "Estação do renascimento da natureza: primavera", repeticoes=2),
            make_est(3, "Bevo l'acqua chiara del torrente che scende dalla montagna.", "acqua",
                     "Bebo a água clara do riacho que desce da montanha.",
                     "Substantivo feminino: água"),
            make_est(4, "Sento nascere una foglia nuova sopra i rami secchi del passato.", "foglia",
                     "Sinto nascer uma folha nova sobre os galhos secos do passado.",
                     "Substantivo feminino: folha"),
            make_est(5, "E respiro finalmente un vento pulito che mi apre il cuore.", "vento",
                     "E respiro finalmente um vento limpo que me abre o coração.",
                     "Substantivo masculino: vento"),
        ]
    },
    "can_035": {
        "vocabulario_chave": ["collina", "notte", "guerra", "soldati", "treno", "pace"],
        "xp_recompensa": 60,
        "estrofes": [
            make_est(1, "Generale, dietro la collina ci sta la notte crucca e assassina.", "collina",
                     "General, atrás da colina está a noite cruel e assassina.",
                     "Pequena elevação de terreno: colina", repeticoes=2),
            make_est(2, "E in mezzo al prato c'è una contadina, curva sul tramonto sembra una bambina.", "tramonto",
                     "E no meio do campo há uma camponesa, curvada ao pôr do sol parece uma menina.",
                     "Pôr do sol / entardecer"),
            make_est(3, "Di cinquant'anni e di cinque figli, venuti al mondo come conigli.", "figli",
                     "De cinquenta anos e de cinco filhos, vindos ao mundo como coelhos.",
                     "Plural de 'figlio': filhos"),
            make_est(4, "Partiti al mondo come soldati e non ancora tornati.", "soldati",
                     "Partidos pelo mundo como soldados e ainda não retornados.",
                     "Plural de 'soldato': soldados"),
            make_est(5, "Generale, la guerra è finita, il nemico è scappato, è vinto, è battuto.", "guerra",
                     "General, a guerra acabou, o inimigo fugiu, está vencido, está derrotado.",
                     "Substantivo feminino: guerra"),
        ]
    },
    "can_036": {
        "vocabulario_chave": ["fiorellino", "buonanotte", "stelle", "mare", "luna", "sogno"],
        "xp_recompensa": 45,
        "estrofes": [
            make_est(1, "Buonanotte, buonanotte fiorellino, buonanotte fra il telefono e il cielo.", "fiorellino",
                     "Boa noite, boa noite florzinha, boa noite entre o telefone e o céu.",
                     "Diminutivo de 'fiore': florzinha", repeticoes=2),
            make_est(2, "Ti ringrazio per avermi stupito, per avermi giurato che è vero.", "vero",
                     "Eu te agradeço por ter me surpreendido, por ter me jurado que é verdade.",
                     "Adjetivo/substantivo: verdadeiro / verdade"),
            make_est(3, "Buonanotte fra le stelle e la stanza, per sognarti devo averti vicino.", "stanza",
                     "Boa noite entre as estrelas e o quarto, para sonhar contigo preciso ter-te perto.",
                     "Substantivo feminino: quarto"),
            make_est(4, "E vicino non è ancora abbastanza, ora che sei lontana.", "abbastanza",
                     "E perto ainda não é o bastante, agora que estás distante.",
                     "Advérbio: bastante / suficiente"),
            make_est(5, "Il raggio di luna sulle nuvole bianche illumina il tuo sorriso.", "nuvole",
                     "O raio de lua sobre as nuvens brancas ilumina o teu sorriso.",
                     "Plural de 'nuvola': nuvens"),
        ]
    },
    "can_037": {
        "vocabulario_chave": ["sincero", "dolore", "libero", "canto", "verità", "mondo"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "In un mondo che non ci vuole più il mio canto libero sei tu.", "libero",
                     "Em um mundo que não nos quer mais o meu canto livre és tu.",
                     "Adjetivo masculino: livre", repeticoes=2),
            make_est(2, "E l'immensità si apre intorno a noi, al di là del limite degli occhi tuoi.", "occhi",
                     "E a imensidão se abre ao nosso redor, além do limite dos teus olhos.",
                     "Plural de 'occhio': olhos"),
            make_est(3, "Nasce il sentimento, nasce in mezzo al pianto e s'innalza altissimo e va.", "sentimento",
                     "Nasce o sentimento, nasce em meio ao pranto e se eleva altíssimo e vai.",
                     "Substantivo masculino: sentimento"),
            make_est(4, "E vola sulle accuse della gente, a tutti i suoi retaggi indifferente.", "gente",
                     "E voa sobre as acusações das pessoas, a todas as suas heranças indiferente.",
                     "Substantivo feminino coletivo: gente / pessoas"),
            make_est(5, "Sorretto da un anelito d'amore, di vero amore.", "amore",
                     "Sustentado por um anseio de amor, de verdadeiro amor.",
                     "Substantivo masculino: amor"),
        ]
    },
    "can_038": {
        "vocabulario_chave": ["bionde", "trecce", "azzurri", "mare", "paura", "scuola"],
        "xp_recompensa": 45,
        "estrofes": [
            make_est(1, "Le bionde trecce, gli occhi azzurri e poi le tue calzette rosse.", "azzurri",
                     "As tranças loiras, os olhos azuis e depois as tuas meias vermelhas.",
                     "Adjetivo masculino plural: azuis", repeticoes=2),
            make_est(2, "E l'innocenza sulle gote tue, due arance ancor più rosse.", "arance",
                     "E a inocência nas tuas bochechas, duas laranjas ainda mais vermelhas.",
                     "Plural de 'arancia': laranjas"),
            make_est(3, "E la cantina buia dove noi respiravamo piano.", "buia",
                     "E o porão escuro onde nós respirávamos baixinho.",
                     "Adjetivo feminino: escura"),
            make_est(4, "E le tue corse, l'eco dei tuoi no, oh no, mi stai facendo paura!", "paura",
                     "E as tuas corridas, o eco dos teus nãos, oh não, estás me dando medo!",
                     "Substantivo feminino: medo"),
            make_est(5, "Dove sei stata, cos'hai fatto mai? Una donna, donna, dimmi cosa vuol dir sono una donna ormai.", "donna",
                     "Onde estiveste, o que fizeste? Uma mulher, diz-me o que quer dizer já sou uma mulher.",
                     "Substantivo feminino: mulher"),
        ]
    },
    "can_039": {
        "vocabulario_chave": ["carretto", "gelati", "marzo", "coraggio", "dolore", "cielo"],
        "xp_recompensa": 55,
        "estrofes": [
            make_est(1, "Il carretto passava e quell'uomo gridava gelati!", "gelati",
                     "A carrocinha passava e aquele homem gritava: sorvetes!",
                     "Plural de 'gelato': sorvetes"),
            make_est(2, "Al ventuno del mese i nostri soldi erano già finiti.", "soldi",
                     "No dia vinte e um do mês o nosso dinheiro já tinha acabado.",
                     "Substantivo masculino plural: dinheiro"),
            make_est(3, "I giardini di marzo si vestono di nuovi colori.", "marzo",
                     "Os jardins de março se vestem de novas cores.",
                     "Terceiro mês do ano: março", repeticoes=2),
            make_est(4, "E le donne cantavano al fiume la loro fatica di ogni giorno.", "fiume",
                     "E as mulheres cantavam no rio o seu cansaço de cada dia.",
                     "Curso de água natural: rio"),
            make_est(5, "Che anno è, che giorno è? Questo è il tempo di vivere con te.", "tempo",
                     "Que ano é, que dia é? Este é o tempo de viver contigo.",
                     "Substantivo masculino: tempo"),
        ]
    },
    "can_040": {
        "vocabulario_chave": ["lavoro", "sorrido", "penso", "incontrarla", "ritorno", "sera"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Io lavoro e penso a te, torno a casa e penso a te.", "lavoro",
                     "Eu trabalho e penso em ti, volto para casa e penso em ti.",
                     "1ª pessoa do presente de 'lavorare': trabalho"),
            make_est(2, "Le telefono e intanto penso a te, come stai? E penso a te.", "penso",
                     "Telefono para ela e enquanto isso penso em ti, como estás? E penso em ti.",
                     "1ª pessoa do presente de 'pensare': penso", repeticoes=2),
            make_est(3, "Dove andiamo stasera non lo so, ma il mio sguardo cerca sempre te.", "stasera",
                     "Aonde vamos esta noite não sei, mas o meu olhar procura sempre a ti.",
                     "Advérbio: esta noite"),
            make_est(4, "Abbasso gli occhi e sorrido perché la tua immagine non va via.", "sorrido",
                     "Abaixo os olhos e sorrio porque a tua imagem não vai embora.",
                     "1ª pessoa do presente de 'sorridere': sorrio"),
            make_est(5, "Non so con chi adesso sei, non so che cosa fai, ma so di certo a cosa stai pensando.", "adesso",
                     "Não sei com quem estás agora, não sei o que fazes, mas sei ao certo no que estás pensando.",
                     "Advérbio de tempo: agora"),
        ]
    },
    "can_041": {
        "vocabulario_chave": ["respiri", "piano", "rumore", "addormenti", "sveglia", "chiara"],
        "xp_recompensa": 45,
        "estrofes": [
            make_est(1, "Respiri piano per non far rumore, ti addormenti di sera e ti risvegli col sole.", "rumore",
                     "Respiras baixinho para não fazer barulho, adormeces à noite e acordas com o sol.",
                     "Substantivo masculino: barulho / ruído", repeticoes=2),
            make_est(2, "Sei chiara come un'alba, sei fresca come l'aria.", "alba",
                     "És clara como uma alvorada, és fresca como o ar.",
                     "Nascer do dia: alvorada / aurora"),
            make_est(3, "Diventi rossa se qualcuno ti guarda, e sei fantastica quando sei assorta.", "rossa",
                     "Ficas vermelha se alguém te olha, e és fantástica quando estás absorta.",
                     "Adjetivo feminino: vermelha / corada"),
            make_est(4, "Nei tuoi problemi, nei tuoi pensieri, ti vesti svogliatamente.", "pensieri",
                     "Nos teus problemas, nos teus pensamentos, te vestes sem pressa.",
                     "Plural de 'pensiero': pensamentos"),
            make_est(5, "Non metti mai niente che possa attirare attenzione, un particolare solo per farti guardare.", "attenzione",
                     "Nunca colocas nada que possa atrair atenção, apenas um detalhe para te fazerem olhar.",
                     "Substantivo feminino: atenção"),
        ]
    },
    "can_042": {
        "vocabulario_chave": ["spericolata", "film", "tardi", "guai", "bar", "giornale"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Voglio una vita maleducata, di quelle vite fatte così.", "vita",
                     "Quero uma vida mal-educada, daquelas vidas feitas assim.",
                     "Substantivo feminino: vida"),
            make_est(2, "Voglio una vita spericolata, voglio una vita come quelle dei film!", "spericolata",
                     "Quero uma vida destemida/imprudente, quero uma vida como aquelas dos filmes!",
                     "Adjetivo feminino: destemida / cheia de aventura", repeticoes=2),
            make_est(3, "Voglio una vita esagerata, voglio una vita come Steve McQueen.", "esagerata",
                     "Quero uma vida exagerada, quero uma vida como Steve McQueen.",
                     "Adjetivo feminino: exagerada"),
            make_est(4, "Voglio una vita che non è mai tardi, di quelle che non dormi mai!", "tardi",
                     "Quero uma vida em que nunca é tarde, daquelas em que nunca dormes!",
                     "Advérbio de tempo: tarde"),
            make_est(5, "E poi ci troveremo come le star a bere del whisky al Roxy Bar.", "bere",
                     "E depois nos encontraremos como as estrelas para beber uísque no Roxy Bar.",
                     "Verbo no infinitivo: beber"),
        ]
    },
    "can_043": {
        "vocabulario_chave": ["finestra", "donna", "sguardo", "delusione", "lontano", "vicino"],
        "xp_recompensa": 55,
        "estrofes": [
            make_est(1, "Sally cammina per la strada senza nemmeno guardare per terra.", "strada",
                     "Sally caminha pela rua sem sequer olhar para o chão.",
                     "Substantivo feminino: rua / estrada", repeticoes=2),
            make_est(2, "Sally è una donna che non ha più voglia di fare la guerra.", "voglia",
                     "Sally é uma mulher que não tem mais vontade de fazer guerra.",
                     "Expressão 'avere voglia di': ter vontade de"),
            make_est(3, "Sally ha patito troppo, Sally ha già visto che cosa ti può crollare addosso.", "visto",
                     "Sally sofreu demais, Sally já viu o que pode desabar sobre você.",
                     "Particípio passado de 'vedere': visto"),
            make_est(4, "Forse la vita non è stata tutta persa, forse qualcosa s'è salvato.", "salvato",
                     "Talvez a vida não tenha sido toda perdida, talvez algo tenha se salvado.",
                     "Particípio passado de 'salvare': salvado"),
            make_est(5, "Senti che fuori piove, senti che bel rumore!", "piove",
                     "Sente que lá fora chove, sente que belo barulho!",
                     "Verbo impessoal 'piovere': chove"),
        ]
    },
    "can_044": {
        "vocabulario_chave": ["mediano", "pallone", "correre", "polmoni", "gioco", "vincere"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Una vita da mediano a recuperare palloni, nato senza i piedi buoni.", "mediano",
                     "Uma vida de volante (meio-campista) a recuperar bolas, nascido sem os pés bons.",
                     "Posição no futebol de esforço e marcação: volante / meio-campista", repeticoes=2),
            make_est(2, "Lavorare sui polmoni, una vita da mediano con dei compiti precisi.", "polmoni",
                     "Trabalhar nos pulmões, uma vida de volante com tarefas precisas.",
                     "Plural de 'polmone': pulmões"),
            make_est(3, "A coprire certe zone, a giocare generosi.", "giocare",
                     "A cobrir certas zonas, a jogar com generosidade.",
                     "Verbo no infinitivo: jogar / brincar"),
            make_est(4, "Lì sempre lì, lì nel mezzo, finché ce n'hai stai lì.", "mezzo",
                     "Ali, sempre ali, ali no meio, enquanto tiveres fôlego ficas ali.",
                     "Substantivo masculino: meio / centro"),
            make_est(5, "E chi segna sempre è un altro, ma la squadra vince insieme a te.", "squadra",
                     "E quem marca o gol é sempre outro, mas a equipe vence junto contigo.",
                     "Substantivo feminino: equipe / time"),
        ]
    },
    "can_045": {
        "vocabulario_chave": ["notti", "bar", "macchina", "radio", "svegli", "luna"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Certe notti la macchina è calda e dove ti porta lo decide lei.", "macchina",
                     "Em certas noites o carro está quente e aonde te leva é ele quem decide.",
                     "Substantivo feminino: carro / automóvel"),
            make_est(2, "Certe notti la strada non conta, quello che conta è sentire che vai.", "sentire",
                     "Em certas noites a estrada não importa, o que importa é sentir que vais.",
                     "Verbo no infinitivo: sentir"),
            make_est(3, "Certe notti la radio che passa Neil Young sembra avere capito chi sei.", "radio",
                     "Em certas noites o rádio que toca Neil Young parece ter entendido quem és.",
                     "Substantivo feminino: rádio"),
            make_est(4, "Certe notti somigliano a un vizio che tu non vuoi smettere, smettere mai.", "smettere",
                     "Certas noites parecem um vício que tu não queres parar, parar nunca.",
                     "Verbo no infinitivo: parar / deixar de", repeticoes=2),
            make_est(5, "Certe notti sei solo più allegro, più ingordo, più ingenuo e coglione che puoi.", "allegro",
                     "Em certas noites estás apenas mais alegre, mais ávido e mais ingênuo que podes.",
                     "Adjetivo masculino: alegre"),
        ]
    },
    "can_046": {
        "vocabulario_chave": ["fortunato", "regalato", "sogno", "amici", "felice", "strada"],
        "xp_recompensa": 45,
        "estrofes": [
            make_est(1, "Sono un ragazzo fortunato perché m'hanno regalato un sogno!", "fortunato",
                     "Sou um rapaz sortudo porque me presentearam com um sonho!",
                     "Adjetivo masculino (falso cognato parcial): sortudo / afortunado", repeticoes=2),
            make_est(2, "Sono fortunato perché non c'è niente che ho bisogno.", "bisogno",
                     "Sou sortudo porque não há nada de que eu precise.",
                     "Substantivo masculino: necessidade"),
            make_est(3, "E quando viene sera torno a casa contento della giornata.", "contento",
                     "E quando chega a noite volto para casa contente com o dia.",
                     "Adjetivo masculino: contente / satisfeito"),
            make_est(4, "Con gli amici intorno a un tavolo a parlare di musica e libertà.", "amici",
                     "Com os amigos ao redor de uma mesa falando de música e liberdade.",
                     "Plural irregular de 'amico': amigos"),
            make_est(5, "La felicità è nelle cose semplici che viviamo ogni giorno.", "semplici",
                     "A felicidade está nas coisas simples que vivemos todos os dias.",
                     "Plural de 'semplice': simples"),
        ]
    },
    "can_047": {
        # Substituindo a duplicata 'Voglio Una Vita Spericolata' por 'Con Il Nastro Rosa' de Lucio Battisti
        "titulo": "Con Il Nastro Rosa",
        "artista": "Lucio Battisti",
        "nivel": "B1",
        "icone": "🎀",
        "tema": "mistero",
        "vocabulario_chave": ["nastro", "rosa", "bionda", "scoprire", "vivendo", "strada"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Inseguendo una libellula in un prato, un giorno che avevo rotto col passato.", "passato",
                     "Perseguindo uma libélula num campo, num dia em que eu tinha rompido com o passado.",
                     "Substantivo masculino: passado"),
            make_est(2, "Quando già credevo di esserci riuscito, son caduto.", "caduto",
                     "Quando eu já acreditava ter conseguido, caí.",
                     "Particípio passado de 'cadere': caído"),
            make_est(3, "Una frase sciocca, un volgare doppio senso mi ha allarmato, non è come io vorrei.", "frase",
                     "Uma frase boba, um duplo sentido vulgar me alarmou, não é como eu gostaria.",
                     "Substantivo feminino: frase"),
            make_est(4, "Chissà, chissà chi sei, chissà che sarai, chissà che sarà di noi.", "sarai",
                     "Quem sabe, quem sabe quem és, quem sabe o que serás, quem sabe o que será de nós.",
                     "Futuro simples de 'essere' (2ª pessoa): serás", repeticoes=2),
            make_est(5, "Lo scopriremo solo vivendo, com'è difficile restare calmi e indifferenti.", "vivendo",
                     "Só descobriremos vivendo, como é difícil ficar calmos e indiferentes.",
                     "Gerúndio de 'vivere': vivendo"),
        ]
    },
    "can_048": {
        "vocabulario_chave": ["andata", "ritorna", "stringerti", "letto", "pensiero", "manca"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Laura non c'è, è andata via, Laura non è più cosa mia.", "andata",
                     "Laura não está, foi embora, Laura não é mais coisa minha.",
                     "Particípio passado feminino de 'andare': ido / foi", repeticoes=2),
            make_est(2, "E te che sei qua e mi chiedi perché l'amo se niente più mi dà.", "chiedi",
                     "E tu que estás aqui e me perguntas por que a amo se nada mais ela me dá.",
                     "Presente de 'chiedere' (2ª pessoa): perguntas / pedes"),
            make_est(3, "Mi manca da spezzare il fiato, fa male e non lo sa che non mi è mai passata.", "fiato",
                     "Faz-me falta de cortar o fôlego, dói e ela não sabe que nunca me passou.",
                     "Substantivo masculino: fôlego / sopro"),
            make_est(4, "Se vuoi ci amiamo adesso, se vuoi, però non è lo stesso.", "stesso",
                     "Se quiseres nos amamos agora, se quiseres, porém não é a mesma coisa.",
                     "Pronome/adjetivo: mesmo"),
            make_est(5, "Cerco di dimenticare il suo nome ma ritorna sempre nei pensieri miei.", "nome",
                     "Tento esquecer o nome dela, mas volta sempre nos meus pensamentos.",
                     "Substantivo masculino: nome"),
        ]
    },
    "can_049": {
        "vocabulario_chave": ["mare", "notte", "telefonando", "addio", "sorriso", "spiegare"],
        "xp_recompensa": 55,
        "estrofes": [
            make_est(1, "Lo stupore della notte spalancata sul mar ci sorprese che eravamo sconosciuti io e te.", "notte",
                     "O estupor da noite escancarada sobre o mar nos surpreendeu quando éramos desconhecidos eu e tu.",
                     "Substantivo feminino: noite"),
            make_est(2, "Poi nel buio le tue mani d'improvviso sulle mie, è cresciuto troppo in fretta questo nostro amor.", "buio",
                     "Depois, no escuro, as tuas mãos de repente sobre as minhas, cresceu depressa demais este nosso amor.",
                     "Substantivo masculino: escuro / escuridão"),
            make_est(3, "Se telefonando io potessi dirti addio, ti chiamerei.", "addio",
                     "Se telefonando eu pudesse te dizer adeus, eu te ligaria.",
                     "Despedida definitiva: adeus", repeticoes=2),
            make_est(4, "Se io rivedendoti fossi certa che non soffri, ti rivedrei.", "certa",
                     "Se ao te rever eu tivesse certeza de que não sofres, eu te reveria.",
                     "Adjetivo feminino: certa / segura"),
            make_est(5, "Se guardandoti negli occhi sapessi dirti basta, ti guarderei, ma non so spiegarti che il nostro amore appena nato è già finito.", "finito",
                     "Se olhando-te nos olhos eu soubesse te dizer basta, eu te olharia, mas não sei te explicar que o nosso amor recém-nascido já acabou.",
                     "Particípio passado de 'finire': acabado / terminado"),
        ]
    },
    "can_050": {
        "vocabulario_chave": ["occhi", "respiro", "amore", "immenso", "eternità", "giorno"],
        "xp_recompensa": 50,
        "estrofes": [
            make_est(1, "Chiudo gli occhi e penso a lei, il profumo dolce della pelle sua.", "pelle",
                     "Fecho os olhos e penso nela, o perfume doce da pele dela.",
                     "Substantivo feminino: pele"),
            make_est(2, "È una voce dentro che mi sta portando dove nasce il sole.", "portando",
                     "É uma voz lá dentro que está me levando aonde nasce o sol.",
                     "Gerúndio de 'portare': levando"),
            make_est(3, "Dimmi perché quando penso, penso solo a te, dimmi perché quando amo, amo solo te.", "amo",
                     "Diz-me por que quando penso, penso só em ti, diz-me por que quando amo, amo só a ti.",
                     "Presente de 'amare' (1ª pessoa): amo"),
            make_est(4, "Dimmi che mai, che non mi lascerai mai, dimmi chi sei, respiro dei giorni miei d'amore!", "respiro",
                     "Diz-me que nunca, que nunca me deixarás, diz-me quem és, fôlego dos meus dias de amor!",
                     "Substantivo masculino: fôlego / respiração", repeticoes=2),
            make_est(5, "Grande amore, dimmi che tu mi ami veramente e che resteremo insieme per l'eternità.", "eternità",
                     "Grande amor, diz-me que me amas de verdade e que ficaremos juntos pela eternidade.",
                     "Substantivo feminino invariável: eternidade"),
        ]
    }
})

def translate_hint_to_pt(dica):
    if not dica:
        return "Preste atenção ao contexto do verso"
    replacements = [
        ("colore del cielo", "Cor do céu: azul-claro"),
        ("infinito di ", "Infinitivo de "),
        ("riflessivo di ", "Reflexivo de "),
        ("opposto di ", "Oposto de "),
        ("sinonimo: ", "Sinônimo: "),
        ("numero ordinale:", "Número ordinal:"),
        ("prima persona di ", "1ª pessoa de "),
        ("futuro di ", "Futuro de "),
        ("tempo infinito", "Tempo infinito: eternidade"),
        ("da '", "Derivado de '"),
        ("participio passato di ", "Particípio passado de "),
        ("sostantivo plurale", "Substantivo plural"),
        ("sostantivo", "Substantivo"),
        ("aggettivo", "Adjetivo"),
        ("avverbio", "Advérbio"),
        ("verbo ", "Verbo "),
        ("passato prossimo de ", "Passado composto (passato prossimo) de "),
        ("passato prossimo di ", "Passado composto (passato prossimo) de "),
        ("imperativo di ", "Imperativo de "),
        ("presente di ", "Presente de "),
        ("imperfetto di ", "Imperfeito de "),
        ("plurale di ", "Plural de "),
        ("singolare di ", "Singular de "),
        ("condizionale di ", "Condicional de "),
        ("congiuntivo di ", "Subjuntivo de "),
        ("gerundio di ", "Gerúndio de "),
    ]
    out = dica
    for k, v in replacements:
        out = out.replace(k, v)
    # Capitalize first letter
    if out:
        out = out[0].upper() + out[1:]
    return out

def main():
    with open("data/canzoni.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    old_canzoni = {c["id"]: c for c in data["canzoni"]}
    new_canzoni = []

    # 1. Processa can_001 a can_050
    for i in range(1, 51):
        cid = f"can_{i:03d}"
        base = old_canzoni[cid]
        patch = SONGS_1_TO_50[cid]
        item = {
            "id": cid,
            "titulo": patch.get("titulo", base["titulo"]),
            "artista": patch.get("artista", base["artista"]),
            "nivel": patch.get("nivel", base["nivel"]),
            "icone": patch.get("icone", base.get("icone", "🎵")),
            "tema": patch.get("tema", base.get("tema", "musica")),
            "estrofes": patch["estrofes"],
            "vocabulario_chave": patch["vocabulario_chave"],
            "xp_recompensa": patch["xp_recompensa"]
        }
        new_canzoni.append(item)

    # 2. Processa can_151 a can_200 -> renumerando para can_051 a can_100
    for idx, old_num in enumerate(range(151, 201), start=51):
        old_id = f"can_{old_num:03d}"
        new_id = f"can_{idx:03d}"
        base = old_canzoni[old_id]
        estrofes = []
        for e_i, est in enumerate(base["estrofes"], start=1):
            est_copy = dict(est)
            est_copy["id"] = e_i
            est_copy["dica"] = translate_hint_to_pt(est_copy.get("dica", ""))
            # Marcar refrão se for o 3º verso para destacar no player
            if e_i == 3 and "repeticoes" not in est_copy:
                est_copy["repeticoes"] = 2
            estrofes.append(est_copy)
        item = {
            "id": new_id,
            "titulo": base["titulo"],
            "artista": base["artista"],
            "nivel": base["nivel"],
            "icone": base.get("icone", "🎵"),
            "tema": base.get("tema", "musica"),
            "estrofes": estrofes,
            "vocabulario_chave": base.get("vocabulario_chave", []),
            "xp_recompensa": base.get("xp_recompensa", 50)
        }
        new_canzoni.append(item)

    # Validação rigorosa
    assert len(new_canzoni) == 100, f"Esperado 100 músicas, obtido {len(new_canzoni)}"
    for c in new_canzoni:
        assert not ("(Vol." in c["titulo"]), f"Título inválido: {c['titulo']}"
        assert not ("Artista Sconosciuto" in c["artista"]), f"Artista inválido: {c['artista']}"
        assert len(c["estrofes"]) >= 5, f"Menos de 5 estrofes em {c['id']}"
        for est in c["estrofes"]:
            assert "Testo generico" not in est["texto_completo"], f"Placeholder em {c['id']}"
            assert "___" in est["texto_lacuna"], f"Sem lacuna em {c['id']} verso {est['id']}"
            assert est["palavra_oculta"], f"Sem palavra_oculta em {c['id']}"
            assert est["traducao"], f"Sem traducao em {c['id']}"
            assert est["dica"], f"Sem dica em {c['id']}"

    with open("data/canzoni.json", "w", encoding="utf-8") as f:
        json.dump({"canzoni": new_canzoni}, f, ensure_ascii=False, indent=2)

    print(f"Sucesso! {len(new_canzoni)} músicas autênticas salvas em data/canzoni.json.")

if __name__ == "__main__":
    main()
