import json

data_updates = {
    "a2-i": {
        "observacao_cards": [
            {"italiano": "Vorrei un tavolo", "traducao": "Eu gostaria de uma mesa", "artigo": "📌", "genero": "regra", "motivo": "Usa-se o condicional 'vorrei' por educação em vez de 'voglio'."},
            {"italiano": "Prendo un caffè", "traducao": "Vou querer um café", "artigo": "📌", "genero": "regra", "motivo": "'Prendere' é extremamente comum para fazer pedidos diretos."}
        ],
        "armadilhas": [
            {"errado": "Voglio un caffè", "certo": "Vorrei un caffè", "motivo": "Em italiano, 'voglio' (eu quero) soa imperativo e grosseiro no comércio. Use 'vorrei'."},
            {"errado": "Il conto, per favore?", "certo": "Il conto, per favore", "motivo": "Não se costuma pedir a conta com 'posso avere' ou outras fórmulas longas. Seja direto: 'Il conto, per favore'."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Pedindo no Bar e Restaurante</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Vorrei...</div><div class=\"ac-body\">Mais formal e polido. Ex: Vorrei il menù.</div></div><div class=\"ac-card\"><div class=\"ac-head\">Prendo...</div><div class=\"ac-body\">Direto mas perfeitamente aceito. Ex: Prendo la pasta.</div></div></div>"
    },
    "a2-ii": {
        "observacao_cards": [
            {"italiano": "Scusi, dov'è...", "traducao": "Com licença, onde é...", "artigo": "📌", "genero": "regra", "motivo": "Para parar desconhecidos na rua, usa-se 'Scusi' (formal)."},
            {"italiano": "Vada dritto", "traducao": "Vá em frente", "artigo": "📌", "genero": "regra", "motivo": "'Vada' é o imperativo formal (Lei) do verbo andare."}
        ],
        "armadilhas": [
            {"errado": "Scusa, dov'è...", "certo": "Scusi, dov'è...", "motivo": "'Scusa' é informal (tu). Para perguntar direções na rua a desconhecidos, use sempre 'Scusi' (Lei)."},
            {"errado": "Gira a destra", "certo": "Giri a destra", "motivo": "Mesmo motivo. 'Giri' é a forma de tratamento formal (Lei) adequada para estranhos."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Direções e Movimento</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Sempre dritto</div><div class=\"ac-body\">Sempre em frente</div></div><div class=\"ac-card\"><div class=\"ac-head\">A destra/sinistra</div><div class=\"ac-body\">Para a direita/esquerda</div></div></div>"
    },
    "a2-iii": {
        "observacao_cards": [
            {"italiano": "Faccio il medico", "traducao": "Sou médico (lit: faço o médico)", "artigo": "📌", "genero": "regra", "motivo": "Com o verbo 'fare', usamos artigo definido antes da profissão."},
            {"italiano": "Sono medico", "traducao": "Sou médico", "artigo": "📌", "genero": "regra", "motivo": "Com o verbo 'essere', omitimos o artigo antes da profissão."}
        ],
        "armadilhas": [
            {"errado": "Sono un medico", "certo": "Sono medico / Faccio il medico", "motivo": "Ao contrário do português, pode-se usar 'sono + profissão' sem artigo, ou 'faccio + artigo + profissão'."},
            {"errado": "Lavoro di ingegnere", "certo": "Lavoro come ingegnere", "motivo": "Usa-se 'come' para indicar o papel ou profissão atual."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Profissões e Trabalho</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Fare il/la</div><div class=\"ac-body\">Ex: Faccio la segretaria</div></div><div class=\"ac-card\"><div class=\"ac-head\">Essere Ø</div><div class=\"ac-body\">Ex: Sono segretaria</div></div></div>"
    },
    "a2-iv": {
        "observacao_cards": [
            {"italiano": "C'è un garage", "traducao": "Tem uma garagem", "artigo": "📌", "genero": "regra", "motivo": "Usamos 'c'è' para indicar a existência de um item (singular)."},
            {"italiano": "Ci sono due bagni", "traducao": "Têm dois banheiros", "artigo": "📌", "genero": "regra", "motivo": "Usamos 'ci sono' para itens no plural."}
        ],
        "armadilhas": [
            {"errado": "Ha due bagni", "certo": "Ci sono due bagni", "motivo": "No sentido de 'existir' ou 'haver', não se usa o verbo avere ('ha'), mas sim 'esserci' (c'è/ci sono)."},
            {"errado": "Nel primo piano", "certo": "Al primo piano", "motivo": "Para andares de edifícios, usa-se a preposição articulada 'al'."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Descrevendo a Casa</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">C'è / Ci sono</div><div class=\"ac-body\">Haver/Existir (Sing/Plural)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Piano</div><div class=\"ac-body\">Al primo piano (No primeiro andar)</div></div></div>"
    },
    "a2-v": {
        "observacao_cards": [
            {"italiano": "Ho mal di testa", "traducao": "Estou com dor de cabeça", "artigo": "📌", "genero": "regra", "motivo": "A estrutura 'ho mal di + parte do corpo' é a mais comum para queixas."},
            {"italiano": "Mi fa male la schiena", "traducao": "Minhas costas doem", "artigo": "📌", "genero": "regra", "motivo": "Usamos 'mi fa male' (singular) ou 'mi fanno male' (plural)."}
        ],
        "armadilhas": [
            {"errado": "Mi duole la testa", "certo": "Ho mal di testa", "motivo": "Embora 'dolere' exista, na linguagem cotidiana usa-se 'avere mal di' ou 'fare male'."},
            {"errado": "Sono con febbre", "certo": "Ho la febbre", "motivo": "Para sintomas e doenças, usa-se o verbo 'avere'."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Falando de Dores</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Ho mal di...</div><div class=\"ac-body\">Ex: mal di pancia, mal di denti</div></div><div class=\"ac-card\"><div class=\"ac-head\">Mi fa/fanno male...</div><div class=\"ac-body\">Ex: mi fa male il piede</div></div></div>"
    },
    "a2-vi": {
        "observacao_cards": [
            {"italiano": "Ho mangiato", "traducao": "Eu comi", "artigo": "📌", "genero": "regra", "motivo": "A maioria dos verbos transitivos (que aceitam objeto direto) usa 'avere'."},
            {"italiano": "Abbiamo parlato", "traducao": "Nós falamos", "artigo": "📌", "genero": "regra", "motivo": "Com 'avere', o particípio passado geralmente termina em -o invariável."}
        ],
        "armadilhas": [
            {"errado": "Io mangiato", "certo": "Io ho mangiato", "motivo": "Nunca se esqueça do verbo auxiliar (avere). O passado próximo exige sempre Auxiliar + Particípio."},
            {"errado": "Abbiamo mangiati", "certo": "Abbiamo mangiato", "motivo": "O particípio acompanhado do auxiliar 'avere' não concorda com o sujeito (fica sempre em -o)."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Passato Prossimo (Avere)</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Verbos Transitivos</div><div class=\"ac-body\">O que respondem 'o que?'. Ex: mangiare, leggere.</div></div><div class=\"ac-card\"><div class=\"ac-head\">Particípio Invariável</div><div class=\"ac-body\">Sempre termina em -o. Ex: ho visto, lei ha visto.</div></div></div>"
    },
    "a2-vii": {
        "observacao_cards": [
            {"italiano": "Sono andato/a", "traducao": "Eu fui", "artigo": "📌", "genero": "regra", "motivo": "Verbos de movimento ou mudança de estado usam 'essere' como auxiliar."},
            {"italiano": "Siamo partiti/e", "traducao": "Nós partimos", "artigo": "📌", "genero": "regra", "motivo": "Com 'essere', o particípio passado deve concordar em gênero e número com o sujeito."}
        ],
        "armadilhas": [
            {"errado": "Ho andato", "certo": "Sono andato", "motivo": "Verbos que indicam movimento de um ponto a outro exigem 'essere'."},
            {"errado": "Maria è partito", "certo": "Maria è partita", "motivo": "É obrigatório concordar o particípio (-o, -a, -i, -e) quando o auxiliar for 'essere'."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Passato Prossimo (Essere)</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Uso de Essere</div><div class=\"ac-body\">Movimento, mudança de estado, reflexivos.</div></div><div class=\"ac-card\"><div class=\"ac-head\">Concordância</div><div class=\"ac-body\">Lui è andato / Lei è andata / Noi siamo andati</div></div></div>"
    },
    "a2-viii": {
        "observacao_cards": [
            {"italiano": "Da bambino giocavo", "traducao": "Quando criança, eu brincava", "artigo": "📌", "genero": "regra", "motivo": "O imperfeito é usado para hábitos e ações repetitivas no passado."},
            {"italiano": "Faceva caldo", "traducao": "Fazia calor", "artigo": "📌", "genero": "regra", "motivo": "Também é usado para descrições físicas ou de estado de espírito no passado."}
        ],
        "armadilhas": [
            {"errado": "Ieri andavo al cinema", "certo": "Ieri sono andato al cinema", "motivo": "Para uma ação pontual e concluída no passado, use o Passato Prossimo, não o Imperfeito."},
            {"errado": "Ero mangiando", "certo": "Stavo mangiando", "motivo": "Para o passado contínuo (estava comendo), use 'stare' no imperfeito + gerúndio."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Uso do Imperfetto</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Hábitos (Passado)</div><div class=\"ac-body\">Ogni estate andavamo al mare.</div></div><div class=\"ac-card\"><div class=\"ac-head\">Descrições</div><div class=\"ac-body\">Il cielo era azzurro e faceva caldo.</div></div></div>"
    },
    "a2-ix": {
        "observacao_cards": [
            {"italiano": "Mentre mangiavo, ha suonato il telefono", "traducao": "Enquanto eu comia, o telefone tocou", "artigo": "📌", "genero": "regra", "motivo": "Imperfetto (ação de fundo) + Passato Prossimo (ação pontual que interrompe)."}
        ],
        "armadilhas": [
            {"errado": "Mentre ho mangiato...", "certo": "Mentre mangiavo...", "motivo": "Após 'mentre' (enquanto), quase sempre se usa o Imperfeito, pois descreve uma ação em andamento."},
            {"errado": "Ieri pioveva e sono rimasto a casa", "certo": "Correto", "motivo": "Pioveva (descrição do clima de fundo) e sono rimasto (decisão pontual/resultado)."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Passato Prossimo vs Imperfetto</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Passato Prossimo</div><div class=\"ac-body\">O que aconteceu (Evento concluído)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Imperfetto</div><div class=\"ac-body\">O que estava acontecendo (Contexto)</div></div></div>"
    },
    "a2-x": {
        "observacao_cards": [
            {"italiano": "L'anno prossimo andrò", "traducao": "Ano que vem eu irei", "artigo": "📌", "genero": "regra", "motivo": "O futuro simples é usado para projetos e planos distantes."},
            {"italiano": "Avrà 30 anni", "traducao": "Ele deve ter 30 anos", "artigo": "📌", "genero": "regra", "motivo": "Futuro epistemológico: usado para expressar dúvida ou suposição no presente."}
        ],
        "armadilhas": [
            {"errado": "Domani io farò", "certo": "Domani faccio", "motivo": "Para o futuro próximo, os italianos usam frequentemente o Presente do Indicativo."},
            {"errado": "Mangerò, mangiarò", "certo": "Mangerò", "motivo": "Os verbos em -are mudam o 'a' para 'e' no radical do futuro (mangiare -> mangerò)."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Futuro Semplice</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Ações Futuras</div><div class=\"ac-body\">Fra un mese partirò per Roma.</div></div><div class=\"ac-card\"><div class=\"ac-head\">Suposições</div><div class=\"ac-body\">Saranno le cinque. (Devem ser cinco)</div></div></div>"
    },
    "a2-xi": {
        "observacao_cards": [
            {"italiano": "Più grande di...", "traducao": "Maior que...", "artigo": "📌", "genero": "regra", "motivo": "Usamos 'di' para comparar nomes, pronomes ou duas pessoas."},
            {"italiano": "Più bello che utile", "traducao": "Mais bonito do que útil", "artigo": "📌", "genero": "regra", "motivo": "Usamos 'che' ao comparar dois adjetivos, verbos ou quantidades."}
        ],
        "armadilhas": [
            {"errado": "Più buono", "certo": "Migliore / Più buono", "motivo": "Em italiano 'più buono' é perfeitamente aceito, mas 'migliore' é mais elegante."},
            {"errado": "Roma è più grande che Milano", "certo": "Roma è più grande di Milano", "motivo": "Na comparação entre dois substantivos, usa-se 'di' e não 'che'."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Comparativos</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Di</div><div class=\"ac-body\">Compara sujeitos (Marco è più alto di Luca).</div></div><div class=\"ac-card\"><div class=\"ac-head\">Che</div><div class=\"ac-body\">Compara qualidades (È più stanco che malato).</div></div></div>"
    },
    "a2-xii": {
        "observacao_cards": [
            {"italiano": "Lo vedo", "traducao": "Eu o vejo", "artigo": "📌", "genero": "regra", "motivo": "Os pronomes diretos substituem um objeto direto."},
            {"italiano": "L'ho visto", "traducao": "Eu o vi", "artigo": "📌", "genero": "regra", "motivo": "Com o Passato Prossimo, o pronome (lo/la) contrai-se com avere (l'ho) e o particípio concorda."}
        ],
        "armadilhas": [
            {"errado": "Vedo lui", "certo": "Lo vedo", "motivo": "Não se costuma usar 'vedo lui' a não ser para forte ênfase. Use o pronome átono antes do verbo."},
            {"errado": "L'ho vista e salutato", "certo": "L'ho vista e l'ho salutata", "motivo": "O particípio deve concordar com o pronome direto de 3ª pessoa."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Pronomi Diretti</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Singulares</div><div class=\"ac-body\">mi (me), ti (te), lo (o), la (a)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Plurais</div><div class=\"ac-body\">ci (nos), vi (vos), li (os), le (as)</div></div></div>"
    },
    "a2-xiii": {
        "observacao_cards": [
            {"italiano": "Gli parlo", "traducao": "Eu falo com ele", "artigo": "📌", "genero": "regra", "motivo": "O pronome indireto responde a 'a chi?' (a quem?). 'Gli' = a lui."},
            {"italiano": "Le telefono", "traducao": "Eu telefono para ela", "artigo": "📌", "genero": "regra", "motivo": "O verbo telefonare exige um objeto indireto (telefonare a)."}
        ],
        "armadilhas": [
            {"errado": "Lo parlo", "certo": "Gli parlo", "motivo": "Falar é 'parlare a', logo exige pronome indireto (gli), não direto (lo)."},
            {"errado": "Gli ho detto (para eles)", "certo": "Ho detto loro / Gli ho detto", "motivo": "No italiano moderno 'gli' é amplamente aceito também para o plural em vez de 'loro'."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Pronomi Indiretti</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">3ª Pessoa Sing.</div><div class=\"ac-body\">Gli (a ele) / Le (a ela) / Le (formal)</div></div><div class=\"ac-card\"><div class=\"ac-head\">Lugar na frase</div><div class=\"ac-body\">Sempre antes do verbo, exceto 'loro'.</div></div></div>"
    },
    "a2-xiv": {
        "observacao_cards": [
            {"italiano": "Mi sveglio", "traducao": "Eu acordo", "artigo": "📌", "genero": "regra", "motivo": "Verbos reflexivos exigem os pronomes mi, ti, si, ci, vi, si."},
            {"italiano": "Mi sono svegliato/a", "traducao": "Eu acordei", "artigo": "📌", "genero": "regra", "motivo": "Todos os verbos reflexivos no Passato Prossimo exigem o auxiliar 'essere'!"}
        ],
        "armadilhas": [
            {"errado": "Mi ho svegliato", "certo": "Mi sono svegliato", "motivo": "Jamais use 'avere' com verbos reflexivos."},
            {"errado": "Svegliomi", "certo": "Mi sveglio", "motivo": "O pronome vem antes do verbo conjugado. Só vai depois com infinitivo ou imperativo."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Verbos Reflexivos</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Pronomes</div><div class=\"ac-body\">mi, ti, si, ci, vi, si</div></div><div class=\"ac-card\"><div class=\"ac-head\">Passado</div><div class=\"ac-body\">Sempre auxiliar Essere + Concordância.</div></div></div>"
    },
    "a2-xv": {
        "observacao_cards": [
            {"italiano": "Me lo dai?", "traducao": "Você me dá isso?", "artigo": "📌", "genero": "regra", "motivo": "Pronome indireto (mi) muda para 'me' com um pronome direto (lo, la...)."},
            {"italiano": "Glielo porto", "traducao": "Eu o levo para ele/ela", "artigo": "📌", "genero": "regra", "motivo": "Gli/Le indiretos unem-se a lo/la/li/le através de um 'e' (glielo)."}
        ],
        "armadilhas": [
            {"errado": "Mi lo dai", "certo": "Me lo dai", "motivo": "A vogal 'i' dos pronomes mi/ti/ci/vi muda sempre para 'e' ao se juntar aos pronomes diretos."},
            {"errado": "Gli lo dico", "certo": "Glielo dico", "motivo": "Nunca devem ficar separados. O 'gli' forma palavra única (glielo)."}
        ],
        "tabela_visual": "<p class=\"tabela-intro\">Pronomi Combinati</p><div class=\"artigo-cards\"><div class=\"ac-card\"><div class=\"ac-head\">Mi/Ti/Ci/Vi + Lo</div><div class=\"ac-body\">Me lo, Te lo, Ce lo, Ve lo</div></div><div class=\"ac-card\"><div class=\"ac-head\">Gli / Le + Lo</div><div class=\"ac-body\">Glielo (Unidos em uma palavra)</div></div></div>"
    }
}

with open('data/mod1.json', 'r', encoding='utf-8') as f:
    mod_data = json.load(f)

for un in mod_data.get('unidades', []):
    uid = un.get('id')
    if uid in data_updates:
        un['observacao_cards'] = data_updates[uid]['observacao_cards']
        un['armadilhas'] = data_updates[uid]['armadilhas']
        un['tabela_visual'] = data_updates[uid]['tabela_visual']

with open('data/mod1_final.json', 'w', encoding='utf-8') as f:
    json.dump(mod_data, f, ensure_ascii=False, indent=2)

print("SUCCESS: Successfully wrote data/mod1_final.json")
