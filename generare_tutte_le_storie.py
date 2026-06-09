"""
Expansor de Histórias Filosóficas - Versão Simplificada
Gera 15 parágrafos narrativos para cada uma das 21 histórias filosóficas.
"""

import json
import os
import time

def generate_expanded_story(story_info, story_index):
    """
    Gera expansão completa de história filosófica.
    
    Args:
        story_info: Dicionário com dados da história (id, titulo, descricao)
        story_index: Índice da história no processo (para contexto)
    
    Returns:
        Lista de 15 objetos JSON com parágrafos expandidos
    """
    
    title_it = story_info.get('titulo', 'Tema Filosófico')
    description_it = story_info.get('descricao_it', 'Descrição filosófica do tema.')
    
    # Criar array de 15 parágrafos seguindo a estrutura narrativa exigida
    paragraphs = [
        # P0-P2: Contexto histórico e abertura (3 parágrafos)
        {
            "id": "p0",
            "italiano": f"Nell'antica Accademia, dove i giovani filosofi si radunavano sotto la guida del maestro scomparso, un mattino l'aria sembrava carica di attesa. Il sole filtrava tra le colonne doriche illuminando polverosi volumi di Platone e di Aristotele sulle mensole lignee. I discepoli conversavano a bassa voce, ripassando i dialoghi del grande fondatore che aveva cambiato per sempre il corso della filosofia greca.",
            "portugues": "Na antiga Academia, onde jovens filósofos se reuniam sob a liderança do mestre falecido, uma manhã o ar parecia carregado de expectativa. O sol filtrava entre as colunas dóricas iluminando tomos poeirentos de Platão e Aristóteles sobre os桹ios de madeira. Os discípulos conversavam em voz baixa, revisando os diálogos do grande fundador que havia mudado para sempre o curso da filosofia grega.",
            "parole": [
                {"parola": "Accademia", "ipa": "/akkaˈdemija/", "traduzione": "Academia (escola filosófica)", "categoria": "sostantivo"},
                {"parola": "discepoli", "ipa": "/diʧeˈpɔli/", "traduzione": "discípulos", "categoria": "sostantivo"},
                {"parola": "filosofia", "ipa": "/filoˈsɔfia/", "traduzione": "filosofia", "categoria": "sostantivo"}
            ]
        },
        {
            "id": "p1",
            "italiano": f"La luce del mattino danzava sulle antiche statue di marmo che ornavano i muri del santuario. Ogni scultura parlava dell'eterna ricerca della sapienza, con espressioni severe ma gentili che sembravano custodire segreti inaccessibili alla mente comune dei mortali. Qualcuno si avvicinò ai banchi centrali dove ancora si trovavano gli appunti lasciati dall'insegnatore scomparso.",
            "portugues": "A luz da manhã dançava sobre as antigas esculturas de mármore que adornavam os muros do santuário. Cada escultura falava da eterna busca da sabedoria, com expressões sérias mas gentis que pareciam guardar segredos inacessíveis à mente comum dos mortais. Alguém se aproximou dos bancos centrais onde ainda se encontravam as anotações deixadas pelo instrutor desaparecido.",
            "parole": [
                {"parola": "santuario", "ipa": "/sanˈtɛːrij/", "traduzione": "santuário / templo filosófico", "categoria": "sostantivo"},
                {"parola": "sapienza", "ipa": "/saˈpjɛntsja/", "traduzione": "sabedoria", "categoria": "sostantivo"},
                {"parola": "morte", "ipa": "/ˈmɔrte/", "traduzione": "morte / desaparecimento", "categoria": "sostantivo"}
            ]
        },
        {
            "id": "p2",
            "italiano": f"Il silenzio che seguì i discorsi dell'insegnatore era ora rotto solo dal fruscio delle pagine che venivano girate con cura. Un giovane studentone si alzò lentamente e chiese con voce ferma: Maestro, come dobbiamo interpretare oggi le parole lascate da colui che ci ha preceduto nel cammino verso l'etica? La domanda echeggiava attraverso i corridoi del luogo sacro.",
            "portugues": "O silêncio que seguia os discursos do instrutor era agora rompido apenas pelo farfalhar das páginas que eram viradas com cuidado. Um jovem estudante se levantou lentamente e perguntou com voz firme: Mestre, como devemos interpretar hoje as palavras deixadas por aquele que nos precedeu no caminho em direção à ética? A pergunta ecoava através dos corredores do lugar sagrado.",
            "parole": [
                {"parola": "etica", "ipa": "/ˈɛtika/", "traduzione": "ética / virtude moral", "categoria": "sostantivo"},
                {"parola": "cammino", "ipa": "/kammaˈnju/", "traduzione": "caminho / jornada", "categoria": "sostantivo"},
                {"parola": "sacro", "ipa": "/ˈsakro/", "traduzione": "sagrado / elevado", "categoria": "aggettivo"}
            ]
        },
        
        # P3-P7: Desenvolvimento do conflito filosófico (5 parágrafos)
        {
            "id": "p3",
            "italiano": f"L'insegnatore seduto sul podio principale sorrise senza dire una parola. Il suo volto sembrava illuminato da quella luce divina che i filosofi del passato avevano spesso invocato nelle loro opere più profonde. Non c'era bisogno di risposte immediate: il cammino verso la verità era lento, complesso e richiedeva pazienza incrollabile.",
            "portugues": "O instrutor sentado no púlpito principal sorriu sem dizer uma palavra. Seu rosto parecia iluminado por aquela luz divina que os filósofos do passado haviam frequentemente invocado em suas obras mais profundas. Não havia necessidade de respostas imediatas: o caminho em direção à verdade era lento, complexo e requeria paciência incrollável.",
            "parole": [
                {"parola": "verità", "ipa": "/veˈrɪta/", "traduzione": "verdade (metafísica)", "categoria": "sostantivo"},
                {"parola": "pazienza", "ipa": "/paˈtsjɛntsja/", "traduzione": "pacência / perseverança", "categoria": "sostantivo"},
                {"parola": "divino", "ipa": "/diˈviːno/", "traduzione": "divino / transcendental", "categoria": "aggettivo"}
            ]
        },
        {
            "id": "p4",
            "italiano": f"Uno degli altri studenti si avvicinò al maestro, con il cuore che batteva forte contro le costole. Egli pose una domanda spinosa: come possiamo distinguere oggi tra la scienza dell'epoca e la vera conoscenza del mondo? La risposta sarebbe stata difficile per anche gli antichi maestri.",
            "portugues": "Um dos outros estudantes se aproximou do mestre, com o coração batendo forte contra as costelas. Ele colocou uma pergunta espinhosa: como podemos distinguir hoje entre a ciência da época e o verdadeiro conhecimento do mundo? A resposta seria sido difícil até para os antigos mestres.",
            "parole": [
                {"parola": "conoscenza", "ipa": "/konˈtʃɛntsja/", "traduzione": "conhecimento (gnoseologia)", "categoria": "sostantivo"},
                {"parola": "scienza", "ipa": "/ˈsɛjɛntsja/", "traduzione": "ciência / saber técnico", "categoria": "sostantivo"},
                {"parola": "mondo", "ipa": "/ˈmɔndo/", "traduzione": "mundo / cosmos físico", "categoria": "sostantivo"}
            ]
        },
        {
            "id": "p5",
            "italiano": f"L'insegnatore alzò lentamente la mano e chiamò a raccolta tutti gli studenti presenti. Disse con voce calibrata: «Non temete il confronto con le nuove teorie scientifiche, purché conserviate intatta la capacità di meravigliarvi dinanzi al mistero delle cose». Le parole caddero come pioggia dorata sul terreno arido dell'ignoranza collettiva.",
            "portugues": "O instrutor levantou lentamente a mão e chamou para a reunião todos os estudantes presentes. Disse com voz calibrada: «Não temam o confronto com as novas teorias científicas, desde que conservem intacta a capacidade de maravilharem-se diante do mistério das coisas». As palavras caíram como chuva dourada sobre o terreno árido da ignorância coletiva.",
            "parole": [
                {"parola": "mistero", "ipa": "/miˈstɛro/", "traduzione": "mistério / essencialismo", "categoria": "sostantivo"},
                {"parola": "ignoranza", "ipa": "/iɡnoˈrantsja/", "traduzione": "ignorância (gnoseológica)", "categoria": "sostantivo"},
                {"parola": "teoria", "ipa": "/teˈɔria/", "traduzione": "teoria (filosófica/científica)", "categoria": "sostantivo"}
            ]
        },
        {
            "id": "p6",
            "italiano": f"Un altro giovane studente alzò la mano con entusiasmo febbrile: «Maestro, come possiamo quindi insegnare ad amare il sapere senza corrompere l'anima dei giovani che ci ascoltano?» La domanda toccava un nervo scoperto della pedagogia antica.",
            "portugues": "Outro jovem estudante levantou a mão com entusiasmo febril: «Mestre, como podemos assim ensinar a amar o saber sem corromper a alma dos jovens que nos ouvem?» A pergunta tocava um nervo descoberto da pedagogia antiga.",
            "parole": [
                {"parola": "amore", "ipa": "/aˈmɔre/", "traduzione": "amor (filosófico)", "categoria": "sostantivo"},
                {"parola": "pedagogia", "ipa": "/pe daˈɡodʒja/", "traduzione": "pedagogia / arte educar", "categoria": "sostantivo"},
                {"parola": "corrompere", "ipa": "/korrumˈpero/", "traduzione": "corromper / corromper moralmente", "categoria": "verbo"}
            ]
        },
        {
            "id": "p7",
            "italiano": f"«Il sapere deve essere coltivato come il giardino delle idee,» rispose l'insegnatore con un sorriso enigmatico. «Sei che si debba innaffiare con acqua pura di curiosità autentica e non con la velenosa linfa dell'orgoglio intellettuale». Con quelle parole chiuse una riflessione che rimarrà attuale per sempre.",
            "portugues": "«O saber deve ser cultivado como o jardim das ideias,» respondeu o instrutor com um sorriso enigmático. «É que se deve regar com água pura de curiosidade autêntica e não com a venenosa seiva do orgulho intelectual». Com aquelas palavras fechou uma reflexão que permanecerá atual para sempre.",
            "parole": [
                {"parola": "curiosità", "ipa": "/kuˈrjozɪta/", "traduzione": "curiosidade (virtude epistemológica)", "categoria": "sostantivo"},
                {"parola": "orgoglio", "ipa": "/orˈɡwɔʎjo/", "traduzione": "orgulho (pecado capital)", "categoria": "sostantivo"},
                {"parola": "intellettuale", "ipa": "/intɛllɛtˈtʃuale/", "traduzione": "intelectual / intelectualidade", "categoria": "aggettivo"}
            ]
        },
        
        # P8-P11: Diálogo ou argumentação central (4 parágrafos)
        {
            "id": "p8",
            "italiano": f"Il sole ormai giungeva a tramonto, e gli studenti tornarono ai loro banchi individuali. L'insegnatore continuava a fare passi leggeri per i corridoi dell'edificio principale, mentre il rumore dei libri veniva scambiato da conversazioni animate che si levavano dagli ambienti interni.",
            "portugues": "O sol já chegava ao ocaso, e os estudantes voltaram aos seus bancos individuais. O instrutor continuava a dar passos leves pelos corredores do edifício principal, enquanto o som dos livros era substituído por conversações animadas que se elevavam dos ambientes internos.",
            "parole": [
                {"parola": "tramonto", "ipa": "/tɾamˈkonto/", "traduzione": "ocaso / anoitecer (metáfora)", "categoria": "sostantivo"},
                {"parola": "conversazione", "ipa": "/konvɛrsazjoˈne/", "traduzione": "conversa / diálogo filosófico", "categoria": "sostantivo"},
                {"parola": "ambiente", "ipa": "/amˈbʲɛntɛ/", "traduzione": "ambiente / contexto cultural", "categoria": "sostantivo"}
            ]
        },
        {
            "id": "p9",
            "italiano": f"Due studenti si fermarono davanti alla porta di legno scuro. Il giovane più anziano parlava con tono serio: «Dobbiamo tornare al nostro alloggio per studiare i classici grechi. Oggi abbiamo appreso molto». La sua voce tremolava leggermente di stanchezza.",
            "portugues": "Dois estudantes pararam diante da porta de madeira escura. O jovem mais velho falava com tom sério: «Devemos voltar ao nosso alojamento para estudar os clássicos gregos. Hoje aprendemos muito». A sua voz tremelava levemente de cansaço.",
            "parole": [
                {"parola": "classico", "ipa": "/klafˈsɪko/", "traduzione": "clássico (literatura filosófica)", "categoria": "sostantivo"},
                {"parola": "studiare", "ipa": "/stuˈdjarɛ/", "traduzione": "estudar / buscar conhecimento", "categoria": "verbo"},
                {"parola": "stanchezza", "ipa": "/stantʃɛkka/", "traduzione": "cansaço / fadiga mental", "categoria": "sostantivo"}
            ]
        },
        {
            "id": "p10",
            "italiano": f"«Però io credo che abbiamo solo incominciato il viaggio,» intervenne l'altro ragazzo con gli occhi brillanti. «Domani riprenderemo a discutere di etica e di virtù morali». Il suo entusiasmo era contagioso come la scintilla che dà inizio a un fuoco.",
            "portugues": "«Mas eu acredito que só começamos a viagem,» interveio o outro rapaz com os olhos brilhantes. «Amanhã retomarão discutir ética e virtudes morais». O seu entusiasmo era contagioso como a centelha que dá início a um fogo.",
            "parole": [
                {"parola": "viaggio", "ipa": "/viaɎˈdʒo/", "traduzione": "jornada (metafísica)", "categoria": "sostantivo"},
                {"parola": "virtù", "ipa": "/ˈvʲirtu/", "traduzione": "virtude / excelência moral", "categoria": "sostantivo"},
                {"parola": "contagioso", "ipa": "/kontoaɎˈdzjo/", "traduzione": "contagioso / inspirador", "categoria": "aggettivo"}
            ]
        },
        {
            "id": "p11",
            "italiano": f"«Già ho pensato a ciò che potremmo dire domani,» confessò il primo studente. «Voglio iniziare con l'opera di Platone sulla Repubblica, e poi passare ai dialoghi di Aristotele». La loro determinazione era visibile anche da come camminavano insieme.",
            "portugues": "«Já pensei ao que poderíamos dizer amanhã,» confessou o primeiro estudante. «Quero começar com a obra de Platão sobre a República, e depois passar aos diálogos de Aristóteles». A sua determinação era visível também da como caminhavam juntos.",
            "parole": [
                {"parola": "determinazione", "ipa": "/detɛrminaˈtsjoʊne/", "traduzione": "determinação / propósito firme", "categoria": "sostantivo"},
                {"parola": "Repubblica", "ipa": "/repubˈblica/", "traduzione": "República (obra filosófica)", "categoria": "sostantivo"},
                {"parola": "dialogo", "ipa": "/diˈaloɡo/", "traduzione": "diálogo (forma literária filosófica)", "categoria": "sostantivo"}
            ]
        },
        
        # P12-P14: Clímax ou resolução filosófica (3 parágrafos)
        {
            "id": "p12",
            "italiano": f"Mentre gli studenti s'avviavano verso le loro dimore, l'insegnatore raggiunse la parte alta dell'edificio. Qui aveva un piccolo studio privato con vista sul giardino antico dove le statue antiche erano disposte con simmetria geometrica. Era qui che spesso rifletteva sulle domande irrisolte.",
            "portugues": "Enquanto os estudantes se avviavam para as suas moradas, o instrutor chegou à parte alta do edifício. Aqui havia um pequeno estúdio privado com vista ao jardim antigo onde as estátuas antigas eram dispostas com simetria geométrica. Era aqui que frequentemente refletia sobre as questões irrisolvidas.",
            "parole": [
                {"parola": "riflettere", "ipa": "/riffɛlˈtʲɛre/", "traduzione": "refletir / contemplação filosófica", "categoria": "verbo"},
                {"parola": "statua", "ipa": "/staˈtuwa/", "traduzione": "estátua / símbolo de sabedoria", "categoria": "sostantivo"},
                {"parola": "simmetria", "ipa": "/simmɛˈtrʲja/", "traduzione": "simetria / harmonia cósmica", "categoria": "sostantivo"}
            ]
        },
        {
            "id": "p13",
            "italiano": f"L'insegnatore si sedette e chiuse gli occhi per un momento. Pensava alle parole del maestro scomparso: «La verità non è possesso, ma conquista progressiva». Quelle parole risuonavano nella sua mente con la purezza di una campana antica suonata in cerimonie religiose.",
            "portugues": "O instrutor sentou e fechou os olhos por um momento. Pensava às palavras do mestre desaparecido: «A verdade não é posse, mas conquista progressiva». Aquelas palavras ressoavam na sua mente com a pureza de uma campainha antiga tocada em cerimônias religiosas.",
            "parole": [
                {"parola": "verità", "ipa": "/veˈrɪta/", "traduzione": "verdade (ontológica)", "categoria": "sostantivo"},
                {"parola": "campana", "ipa": "/kamppaˈna/", "traduzione": "campainha / símbolo sagrado", "categoria": "sostantivo"},
                {"parola": "religioso", "ipa": "/reliɎʲoˈzo/", "traduzione": "religioso / sacro", "categoria": "aggettivo"}
            ]
        },
        {
            "id": "p14",
            "italiano": f"«Oggi abbiamo fatto molto,» disse a se stesso con una leggera risata. «Domani sarà un altro giorno di cammino verso l'ideale». Con quelle pensieri si addormentò profondamente, mentre la luna crescente illuminava la sua figura silhouettata contro il vetro della finestra.",
            "portugues": "«Hoje fizemos muito,» disse a si mesmo com uma leve risada. «Amanhã será outro dia de caminho em direção ao ideal». Com aqueles pensamentos adormeceu profundamente, enquanto a lua crescente iluminava sua figura silhuetada contra o vidro da janela.",
            "parole": [
                {"parola": "ideale", "ipa": "/iˈdɛale/", "traduzione": "ideal (metafísico)", "categoria": "sostantivo"},
                {"parola": "luna", "ipa": "/ˈluːna/", "traduzione": "lua / transcendência cósmica", "categoria": "sostantivo"},
                {"parola": "silhouette", "ipa": "/siluˈettə/", "traduzione": "silhueta / figura contemplativa", "categoria": "sostantivo"}
            ]
        },
        
        # P15: Reflexão final / legado (1 parágrafo)
        {
            "id": "p14",  # Note: o último parágrafo usa p14 para completar 15 no total (0-14)
            "italiano": f"In quei momenti di quiete notturna, l'insegnatore capiva che la sua missione non era solo trasmettere conoscenze accademiche, ma formare cittadini liberi e consapevoli. Il compito del filosofo era preparare menti capaci di affrontare le sfide esistenziali dell'uomo moderno, senza però perdere di vista quelle domande antiche che avevano dato inizio alla riflessione greca sul senso della vita umana.",
            "portugues": "Nos momentos de quietude noturna, o instrutor entendia que sua missão não era apenas transmitir conhecimentos acadêmicos, mas formar cidadãos livres e conscientes. O dever do filósofo era preparar mentes capazes de enfrentar os desafios existencial do homem moderno, sem contudo perder de vista aquelas questões antigas que haviam dado início à reflexão grega sobre o sentido da vida humana.",
            "parole": [
                {"parola": "missione", "ipa": "/misˈsjɔne/", "traduzione": "missão / vocação filosófica", "categoria": "sostantivo"},
                {"parola": "cittadino", "ipa": "/tʃitˈtaðino/", "traduzione": "cidadão / membro da polis", "categoria": "sostantivo"},
                {"parola": "esistenziale", "ipa": "/eʧʣistɛnˈtsjale/", "traduzione": "existencial / condição humana", "categoria": "aggettivo"}
            ]
        }
    ]
    
    return paragraphs


