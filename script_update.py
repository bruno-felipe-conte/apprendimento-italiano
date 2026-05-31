import json
import codecs

with codecs.open('data/mod2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

replacements = {
    "b1-i": {
        "tabela_visual": "<p class=\"tabela-intro\">Tabela de consulta rapida — Il mondo digitale e i social media</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Italianizacao</div><div class=\"ac-body\">Verbo ingles + -are (ex: chattare, postare)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Genero dos Anglicismos</div><div class=\"ac-body\">Usa a regra normal (il selfie, lo screenshot)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Plurais Ingleses</div><div class=\"ac-body\">Invariaveis (i like, i follower)</div></div></div>",
        "observacao_cards": [
            {"italiano": "Ho postato una foto.", "traducao": "Postei uma foto.", "artigo": "📌", "genero": "importante", "motivo": "Uso de verbo adaptado do ingles com sufixo -are."},
            {"italiano": "I follower sono tanti.", "traducao": "Os seguidores sao muitos.", "artigo": "⚠️", "genero": "regra", "motivo": "Emprestimos ingleses nao ganham -s de plural em italiano."},
            {"italiano": "Penso che i social siano utili.", "traducao": "Acho que as redes sociais sao uteis.", "artigo": "💡", "genero": "dica", "motivo": "Verbos de opiniao exigem o congiuntivo na oracao subordinada."}
        ],
        "armadilhas": [
            {"errado": "I likes", "certo": "I like", "motivo": "Palavras estrangeiras adotadas em italiano sao invariaveis no plural."},
            {"errado": "Downloadare", "certo": "Scaricare", "motivo": "Embora o italiano crie neologismos (chattare), prefere-se usar o termo italiano puro quando existe (scaricare em vez de downloadare) no discurso mais formal."}
        ]
    },
    "b1-ii": {
        "tabela_visual": "<p class=\"tabela-intro\">Tabela de consulta rapida — Ambiente di lavoro e linguaggio professionale</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Abertura de Email</div><div class=\"ac-body\">Gentile + Titulo + Sobrenome</div></div><div class=\"ac-card\"><div class=\"ac-head\">Pedidos Polidos</div><div class=\"ac-body\">Condicional (Potrebbe...)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Encerramento</div><div class=\"ac-body\">Cordiali saluti</div></div></div>",
        "observacao_cards": [
            {"italiano": "Gentile Dottor Rossi", "traducao": "Prezado Doutor Rossi", "artigo": "📌", "genero": "regra", "motivo": "Obrigatorio o uso de titulo academico e 'Gentile' em e-mails formais."},
            {"italiano": "Potrebbe inviarmi il documento?", "traducao": "Poderia me enviar o documento?", "artigo": "💡", "genero": "dica", "motivo": "Uso do condicional para suavizar pedidos no ambiente profissional."},
            {"italiano": "La riunione è stata rinviata.", "traducao": "A reuniao foi adiada.", "artigo": "⚠️", "genero": "importante", "motivo": "A voz passiva e muito comum no discurso corporativo para despersonalizar acoes."}
        ],
        "armadilhas": [
            {"errado": "Caro Dottor Rossi", "certo": "Gentile Dottor Rossi", "motivo": "'Caro' e usado apenas para pessoas com as quais voce tem intimidade. Em contexto formal, use 'Gentile'."},
            {"errado": "Può darmi...", "certo": "Potrebbe darmi...", "motivo": "O presente indicativo ('può') soa muito direto e pouco cortes num pedido formal. Prefira o condizionale ('potrebbe')."}
        ]
    },
    "b1-iii": {
        "tabela_visual": "<p class=\"tabela-intro\">Tabela de consulta rapida — Cultura e societa italiana</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Concessao</div><div class=\"ac-body\">Nonostante / Sebbene + Congiuntivo</div></div><div class=\"ac-card\"><div class=\"ac-head\">Oposicao</div><div class=\"ac-body\">Da un lato... dall'altro</div></div><div class=\"ac-card\"><div class=\"ac-head\">Mudanca de Estado</div><div class=\"ac-body\">Cambiare com essere ou avere</div></div></div>",
        "observacao_cards": [
            {"italiano": "Nonostante sia tardi...", "traducao": "Apesar de ser tarde...", "artigo": "📌", "genero": "regra", "motivo": "Conjuncoes concessivas exigem o modo congiuntivo."},
            {"italiano": "Il paese è cambiato.", "traducao": "O pais mudou.", "artigo": "⚠️", "genero": "importante", "motivo": "O verbo 'cambiare' exige o auxiliar 'essere' quando a mudanca afeta o proprio sujeito."},
            {"italiano": "Ha cambiato lavoro.", "traducao": "Ele trocou de emprego.", "artigo": "💡", "genero": "dica", "motivo": "'Cambiare' exige 'avere' quando significa trocar ou modificar alguma coisa (objeto direto)."}
        ],
        "armadilhas": [
            {"errado": "Nonostante è...", "certo": "Nonostante sia...", "motivo": "Em portugues usamos o indicativo ou infinitivo com 'apesar de', mas em italiano exige-se o congiuntivo."},
            {"errado": "Il mondo ha cambiato.", "certo": "Il mondo è cambiato.", "motivo": "Quando a mudanca ocorre por si so (intransitivo), deve-se usar o auxiliar 'essere'."}
        ]
    },
    "b1-iv": {
        "tabela_visual": "<p class=\"tabela-intro\">Tabela de consulta rapida — Expressar Opinioes</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Subjetivo</div><div class=\"ac-body\">Credo che + Congiuntivo</div></div><div class=\"ac-card\"><div class=\"ac-head\">Objetivo</div><div class=\"ac-body\">È evidente che + Indicativo</div></div><div class=\"ac-card\"><div class=\"ac-head\">Oposicao</div><div class=\"ac-body\">Tuttavia / Eppure</div></div></div>",
        "observacao_cards": [
            {"italiano": "Penso che sia vero.", "traducao": "Acho que e verdade.", "artigo": "📌", "genero": "regra", "motivo": "Verbos de opiniao requerem o congiuntivo para indicar subjetividade."},
            {"italiano": "È evidente che hai ragione.", "traducao": "E evidente que tens razao.", "artigo": "⚠️", "genero": "importante", "motivo": "Expressoes de certeza e objetividade exigem o indicativo."},
            {"italiano": "Non credo che lui venga.", "traducao": "Nao acredito que ele venha.", "artigo": "💡", "genero": "dica", "motivo": "A negacao de uma opiniao ('non credo') tambem exige o congiuntivo."}
        ],
        "armadilhas": [
            {"errado": "Penso che è...", "certo": "Penso che sia...", "motivo": "Um dos erros mais comuns de estrangeiros (e ate nativos). Opiniao pessoal pede congiuntivo."},
            {"errado": "È ovvio che sia...", "certo": "È ovvio che è...", "motivo": "Certezas impessoais ('è ovvio', 'è certo') levam indicativo, pois nao deixam margem para duvida."}
        ]
    },
    "b1-v": {
        "tabela_visual": "<p class=\"tabela-intro\">Tabela de consulta rapida — Italiano regional</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Norte</div><div class=\"ac-body\">Vogais mais fechadas, ritmo rapido</div></div><div class=\"ac-card\"><div class=\"ac-head\">Sul</div><div class=\"ac-body\">Vogais abertas, consoantes fortes</div></div><div class=\"ac-card\"><div class=\"ac-head\">Generalizacao</div><div class=\"ac-body\">Si + verbo (Si mangia bene)</div></div></div>",
        "observacao_cards": [
            {"italiano": "In Italia si mangia bene.", "traducao": "Na Italia come-se bem.", "artigo": "📌", "genero": "regra", "motivo": "O 'si impersonale' e muito usado para falar de habitos culturais."},
            {"italiano": "Non ho capito bene.", "traducao": "Nao entendi bem.", "artigo": "💡", "genero": "dica", "motivo": "Frase essencial para lidar com forte sotaque regional ou dialeto."},
            {"italiano": "È un bel casino.", "traducao": "E uma bela bagunca.", "artigo": "⚠️", "genero": "importante", "motivo": "Palavra informal usada em toda a Italia que perdeu o sentido original (bordel) e hoje significa confusao."}
        ],
        "armadilhas": [
            {"errado": "Noi si mangia...", "certo": "Noi mangiamo... ou Si mangia...", "motivo": "Na Toscana usa-se 'noi si mangia', mas no italiano standard isso e gramaticalmente incorreto."},
            {"errado": "Dialetto", "certo": "Italiano regionale / Dialetto", "motivo": "Nao confunda 'italiano regional' (italiano com sotaque local) com 'dialeto' (uma lingua separada com sua propria gramatica e vocabulario)."}
        ]
    },
    "b1-vi": {
        "tabela_visual": "<p class=\"tabela-intro\">Tabela de consulta rapida — Il Congiuntivo Presente</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">-ARE (parlare)</div><div class=\"ac-body\">io parli, tu parli, lui parli</div></div><div class=\"ac-card\"><div class=\"ac-head\">-ERE (leggere)</div><div class=\"ac-body\">io legga, tu legga, lui legga</div></div><div class=\"ac-card\"><div class=\"ac-head\">-IRE (partire)</div><div class=\"ac-body\">io parta, tu parta, lui parta</div></div></div>",
        "observacao_cards": [
            {"italiano": "Spero che tu capisca.", "traducao": "Espero que entendas.", "artigo": "📌", "genero": "regra", "motivo": "Verbos em -ere e -ire terminam em -a nas tres primeiras pessoas do singular."},
            {"italiano": "Penso che lui parli.", "traducao": "Acho que ele fala.", "artigo": "💡", "genero": "dica", "motivo": "Verbos em -are terminam em -i nas tres primeiras pessoas do singular do congiuntivo."},
            {"italiano": "È importante che andiamo.", "traducao": "E importante que nos vamos.", "artigo": "⚠️", "genero": "importante", "motivo": "A forma de 'noi' no congiuntivo presente e identica ao indicativo presente (-iamo)."}
        ],
        "armadilhas": [
            {"errado": "Spero che lui capisce.", "certo": "Spero che lui capisca.", "motivo": "O verbo sperare exige o congiuntivo na oracao subordinada, nao o indicativo."},
            {"errado": "Credo che parliamo", "certo": "Credo che parliamo", "motivo": "Neste caso a forma esta correta (identica ao indicativo), a armadilha e achar que ha uma forma diferente para 'noi' no congiuntivo presente."}
        ]
    },
    "b1-vii": {
        "tabela_visual": "<p class=\"tabela-intro\">Tabela de consulta rapida — Il Condizionale Presente</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Radical (parlare)</div><div class=\"ac-body\">parler- (o 'a' vira 'e')</div></div><div class=\"ac-card\"><div class=\"ac-head\">Terminacoes</div><div class=\"ac-body\">-ei, -esti, -ebbe, -emmo, -este, -ebbero</div></div><div class=\"ac-card\"><div class=\"ac-head\">Verbos em -ire</div><div class=\"ac-body\">partire → partirei (nao muda vogal)</div></div></div>",
        "observacao_cards": [
            {"italiano": "Io mangerei un gelato.", "traducao": "Eu comeria um sorvete.", "artigo": "📌", "genero": "regra", "motivo": "A maioria dos verbos em -are muda o 'a' para 'e' no radical (mangiare -> mangerei)."},
            {"italiano": "Vorrei un caffè.", "traducao": "Eu gostaria de um cafe.", "artigo": "💡", "genero": "dica", "motivo": "'Vorrei' (de volere) e a forma mais comum para pedir algo de forma educada."},
            {"italiano": "Andrebbe a Roma se potesse.", "traducao": "Iria a Roma se pudesse.", "artigo": "⚠️", "genero": "importante", "motivo": "O condicional e usado na oracao principal do periodo hipotetico irreal."}
        ],
        "armadilhas": [
            {"errado": "Io parlarei", "certo": "Io parlerei", "motivo": "Diferente do portugues, os verbos em -are mudam o 'a' para 'e' no condicional italiano."},
            {"errado": "Voglio un caffè", "certo": "Vorrei un caffè", "motivo": "Em bares e restaurantes italianos, 'voglio' soa rude. O condicional de cortesia ('vorrei') e fundamental."}
        ]
    },
    "b1-viii": {
        "tabela_visual": "<p class=\"tabela-intro\">Tabela de consulta rapida — I Pronomi Relativi</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Suj/Obj Direto</div><div class=\"ac-body\">Che (invariavel)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Com Preposicao</div><div class=\"ac-body\">Cui (invariavel)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Posse</div><div class=\"ac-body\">Il cui / la cui / i cui / le cui</div></div></div>",
        "observacao_cards": [
            {"italiano": "Il libro che leggo.", "traducao": "O livro que eu leio.", "artigo": "📌", "genero": "regra", "motivo": "'Che' funciona como sujeito ou objeto direto e nao aceita preposicao."},
            {"italiano": "L'amico con cui esco.", "traducao": "O amigo com quem eu saio.", "artigo": "💡", "genero": "dica", "motivo": "'Cui' e sempre precedido por uma preposicao (con, di, a, per, etc.)."},
            {"italiano": "La ragazza il cui padre è medico.", "traducao": "A garota cujo pai e medico.", "artigo": "⚠️", "genero": "importante", "motivo": "'Cui' precedido de artigo definido equivale a 'cujo(s)/cuja(s)'. O artigo concorda com a coisa possuida."}
        ],
        "armadilhas": [
            {"errado": "La persona che parlo.", "certo": "La persona con cui parlo.", "motivo": "Em italiano nao se pode usar 'che' com preposicao implicita. E preciso usar a preposicao + 'cui'."},
            {"errado": "L'uomo il quale libro...", "certo": "L'uomo il cui libro...", "motivo": "Para posse (cujo), a estrutura e sempre Artigo + cui + Substantivo possuido."}
        ]
    },
    "b1-ix": {
        "tabela_visual": "<p class=\"tabela-intro\">Tabela de consulta rapida — La Forma Passiva</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Presente</div><div class=\"ac-body\">è mangiato/a/i/e (da)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Passato Prossimo</div><div class=\"ac-body\">è stato mangiato/a (da)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Auxiliar Venire</div><div class=\"ac-body\">Viene mangiato (enfatiza acao)</div></div></div>",
        "observacao_cards": [
            {"italiano": "La mela è mangiata da me.", "traducao": "A maca e comida por mim.", "artigo": "📌", "genero": "regra", "motivo": "Forma passiva basica usa o auxiliar 'essere' mais o participio passado, concordando em genero e numero."},
            {"italiano": "La casa è stata venduta.", "traducao": "A casa foi vendida.", "artigo": "💡", "genero": "dica", "motivo": "No passato prossimo o auxiliar 'essere' fica 'è stato', resultando em uma estrutura tripla (è + stato + participio)."},
            {"italiano": "La porta viene aperta.", "traducao": "A porta e (esta sendo) aberta.", "artigo": "⚠️", "genero": "importante", "motivo": "O verbo 'venire' e frequentemente usado no lugar de 'essere' nos tempos simples para enfatizar que a acao esta ocorrendo."}
        ],
        "armadilhas": [
            {"errado": "Il libro è statato scritto.", "certo": "Il libro è stato scritto.", "motivo": "Atencao a dupla forma participial: essere -> stato, scrivere -> scritto. Em portugues dizemos apenas 'foi escrito'."},
            {"errado": "La mela ha mangiata dal bambino.", "certo": "La mela è (stata) mangiata dal bambino.", "motivo": "A voz passiva NUNCA se forma com o auxiliar 'avere'."}
        ]
    },
    "b1-x": {
        "tabela_visual": "<p class=\"tabela-intro\">Tabela de consulta rapida — Il Gerundio</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">-ARE (parlare)</div><div class=\"ac-body\">parlando</div></div><div class=\"ac-card\"><div class=\"ac-head\">-ERE / -IRE</div><div class=\"ac-body\">leggendo / partendo</div></div><div class=\"ac-card\"><div class=\"ac-head\">Stare + Gerundio</div><div class=\"ac-body\">Sto mangiando (acao em progresso)</div></div></div>",
        "observacao_cards": [
            {"italiano": "Sto studiando l'italiano.", "traducao": "Estou estudando italiano.", "artigo": "📌", "genero": "regra", "motivo": "A estrutura stare + gerundio e o presente continuo, usada para acoes que ocorrem no exato momento da fala."},
            {"italiano": "Passeggiando, ho visto Marco.", "traducao": "Passeando, vi o Marco.", "artigo": "💡", "genero": "dica", "motivo": "O gerundio sozinho expressa uma acao simultanea (causal ou temporal) que partilha do mesmo sujeito da oracao principal."},
            {"italiano": "Facendo / Dicendo / Bevendo", "traducao": "Fazendo / Dizendo / Bebendo", "artigo": "⚠️", "genero": "importante", "motivo": "Os verbos fare, dire e bere formam o gerundio a partir da raiz antiga (facere, dicere, bevere)."}
        ],
        "armadilhas": [
            {"errado": "Stavo per studiando...", "certo": "Stavo studiando / Stavo per studiare", "motivo": "'Stare per' exige o infinito (acao prestes a acontecer), enquanto 'Stare + gerundio' e a acao ja em progresso."},
            {"errado": "Io vedendo il film, il telefono ha squillato.", "certo": "Mentre vedevo il film, il telefono ha squillato.", "motivo": "O gerundio absoluto (sem estar ligado ao sujeito da oracao principal) soa estranho; evite se os sujeitos forem diferentes."}
        ]
    },
    "b1-xi": {
        "tabela_visual": "<p class=\"tabela-intro\">Tabela de consulta rapida — Congiuntivo Imperfetto</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">-ARE (parlare)</div><div class=\"ac-body\">parlassi, parlassi, parlasse, parlassimo...</div></div><div class=\"ac-card\"><div class=\"ac-head\">-ERE (credere)</div><div class=\"ac-body\">credessi, credessi, credesse, credessimo...</div></div><div class=\"ac-card\"><div class=\"ac-head\">-IRE (sentire)</div><div class=\"ac-body\">sentissi, sentissi, sentisse, sentissimo...</div></div></div>",
        "observacao_cards": [
            {"italiano": "Credevo che lui andasse a Roma.", "traducao": "Eu achava que ele ia a Roma.", "artigo": "📌", "genero": "regra", "motivo": "Se o verbo principal esta no passado (credevo) e exige congiuntivo, usa-se o congiuntivo imperfetto para a mesma epoca."},
            {"italiano": "Se avessi soldi, viaggerei.", "traducao": "Se eu tivesse dinheiro, viajaria.", "artigo": "💡", "genero": "dica", "motivo": "E a estrutura chave do 'periodo ipotetico' da impossibilidade/hipotese no presente (Se + cong. imperfetto, condizionale presente)."},
            {"italiano": "Fossi, fossi, fosse...", "traducao": "Fosse, fosse, fosse...", "artigo": "⚠️", "genero": "importante", "motivo": "O verbo 'essere' tem formas bem proprias (fossi, fosse, fossimo, foste, fossero)."}
        ],
        "armadilhas": [
            {"errado": "Se io avrei tempo...", "certo": "Se io avessi tempo...", "motivo": "Erro gravissimo (o classico 'erro do condicional no lugar do congiuntivo'). Depois do 'se' hipotetico nunca se usa o condicional, apenas o congiuntivo."},
            {"errado": "Pensavo che lui viene.", "certo": "Pensavo che lui venisse.", "motivo": "O indicativo depois de um verbo de opiniao no passado e um erro. A concordancia dos tempos verbais exige o congiuntivo imperfetto."}
        ]
    },
    "b1-xii": {
        "tabela_visual": "<p class=\"tabela-intro\">Tabela de consulta rapida — I Modali al Passato</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Com Avere</div><div class=\"ac-body\">Ho dovuto mangiare (verbo princ. usa avere)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Com Essere</div><div class=\"ac-body\">Sono dovuto andare (verbo princ. usa essere)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Pronominais</div><div class=\"ac-body\">Mi sono dovuto alzare / Ho dovuto alzarmi</div></div></div>",
        "observacao_cards": [
            {"italiano": "Ho voluto mangiare una pizza.", "traducao": "Eu quis comer uma pizza.", "artigo": "📌", "genero": "regra", "motivo": "O verbo modal 'volere' toma emprestado o auxiliar do verbo principal ('mangiare' exige 'avere')."},
            {"italiano": "Sono dovuto partire presto.", "traducao": "Eu tive que partir cedo.", "artigo": "💡", "genero": "dica", "motivo": "Como 'partire' exige 'essere', o modal 'dovere' acompanha a regra e tambem usa 'essere'."},
            {"italiano": "Non ci sono potuto andare.", "traducao": "Nao pude ir (la).", "artigo": "⚠️", "genero": "importante", "motivo": "Se houver um pronome atono (ci, mi, ti, lo) antes do verbo, o auxiliar OBRIGATORIAMENTE sera 'essere' (se o verbo pedir essere)."}
        ],
        "armadilhas": [
            {"errado": "Ho dovuto partire.", "certo": "Sono dovuto partire. / Ho dovuto partire (aceito mas menos elegante).", "motivo": "A regra classica exige 'essere' quando o verbo no infinitivo exige 'essere'. Contudo, na lingua falada moderna, usar 'avere' com modais e cada vez mais tolerado."},
            {"errado": "Mi ho potuto lavare.", "certo": "Mi sono potuto lavare. / Ho potuto lavarmi.", "motivo": "Com verbos reflexivos, se o pronome reflexivo (mi) vem antes do auxiliar, usa-se 'essere'. Se vai anexado ao infinitivo, usa-se 'avere'."}
        ]
    }
}

for u in data.get('unidades', []):
    uid = u['id']
    if uid in replacements:
        u['tabela_visual'] = replacements[uid]['tabela_visual']
        u['observacao_cards'] = replacements[uid]['observacao_cards']
        u['armadilhas'] = replacements[uid]['armadilhas']

with codecs.open('data/mod2_final.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("SUCCESS: data/mod2_final.json written!")
