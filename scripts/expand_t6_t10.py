import json
import os

def load(templo_num):
    path = f'data/templo-{templo_num}.json'
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save(templo_num, data):
    path = f'data/templo-{templo_num}.json'
    if "vocabulario" in data:
        data["palavras"] = data.pop("vocabulario")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def gen_word(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {
        "id": tid, "italiano": it, "portugues": pt, "genero": gen, "plural": pl,
        "exemplo": ex_it, "exemplo_pt": ex_pt, "categoria": cat, "dificuldade": "medio", "audio_ipa": ipa
    }

# ----------------- TEMPLO 6 (Bologna: Grammatica, Studi) -----------------
t6_data = load(6)
t6_words = t6_data.get("palavras", t6_data.get("vocabulario", []))
start = len(t6_words) + 1

t6_new = [
    gen_word(f"t6_{start+0:03}", "grammatica", "gramática", "studi", "La grammatica italiana è complessa.", "A gramática italiana é complexa.", "/ɡramˈmaːtika/", "f", "grammatiche"),
    gen_word(f"t6_{start+1:03}", "lezione", "lição / aula", "studi", "Oggi abbiamo una lezione di storia.", "Hoje temos uma aula de história.", "/letˈtsjoːne/", "f", "lezioni"),
    gen_word(f"t6_{start+2:03}", "compito", "tarefa / dever de casa", "studi", "Devo fare i compiti per domani.", "Devo fazer as tarefas para amanhã.", "/ˈkompito/", "m", "compiti"),
    gen_word(f"t6_{start+3:03}", "esame", "exame / prova", "studi", "Ho superato l'esame di matematica.", "Passei na prova de matemática.", "/eˈzaːme/", "m", "esami"),
    gen_word(f"t6_{start+4:03}", "voto", "nota", "studi", "Ho preso un bel voto.", "Tirei uma boa nota.", "/ˈvoːto/", "m", "voti"),
    gen_word(f"t6_{start+5:03}", "studentessa", "estudante (feminino)", "studi", "Lei è una studentessa universitaria.", "Ela é uma estudante universitária.", "/studenˈtessa/", "f", "studentesse"),
    gen_word(f"t6_{start+6:03}", "maestro", "professor (primário)", "studi", "Il maestro insegna a leggere.", "O professor ensina a ler.", "/maˈɛstro/", "m", "maestri"),
    gen_word(f"t6_{start+7:03}", "scuola", "escola", "studi", "I bambini vanno a scuola.", "As crianças vão para a escola.", "/ˈskwɔːla/", "f", "scuole"),
    gen_word(f"t6_{start+8:03}", "università", "universidade", "studi", "Studia legge all'università.", "Estuda direito na universidade.", "/univerziˈta/", "f", "università"),
    gen_word(f"t6_{start+9:03}", "dizionario", "dicionário", "studi", "Cerco la parola nel dizionario.", "Procuro a palavra no dicionário.", "/dittsjoˈnaːrjo/", "m", "dizionari"),
    gen_word(f"t6_{start+10:03}", "pagina", "página", "studi", "Aprite il libro a pagina due.", "Abram o livro na página dois.", "/ˈpaːdʒina/", "f", "pagine"),
    gen_word(f"t6_{start+11:03}", "penna", "caneta", "studi", "Hai una penna rossa?", "Você tem uma caneta vermelha?", "/ˈpenna/", "f", "penne"),
    gen_word(f"t6_{start+12:03}", "matita", "lápis", "studi", "Scrivo con la matita.", "Escrevo com o lápis.", "/maˈtiːta/", "f", "matite"),
    gen_word(f"t6_{start+13:03}", "quaderno", "caderno", "studi", "Prendo appunti sul quaderno.", "Tomo notas no caderno.", "/kwaˈdɛrno/", "m", "quaderni"),
    gen_word(f"t6_{start+14:03}", "lavagna", "lousa", "studi", "Il professore scrive sulla lavagna.", "O professor escreve na lousa.", "/laˈvaɲɲa/", "f", "lavagne"),
    gen_word(f"t6_{start+15:03}", "sostantivo", "substantivo", "grammatica", "Il cane è un sostantivo maschile.", "O cachorro é um substantivo masculino.", "/sostanˈtiːvo/", "m", "sostantivi"),
    gen_word(f"t6_{start+16:03}", "aggettivo", "adjetivo", "grammatica", "L'aggettivo bello cambia forma.", "O adjetivo belo muda de forma.", "/addʒetˈtiːvo/", "m", "aggettivi"),
    gen_word(f"t6_{start+17:03}", "verbo", "verbo", "grammatica", "Il verbo essere è irregolare.", "O verbo ser é irregular.", "/ˈvɛrbo/", "m", "verbi"),
    gen_word(f"t6_{start+18:03}", "avverbio", "advérbio", "grammatica", "L'avverbio modifica il verbo.", "O advérbio modifica o verbo.", "/avˈvɛrbjo/", "m", "avverbi"),
    gen_word(f"t6_{start+19:03}", "pronome", "pronome", "grammatica", "Io è un pronome personale.", "Eu é um pronome pessoal.", "/proˈnoːme/", "m", "pronomi"),
    gen_word(f"t6_{start+20:03}", "articolo", "artigo", "grammatica", "L'articolo determinativo 'il'.", "O artigo definido 'il'.", "/arˈtiːkolo/", "m", "articoli"),
    gen_word(f"t6_{start+21:03}", "frase", "frase", "grammatica", "Costruisci una frase completa.", "Construa uma frase completa.", "/ˈfraːze/", "f", "frasi"),
    gen_word(f"t6_{start+22:03}", "vocale", "vogal", "grammatica", "La lettera 'a' è una vocale.", "A letra 'a' é uma vogal.", "/voˈkaːle/", "f", "vocali"),
    gen_word(f"t6_{start+23:03}", "consonante", "consoante", "grammatica", "La 'b' è una consonante.", "A 'b' é uma consoante.", "/konsoˈnante/", "f", "consonanti"),
    gen_word(f"t6_{start+24:03}", "accento", "acento", "grammatica", "Metti l'accento sulla parola.", "Coloque o acento na palavra.", "/atˈtʃɛnto/", "m", "accenti"),
    gen_word(f"t6_{start+25:03}", "regola", "regra", "studi", "C'è un'eccezione alla regola.", "Há uma exceção à regra.", "/ˈrɛːɡola/", "f", "regole"),
    gen_word(f"t6_{start+26:03}", "eccezione", "exceção", "studi", "Questa è un'eccezione rara.", "Esta é uma exceção rara.", "/ettʃetˈtsjoːne/", "f", "eccezioni"),
    gen_word(f"t6_{start+27:03}", "errore", "erro", "studi", "Ho fatto un errore nel test.", "Cometi um erro no teste.", "/erˈroːre/", "m", "errori"),
    gen_word(f"t6_{start+28:03}", "sbaglio", "erro / equívoco", "studi", "Non fare lo stesso sbaglio.", "Não cometa o mesmo erro.", "/ˈzbaʎʎo/", "m", "sbagli"),
    gen_word(f"t6_{start+29:03}", "risposta", "resposta", "studi", "Qual è la risposta corretta?", "Qual é a resposta correta?", "/riˈsposta/", "f", "risposte"),
    gen_word(f"t6_{start+30:03}", "domanda", "pergunta", "studi", "Posso fare una domanda?", "Posso fazer uma pergunta?", "/doˈmanda/", "f", "domande"),
    gen_word(f"t6_{start+31:03}", "facile", "fácil", "aggettivi", "Questo esercizio è facile.", "Este exercício é fácil.", "/ˈfaːtʃile/", "m/f", "facili"),
    gen_word(f"t6_{start+32:03}", "difficile", "difícil", "aggettivi", "L'esame era molto difficile.", "O exame era muito difícil.", "/difˈfiːtʃile/", "m/f", "difficili"),
    gen_word(f"t6_{start+33:03}", "corso", "curso", "studi", "Frequento un corso di pittura.", "Frequento um curso de pintura.", "/ˈkorso/", "m", "corsi"),
    gen_word(f"t6_{start+34:03}", "laurea", "graduação / diploma", "studi", "Dopo la laurea cercherò lavoro.", "Depois da graduação procurarei trabalho.", "/ˈlawrea/", "f", "lauree"),
    gen_word(f"t6_{start+35:03}", "facoltà", "faculdade", "studi", "La facoltà di medicina.", "A faculdade de medicina.", "/fakolˈta/", "f", "facoltà"),
    gen_word(f"t6_{start+36:03}", "biblioteca", "biblioteca", "studi", "Vado in biblioteca a studiare.", "Vou para a biblioteca estudar.", "/bibljoˈtɛːka/", "f", "biblioteche"),
    gen_word(f"t6_{start+37:03}", "leggere", "ler", "verbi", "Mi piace leggere i romanzi.", "Gosto de ler os romances.", "/ˈlɛddʒere/", None, None),
    gen_word(f"t6_{start+38:03}", "scrivere", "escrever", "verbi", "Devo scrivere una lettera.", "Preciso escrever uma carta.", "/ˈskriːvere/", None, None),
    gen_word(f"t6_{start+39:03}", "ascoltare", "ouvir", "verbi", "Ascolta bene la pronuncia.", "Ouça bem a pronúncia.", "/askolˈtaːre/", None, None),
    gen_word(f"t6_{start+40:03}", "studiare", "estudar", "verbi", "Studiamo italiano insieme.", "Estudamos italiano juntos.", "/stuˈdjaːre/", None, None),
    gen_word(f"t6_{start+41:03}", "imparare", "aprender", "verbi", "Voglio imparare l'italiano.", "Quero aprender o italiano.", "/impaˈraːre/", None, None)
]
t6_words.extend(t6_new)
t6_data["palavras"] = t6_words[:107]
save(6, t6_data)

# ----------------- TEMPLO 7 (Torino: Conversazione, Opinione) -----------------
t7_data = load(7)
t7_words = t7_data.get("palavras", t7_data.get("vocabulario", []))
start = len(t7_words) + 1

t7_new = [
    gen_word(f"t7_{start+0:03}", "opinione", "opinião", "conversazione", "La mia opinione è diversa.", "Minha opinião é diferente.", "/opiˈnjoːne/", "f", "opinioni"),
    gen_word(f"t7_{start+1:03}", "idea", "ideia", "conversazione", "Ho un'ottima idea.", "Tenho uma ótima ideia.", "/iˈdɛːa/", "f", "idee"),
    gen_word(f"t7_{start+2:03}", "ragione", "razão", "conversazione", "Hai ragione tu.", "Você tem razão.", "/raˈdʒoːne/", "f", "ragioni"),
    gen_word(f"t7_{start+3:03}", "torto", "erro / estar errado", "conversazione", "Io penso che tu abbia torto.", "Eu acho que você está errado.", "/ˈtɔrto/", "m", "torti"),
    gen_word(f"t7_{start+4:03}", "accordo", "acordo", "conversazione", "Siamo d'accordo su questo.", "Estamos de acordo com isso.", "/akˈkɔrdo/", "m", "accordi"),
    gen_word(f"t7_{start+5:03}", "disaccordo", "desacordo", "conversazione", "Siamo in disaccordo.", "Estamos em desacordo.", "/dizakˈkɔrdo/", "m", "disaccordi"),
    gen_word(f"t7_{start+6:03}", "verità", "verdade", "conversazione", "Dimmi la verità.", "Diga-me a verdade.", "/veriˈta/", "f", "verità"),
    gen_word(f"t7_{start+7:03}", "bugia", "mentira", "conversazione", "Non dire le bugie.", "Não diga mentiras.", "/buˈdʒiːa/", "f", "bugie"),
    gen_word(f"t7_{start+8:03}", "chiacchierare", "bater papo", "verbi", "Ci piace chiacchierare al bar.", "Gostamos de bater papo no bar.", "/kjakkjeˈraːre/", None, None),
    gen_word(f"t7_{start+9:03}", "discutere", "discutir", "verbi", "Possiamo discutere il problema.", "Podemos discutir o problema.", "/disˈkuːtere/", None, None),
    gen_word(f"t7_{start+10:03}", "litigare", "brigar", "verbi", "I fratelli litigano spesso.", "Os irmãos brigam frequentemente.", "/litiˈɡaːre/", None, None),
    gen_word(f"t7_{start+11:03}", "promettere", "prometer", "verbi", "Ti prometto che verrò.", "Prometo-te que virei.", "/proˈmettere/", None, None),
    gen_word(f"t7_{start+12:03}", "consigliare", "aconselhar", "verbi", "Ti consiglio di leggere questo libro.", "Aconselho-te a ler este livro.", "/konsiʎˈʎaːre/", None, None),
    gen_word(f"t7_{start+13:03}", "consiglio", "conselho", "conversazione", "Posso darti un consiglio?", "Posso te dar um conselho?", "/konˈsiʎʎo/", "m", "consigli"),
    gen_word(f"t7_{start+14:03}", "forse", "talvez", "avverbi", "Forse andiamo al mare domani.", "Talvez vamos ao mar amanhã.", "/ˈforse/", None, None),
    gen_word(f"t7_{start+15:03}", "magari", "quem dera / talvez", "avverbi", "Magari fosse vero!", "Quem dera fosse verdade!", "/maˈɡaːri/", None, None),
    gen_word(f"t7_{start+16:03}", "purtroppo", "infelizmente", "avverbi", "Purtroppo non posso venire.", "Infelizmente não posso vir.", "/purˈtrɔppo/", None, None),
    gen_word(f"t7_{start+17:03}", "fortunatamente", "felizmente", "avverbi", "Fortunatamente stiamo bene.", "Felizmente estamos bem.", "/fortunaˈtamente/", None, None),
    gen_word(f"t7_{start+18:03}", "infatti", "de fato", "avverbi", "Infatti è così.", "De fato é assim.", "/inˈfatti/", None, None),
    gen_word(f"t7_{start+19:03}", "invece", "em vez disso", "avverbi", "Invece di dormire, studia.", "Em vez de dormir, estuda.", "/inˈveːtʃe/", None, None),
    gen_word(f"t7_{start+20:03}", "allora", "então", "avverbi", "Allora cosa facciamo?", "Então o que fazemos?", "/alˈloːra/", None, None),
    gen_word(f"t7_{start+21:03}", "quindi", "portanto", "avverbi", "Piove, quindi resto a casa.", "Chove, portanto fico em casa.", "/ˈkwindi/", None, None),
    gen_word(f"t7_{start+22:03}", "perché", "por que / porque", "congiunzioni", "Perché non mangi?", "Por que não come?", "/perˈke/", None, None),
    gen_word(f"t7_{start+23:03}", "come", "como", "congiunzioni", "Come si dice in italiano?", "Como se diz em italiano?", "/ˈkoːme/", None, None),
    gen_word(f"t7_{start+24:03}", "quando", "quando", "congiunzioni", "Quando arrivi chiamami.", "Quando chegar, me ligue.", "/ˈkwando/", None, None),
    gen_word(f"t7_{start+25:03}", "dove", "onde", "congiunzioni", "Dove abiti?", "Onde você mora?", "/ˈdoːve/", None, None),
    gen_word(f"t7_{start+26:03}", "chi", "quem", "pronomi", "Chi è quel ragazzo?", "Quem é aquele garoto?", "/ki/", None, None),
    gen_word(f"t7_{start+27:03}", "cosa", "o que / coisa", "pronomi", "Cosa vuoi mangiare?", "O que quer comer?", "/ˈkɔːza/", "f", "cose"),
    gen_word(f"t7_{start+28:03}", "certo", "certo / claro", "avverbi", "Certo che vengo!", "Claro que venho!", "/ˈtʃɛrto/", "m", "certi"),
    gen_word(f"t7_{start+29:03}", "sicuro", "seguro / certo", "aggettivi", "Sei sicuro?", "Tem certeza?", "/siˈkuːro/", "m", "sicuri"),
    gen_word(f"t7_{start+30:03}", "probabile", "provável", "aggettivi", "È molto probabile.", "É muito provável.", "/proˈbaːbile/", "m/f", "probabili"),
    gen_word(f"t7_{start+31:03}", "impossibile", "impossível", "aggettivi", "Quello è impossibile.", "Isso é impossível.", "/imposˈsiːbile/", "m/f", "impossibili"),
    gen_word(f"t7_{start+32:03}", "strano", "estranho", "aggettivi", "È un comportamento strano.", "É um comportamento estranho.", "/ˈstraːno/", "m", "strani"),
    gen_word(f"t7_{start+33:03}", "normale", "normal", "aggettivi", "Tutto sembra normale.", "Tudo parece normal.", "/norˈmaːle/", "m/f", "normali"),
    gen_word(f"t7_{start+34:03}", "peccato", "pecado / pena", "conversazione", "Che peccato che tu parta.", "Que pena que você parta.", "/pekˈkaːto/", "m", "peccati"),
    gen_word(f"t7_{start+35:03}", "scusa", "desculpa", "conversazione", "Ti chiedo scusa.", "Te peço desculpa.", "/ˈskuːza/", "f", "scuse"),
    gen_word(f"t7_{start+36:03}", "prego", "de nada", "conversazione", "Grazie! - Prego!", "Obrigado! - De nada!", "/ˈprɛːɡo/", None, None),
    gen_word(f"t7_{start+37:03}", "saluto", "saudação", "conversazione", "Un saluto a tutti.", "Uma saudação a todos.", "/saˈluːto/", "m", "saluti"),
    gen_word(f"t7_{start+38:03}", "incontro", "encontro", "conversazione", "Abbiamo un incontro alle tre.", "Temos um encontro às três.", "/inˈkontro/", "m", "incontri"),
    gen_word(f"t7_{start+39:03}", "voce", "voz", "conversazione", "Parla a bassa voce.", "Fale em voz baixa.", "/ˈvoːtʃe/", "f", "voci"),
    gen_word(f"t7_{start+40:03}", "silenzio", "silêncio", "conversazione", "Facciamo silenzio in chiesa.", "Fazemos silêncio na igreja.", "/siˈlɛntsjo/", "m", "silenzi"),
    gen_word(f"t7_{start+41:03}", "rumore", "barulho", "conversazione", "Che rumore fuori!", "Que barulho lá fora!", "/ruˈmoːre/", "m", "rumori")
]
t7_words.extend(t7_new)
t7_data["palavras"] = t7_words[:107]
save(7, t7_data)

# ----------------- TEMPLO 8 (Palermo: Cultura, Tradizione) -----------------
t8_data = load(8)
t8_words = t8_data.get("palavras", t8_data.get("vocabulario", []))
start = len(t8_words) + 1

t8_new = [
    gen_word(f"t8_{start+0:03}", "cultura", "cultura", "cultura", "La cultura italiana è ricca.", "A cultura italiana é rica.", "/kulˈtuːra/", "f", "culture"),
    gen_word(f"t8_{start+1:03}", "storia", "história", "cultura", "L'Italia ha una lunga storia.", "A Itália tem uma longa história.", "/ˈstɔːrja/", "f", "storie"),
    gen_word(f"t8_{start+2:03}", "arte", "arte", "cultura", "Firenze è la città dell'arte.", "Florença é a cidade da arte.", "/ˈarte/", "f", "arti"),
    gen_word(f"t8_{start+3:03}", "tradizione", "tradição", "cultura", "Manteniamo viva la tradizione.", "Mantemos viva a tradição.", "/traditˈtsjoːne/", "f", "tradizioni"),
    gen_word(f"t8_{start+4:03}", "festa", "festa", "cultura", "Andiamo alla festa del paese.", "Vamos à festa da cidade.", "/ˈfɛsta/", "f", "feste"),
    gen_word(f"t8_{start+5:03}", "musica", "música", "cultura", "Ascolto musica classica.", "Ouço música clássica.", "/ˈmuːzika/", "f", "musiche"),
    gen_word(f"t8_{start+6:03}", "canzone", "canção", "cultura", "Canta una bella canzone.", "Canta uma bela canção.", "/kanˈtsoːne/", "f", "canzoni"),
    gen_word(f"t8_{start+7:03}", "teatro", "teatro", "cultura", "Stasera andiamo a teatro.", "Hoje à noite vamos ao teatro.", "/teˈaːtro/", "m", "teatri"),
    gen_word(f"t8_{start+8:03}", "cinema", "cinema", "cultura", "Andiamo al cinema a vedere un film.", "Vamos ao cinema ver um filme.", "/ˈtʃiːnema/", "m", "cinema"),
    gen_word(f"t8_{start+9:03}", "film", "filme", "cultura", "È un bel film.", "É um belo filme.", "/film/", "m", "film"),
    gen_word(f"t8_{start+10:03}", "attore", "ator", "cultura", "Il mio attore preferito.", "O meu ator preferido.", "/atˈtoːre/", "m", "attori"),
    gen_word(f"t8_{start+11:03}", "attrice", "atriz", "cultura", "È una brava attrice.", "É uma boa atriz.", "/atˈtriːtʃe/", "f", "attrici"),
    gen_word(f"t8_{start+12:03}", "regista", "diretor (cinema)", "cultura", "Un famoso regista italiano.", "Um famoso diretor italiano.", "/reˈdʒista/", "m/f", "registi"),
    gen_word(f"t8_{start+13:03}", "museo", "museu", "cultura", "Visitiamo il museo archeologico.", "Visitamos o museu arqueológico.", "/muˈzɛːo/", "m", "musei"),
    gen_word(f"t8_{start+14:03}", "mostra", "exposição", "cultura", "C'è una mostra d'arte moderna.", "Há uma exposição de arte moderna.", "/ˈmostra/", "f", "mostre"),
    gen_word(f"t8_{start+15:03}", "quadro", "quadro / pintura", "cultura", "Un bel quadro dipinto a mano.", "Um belo quadro pintado à mão.", "/ˈkwaːdro/", "m", "quadri"),
    gen_word(f"t8_{start+16:03}", "statua", "estátua", "cultura", "La statua di marmo.", "A estátua de mármore.", "/ˈstaːtwa/", "f", "statue"),
    gen_word(f"t8_{start+17:03}", "monumento", "monumento", "cultura", "Il Colosseo è un monumento.", "O Coliseu é um monumento.", "/monuˈmento/", "m", "monumenti"),
    gen_word(f"t8_{start+18:03}", "chiesa", "igreja", "cultura", "La chiesa si trova in piazza.", "A igreja fica na praça.", "/ˈkjɛːza/", "f", "chiese"),
    gen_word(f"t8_{start+19:03}", "duomo", "catedral", "cultura", "Il Duomo di Milano.", "A catedral de Milão.", "/ˈdwɔːmo/", "m", "duomi"),
    gen_word(f"t8_{start+20:03}", "castello", "castelo", "cultura", "Un antico castello medievale.", "Um antigo castelo medieval.", "/kasˈtɛllo/", "m", "castelli"),
    gen_word(f"t8_{start+21:03}", "piazza", "praça", "cultura", "La piazza centrale della città.", "A praça central da cidade.", "/ˈpjattsa/", "f", "piazze"),
    gen_word(f"t8_{start+22:03}", "fontana", "fonte", "cultura", "La Fontana di Trevi a Roma.", "A Fonte de Trevi em Roma.", "/fonˈtaːna/", "f", "fontane"),
    gen_word(f"t8_{start+23:03}", "ponte", "ponte", "cultura", "Il Ponte Vecchio a Firenze.", "A Ponte Vecchio em Florença.", "/ˈponte/", "m", "ponti"),
    gen_word(f"t8_{start+24:03}", "religione", "religião", "cultura", "La religione cattolica in Italia.", "A religião católica na Itália.", "/reliˈdʒoːne/", "f", "religioni"),
    gen_word(f"t8_{start+25:03}", "dio", "deus", "cultura", "Credi in Dio?", "Você acredita em Deus?", "/ˈdiːo/", "m", "dei"),
    gen_word(f"t8_{start+26:03}", "papa", "papa", "cultura", "Il Papa vive in Vaticano.", "O Papa vive no Vaticano.", "/ˈpaːpa/", "m", "papi"),
    gen_word(f"t8_{start+27:03}", "natale", "natal", "cultura", "Buon Natale e felice anno nuovo.", "Feliz Natal e próspero ano novo.", "/naˈtaːle/", "m", None),
    gen_word(f"t8_{start+28:03}", "pasqua", "páscoa", "cultura", "A Pasqua mangiamo l'uovo di cioccolato.", "Na Páscoa comemos o ovo de chocolate.", "/ˈpaskwa/", "f", None),
    gen_word(f"t8_{start+29:03}", "regalo", "presente", "cultura", "Questo regalo è per te.", "Este presente é para você.", "/reˈɡaːlo/", "m", "regali"),
    gen_word(f"t8_{start+30:03}", "vacanza", "férias", "cultura", "Ad agosto andiamo in vacanza.", "Em agosto vamos de férias.", "/vaˈkantsa/", "f", "vacanze"),
    gen_word(f"t8_{start+31:03}", "viaggio", "viagem", "cultura", "Un bellissimo viaggio in Italia.", "Uma belíssima viagem à Itália.", "/ˈvjaddʒo/", "m", "viaggi"),
    gen_word(f"t8_{start+32:03}", "turista", "turista", "cultura", "La città è piena di turisti.", "A cidade está cheia de turistas.", "/tuˈrista/", "m/f", "turisti"),
    gen_word(f"t8_{start+33:03}", "guida", "guia", "cultura", "Abbiamo prenotato una guida locale.", "Reservamos um guia local.", "/ˈɡwiːda/", "f", "guide"),
    gen_word(f"t8_{start+34:03}", "mappa", "mapa", "cultura", "Guarda la mappa del centro storico.", "Olhe o mapa do centro histórico.", "/ˈmappa/", "f", "mappe"),
    gen_word(f"t8_{start+35:03}", "biglietto", "ingresso", "cultura", "Due biglietti per il museo, per favore.", "Dois ingressos para o museu, por favor.", "/biʎˈʎetto/", "m", "biglietti"),
    gen_word(f"t8_{start+36:03}", "prezzo", "preço", "cultura", "Qual è il prezzo del biglietto?", "Qual é o preço do ingresso?", "/ˈprɛttso/", "m", "prezzi"),
    gen_word(f"t8_{start+37:03}", "gratis", "grátis", "cultura", "L'ingresso oggi è gratis.", "A entrada hoje é grátis.", "/ˈɡratis/", None, None),
    gen_word(f"t8_{start+38:03}", "aperto", "aberto", "cultura", "Il museo è aperto tutti i giorni.", "O museu está aberto todos os dias.", "/aˈpɛrto/", "m", "aperti"),
    gen_word(f"t8_{start+39:03}", "chiuso", "fechado", "cultura", "La domenica il negozio è chiuso.", "Aos domingos a loja está fechada.", "/ˈkjuːzo/", "m", "chiusi"),
    gen_word(f"t8_{start+40:03}", "fotografia", "fotografia / foto", "cultura", "Posso scattare una fotografia?", "Posso tirar uma foto?", "/fotoɡraˈfiːa/", "f", "fotografie"),
    gen_word(f"t8_{start+41:03}", "ricordo", "lembrança / souvenir", "cultura", "Compro un ricordo per mia madre.", "Compro uma lembrancinha para minha mãe.", "/riˈkɔrdo/", "m", "ricordi")
]
t8_words.extend(t8_new)
t8_data["palavras"] = t8_words[:107]
save(8, t8_data)

# ----------------- TEMPLO 9 (Bari: Lavoro, Professioni) -----------------
t9_data = load(9)
t9_words = t9_data.get("palavras", t9_data.get("vocabulario", []))
start = len(t9_words) + 1

t9_new = [
    gen_word(f"t9_{start+0:03}", "professione", "profissão", "lavoro", "Qual è la tua professione?", "Qual é a sua profissão?", "/profesˈsjoːne/", "f", "professioni"),
    gen_word(f"t9_{start+1:03}", "mestiere", "ofício / profissão", "lavoro", "Fa il mestiere del falegname.", "Faz o ofício de carpinteiro.", "/mesˈtjɛːre/", "m", "mestieri"),
    gen_word(f"t9_{start+2:03}", "impiegato", "empregado / funcionário", "lavoro", "È impiegato in banca.", "É funcionário no banco.", "/impjeˈɡaːto/", "m", "impiegati"),
    gen_word(f"t9_{start+3:03}", "operaio", "operário", "lavoro", "L'operaio lavora in fabbrica.", "O operário trabalha na fábrica.", "/opeˈraːjo/", "m", "operai"),
    gen_word(f"t9_{start+4:03}", "medico", "médico", "lavoro", "Il medico lavora in ospedale.", "O médico trabalha no hospital.", "/ˈmɛːdiko/", "m", "medici"),
    gen_word(f"t9_{start+5:03}", "infermiere", "enfermeiro", "lavoro", "L'infermiere cura i malati.", "O enfermeiro cuida dos doentes.", "/inferˈmjɛːre/", "m", "infermieri"),
    gen_word(f"t9_{start+6:03}", "avvocato", "advogado", "lavoro", "Ho bisogno di un buon avvocato.", "Preciso de um bom advogado.", "/avvoˈkaːto/", "m", "avvocati"),
    gen_word(f"t9_{start+7:03}", "ingegnere", "engenheiro", "lavoro", "L'ingegnere progetta ponti.", "O engenheiro projeta pontes.", "/indʒeˈɲɛːre/", "m", "ingegneri"),
    gen_word(f"t9_{start+8:03}", "architetto", "arquiteto", "lavoro", "L'architetto disegna case belle.", "O arquiteto desenha casas bonitas.", "/arkiˈtetto/", "m", "architetti"),
    gen_word(f"t9_{start+9:03}", "insegnante", "professor (geral)", "lavoro", "Mia madre è insegnante.", "Minha mãe é professora.", "/inseɲˈɲante/", "m/f", "insegnanti"),
    gen_word(f"t9_{start+10:03}", "professore", "professor (secundário/universitário)", "lavoro", "Il professore tiene una lezione.", "O professor dá uma aula.", "/profesˈsoːre/", "m", "professori"),
    gen_word(f"t9_{start+11:03}", "studente", "estudante", "lavoro", "Sono uno studente di lingue.", "Sou um estudante de línguas.", "/stuˈdɛnte/", "m", "studenti"),
    gen_word(f"t9_{start+12:03}", "segretario", "secretário", "lavoro", "La segretaria risponde al telefono.", "A secretária atende o telefone.", "/seɡreˈtaːrjo/", "m", "segretari"),
    gen_word(f"t9_{start+13:03}", "dirigente", "dirigente / diretor", "lavoro", "Il dirigente dell'azienda.", "O dirigente da empresa.", "/diriˈdʒɛnte/", "m", "dirigenti"),
    gen_word(f"t9_{start+14:03}", "imprenditore", "empreendedor / empresário", "lavoro", "Un giovane imprenditore di successo.", "Um jovem empreendedor de sucesso.", "/imprendiˈtoːre/", "m", "imprenditori"),
    gen_word(f"t9_{start+15:03}", "negoziante", "lojista", "lavoro", "Il negoziante vende vestiti.", "O lojista vende roupas.", "/neɡotˈtsjante/", "m/f", "negozianti"),
    gen_word(f"t9_{start+16:03}", "cuoco", "cozinheiro", "lavoro", "Il cuoco prepara la cena.", "O cozinheiro prepara o jantar.", "/ˈkwɔːko/", "m", "cuochi"),
    gen_word(f"t9_{start+17:03}", "poliziotto", "policial", "lavoro", "Il poliziotto ferma il traffico.", "O policial para o tráfego.", "/politˈtsjɔtto/", "m", "poliziotti"),
    gen_word(f"t9_{start+18:03}", "pensionato", "aposentato", "lavoro", "Mio nonno è pensionato.", "Meu avô é aposentado.", "/pensjoˈnaːto/", "m", "pensionati"),
    gen_word(f"t9_{start+19:03}", "disoccupato", "desempregado", "lavoro", "Ora sono disoccupato e cerco lavoro.", "Agora estou desempregado e procuro trabalho.", "/dizokkuˈpaːto/", "m", "disoccupati"),
    gen_word(f"t9_{start+20:03}", "fabbrica", "fábrica", "lavoro", "Lavora in una fabbrica di auto.", "Trabalha numa fábrica de carros.", "/ˈfabbrika/", "f", "fabbriche"),
    gen_word(f"t9_{start+21:03}", "progetto", "projeto", "lavoro", "Iniziamo un nuovo progetto.", "Começamos um novo projeto.", "/proˈdʒɛtto/", "m", "progetti"),
    gen_word(f"t9_{start+22:03}", "cliente", "cliente", "lavoro", "Il cliente ha sempre ragione.", "O cliente tem sempre razão.", "/kliˈɛnte/", "m/f", "clienti"),
    gen_word(f"t9_{start+23:03}", "contratto", "contrato", "lavoro", "Firma il contratto di lavoro.", "Assina o contrato de trabalho.", "/konˈtratto/", "m", "contratti"),
    gen_word(f"t9_{start+24:03}", "soldi", "dinheiro (informal)", "economia", "Non ho soldi con me.", "Não tenho dinheiro comigo.", "/ˈsɔldi/", "m", "soldi"),
    gen_word(f"t9_{start+25:03}", "denaro", "dinheiro (formal)", "economia", "Il denaro non fa la felicità.", "O dinheiro não traz felicidade.", "/deˈnaːro/", "m", "denari"),
    gen_word(f"t9_{start+26:03}", "banca", "banco", "economia", "Devo andare in banca a prelevare.", "Devo ir ao banco sacar (dinheiro).", "/ˈbaŋka/", "f", "banche"),
    gen_word(f"t9_{start+27:03}", "carta", "cartão / papel", "economia", "Pago con la carta di credito.", "Pago com o cartão de crédito.", "/ˈkarta/", "f", "carte"),
    gen_word(f"t9_{start+28:03}", "sciopero", "greve", "lavoro", "Oggi c'è lo sciopero dei treni.", "Hoje tem greve dos trens.", "/ˈʃɔːpero/", "m", "scioperi"),
    gen_word(f"t9_{start+29:03}", "affare", "negócio", "economia", "Abbiamo concluso un buon affare.", "Fechamos um bom negócio.", "/afˈfaːre/", "m", "affari"),
    gen_word(f"t9_{start+30:03}", "merito", "mérito", "lavoro", "Hai ottenuto il lavoro con merito.", "Você conseguiu o trabalho por mérito.", "/ˈmɛːrito/", "m", "meriti"),
    gen_word(f"t9_{start+31:03}", "colloquio", "entrevista (de emprego)", "lavoro", "Domani ho un colloquio di lavoro.", "Amanhã tenho uma entrevista de emprego.", "/kolˈlɔkwjo/", "m", "colloqui"),
    gen_word(f"t9_{start+32:03}", "guadagnare", "ganhar (dinheiro)", "verbi", "Lavora molto per guadagnare bene.", "Trabalha muito para ganhar bem.", "/ɡwadaɲˈɲaːre/", None, None),
    gen_word(f"t9_{start+33:03}", "spendere", "gastar", "verbi", "Non spendere troppi soldi.", "Não gaste dinheiro demais.", "/ˈspɛndere/", None, None),
    gen_word(f"t9_{start+34:03}", "risparmiare", "economizar / poupar", "verbi", "Voglio risparmiare per comprare casa.", "Quero poupar para comprar casa.", "/risparˈmjaːre/", None, None),
    gen_word(f"t9_{start+35:03}", "assumere", "contratar", "verbi", "L'azienda assume nuovi impiegati.", "A empresa contrata novos funcionários.", "/asˈsuːmere/", None, None),
    gen_word(f"t9_{start+36:03}", "licenziare", "demitir", "verbi", "Il capo ha licenziato due operai.", "O chefe demitiu dois operários.", "/litʃenˈtsjaːre/", None, None),
    gen_word(f"t9_{start+37:03}", "promozione", "promoção", "lavoro", "Ha ottenuto una promozione.", "Ele conseguiu uma promoção.", "/promotˈtsjoːne/", "f", "promozioni"),
    gen_word(f"t9_{start+38:03}", "mercato", "mercado", "economia", "La frutta al mercato è fresca.", "A fruta no mercado é fresca.", "/merˈkaːto/", "m", "mercati"),
    gen_word(f"t9_{start+39:03}", "economia", "economia", "economia", "L'economia cresce lentamente.", "A economia cresce lentamente.", "/ekonoˈmiːa/", "f", "economie"),
    gen_word(f"t9_{start+40:03}", "prezzo", "preço", "economia", "Il prezzo della benzina è alto.", "O preço da gasolina está alto.", "/ˈprɛttso/", "m", "prezzi"),
    gen_word(f"t9_{start+41:03}", "valore", "valor", "economia", "Questo quadro ha un grande valore.", "Este quadro tem um grande valor.", "/vaˈloːre/", "m", "valori")
]
t9_words.extend(t9_new)
t9_data["palavras"] = t9_words[:107]
save(9, t9_data)

# ----------------- TEMPLO 10 (Siena: Letteratura, Arte) -----------------
t10_data = load(10)
t10_words = t10_data.get("palavras", t10_data.get("vocabulario", []))
start = len(t10_words) + 1

t10_new = [
    gen_word(f"t10_{start+0:03}", "letteratura", "literatura", "arte", "Studiamo la letteratura italiana.", "Estudamos a literatura italiana.", "/letteraˈtuːra/", "f", "letterature"),
    gen_word(f"t10_{start+1:03}", "libro", "livro", "arte", "Sto leggendo un libro bello.", "Estou lendo um livro bonito.", "/ˈliːbro/", "m", "libri"),
    gen_word(f"t10_{start+2:03}", "romanzo", "romance", "arte", "Un famoso romanzo storico.", "Um famoso romance histórico.", "/roˈmandzo/", "m", "romanzi"),
    gen_word(f"t10_{start+3:03}", "poesia", "poesia", "arte", "Scrive poesia d'amore.", "Escreve poesia de amor.", "/poeˈziːa/", "f", "poesie"),
    gen_word(f"t10_{start+4:03}", "poeta", "poeta", "arte", "Dante è un grande poeta.", "Dante é um grande poeta.", "/poˈɛːta/", "m", "poeti"),
    gen_word(f"t10_{start+5:03}", "scrittore", "escritor", "arte", "Il mio scrittore preferito.", "O meu escritor preferido.", "/skritˈtoːre/", "m", "scrittori"),
    gen_word(f"t10_{start+6:03}", "autore", "autor", "arte", "L'autore del libro è sconosciuto.", "O autor do livro é desconhecido.", "/awˈtoːre/", "m", "autori"),
    gen_word(f"t10_{start+7:03}", "storia", "conto / história", "arte", "Una bella storia della buonanotte.", "Uma bela história de ninar.", "/ˈstɔːrja/", "f", "storie"),
    gen_word(f"t10_{start+8:03}", "racconto", "conto / narrativa", "arte", "Un breve racconto giallo.", "Um breve conto policial.", "/rakˈkonto/", "m", "racconti"),
    gen_word(f"t10_{start+9:03}", "parola", "palavra", "grammatica", "Una parola molto difficile.", "Uma palavra muito difícil.", "/paˈrɔːla/", "f", "parole"),
    gen_word(f"t10_{start+10:03}", "frase", "frase", "grammatica", "Scrivi una frase intera.", "Escreva uma frase inteira.", "/ˈfraːze/", "f", "frasi"),
    gen_word(f"t10_{start+11:03}", "capitolo", "capítulo", "arte", "Siamo al primo capitolo.", "Estamos no primeiro capítulo.", "/kaˈpiːtolo/", "m", "capitoli"),
    gen_word(f"t10_{start+12:03}", "titolo", "título", "arte", "Qual è il titolo del film?", "Qual é o título do filme?", "/ˈtiːtolo/", "m", "titoli"),
    gen_word(f"t10_{start+13:03}", "personaggio", "personagem", "arte", "Il personaggio principale del libro.", "O personagem principal do livro.", "/personˈnaddʒo/", "m", "personaggi"),
    gen_word(f"t10_{start+14:03}", "arte", "arte", "arte", "Un'opera d'arte contemporanea.", "Uma obra de arte contemporânea.", "/ˈarte/", "f", "arti"),
    gen_word(f"t10_{start+15:03}", "pittura", "pintura", "arte", "La pittura a olio.", "A pintura a óleo.", "/pitˈtuːra/", "f", "pitture"),
    gen_word(f"t10_{start+16:03}", "scultura", "escultura", "arte", "Una scultura di Michelangelo.", "Uma escultura de Michelangelo.", "/skulˈtuːra/", "f", "sculture"),
    gen_word(f"t10_{start+17:03}", "architettura", "arquitetura", "arte", "L'architettura gotica in Europa.", "A arquitetura gótica na Europa.", "/arkitetˈtuːra/", "f", "architetture"),
    gen_word(f"t10_{start+18:03}", "disegno", "desenho", "arte", "Un disegno fatto a matita.", "Um desenho feito a lápis.", "/diˈzeɲɲo/", "m", "disegni"),
    gen_word(f"t10_{start+19:03}", "colore", "cor", "arte", "Usa dei colori vivaci.", "Usa cores vivas.", "/koˈloːre/", "m", "colori"),
    gen_word(f"t10_{start+20:03}", "ombra", "sombra", "arte", "Il gioco di luce e ombra.", "O jogo de luz e sombra.", "/ˈombra/", "f", "ombre"),
    gen_word(f"t10_{start+21:03}", "luce", "luz", "arte", "La luce entra dalla finestra.", "A luz entra pela janela.", "/ˈluːtʃe/", "f", "luci"),
    gen_word(f"t10_{start+22:03}", "bellezza", "beleza", "arte", "Amiamo la bellezza naturale.", "Amamos a beleza natural.", "/belˈlettsa/", "f", "bellezze"),
    gen_word(f"t10_{start+23:03}", "creatività", "criatividade", "arte", "I bambini hanno molta creatività.", "As crianças têm muita criatividade.", "/kreativiˈta/", "f", "creatività"),
    gen_word(f"t10_{start+24:03}", "fantasia", "fantasia / imaginação", "arte", "Usa la tua fantasia.", "Use a sua imaginação.", "/fantaˈziːa/", "f", "fantasie"),
    gen_word(f"t10_{start+25:03}", "sogno", "sonho", "arte", "Ho fatto uno strano sogno.", "Tive um sonho estranho.", "/ˈsoɲɲo/", "m", "sogni"),
    gen_word(f"t10_{start+26:03}", "immaginare", "imaginar", "verbi", "Prova a immaginare il futuro.", "Tente imaginar o futuro.", "/immadʒiˈnaːre/", None, None),
    gen_word(f"t10_{start+27:03}", "creare", "criar", "verbi", "L'artista crea opere uniche.", "O artista cria obras únicas.", "/kreˈaːre/", None, None),
    gen_word(f"t10_{start+28:03}", "pensiero", "pensamento", "arte", "È perso nei suoi pensieri.", "Está perdido nos seus pensamentos.", "/penˈsjɛːro/", "m", "pensieri"),
    gen_word(f"t10_{start+29:03}", "mente", "mente", "arte", "Avere la mente aperta.", "Ter a mente aberta.", "/ˈmente/", "f", "menti"),
    gen_word(f"t10_{start+30:03}", "anima", "alma", "arte", "La musica guarisce l'anima.", "A música cura a alma.", "/ˈaːnima/", "f", "anime"),
    gen_word(f"t10_{start+31:03}", "emozione", "emoção", "arte", "Provo una forte emozione.", "Sinto uma forte emoção.", "/emotˈtsjoːne/", "f", "emozioni"),
    gen_word(f"t10_{start+32:03}", "sentimento", "sentimento", "arte", "Un sentimento di pace profonda.", "Um sentimento de paz profunda.", "/sentiˈmento/", "m", "sentimenti"),
    gen_word(f"t10_{start+33:03}", "amore", "amor", "arte", "L'amore muove il mondo.", "O amor move o mundo.", "/aˈmoːre/", "m", "amori"),
    gen_word(f"t10_{start+34:03}", "passione", "paixão", "arte", "La pittura è la mia passione.", "A pintura é a minha paixão.", "/pasˈsjoːne/", "f", "passioni"),
    gen_word(f"t10_{start+35:03}", "dolore", "dor", "arte", "Una storia piena di dolore.", "Uma história cheia de dor.", "/doˈloːre/", "m", "dolori"),
    gen_word(f"t10_{start+36:03}", "gioia", "alegria", "arte", "Pieni di gioia per la vittoria.", "Cheios de alegria pela vitória.", "/ˈdʒɔːja/", "f", "gioie"),
    gen_word(f"t10_{start+37:03}", "vita", "vida", "arte", "La vita è bella.", "A vida é bela.", "/ˈviːta/", "f", "vite"),
    gen_word(f"t10_{start+38:03}", "morte", "morte", "arte", "Il mistero della morte.", "O mistério da morte.", "/ˈmɔrte/", "f", "morti"),
    gen_word(f"t10_{start+39:03}", "destino", "destino", "arte", "Credi nel destino?", "Acreditas no destino?", "/desˈtiːno/", "m", "destini"),
    gen_word(f"t10_{start+40:03}", "libertà", "liberdade", "arte", "La libertà è il bene più grande.", "A liberdade é o maior bem.", "/liberˈta/", "f", "libertà"),
    gen_word(f"t10_{start+41:03}", "verità", "verdade (conceito)", "arte", "La ricerca della verità assoluta.", "A busca da verdade absoluta.", "/veriˈta/", "f", "verità")
]
t10_words.extend(t10_new)
t10_data["palavras"] = t10_words[:107]
save(10, t10_data)

print(f"Completato! T6-T10 salvi.")
