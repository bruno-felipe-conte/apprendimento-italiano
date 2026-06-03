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
    # Persone
    ("studente", "estudante", "persone", "Lo studente legge il libro.", "O estudante lê o livro.", "/stuˈdɛnte/", "m", "studenti"),
    ("studentessa", "estudante (feminino)", "persone", "La studentessa scrive gli appunti.", "A estudante escreve as anotações.", "/studenˈtessa/", "f", "studentesse"),
    ("professore", "professor", "persone", "Il professore spiega la lezione.", "O professor explica a lição.", "/profesˈsore/", "m", "professori"),
    ("professoressa", "professora", "persone", "La professoressa è molto severa.", "A professora é muito severa.", "/professoˈressa/", "f", "professoresse"),
    ("maestro", "professor (ensino fundamental)", "persone", "Il maestro insegna a leggere.", "O professor ensina a ler.", "/maˈɛstro/", "m", "maestri"),
    ("alunno", "aluno", "persone", "Ogni alunno ha un banco.", "Cada aluno tem uma carteira.", "/aˈlunno/", "m", "alunni"),
    ("preside", "diretor (escola)", "persone", "Il preside organizza la scuola.", "O diretor organiza a escola.", "/ˈprɛzide/", "m", "presidi"),
    ("rettore", "reitor", "persone", "Il rettore dell'università parla oggi.", "O reitor da universidade fala hoje.", "/retˈtore/", "m", "rettori"),
    ("compagno", "colega", "persone", "Lui è il mio compagno di classe.", "Ele é meu colega de classe.", "/komˈpaɲɲo/", "m", "compagni"),
    ("bidello", "zelador (escola)", "persone", "Il bidello suona la campanella.", "O zelador toca o sinal.", "/biˈdɛllo/", "m", "bidelli"),
    ("laureato", "formado", "persone", "Mio fratello è laureato in legge.", "Meu irmão é formado em direito.", "/laureˈato/", "m", "laureati"),
    ("matricola", "calouro", "persone", "Sono una matricola all'università.", "Sou um calouro na universidade.", "/maˈtrikola/", "f", "matricole"),

    # Luoghi
    ("scuola", "escola", "luoghi", "I bambini vanno a scuola.", "As crianças vão para a escola.", "/ˈskwɔla/", "f", "scuole"),
    ("università", "universidade", "luoghi", "L'università è molto grande.", "A universidade é muito grande.", "/univerziˈta/", "f", "università"),
    ("aula", "sala de aula", "luoghi", "L'aula è piena di studenti.", "A sala de aula está cheia de estudantes.", "/ˈaula/", "f", "aule"),
    ("classe", "classe", "luoghi", "La nostra classe è al primo piano.", "A nossa classe fica no primeiro andar.", "/ˈklasse/", "f", "classi"),
    ("biblioteca", "biblioteca", "luoghi", "Studio in biblioteca ogni giorno.", "Estudo na biblioteca todo dia.", "/bibljoˈtɛka/", "f", "biblioteche"),
    ("laboratorio", "laboratório", "luoghi", "Facciamo esperimenti nel laboratorio.", "Fazemos experiências no laboratório.", "/laboraˈtɔrjo/", "m", "laboratori"),
    ("palestra", "ginásio", "luoghi", "Facciamo ginnastica in palestra.", "Fazemos ginástica no ginásio.", "/paˈlɛstra/", "f", "palestre"),
    ("mensa", "refeitório", "luoghi", "Mangiamo tutti insieme in mensa.", "Comemos todos juntos no refeitório.", "/ˈmɛnsa/", "f", "mense"),
    ("corridoio", "corredor", "luoghi", "Non correre nel corridoio!", "Não corra no corredor!", "/korriˈdojo/", "m", "corridoi"),
    ("cortile", "pátio", "luoghi", "I bambini giocano nel cortile.", "As crianças brincam no pátio.", "/korˈtile/", "m", "cortili"),
    ("segreteria", "secretaria", "luoghi", "Devo andare in segreteria studenti.", "Preciso ir à secretaria de alunos.", "/seɡreteˈria/", "f", "segreterie"),
    ("asilo", "jardim de infância", "luoghi", "Mio figlio va ancora all'asilo.", "Meu filho ainda vai ao jardim de infância.", "/aˈzilo/", "m", "asili"),
    ("liceo", "ensino médio", "luoghi", "Frequento il liceo classico.", "Frequento o ensino médio clássico.", "/liˈtʃɛo/", "m", "licei"),
    ("istituto", "instituto", "luoghi", "Questo è un istituto tecnico.", "Este é um instituto técnico.", "/istiˈtuto/", "m", "istituti"),
    ("dipartimento", "departamento", "luoghi", "Il dipartimento di storia.", "O departamento de história.", "/dipartiˈmento/", "m", "dipartimenti"),
    ("campus", "campus", "luoghi", "Il campus universitario è verde.", "O campus universitário é verde.", "/ˈkampus/", "m", "campus"),
    ("facoltà", "faculdade", "luoghi", "La facoltà di medicina è difficile.", "A faculdade de medicina é difícil.", "/fakolˈta/", "f", "facoltà"),

    # Oggetti
    ("libro", "livro", "oggetti", "Ho letto un bel libro.", "Eu li um belo livro.", "/ˈlibro/", "m", "libri"),
    ("quaderno", "caderno", "oggetti", "Scrivi gli appunti sul quaderno.", "Escreva as anotações no caderno.", "/kwaˈdɛrno/", "m", "quaderni"),
    ("penna", "caneta", "oggetti", "La penna blu non scrive più.", "A caneta azul não escreve mais.", "/ˈpenna/", "f", "penne"),
    ("matita", "lápis", "oggetti", "Uso una matita per disegnare.", "Uso um lápis para desenhar.", "/maˈtita/", "f", "matite"),
    ("gomma", "borracha", "oggetti", "Ho cancellato l'errore con la gomma.", "Apaguei o erro com a borracha.", "/ˈɡomma/", "f", "gomme"),
    ("zaino", "mochila", "oggetti", "Il mio zaino è molto pesante.", "Minha mochila está muito pesada.", "/ˈdzajno/", "m", "zaini"),
    ("lavagna", "lousa", "oggetti", "Il professore scrive sulla lavagna.", "O professor escreve na lousa.", "/laˈvaɲɲa/", "f", "lavagne"),
    ("gesso", "giz", "oggetti", "Manca il gesso per scrivere.", "Falta o giz para escrever.", "/ˈdʒɛsso/", "m", "gessi"),
    ("banco", "carteira", "oggetti", "Siediti al tuo banco.", "Sente-se na sua carteira.", "/ˈbanko/", "m", "banchi"),
    ("sedia", "cadeira", "oggetti", "Questa sedia è scomoda.", "Esta cadeira é desconfortável.", "/ˈsɛdja/", "f", "sedie"),
    ("astuccio", "estojo", "oggetti", "Ho perso il mio astuccio.", "Perdi o meu estojo.", "/asˈtuttʃo/", "m", "astucci"),
    ("righello", "régua", "oggetti", "Usa il righello per fare una linea.", "Use a régua para fazer uma linha.", "/riˈɡɛllo/", "m", "righelli"),
    ("foglio", "folha", "oggetti", "Prendi un foglio di carta.", "Pegue uma folha de papel.", "/ˈfɔʎʎo/", "m", "fogli"),
    ("vocabolario", "vocabulário", "oggetti", "Cerca la parola sul vocabolario.", "Procure a palavra no vocabulário.", "/vokaboˈlarjo/", "m", "vocabolari"),
    ("dizionario", "dicionário", "oggetti", "Uso un dizionario bilingue.", "Uso um dicionário bilíngue.", "/ditsjoˈnarjo/", "m", "dizionari"),
    ("calcolatrice", "calculadora", "oggetti", "Non usare la calcolatrice all'esame.", "Não use a calculadora no exame.", "/kalkolaˈtritʃe/", "f", "calcolatrici"),
    ("mappa", "mapa", "oggetti", "Guardiamo la mappa del mondo.", "Vamos olhar o mapa do mundo.", "/ˈmappa/", "f", "mappe"),
    ("diario", "diário", "oggetti", "Scrivi i compiti sul diario.", "Escreva as tarefas no diário.", "/diˈarjo/", "m", "diari"),
    ("pennarello", "canetinha", "oggetti", "Ho un pennarello rosso.", "Tenho uma canetinha vermelha.", "/pennaˈrɛllo/", "m", "pennarelli"),
    ("evidenziatore", "marca-texto", "oggetti", "Usa l'evidenziatore giallo.", "Use o marca-texto amarelo.", "/evidentsjaˈtore/", "m", "evidenziatori"),
    ("compasso", "compasso", "oggetti", "Usa il compasso per fare un cerchio.", "Use o compasso para fazer um círculo.", "/komˈpasso/", "m", "compassi"),

    # Concetti
    ("materia", "matéria", "concetti", "Qual è la tua materia preferita?", "Qual é a sua matéria preferida?", "/maˈtɛrja/", "f", "materie"),
    ("corso", "curso", "concetti", "Frequento un corso di italiano.", "Frequento um curso de italiano.", "/ˈkorso/", "m", "corsi"),
    ("lezione", "aula (lição)", "concetti", "La lezione comincia alle nove.", "A aula começa às nove.", "/letˈtsjone/", "f", "lezioni"),
    ("esame", "exame", "concetti", "Ho un esame molto difficile.", "Tenho um exame muito difícil.", "/eˈzame/", "m", "esami"),
    ("voto", "nota", "concetti", "Ho preso un buon voto.", "Tirei uma boa nota.", "/ˈvoto/", "m", "voti"),
    ("compito", "tarefa", "concetti", "Hai fatto il compito di casa?", "Você fez a tarefa de casa?", "/ˈkompito/", "m", "compiti"),
    ("prova", "prova", "concetti", "Domani c'è una prova scritta.", "Amanhã tem uma prova escrita.", "/ˈprɔva/", "f", "prove"),
    ("interrogazione", "arguição oral", "concetti", "Ho un'interrogazione di storia.", "Tenho uma arguição oral de história.", "/interroɡatˈtsjone/", "f", "interrogazioni"),
    ("laurea", "formatura", "concetti", "Festeggiamo la sua laurea.", "Festejamos a sua formatura.", "/ˈlaurea/", "f", "lauree"),
    ("tesi", "tese", "concetti", "Sto scrivendo la mia tesi.", "Estou escrevendo a minha tese.", "/ˈtɛzi/", "f", "tesi"),
    ("diploma", "diploma", "concetti", "Ho finalmente preso il diploma.", "Finalmente peguei o diploma.", "/diˈplɔma/", "m", "diplomi"),
    ("borsa di studio", "bolsa de estudo", "concetti", "Ha vinto una borsa di studio.", "Ela ganhou uma bolsa de estudo.", "/ˈborsa di ˈstudjo/", "f", "borse di studio"),
    ("appunti", "anotações", "concetti", "Prendo appunti durante la lezione.", "Faço anotações durante a aula.", "/apˈpunti/", "m", "appunti"),
    ("errore", "erro", "concetti", "Ho fatto un errore nel test.", "Cometi um erro no teste.", "/erˈrore/", "m", "errori"),
    ("correzione", "correção", "concetti", "Il professore fa la correzione.", "O professor faz a correção.", "/korretˈtsjone/", "f", "correzioni"),
    ("semestre", "semestre", "concetti", "Il primo semestre finisce a gennaio.", "O primeiro semestre termina em janeiro.", "/seˈmɛstre/", "m", "semestri"),
    ("trimestre", "trimestre", "concetti", "Siamo nel secondo trimestre.", "Estamos no segundo trimestre.", "/triˈmɛstre/", "m", "trimestri"),
    ("pausa", "pausa", "concetti", "Facciamo una pausa di dieci minuti.", "Vamos fazer uma pausa de dez minutos.", "/ˈpauza/", "f", "pause"),
    ("ricreazione", "recreio", "concetti", "Giochiamo durante la ricreazione.", "Brincamos durante o recreio.", "/rikreatˈtsjone/", "f", "ricreazioni"),
    ("vacanza", "férias", "concetti", "Amo le vacanze estive.", "Amo as férias de verão.", "/vaˈkantsa/", "f", "vacanze"),
    ("master", "mestrado", "concetti", "Sta facendo un master a Milano.", "Ele está fazendo um mestrado em Milão.", "/ˈmaster/", "m", "master"),
    ("dottorato", "doutorado", "concetti", "Ha finito il suo dottorato.", "Ele terminou o seu doutorado.", "/dottoˈrato/", "m", "dottorati"),
    ("iscrizione", "matrícula", "concetti", "L'iscrizione è aperta.", "A matrícula está aberta.", "/iskritˈtsjone/", "f", "iscrizioni"),
    ("frequenza", "frequência", "concetti", "La frequenza è obbligatoria.", "A frequência é obrigatória.", "/freˈkwɛntsa/", "f", "frequenze"),
    ("appello", "chamada", "concetti", "Il maestro fa l'appello.", "O professor faz a chamada.", "/apˈpɛllo/", "m", "appelli"),
    ("sessione", "sessão", "concetti", "La sessione d'esami inizia oggi.", "A sessão de exames começa hoje.", "/sesˈsjone/", "f", "sessioni"),
    ("cattedra", "mesa do professor", "concetti", "Il professore siede in cattedra.", "O professor senta-se à mesa.", "/ˈkattedra/", "f", "cattedre"),

    # Verbi
    ("studiare", "estudar", "verbi", "Devo studiare per l'esame.", "Devo estudar para o exame.", "/stuˈdjare/", None, None),
    ("imparare", "aprender", "verbi", "Voglio imparare l'italiano.", "Quero aprender italiano.", "/impaˈrare/", None, None),
    ("insegnare", "ensinar", "verbi", "Lui insegna matematica.", "Ele ensina matemática.", "/inseɲˈɲare/", None, None),
    ("leggere", "ler", "verbi", "Mi piace leggere i romanzi.", "Gosto de ler os romances.", "/ˈlɛddʒere/", None, None),
    ("scrivere", "escrever", "verbi", "Devi scrivere un tema.", "Você deve escrever uma redação.", "/ˈskrivere/", None, None),
    ("ascoltare", "escutar", "verbi", "Ascolta bene il professore.", "Escute bem o professor.", "/askolˈtare/", None, None),
    ("ripetere", "repetir", "verbi", "Puoi ripetere la domanda?", "Você pode repetir a pergunta?", "/riˈpɛtere/", None, None),
    ("spiegare", "explicar", "verbi", "Puoi spiegare questo concetto?", "Pode explicar este conceito?", "/spjeˈɡare/", None, None),
    ("capire", "entender", "verbi", "Ora riesco a capire tutto.", "Agora consigo entender tudo.", "/kaˈpire/", None, None),
    ("domandare", "perguntar", "verbi", "Non aver paura di domandare.", "Não tenha medo de perguntar.", "/domanˈdare/", None, None),
    ("rispondere", "responder", "verbi", "Chi vuole rispondere?", "Quem quer responder?", "/riˈspondere/", None, None),
    ("bocciare", "reprovar", "verbi", "Il professore mi ha bocciato.", "O professor me reprovou.", "/botˈtʃare/", None, None),
    ("promuovere", "passar (de ano)", "verbi", "Sono stato promosso a pieni voti.", "Passei com nota máxima.", "/proˈmwɔvere/", None, None),
    ("laurearsi", "formar-se", "verbi", "Spero di laurearmi presto.", "Espero me formar logo.", "/laureˈarsi/", None, None),
    ("diplomarsi", "formar-se (ensino médio)", "verbi", "Si è diplomato lo scorso anno.", "Ele se formou no ano passado.", "/diploˈmarsi/", None, None),
    ("copiare", "copiar", "verbi", "Non copiare durante l'esame!", "Não copie durante o exame!", "/koˈpjare/", None, None),
    ("ripassare", "revisar", "verbi", "Devo ripassare gli appunti.", "Preciso revisar as anotações.", "/ripasˈsare/", None, None),
    ("cancellare", "apagar", "verbi", "Puoi cancellare la lavagna?", "Pode apagar a lousa?", "/kantʃelˈlare/", None, None),
    ("iscriversi", "matricular-se", "verbi", "Voglio iscrivermi al corso.", "Quero me matricular no curso.", "/iˈskriversi/", None, None),
    ("frequentare", "frequentar", "verbi", "Lui non frequenta mai le lezioni.", "Ele nunca frequenta as aulas.", "/frekwenˈtare/", None, None),
    ("superare", "passar (em prova)", "verbi", "Ho superato l'esame di fisica.", "Passei no exame de física.", "/supeˈrare/", None, None),
    ("fallire", "falhar", "verbi", "Temo di fallire il test.", "Temo falhar no teste.", "/falˈlire/", None, None),

    # Altro
    ("facile", "fácil", "altro", "Questo esercizio è facile.", "Este exercício é fácil.", "/ˈfatʃile/", "m", "facili"),
    ("difficile", "difícil", "altro", "La matematica è difficile.", "A matemática é difícil.", "/difˈfitʃile/", "m", "difficili"),
    ("presente", "presente", "altro", "Sono tutti presenti oggi.", "Estão todos presentes hoje.", "/preˈzɛnte/", "m", "presenti"),
    ("assente", "ausente", "altro", "Marco è assente oggi.", "Marco está ausente hoje.", "/asˈsɛnte/", "m", "assenti"),
    ("preparato", "preparado", "altro", "Mi sento molto preparato.", "Me sinto muito preparado.", "/prepaˈrato/", "m", "preparati"),
    ("attento", "atento", "altro", "Sii attento in classe.", "Seja atento na classe.", "/atˈtɛnto/", "m", "attenti"),
    ("distratto", "distraído", "altro", "Quel bambino è troppo distratto.", "Aquele menino é distraído demais.", "/diˈstratto/", "m", "distratti"),
    ("elementare", "elementar", "altro", "La scuola elementare.", "A escola elementar.", "/elemenˈtare/", "f", "elementari"),
    ("superiore", "superior", "altro", "L'istruzione superiore.", "A instrução superior.", "/supeˈrjore/", "f", "superiori"),
    ("accademico", "acadêmico", "altro", "L'anno accademico inizia a settembre.", "O ano acadêmico começa em setembro.", "/akkaˈdɛmiko/", "m", "accademici"),
    ("severo", "severo", "altro", "Il professore è severo ma giusto.", "O professor é severo mas justo.", "/seˈvɛro/", "m", "severi")
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
    
    path = os.path.join(OUT, "data", f"templo-{templo_num}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"OK templo-{templo_num}.json -- {len(palavras)} palavras")

if __name__ == "__main__":
    salvar(18, "La Scuola e l'Università", "Napoli", "A2", words_data)