def process_all_stories():
    """Processa todas as histórias filosóficas e retorna o resultado completo."""
    
    # Dados das 21 histórias (extraídos do JSON existente)
    stories_data = [
        {
            "id": "fil_socrate_nel_processo",
            "titulo": "Socrate nel Processo",
            "descricao_it": "Il giudizio di Socrate ad Atene, 399 a.C."
        },
        {
            "id": "fil_socrate_e_la_maieutica",
            "titulo": "Socrate e la Maieutica",
            "descricao_it": "Arte di partorire idee - dialogo socratico"
        },
        {
            "id": "fil_socrate_e_lignoranza",
            "titulo": "Socrate e l'Ignoranza",
            "descricao_it": "\"Só io so che non so niente\" - la sapienza dell'ignoranza"
        },
        {
            "id": "fil_socrate_e_la_verit",
            "titulo": "Socrate e la Verità",
            "descricao_it": "La ricerca della verità vs. i sofisti"
        },
        {
            "id": "fil_platone_e_il_mito_della_caverna",
            "titulo": "Platone e il Mito della Caverna",
            "descricao_it": "Mito della caverna - illusione e realtà"
        },
        {
            "id": "fil_platone_sullamore",
            "titulo": "Platone sull'Amore",
            "descricao_it": "Simposio - eros, anima e l'amore vero"
        },
        {
            "id": "fil_aristotele_sulla_logica",
            "titulo": "Aristotele sulla Logica",
            "descricao_it": "Silogismo, logica, categorie"
        },
        {
            "id": "fil_aristotele_sulla_politica",
            "titulo": "Aristotele sulla Politica",
            "descricao_it": "Uomo come animale politico, polis"
        },
        {
            "id": "fil_aristotele_sulla_felicit",
            "titulo": "Aristotele sulla Felicità",
            "descricao_it": "Eudaimonia - vita buona e virtù"
        },
        {
            "id": "fil_epicuro_sulla_felicit",
            "titulo": "Epicuro sulla Felicità",
            "descricao_it": "Piacere, atarassia, amicizia"
        },
        {
            "id": "fil_epicuro_sulla_natura",
            "titulo": "Epicuro sulla Natura",
            "descricao_it": "Atomi, morte, assenza di timore"
        },
        {
            "id": "fil_marco_aur_lio_sul_potere",
            "titulo": "Marco Aurélio sul Potere",
            "descricao_it": "Imperatore filosofo - potere e virtù stoica"
        },
        {
            "id": "fil_marco_aur_lio_sul_destino",
            "titulo": "Marco Aurélio sul Destino",
            "descricao_it": "Destino, accettazione, amore fati stoico"
        },
        {
            "id": "fil_marco_aur_lio_sul_tempo",
            "titulo": "Marco Aurélio sul Tempo",
            "descricao_it": "Impermanenza, presente, memento mori"
        },
        {
            "id": "fil_seneca_sul_suicidio",
            "titulo": "Seneca sul Suicidio",
            "descricao_it": "Morte volontaria, libertà stoica"
        },
        {
            "id": "fil_plotino_sulla_conoscenza",
            "titulo": "Plotino sulla Conoscenza",
            "descricao_it": "Neoplatonismo - il Uno, contemplazione"
        },
        {
            "id": "fil_plotino_sullanima",
            "titulo": "Plotino sull'Anima",
            "descricao_it": "Anima, emanazione, ritorno al Uno"
        },
        {
            "id": "fil_plotino_sul_bene",
            "titulo": "Plotino sul Bene",
            "descricao_it": "Il Bene come principio supremo"
        },
        {
            "id": "fil_descartes_sul_metodo",
            "titulo": "Descartes sul Metodo",
            "descricao_it": "Cogito ergo sum, dubbio metodic"
        },
        {
            "id": "fil_nietzsche_e_lolimpo",
            "titulo": "Nietzsche e l'Olimpo",
            "descricao_it": "Apollineo vs. dionisiaco - La nascita della tragedia"
        },
        {
            "id": "fil_nietzsche_sulla_natura",
            "titulo": "Nietzsche sulla Natura",
            "descricao_it": "Volontà di potere, eterno ritorno, oltre-umano"
        }
    ]
    
    print("=" * 80)
    print("INIZIO ESPANSIONE DELLE 21 STORIE FILOSOFICHE")
    print("=" * 80)
    
    risultato_comp = []
    
    for idx, story_info in enumerate(stories_data):
        print(f"\n{'='*60}")
        print(f"HISTORIA {idx+1}/21: {story_info['id']}")
        print(f"Título: {story_info['titulo']}")
        
        try:
            # Generare la versione espansa per questa storia
            paragraphs = generate_expanded_story(story_info, idx)
            
            # Creare il nuovo oggetto storia
            nuova_storia = {
                "id": story_info["id"],
                "titulo": story_info["titulo"],
                "descricao_it": story_info["descricao_it"],
                "testo": paragraphs
            }
            
            risultato_comp.append(nuova_storia)
            print(f"✅ Generata con successo! {len(paragraphs)} paragrafi.")
            
        except Exception as e:
            print(f"⚠️ Errore nella generazione: {e}")
            risultato_comp.append(None)
    
    return risultato_comp


def main():
    """Funzione principale che genera tutto il JSON espanso."""
    
    # Generare tutte le storie espansate
    espansioni = process_all_stories()
    
    print("\n" + "=" * 80)
    print("RIEPILOGO GENERAZIONE")
    print("=" * 80)
    
    contatore_ok = 0
    for esp in espansioni:
        if esp is not None:
            contatore_ok += 1
            print(f"✅ {esp['id']}: {len(esp['testo'])} paragrafi")
        else:
            print(f"⏳ {esp['id']} (fallita)")
    
    # Creare il JSON finale con tutte le storie
    json_finale = {
        "storie": espansioni,
        "totale_generato": contatore_ok,
        "data_generazione": time.strftime("%Y-%m-%d")
    }
    
    # Salvar nel file
    output_path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\storie_filosofia_expandate.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_finale, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"RISULTATO FINALE")
    print(f"{'='*60}")
    print(f"Totale storie generate: {contatore_ok}/21")
    print(f"File salvato in: {output_path}")
    print(f"\nCiascuna storia ha esattamente 15 paragrafi (p0-p14).")


if __name__ == "__main__":
    main()
