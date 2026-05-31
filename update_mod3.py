import json

filepath = 'c:/Users/bruno/Documents/italian-learning-app-pro/data/mod3.json'
outpath = 'c:/Users/bruno/Documents/italian-learning-app-pro/data/mod3_final.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# The content mapping
updates = {
    "b2-i": {
        "observacao_cards": [
            {
                "italiano": "Se Dante fosse vissuto oggi, avrebbe scritto un blog.",
                "traducao": "Se Dante tivesse vivido hoje, teria escrito um blog.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Período hipotético da irrealidade no passado exige Congiuntivo Trapassato na condição e Condizionale Passato na consequência."
            },
            {
                "italiano": "L'autore diceva che l'opera fosse completa.",
                "traducao": "O autor dizia que a obra estava completa.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Discurso indireto introduzido por um verbo no passado ('diceva') exige Congiuntivo Imperfetto (ação simultânea) ou Trapassato (anterioridade)."
            }
        ],
        "armadilhas": [
            {
                "errado": "Se avesse vissuto oggi...",
                "certo": "Se fosse vissuto oggi...",
                "motivo": "Vivere em tempos compostos usa o auxiliar 'essere' quando indica a existência da pessoa. 'Avere' é usado mais raramente, quando é transitivo (ex: ha vissuto una bella vita)."
            },
            {
                "errado": "La Divina Commedia ha stata scritta...",
                "certo": "La Divina Commedia è stata scritta...",
                "motivo": "A voz passiva sempre exige o verbo auxiliar 'essere', nunca 'avere'."
            }
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Construções da Literatura Clássica Italiana</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Hipótese Passada</div><div class=\"ac-body\">se + cong. trapassato &rarr; cond. passato</div></div><div class=\"ac-card\"><div class=\"ac-head\">Discurso Indireto Passado</div><div class=\"ac-body\">verbo passato + che + cong. imperfetto/trapassato</div></div></div>"
    },
    "b2-ii": {
        "observacao_cards": [
            {
                "italiano": "Crollo delle borse: persi 200 miliardi.",
                "traducao": "Queda das bolsas: perdidos 200 bilhões.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Os 'Titoli nominali' (manchetes nominais) omitem verbos como 'essere' e sujeitos óbvios para causar impacto e poupar espaço impresso."
            },
            {
                "italiano": "Secondo fonti vicine al governo, la manovra sarebbe pronta.",
                "traducao": "Segundo fontes próximas ao governo, a medida estaria pronta.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Condizionale di dissociazione: usado no jornalismo para noticiar informações que ainda não foram oficialmente confirmadas."
            }
        ],
        "armadilhas": [
            {
                "errado": "I carabinieri hanno arrestato due persone. (Em manchetes jornalísticas)",
                "certo": "Carabinieri: arrestati due sospetti. / Due arresti dai carabinieri.",
                "motivo": "Em títulos jornalísticos, evita-se a voz ativa padrão, optando por frases curtas centradas em substantivos ou no particípio passado passivo."
            },
            {
                "errado": "Governo è approvato la legge.",
                "certo": "Il governo ha approvato la legge. / Approvata la legge dal governo.",
                "motivo": "A passiva com o particípio solto na manchete pode confundir. 'Il governo ha approvato' ou a passiva 'La legge è stata approvata'."
            }
        ],
        "tabela_visual": "<p class=\"tabela-intro\">O Vocabulário Jornalístico (5W + Condizionale)</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Titolo Nominale</div><div class=\"ac-body\">Omissão de auxiliares e artigos (Sostantivo + Participio)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Condizionale Jornalístico</div><div class=\"ac-body\">Uso para indicar incerteza (secondo indiscrezioni)</div></div></div>"
    },
    "b2-iii": {
        "observacao_cards": [
            {
                "italiano": "L'azienda ha aumentato i prezzi.",
                "traducao": "A empresa aumentou os preços.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "O verbo 'aumentare', quando transitivo direto (tem objeto), exige sempre o auxiliar 'avere'."
            },
            {
                "italiano": "Il fatturato è aumentato del 10%.",
                "traducao": "O faturamento aumentou 10%.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Quando 'aumentare' é intransitivo (o sujeito em si aumentou de tamanho/valor), o auxiliar é 'essere'."
            }
        ],
        "armadilhas": [
            {
                "errado": "Il bilancio ha cresciuto.",
                "certo": "Il bilancio è cresciuto.",
                "motivo": "O verbo 'crescere' em contextos financeiros e em geral é intransitivo, exigindo o auxiliar 'essere'."
            },
            {
                "errado": "Facciamo questo per che il progetto abbia successo.",
                "certo": "Facciamo questo affinché il progetto abbia successo.",
                "motivo": "No ambiente corporativo formal, usa-se 'affinché' ('a fim de que') no lugar do coloquial 'perché' para finalidade."
            }
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Vocabulário de Negócios e Transições Formais</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Finalidade Formal</div><div class=\"ac-body\">affinché + congiuntivo</div></div><div class=\"ac-card\"><div class=\"ac-head\">Hipótese de Negócios</div><div class=\"ac-body\">qualora + congiuntivo</div></div></div>"
    },
    "b2-iv": {
        "observacao_cards": [
            {
                "italiano": "Il governo ha perso la fiducia e si va alle urne.",
                "traducao": "O governo perdeu a moção de confiança e vai-se às urnas.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "A estabilidade política usa verbos fundamentais (fiducia/sfiducia) e o destino final em caso de crise política é sempre 'alle urne' (eleições)."
            },
            {
                "italiano": "La proposta è stata promulgata dal Presidente della Repubblica.",
                "traducao": "A proposta foi promulgada pelo Presidente da República.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "O passivo institucional impessoal ('è stato promulgato', 'verrà approvato') é o motor dos textos oficiais da política."
            }
        ],
        "armadilhas": [
            {
                "errado": "La Camera delle Deputate ha votato.",
                "certo": "La Camera dei Deputati ha votato.",
                "motivo": "O termo oficial é 'Camera dei Deputati' (masculino genérico universal), representando a câmara baixa da Itália."
            },
            {
                "errado": "Il ministro ha detto che la legge è buona.",
                "certo": "Il ministro ha dichiarato che la legge fosse essenziale.",
                "motivo": "No jargão político, não se diz apenas 'dire'. Usa-se 'dichiarare' ou 'affermare' junto ao congiuntivo do discurso indireto."
            }
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Estrutura Política e Palavras-Chave</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Parlamento (Legislativo)</div><div class=\"ac-body\">Camera dei Deputati + Senato della Repubblica</div></div><div class=\"ac-card\"><div class=\"ac-head\">Governo (Executivo)</div><div class=\"ac-body\">Consiglio dei Ministri, liderado pelo Premier</div></div></div>"
    },
    "b2-v": {
        "observacao_cards": [
            {
                "italiano": "Il film è diretto da Paolo Sorrentino.",
                "traducao": "O filme é dirigido por Paolo Sorrentino.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Particípio irregular essencial: o particípio passado de 'dirigere' é 'diretto'."
            },
            {
                "italiano": "Si potrebbe affermare che quest'opera abbia cambiato la storia del cinema.",
                "traducao": "Poderia-se afirmar que esta obra mudou a história do cinema.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "A estrutura de impessoalidade (Si + Condizionale) torna a crítica e a opinião sofisticadas ('Si potrebbe dire/affermare/sostenere')."
            }
        ],
        "armadilhas": [
            {
                "errado": "Il film ha stato girato a Cinecittà.",
                "certo": "Il film è stato girato a Cinecittà.",
                "motivo": "A ação passiva sempre toma o auxiliar 'essere' (è stato girato = foi filmado)."
            },
            {
                "errado": "Secondo me, che il film è un capolavoro.",
                "certo": "A mio avviso, il film è un capolavoro.",
                "motivo": "Em textos críticos B2, fuja do batido 'secondo me'. Use 'A mio avviso', 'A mio parere' ou 'Dal mio punto di vista'."
            }
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Vocabulário da Crítica Cinematográfica Italiana</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Autoria/Direção</div><div class=\"ac-body\">la regia è di / è diretto da / girato da</div></div><div class=\"ac-card\"><div class=\"ac-head\">Influência</div><div class=\"ac-body\">ha segnato una svolta / considerato un capolavoro / ha aperto la strada</div></div></div>"
    },
    "b2-vi": {
        "observacao_cards": [
            {
                "italiano": "Penso che Marco sia andato a Roma.",
                "traducao": "Acho que o Marco foi a Roma.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Congiuntivo Passato denota uma ação passada ('sia andato') em relação a um verbo principal no presente ('Penso')."
            },
            {
                "italiano": "Pensavo che Marco fosse andato a Roma.",
                "traducao": "Eu achava que o Marco tivesse ido a Roma.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Congiuntivo Trapassato marca uma ação anterior a um verbo que já estava no passado ('Pensavo')."
            }
        ],
        "armadilhas": [
            {
                "errado": "Spero che lui ha capito.",
                "certo": "Spero che lui abbia capito.",
                "motivo": "Verbos de esperança ou opinião sempre puxam subjuntivo. Sendo ação concluída, o auxiliar (abbia) acompanha o particípio."
            },
            {
                "errado": "Speravo che lui abbia capito.",
                "certo": "Speravo che lui avesse capito.",
                "motivo": "Se a frase principal já está no passado (Speravo), a subordinação correta de tempo anterior precisa do Trapassato (avesse capito)."
            }
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Tempos Compostos do Subjuntivo Italiano</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Congiuntivo Passato</div><div class=\"ac-body\">Cong. Presente (abbia/sia) + Participio Passato</div></div><div class=\"ac-card\"><div class=\"ac-head\">Congiuntivo Trapassato</div><div class=\"ac-body\">Cong. Imperfetto (avesse/fosse) + Participio Passato</div></div></div>"
    },
    "b2-vii": {
        "observacao_cards": [
            {
                "italiano": "Se avessi soldi, comprerei una casa.",
                "traducao": "Se eu tivesse dinheiro, compraria uma casa.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Condição de possibilidade (2º tipo): na partícula 'se' o verbo é Congiuntivo Imperfetto. O resultado é Condizionale Presente."
            },
            {
                "italiano": "Se avessi studiato, avrei passato l'esame.",
                "traducao": "Se eu tivesse estudado, teria passado na prova.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Condição de irrealidade passada (3º tipo): usa-se o Congiuntivo Trapassato (se avessi studiato) e Condizionale Passato (avrei passato)."
            }
        ],
        "armadilhas": [
            {
                "errado": "Se io avrei tempo, andrei in vacanza.",
                "certo": "Se io avessi tempo, andrei in vacanza.",
                "motivo": "O erro de usar 'Condizionale' logo depois do 'se' é tão temido na Itália que vira meme. Após 'Se' hipotético, a estrutura exige SEMPRE Congiuntivo."
            },
            {
                "errado": "Se studierei di più, passerei l'esame.",
                "certo": "Se studiassi di più, passerei l'esame.",
                "motivo": "Mesma regra de ouro: 'studierei' é condicional. O correto é a forma do subjuntivo imperfeito 'studiassi'."
            }
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Os Tipos do Período Hipotético</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Possibilidade Atual (Tipo 2)</div><div class=\"ac-body\">Se + Congiuntivo Imperfetto &rarr; Condizionale Presente</div></div><div class=\"ac-card\"><div class=\"ac-head\">Irrealidade Passada (Tipo 3)</div><div class=\"ac-body\">Se + Congiuntivo Trapassato &rarr; Condizionale Passato</div></div></div>"
    },
    "b2-viii": {
        "observacao_cards": [
            {
                "italiano": "Ha detto: 'Vado a casa.' &rarr; Ha detto che andava a casa.",
                "traducao": "Ele disse: 'Vou pra casa.' &rarr; Disse que ia para casa.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Ação simultânea: Quando a frase matriz está no passado (ha detto), o tempo 'Presente' muda para 'Imperfetto'."
            },
            {
                "italiano": "Disse: 'Partirò domani.' &rarr; Disse che sarebbe partito il giorno dopo.",
                "traducao": "Ele disse: 'Partirei amanhã.' &rarr; Ele disse que partiria no dia seguinte.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "O futuro do discurso direto vira Condizionale Passato (exprime futuro no passado) no discurso indireto."
            }
        ],
        "armadilhas": [
            {
                "errado": "Luigi mi ha detto che (lui) va a casa.",
                "certo": "Luigi mi ha detto che (lui) andava a casa.",
                "motivo": "A concordância temporal italiana (consecutio temporum) é rigorosa: matriz passada força o recuo do tempo do verbo subordinado (presente &rarr; imperfetto)."
            },
            {
                "errado": "Disse che lo farà domani.",
                "certo": "Disse che lo avrebbe fatto il giorno dopo.",
                "motivo": "Os advérbios e expressões de tempo também devem mudar de perspectiva (domani &rarr; il giorno seguente / il giorno dopo)."
            }
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Concordância Temporal no Discurso Indireto</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Matriz no Passato + Subordinada no Presente</div><div class=\"ac-body\">Transforma-se em Imperfetto</div></div><div class=\"ac-card\"><div class=\"ac-head\">Matriz no Passato + Subordinada no Futuro</div><div class=\"ac-body\">Transforma-se em Condizionale Passato</div></div></div>"
    },
    "b2-ix": {
        "observacao_cards": [
            {
                "italiano": "Nonostante piova, esco lo stesso.",
                "traducao": "Apesar de estar chovendo, saio mesmo assim.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Os conectivos de concessão pura (nonostante, sebbene, benché, malgrado) obrigatoriamente exigem verbo no Congiuntivo."
            },
            {
                "italiano": "Studio l'italiano affinché io possa vivere a Roma.",
                "traducao": "Estudo italiano a fim de poder viver em Roma.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "O conectivo de finalidade erudito 'affinché' também atrai exclusivamente o Congiuntivo."
            }
        ],
        "armadilhas": [
            {
                "errado": "Sebbene è stanco, lavora.",
                "certo": "Sebbene sia stanco, lavora.",
                "motivo": "O falante de português costuma errar pensando em 'apesar de (ser)'. Mas o 'sebbene' deve ser seguido do Congiuntivo (sebbene sia)."
            },
            {
                "errado": "Anche se sia difficile, lo faccio.",
                "certo": "Anche se è difficile, lo faccio.",
                "motivo": "A armadilha máxima dos exames: 'Anche se' significa 'Mesmo que' e rege o modo INDICATIVO quando retrata um fato real no presente."
            }
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Modos Verbais com Conectivos Especiais</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Exigem Congiuntivo Sempre</div><div class=\"ac-body\">Nonostante, Sebbene, Benché, Affinché, Qualora, Purché</div></div><div class=\"ac-card\"><div class=\"ac-head\">Exigem Indicativo (para fatos reais)</div><div class=\"ac-body\">Anche se, Poiché, Dal momento che, Dato che</div></div></div>"
    },
    "b2-x": {
        "observacao_cards": [
            {
                "italiano": "Dante nacque a Firenze nel 1265.",
                "traducao": "Dante nasceu em Florença em 1265.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Passato Remoto: O tempo mestre da narração de fatos acabados que já não têm ligação psicológica com o presente."
            },
            {
                "italiano": "Avendo finito di studiare, uscì.",
                "traducao": "Tendo terminado de estudar, ele saiu.",
                "artigo": "📌",
                "genero": "regra",
                "motivo": "Uso elegante do Gerúndio Composto em textos formais italianos para substituir grandes orações subordinadas de tempo ou causa."
            }
        ],
        "armadilhas": [
            {
                "errado": "Ieri andai in banca (em conversas cotidianas).",
                "certo": "Ieri sono andato in banca.",
                "motivo": "Para os italianos do Norte e Centro da Itália, o passato remoto na fala diária soa excessivamente erudito ou obsoleto. Para as ações do dia a dia, usa-se o passato prossimo."
            },
            {
                "errado": "Dopo di aver fatto questo...",
                "certo": "Dopo aver fatto questo...",
                "motivo": "Uma falsa tradução do 'depois de'. Em italiano formal (e informal), 'Dopo' liga-se diretamente ao verbo no infinitivo composto: 'Dopo aver', 'Dopo esserci andato'."
            }
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Marcadores do Estilo Literário e Elevado</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Tempo Narrativo Histórico</div><div class=\"ac-body\">Passato Remoto (Ação Principal) vs Imperfetto (Cenário)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Construções Subordinadas Sintéticas</div><div class=\"ac-body\">Gerúndio (Essendo uscito) / Infinito Passato (Dopo aver letto) / Participio Assoluto (Finito il lavoro)</div></div></div>"
    }
}

for u in data.get('unidades', []):
    uid = u.get('id')
    if uid in updates:
        u['observacao_cards'] = updates[uid]['observacao_cards']
        u['armadilhas'] = updates[uid]['armadilhas']
        u['tabela_visual'] = updates[uid]['tabela_visual']

with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("SUCCESS")
