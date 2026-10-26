#!/usr/bin/env python3
"""
scripts/deck3_preposizioni.py
Gera 100 Flashcards de Preposições, Articulações e Regências Verbais.
"""

from typing import Any


def get_deck_preposizioni() -> list[dict[str, Any]]:
    raw = [
        # 1. Cidades vs Países
        ("a", "em / a (com cidades e ilhas pequenas)", "A1",
         "Domani prendo il treno e vado ___ Roma per lavoro.", "a",
         "Amanhã pego o trem e vou a Roma a trabalho.",
         "Usa-se a preposição simples 'a' com nomes de cidades",
         "/a/", "Regra canônica: 'a' + cidade (a Roma, a Milano, a Napoli)."),

        ("in", "em / no / na (com países, regiões e grandes ilhas)", "A1",
         "La prossima estate faremo un viaggio ___ Italia.", "in",
         "No próximo verão faremos uma viagem na/para a Itália.",
         "Usa-se a preposição 'in' com países, continentes e regiões",
         "/in/", "Regra canônica: 'in' + país (in Italia, in Brasile, in Francia)."),

        ("a", "em (com cidades de chegada/estadia)", "A1",
         "Mio fratello abita ___ Firenze da più di tre anni.", "a",
         "Meu irmão mora em Florença há mais de três anos.",
         "Mora em uma cidade: preposição 'a'",
         "/a/", "Para moradia ou permanência em cidades: 'abitare a Firenze'."),

        ("in", "em (com regiões da Itália)", "A1",
         "La città di Pisa si trova ___ Toscana.", "in",
         "A cidade de Pisa se encontra na Toscana.",
         "Toscana é uma região administrativa da Itália",
         "/in/", "Regiões italianas pedem 'in': in Toscana, in Lombardia, in Sicilia."),

        # 2. Meios de transporte
        ("a", "a (a pé / a cavalo)", "A1",
         "Il centro storico è vicino: possiamo andare ___ piedi.", "a",
         "O centro histórico é perto: podemos ir a pé.",
         "Locomoção pedestre: 'a piedi'",
         "/a ˈpjɛːdi/", "Com transporte corporal ou animal usa-se 'a': a piedi, a cavallo."),

        ("in", "de (com meios de transporte motorizados)", "A1",
         "Per andare da Roma a Milano preferisco viaggiare ___ treno.", "in",
         "Para ir de Roma a Milão prefiro viajar de trem.",
         "Veículos motorizados ou coletivos pedem 'in'",
         "/in ˈtreːno/", "Usa-se 'in' sem artigo: in treno, in aereo, in macchina, in autobus, in metro."),

        ("in", "de avião", "A1",
         "Quanto ci vuole per andare a New York ___ aereo?", "in",
         "Quanto tempo leva para ir a Nova York de avião?",
         "Meio de transporte aéreo",
         "/in aˈɛːreo/", "Meio de transporte em geral pede 'in': in aereo."),

        ("in", "de carro / de automóvel", "A1",
         "È più comodo andare al lago ___ macchina o in pullman?", "in",
         "É mais confortável ir ao lago de carro ou de ônibus turístico?",
         "Veículo próprio",
         "/in ˈmakkina/", "Usa-se 'in macchina' para locomoção em carro próprio."),

        # 3. Estabelecimentos terminados em -ia e cômodos
        ("in", "na / em (estabelecimentos terminados em -ia)", "A1",
         "Devo comprare un'aspirina: vado subito ___ farmacia.", "in",
         "Preciso comprar uma aspirina: vou imediatamente à farmácia.",
         "Locais terminados em -ia pedem 'in' sem artigo",
         "/in farmaˈtʃiːa/", "Locais com sufixo -ia pedem 'in': in farmacia, in pizzeria, in pasticceria."),

        ("in", "na pizzaria", "A1",
         "Stasera ci troviamo tutti insieme ___ pizzeria.", "in",
         "Hoje à noite nos encontramos todos juntos na pizzaria.",
         "Estabelecimento em -ia",
         "/in pittseˈriːa/", "Regra de ouro: estabelecimentos em -ia dispensam artigo com 'in'."),

        ("in", "na biblioteca", "A1",
         "Gli studenti vanno a studiare ___ biblioteca ogni pomeriggio.", "in",
         "Os estudantes vão estudar na biblioteca todas as tardes.",
         "Local público com sufixo -teca",
         "/in bibljoˈtɛːka/", "Palavras com terminação -teca usam 'in': in biblioteca, in discoteca."),

        ("in", "no banco / na agência bancária", "A1",
         "Devo fare un bonifico urgente: passo prima ___ banca.", "in",
         "Preciso fazer uma transferência urgente: passo antes no banco.",
         "Local comercial clássico com 'in'",
         "/in ˈbaŋka/", "Locais institucionais comuns: in banca, in posta, in ufficio."),

        ("in", "no escritório", "A1",
         "Oggi il direttore rimane ___ ufficio fino a tardi.", "in",
         "Hoje o diretor permanece no escritório até tarde.",
         "Permanência no local de trabalho",
         "/in ufˈfiːtʃo/", "Expressão fixa: 'in ufficio' (no escritório)."),

        ("in", "na cozinha", "A1",
         "Il caffè è pronto: la mamma è ___ cucina a preparare la colazione.", "in",
         "O café está pronto: a mamãe está na cozinha preparando o café da manhã.",
         "Cômodo da casa",
         "/in kuˈtʃiːna/", "Cômodos principais usam 'in': in cucina, in salotto, in camera."),

        # 4. Lugares fixos com 'a'
        ("a", "em casa", "A1",
         "La domenica preferisco rimanere ___ casa a riposare.", "a",
         "No domingo prefiro ficar em casa descansando.",
         "Expressão fixa de moradia: 'a casa'",
         "/a ˈkaːza/", "Com casa usa-se 'a casa' (em casa / para casa)."),

        ("a", "na escola", "A1",
         "A che ora arrivano i bambini ___ scuola la mattina?", "a",
         "A que horas chegam as crianças na escola pela manhã?",
         "Instituição escolar com 'a'",
         "/a ˈskwɔːla/", "Expressão fixa: 'a scuola'."),

        ("a", "no teatro", "A1",
         "Stasera andiamo ___ teatro a vedere un'opera lirica di Verdi.", "a",
         "Hoje à noite vamos ao teatro ver uma ópera lírica de Verdi.",
         "Local cultural clássico com 'a'",
         "/a teˈaːtro/", "Expressão fixa: 'a teatro'."),

        ("a", "à mesa (para comer)", "A1",
         "Tutti ___ tavola! Il pranzo è servito ed è ancora caldo.", "a",
         "Todos à mesa! O almoço está servido e ainda está quente.",
         "Chamada para a refeição",
         "/a ˈtaːvola/", "Diz-se 'a tavola' para o ato de sentar-se para comer."),

        ("a", "na cama / para a cama", "A1",
         "Sono stanchissimo: vado subito ___ letto a dormire.", "a",
         "Estou cansadíssimo: vou imediatamente para a cama dormir.",
         "Ir dormir",
         "/a ˈlɛtto/", "Expressão fixa para dormir: 'andare a letto'."),

        # 5. Preposição DA (proveniência, duração, profissão)
        ("da", "de / desde (ponto de partida)", "A1",
         "Questo aereo parte ___ Milano e arriva a Palermo.", "da",
         "Este avião parte de Milão e chega a Palermo.",
         "Ponto de partida / origem espacial",
         "/da/", "A preposição 'da' marca origem ou proveniência espacial."),

        ("da", "há / desde (duração contínua no presente)", "A1",
         "Studio l'italiano con costanza ___ sei mesi.", "da",
         "Estudo italiano com constância há seis meses.",
         "Ação contínua iniciada no passado e mantida no presente",
         "/da/", "Em italiano, 'da + período' equivale ao português 'há X tempo'."),

        ("dal", "ao / no (ir a um profissional - da + il)", "A1",
         "Ho un forte mal di denti e oggi devo andare ___ dentista.", "dal",
         "Estou com uma forte dor de dente e hoje preciso ir ao dentista.",
         "Ir a um profissional: 'da' articulado com o artigo",
         "/dal denˈtiːsta/", "Ir à casa ou consultório de alguém pede 'da + artigo': dal medico, dal dentista."),

        ("dal", "ao médico", "A1",
         "Non ti senti bene? Allora dovresti proprio andare ___ medico.", "dal",
         "Você não está se sentindo bem? Então você deveria mesmo ir ao médico.",
         "Profissional da saúde masculino (da + il)",
         "/dal ˈmɛːdiko/", "Ir ao consultório de uma pessoa: 'dal medico'."),

        ("da", "na casa de (com nome de pessoa)", "A1",
         "Stasera andiamo a cena ___ Giovanni a mangiare una pizza.", "da",
         "Hoje à noite vamos jantar na casa de Giovanni comer uma pizza.",
         "Ir à residência de alguém com nome próprio",
         "/da dʒoˈvanni/", "Com nomes próprios dispensa-se artigo: 'vado da Giovanni' = vou à casa de Giovanni."),

        ("dai", "na casa dos (plural - da + i)", "A1",
         "La domenica andiamo sempre a pranzo ___ nonni in campagna.", "dai",
         "No domingo vamos sempre almoçar na casa dos avós no campo.",
         "Residência de familiares no plural (da + i nonni)",
         "/dai ˈnɔnni/", "Ir à casa de pessoas no plural: 'dai nonni', 'dagli amici'."),

        ("da", "de (finalidade / uso do objeto)", "A1",
         "D'estate non esco mai di casa senza i miei occhiali ___ sole.", "da",
         "No verão nunca saio de casa sem os meus óculos de sol.",
         "Finalidade ou propósito do objeto",
         "/da ˈsoːle/", "Função do objeto: occhiali da sole, macchina da caffè, camera da letto."),

        ("da", "máquina de café", "A1",
         "Per fare un buon espresso a casa serve una buona macchina ___ caffè.", "da",
         "Para fazer um bom espresso em casa é necessária uma boa máquina de café.",
         "Finalidade da máquina",
         "/da kafˈfɛ/", "Expressão fixa de utilidade: 'macchina da caffè'."),

        ("da", "quarto de dormir", "A1",
         "Questa casa ha un grande salotto e due comode camere ___ letto.", "da",
         "Esta casa tem uma grande sala e dois confortáveis quartos de dormir.",
         "Função do cômodo",
         "/da ˈlɛtto/", "Cômodo destinado a dormir: 'camera da letto'."),

        ("da", "vestido de noite / festa", "A2",
         "Per il galà di stasera ha scelto uno splendido vestito ___ sera.", "da",
         "Para o baile de gala desta noite ela escolheu um lindo vestido de noite.",
         "Uso específico de vestuário",
         "/da ˈseːra/", "Roupas destinadas a ocasiões: vestito da sera, scarpe da ginnastica."),

        # 6. Preposição DI (posse, matéria, tópico)
        ("di", "de (posse / propriedade)", "A1",
         "Questo bel libro di racconti è ___ Marco.", "di",
         "Este belo livro de contos é do Marco.",
         "Posse de alguém",
         "/di/", "A posse direta é indicada pela preposição simples ou articulada 'di'."),

        ("di", "de (material de fabricação)", "A1",
         "Abbiamo comprato un tavolo massiccio fatto ___ legno pregiato.", "di",
         "Compramos uma mesa maciça feita de madeira de lei.",
         "Matéria-prima de construção",
         "/di ˈleɲɲo/", "Matéria: di legno, di ferro, di vetro, d'oro, d'argento."),

        ("d'", "de ouro (elidido diante de vogal)", "A1",
         "Per il loro anniversario si sono regalati un anello ___ oro.", "d'",
         "Pelo aniversário de casamento eles se presentearam com um anel de ouro.",
         "Material com vogal inicial: di + oro = d'oro",
         "/ˈdɔːro/", "Elisão obrigatória de di diante de ouro: 'un anello d'oro'."),

        ("di", "de (assunto / tema de conversa)", "A1",
         "Di cosa state parlando con tanto entusiasmo? — Parliamo ___ musica.", "di",
         "De que vocês estão falando com tanto entusiasmo? — Falamos de música.",
         "Falar a respeito de algo: 'parlare di'",
         "/di ˈmuːzika/", "O verbo 'parlare' rege a preposição 'di' para indicar o assunto."),

        # 7. Regências Verbais Fundamentais com DI
        ("di", "ter necessidade de / precisar de", "A1",
         "Per superare questo esame ho davvero bisogno ___ studiare ogni giorno.", "di",
         "Para passar nesta prova tenho realmente necessidade de estudar todo dia.",
         "Regência de 'avere bisogno': pede 'di'",
         "/aˈveːre biˈzoɲɲo di/", "Locução verbal essencial: 'avere bisogno di + nome/verbo'."),

        ("di", "ter vontade de / apetecer", "A1",
         "Stasera fa freddo: ho proprio voglia ___ bere una cioccolata calda.", "di",
         "Hoje à noite faz frio: tenho mesmo vontade de tomar um chocolate quente.",
         "Regência de 'avere voglia': pede 'di'",
         "/aˈveːre ˈvɔʎʎa di/", "Vontade de fazer algo: 'avere voglia di + infinito'."),

        ("di", "lembrar-se de", "A2",
         "Ti ricordi ___ chiudere la porta a chiave prima di uscire?", "di",
         "Você se lembra de trancar a porta com chave antes de sair?",
         "Regência de 'ricordarsi': pede 'di'",
         "/riˈkordarsi di/", "Lembrar-se de realizar uma ação: 'ricordarsi di fare qc.'."),

        ("di", "terminar de / acabar de (+ infinitivo)", "A2",
         "Appena finisco ___ pranzare ti chiamo subito al telefono.", "di",
         "Assim que terminar de almoçar ligo logo para você no telefone.",
         "Regência de 'finire': pede 'di' diante de infinitivo",
         "/fiˈniːre di/", "Encerrar uma atividade: 'finire di + infinito'."),

        ("di", "decidir (+ infinitivo)", "A2",
         "Abbiamo deciso ___ passare le vacanze estive in Sicilia.", "di",
         "Decidemos passar as férias de verão na Sicília.",
         "Regência de 'decidere': pede 'di'",
         "/deˈtʃiːdere di/", "Tomar uma decisão de fazer: 'decidere di fare qc.'."),

        ("di", "tentar / procurar (+ infinitivo)", "A2",
         "Cerca ___ non fare troppo rumore perché il bambino sta dormendo.", "di",
         "Tente não fazer muito barulho porque a criança está dormindo.",
         "Regência de 'cercare': pede 'di'",
         "/tʃerˈkaːre di/", "Tentar ou empenhar-se em fazer algo: 'cercare di fare qc.'."),

        ("di", "esperar / ter a esperança de (+ infinitivo)", "B1",
         "Spero ___ rivederti presto alla festa di sabato prossimo.", "di",
         "Espero te rever em breve na festa de sábado que vem.",
         "Regência de 'sperare' com mesmo sujeito",
         "/speˈraːre di/", "Quando o sujeito é o mesmo: 'spero di rivederti'."),

        ("di", "ter medo de", "A1",
         "Il mio gattino ha molta paura ___ temporali forti.", "dei",
         "Meu gatinho tem muito medo das tempestades fortes.",
         "Regência de 'avere paura': pede 'di' articulado (di + i = dei)",
         "/aˈveːre paˈuːra dei/", "Expressão de temor: 'avere paura di/dei'."),

        # 8. Regências Verbais Fundamentais com A
        ("a", "começar a (+ infinitivo)", "A1",
         "Prendi l'ombrello perché comincia ___ piovere forte.", "a",
         "Pegue o guarda-chuva porque está começando a chover forte.",
         "Regência de 'cominciare': pede sempre 'a'",
         "/kominˈtʃaːre a/", "Iniciar uma ação: 'cominciare a + infinito' ou 'iniziare a + infinito'."),

        ("a", "iniciar a (+ infinitivo)", "A1",
         "A che ora inizi ___ lavorare la mattina?", "a",
         "A que horas você começa a trabalhar de manhã?",
         "Regência de 'iniziare': pede 'a'",
         "/iniˈtsjaːre a/", "Sinônimo de cominciare: 'iniziare a fare qc.'."),

        ("a", "aprender a (+ infinitivo)", "A1",
         "I bambini imparano ___ nuotare molto velocemente d'estate.", "a",
         "As crianças aprendem a nadar muito rapidamente no verão.",
         "Regência de 'imparare': pede 'a'",
         "/impaˈraːre a/", "Adquirir uma habilidade: 'imparare a fare qc.'."),

        ("a", "continuar a (+ infinitivo)", "A2",
         "Nonostante la pioggia battente, loro continuano ___ camminare.", "a",
         "Apesar da chuva forte, eles continuam a caminhar.",
         "Regência de 'continuare': pede 'a'",
         "/kontiˈnwaːre a/", "Manter uma atividade em progresso: 'continuare a fare qc.'."),

        ("a", "conseguir / ser capaz de (+ infinitivo)", "A2",
         "Non riesco ___ capire questa complicata regola di grammatica.", "a",
         "Não consigo entender esta regra gramatical complicada.",
         "Regência de 'riuscire': pede 'a'",
         "/rjuʃˈʃiːre a/", "Capacidade de obter sucesso numa ação: 'riuscire a fare qc.'."),

        ("a", "ajudar alguém a (+ infinitivo)", "A1",
         "Mi aiuti ___ portare queste valigie pesanti fino al secondo piano?", "a",
         "Você me ajuda a carregar estas malas pesadas até o segundo andar?",
         "Regência de 'aiutare': pede 'a'",
         "/ajuˈtaːre a/", "Prestar assistência em uma tarefa: 'aiutare qcn. a fare qc.'."),

        ("a", "experimentar / tentar (+ infinitivo)", "A2",
         "Prova ___ spegnere e riaccendere il computer per risolvere il blocco.", "a",
         "Experimente desligar e ligar de novo o computador para resolver o travamento.",
         "Regência de 'provare': pede 'a'",
         "/proˈvaːre a/", "Fazer uma tentativa prática: 'provare a fare qc.'."),

        ("a", "ir fazer algo (+ infinitivo)", "A1",
         "Oggi andiamo ___ fare la spesa al nuovo supermercato del quartiere.", "a",
         "Hoje vamos fazer compras no novo supermercado do bairro.",
         "Regência de deslocamento para ação: 'andare a'",
         "/anˈdaːre a/", "Deslocar-se para executar um ato: 'andare a fare la spesa'."),

        ("a", "ficar a fazer algo (+ infinitivo)", "A2",
         "Non restare lì ___ guardare senza fare niente: dacci una mano!", "a",
         "Não fique aí a olhar sem fazer nada: dê-nos uma mão!",
         "Permanecer em uma atitude: 'restare a'",
         "/reˈstaːre a/", "Manter-se numa postura ou ação: 'restare a guardare'."),

        # 9. Preposição SU (posição superior, tema)
        ("sul", "sobre o / em cima do (su + il)", "A1",
         "Il gatto dorme beato ___ divano del soggiorno.", "sul",
         "O gato dorme feliz sobre o sofá da sala.",
         "Contato físico superior com substantivo masculino com 'il'",
         "/sul diˈvaːno/", "Contração de 'su + il = sul'."),

        ("sulla", "sobre a / em cima da (su + la)", "A1",
         "Ho appoggiato le chiavi di casa ___ tavola della cucina.", "sulla",
         "Apoiei as chaves de casa sobre a mesa da cozinha.",
         "Contração com feminino singular: su + la",
         "/ˈsulla ˈtaːvola/", "Contração de 'su + la = sulla'."),

        ("su", "sobre / a respeito de (tópico)", "A2",
         "Abbiamo visto un documentario molto interessante ___ Venezia antica.", "su",
         "Vimos um documentário muito interessante sobre a Veneza antiga.",
         "Tema de uma obra ou palestra",
         "/su/", "Tratar de um tema: 'un libro su Dante', 'un film su Roma'."),

        ("sull'", "sobre o/a (com palavra começada em vogal - su + l')", "A1",
         "La borsa è appoggiata ___ armadio in camera da letto.", "sull'",
         "A bolsa está apoiada sobre o armário no quarto de dormir.",
         "Contração antes de vogal: su + l'",
         "/sull arˈmaːdjo/", "Diante de vogal usa-se sull': sull'armadio, sull'albero."),

        # 10. Preposição PER (destino, causa, duração fechada)
        ("per", "para (direção de transporte)", "A1",
         "Il treno veloce ___ Roma Termini parte dal binario numero cinque.", "per",
         "O trem rápido para Roma Termini parte da plataforma número cinco.",
         "Destino de trem, ônibus ou voo",
         "/per/", "Destino de transporte público: 'il treno per Firenze'."),

        ("per", "por / durante (duração concluída no tempo)", "A1",
         "Ho abitato a Milano ___ due anni quando ero all'università.", "per",
         "Morei em Milão por dois anos quando estava na universidade.",
         "Tempo concluído no passado",
         "/per/", "Para período com início e fim no passado usa-se 'per': 'per due anni'."),

        ("per", "por / de (causa / motivo)", "A2",
         "Piangeva dalla commozione ___ la gioia di aver vinto il concorso.", "per",
         "Chorava de comoção pela alegria de ter vencido o concurso.",
         "Causa determinante de uma emoção",
         "/per la ˈdʒɔːja/", "Expressar o motivo ou razão: 'per la gioia', 'per paura'."),

        ("per", "para (favor cortês / benefício)", "A1",
         "Puoi chiudere la finestra, ___ favore? Fa un po' freddo.", "per",
         "Você pode fechar a janela, por favor? Faz um pouco de frio.",
         "Expressão de cortesia universal",
         "/per faˈvoːre/", "Expressão fixa: 'per favore' (por favor)."),

        # 11. Preposições TRA / FRA (tempo futuro e espaço intermediário)
        ("tra", "daqui a / entre (tempo futuro)", "A1",
         "Il film comincia ___ dieci minuti esatti: sbrighiamoci a entrare!", "tra",
         "O filme começa daqui a exatos dez minutos: apressemos-nos a entrar!",
         "Tempo que falta para acontecer",
         "/tra ˈdjɛːtʃi ˈmiːnuti/", "'Tra' e 'fra' são perfeitamente intercambiáveis para tempo futuro."),

        ("fra", "daqui a (tempo futuro)", "A1",
         "Partiamo per le vacanze al mare ___ due settimane.", "fra",
         "Partimos para as férias na praia daqui a duas semanas.",
         "Equivalente exato de 'tra'",
         "/fra/", "Usa-se 'fra' por razões de eufonia, especialmente se a palavra seguinte não começar com f-."),

        ("tra", "entre dois pontos geográficos", "A1",
         "Orvieto si trova a metà strada ___ Roma e Firenze.", "tra",
         "Orvieto fica no meio do caminho entre Roma e Florença.",
         "Espaço intermediário entre dois pontos",
         "/tra/", "Posição intermediária física: 'tra due città'."),

        ("tra", "entre (comunidade de amigos/pessoas)", "A1",
         "___ amici non c'è bisogno di troppe formalità.", "Tra",
         "Entre amigos não há necessidade de excesso de formalidades.",
         "Relação mútua",
         "/tra aˈmiːtʃi/", "Convivência compartilhada: 'tra amici', 'fra di noi'."),

        # 12. Preposições Articuladas em Detalhe (Contrações Obrigatórias)
        ("del", "do (di + il)", "A1",
         "Questo è l'orologio ___ nonno che ho ereditato.", "del",
         "Este é o relógio do avô que herdei.",
         "Contração de di + il",
         "/del/", "Articulada masculina singular padrão."),

        ("dello", "do (di + lo - diante de s impuro / z / gn / ps)", "A1",
         "Ecco lo zaino ___ studente che ha dimenticato in classe.", "dello",
         "Eis a mochila do estudante que ele esqueceu na sala.",
         "Diante de substantivo masculino iniciado por st-",
         "/ˈdello stuˈdɛnte/", "Usa-se 'dello' diante de s+consoante, z, gn, ps: dello studente, dello zio."),

        ("dell'", "do / da (di + l' - diante de vogal)", "A1",
         "Il profumo ___ arancia fresca riempie tutta la cucina.", "dell'",
         "O perfume da laranja fresca enche toda a cozinha.",
         "Diante de palavra iniciada por vogal",
         "/dell aˈrantʃa/", "Elisão diante de vogal: dell'arancia, dell'amico."),

        ("della", "da (di + la - feminino singular)", "A1",
         "La porta ___ cucina è rimasta aperta.", "della",
         "A porta da cozinha ficou aberta.",
         "Feminino singular padrão",
         "/ˈdella/", "Contração de di + la = della."),

        ("dei", "dos (di + i - masculino plural)", "A1",
         "I libri ___ ragazzi sono tutti ordinati sullo scaffale.", "dei",
         "Os livros dos meninos estão todos arrumados na estante.",
         "Masculino plural padrão",
         "/dei/", "Contração de di + i = dei."),

        ("degli", "dos (di + gli - masculino plural com vogal / s impuro / z)", "A1",
         "I consigli ___ amici fidati sono sempre preziosi.", "degli",
         "Os conselhos dos amigos de confiança são sempre preciosos.",
         "Masculino plural diante de vogal (amici)",
         "/ˈdeʎʎi aˈmiːtʃi/", "Usa-se 'degli' diante de vogal, s+consoante ou z: degli amici, degli studenti."),

        ("delle", "das (di + le - feminino plural)", "A1",
         "Il colore ___ foglie in autunno diventa dorato.", "delle",
         "A cor das folhas no outono fica dourada.",
         "Feminino plural",
         "/ˈdelle/", "Contração de di + le = delle."),

        ("al", "ao (a + il)", "A1",
         "Vado ___ mercato a comprare frutta fresca di stagione.", "al",
         "Vou ao mercado comprar frutas frescas da época.",
         "Contração a + il",
         "/al/", "Contração básica masculina singular: al cinema, al bar, al mercato."),

        ("allo", "ao (a + lo - diante de s impuro / z)", "A1",
         "Domenica prossima andiamo tutti ___ stadio a vedere la partita.", "allo",
         "No próximo domingo vamos todos ao estádio ver o jogo.",
         "Diante de s+consoante (stadio)",
         "/ˈallo ˈstaːdjo/", "Usa-se 'allo' com termos masculinos em s-impuro ou z: allo stadio, allo zoo."),

        ("all'", "ao / à (a + l' - diante de vogal)", "A1",
         "Siamo arrivati ___ aeroporto con due ore di anticipo.", "all'",
         "Chegamos ao aeroporto com duas horas de antecedência.",
         "Diante de vogal",
         "/all aeroˈpɔrto/", "Contração elidida: all'aeroporto, all'inizio, all'ospedale."),

        ("alla", "à (a + la - feminino singular)", "A1",
         "Chiedi l'orario del treno ___ stazione centrale.", "alla",
         "Peça o horário do trem na estação central.",
         "Feminino singular",
         "/ˈalla statˈtsjoːne/", "Contração a + la = alla: alla stazione, alla fermata."),

        ("ai", "aos (a + i - masculino plural)", "A1",
         "Ho fatto gli auguri di buon compleanno ___ miei colleghi.", "ai",
         "Dei os parabéns de aniversário aos meus colegas.",
         "Masculino plural",
         "/ai/", "Contração a + i = ai."),

        ("agli", "aos (a + gli - masculino plural com vogal/s impuro)", "A1",
         "Il professore ha spiegato il compito ___ studenti con pazienza.", "agli",
         "O professor explicou a tarefa aos estudantes com paciência.",
         "Diante de s+consoante no plural",
         "/ˈaʎʎi stuˈdɛnti/", "Contração a + gli = agli."),

        ("alle", "às (a + le - feminino plural / horas)", "A1",
         "Ci vediamo puntuali ___ otto di sera davanti al ristorante.", "alle",
         "Nos vemos pontuais às oito da noite em frente ao restaurante.",
         "Indicação de horas no relógio",
         "/ˈalle ˈɔtto/", "Para horas usa-se sempre 'alle': alle otto, alle tre, alle cinque."),

        ("nel", "no (in + il)", "A1",
         "Ho dimenticato gli occhiali da sole ___ cassetto del comodino.", "nel",
         "Esqueci os óculos de sol na gaveta da mesinha de cabeceira.",
         "Contração in + il",
         "/nel kasˈsetto/", "Contração de in + il = nel."),

        ("nello", "no (in + lo)", "A1",
         "Metti i quaderni ___ zaino prima di uscire per andare a scuola.", "nello",
         "Coloque os cadernos na mochila antes de sair para ir à escola.",
         "Diante de z- (zaino)",
         "/ˈnello ˈdzaiːno/", "Contração in + lo = nello: nello zaino, nello specchio."),

        ("nell'", "no / na (in + l' - diante de vogal)", "A1",
         "La chiave è rimasta infilata ___ serratura della porta.", "nell'",
         "A chave ficou enfiada na fechadura da porta.",
         "Diante de vogal",
         "/nell/", "Contração in + l' = nell': nell'acqua, nell'armadio."),

        ("nella", "na (in + la)", "A1",
         "C'è una sorpresa speciale nascosta ___ scatola regalo.", "nella",
         "Há uma surpresa especial escondida na caixa de presente.",
         "Feminino singular",
         "/ˈnella ˈskaːtola/", "Contração in + la = nella."),

        ("nei", "nos (in + i)", "A1",
         "D'estate facciamo lunghe passeggiate ___ boschi della montagna.", "nei",
         "No verão fazemos longas caminhadas nos bosques da montanha.",
         "Masculino plural",
         "/nei ˈbɔski/", "Contração in + i = nei."),

        ("negli", "nos (in + gli)", "A1",
         "Ho vissuto per tre anni ___ Stati Uniti per motivi di studio.", "negli",
         "Vivi por três anos nos Estados Unidos por motivos de estudo.",
         "Diante de s+consoante no plural",
         "/ˈneʎʎi ˈstaːti uˈniːti/", "Contração in + gli = negli: negli Stati Uniti, negli occhi."),

        ("nelle", "nas (in + le)", "A1",
         "Ci sono molti fiori colorati ___ aiuole del giardino.", "nelle",
         "Há muitas flores coloridas nos canteiros do jardim.",
         "Feminino plural",
         "/ˈnelle/", "Contração in + le = nelle."),

        # 13. Locuções Prepositivas Clássicas
        ("davanti a", "na frente de / diante de", "A1",
         "Ci vediamo ___ alla fontana in piazza?", "davanti",
         "Nos vemos na frente da fonte na praça?",
         "Posição frontal no espaço",
         "/daˈvanti a/", "Locução de posição: 'davanti a'."),

        ("dietro a", "atrás de", "A1",
         "Il gatto si è nascosto ___ alla porta per fare un agguato.", "dietro",
         "O gato se escondeu atrás da porta para dar um bote.",
         "Posição posterior",
         "/ˈdjɛːtro a/", "Locução de posição: 'dietro a'."),

        ("vicino a", "perto de / próximo a", "A1",
         "Abito molto ___ alla fermata della metropolitana.", "vicino",
         "Moro muito perto da estação de metrô.",
         "Proximidade espacial",
         "/viˈtʃiːno a/", "Rege a preposição 'a': 'vicino a'."),

        ("lontano da", "longe de", "A1",
         "L'aeroporto è abbastanza ___ dal centro della città.", "lontano",
         "O aeroporto fica bastante longe do centro da cidade.",
         "Distância espacial",
         "/lonˈtaːno da/", "Rege a preposição 'da': 'lontano da'."),

        ("accanto a", "ao lado de / junto de", "A1",
         "Siediti qui ___ a me, così possiamo chiacchierare.", "accanto",
         "Sente-se aqui ao meu lado, assim podemos conversar.",
         "Lateralidade imediata",
         "/akˈkanto a/", "Rege 'a': 'accanto a'."),

        ("insieme a", "junto com", "A1",
         "Vado al concerto di musica jazz ___ a mio fratello.", "insieme",
         "Vou ao concerto de jazz junto com meu irmão.",
         "Companhia compartilhada",
         "/inˈsjɛːme a/", "Locução de companhia: 'insieme a'."),

        ("prima di", "antes de (+ infinitivo/nome)", "A1",
         "Bevi un bicchiere d'acqua ___ di andare a correre.", "prima",
         "Beba um copo de água antes de ir correr.",
         "Precedência temporal",
         "/ˈpriːma di/", "Rege 'di': 'prima di mangiare', 'prima di cena'."),

        ("dopo di", "depois de (+ pronome)", "A1",
         "Puoi entrare tranquillamente subito ___ di me.", "dopo",
         "Você pode entrar tranquilamente logo depois de mim.",
         "Sucessão temporal com pronome",
         "/ˈdɔːpo di/", "Com pronomes tônicos pede 'di': 'dopo di me', 'dopo di te'."),

        ("senza di", "sem (+ pronome)", "A1",
         "Non possiamo partire per il viaggio ___ di te!", "senza",
         "Não podemos partir para a viagem sem você!",
         "Ausência com pronome",
         "/ˈsɛntsa di/", "Com pronomes pede 'di': 'senza di me', 'senza di te'."),

        ("invece di", "em vez de / ao invés de", "A2",
         "Perché non vieni al cinema con noi ___ di restare a casa da solo?", "invece",
         "Por que não vem ao cinema conosco em vez de ficar em casa sozinho?",
         "Alternativa / substituição",
         "/inˈveːtʃe di/", "Locução: 'invece di + infinito'."),

        ("grazie a", "graças a", "A2",
         "Ha superato l'esame brillantemente ___ all'aiuto del suo insegnante.", "grazie",
         "Passou na prova brilhantemente graças à ajuda de seu professor.",
         "Causa positiva / reconhecimento",
         "/ˈɡrattsje a/", "Rege 'a': 'grazie a te', 'grazie a lui'."),

        ("a causa di", "por causa de / devido a", "A2",
         "Il volo è stato cancellato a ___ della fitta nebbia.", "causa",
         "O voo foi cancelado por causa da neblina densa.",
         "Causa com sentido desfavorável",
         "/a ˈkawza di/", "Locução causal formal: 'a causa di'."),

        ("in mezzo a", "no meio de / entre", "A2",
         "Ci siamo trovati bloccati in ___ al traffico dell'ora di punta.", "mezzo",
         "Nós nos encontramos travados no meio do trânsito do horário de pico.",
         "Centro de um espaço ou grupo",
         "/in ˈmɛddzo a/", "Localização central: 'in mezzo a'."),

        ("fino a", "até (+ lugar/tempo)", "A1",
         "Ti accompagno volentieri ___ alla porta di casa.", "fino",
         "Eu te acompanho com prazer até a porta de casa.",
         "Limite espacial ou temporal",
         "/ˈfiːno a/", "Limite de percurso ou tempo: 'fino a Roma', 'fino alle sei'."),

        ("intorno a", "em volta de / por volta de", "A2",
         "Ci siamo seduti tutti ___ al tavolo rotondo del giardino.", "intorno",
         "Sentamo-nos todos em volta da mesa redonda do jardim.",
         "Disposição circular ou aproximação de horário",
         "/inˈtorno a/", "Círculo espacial ou horário aproximado: 'intorno alle otto'."),

        ("sul serio", "a sério / de verdade", "A2",
         "Ma dici ___ o stai scherzando per farmi ridere?", "sul serio",
         "Mas você está falando sério ou está brincando para me fazer rir?",
         "Expressão adverbial com 'su'",
         "/sul ˈsɛːrjo/", "Expressão fixa: 'parlare sul serio', 'prendere sul serio'."),

        ("a caso", "ao acaso / aleatoriamente", "A2",
         "Non scegliere le risposte ___: leggi con attenzione ogni domanda!", "a caso",
         "Não escolha as respostas ao acaso: leia com atenção cada pergunta!",
         "Sem planejamento deliberado",
         "/a ˈkaːzo/", "Locução adverbial: 'a caso' (ao acaso)."),

        ("di fretta", "com pressa / às pressas", "A1",
         "Stamattina sono uscito ___ e ho dimenticato l'ombrello.", "di fretta",
         "Esta manhã saí com pressa e esqueci o guarda-chuva.",
         "Modo apressado de fazer uma ação",
         "/di ˈfretta/", "Locução adverbial de pressa: 'essere di fretta', 'fare di fretta'."),
    ]

    cards = []
    for idx, (it, pt, niv, fr, ver, tr_fr, dic, ipa, exp) in enumerate(raw[:100], 1):
        cards.append({
            "id": f"fc_prep_{idx:03d}",
            "deck": "preposizioni",
            "deck_nome": "Preposições & Regências",
            "nivel": niv,
            "italiano": it,
            "portugues": pt,
            "categoria": "preposizioni",
            "frente": fr,
            "verso": ver,
            "traducao_frase": tr_fr,
            "dica": dic,
            "exemplo": fr.replace("___", ver),
            "exemplo_pt": tr_fr,
            "audio_palavra": it,
            "audio_frase": fr.replace("___", ver),
            "audio_ipa": ipa,
            "explicacao": exp
        })
    return cards
