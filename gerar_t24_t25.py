import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def w(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {
        "id": tid, "italiano": it, "portugues": pt, "genero": gen, "plural": pl,
        "exemplo": ex_it, "exemplo_pt": ex_pt, "categoria": cat, "dificuldade": "medio", "audio_ipa": ipa
    }

# T24: La Tecnologia Moderna
t24_data = [
    # Hardware e Dispositivi
    ("computer", "computador", "hardware", "Il mio computer è rotto.", "Meu computador quebrou.", "/komˈpjuter/", "m", "computer"),
    ("smartphone", "smartphone", "hardware", "Non riesco a vivere senza smartphone.", "Não consigo viver sem smartphone.", "/ˈzmartfon/", "m", "smartphone"),
    ("schermo", "tela", "hardware", "Lo schermo è molto grande.", "A tela é muito grande.", "/ˈskermo/", "m", "schermi"),
    ("tastiera", "teclado", "hardware", "Una tastiera senza fili.", "Um teclado sem fio.", "/tasˈtjɛra/", "f", "tastiere"),
    ("mouse", "mouse", "hardware", "Uso un mouse ottico.", "Uso um mouse óptico.", "/ˈmaus/", "m", "mouse"),
    ("stampante", "impressora", "hardware", "La stampante non ha inchiostro.", "A impressora não tem tinta.", "/stamˈpante/", "f", "stampanti"),
    ("tablet", "tablet", "hardware", "Leggo le notizie sul tablet.", "Leio as notícias no tablet.", "/ˈtablɛt/", "m", "tablet"),
    ("portatile", "notebook", "hardware", "Porto il portatile in ufficio.", "Levo o notebook para o escritório.", "/porˈtatile/", "m", "portatili"),
    ("cuffie", "fones de ouvido", "hardware", "Ascolto la musica con le cuffie.", "Escuto música com fones de ouvido.", "/ˈkuffje/", "f", "cuffie"),
    ("batteria", "bateria", "hardware", "La batteria è quasi scarica.", "A bateria está quase descarregada.", "/batteˈria/", "f", "batterie"),
    ("caricabatterie", "carregador", "hardware", "Hai un caricabatterie?", "Você tem um carregador?", "/karikabatˈtɛrje/", "m", "caricabatterie"),
    ("memoria", "memória", "hardware", "Il telefono ha poca memoria.", "O telefone tem pouca memória.", "/meˈmɔrja/", "f", "memorie"),
    ("disco fisso", "disco rígido", "hardware", "Un disco fisso da un terabyte.", "Um disco rígido de um terabyte.", "/ˈdisko ˈfisso/", "m", "dischi fissi"),
    ("microfono", "microfone", "hardware", "Parla al microfono.", "Fale ao microfone.", "/miˈkrɔfono/", "m", "microfoni"),
    ("webcam", "webcam", "hardware", "Accendi la webcam.", "Ligue a webcam.", "/ˈwɛbkam/", "f", "webcam"),
    ("altoparlante", "alto-falante", "hardware", "L'altoparlante è acceso.", "O alto-falante está ligado.", "/altoparˈlante/", "m", "altoparlanti"),
    ("cavo", "cabo", "hardware", "Usa il cavo USB.", "Use o cabo USB.", "/ˈkavo/", "m", "cavi"),
    ("chiavetta", "pendrive", "hardware", "I file sono nella chiavetta.", "Os arquivos estão no pendrive.", "/kjaˈvetta/", "f", "chiavette"),

    # Internet e Reti
    ("internet", "internet", "reti", "Navigare su internet.", "Navegar na internet.", "/ˈintɛrnɛt/", "m", "internet"),
    ("rete", "rede", "reti", "La rete Wi-Fi non funziona.", "A rede Wi-Fi não funciona.", "/ˈrete/", "f", "reti"),
    ("connessione", "conexão", "reti", "Una connessione molto lenta.", "Uma conexão muito lenta.", "/konnesˈsjone/", "f", "connessioni"),
    ("router", "roteador", "reti", "Devi riavviare il router.", "Você deve reiniciar o roteador.", "/ˈruter/", "m", "router"),
    ("segnale", "sinal", "reti", "Non c'è segnale qui.", "Não tem sinal aqui.", "/seɲˈɲale/", "m", "segnali"),
    ("server", "servidor", "reti", "Il server è offline.", "O servidor está offline.", "/ˈsɛrver/", "m", "server"),
    ("sito", "site", "reti", "Visita il nostro sito web.", "Visite nosso site.", "/ˈsito/", "m", "siti"),
    ("link", "link", "reti", "Clicca su questo link.", "Clique neste link.", "/link/", "m", "link"),
    ("pagina", "página", "reti", "Una pagina web.", "Uma página web.", "/ˈpadʒina/", "f", "pagine"),
    ("motore di ricerca", "buscador", "reti", "Usa un motore di ricerca.", "Use um buscador.", "/moˈtore di riˈtʃerka/", "m", "motori di ricerca"),
    ("nuvola", "nuvem (cloud)", "reti", "Salva i dati nella nuvola.", "Salve os dados na nuvem.", "/ˈnuvola/", "f", "nuvole"),
    ("fibra ottica", "fibra ótica", "reti", "A casa ho la fibra ottica.", "Em casa tenho fibra ótica.", "/ˈfibra ˈɔttika/", "f", "fibre ottiche"),
    ("banda larga", "banda larga", "reti", "Una connessione a banda larga.", "Uma conexão de banda larga.", "/ˈbanda ˈlarɡa/", "f", "bande larghe"),
    
    # Software e App
    ("applicazione", "aplicativo", "software", "Ho scaricato un'applicazione.", "Baixei um aplicativo.", "/applikatˈtsjone/", "f", "applicazioni"),
    ("software", "software", "software", "Questo software è gratuito.", "Este software é gratuito.", "/ˈsɔftwɛr/", "m", "software"),
    ("programma", "programa", "software", "Un programma di scrittura.", "Um programa de escrita.", "/proˈɡramma/", "m", "programmi"),
    ("sistema operativo", "sistema operacional", "software", "Aggiorna il sistema operativo.", "Atualize o sistema operacional.", "/sisˈtɛma operaˈtivo/", "m", "sistemi operativi"),
    ("file", "arquivo", "software", "Ho cancellato il file per sbaglio.", "Apaguei o arquivo sem querer.", "/ˈfail/", "m", "file"),
    ("cartella", "pasta", "software", "Salva il documento nella cartella.", "Salve o documento na pasta.", "/karˈtɛlla/", "f", "cartelle"),
    ("finestra", "janela", "software", "Chiudi questa finestra.", "Feche esta janela.", "/fiˈnɛstra/", "f", "finestre"),
    ("menu", "menu", "software", "Apri il menu principale.", "Abra o menu principal.", "/meˈnu/", "m", "menu"),
    ("password", "senha", "software", "Hai dimenticato la password?", "Você esqueceu a senha?", "/ˈpasswɔrd/", "f", "password"),
    ("nome utente", "nome de usuário", "software", "Inserisci il nome utente.", "Insira o nome de usuário.", "/ˈnome uˈtɛnte/", "m", "nomi utente"),
    ("aggiornamento", "atualização", "software", "Un nuovo aggiornamento è disponibile.", "Uma nova atualização está disponível.", "/addʒornaˈmento/", "m", "aggiornamenti"),
    ("virus", "vírus", "software", "Il computer ha un virus.", "O computador tem um vírus.", "/ˈvirus/", "m", "virus"),
    ("antivirus", "antivírus", "software", "Installa un antivirus efficace.", "Instale um antivírus eficaz.", "/antiˈvirus/", "m", "antivirus"),
    ("codice", "código", "software", "Scrivere codice di programmazione.", "Escrever código de programação.", "/ˈkɔditʃe/", "m", "codici"),
    ("database", "banco de dados", "software", "Interrogare il database.", "Consultar o banco de dados.", "/dataˈbeiz/", "m", "database"),
    ("intelligenza artificiale", "inteligência artificial", "software", "L'intelligenza artificiale apprende.", "A inteligência artificial aprende.", "/intellidˈdʒɛntsa artifiˈtʃale/", "f", "intelligenze artificiali"),
    ("profilo", "perfil", "software", "Modifica il tuo profilo.", "Modifique o seu perfil.", "/proˈfilo/", "m", "profili"),
    
    # Social e Comunicazione
    ("messaggio", "mensagem", "social", "Ho ricevuto un messaggio.", "Recebi uma mensagem.", "/mesˈsaddʒo/", "m", "messaggi"),
    ("email", "e-mail", "social", "Ti mando un'email.", "Eu te mando um e-mail.", "/iˈmeil/", "f", "email"),
    ("allegato", "anexo", "social", "Controlla l'allegato nell'email.", "Verifique o anexo no e-mail.", "/alleˈɡato/", "m", "allegati"),
    ("chat", "chat", "social", "Scrivimi in chat.", "Me escreva no chat.", "/tʃat/", "f", "chat"),
    ("videochiamata", "chamada de vídeo", "social", "Facciamo una videochiamata.", "Vamos fazer uma chamada de vídeo.", "/videokjaˈmata/", "f", "videochiamate"),
    ("foto", "foto", "social", "Condividere una foto.", "Compartilhar uma foto.", "/ˈfɔto/", "f", "foto"),
    ("post", "post/publicação", "social", "Ho letto il tuo post.", "Li a sua publicação.", "/pɔst/", "m", "post"),
    ("mi piace", "curtida", "social", "Ho messo mi piace.", "Eu dei uma curtida.", "/mi ˈpjatʃe/", "m", "mi piace"),
    ("commento", "comentário", "social", "Lascia un commento.", "Deixe um comentário.", "/komˈmento/", "m", "commenti"),
    ("notifica", "notificação", "social", "Hai una nuova notifica.", "Você tem uma nova notificação.", "/noˈtifika/", "f", "notifiche"),
    ("seguace", "seguidor", "social", "Ha molti seguaci online.", "Tem muitos seguidores online.", "/seˈɡwatʃe/", "m", "seguaci"),
    ("influencer", "influenciador", "social", "È una nota influencer.", "É uma famosa influenciadora.", "/influˈɛnser/", "m/f", "influencer"),
    ("blog", "blog", "social", "Scrivo articoli sul mio blog.", "Escrevo artigos no meu blog.", "/blɔɡ/", "m", "blog"),
    
    # Verbi Tecnologici
    ("accendere", "ligar", "verbi", "Devo accendere il computer.", "Preciso ligar o computador.", "/atˈtʃɛndere/", None, None),
    ("spegnere", "desligar", "verbi", "Ricordati di spegnere lo schermo.", "Lembre-se de desligar a tela.", "/ˈspeɲɲere/", None, None),
    ("riavviare", "reiniciar", "verbi", "Prova a riavviare il dispositivo.", "Tente reiniciar o dispositivo.", "/riavviˈare/", None, None),
    ("scaricare", "baixar/download", "verbi", "Voglio scaricare questa canzone.", "Quero baixar esta música.", "/skariˈkare/", None, None),
    ("caricare", "carregar/upload", "verbi", "Sto caricando un video.", "Estou carregando um vídeo.", "/kariˈkare/", None, None),
    ("installare", "instalar", "verbi", "Installare il nuovo software.", "Instalar o novo software.", "/instalˈlare/", None, None),
    ("disinstallare", "desinstalar", "verbi", "Devo disinstallare l'app.", "Devo desinstalar o aplicativo.", "/dizinstalˈlare/", None, None),
    ("salvare", "salvar", "verbi", "Non ho dimenticato di salvare.", "Não esqueci de salvar.", "/salˈvare/", None, None),
    ("cancellare", "apagar", "verbi", "Non cancellare questo file.", "Não apague este arquivo.", "/kantʃelˈlare/", None, None),
    ("copiare", "copiar", "verbi", "Copiare e incollare il testo.", "Copiar e colar o texto.", "/koˈpjare/", None, None),
    ("incollare", "colar", "verbi", "Incollare il link qui.", "Colar o link aqui.", "/inkolˈlare/", None, None),
    ("tagliare", "cortar", "verbi", "Tagliare la parte finale del video.", "Cortar a parte final do vídeo.", "/taˈʎʎare/", None, None),
    ("cliccare", "clicar", "verbi", "Cliccare col tasto destro.", "Clicar com o botão direito.", "/klikˈkare/", None, None),
    ("digitare", "digitar", "verbi", "Digitare la password.", "Digitar a senha.", "/didʒiˈtare/", None, None),
    ("navigare", "navegar", "verbi", "Navigare in incognito.", "Navegar de forma anônima.", "/naviˈɡare/", None, None),
    ("collegare", "conectar", "verbi", "Collegare il telefono al computer.", "Conectar o telefone ao computador.", "/kolleˈɡare/", None, None),
    ("condividere", "compartilhar", "verbi", "Condividere la foto su Facebook.", "Compartilhar a foto no Facebook.", "/kondiˈvidere/", None, None),
    ("scorrere", "rolar (scroll)", "verbi", "Scorrere la pagina verso il basso.", "Rolar a página para baixo.", "/ˈskorrere/", None, None),
    ("hackerare", "hackear", "verbi", "Hanno hackerato il sito.", "Hackearam o site.", "/hakeˈrare/", None, None),
    ("chattare", "teclar/bater papo", "verbi", "Amano chattare ore e ore.", "Amam teclar por horas e horas.", "/tʃatˈtare/", None, None),
    
    # Aggettivi e Altro
    ("digitale", "digital", "aggettivi", "L'era digitale.", "A era digital.", "/didʒiˈtale/", "m", "digitali"),
    ("virtuale", "virtual", "aggettivi", "La realtà virtuale.", "A realidade virtual.", "/virˈtwale/", "m", "virtuali"),
    ("tecnologico", "tecnológico", "aggettivi", "Sviluppo tecnologico.", "Desenvolvimento tecnológico.", "/teknoˈlɔdʒiko/", "m", "tecnologici"),
    ("informatico", "informático", "aggettivi", "Un problema informatico.", "Um problema informático.", "/inforˈmatiko/", "m", "informatici"),
    ("automatico", "automático", "aggettivi", "Il salvataggio è automatico.", "O salvamento é automático.", "/autoˈmatiko/", "m", "automatici"),
    ("interattivo", "interativo", "aggettivi", "Un museo interattivo.", "Um museu interativo.", "/interatˈtivo/", "m", "interattivi"),
    ("intelligente", "inteligente", "aggettivi", "Una casa intelligente.", "Uma casa inteligente.", "/intellidˈdʒɛnte/", "m", "intelligenti"),
    ("online", "on-line", "aggettivi", "Sono sempre online.", "Estou sempre on-line.", "/onˈlain/", None, None),
    ("offline", "off-line", "aggettivi", "Lavorare in modalità offline.", "Trabalhar em modo off-line.", "/ofˈflain/", None, None)
]

# T25: Il Commercio e i Soldi
t25_data = [
    # Negozi e Luoghi
    ("negozio", "loja", "luoghi", "Il negozio è chiuso.", "A loja está fechada.", "/neˈɡɔtsjo/", "m", "negozi"),
    ("mercato", "mercado", "luoghi", "Compro la frutta al mercato.", "Compro a fruta no mercado.", "/merˈkato/", "m", "mercati"),
    ("supermercato", "supermercato", "luoghi", "Andiamo al supermercato oggi.", "Vamos ao supermercado hoje.", "/supermerˈkato/", "m", "supermercati"),
    ("centro commerciale", "shopping center", "luoghi", "Fare shopping al centro commerciale.", "Fazer compras no shopping center.", "/ˈtʃɛntro kommerˈtʃale/", "m", "centri commerciali"),
    ("cassa", "caixa", "luoghi", "Pagare alla cassa.", "Pagar no caixa.", "/ˈkassa/", "f", "casse"),
    ("vetrina", "vitrine", "luoghi", "Guardare la vetrina.", "Olhar a vitrine.", "/veˈtrina/", "f", "vetrine"),
    ("scaffale", "prateleira", "luoghi", "Il prodotto è sullo scaffale.", "O produto está na prateleira.", "/skafˈfale/", "m", "scaffali"),
    ("corsia", "corredor (loja)", "luoghi", "La corsia dei detersivi.", "O corredor dos detergentes.", "/korˈsia/", "f", "corsie"),
    ("magazzino", "armazém", "luoghi", "Il prodotto è nel magazzino.", "O produto está no armazém.", "/maɡadˈdzino/", "m", "magazzini"),
    ("boutique", "butique", "luoghi", "Una boutique di lusso.", "Uma butique de luxo.", "/buˈtik/", "f", "boutique"),
    ("panetteria", "padaria", "luoghi", "Compra il pane in panetteria.", "Compre o pão na padaria.", "/panetteˈria/", "f", "panetterie"),
    ("macelleria", "açougue", "luoghi", "Carne fresca in macelleria.", "Carne fresca no açougue.", "/matʃelleˈria/", "f", "macellerie"),
    ("pescheria", "peixaria", "luoghi", "Andiamo in pescheria.", "Vamos à peixaria.", "/peskeˈria/", "f", "pescherie"),
    ("farmacia", "farmácia", "luoghi", "Compra la medicina in farmacia.", "Compre o remédio na farmácia.", "/farmaˈtʃia/", "f", "farmacie"),
    ("libreria", "livraria", "luoghi", "Una libreria fornitissima.", "Uma livraria bem abastecida.", "/libreˈria/", "f", "librerie"),
    
    # Persone
    ("cliente", "cliente", "persone", "Il cliente ha sempre ragione.", "O cliente tem sempre razão.", "/kliˈɛnte/", "m/f", "clienti"),
    ("commesso", "vendedor", "persone", "Chiedi al commesso.", "Pergunte ao vendedor.", "/komˈmesso/", "m", "commessi"),
    ("cassiere", "caixa (pessoa)", "persone", "Il cassiere mi ha dato il resto.", "O caixa me deu o troco.", "/kasˈsjɛre/", "m", "cassieri"),
    ("direttore", "diretor/gerente", "persone", "Voglio parlare col direttore.", "Quero falar com o gerente.", "/diretˈtore/", "m", "direttori"),
    ("compratore", "comprador", "persone", "Trovare un compratore per la casa.", "Encontrar um comprador para a casa.", "/kompraˈtore/", "m", "compratori"),
    ("venditore", "vendedor ambulante/vendedor", "persone", "Il venditore ambulante.", "O vendedor ambulante.", "/vendiˈtore/", "m", "venditori"),
    ("consumatore", "consumidor", "persone", "I diritti del consumatore.", "Os direitos do consumidor.", "/konsumaˈtore/", "m", "consumatori"),
    
    # Oggetti e Soldi
    ("soldi", "dinheiro", "denaro", "Non ho soldi con me.", "Não tenho dinheiro comigo.", "/ˈsɔldi/", "m", "soldi"),
    ("denaro", "dinheiro", "denaro", "Un prestito di denaro.", "Um empréstimo de dinheiro.", "/deˈnaro/", "m", "denari"),
    ("prezzo", "preço", "denaro", "Il prezzo è molto alto.", "O preço é muito alto.", "/ˈprɛttso/", "m", "prezzi"),
    ("offerta", "oferta", "denaro", "C'è un'ottima offerta.", "Há uma ótima oferta.", "/ofˈfɛrta/", "f", "offerte"),
    ("sconto", "desconto", "denaro", "Fare uno sconto del dieci percento.", "Fazer um desconto de dez por cento.", "/ˈskonto/", "m", "sconti"),
    ("scontrino", "nota fiscal/recibo", "denaro", "Tieni lo scontrino.", "Guarde o recibo.", "/skonˈtrino/", "m", "scontrini"),
    ("banconota", "cédula", "denaro", "Una banconota da venti euro.", "Uma cédula de vinte euros.", "/bankoˈnɔta/", "f", "banconote"),
    ("moneta", "moeda", "denaro", "Non ho una moneta per il carrello.", "Não tenho uma moeda para o carrinho.", "/moˈneta/", "f", "monete"),
    ("spiccioli", "trocados", "denaro", "Hai degli spiccioli?", "Você tem alguns trocados?", "/ˈspittʃoli/", "m", "spiccioli"),
    ("resto", "troco", "denaro", "Tieni il resto.", "Fique com o troco.", "/ˈrɛsto/", "m", "resti"),
    ("carta di credito", "cartão de crédito", "denaro", "Pagare con la carta di credito.", "Pagar com o cartão de crédito.", "/ˈkarta di ˈkredito/", "f", "carte di credito"),
    ("bancomat", "cartão de débito/caixa eletrônico", "denaro", "Ritirare soldi al bancomat.", "Sacar dinheiro no caixa eletrônico.", "/ˈbankomat/", "m", "bancomat"),
    ("assegno", "cheque", "denaro", "Compilare un assegno.", "Preencher um cheque.", "/asˈseɲɲo/", "m", "assegni"),
    ("conto", "conta", "denaro", "Porti il conto, per favore?", "Pode trazer a conta, por favor?", "/ˈkonto/", "m", "conti"),
    ("bonifico", "transferência", "denaro", "Fare un bonifico bancario.", "Fazer uma transferência bancária.", "/boˈnifiko/", "m", "bonifici"),
    ("prestito", "empréstimo", "denaro", "Chiedere un prestito in banca.", "Pedir um empréstimo no banco.", "/ˈprɛstito/", "m", "prestiti"),
    ("mutuo", "financiamento imobiliário", "denaro", "Accendere un mutuo.", "Fazer um financiamento imobiliário.", "/ˈmutwo/", "m", "mutui"),
    ("tassa", "taxa", "denaro", "Pagare una tassa.", "Pagar uma taxa.", "/ˈtassa/", "f", "tasse"),
    ("imposta", "imposto", "denaro", "Le imposte sul reddito.", "Os impostos de renda.", "/imˈpɔsta/", "f", "imposte"),
    ("debito", "dívida", "denaro", "Avere un grosso debito.", "Ter uma grande dívida.", "/ˈdebito/", "m", "debiti"),
    ("credito", "crédito", "denaro", "Comprare a credito.", "Comprar a crédito.", "/ˈkredito/", "m", "crediti"),
    ("portafoglio", "carteira", "denaro", "Ho dimenticato il portafoglio.", "Esqueci a carteira.", "/portaˈfɔʎʎo/", "m", "portafogli"),
    ("saldi", "liquidação", "denaro", "Comprare durante i saldi.", "Comprar durante a liquidação.", "/ˈsaldi/", "m", "saldi"),
    ("fattura", "fatura", "denaro", "Emettere una fattura.", "Emitir uma fatura.", "/fatˈtura/", "f", "fatture"),
    ("busta paga", "contracheque", "denaro", "Ricevere la busta paga.", "Receber o contracheque.", "/ˈbusta ˈpaɡa/", "f", "buste paga"),
    ("stipendio", "salário", "denaro", "Uno stipendio molto basso.", "Um salário muito baixo.", "/stiˈpɛndjo/", "m", "stipendi"),
    ("salario", "salário", "denaro", "Aumento del salario.", "Aumento do salário.", "/saˈlarjo/", "m", "salari"),
    ("bilancio", "orçamento/balanço", "denaro", "Il bilancio dell'azienda.", "O balanço da empresa.", "/biˈlantʃo/", "m", "bilanci"),
    ("azione", "ação (financeira)", "denaro", "Vendere le azioni in borsa.", "Vender as ações na bolsa.", "/atˈtsjone/", "f", "azioni"),
    ("borsa", "bolsa (sacola ou valores)", "denaro", "La borsa crolla oggi.", "A bolsa de valores cai hoje.", "/ˈborsa/", "f", "borse"),
    
    # Prodotti e Spesa
    ("prodotto", "produto", "oggetti", "Un prodotto di qualità.", "Um produto de qualidade.", "/proˈdotto/", "m", "prodotti"),
    ("merce", "mercadoria", "oggetti", "Trasportare la merce.", "Transportar a mercadoria.", "/ˈmɛrtʃe/", "f", "merci"),
    ("articolo", "artigo", "oggetti", "Questo articolo è esaurito.", "Este artigo está esgotato.", "/arˈtikolo/", "m", "articoli"),
    ("marca", "marca", "oggetti", "Un vestito di marca.", "Uma roupa de marca.", "/ˈmarka/", "f", "marche"),
    ("qualità", "qualidade", "oggetti", "La qualità costa.", "A qualidade custa.", "/kwaliˈta/", "f", "qualità"),
    ("taglia", "tamanho/número (roupa)", "oggetti", "Hai questa maglia nella mia taglia?", "Você tem essa blusa no meu tamanho?", "/ˈtaʎʎa/", "f", "taglie"),
    ("carrello", "carrinho", "oggetti", "Spingere il carrello.", "Empurrar o carrinho.", "/karˈrɛllo/", "m", "carrelli"),
    ("cestino", "cestinha", "oggetti", "Usa un cestino per la spesa.", "Use uma cestinha para a compra.", "/tʃesˈtino/", "m", "cestini"),
    ("busta", "sacola", "oggetti", "Vuoi una busta per la spesa?", "Você quer uma sacola para a compra?", "/ˈbusta/", "f", "buste"),
    ("spesa", "compras (de supermercado)", "oggetti", "Fare la spesa al mercato.", "Fazer as compras no mercado.", "/ˈspeza/", "f", "spese"),
    ("spese", "despesas", "denaro", "Avere troppe spese.", "Ter demasiadas despesas.", "/ˈspeze/", "f", "spese"),
    ("garanzia", "garantia", "oggetti", "Il televisore è in garanzia.", "A televisão está na garantia.", "/ɡaranˈtsia/", "f", "garanzie"),
    
    # Verbi
    ("comprare", "comprar", "verbi", "Voglio comprare un libro.", "Quero comprar um livro.", "/komˈprare/", None, None),
    ("acquistare", "adquirir/comprar", "verbi", "Acquistare una casa.", "Adquirir uma casa.", "/akkwisˈtare/", None, None),
    ("vendere", "vender", "verbi", "Lui vuole vendere la sua auto.", "Ele quer vender o carro dele.", "/ˈvendere/", None, None),
    ("pagare", "pagar", "verbi", "Posso pagare in contanti?", "Posso pagar em dinheiro vivo?", "/paˈɡare/", None, None),
    ("spendere", "gastar", "verbi", "Non devi spendere troppo.", "Você não deve gastar muito.", "/ˈspɛndere/", None, None),
    ("costare", "custar", "verbi", "Quanto costa questo orologio?", "Quanto custa este relógio?", "/kosˈtare/", None, None),
    ("risparmiare", "economizar/poupar", "verbi", "Devo risparmiare per il viaggio.", "Devo economizar para a viagem.", "/risparˈmjare/", None, None),
    ("restituire", "devolver", "verbi", "Posso restituire l'articolo?", "Posso devolver o artigo?", "/restituˈire/", None, None),
    ("cambiare", "trocar/mudar", "verbi", "Posso cambiare questa maglia?", "Posso trocar esta blusa?", "/kamˈbjare/", None, None),
    ("provare", "provar", "verbi", "Posso provare queste scarpe?", "Posso provar estes sapatos?", "/proˈvare/", None, None),
    ("valere", "valer", "verbi", "Non vale la pena.", "Não vale a pena.", "/vaˈlere/", None, None),
    ("prestare", "emprestar", "verbi", "Mi puoi prestare venti euro?", "Você pode me emprestar vinte euros?", "/presˈtare/", None, None),
    ("guadagnare", "ganhar (dinheiro)", "verbi", "Lui guadagna molto bene.", "Ele ganha muito bem.", "/ɡwadaɲˈɲare/", None, None),
    ("investire", "investir", "verbi", "Investire in borsa.", "Investir na bolsa.", "/invesˈtire/", None, None),
    ("sprecare", "desperdiçar", "verbi", "Non sprecare i tuoi soldi.", "Não desperdice o seu dinheiro.", "/spreˈkare/", None, None),
    ("contrattare", "pechinchar", "verbi", "Al mercato si può contrattare.", "No mercado se pode pechinchar.", "/kontratˈtare/", None, None),
    
    # Aggettivi e Altro
    ("costoso", "caro", "aggettivi", "Questo ristorante è molto costoso.", "Este restaurante é muito caro.", "/kosˈtozo/", "m", "costosi"),
    ("caro", "caro", "aggettivi", "Tutto è così caro oggi.", "Tudo é tão caro hoje.", "/ˈkaro/", "m", "cari"),
    ("economico", "barato", "aggettivi", "Cerco un hotel economico.", "Procuro um hotel barato.", "/ekoˈnɔmiko/", "m", "economici"),
    ("gratis", "grátis", "aggettivi", "L'ingresso è gratis per i bambini.", "A entrada é grátis para as crianças.", "/ˈɡratis/", None, None),
    ("gratuito", "gratuito", "aggettivi", "Il parcheggio è gratuito.", "O estacionamento é gratuito.", "/ɡraˈtuito/", "m", "gratuiti"),
    ("caro", "prezado (formal)", "aggettivi", "Caro cliente.", "Prezado cliente.", "/ˈkaro/", "m", "cari"),
    ("nuovo", "novo", "aggettivi", "Comprato nuovo, mai usato.", "Comprado novo, nunca usado.", "/ˈnwɔvo/", "m", "nuovi"),
    ("usato", "usado", "aggettivi", "Un negozio di abiti usati.", "Uma loja de roupas usadas.", "/uˈzato/", "m", "usati"),
    ("esaurito", "esgotado", "aggettivi", "Il libro è andato esaurito.", "O livro está esgotado.", "/ezauˈrito/", "m", "esauriti"),
    ("difettoso", "com defeito", "aggettivi", "Questo cellulare è difettoso.", "Este celular está com defeito.", "/difetˈtozo/", "m", "difettosi"),
    ("autentico", "autêntico", "aggettivi", "Una borsa di pelle autentica.", "Uma bolsa de couro autêntica.", "/auˈtɛntiko/", "m", "autentici"),
    ("falso", "falso", "aggettivi", "Ha pagato con una banconota falsa.", "Ele pagou com uma cédula falsa.", "/ˈfalso/", "m", "falsi")
]

def create_new(templo_num, nome, citta, livello, parole_data):
    palavras = []
    for i, (it, pt, cat, ex_it, ex_pt, ipa, gen, pl) in enumerate(parole_data, 1):
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
    print(f"CREATED templo-{templo_num}.json -- {len(palavras)} parole")

if __name__ == "__main__":
    create_new(24, "La Tecnologia Moderna", "Milano", "B1", t24_data)
    create_new(25, "Il Commercio e i Soldi", "Genova", "A2", t25_data)
