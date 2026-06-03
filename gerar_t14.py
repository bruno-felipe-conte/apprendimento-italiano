#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def w(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {
        "id": tid,
        "italiano": it,
        "portugues": pt,
        "genero": gen,
        "plural": pl,
        "exemplo": ex_it,
        "exemplo_pt": ex_pt,
        "categoria": cat,
        "dificuldade": "medio",
        "audio_ipa": ipa
    }

words_data = [
    # Colors
    ("rosso", "vermelho", "colori", "Il vestito rosso è bellissimo.", "O vestido vermelho é lindíssimo.", "/ˈrosso/", "m", "rossi"),
    ("blu", "azul", "colori", "Il cielo è molto blu oggi.", "O céu está muito azul hoje.", "/blu/", "m", "blu"),
    ("giallo", "amarelo", "colori", "Ho comprato un fiore giallo.", "Comprei uma flor amarela.", "/ˈdʒallo/", "m", "gialli"),
    ("verde", "verde", "colori", "L'erba del giardino è verde.", "A grama do jardim é verde.", "/ˈverde/", "m", "verdi"),
    ("arancione", "laranja", "colori", "Il tramonto era arancione.", "O pôr do sol era laranja.", "/aranˈtʃone/", "m", "arancioni"),
    ("viola", "roxo", "colori", "Ha scelto una camicia viola.", "Ele escolheu uma camisa roxa.", "/ˈvjɔla/", "m", "viola"),
    ("rosa", "rosa", "colori", "La stanza è dipinta di rosa.", "O quarto é pintado de rosa.", "/ˈrɔza/", "m", "rosa"),
    ("marrone", "marrom", "colori", "Ho un cane marrone chiaro.", "Tenho um cachorro marrom claro.", "/marˈrone/", "m", "marroni"),
    ("nero", "preto", "colori", "Il gatto nero dorme sul divano.", "O gato preto dorme no sofá.", "/ˈnero/", "m", "neri"),
    ("bianco", "branco", "colori", "La neve è di colore bianco.", "A neve é de cor branca.", "/ˈbjanko/", "m", "bianchi"),
    ("grigio", "cinza", "colori", "Oggi il cielo è grigio e triste.", "Hoje o céu está cinza e triste.", "/ˈɡridʒo/", "m", "grigi"),
    ("azzurro", "azul claro", "colori", "Ha gli occhi di un azzurro intenso.", "Ela tem olhos de um azul claro intenso.", "/adˈdzurro/", "m", "azzurri"),
    ("celeste", "azul celeste", "colori", "Ha comprato un abito celeste.", "Ele comprou um terno azul celeste.", "/tʃeˈlɛste/", "m", "celesti"),
    ("dorato", "dourado", "colori", "Indossa un orologio dorato.", "Ela usa um relógio dourado.", "/doˈrato/", "m", "dorati"),
    ("argentato", "prateado", "colori", "La macchina nuova è argentata.", "O carro novo é prateado.", "/ardʒenˈtato/", "m", "argentati"),
    ("biondo", "loiro", "colori", "Il bambino ha i capelli biondi.", "O menino tem cabelos loiros.", "/ˈbjondo/", "m", "biondi"),
    ("castano", "castanho", "colori", "Lei ha i capelli castani.", "Ela tem cabelos castanhos.", "/kasˈtano/", "m", "castani"),
    ("turchese", "turquesa", "colori", "L'acqua del mare è turchese.", "A água do mar é turquesa.", "/turˈkese/", "m", "turchesi"),
    ("beige", "bege", "colori", "Il cappotto beige è molto elegante.", "O casaco bege é muito elegante.", "/bɛʒ/", "m", "beige"),
    ("fucsia", "fúcsia", "colori", "Il fiore fucsia attira le api.", "A flor fúcsia atrai as abelhas.", "/ˈfuksja/", "m", "fucsia"),
    
    # Qualities
    ("chiaro", "claro", "qualità", "Il colore chiaro riflette la luce.", "A cor clara reflete a luz.", "/ˈkjaro/", "m", "chiari"),
    ("scuro", "escuro", "qualità", "Preferisco il blu scuro.", "Prefiro o azul escuro.", "/ˈskuro/", "m", "scuri"),
    ("lucido", "brilhante", "qualità", "Il pavimento lucido è scivoloso.", "O piso brilhante é escorregadio.", "/ˈlutʃido/", "m", "lucidi"),
    ("opaco", "opaco", "qualità", "Il vetro opaco garantisce privacy.", "O vidro opaco garante privacidade.", "/oˈpako/", "m", "opachi"),
    ("brillante", "cintilante", "qualità", "Ha un sorriso brillante.", "Ela tem um sorriso cintilante.", "/brilˈlante/", "m", "brillanti"),
    ("pallido", "pálido", "qualità", "Sembri un po' pallido oggi.", "Você parece um pouco pálido hoje.", "/ˈpallido/", "m", "pallidi"),
    ("vivace", "vivo", "qualità", "Usa colori molto vivaci nei suoi quadri.", "Ele usa cores muito vivas em seus quadros.", "/viˈvatʃe/", "m", "vivaci"),
    ("intenso", "intenso", "qualità", "Ha uno sguardo intenso.", "Ele tem um olhar intenso.", "/inˈtɛnso/", "m", "intensi"),
    ("trasparente", "transparente", "qualità", "L'acqua del lago è trasparente.", "A água do lago é transparente.", "/traspaˈrɛnte/", "m", "trasparenti"),
    ("traslucido", "translúcido", "qualità", "Il materiale traslucido fa passare la luce.", "O material translúcido deixa a luz passar.", "/trazˈlutʃido/", "m", "traslucidi"),
    ("torbido", "turvo", "qualità", "Il fiume è torbido dopo la pioggia.", "O rio está turvo depois da chuva.", "/ˈtorbido/", "m", "torbidi"),
    ("fosco", "sombrio", "qualità", "Il cielo fosco annuncia tempesta.", "O céu sombrio anuncia tempestade.", "/ˈfosko/", "m", "foschi"),
    ("nitido", "nítido", "qualità", "L'immagine sul televisore è molto nitida.", "A imagem na televisão é muito nítida.", "/ˈnitido/", "m", "nitidi"),
    ("sfocato", "desfocado", "qualità", "La foto purtroppo è uscita sfocata.", "A foto infelizmente saiu desfocada.", "/sfoˈkato/", "m", "sfocati"),
    ("luminoso", "luminoso", "qualità", "L'appartamento è grande e luminoso.", "O apartamento é grande e luminoso.", "/lumiˈnoso/", "m", "luminosi"),
    ("buio", "escuro", "qualità", "Fa paura camminare nel buio.", "Dá medo andar no escuro.", "/ˈbujo/", "m", "bui"),
    ("ombreggiato", "sombreado", "qualità", "Un giardino fresco e ombreggiato.", "Um jardim fresco e sombreado.", "/ombreidˈdʒato/", "m", "ombreggiati"),
    ("colorato", "colorido", "qualità", "Ha indossato un vestito colorato.", "Ela vestiu uma roupa colorida.", "/koloˈrato/", "m", "colorati"),
    ("scolorito", "desbotado", "qualità", "I vecchi jeans sono scoloriti.", "Os jeans velhos estão desbotados.", "/skoloˈrito/", "m", "scoloriti"),
    ("sbiadito", "desbotado", "qualità", "La foto nel quadro è sbiadita.", "A foto no quadro está desbotada.", "/zbjaˈdito/", "m", "sbiaditi"),
    ("abbagliante", "ofuscante", "qualità", "La luce del sole era abbagliante.", "A luz do sol era ofuscante.", "/abbaiˈʎante/", "m", "abbaglianti"),
    ("fluorescente", "fluorescente", "qualità", "Indossa un giubbotto fluorescente.", "Ele veste um colete fluorescente.", "/flworeʃˈʃɛnte/", "m", "fluorescenti"),
    ("pastello", "pastel", "qualità", "I colori pastello sono molto delicati.", "As cores pastel são muito delicadas.", "/pasˈtɛllo/", "m", "pastelli"),
    ("cromatico", "cromático", "qualità", "La scala cromatica in pittura.", "A escala cromática na pintura.", "/kroˈmatiko/", "m", "cromatici"),
    ("monocromatico", "monocromático", "qualità", "Il design monocromatico è elegante.", "O design monocromático é elegante.", "/monokroˈmatiko/", "m", "monocromatici"),
    ("variopinto", "multicolorido", "qualità", "Un uccello dalle piume variopinte.", "Um pássaro de penas multicoloridas.", "/varjoˈpinto/", "m", "variopinti"),
    ("macchiato", "manchato", "qualità", "Il tappeto è macchiato di vino.", "O tapete está manchado de vinho.", "/makˈkjato/", "m", "macchiati"),
    ("a righe", "listrado", "qualità", "Una camicia a righe blu e bianche.", "Uma camisa listrada de azul e branco.", "/a ˈriɡe/", None, None),
    ("a pois", "de bolinhas", "qualità", "Una gonna a pois anni cinquanta.", "Uma saia de bolinhas dos anos cinquenta.", "/a pwˈa/", None, None),
    ("a quadretti", "xadrez", "qualità", "Una tovaglia a quadretti rossi.", "Uma toalha de mesa xadrez vermelha.", "/a kwaˈdretti/", None, None),
    
    # Shapes & Visuals
    ("forma", "forma", "aspetto", "La scatola ha la forma di un cuore.", "A caixa tem a forma de um coração.", "/ˈforma/", "f", "forme"),
    ("aspetto", "aparência", "aspetto", "L'aspetto del palazzo è moderno.", "A aparência do prédio é moderna.", "/asˈpɛtto/", "m", "aspetti"),
    ("sfumatura", "nuance", "aspetto", "Questa pittura ha una sfumatura dorata.", "Esta pintura tem uma nuance dourada.", "/sfumaˈtura/", "f", "sfumature"),
    ("contrasto", "contraste", "aspetto", "Il contrasto tra bianco e nero.", "O contraste entre branco e preto.", "/konˈtrasto/", "m", "contrasti"),
    ("tono", "tom", "aspetto", "Un tono di blu molto rilassante.", "Um tom de azul muito relaxante.", "/ˈtɔno/", "m", "toni"),
    ("palette", "paleta", "aspetto", "La palette di colori autunnali.", "A paleta de cores outonais.", "/paˈlɛt/", "f", "palette"),
    ("riflesso", "reflexo", "aspetto", "Il riflesso della luna sul lago.", "O reflexo da lua no lago.", "/riˈflɛsso/", "m", "riflessi"),
    ("luce", "luz", "aspetto", "La luce entra dalla finestra.", "A luz entra pela janela.", "/ˈlutʃe/", "f", "luci"),
    ("ombra", "sombra", "aspetto", "Riposiamo all'ombra di un albero.", "Vamos descansar à sombra de uma árvore.", "/ˈombra/", "f", "ombre"),
    ("bagliore", "clarão", "aspetto", "Ho visto un bagliore nel cielo.", "Vi um clarão no céu.", "/baiˈʎore/", "m", "bagliori"),
    ("raggio", "raio", "aspetto", "Un raggio di sole scalda la stanza.", "Um raio de sol aquece o quarto.", "/ˈraddʒo/", "m", "raggi"),
    ("penombra", "penumbra", "aspetto", "Leggeva in penombra.", "Ele lia na penumbra.", "/peˈnombra/", "f", "penombre"),
    ("chiaroscuro", "claro-escuro", "aspetto", "L'effetto chiaroscuro nel dipinto.", "O efeito claro-escuro na pintura.", "/kjaroˈskuro/", "m", "chiaroscuri"),
    ("linea", "linha", "aspetto", "Traccia una linea retta sul foglio.", "Trace uma linha reta na folha.", "/ˈlinea/", "f", "linee"),
    ("contorno", "contorno", "aspetto", "Il contorno delle montagne al tramonto.", "O contorno das montanhas no pôr do sol.", "/konˈtorno/", "m", "contorni"),
    ("profilo", "perfil", "aspetto", "Mi piace il tuo profilo destro.", "Gosto do seu perfil direito.", "/proˈfilo/", "m", "profili"),
    ("superficie", "superfície", "aspetto", "La superficie dell'acqua è calma.", "A superfície da água está calma.", "/superˈfitʃe/", "f", "superfici"),
    ("profondità", "profundidade", "aspetto", "La piscina ha una profondità di due metri.", "A piscina tem uma profundidade de dois metros.", "/profondiˈta/", "f", "profondità"),
    ("prospettiva", "perspectiva", "aspetto", "Un disegno con una buona prospettiva.", "Um desenho com uma boa perspectiva.", "/prospetˈtiva/", "f", "prospettive"),
    ("dimensione", "dimensão", "aspetto", "Qual è la dimensione della scatola?", "Qual é a dimensão da caixa?", "/dimenˈsjone/", "f", "dimensioni"),
    ("grandezza", "tamanho", "aspetto", "La grandezza del problema è notevole.", "O tamanho do problema é notável.", "/ɡranˈdettsa/", "f", "grandezze"),
    ("altezza", "altura", "aspetto", "L'altezza della montagna è impressionante.", "A altura da montanha é impressionante.", "/alˈtettsa/", "f", "altezze"),
    ("larghezza", "largura", "aspetto", "La larghezza della porta.", "A largura da porta.", "/larˈɡettsa/", "f", "larghezze"),
    ("lunghezza", "comprimento", "aspetto", "La lunghezza del fiume Po.", "O comprimento do rio Pó.", "/lunˈɡettsa/", "f", "lunghezze"),
    ("spessore", "espessura", "aspetto", "Il muro ha uno spessore di mezzo metro.", "O muro tem uma espessura de meio metro.", "/spesˈsore/", "m", "spessori"),
    ("rotondo", "redondo", "aspetto", "Il tavolo rotondo in cucina.", "A mesa redonda na cozinha.", "/roˈtondo/", "m", "rotondi"),
    ("quadrato", "quadrado", "aspetto", "Il tappeto è quadrato.", "O tapete é quadrado.", "/kwaˈdrato/", "m", "quadrati"),
    ("triangolare", "triangular", "aspetto", "Un cartello stradale triangolare.", "Uma placa de trânsito triangular.", "/trianɡoˈlare/", "m", "triangolari"),
    ("rettangolare", "retangular", "aspetto", "La finestra è rettangolare.", "A janela é retangular.", "/rettanɡoˈlare/", "m", "rettangolari"),
    ("ovale", "oval", "aspetto", "Ha un viso ovale molto bello.", "Ela tem um rosto oval muito bonito.", "/oˈvale/", "m", "ovali"),
    
    # Verbs
    ("colorare", "colorir", "verbi", "I bambini amano colorare.", "As crianças adoram colorir.", "/koloˈrare/", None, None),
    ("dipingere", "pintar", "verbi", "Voglio dipingere la mia stanza.", "Quero pintar o meu quarto.", "/diˈpindʒere/", None, None),
    ("disegnare", "desenhar", "verbi", "Lui sa disegnare molto bene.", "Ele sabe desenhar muito bem.", "/dizeɲˈɲare/", None, None),
    ("illuminare", "iluminar", "verbi", "La lampada serve a illuminare.", "A lâmpada serve para iluminar.", "/illumiˈnare/", None, None),
    ("oscurare", "escurecer", "verbi", "Le nuvole oscurano il cielo.", "As nuvens escurecem o céu.", "/oskuˈrare/", None, None),
    ("brillare", "brilhar", "verbi", "Le stelle brillano di notte.", "As estrelas brilham de noite.", "/brilˈlare/", None, None),
    ("risplendere", "resplandecer", "verbi", "Il sole risplende alto.", "O sol resplandece alto.", "/riˈsplɛndere/", None, None),
    ("riflettere", "refletir", "verbi", "Lo specchio riflette l'immagine.", "O espelho reflete a imagem.", "/riˈflɛttere/", None, None),
    ("sfumare", "esfumaçar", "verbi", "Sfumare i colori per creare profondità.", "Esfumaçar as cores para criar profundidade.", "/sfuˈmare/", None, None),
    ("sbiadire", "desbotar", "verbi", "Il sole fa sbiadire i tessuti.", "O sol faz desbotar os tecidos.", "/zbjaˈdire/", None, None),
    ("macchiare", "manchar", "verbi", "Attento a non macchiare la camicia.", "Cuidado para não manchar a camisa.", "/makˈkjare/", None, None),
    ("osservare", "observar", "verbi", "Mi piace osservare le persone.", "Gosto de observar as pessoas.", "/osserˈvare/", None, None),
    ("guardare", "olhar", "verbi", "Guardare la televisione la sera.", "Olhar a televisão à noite.", "/ɡwarˈdare/", None, None),
    ("ammirare", "admirar", "verbi", "Tutti si fermano ad ammirare il quadro.", "Todos param para admirar o quadro.", "/ammiˈrare/", None, None),
    ("intravedere", "entrever", "verbi", "Riesco a intravedere la montagna.", "Consigo entrever a montanha.", "/intraveˈdere/", None, None),
    
    # Others
    ("vista", "visão", "ottica", "Ha una vista perfetta.", "Ele tem uma visão perfeita.", "/ˈvista/", "f", "viste"),
    ("visione", "visão", "ottica", "La sua visione del mondo è unica.", "A sua visão do mundo é única.", "/viˈzjone/", "f", "visioni"),
    ("sguardo", "olhar", "ottica", "Ha uno sguardo profondo.", "Tem um olhar profundo.", "/ˈzɡwardo/", "m", "sguardi"),
    ("occhiali", "óculos", "ottica", "Devo comprare occhiali nuovi.", "Preciso comprar óculos novos.", "/okˈkjali/", "m", "occhiali"),
    ("specchio", "espelho", "ottica", "Guardati allo specchio.", "Olhe-se no espelho.", "/ˈspɛkkjo/", "m", "specchi"),
    ("lente", "lente", "ottica", "La lente della macchina fotografica.", "A lente da câmera fotográfica.", "/ˈlɛnte/", "f", "lenti"),
    ("prisma", "prisma", "ottica", "La luce passa attraverso il prisma.", "A luz passa através do prisma.", "/ˈprizma/", "m", "prismi"),
    ("ottica", "ótica", "ottica", "Il negozio di ottica è chiuso.", "A loja de ótica está fechada.", "/ˈɔttika/", "f", "ottiche"),
    ("visibile", "visível", "ottica", "La luna è ben visibile oggi.", "A lua está bem visível hoje.", "/viˈzibile/", "m", "visibili"),
    ("invisibile", "invisível", "ottica", "Il vento è invisibile.", "O vento é invisível.", "/inviˈzibile/", "m", "invisibili"),
    ("cieco", "cego", "ottica", "Il cane guida aiuta l'uomo cieco.", "O cão-guia ajuda o homem cego.", "/ˈtʃɛko/", "m", "ciechi"),
    ("abbagliato", "ofuscado", "ottica", "Sono rimasto abbagliato dai fari.", "Fiquei ofuscado pelos faróis.", "/abbaiˈʎato/", "m", "abbagliati")
]

def salvar(templo_num, nome, citta, livello, palavras_raw):
    palavras = []
    for i, (it, pt, cat, ex_it, ex_pt, ipa, gen, pl) in enumerate(palavras_raw, 1):
        tid = f"t{templo_num}_{i:03d}"
        palavras.append(w(tid, it, pt, cat, ex_it, ex_pt, ipa, gen, pl))
        
    obj = {
        "templo": templo_num,
        "nome": nome,
        "cidade": citta,
        "nivel": livello,
        "palavras": palavras
    }
    
    # Save to data directory
    path = os.path.join(OUT, "data", f"templo-{templo_num}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"OK templo-{templo_num}.json -- {len(palavras)} palavras")

if __name__ == "__main__":
    salvar(14, "I Colori e le Qualità Visive", "Firenze", "A2", words_data)
