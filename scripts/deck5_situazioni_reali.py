#!/usr/bin/env python3
"""
scripts/deck5_situazioni_reali.py
Gera 100 Flashcards Cloze de Situações da Vida Real:
  1. Al Bar / Caffè (10)
  2. Al Ristorante / Trattoria (10)
  3. Alla Stazione dei Treni (10)
  4. All'Aeroporto (10)
  5. In Farmacia e Salute (10)
  6. All'Hotel / Alloggio (10)
  7. Per Strada / Indicazioni (10)
  8. Nei Negozi / Shopping (10)
  9. Al Supermercato / Mercato (10)
  10. Poste, Emergenze e Vita Sociale (10)
"""

from typing import Any


def get_deck_situazioni_reali() -> list[dict[str, Any]]:
    raw = [
        # --- 1. Al Bar / Caffè (10) ---
        ("un caffè", "um espresso simples", "A1",
         "Buongiorno! Vorrei ___ al banco, per favore.", "un caffè",
         "Bom dia! Gostaria de um café no balcão, por favor.",
         "Pedido básico no bar: um café espresso simples",
         "/un kafˈfɛ/", "Na Itália, pedir 'un caffè' significa automaticamente um café espresso puro."),

        ("al banco", "no balcão (sem taxa de mesa)", "A1",
         "Prendiamo il cappuccino ___ o ci sediamo fuori al tavolo?", "al banco",
         "Tomamos o cappuccino no balcão ou sentamos lá fora na mesa?",
         "Local de consumo em pé no bar",
         "/al ˈbaŋko/", "Consumir 'al banco' é mais rápido e mais econômico do que 'al tavolo'."),

        ("al tavolo", "na mesa (com taxa de serviço/coperto)", "A1",
         "Se ci accomodiamo ___ c'è il servizio del cameriere.", "al tavolo",
         "Se nos acomodarmos na mesa há o serviço do garçom.",
         "Consumo sentado à mesa",
         "/al ˈtaːvolo/", "O consumo 'al tavolo' pode incluir acréscimo de serviço."),

        ("cornetto", "croissant italiano matinal", "A1",
         "Per me un caffè macchiato e un ___ alla crema, grazie.", "cornetto",
         "Para mim um café macchiato e um croissant de creme, obrigado.",
         "Doce típico do café da manhã italiano",
         "/korˈnetto/", "O pão doce típico do café da manhã na Itália chama-se 'cornetto' (em Roma/sul) ou 'brioche' (no norte)."),

        ("caffè macchiato", "espresso com uma 'mancha' de leite quente", "A1",
         "Preferisco un ___ caldo con un goccio di latte montato.", "caffè macchiato",
         "Prefiro um café com um pingo de leite quente.",
         "Café espresso com pingo de leite",
         "/kafˈfɛ makˈkjaːto/", "Leva apenas uma manchinha ('macchia') de leite."),

        ("caffè corretto", "espresso com uma dose de licor/grappa", "A2",
         "Dopo cena il signore ordina un ___ con la grappa.", "caffè corretto",
         "Depois do jantar o senhor pede um café corrigido com grappa.",
         "Café com adição de bebida alcoólica",
         "/kafˈfɛ korˈrɛtto/", "Corretto = com algumas gotas de grappa, sambuca ou conhaque."),

        ("spremuta", "suco de laranja natural espremido na hora", "A1",
         "Vorrei una ___ d'arancia fresca senza zucchero, per favore.", "spremuta",
         "Gostaria de um suco de laranja natural sem açúcar, por favor.",
         "Suco espremido na hora",
         "/spreˈmuːta/", "Suco de laranja espremido na hora chama-se 'spremuta d'arancia'."),

        ("scontrino", "comprovante fiscal / cupom de pagamento", "A1",
         "Prima si fa lo ___ alla cassa, poi si ordina al barista.", "scontrino",
         "Primeiro se tira o cupom fiscal no caixa, depois se pede ao barista.",
         "Cupom impresso do caixa",
         "/skonˈtriːno/", "Em muitos bares italianos tradicionais, paga-se primeiro no caixa e leva-se o 'scontrino' ao balcão."),

        ("resto", "troco em dinheiro", "A1",
         "Ecco a Lei il caffè e due euro di ___.", "resto",
         "Aqui está para o senhor o café e dois euros de troco.",
         "Diferença devolvida em dinheiro",
         "/ˈrɛsto/", "Troco de pagamento se chama 'il resto'."),

        ("tramezzino", "sanduíche triangular macio sem casca", "A1",
         "Per lo spuntino prendo un ___ con tonno e pomodoro.", "tramezzino",
         "Para o lanche pego um sanduíche triangular de atum e tomate.",
         "Sanduíche típico de pão de fôrma triangular",
         "/tramedˈdziːno/", "Clássico lanche rápido nos bares e cafés italianos."),

        # --- 2. Al Ristorante / Trattoria (10) ---
        ("prenotazione", "reserva de mesa", "A1",
         "Buonasera, abbiamo una ___ a nome Rossi per quattro persone.", "prenotazione",
         "Boa noite, temos uma reserva em nome de Rossi para quatro pessoas.",
         "Reserva prévia",
         "/prenotatˈtsjoːne/", "A reserva se diz 'la prenotazione'. Reservar é 'prenotare'."),

        ("il menù", "o cardápio", "A1",
         "Possiamo dare un'occhiata al ___ prima di ordinare?", "menù",
         "Podemos dar uma olhada no cardápio antes de pedir?",
         "Lista de pratos e preços",
         "/meˈnu/", "Também chamado de 'la carta'."),

        ("antipasto", "entrada / aperitivo antes da massa", "A1",
         "Come ___ vorremmo un tagliere misto di salumi e formaggi.", "antipasto",
         "Como entrada gostaríamos de uma tábua mista de frios e queijos.",
         "Prato que antecede o primeiro prato",
         "/antiˈpaːsto/", "A clássica refeição italiana inicia pelo 'antipasto'."),

        ("primo", "primeiro prato (massa, risoto, sopa)", "A1",
         "Per ___ prendo le tagliatelle ai funghi porcini.", "primo",
         "De primeiro prato vou querer o talharim com cogumelos porcini.",
         "Prato principal de carboidrato",
         "/ˈpriːmo/", "O 'primo piatto' é tipicamente pasta, risoto ou gnocchi."),

        ("secondo", "segundo prato (carne, peixe ou ovos)", "A1",
         "E per ___, gradite della carne alla griglia o del pesce fresco?", "secondo",
         "E de segundo prato, os senhores gostariam de carne grelhada ou peixe fresco?",
         "Prato proteico da refeição italiana",
         "/seˈkondo/", "O 'secondo' vem após a massa, acompanhado de contorno."),

        ("contorno", "guarnição / acompanhamento de legumes ou salada", "A1",
         "Come ___ ordiniamo patate al forno e insalata mista.", "contorno",
         "Como guarnição pedimos batatas ao forno e salada mista.",
         "Acompanhamento vegetal",
         "/konˈtorno/", "Legumes grelhados, salada ou batatas que acompanham o secondo."),

        ("coperto", "taxa de talher, pão e serviço de mesa", "A1",
         "Nel conto c'è sempre la voce del ___ per il pane e la tavola.", "coperto",
         "Na conta há sempre o item do coperto pelo pão e serviço de mesa.",
         "Taxa tradicional de mesa italiana",
         "/koˈpɛrto/", "Taxa fixa tradicional italiana (geralmente entre 1,50€ e 3,50€ por pessoa)."),

        ("il conto", "a conta da refeição", "A1",
         "Cameriere, ci porta ___ per favore quando ha un attimo?", "il conto",
         "Garçom, traz-nos a conta por favor quando tiver um momento?",
         "Valor total do consumo",
         "/il ˈkonto/", "Pedir a conta: 'Il conto, per favore'."),

        ("acqua naturale", "água mineral sem gás", "A1",
         "Da bere desideriamo una bottiglia di ___ a temperatura ambiente.", "acqua naturale",
         "Para beber queremos uma garrafa de água sem gás em temperatura ambiente.",
         "Água sem gás",
         "/ˈakkwa natuˈraːle/", "Água sem gás = naturale ou liscia. Com gás = frizzante ou gassata."),

        ("acqua frizzante", "água mineral com gás", "A1",
         "Io invece preferisco una bottiglia di ___ fresca di frigo.", "acqua frizzante",
         "Eu por outro lado prefiro uma garrafa de água com gás gelada da geladeira.",
         "Água com gás borbulhante",
         "/ˈakkwa fritˈtsante/", "Com gás = frizzante."),

        # --- 3. Alla Stazione dei Treni (10) ---
        ("biglietto", "passagem / bilhete de trem", "A1",
         "Vorrei un ___ per Firenze per il treno delle quattordici.", "biglietto",
         "Gostaria de uma passagem para Florença para o trem das quatorze horas.",
         "Tíquete de viagem",
         "/biʎˈʎetto/", "Passagem de transporte público ferroviário."),

        ("sola andata", "somente ida", "A1",
         "Le serve un biglietto di ___ o andata e ritorno?", "sola andata",
         "O senhor precisa de uma passagem de somente ida ou ida e volta?",
         "Viagem só em um sentido",
         "/ˈsoːla anˈdaːta/", "Sola andata (só ida) vs andata e ritorno (ida e volta)."),

        ("andata e ritorno", "ida e volta", "A1",
         "Prendo un biglietto di ___ con ritorno domenica sera.", "andata e ritorno",
         "Compro uma passagem de ida e volta com retorno no domingo à noite.",
         "Viagem completa de ida e regresso",
         "/anˈdaːta e riˈtorno/", "Ida e volta."),

        ("binario", "plataforma / trilho de embarque", "A1",
         "Da quale ___ parte il treno Frecciarossa per Venezia?", "binario",
         "De qual plataforma parte o trem Frecciarossa para Veneza?",
         "Trilho/plataforma numerada na estação",
         "/biˈnaːrjo/", "Plataforma onde o trem para (ex: Binario 3)."),

        ("convalidare", "validar / carimbar o bilhete antes de subir", "A1",
         "Attenzione: deve ___ il biglietto regionale alle macchinette gialle!", "convalidare",
         "Atenção: você deve validar o bilhete regional nas maquininhas amarelas!",
         "Carimbar na máquina validadora",
         "/konvaliˈdaːre/", "Obrigatório para bilhetes regionais sem assento reservado para evitar multa."),

        ("ritardo", "atraso no horário", "A1",
         "Il treno regionale viaggia con quindici minuti di ___.", "ritardo",
         "O trem regional viaja com quinze minutos de atraso.",
         "Demora no horário programado",
         "/riˈtardo/", "Atraso: 'essere in ritardo', 'viaggiare con ritardo'."),

        ("anticipo", "antecedência / adiantado", "A1",
         "Oggi il Frecciarossa è arrivato addirittura con cinque minuti di ___.", "anticipo",
         "Hoje o Frecciarossa chegou inclusive com cinco minutos de antecedência.",
         "Chegar antes da hora",
         "/anˈtiːtʃipo/", "Estar adiantado: 'in anticipo'."),

        ("coincidenza", "baldeação / conexão entre trens", "A2",
         "A Bologna dobbiamo scendere per prendere la ___ per Verona.", "coincidenza",
         "Em Bolonha devemos descer para pegar a conexão para Verona.",
         "Troca de trem em estação intermediária",
         "/kointʃiˈdɛntsa/", "Conexão ferroviária chama-se 'coincidenza'."),

        ("posto", "assento / lugar marcado", "A1",
         "Scusi, questo è il mio ___: carrozza sei, numero quarantacinque.", "posto",
         "Com licença, este é o meu assento: vagão seis, número 45.",
         "Lugar para sentar no vagão",
         "/ˈpɔsto/", "Assento reservado: posto a sedere."),

        ("carrozza", "vagão de trem de passageiros", "A1",
         "Il nostro posto riservato si trova nella ___ numero quattro.", "carrozza",
         "O nosso assento reservado fica no vagão número quatro.",
         "Vagão ferroviário",
         "/karˈrɔttsa/", "Vagão de trem em italiano chama-se 'carrozza'."),

        # --- 4. All'Aeroporto (10) ---
        ("carta d'imbarco", "cartão de embarque (boarding pass)", "A1",
         "Mostri il documento d'identità e la ___ al gate.", "carta d'imbarco",
         "Mostre o documento de identidade e o cartão de embarque no portão.",
         "Bilhete com código de barras para entrar no avião",
         "/ˈkarta dimˈbarko/", "Documento oficial de acesso à aeronave."),

        ("bagaglio a mano", "bagagem de mão", "A1",
         "Posso portare questo piccolo zaino come ___ a bordo?", "bagaglio a mano",
         "Posso levar esta pequena mochila como bagagem de mão a bordo?",
         "Mala pequena que vai na cabine",
         "/baˈɡaʎʎo a ˈmaːno/", "Bagagem que você leva consigo na cabine do avião."),

        ("bagaglio da stiva", "bagagem despachada no porão do avião", "A2",
         "Dobbiamo registrare la valigia pesante al banco come ___.", "bagaglio da stiva",
         "Devemos despachar a mala pesada no balcão como bagagem de porão.",
         "Mala despachada",
         "/baˈɡaʎʎo da ˈstiːva/", "Bagagem de porão que vai no compartimento de carga."),

        ("controllo di sicurezza", "inspeção / controle de segurança do raio-X", "A1",
         "Tolga la cintura e il computer prima del ___.", "controllo di sicurezza",
         "Tire o cinto e o computador antes da inspeção de segurança.",
         "Área de inspeção e raio-X",
         "/konˈtrɔllo di sikuˈrettsa/", "Controle de segurança no aeroporto."),

        ("porta d'imbarco", "portão de embarque (gate)", "A1",
         "Il volo per Roma parte dalla ___ numero B12.", "porta d'imbarco",
         "O voo para Roma parte pelo portão de embarque número B12.",
         "Portão de embarque para o avião",
         "/ˈpɔrta dimˈbarko/", "Em italiano gate traduz-se como 'porta d'imbarco' ou simplesmente 'uscita'."),

        ("decollo", "decolagem da aeronave", "A2",
         "Allacciate le cinture di sicurezza: siamo pronti per il ___.", "decollo",
         "Apertem os cintos de segurança: estamos prontos para a decolagem.",
         "Momento em que o avião sai do solo",
         "/deˈkɔllo/", "Decolar é 'decollare'. Decolagem é 'il decollo'."),

        ("atterraggio", "pouso / aterrissagem da aeronave", "A2",
         "L'aereo è atterrato regolarmente: perfetto ___ a Milano Malpensa.", "atterraggio",
         "O avião pousou regularmente: pouso perfeito em Milão Malpensa.",
         "Momento em que o avião toca a pista",
         "/atterˈraddʒo/", "Aterrissar é 'atterrare'. Pouso é 'l'atterraggio'."),

        ("dogana", "alfândega de controle de mercadorias", "A2",
         "Dopo aver ritirato le valigie bisogna passare attraverso la ___.", "dogana",
         "Após retirar as malas é preciso passar através da alfândega.",
         "Controle aduaneiro de fronteira",
         "/doˈɡaːna/", "Alfândega oficial de fronteira e aeroporto."),

        ("passaporto", "passaporte oficial de viagem", "A1",
         "Tenga a portata di mano il Suo ___ valido per l'espatrio.", "passaporto",
         "Tenha à mão o seu passaporte válido para o exterior.",
         "Documento internacional de viagem",
         "/passaˈpɔrto/", "Documento de identidade para viagens internacionais."),

        ("nastro bagagli", "esteira rolante de restituição de bagagens", "A1",
         "Le valigie del nostro volo arriveranno sul ___ numero tre.", "nastro bagagli",
         "As malas do nosso voo chegarão na esteira número três.",
         "Esteira giratória de malas",
         "/ˈnastro baˈɡaʎʎi/", "Onde se recolhem as malas despachadas no desembarque."),

        # --- 5. In Farmacia e Salute (10) ---
        ("ricetta", "receita médica prescrita", "A1",
         "Questo farmaco antibiotico si può comprare solo con la ___ medica.", "ricetta",
         "Este medicamento antibiótico só pode ser comprado com a receita médica.",
         "Prescrição oficial do médico",
         "/riˈtʃɛtta/", "Receita médica (e também receita culinária de cozinha)."),

        ("febbre", "temperatura corporal elevada / febre", "A1",
         "Il bambino scotta: misura la temperatura con il termometro, ha la ___.", "febbre",
         "A criança está quente: meça a temperatura com o termômetro, ela está com febre.",
         "Estado febril",
         "/ˈfɛbbre/", "Ter febre: 'avere la febbre'."),

        ("antidolorifico", "remédio analgésico para dor", "A2",
         "Ha un forte mal di denti: ha bisogno di un ___ efficace.", "antidolorifico",
         "Ele está com forte dor de dente: precisa de um analgésico eficaz.",
         "Medicamento para aliviar dores",
         "/antidoloˈriːfiko/", "Remédio que combate a dor (dolore)."),

        ("sciroppo", "xarope líquido para tosse", "A1",
         "Per la tosse secca prenda un cucchiaio di questo ___ prima di dormire.", "sciroppo",
         "Para a tosse seca tome uma colher deste xarope antes de dormir.",
         "Medicamento líquido viscoso",
         "/ʃiˈrɔppo/", "Medicamento para a tosse: sciroppo per la tosse."),

        ("pastiglie", "pastilhas para garganta ou comprimidos", "A1",
         "Ho un forte bruciore alla gola: mi consiglia delle ___ lenitive?", "pastiglie",
         "Estou com forte queimação na garganta: você me recomenda pastilhas calmantes?",
         "Pastilhas de chupar ou comprimidos",
         "/pasˈtiʎʎe/", "Pastilhas de garganta: 'pastiglie per la gola'."),

        ("cerotto", "curativo adesivo / band-aid", "A1",
         "Mi sono tagliato un dito con la carta: mi metti un ___ per favore?", "cerotto",
         "Cortei um dedo com o papel: você coloca um curativo adesivo em mim por favor?",
         "Curativo adesivo",
         "/tʃeˈrɔtto/", "Band-aid ou adesivo de proteção para pequenos cortes."),

        ("raffreddore", "resfriado nasal comum", "A1",
         "Ho il naso chiuso e starnutisco in continuazione: ho preso un forte ___.", "raffreddore",
         "Estou com o nariz entupido e espirro sem parar: peguei um resfriado forte.",
         "Infecção viral leve das vias aéreas",
         "/raffredˈdoːre/", "Pegar um resfriado: 'prendere un raffreddore'."),

        ("mal di testa", "dor de cabeça / cefaleia", "A1",
         "Oggi non riesco a concentrarmi per colpa di questo fastidioso ___.", "mal di testa",
         "Hoje não consigo me concentrar por culpa desta incômoda dor de cabeça.",
         "Dor na cabeça",
         "/mal di ˈtɛsta/", "Expressão fixa: 'avere mal di testa'."),

        ("mal di pancia", "dor de barriga / estômago", "A1",
         "Dopo aver mangiato troppo gelato il bambino ha avuto un forte ___.", "mal di pancia",
         "Após ter comido muito sorvete a criança teve uma forte dor de barriga.",
         "Desconforto abdominal",
         "/mal di ˈpantʃa/", "Dor abdominal: mal di pancia."),

        ("dosi", "dosagem / posologia de um medicamento", "A2",
         "Legga attentamente il foglietto illustrativo per conoscere le ___ corrette.", "dosi",
         "Leia atentamente a bula para saber as dosagens corretas.",
         "Quantidade diária recomendada",
         "/ˈdɔːzi/", "Quantidade de tomada do remédio."),

        # --- 6. All'Hotel / Alloggio (10) ---
        ("camera singola", "quarto individual para uma pessoa", "A1",
         "Vorrei prenotare una ___ con bagno privato per tre notti.", "camera singola",
         "Gostaria de reservar um quarto individual com banheiro privativo por três noites.",
         "Acomodação de hotel para um hóspede",
         "/ˈkaːmera ˈsiŋɡola/", "Quarto para 1 pessoa = singola. Para 2 = doppia ou matrimoniale."),

        ("camera matrimoniale", "quarto de casal com cama ampla", "A1",
         "Siamo marito e moglie e preferiamo una ___ con letto grande.", "camera matrimoniale",
         "Somos marido e mulher e preferimos um quarto de casal com cama grande.",
         "Quarto com cama de casal",
         "/ˈkaːmera matrimoˈnjaːle/", "Cama de casal inteira chama-se 'letto matrimoniale'."),

        ("chiave", "chave da porta do quarto", "A1",
         "Ecco a Lei la ___ della camera numero duecentoquattro al secondo piano.", "chiave",
         "Aqui está para o senhor a chave do quarto número 204 no segundo andar.",
         "Instrumento de abertura da porta",
         "/ˈkjaːve/", "Pode ser física ou cartão magnético ('scheda magnetica')."),

        ("colazione inclusa", "café da manhã incluso na diária", "A1",
         "Il prezzo della camera è di cento euro a notte con la ___.", "colazione inclusa",
         "O preço do quarto é de cem euros por noite com o café da manhã incluso.",
         "Refeição matinal sem custo extra",
         "/kolatˈtsjoːne inˈkluːza/", "Refeição inclusa no preço."),

        ("check-out", "saída do hotel com encerramento da conta", "A1",
         "A che ora dobbiamo lasciare la camera per fare il ___ domani mattina?", "check-out",
         "A que horas devemos desocupar o quarto para fazer o check-out amanhã de manhã?",
         "Horário limite de saída do hotel",
         "/ˈtʃɛkawt/", "Termo internacional amplamente usado em toda a Itália para a saída do hotel."),

        ("aria condizionata", "ar-condicionado para refrigeração", "A1",
         "Fa molto caldo nella stanza: accendiamo l'___ per favore?", "aria condizionata",
         "Faz muito calor no quarto: ligamos o ar-condicionado por favor?",
         "Sistema de climatização",
         "/ˈaːrja kondittsjoˈnaːta/", "Aparelho de refrigeração de ar."),

        ("bagno privato", "banheiro privativo exclusivo", "A1",
         "Tutte le camere del nostro albergo dispongono di un ___ con doccia.", "bagno privato",
         "Todos os quartos do nosso hotel dispõem de um banheiro privativo com chuveiro.",
         "Banheiro não compartilhado",
         "/ˈbaɲɲo priˈvaːto/", "Banheiro dentro do próprio quarto."),

        ("ricezione", "recepção do hotel (ou portaria)", "A1",
         "Se avete bisogno di cuscini extra chiamate pure il numero nove della ___.", "ricezione",
         "Se vocês precisarem de travesseiros extras liguem para o número nove da recepção.",
         "Balcão de atendimento do hotel",
         "/ritʃetˈtsjoːne/", "Também chamado de 'reception' ou 'reception / portineria'."),

        ("deposito bagagli", "guarda-volumes para deixar as malas", "A1",
         "Possiamo lasciare le valigie nel vostro ___ dopo il check-out?", "deposito bagagli",
         "Podemos deixar as malas no seu guarda-volumes após o check-out?",
         "Local seguro para guardar malas temporariamente",
         "/deˈpɔːzito baˈɡaʎʎi/", "Serviço muito útil antes de ir para a estação."),

        ("ascensore", "elevador do prédio", "A1",
         "La Sua camera è al quarto piano: può prendere comodamente l'___ a destra.", "ascensore",
         "O seu quarto fica no quarto andar: pode pegar confortavelmente o elevador à direita.",
         "Equipamento de subida vertical",
         "/aʃʃenˈsoːre/", "Elevador mecânico."),

        # --- 7. Per Strada / Chiedere Indicazioni (10) ---
        ("giri a destra", "vire à direita (tratamento formal)", "A1",
         "All'incrocio con il semaforo ___ e prosegua per cento metri.", "giri a destra",
         "No cruzamento com o semáforo vire à direita e continue por cem metros.",
         "Instrução formal de direção para a direita",
         "/ˈdʒiːri a ˈdɛstra/", "Imperativo formal (Lei) de girare: 'giri a destra'."),

        ("giri a sinistra", "vire à esquerda (tratamento formal)", "A1",
         "Oltrepassi la piazza e poi ___ subito dopo la chiesa.", "giri a sinistra",
         "Passe a praça e depois vire à esquerda logo após a igreja.",
         "Instrução formal de direção para a esquerda",
         "/ˈdʒiːri a siˈnistra/", "Vire para o lado esquerdo."),

        ("vada dritto", "siga em frente / vá direto (tratamento formal)", "A1",
         "___ per questa strada finché non vede la fontana monumentale.", "Vada dritto",
         "Siga em frente por esta rua até enxergar a fonte monumental.",
         "Instrução formal de seguir em linha reta",
         "/ˈvaːda ˈdritto/", "Seguir sempre na mesma direção reta."),

        ("attraversi", "atravesse (tratamento formal)", "A1",
         "___ la strada sulle strisce pedonali per raggiungere il museo.", "Attraversi",
         "Atravesse a rua na faixa de pedestres para chegar ao museu.",
         "Cruzamento de rua formal",
         "/attraˈvɛrsi/", "Imperativo formal do verbo attraversare."),

        ("strisce pedonali", "faixa de pedestres de segurança", "A1",
         "Bisogna sempre attraversare la strada sulle ___ per sicurezza.", "strisce pedonali",
         "É preciso sempre atravessar a rua na faixa de pedestres por segurança.",
         "Pintura branca no chão para pedestres",
         "/ˈstriʃʃe pedoˈnaːli/", "Faixa zebrada pintada no asfalto."),

        ("semaforo", "semáforo / sinal de trânsito", "A1",
         "Fermati quando il ___ diventa rosso per evitare multe e pericoli.", "semaforo",
         "Pare quando o semáforo ficar vermelho para evitar multas e perigos.",
         "Sinal luminoso de trânsito",
         "/seˈmaːforo/", "Sinal de controle de tráfego de veículos."),

        ("incrocio", "cruzamento / encruzilhada de ruas", "A1",
         "La farmacia si trova esattamente all'___ tra Corso Roma e Via Garibaldi.", "incrocio",
         "A farmácia fica exatamente no cruzamento entre o Corso Roma e a Via Garibaldi.",
         "Ponto onde duas ruas se cruzam",
         "/inˈkrɔːtʃo/", "Interseção viária."),

        ("in fondo alla strada", "no fim da rua / ao término do caminho", "A1",
         "La stazione dei pullman si trova proprio ___ sulla sinistra.", "in fondo alla strada",
         "A estação de ônibus fica bem no fim da rua, à esquerda.",
         "Extremidade final de uma rua",
         "/in ˈfondo ˈalla ˈstraːda/", "Localização no término do percurso."),

        ("quanto dista", "a que distância fica / quanto dista", "A2",
         "Scusi, sa dirmi ___ il Colosseo da questa piazza a piedi?", "quanto dista",
         "Com licença, sabe me dizer a que distância fica o Coliseu desta praça a pé?",
         "Pergunta sobre distância métrica ou temporal",
         "/ˈkwanto ˈdista/", "Perguntar a distância: 'quanto dista da qui?'."),

        ("mi sono perso", "me perdi / estou desorientado", "A1",
         "Scusi, può aiutarmi? ___ e sto cercando la piazza centrale.", "Mi sono perso",
         "Com licença, pode me ajudar? Eu me perdi e estou procurando a praça central.",
         "Expressão para quando se está perdido no caminho",
         "/mi ˈsoːno ˈpɛrso/", "Perder-se em uma cidade nova: 'mi sono perso' (homem) / 'persa' (mulher)."),

        # --- 8. Nei Negozi / Shopping (10) ---
        ("taglia", "tamanho de roupa (calça, camisa, vestido)", "A1",
         "Che ___ porta di pantaloni? Una quarantadue o quarantaquattro?", "taglia",
         "Qual tamanho de calças você usa? Um 42 ou 44?",
         "Tamanho de vestuário",
         "/ˈtaʎʎa/", "Para roupas usa-se 'la taglia'. Para sapatos usa-se 'il numero'."),

        ("numero", "número de calçado / sapato", "A1",
         "Di scarpe porto il ___ quarantaquattro.", "numero",
         "De sapatos eu calço o número 44.",
         "Tamanho de calçado",
         "/ˈnuːmero/", "Para sapatos a pergunta é: 'Che numero porta?'."),

        ("camerino", "provador de roupas na loja", "A1",
         "Dov'è il ___ per provare questa camicia di lino?", "camerino",
         "Onde fica o provador para experimentar esta camisa de linho?",
         "Cabine individual de prova",
         "/kameˈriːno/", "Local de experimentar roupas na loja: 'camerino di prova'."),

        ("posso provare", "posso experimentar / provar?", "A1",
         "Questa giacca verde è stupenda: ___ prima di decidere?", "posso provarla",
         "Esta jaqueta verde é maravilhosa: posso experimentá-la antes de decidir?",
         "Pergunta de cortesia antes de comprar",
         "/ˈpɔsso proˈvaːrla/", "Pedir autorização para experimentar a peça."),

        ("sconto", "desconto no preço original", "A1",
         "Se pago subito in contanti c'è un piccolo ___ sul prezzo?", "sconto",
         "Se eu pagar na hora em dinheiro há um pequeno desconto no preço?",
         "Abatimento financeiro",
         "/ˈskonto/", "Redução de preço: 'fare uno sconto'."),

        ("saldi", "liquidação / queima de estoque de estação", "A1",
         "A gennaio e a luglio in Italia iniziano i grandi ___ invernali ed estivi.", "saldi",
         "Em janeiro e julho na Itália começam as grandes liquidações de inverno e verão.",
         "Período oficial de liquidação",
         "/ˈsaldi/", "Temporada de liquidações regulamentada por lei na Itália."),

        ("vetrina", "vitrine de loja para exibição", "A1",
         "Ho visto un vestito meraviglioso esposto nella ___ del negozio.", "vetrina",
         "Vi um vestido maravilhoso exposto na vitrine da loja.",
         "Expositor envidraçado",
         "/veˈtriːna/", "Vidraça onde se expõem produtos para o público da rua."),

        ("reparto", "seção / departamento de uma grande loja", "A2",
         "I vestiti per bambini si trovano al secondo piano nel ___ infanzia.", "reparto",
         "As roupas infantis ficam no segundo andar na seção infantil.",
         "Divisão de uma loja de departamentos",
         "/reˈparto/", "Setor específico de compras."),

        ("borsa della spesa", "sacola de compras reutilizável", "A1",
         "Ha portato una ___ con sé o desidera un sacchetto alla cassa?", "borsa della spesa",
         "O senhor trouxe uma sacola de compras consigo ou deseja uma sacolinha no caixa?",
         "Sacola para carregar produtos",
         "/ˈbɔrsa ˈdella ˈspeːza/", "Sacola de tecido ou plástico reutilizável."),

        ("garanzia", "garantia formal do produto adquirido", "A2",
         "Conservi lo scontrino fiscale: vale per due anni di ___ ufficiale.", "garanzia",
         "Guarde o cupom fiscal: vale por dois anos de garantia oficial.",
         "Termo de cobertura técnica",
         "/ɡaranˈtsiːa/", "Direito legal de reparo ou troca do produto."),

        # --- 9. Al Supermercato / Mercato (10) ---
        ("carrello", "carrinho de compras do supermercado", "A1",
         "Serve una moneta da un euro per sbloccare il ___ della spesa.", "carrello",
         "É necessária uma moeda de um euro para destravar o carrinho de compras.",
         "Carrinho com rodinhas para produtos",
         "/karˈrɛllo/", "Na Itália a maioria dos carrinhos exige uma moeda para ser liberado."),

        ("cestino", "cestinha de mão para poucas compras", "A1",
         "Devo comprare solo due cose, prendo un comodo ___ di plastica.", "cestino",
         "Preciso comprar apenas duas coisas, pego uma confortável cestinha de plástico.",
         "Cesta portátil de mão",
         "/tʃeˈstiːno/", "Cesta leve para poucas compras."),

        ("guanti monouso", "luvas descartáveis para pegar frutas e legumes", "A1",
         "È obbligatorio indossare i ___ prima di toccare la frutta nel reparto.", "guanti monouso",
         "É obrigatório colocar as luvas descartáveis antes de tocar nas frutas na seção.",
         "Regra rígida de higiene nos supermercados italianos",
         "/ˈɡwanti monoˈuːzo/", "Na Itália é estritamente obrigatório usar luvas plásticas para escolher frutas/legumes."),

        ("pesare", "pesar a fruta na balança", "A1",
         "Non dimenticare di ___ le mele e incollare l'etichetta con il prezzo!", "pesare",
         "Não se esqueça de pesar as maçãs e colar a etiqueta com o preço!",
         "Pesar e etiquetar antes de ir ao caixa",
         "/peˈzaːre/", "O próprio cliente deve pesar o saco de frutas e colocar a etiqueta com código de barras."),

        ("scadenza", "prazo de validade de um alimento perecível", "A2",
         "Controlla sempre la data di ___ stampata sulla confezione del latte.", "scadenza",
         "Verifique sempre a data de validade impressa na embalagem de leite.",
         "Limite de tempo para consumo",
         "/skaˈdɛntsa/", "Data limite de consumo: data di scadenza."),

        ("surgelati", "produtos congelados mantidos no freezer", "A1",
         "Il gelato e le verdure congelate si trovano nel banco dei ___.", "surgelati",
         "O sorvete e as verduras congeladas ficam no balcão de congelados.",
         "Setor de alimentos ultracongelados",
         "/surdʒeˈlaːti/", "Freezer de produtos congelados industrialmente."),

        ("prodotti tipici", "produtos alimentícios típicos e artesanais locais", "A1",
         "In questo mercato rionale si possono acquistare fantastici ___ regionali.", "prodotti tipici",
         "Neste mercado de bairro é possível comprar fantásticos produtos típicos regionais.",
         "Especialidades da culinária local",
         "/proˈdɔtti ˈtiːpitʃi/", "Queijos, vinhos e azeites com denominação de origem protegida."),

        ("al chilo", "por quilo de peso", "A1",
         "Quanto costano queste arance siciliane ___? — Due euro al chilo.", "al chilo",
         "Quanto custam estas laranjas sicilianas por quilo? — Dois euros por quilo.",
         "Preço cobrado pela unidade de peso quilograma",
         "/al ˈkiːlo/", "Venda por peso métrico."),

        ("etto", "cem gramas de peso (unidade cotidiana italiana)", "A1",
         "Mi dia per favore un ___ e mezzo di prosciutto crudo di Parma affettato sottile.", "etto",
         "Dê-me por favor 150 gramas de presunto cru de Parma fatiado fino.",
         "Medida de 100 gramas indispensável na Itália",
         "/ˈɛtto/", "1 etto = 100 gramas. 'Un etto e mezzo' = 150g. Indispensável para frios e queijos!"),

        ("cassa continua", "caixa de pagamento do supermercado", "A1",
         "C'è una fila abbastanza lunga alla ___ numero due.", "cassa",
         "Há uma fila bastante longa no caixa número dois.",
         "Ponto final de pagamento das compras",
         "/ˈkassa/", "Local onde se passa as compras na esteira e se efetua o pagamento."),

        # --- 10. Poste, Emergenze e Vita Sociale (10) ---
        ("spedire", "enviar uma carta ou pacote pelos correios", "A1",
         "Vado alle poste per ___ un pacco regalo alla mia famiglia.", "spedire",
         "Vou aos correios para enviar um pacote de presente para a minha família.",
         "Remeter encomenda ou correspondência",
         "/speˈdiːre/", "Verbo enviar por correio ou transportadora."),

        ("francobollo", "selo postal para postagem", "A1",
         "Mi serve un ___ per posta prioritaria per spedire questa cartolina.", "francobollo",
         "Preciso de um selo para correio prioritário para enviar este cartão-postal.",
         "Selo adesivo dos correios",
         "/frankoˈbɔllo/", "Selo postal oficial."),

        ("raccomandata", "carta registrada com aviso de recebimento", "A2",
         "I documenti ufficiali devono essere inviati tramite lettera ___ con ricevuta.", "raccomandata",
         "Os documentos oficiais devem ser enviados via carta registrada com comprovante.",
         "Modalidade segura de correio",
         "/rakkomandoˈtaːta/", "Correspondência formal de valor comprobatório legal."),

        ("soccorso", "socorro / primeiros socorros de urgência", "A1",
         "In caso di emergenza medica grave chiama subito il pronto ___!", "soccorso",
         "Em caso de emergência médica grave chame imediatamente o pronto-socorro!",
         "Atendimento emergencial de saúde",
         "/sokˈkorso/", "Pronto-Socorro: Pronto Soccorso (tel: 118 ou 112)."),

        ("chiamare il 112", "ligar para o número único de emergência europeu 112", "A1",
         "Per qualsiasi emergenza in Italia bisogna ___ con il cellulare.", "chiamare il 112",
         "Para qualquer emergência na Itália é preciso ligar para o 112 com o celular.",
         "Número único de polícia, ambulância e bombeiros",
         "/kjaˈmaːre il ˈtʃɛntoˈdoːditʃi/", "O número de emergência universal gratuito na União Europeia."),

        ("aiuto", "pedido de socorro / ajuda urgente", "A1",
         "Gridò forte: '___! Qualcuno mi aiuti, mi hanno rubato la borsa!'", "Aiuto",
         "Gritou forte: 'Socorro! Alguém me ajude, roubaram a minha bolsa!'",
         "Grito de socorro emergencial",
         "/aˈjuːto/", "Palavra direta para pedir auxílio em perigo."),

        ("denuncia", "boletim de ocorrência policial formal", "A2",
         "Dobbiamo andare dai Carabinieri per sporgere una ___ di furto.", "denuncia",
         "Devemos ir aos Carabinieri para registrar um boletim de ocorrência de furto.",
         "Queixa formal de crime",
         "/deˈnuntʃa/", "Registro formal de furto, perda de passaporte ou violência."),

        ("piacere", "prazer em conhecer (apresentação social)", "A1",
         "Ciao, mi chiamo Bruno! — Molto ___, io mi chiamo Marco!", "piacere",
         "Oi, meu nome é Bruno! — Muito prazer, eu me chamo Marco!",
         "Fórmula de cumprimento cordial entre desconhecidos",
         "/pjaˈtʃeːre/", "Saudação clássica de apresentação formal ou informal."),

        ("auguri", "felicitações / parabéns (aniversário, ano novo)", "A1",
         "Oggi è il tuo compleanno: tantissimi ___ di cuore!", "auguri",
         "Hoje é o seu aniversário: muitíssimos parabéns de coração!",
         "Desejo de felicidade em ocasiões comemorativas",
         "/awˈɡuːri/", "Usado para aniversário, Natal, Páscoa e festas: 'Tanti auguri!'."),

        ("buon viaggio", "boa viagem (votos de boa partida)", "A1",
         "State per partire per Roma: vi auguro di cuore un ___ e tanto divertimento!", "buon viaggio",
         "Vocês estão para partir para Roma: desejo-lhes de coração uma boa viagem e muita diversão!",
         "Votos de boa jornada a quem vai viajar",
         "/bwɔn ˈvjaddʒo/", "Expressão clássica de despedida para viajantes."),
    ]

    cards = []
    for idx, (it, pt, niv, fr, ver, tr_fr, dic, ipa, exp) in enumerate(raw[:100], 1):
        cards.append({
            "id": f"fc_sit_{idx:03d}",
            "deck": "situazioni_reali",
            "deck_nome": "Situações da Vida Real (Cloze)",
            "nivel": niv,
            "italiano": it,
            "portugues": pt,
            "categoria": "situazioni_reali",
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
