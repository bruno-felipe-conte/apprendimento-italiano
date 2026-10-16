#!/usr/bin/env python3
"""
Enriquece e corrige data/grammar.json:
1. Preenche todas as 15 lições dos módulos C1 (c1-i a c1-x) e C2 (c2-i a c2-v) com teoria completa em português,
   tabela_visual, alerta, inventario, definicao (Veja/Pense/Entenda), tecnica, observacao_cards, exemplos_prc,
   armadilhas, ponte, coda e exemplos.
2. Corrige os 84 observacao_cards de a1-lez3 a a1-lez30 para terem traduções reais em português na frente,
   badge gramatical adequado (em vez de 'importante') e explicação detalhada no verso.
3. Remove os exercícios corrompidos '--- EXERCÍCIOS EXTRAS ---' e '(Extra)' duplicados que tinham 'undefined'
   ou respostas erradas copiadas de outras lições.
4. Traduz/adapta para português didático as explicações de exercícios que estavam apenas em italiano.
"""
import json
import re

def make_tabela_visual(titulo, pares):
    cards_html = "".join(
        f'<div class="ac-card"><div class="ac-head">{h}</div><div class="ac-body">{b}</div></div>'
        for h, b in pares
    )
    return f'<p class="tabela-intro">{titulo}</p><div class="artigo-cards">{cards_html}</div>'

C1_C2_CONTENT = {
    "c1-i": {
        "alerta": "No nível C1, o Congiuntivo deixa de ser apenas automático após 'penso che' e passa a diferenciar nuances finas de certeza, concessão, restrição e busca indefinida que até falantes nativos confundem.",
        "inventario": [
            "Cerco un assistente che parli cinese. (indefinido/buscado → Congiuntivo)",
            "Ho un assistente che parla cinese. (conhecido/real → Indicativo)",
            "Sebbene / Benché / Nonostante + Congiuntivo (concessão real)",
            "A patto che / Purché / Qualora + Congiuntivo (condição restritiva)",
            "Prima che + Congiuntivo vs Dopo che + Indicativo"
        ],
        "definicao": {
            "fenomeno": "Em orações relativas, concessivas e condicionais avançadas, a escolha entre Indicativo e Congiuntivo altera completamente o significado da frase (fato constatado vs hipótese/restrição).",
            "causa": "Por que dizemos 'Cerco qualcuno che parli' (subjuntivo) mas 'Conosco qualcuno che parla' (indicativo)?",
            "conceito": "O Congiuntivo Avançado marca a não-factualidade, a subjetividade ou a restrição. Nas relativas restritivas de busca ('cerco/voglio un X che...'), o referente ainda é virtual; nas concessivas ('benché', 'nonostante', 'per quanto'), o fato é admitido sob tensão; nas condicionais formais ('qualora', 'purché'), impõe-se uma condição estrita."
        },
        "tecnica": "**Como dominar as nuances do Congiuntivo C1:**\n\n1. **Relativas de busca vs posse:** Se você procura, deseja ou nega a existência de algo (*cerco, vorrei, non c'è nessuno che...*), use **Congiuntivo**. Se já possui ou conhece, use **Indicativo**.\n2. **Concessivas obrigatórias:** Após *benché, sebbene, nonostante, malgrado, per quanto*, use sempre o **Congiuntivo** (*Presente/Passato* no eixo presente; *Imperfetto/Trapassato* no eixo passado).\n3. **Condicionais restritivas:** *Purché, a patto che, a condizione che* exigem **Congiuntivo Presente ou Imperfetto**; *qualora* exige preferencialmente o **Congiuntivo**.\n4. **Superlativo relativo:** Após *il più... che*, *l'unico... che*, *il primo... che*, o italiano culto prefere o **Congiuntivo** (*È il film più bello che io abbia mai visto*).",
        "teoria": "### Usos Avançados do Congiuntivo (Nível C1)\n\nNo italiano culto, o **congiuntivo** não depende apenas de verbos de opinião (*credere, pensare*). Ele atua como um marcador semântico de **virtualidade** e **modalização**.\n\n#### 1. Orações Relativas (Indicativo vs Congiuntivo)\n| Contexto | Modo | Exemplo |\n|---|---|---|\n| Referente específico e real | **Indicativo** | *Conosco un medico che **lavora** a Milano.* |\n| Referente virtual, buscado ou negado | **Congiuntivo** | *Cerco un medico che **lavori** la domenica.* |\n| Após superlativo ou *unico/primo/ultimo* | **Congiuntivo** | *Sei l'unica persona di cui mi **fidi**.* |\n\n#### 2. Conjunções que exigem sempre o Congiuntivo\n- **Concessivas:** *benché, sebbene, nonostante, malgrado, per quanto + adj.* → *Nonostante **avesse** studiato molto, non ha superato l'esame.*\n- **Restritivas / Condicionais:** *purché, a patto che, a condizione che, qualora* → *Ti aiuto purché tu **faccia** la tua parte.*\n- **Temporais de anterioridade e hipótese:** *prima che, finché non (hipotético)* → *Esco prima che **piova**.*\n- **Modais hipotéticas:** *come se, quasi che* (+ Imperfetto/Trapassato) → *Parla come se **fosse** il direttore.*",
        "tabela_visual": make_tabela_visual("Mapa de Decisão do Congiuntivo Avançado", [
            ("Relativa Virtual", "Cerco qualcuno che + Congiuntivo (parli / sapesse)"),
            ("Concessiva Real", "Benché / Nonostante / Sebbene + Congiuntivo"),
            ("Condição Estrita", "Purché / A patto che / Qualora + Congiuntivo"),
            ("Comparação Irreal", "Come se + Congiuntivo Imperfetto / Trapassato")
        ]),
        "observacao_cards": [
            {"italiano": "Cerco qualcuno che parli il cinese.", "traducao": "Procuro alguém que fale chinês.", "artigo": "Cong. Pres.", "genero": "relativa virtual", "motivo": "Como ainda não sabemos se essa pessoa existe, o italiano exige o Congiuntivo Presente (parli)."},
            {"italiano": "Nonostante avesse studiato molto, non ha superato l'esame.", "traducao": "Apesar de ter estudado muito, não passou no exame.", "artigo": "Trapassato", "genero": "concessiva", "motivo": "Nonostante rege Congiuntivo; como a ação de estudar é anterior ao passado, usa-se o Trapassato (avesse studiato)."},
            {"italiano": "È il libro più interessante che io abbia mai letto.", "traducao": "É o livro mais interessante que eu já li.", "artigo": "Cong. Pass.", "genero": "superlativo", "motivo": "Após superlativo relativo ('il più... che'), o registro culto italiano usa o Congiuntivo (abbia letto)."}
        ],
        "exemplos_prc": [
            {"oracao": "Cerco un appartamento che abbia il terrazzo.", "pergunta": "Por que usamos 'abbia' (subjuntivo) e não 'ha'?", "resposta": "Procuro um apartamento que tenha terraço.", "conclusao": "O apartamento ainda é um desejo/busca virtual, portanto exige o Congiuntivo Presente."},
            {"oracao": "Si comporta come se nulla fosse successo.", "pergunta": "Qual tempo segue a locução 'come se'?", "resposta": "Ele se comporta como se nada tivesse acontecido.", "conclusao": "'Come se' introduz uma comparação irreal e exige sempre Congiuntivo Imperfetto ou Trapassato."},
            {"oracao": "Qualora dovessero sorgere problemi, ci contatti subito.", "pergunta": "Qual é a função de 'qualora' no registro formal?", "resposta": "Caso surjam problemas, entre em contato conosco imediatamente.", "conclusao": "'Qualora' equivale a um 'se porventura' formal e exige obrigatoriamente o Congiuntivo."}
        ],
        "armadilhas": [
            {"errado": "Nonostante ha piovuto tutto il giorno, siamo usciti.", "certo": "Nonostante abbia piovuto tutto il giorno, siamo usciti.", "motivo": "Diferente de 'anche se' (que aceita indicativo), 'nonostante', 'benché' e 'sebbene' exigem sempre o Congiuntivo."},
            {"errado": "Parla come se sa tutto lui.", "certo": "Parla come se sapesse tutto lui.", "motivo": "A locução 'come se' nunca aceita o Indicativo nem o Congiuntivo Presente: exige Congiuntivo Imperfetto ou Trapassato."}
        ],
        "ponte": "**Em português:** Também usamos o subjuntivo em relativas virtuais (*Procuro alguém que fale*), mas com *apesar de* usamos infinitivo (*apesar de ter estudado*). Em italiano, *nonostante* e *benché* com verbo finito exigem o **Congiuntivo** explícito.",
        "coda": "Regra de bolso C1: se há busca incerta (*cerco chi...*), concessão formal (*benché/nonostante*), condição restritiva (*purché/qualora*) ou superlativo (*il più... che*), acione imediatamente o Congiuntivo.",
        "exemplos": [
            "Non c'è nessuno che possa risolvere questo problema in cinque minuti.",
            "Benché fosse tardi, hanno deciso di proseguire il viaggio.",
            "Accetto l'incarico a patto che mi diate piena autonomia."
        ]
    },
    "c1-ii": {
        "alerta": "O Período Hipotético do Tipo 3 (Irrealidade no Passado) e os períodos mistos permitem expressar arrependimentos, hipóteses contrafactuais e consequências presentes de escolhas passadas.",
        "inventario": [
            "Tipo 3 Puro: Se + Congiuntivo Trapassato → Condizionale Composto",
            "Se avessi studiato, avrei superato l'esame.",
            "Tipo Misto (Passado → Presente): Se + Cong. Trapassato → Condizionale Semplice",
            "Se avessi accettato quel lavoro, oggi vivrei a Londra.",
            "Forma Coloquial Literária: Imperfetto Indicativo duplo (Se lo sapevo, non venivo)"
        ],
        "definicao": {
            "fenomeno": "Quando imaginamos um passado diferente daquele que realmente ocorreu, tanto a condição (prótase) quanto a consequência (apódose) recuam para tempos compostos.",
            "causa": "Como diferenciar uma consequência que ficou encerrada no passado de uma consequência que ainda afeta o presente ('oggi')?",
            "conceito": "No **Tipo 3 puro**, condição e resultado pertencem ao passado (*Se fossi partito, sarei arrivato*). No **Período Hipotético Misto**, a condição ocorreu no passado (*Se avessi risparmiato*), mas o resultado é sentido no presente (*oggi avrei una casa* → Condizionale Semplice)."
        },
        "tecnica": "**Como construir hipóteses contrafactuais sem errar:**\n\n1. **Prótase (Cláusula com SE no passado):** Use sempre o **Congiuntivo Trapassato** (*avessi fatto / fossi andato*). Jamais use o condicional logo após o *se*!\n2. **Apódose no Passado:** Se o resultado também ficou no passado, use o **Condizionale Composto** (*avrei fatto / sarei andato*).\n3. **Apódose no Presente (Misto):** Se houver marcadores como *oggi, adesso, ora*, use o **Condizionale Semplice** (*oggi sarei felice*).\n4. **Prótase implícita:** Pode ser construída com *a + infinitivo* ou *gerúndio* (*A saperlo prima, non sarei venuto*).",
        "teoria": "### Período Hipotético da Irrealidade (Tipo 3 e Mistos)\n\nO **Periodo Ipotetico dell'Irrealtà** analisa cenários contrafactuais — aquilo que não aconteceu e não pode mais ser mudado.\n\n| Estrutura | Prótase (Condição) | Apódose (Consequência) | Exemplo |\n|---|---|---|---|\n| **Tipo 2** (Presente irreal) | *Se* + Cong. Imperfetto | Condizionale Semplice | *Se **avessi** tempo, **verrei**.* |\n| **Tipo 3** (Passado irreal) | *Se* + Cong. Trapassato | Condizionale Composto | *Se **avessi avuto** tempo, **sarei venuto**.* |\n| **Misto** (Passado → Hoje) | *Se* + Cong. Trapassato | Condizionale Semplice | *Se **fossi partito** ieri, oggi **sarei** a Roma.* |\n| **Registro Falado** (Informal) | *Se* + Imperfetto Ind. | Imperfetto Ind. | *Se me lo **dicevi**, ti **aiutavo**.* |",
        "tabela_visual": make_tabela_visual("Fórmulas do Período Hipotético Avançado", [
            ("Tipo 3 (Passado)", "Se + avessi/fossi + part. → avrei/sarei + part."),
            ("Misto (Passado → Hoje)", "Se + avessi/fossi + part. → Condizionale Presente (oggi)"),
            ("Implícito com Infinitivo", "A saperlo prima (= Se lo avessi saputo), sarei rimasto"),
            ("Italiano Falado (Informal)", "Se + Imperfetto Indicativo → Imperfetto Indicativo")
        ]),
        "observacao_cards": [
            {"italiano": "Se avessi studiato, avresti passato l'esame.", "traducao": "Se você tivesse estudado, teria passado no exame.", "artigo": "Tipo 3", "genero": "passado irreal", "motivo": "Condição e resultado irreais no passado: Congiuntivo Trapassato + Condizionale Composto."},
            {"italiano": "Se avessi accettato quel posto, oggi vivrei a Milano.", "traducao": "Se eu tivesse aceitado aquela vaga, hoje moraria em Milão.", "artigo": "Misto", "genero": "passado→presente", "motivo": "Condição no passado (avessi accettato) com efeito no presente (oggi vivrei → Condizionale Semplice)."},
            {"italiano": "A saperlo prima, non sarei venuto.", "traducao": "Se eu soubesse antes, não teria vindo.", "artigo": "A + Inf.", "genero": "prótase implícita", "motivo": "'A saperlo' substitui 'Se lo avessi saputo' de forma elegante e idiomática."}
        ],
        "exemplos_prc": [
            {"oracao": "Se fossi stato più attento, non avrei fatto quell'errore.", "pergunta": "Por que usamos 'fossi stato' na primeira parte e 'avrei fatto' na segunda?", "resposta": "Se eu tivesse sido mais atento, não teria cometido aquele erro.", "conclusao": "A prótase com 'se' exige Congiuntivo Trapassato; a consequência exige Condizionale Composto."},
            {"oracao": "Se non avessi perso il treno, adesso sarei già a casa.", "pergunta": "Por que a segunda parte usa 'sarei' e não 'sarei stato'?", "resposta": "Se eu não tivesse perdido o trem, agora já estaria em casa.", "conclusao": "O advérbio 'adesso' mostra que a consequência ocorre no momento presente (período hipotético misto)."}
        ],
        "armadilhas": [
            {"errado": "Se avrei saputo la verità, te l'avrei detta.", "certo": "Se avessi saputo la verità, te l'avrei detta.", "motivo": "Erro gravíssimo em italiano ('doppio condizionale'): a conjunção condicional 'se' NUNCA é seguida pelo condicional."},
            {"errado": "Se avessi studiato medicina, oggi sarei stato medico.", "certo": "Se avessi studiato medicina, oggi sarei medico.", "motivo": "Quando a consequência vale para 'oggi' (presente), usa-se o Condizionale Semplice (sarei), não o Composto."}
        ],
        "ponte": "**Em português:** Na fala cotidiana brasileira é comum usar o mais-que-perfeito ou imperfeito (*Se eu soubesse, tinha ido*). Em italiano culto (C1), a simetria **Congiuntivo Trapassato + Condizionale Composto** é rigorosamente cobrada.",
        "coda": "Nunca coloque *avrei/sarei* na cláusula do *se*. Na condição vai sempre o **SS** (*avessi/fossi*); na consequência vai o **R** (*avrei/sarei*).",
        "exemplos": [
            "Se ci avessero avvertiti in tempo, avremmo evitato il traffico.",
            "Se avessi ascoltato i tuoi consigli, ora non avrei questi problemi.",
            "Senza il tuo aiuto, non ce l'avremmo mai fatta."
        ]
    },
    "c1-iii": {
        "alerta": "A nominalização — transformar verbos e adjetivos em substantivos abstratos — é a marca registrada da escrita acadêmica, jurídica e corporativa italiana de nível C1.",
        "inventario": [
            "Verbo → Substantivo: analizzare → l'analisi | decidere → la decisione",
            "Adjetivo → Substantivo: possibile → la possibilità | urgente → l'urgenza",
            "Sufixos produtivos: -zione, -mento, -anza/-enza, -ità, -aggio",
            "Verbos de suporte formais: effettuare un controllo (= controllare), prendere in esame (= esaminare)"
        ],
        "definicao": {
            "fenomeno": "Em vez de encadear várias orações subordinadas verbais ('Dopo che il governo ha approvato la legge...'), o italiano formal condensa a ação num sintagma nominal ('Dopo l'approvazione della legge da parte del governo...').",
            "causa": "Como transformar uma frase verbal comum em um período denso, objetivo e impessoal?",
            "conceito": "A **nominalização** desloca o peso semântico do verbo para um substantivo abstrato (geralmente derivado por sufixos como *-zione*, *-mento*, *-ità*) acompanhado de preposições formais (*in seguito a, ai fini di, da parte di*) ou verbos de suporte (*effettuare, procedere a, determinare*)."
        },
        "tecnica": "**Passo a passo para nominalizar uma frase em italiano:**\n\n1. **Substitua a conjunção + verbo** por uma preposição + substantivo: *Quando è arrivato il treno* → *All'arrivo del treno*.\n2. **Transforme o sujeito do verbo ativo** em complemento introduzido por *di* ou *da parte di*: *Il parlamento ha ridotto le tasse* → *La riduzione delle tasse da parte del parlamento*.\n3. **Use verbos de suporte formais:** troque *controllare* por *effettuare una verifica*, *decidere* por *giungere alla decisione*.\n4. **Equilíbrio estilístico:** use a nominalização em relatórios, ensaios e e-mails formais, mas evite o excesso burocrático (*antilingua*) na fala cotidiana.",
        "teoria": "### Nominalizzazione e Stile Formale\n\nNo registro **formale, accademico e burocratico**, o italiano prefere construções nominais concisas em vez de orações subordinadas longas.\n\n#### 1. Principais Transformações Verbo → Substantivo\n| Estilo Verbal (Padrão) | Estilo Nominalizado (Formal C1) |\n|---|---|\n| *Perché i prezzi sono aumentati...* | *A causa dell'**aumento** dei prezzi...* |\n| *Dopo che il contratto è stato firmato...* | *In seguito alla **firma** del contratto...* |\n| *Per ridurre i costi aziendali...* | *Ai fini del **contenimento** dei costi aziendali...* |\n| *Se le norme vengono violate...* | *In caso di **violazione** delle norme...* |\n\n#### 2. Sufixos de Derivação Nominal\n- **-zione / -sione:** *produrre → produzione, espandere → espansione, verificare → verificazione/verifica*\n- **-mento:** *cambiare → cambiamento, migliorare → miglioramento, trasferire → trasferimento*\n- **-anza / -enza:** *scadere → scadenza, partire → partenza, tollerare → tolleranza*\n- **-ità:** *stabile → stabilità, compatibile → compatibilità*",
        "tabela_visual": make_tabela_visual("Conversão Verbal → Nominal (Registro C1)", [
            ("Causa", "Perché è crollato → A causa del crollo di"),
            ("Tempo", "Dopo che hanno aperto → In seguito all'apertura di"),
            ("Finalidade", "Per tutelare → Ai fini della tutela di"),
            ("Verbo de Suporte", "Controllare / Esaminare → Effettuare un controllo / Prendere in esame")
        ]),
        "observacao_cards": [
            {"italiano": "In seguito all'approvazione del bilancio, la seduta è tolta.", "traducao": "Em seguida à aprovação do orçamento, a sessão está encerrada.", "artigo": "-zione", "genero": "nominalização", "motivo": "'Approvare' torna-se 'l'approvazione', condensando a oração temporal com 'in seguito a'."},
            {"italiano": "Si prega di procedere alla compilazione del modulo.", "traducao": "Solicita-se proceder ao preenchimento do formulário.", "artigo": "Suporte", "genero": "estilo formal", "motivo": "'Procedere alla compilazione' substitui 'compilare' no registro administrativo e formal."},
            {"italiano": "Il mancato rispetto delle scadenze comporterà sanzioni.", "traducao": "O descumprimento dos prazos acarretará sanções.", "artigo": "Mancato + N", "genero": "jurídico", "motivo": "'Il mancato + substantivo' é a forma padrão formal para 'il fatto di non aver rispettato'."}
        ],
        "exemplos_prc": [
            {"oracao": "L'azienda ha deciso di chiudere lo stabilimento → La decisione dell'azienda di chiudere lo stabilimento.", "pergunta": "O que mudou na estrutura da frase?", "resposta": "A decisão da empresa de fechar a fábrica.", "conclusao": "O verbo finito 'ha deciso' foi transformado no núcleo nominal 'La decisione', tornando a frase um tópico temático."},
            {"oracao": "In caso di smarrimento del bagaglio, rivolgersi all'ufficio reclami.", "pergunta": "Qual verbo deu origem a 'smarrimento'?", "resposta": "Em caso de extravio da bagagem, dirigir-se ao setor de reclamações.", "conclusao": "Deriva do verbo 'smarrire' (extraviar/perder) com o sufixo '-mento', típico de avisos oficiais."}
        ],
        "armadilhas": [
            {"errado": "Dopo l'approvamento della legge da il Senato...", "certo": "Dopo l'approvazione della legge da parte del Senato...", "motivo": "O substantivo correto de 'approvare' é 'approvazione', e o agente de um substantivo verbal usa 'da parte di' (não apenas 'da')."},
            {"errado": "Per il mancato pagando della fattura...", "certo": "Per il mancato pagamento della fattura...", "motivo": "A estrutura formal usa 'il mancato + substantivo' (il mancato pagamento, la mancata consegna), nunca gerúndio."}
        ],
        "ponte": "**Em português:** Também usamos nominalizações na escrita formal (*O descumprimento das regras*). A construção italiana **il mancato + substantivo** (*il mancato pagamento*, *la mancata risposta*) corresponde diretamente ao nosso *o não pagamento / a falta de resposta*.",
        "coda": "Para elevar imediatamente seu texto ao nível C1 na prova CELI/CILS, substitua pelo menos duas subordinadas iniciadas por *quando/perché* por *in seguito a / a causa di + substantivo abstrato*.",
        "exemplos": [
            "La crescente diffusione dello smart working ha trasformato il mercato immobiliare.",
            "Si comunica l'annullamento del volo per avverse condizioni meteorologiche.",
            "Ai fini del rilascio del passaporto è necessaria la presenza del richiedente."
        ]
    },
    "c1-iv": {
        "alerta": "Conectivos avançados (*pertanto, tuttavia, benché, qualora, anziché, nondimeno*) são a espinha dorsal de um texto argumentativo coeso e elegante em nível C1.",
        "inventario": [
            "Concessivos: tuttavia, nondimeno, ciononostante, per quanto (+ cong.), sebbene (+ cong.)",
            "Conclusivos / Consecutivos: pertanto, di conseguenza, sicché, ragion per cui",
            "Aditivos e Correlativos: nonché, oltre a ciò, non solo... ma anche, sia... sia",
            "Substitutivos e Opositivos: anziché, invece di, laddove, mentre invece"
        ],
        "definicao": {
            "fenomeno": "Enquanto um falante iniciante conecta tudo apenas com *ma, perché, quindi, e*, o falante C1 articula relações lógicas precisas (oposição, ressalva, consequência formal, adição enfática).",
            "causa": "Qual conectivo escolher e qual modo verbal (*Indicativo*, *Congiuntivo* ou *Infinitivo*) cada um exige?",
            "conceito": "Os conectivos dividem-se entre **coordenativos/textuais** (como *tuttavia, pertanto, ciononostante*, que ligam períodos com o **Indicativo**) e **subordinativos** (como *benché, qualora, affinché*, que exigem o **Congiuntivo**, ou *anziché, prima di*, seguidos de **Infinitivo**)."
        },
        "tecnica": "**Regras de ouro para usar conectivos C1:**\n\n1. **Oposição sem mudar para o subjuntivo:** Use *tuttavia*, *ciononostante* ou *nondimeno* após ponto ou ponto e vírgula com verbo no **Indicativo**.\n2. **Concessão subordinada:** Use *sebbene*, *benché*, *per quanto* com **Congiuntivo**.\n3. **Causa formal no início da frase:** Use *poiché*, *giacché* ou *dal momento che* (+ Indicativo) em vez de começar frases formais com *perché*.\n4. **Substituição elegante:** Use *anziché + infinitivo* (*Anziché protestare, proponi una soluzione* = Em vez de protestar).",
        "teoria": "### Connettivi Avanzati e Coesione Testuale\n\nA coesão textual de alto nível depende da variedade e precisão dos conectivos lógicos.\n\n| Função Lógica | Conectivos C1 | Modo Verbal Exigido |\n|---|---|---|\n| **Concessão** | *benché, sebbene, nonostante, per quanto* | **Congiuntivo** |\n| **Contra-argumento** | *tuttavia, ciononostante, nondimeno, eppure* | **Indicativo** |\n| **Causa Formal** | *poiché, giacché, dato che, visto che, in quanto* | **Indicativo** |\n| **Consequência** | *pertanto, di conseguenza, perciò, sicché* | **Indicativo** |\n| **Finalidade** | *affinché, onde evitare che* / *al fine di* | **Congiuntivo** / **Infinitivo** |\n| **Exclusão / Troca** | *anziché, invece di, piuttosto che* | **Infinitivo** |\n| **Adição culta** | *inoltre, altresì, nonché* | — |",
        "tabela_visual": make_tabela_visual("Conectivos de Alto Nível por Função", [
            ("Contra-argumento", "Tuttavia / Ciononostante / Nondimeno (+ Indicativo)"),
            ("Conclusão Formal", "Pertanto / Di conseguenza / Ragion per cui"),
            ("Finalidade Culta", "Affinché (+ Congiuntivo) | Al fine di (+ Infinitivo)"),
            ("Substituição", "Anziché / Piuttosto che (+ Infinitivo)")
        ]),
        "observacao_cards": [
            {"italiano": "Il progetto è ambizioso; tuttavia, i fondi sono insufficienti.", "traducao": "O projeto é ambicioso; todavia, os fundos são insuficientes.", "artigo": "Tuttavia", "genero": "adversativo", "motivo": "'Tuttavia' introduz uma ressalva formal no Indicativo, ideal após ponto e vírgula."},
            {"italiano": "La domanda è incompleta; pertanto non potrà essere accolta.", "traducao": "O pedido está incompleto; portanto, não poderá ser aceito.", "artigo": "Pertanto", "genero": "conclusivo", "motivo": "'Pertanto' é o equivalente formal e elegante de 'quindi' ou 'perciò'."},
            {"italiano": "Anziché lamentarti, prova a cercare una soluzione.", "traducao": "Em vez de reclamar, tente procurar uma solução.", "artigo": "Anziché", "genero": "substitutivo", "motivo": "'Anziché' (+ infinitivo) substitui 'invece di' com maior sofisticação estilística."}
        ],
        "exemplos_prc": [
            {"oracao": "Poiché non abbiamo ricevuto risposta, procederemo per vie legali.", "pergunta": "Por que usamos 'Poiché' em vez de 'Perché' no início da frase?", "resposta": "Como / Já que não recebemos resposta, procederemos pelas vias legais.", "conclusao": "Em italiano formal, evita-se iniciar o período com 'perché' causal; prefere-se 'poiché', 'dato che' ou 'dal momento che'."},
            {"oracao": "Il candidato parla fluentemente inglese nonché tedesco.", "pergunta": "Qual é o valor de 'nonché' nesta frase?", "resposta": "O candidato fala fluentemente inglês, bem como alemão.", "conclusao": "'Nonché' equivale a 'bem como / assim como', adicionando um elemento de destaque no registro culto."}
        ],
        "armadilhas": [
            {"errado": "Tuttavia che sia difficile, ci proveremo.", "certo": "Sebbene sia difficile, ci proveremo. / È difficile; tuttavia ci proveremo.", "motivo": "'Tuttavia' é advérbio conectivo (não leva 'che' nem subjuntivo). Para subordinar com subjuntivo, use 'sebbene' ou 'benché'."},
            {"errado": "Preferisco leggere piuttosto che guardare la TV o uscire.", "certo": "Preferisco leggere anziché guardare la TV.", "motivo": "No italiano padrão tradicional, 'piuttosto che' significa 'em vez de' (e não 'ou' alternativo, que é um modismo recente criticado em exames formais)."}
        ],
        "ponte": "**Em português:** *Pertanto* = portanto; *tuttavia* = todavia/contudo; *nonché* = bem como; *anziché* = ao invés de. Cuidado apenas com a regência de modo verbal de cada um!",
        "coda": "Substitua na sua escrita: *ma* → *tuttavia*; *quindi* → *pertanto*; *perché* (no início) → *poiché*; *per + inf.* → *al fine di + inf.*",
        "exemplos": [
            "I dati confermano la ripresa; ciononostante, resta alta l'inflazione.",
            "Il documento va inviato entro venerdì affinché la commissione possa valutarlo.",
            "Laddove si riscontrino irregolarità, il contratto verrà rescisso."
        ]
    },
    "c1-v": {
        "alerta": "O italiano jornalístico e midiático possui uma gramática própria: manchetes elípticas sem verbo, Condizionale di Dissociazione para notícias não confirmadas e metáforas políticas constantes.",
        "inventario": [
            "Condizionale giornalistico: Il ministro avrebbe presentato le dimissioni (alegação não confirmada)",
            "Stile nominale nei titoli: Svolta nelle indagini. Caos trasporti a Roma.",
            "Passivo com 'andare': I documenti sono andati distrutti / Il testo va modificato",
            "Jargão da imprensa: fumata nera, stangata, poltrona, retroscena, braccio di ferro"
        ],
        "definicao": {
            "fenomeno": "Ao ler jornais como *Corriere della Sera* ou *La Repubblica*, encontramos manchetes sem verbos conjugados e notícias inteiras no condicional (*sarebbe*, *avrebbe*).",
            "causa": "Por que os jornalistas italianos usam o Condicional (*avrebbe detto*) mesmo quando falam de algo que aconteceu ontem?",
            "conceito": "Trata-se do **Condizionale di Dissociazione (ou Giornalistico)**: o repórter relata uma informação atribuída a fontes externas sem assumir responsabilidade jurídica direta pela sua veracidade absoluta (*Segundo as fontes, o suspeito teria fugido*)."
        },
        "tecnica": "**Como decodificar e produzir textos jornalísticos em italiano:**\n\n1. **Manchetes (Titoli):** Omita o verbo *essere* e os artigos; use dois-pontos para indicar discurso ou causa (*Sciopero dei treni: disagi in tutta Italia*).\n2. **Notícia não oficial:** Use o **Condizionale Composto** para fatos passados ainda sob investigação (*L'accordo sarebbe stato raggiunto nella notte*).\n3. **Dever/Necessidade impessoal:** Use *andare + particípio passado* (*La riforma va approvata entro dicembre* = deve ser aprovada).\n4. **Léxico figurado:** *Fumata nera* (negociação sem acordo), *stangata* (aumento pesado de impostos/preços), *rimpasto* (reforma ministerial).",
        "teoria": "### Il Linguaggio dei Media e del Giornalismo\n\nO italiano da imprensa (*linguaggio giornalistico*) busca impacto, síntese e cautela informativa.\n\n#### 1. Estruturas Gramaticais Típicas da Imprensa\n| Estrutura | Função | Exemplo |\n|---|---|---|\n| **Condizionale di dissociazione** | Fato não confirmado oficialmente | *Il sindaco **avrebbe ricevuto** un avviso di garanzia.* |\n| **Frase nominale (Manchete)** | Síntese máxima e impacto | *Inflazione in calo, borse in rialzo.* |\n| **Infinito narrativo / Futuro retrospettivo** | Dinamismo histórico | *La crisi scoppia nel 2008 e **porterà** a nuove regole.* |\n| **Andare + Participio Passato** | Obrigação (*deve ser*) ou perda acidental | *Questa norma **va cambiata**.* / *L'archivio è **andato perduto**.* |\n\n#### 2. Expressões Idiomáticas do Jornalismo Italiano\n- **Fumata nera / fumata bianca:** fracasso / sucesso em uma negociação.\n- **Braccio di ferro:** queda de braço / disputa acirrada entre duas partes.\n- **Tagliola / Stangata:** corte brusco / golpe financeiro (aumento de tarifas ou impostos).\n- **Scendere in campo:** entrar na disputa política ou empresarial.",
        "tabela_visual": make_tabela_visual("Chaves do Italiano Jornalístico", [
            ("Condizionale di Dissociazione", "Avrebbe dichiarato / Sarebbe fuggito (segundo fontes)"),
            ("Manchete Nominal", "Tasse, nuovo decreto del governo (sem verbo finito)"),
            ("Andare + Particípio", "Il modulo va firmato (= deve ser assinado)"),
            ("Jargão Político", "Fumata nera (sem acordo) | Braccio di ferro (impasse)")
        ]),
        "observacao_cards": [
            {"italiano": "Secondo le prime indiscrezioni, l'accordo sarebbe vicino.", "traducao": "Segundo os primeiros bastidores, o acordo estaria próximo.", "artigo": "Cond. Giornal.", "genero": "imprensa", "motivo": "O condicional 'sarebbe' indica rumor ou informação ainda não oficializada."},
            {"italiano": "La domanda va presentata entro il 30 giugno.", "traducao": "O requerimento deve ser apresentado até 30 de junho.", "artigo": "Va + Part.", "genero": "passiva de dever", "motivo": "Nos tempos simples, 'andare + particípio' expressa obrigação passiva (= deve essere presentata)."},
            {"italiano": "Vertice nella notte: ancora fumata nera sul salario minimo.", "traducao": "Cúpula durante a noite: ainda sem acordo sobre o salário mínimo.", "artigo": "Fumata nera", "genero": "jargão midiático", "motivo": "Alusão ao conclave papal: 'fumata nera' significa reunião encerrada sem consenso."}
        ],
        "exemplos_prc": [
            {"oracao": "Tre persone sarebbero rimaste ferite nell'incidente.", "pergunta": "Por que o jornalista escreveu 'sarebbero rimaste' em vez de 'sono rimaste'?", "resposta": "Três pessoas teriam ficado feridas no acidente.", "conclusao": "É o condicional jornalístico: o número exato de feridos ainda aguarda confirmação oficial."},
            {"oracao": "Nel rogo sono andati distrutti preziosi manoscritti.", "pergunta": "Qual é a diferença entre 'andare distrutto' e 'andare modificato'?", "resposta": "No incêndio foram destruídos preciosos manuscritos.", "conclusao": "Com verbos de perda/destruição (perduto, distrutto, smarrito), 'andare' indica acontecimento acidental, e não obrigação."}
        ],
        "armadilhas": [
            {"errado": "La legge è andata approvata ieri dal Parlamento.", "certo": "La legge è stata approvata ieri. / La legge va approvata subito.", "motivo": "'Andare + particípio' com sentido de obrigação ('deve ser') NÃO pode ser usado nos tempos compostos (passato prossimo)."},
            {"errado": "Il presidente ha detto che si dimetterebbe ieri.", "certo": "Il presidente avrebbe dato le dimissioni ieri.", "motivo": "Para expressar notícia não confirmada no passado, usa-se o Condizionale Composto (avrebbe dato)."}
        ],
        "ponte": "**Em português:** O nosso jornalismo também usa o futuro do pretérito composto (*O ministro teria se demitido*). Já a estrutura **va fatto** (*deve ser feito*) não tem equivalente literal com o verbo *ir* em português — traduza sempre por *deve ser + particípio*.",
        "coda": "Ao ler notícias em italiano: viu condicional sem *se*? É informação de bastidores. Viu *va + particípio*? Significa *deve ser feito*.",
        "exemplos": [
            "Svolta nelle indagini: l'uomo sarebbe stato ripreso dalle telecamere.",
            "Caro bollette, in arrivo una nuova stangata per le famiglie.",
            "Il testo del decreto va rivisto prima del voto in aula."
        ]
    },
    "c1-vi": {
        "alerta": "O uso avançado de Infinito, Gerundio e Participio (orações implícitas) é o que separa uma escrita fluida e nativa de um texto travado cheio de 'che' repetitivos.",
        "inventario": [
            "Gerundio Composto causal/temporal: Avendo vissuto a Roma, conosco bene la città.",
            "Participio Passato Absoluto: Finanziato il progetto, sono iniziati i lavori.",
            "Infinito Passato após verbos e preposições: Credo di aver capito / Dopo aver letto.",
            "Restrição de sujeito: o Gerúndio refere-se por regra ao sujeito da oração principal."
        ],
        "definicao": {
            "fenomeno": "As formas nominais do verbo (*modi indefiniti*: infinito, participio, gerundio) permitem comprimir orações subordinadas inteiras sem usar conjunções nem pronomes relativos.",
            "causa": "Quando podemos usar o Gerúndio ou o Infinitivo, e quando o Participio Passato pode ter um sujeito próprio (construção absoluta)?",
            "conceito": "Nas subordinadas implícitas com **Infinito** e **Gerundio**, exige-se normalmente correferência de sujeito com a oração principal. Já o **Participio Passato Absoluto** (*Risolto il problema, siamo partiti*) permite sujeito próprio e equivale a uma temporal/causal passiva (*Dopo che il problema è stato risolto*)."
        },
        "tecnica": "**Como usar os Modi Indefiniti com precisão de nível C1:**\n\n1. **Anterioridade no Infinitivo:** Use *dopo + infinito passato* (*Dopo aver mangiato*, *Dopo essere usciti*).\n2. **Causa/Anterioridade no Gerúndio:** Use o **Gerundio Composto** (*Essendo arrivato in ritardo, ha perso il treno* = Como chegou atrasado).\n3. **Particípio Absoluto (elegância máxima):** Comece a frase com o particípio concordando em gênero e número com o elemento concluído: *Terminata la riunione, i soci hanno firmato il verbale*.\n4. **Verifique o sujeito do Gerúndio:** O sujeito do gerúndio deve coincidir com o sujeito da principal (evite ambiguidades!).",
        "teoria": "### Modi Indefiniti Avanzati (Infinito, Gerundio, Participio)\n\nOs **modi indefiniti** substituem subordinadas explícitas, conferindo concisão e ritmo à prosa italiana.\n\n| Forma Implícita | Equivalente Explícito | Exemplo C1 |\n|---|---|---|\n| **Gerundio Presente** | Causal / Condicional / Temporal | ***Sapendo** che eri qui, sono passato.* (= Poiché sapevo) |\n| **Gerundio Composto** | Causal / Temporal anterior | ***Avendo terminato** i fondi, il progetto si è fermato.* |\n| **Participio Passato Assoluto** | *Dopo che / Una volta che* | ***Superata** la crisi, l'azienda è cresciuta.* |\n| **Infinito Passato** | Completiva / Temporal anterior | *Si è scusato **per non essere venuto**.* |\n| **Participio Presente** | Relativa formal/burocrática | *I documenti **attestanti** la residenza...* (= che attestano) |",
        "tabela_visual": make_tabela_visual("Estruturas Implícitas de Nível C1", [
            ("Gerundio Composto", "Avendo capito / Essendo partito (Causa ou tempo anterior)"),
            ("Participio Assoluto", "Finita la festa, tutti sono tornati a casa (Concorda com 'la festa')"),
            ("Infinito Passato", "Dopo aver detto / Penso di essere stato"),
            ("Participio Presente", "Avente diritto / Riguardante (= che ha / che riguarda)")
        ]),
        "observacao_cards": [
            {"italiano": "Essendo rimasto senza soldi, ha chiesto un prestito.", "traducao": "Tendo ficado sem dinheiro, pediu um empréstimo.", "artigo": "Ger. Comp.", "genero": "causal anterior", "motivo": "O Gerundio Composto com 'essere' concorda com o sujeito (rimasto) e indica a causa anterior."},
            {"italiano": "Approvata la legge, il governo ha convocato la stampa.", "traducao": "Aprovada a lei, o governo convocou a imprensa.", "artigo": "Part. Assol.", "genero": "temporal", "motivo": "O Participio Passato Absoluto concorda com 'la legge' (approvata) mesmo tendo sujeito diferente da principal."},
            {"italiano": "Mi dispiace di non averti potuto aiutare ieri.", "traducao": "Sinto muito por não ter podido te ajudar ontem.", "artigo": "Inf. Pass.", "genero": "anterioridade", "motivo": "O Infinito Passato (averti potuto aiutare) marca ação anterior ao sentimento presente."}
        ],
        "exemplos_prc": [
            {"oracao": "Pur avendo studiato molto, non si sentiva pronto.", "pergunta": "Qual é o valor de 'Pur + gerúndio'?", "resposta": "Mesmo tendo estudado muito, não se sentia pronto.", "conclusao": "'Pur + gerundio' (presente ou composto) cria uma subordinada concessiva implícita muito elegante (= Benché avesse studiato)."},
            {"oracao": "Chiusi gli sportelli, non sarà più possibile accedere.", "pergunta": "Por que 'Chiusi' está no masculino plural?", "resposta": "Fechados os guichês, não será mais possível entrar.", "conclusao": "No particípio absoluto, o particípio concorda obrigatoriamente com o seu próprio sujeito ('gli sportelli')."}
        ],
        "armadilhas": [
            {"errado": "Camminando per strada, la pioggia mi ha bagnato.", "certo": "Mentre camminavo per strada, la pioggia mi ha bagnato.", "motivo": "Em italiano, o sujeito do gerúndio deve ser o mesmo da oração principal (quem caminhava era 'eu', não 'a chuva')."},
            {"errado": "Dopo avere arrivato a casa, ho telefonato.", "certo": "Dopo essere arrivato a casa, ho telefonato.", "motivo": "Verbos intransitivos de movimento (arrivare, partire, andare) exigem o auxiliar ESSERE também no Infinito Passato e no Gerundio Composto."}
        ],
        "ponte": "**Em português:** Temos o infinitivo pessoal flexionado (*Depois de chegarmos*). O italiano **não possui infinitivo pessoal**: se o sujeito for o mesmo, usa-se o *Infinito Passato* (*Dopo essere arrivati*); se os sujeitos forem diferentes, usa-se *Dopo che + verbo conjugado* ou o *Participio Assoluto*.",
        "coda": "Destaque estilístico C1: use **Pur + gerundio** (*Pur sapendo che...* = Mesmo sabendo que...) para concessivas curtas e elegantes.",
        "exemplos": [
            "Pur condividendo le tue premesse, giungo a una conclusione diversa.",
            "Risolti i problemi tecnici, la piattaforma è tornata operativa.",
            "Si rammarica di non aver colto quell'opportunità."
        ]
    },
    "c1-vii": {
        "alerta": "Dominar o léxico setorial do Direito, Economia e Política é indispensável para ler contratos, editais públicos, notícias financeiras e atuar profissionalmente na Itália.",
        "inventario": [
            "Direito: entrare in vigore, abrogare, ricorso, sentenza passata in giudicato, ai sensi di",
            "Economia: fatturato, gettito fiscale, tasso d'interesse, potere d'acquisto, inflazione",
            "Política e Administração: disegno di legge (DDL), decreto-legge, fiducia, promulgare",
            "Colocações fixas: stipulare un contratto, presentare le dimissioni, bandire un concorso"
        ],
        "definicao": {
            "fenomeno": "Nos textos jurídicos, econômicos e institucionais, verbos genéricos como *fare*, *dire* ou *cambiare* dão lugar a colocações técnicas precisas (*stipulare, sancire, emendare, erogare*).",
            "causa": "Por que não se diz 'fare un contratto' ou 'fare una legge' em contextos formais?",
            "conceito": "Os **linguaggi settoriali** utilizam termos monorreferenciais (cada palavra tem um significado técnico único e inequívoco) e colocações verbo-nominais cristalizadas (*stipulare un contratto, promulgare una legge, erogare un finanziamento*)."
        },
        "tecnica": "**Colocações técnicas essenciais para memorizar em blocos:**\n\n1. **Contratos e Normas:** *stipulare / rescindere un contratto*; *approvare / promulgare / abrogare una legge*; *ai sensi dell'articolo 5* (nos termos do art. 5º).\n2. **Finanças e Empresas:** *registrare un calo / un incremento del fatturato*; *stanziare fondi* (alocar verbas); *erogare un prestito* (conceder um empréstimo).\n3. **Justiça:** *sporgere denuncia* (registrar queixa); *impugnare una sentenza* (recorrer de uma sentença); *emettere un verdetto*.\n4. **Instituições:** *porre la questione di fiducia* (voto de confiança parlamentar); *indire le elezioni* (convocar eleições).",
        "teoria": "### Lessico Settoriale: Diritto, Economia e Politica\n\nO domínio das **collocazioni tecnico-specialistiche** garante precisão e autoridade profissional.\n\n#### 1. Direito e Burocracia (*Linguaggio Giuridico-Amministrativo*)\n| Expressão Técnica | Significado em Português | Uso em Frase |\n|---|---|---|\n| **Ai sensi di / In conformità a** | Nos termos de / Em conformidade com | *Ai sensi dell'art. 12 del codice civile...* |\n| **Stipulare / Rescindere** | Celebrar (assinar) / Rescindir | *Le parti hanno stipulato un contratto.* |\n| **Entrare in vigore / Abrogare** | Entrar em vigor / Revogar | *La norma entrerà in vigore a gennaio.* |\n| **Sporgere denuncia** | Apresentar queixa / Boletim de ocorrência | *La vittima ha sporto denuncia.* |\n\n#### 2. Economia e Política (*Economia e Istituzioni*)\n- **Fatturato / Utile netto:** faturamento bruto / lucro líquido.\n- **Stanziare fondi:** destinar/liberar recursos orçamentários.\n- **Gettito fiscale / Evasione fiscale:** arrecadação tributária / sonegação fiscal.\n- **Disegno di legge (DDL) / Decreto-legge:** projeto de lei / medida provisória com força de lei.",
        "tabela_visual": make_tabela_visual("Colocações Profissionais (Verbo + Substantivo)", [
            ("Contratos", "Stipulare (celebrar) / Rescindere (resilir) un contratto"),
            ("Leis", "Promulgare (promulgar) / Abrogare (revogar) una legge"),
            ("Orçamento", "Stanziare fondi (alocar verbas) / Erogare un credito"),
            ("Justiça", "Sporgere denuncia (dar queixa) / Impugnare una sentenza")
        ]),
        "observacao_cards": [
            {"italiano": "Il governo ha stanziato due miliardi per la sanità.", "traducao": "O governo destinou dois bilhões para a saúde.", "artigo": "Stanziare", "genero": "economia pública", "motivo": "'Stanziare fondi/risorse' é o verbo técnico exato para alocar verbas no orçamento."},
            {"italiano": "Il contratto è disciplinato ai sensi della legge italiana.", "traducao": "O contrato é regido nos termos da lei italiana.", "artigo": "Ai sensi di", "genero": "jurídico", "motivo": "'Ai sensi di' é a locução prepositiva jurídica padrão para citar leis e artigos."},
            {"italiano": "L'azienda ha registrato un incremento del fatturato del 12%.", "traducao": "A empresa registrou um aumento de 12% no faturamento.", "artigo": "Fatturato", "genero": "finanças", "motivo": "'Fatturato' refere-se à receita total de vendas; o lucro descontadas as despesas é 'l'utile'."}
        ],
        "exemplos_prc": [
            {"oracao": "Il Presidente della Repubblica promulga le leggi approvate dal Parlamento.", "pergunta": "Qual é a diferença entre 'approvare' e 'promulgare'?", "resposta": "O Presidente da República promulga as leis aprovadas pelo Parlamento.", "conclusao": "O Parlamento aprova (vota) o texto; o Presidente da República o promulga oficialmente para que entre em vigor."},
            {"oracao": "Il cittadino può presentare ricorso entro trenta giorni dalla notifica.", "pergunta": "O que significa 'presentare ricorso'?", "resposta": "O cidadão pode interpor recurso em até trinta dias após a notificação.", "conclusao": "Colocação jurídica formal para contestar uma multa, decisão administrativa ou sentença."}
        ],
        "armadilhas": [
            {"errado": "Abbiamo fatto una denuncia alla polizia.", "certo": "Abbiamo sporto denuncia alla polizia.", "motivo": "No registro formal e jurídico, o verbo que acompanha 'denuncia' ou 'querela' é 'sporgere' (particípio: sporto)."},
            {"errado": "La legge è stata cancellata dalla Corte Costituzionale.", "certo": "La legge è stata abrogata (o dichiarata incostituzionale).", "motivo": "Leis não são 'cancellate', mas sim 'abrogate' (revogadas) ou 'emendate' (emendadas)."}
        ],
        "ponte": "**Em português:** Muitos termos jurídicos vêm do mesmo fundo latino (*ab-rogar, promulgar, rescindir, interpor recurso*). Atenção ao falso amigo parcial **fatturato** (faturamento/receita bruta) versus **utile** (lucro).",
        "coda": "Troque o verbo *fare* por verbos de precisão: *stipulare* (contrato), *sporgere* (denúncia), *stanziare* (verbas), *bandire* (concurso).",
        "exemplos": [
            "L'aumento dei tassi d'interesse ha ridotto il potere d'acquisto delle famiglie.",
            "Il bando di concorso scade improrogabilmente il prossimo lunedì.",
            "La clausola vessatoria è nulla ai sensi del Codice del Consumo."
        ]
    },
    "c1-viii": {
        "alerta": "Expressões idiomáticas e metáforas cristalizadas carregam séculos de história italiana: traduzi-las palavra por palavra leva a mal-entendidos graves.",
        "inventario": [
            "Essere al verde (estar sem dinheiro) | Avere le mani bucate (ser gastador)",
            "Prendere fischi per fiaschi (confundir alhos com bugalhos)",
            "Piove sul bagnato (desgraça pouca é bobagem / chover no molhado como agravamento)",
            "Fare il passo più lungo della gamba (dar o passo maior que a perna)",
            "Gettare la spugna (jogar a toalha) | Menare il can per l'aia (enrolar / fugir do assunto)"
        ],
        "definicao": {
            "fenomeno": "Na comunicação de nível C1, falantes nativos usam metáforas lexicais (*avere un diavolo per capello*, *toccare il cielo con un dito*) cujo sentido global não pode ser deduzido somando as palavras isoladas.",
            "causa": "Por que algumas metáforas parecem idênticas ao português, mas têm sentido diferente (como 'piove sul bagnato')?",
            "conceito": "As **espressioni idiomatiche** e **metafore lessicalizzate** refletem referências culturais históricas (como as velas verdes dos leilões falidos em *essere al verde*). Dominar seu registro e suas sutilezas semânticas garante fluência natural."
        },
        "tecnica": "**Como interpretar e usar expressões figuradas em italiano:**\n\n1. **Identifique o campo semântico:** Corpo humano (*avere sale in zucca* = ter juízo na cabeça; *costare un occhio della testa*), cores (*essere al verde*; *passare la notte in bianco*), animais (*in bocca al lupo*).\n2. **Cuidado com os falsos gêmeos idiomáticos:** Em italiano, *Piove sul bagnato* significa que um problema novo se soma a uma situação já ruim (*Desgraça pouca é bobagem*), e não *fazer algo inútil*!\n3. **Adapte ao registro:** Expressões como *menare il can per l'aia* (enrolar) ou *prendere due piccioni con una fava* cabem perfeitamente em crônicas, debates e conversas cultas.",
        "teoria": "### Metafore e Linguaggio Figurato\n\nO domínio do **linguaggio figurato** é um indicador decisivo de proficiência C1.\n\n#### 1. Expressões Idiomáticas Essenciais\n| Expressão Italiana | Sentido Real em Português | Origem / Nuance |\n|---|---|---|\n| **Essere al verde** | Estar sem dinheiro / duro | Velas de leilão tinham a base verde quando acabavam |\n| **Prendere fischi per fiaschi** | Confundir alhos com bugalhos | Trocar uma coisa por outra totalmente diferente |\n| **Menare il can per l'aia** | Enrolar / rodear sem ir ao ponto | Passear o cão pelo pátio para ganhar tempo |\n| **Avere un diavolo per capello** | Estar furioso | Cada fio de cabelo tomado pela raiva |\n| **Piove sul bagnato** | Um azar em cima de outro (ou sorte sobre sorte) | Diferente do PT 'chover no molhado'! |\n| **Mettere la pulce nell'orecchio** | Colocar uma pulga atrás da orelha | Despertar uma suspeita ou dúvida |",
        "tabela_visual": make_tabela_visual("Expressões Idiomáticas C1 e seus Sentidos", [
            ("Essere al verde", "Estar sem um tostão (oposto: navigare nell'oro)"),
            ("Prendere fischi per fiaschi", "Entender tudo errado / confundir alhos com bugalhos"),
            ("Menare il can per l'aia", "Enrolar na conversa / fugir do ponto principal"),
            ("Piove sul bagnato", "Agravamento de algo já difícil (falso gêmeo do PT!)")
        ]),
        "observacao_cards": [
            {"italiano": "Hai preso fischi per fiaschi: non volevo criticarti!", "traducao": "Você confundiu alhos com bugalhos: eu não queria te criticar!", "artigo": "Idiomático", "genero": "mal-entendido", "motivo": "'Prendere fischi per fiaschi' significa interpretar equivocadamente uma situação ou fala."},
            {"italiano": "Smettila di menare il can per l'aia e dimmi la verità.", "traducao": "Pare de enrolar e me diga a verdade.", "artigo": "Figurativo", "genero": "conversação", "motivo": "Indica quem divaga propositalmente para adiar uma resposta difícil."},
            {"italiano": "Oltre alla multa si è rotta anche l'auto: piove sempre sul bagnato!", "traducao": "Além da multa, o carro também quebrou: um azar nunca vem só!", "artigo": "Atenção!", "genero": "falso gêmeo", "motivo": "Em italiano, 'piovere sul bagnato' indica coisas que se acumulam onde já há excesso (geralmente problemas)."}
        ],
        "exemplos_prc": [
            {"oracao": "Dopo le vacanze estive sono completamente al verde.", "pergunta": "O que significa 'essere al verde'?", "resposta": "Depois das férias de verão estou completamente sem dinheiro.", "conclusao": "Refere-se ao fundo verde das antigas velas usadas em leilões públicos: quando a cera chegava ao verde, o tempo e os recursos haviam acabado."},
            {"oracao": "Con quella risposta evasiva mi ha messo la pulce nell'orecchio.", "pergunta": "Qual é o equivalente em português?", "resposta": "Com aquela resposta evasiva ele me colocou uma pulga atrás da orelha.", "conclusao": "Significa despertar uma dúvida persistente ou suspeita em alguém."}
        ],
        "armadilhas": [
            {"errado": "In bocca al lupo! — Grazie!", "certo": "In bocca al lupo! — Crepi il lupo! (ou: Viva il lupo!)", "motivo": "Na tradição italiana, responder 'Grazie' a 'In bocca al lupo' dá azar; responde-se 'Crepi (il lupo)!' ou modernamente 'Viva il lupo!'."},
            {"errado": "Ripetere questa regola è come piovere sul bagnato.", "certo": "Ripetere questa regola è del tutto superfluo (ou: è come portare vasi a Samo).", "motivo": "Em italiano, 'piovere sul bagnato' não significa 'ser redundante', mas sim acumular eventos sobre uma situação já saturada."}
        ],
        "ponte": "**Em português:** Compartilhamos dezenas de metáforas (*dar o passo maior que a perna* = *fare il passo più lungo della gamba*; *custar os olhos da cara* = *costare un occhio della testa*), mas atenção especial a *piovere sul bagnato* e *gettare la spugna* (*jogar a toalha*, literalmente 'a esponja').",
        "coda": "Incorporar uma expressão idiomática precisa na prova oral do C1 demonstra naturalidade e domínio cultural profundo.",
        "exemplos": [
            "Non fare il passo più lungo della gamba con questo investimento.",
            "Quando ha scoperto il tradimento, aveva un diavolo per capello.",
            "Dopo ore di trattativa hanno finalmente trovato la quadra."
        ]
    },
    "c1-ix": {
        "alerta": "No Discurso Indireto avançado, quando o verbo introdutor está no passado (*ha detto, pensava*), toda a grade de tempos verbais e expressões de tempo/espaço sofre um deslocamento sistemático.",
        "inventario": [
            "Presente → Imperfetto: 'Piove' → Ha detto che pioveva.",
            "Passato Prossimo → Trapassato Prossimo: 'Ho finito' → Ha detto che aveva finito.",
            "Futuro → Condizionale Composto: 'Verrò domani' → Ha detto che sarebbe venuto il giorno dopo.",
            "Deíticos: oggi → quel giorno | ieri → il giorno prima | qui → lì | questo → quello"
        ],
        "definicao": {
            "fenomeno": "A **consecutio temporum** (concordância dos tempos) e a transposição do discurso direto para o indireto no passado exigem o ajuste simultâneo de pronomes, advérbios de tempo/lugar e tempos verbais.",
            "causa": "Por que o futuro no passado ('Disse que viria') se expressa em italiano com o Condizionale Composto ('Ha detto che sarebbe venuto') e não com o Condizionale Semplice?",
            "conceito": "Esta é uma das regras mais importantes da gramática italiana: o **futuro no passado** (*futuro nel passato*) é expresso obrigatoriamente pelo **Condizionale Composto** (*avrebbe fatto, sarebbe andato*), enquanto o português usa o futuro do pretérito simples (*faria, iria*)."
        },
        "tecnica": "**Mapa de Transposição no Passado (*Ha detto che...*):**\n\n1. **Simultaneidade no passado:** Presente (*studio*) → **Imperfetto** (*studiava*).\n2. **Anterioridade no passado:** Passato Prossimo (*ho studiato*) → **Trapassato Prossimo** (*aveva studiato*).\n3. **Posterioridade (Futuro no passado):** Futuro (*studierò*) → **Condizionale Composto** (*avrebbe studiato*).\n4. **Imperativo:** *'Studia!'* → *Mi ha detto **di studiare***.\n5. **Advérbios (Deíticos):** *oggi → quel giorno*; *domani → il giorno dopo / l'indomani*; *ieri → il giorno prima*; *ora → allora*; *qui → lì*.",
        "teoria": "### Stile Indiretto e Consecutio Temporum Avanzata\n\nQuando o verbo declarativo está no passado (*ha detto, ha spiegato, sosteneva*), ocorre o deslocamento temporal e dêitico.\n\n| Discurso Direto | Discurso Indireto (Verbo no Passado) | Exemplo |\n|---|---|---|\n| **Presente** (*vado*) | **Imperfetto** (*andava*) | *«Sto bene» → Disse che **stava** bene.* |\n| **Passato Prossimo** (*sono andato*) | **Trapassato Prossimo** (*era andato*) | *«Ho capito» → Disse che **aveva capito**.* |\n| **Futuro Semplice** (*andrò*) | **Condizionale Composto** (*sarebbe andato*) | *«Partirò domani» → Disse che **sarebbe partito** il giorno dopo.* |\n| **Imperativo** (*vai!*) | **di + Infinito** (*di andare*) | *«Aspetta qui!» → Mi chiese **di aspettare** lì.* |\n| **Periodo Ipotetico Tipo 1** | **Tipo 3** (ou Tipo 2) | *«Se potrò, verrò» → Disse che se **avesse potuto**, **sarebbe venuto**.* |",
        "tabela_visual": make_tabela_visual("Transposição do Discurso Indireto no Passado", [
            ("Presente → Imperfetto", "«Lavoro qui» → Disse che lavorava lì"),
            ("Passato → Trapassato", "«Sono uscito ieri» → Disse che era uscito il giorno prima"),
            ("Futuro → Cond. Composto", "«Tornerò domani» → Disse che sarebbe tornato l'indomani"),
            ("Imperativo → di + Inf.", "«Chiudi la porta!» → Mi disse di chiudere la porta")
        ]),
        "observacao_cards": [
            {"italiano": "Marco mi ha promesso che sarebbe arrivato in orario.", "traducao": "Marco me prometeu que chegaria no horário.", "artigo": "Cond. Comp.", "genero": "futuro no passado", "motivo": "Em italiano, o futuro em relação a um verbo no passado usa SEMPRE o Condizionale Composto (sarebbe arrivato)."},
            {"italiano": "Mi chiese se avessi già visitato Firenze prima di allora.", "traducao": "Perguntou-me se eu já tinha visitado Florença antes daquilo.", "artigo": "Se + Trapass.", "genero": "interrogativa indireta", "motivo": "Interrogativas indiretas no passado admitem o Congiuntivo Trapassato (avessi visitato) no registro culto."},
            {"italiano": "Giulia disse che il giorno seguente avrebbe firmato il contratto.", "traducao": "Giulia disse que no dia seguinte assinaria o contrato.", "artigo": "Deítico", "genero": "transposição", "motivo": "'Domani' converte-se em 'il giorno seguente / l'indomani' e 'firmerò' em 'avrebbe firmato'."}
        ],
        "exemplos_prc": [
            {"oracao": "«Domani chiamerò l'avvocato» → Ha detto che il giorno dopo avrebbe chiamato l'avvocato.", "pergunta": "Por que não podemos dizer 'chiamerebbe' em italiano?", "resposta": "Ele disse que no dia seguinte ligaria para o advogado.", "conclusao": "No italiano padrão, o Condizionale Semplice expressa apenas hipótese presente; para posterioridade no passado, é obrigatório o Condizionale Composto."},
            {"oracao": "L'insegnante ci ordinò di consegnare i fogli immediatamente.", "pergunta": "Como o imperativo 'Consegnate!' foi transformado?", "resposta": "O professor nos ordenou entregar as folhas imediatamente.", "conclusao": "Ordens e pedidos no discurso indireto transformam-se em 'di + infinitivo' (ou 'che + congiuntivo imperfetto')."}
        ],
        "armadilhas": [
            {"errado": "Pensavo che Maria verrebbe alla festa ieri sera.", "certo": "Pensavo che Maria sarebbe venuta alla festa ieri sera.", "motivo": "Armadilha clássica para lusófonos: 'eu achava que ela viria' traduz-se obrigatoriamente com Condizionale Composto (sarebbe venuta)."},
            {"errado": "Ha detto che partirà il giorno prima.", "certo": "Ha detto che sarebbe partito il giorno dopo.", "motivo": "'Domani' no discurso indireto passado vira 'il giorno dopo' ou 'l'indomani' ('il giorno prima' corresponde a 'ieri')."}
        ],
        "ponte": "**Diferença crucial PT ↔ IT:** Em português dizemos *Ele disse que **viria*** (futuro do pretérito simples). Em italiano, isso é um erro gramatical! Deve-se dizer *Ha detto che **sarebbe venuto*** (Condizionale Composto).",
        "coda": "Grave esta equivalência de ouro: **PT: disse que faria = IT: ha detto che avrebbe fatto**.",
        "exemplos": [
            "Sapevo già che non avrebbero accettato la nostra offerta.",
            "Ci assicurò che entro quella sera tutto sarebbe stato risolto.",
            "Mi domandò dove fossi stato tutta la settimana precedente."
        ]
    },
    "c1-x": {
        "alerta": "A sintaxe marcada (dislocazione a sinistra, dislocazione a destra, frase scissa) altera a ordem padrão SVO para destacar o tema conhecido ou o foco informativo da frase.",
        "inventario": [
            "Dislocazione a sinistra (Tema + pronome clítico): Il libro, l'ho già letto.",
            "Dislocazione a destra (Pronome catafórico + Tema): L'ho già letto, il libro.",
            "Frase scissa (Foco contrastivo): È Marco che ha rotto il vaso / È a te che parlo.",
            "Tema sospeso / Anacoluto: Io, la mia patria è il mondo."
        ],
        "definicao": {
            "fenomeno": "Na língua viva e na prosa literária, o italiano raramente mantém a ordem rígida Sujeito-Verbo-Objeto quando quer enfatizar um elemento ou retomar algo já mencionado no diálogo.",
            "causa": "Por que em 'Il caffè, lo prendo amaro' o pronome 'lo' é obrigatório, mas em 'IL CAFFÈ voglio (non il tè)' não há pronome?",
            "conceito": "Na **dislocazione a sinistra** (*Il caffè, lo prendo amaro*), o objeto é deslocado como **tópico conhecido** e precisa ser retomado por um pronome clítico (*lo, la, li, le, ne, ci*). Já na **focalizzazione contrastiva** (*IL CAFFÈ voglio, non il tè*) ou na **frase scissa** (*È il caffè che voglio*), destaca-se uma informação nova/exclusiva sem pronome de retomada."
        },
        "tecnica": "**Como identificar e construir estruturas sintáticas marcadas:**\n\n1. **Dislocazione a sinistra:** Coloque o elemento no início da frase e retome-o obrigatoriamente com o clítico correspondente (*I documenti, **li** ho inviati ieri*; *Di questo problema, **ne** abbiamo già parlato*).\n2. **Dislocazione a destra:** Antecipe o clítico e coloque o elemento no final após breve pausa (*Non **ci** vado più, in quel ristorante*).\n3. **Frase Scissa:** Use *Essere + Foco + che + resto da frase* (*È con il direttore che voglio parlare*).\n4. **Frase Scissa Implícita:** Quando o foco é o sujeito, pode-se usar *a + infinitivo* (*Sei stato tu a dirlo* = Foi você quem disse isso).",
        "teoria": "### Sintassi Avanzata e Costruzioni Marcate\n\nAs **costruzioni marcate** organizam a estrutura informacional da frase entre **Tema** (dado conhecido) e **Rema / Focus** (informação nova).\n\n| Construção | Estrutura | Exemplo | Função Pragmática |\n|---|---|---|---|\n| **Dislocazione a sinistra** | Elemento + Clítico + Verbo | *La macchina, **l'**ho venduta.* | Retoma um tópico já ativo na conversa |\n| **Dislocazione a destra** | Clítico + Verbo, + Elemento | ***Lo** vuoi, un caffè?* | Suaviza perguntas e confirma o tópico no fim |\n| **Frase scissa** | *Essere* + Foco + *che* | ***È domani che** parte il treno.* | Isola e contrasta a informação nova |\n| **Scissa implicita** | *Essere* + Sujeito + *a* + Inf. | ***Sono stati loro a** chiamare.* | Destaca o agente da ação com elegância |",
        "tabela_visual": make_tabela_visual("Construções Sintáticas Marcadas (C1)", [
            ("Dislocazione a Sinistra", "La torta, l'ha preparata Giulia (Retomada com clítico)"),
            ("Dislocazione a Destra", "Ne abbiamo già discusso, di questo (Antecipação catafórica)"),
            ("Frase Scissa Explícita", "È a Roma che voglio vivere (Foco + che)"),
            ("Frase Scissa Implícita", "Sei stato tu a vincere (Foco sujeito + a + infinitivo)")
        ]),
        "observacao_cards": [
            {"italiano": "Le chiavi, le ho lasciate sul tavolo.", "traducao": "As chaves, eu as deixei sobre a mesa.", "artigo": "Disloc. SX", "genero": "tópico + clítico", "motivo": "O objeto direto deslocado à esquerda ('Le chiavi') exige retomada obrigatória pelo pronome 'le' e concordância do particípio (lasciate)."},
            {"italiano": "È stato il vento a far cadere l'albero.", "traducao": "Foi o vento que derrubou a árvore.", "artigo": "Scissa", "genero": "foco no sujeito", "motivo": "Frase scissa implícita: quando o foco é o sujeito, 'a + infinitivo' é muito natural e elegante."},
            {"italiano": "Lo prendi anche tu, un gelato?", "traducao": "Você também vai tomar um sorvete?", "artigo": "Disloc. DX", "genero": "afetivo / oral", "motivo": "Na dislocazione a destra, o pronome 'Lo' antecipa 'un gelato', criando tom coloquial e convidativo."}
        ],
        "exemplos_prc": [
            {"oracao": "I biglietti, li hai presi tu?", "pergunta": "Por que o particípio 'presi' está no masculino plural?", "resposta": "Os ingressos, foi você quem os comprou?", "conclusao": "Na dislocazione a sinistra, o pronome clítico 'li' precede o verbo 'avere', tornando obrigatória a concordância do particípio passado ('presi')."},
            {"oracao": "Non è il denaro che cerco, ma la serenità.", "pergunta": "Qual construção sintática é usada aqui?", "resposta": "Não é o dinheiro que procuro, mas a serenidade.", "conclusao": "É uma frase scissa negativa usada para criar foco contrastivo forte."}
        ],
        "armadilhas": [
            {"errado": "Le lettere, ho spedite stamattina.", "certo": "Le lettere, le ho spedite stamattina.", "motivo": "Na dislocazione a sinistra do objeto direto, o pronome clítico de retomada (lo/la/li/le) é obrigatório em italiano."},
            {"errado": "Le lettere, le ho spedito stamattina.", "certo": "Le lettere, le ho spedite stamattina.", "motivo": "Sempre que o pronome direto (lo, la, li, le) antecede o auxiliar avere, o particípio passado deve concordar em gênero e número (spedite)."}
        ],
        "ponte": "**Em português:** No Brasil dizemos *O livro, eu já li* sem pronome. Em italiano, omitir o pronome clítico na dislocação à esquerda soa incompleto: diga sempre *Il libro, **l'**ho già letto*.",
        "coda": "Lembre-se da regra de ouro: deslocou o objeto direto para o início da frase? Coloque o pronome (*lo/la/li/le*) antes do verbo e faça o particípio concordar!",
        "exemplos": [
            "Questo film, l'abbiamo già visto tre volte.",
            "È solo studiando con costanza che si raggiunge il livello C1.",
            "Non ci credo più, alle sue promesse."
        ]
    },
    "c2-i": {
        "alerta": "Conhecer a história da língua italiana — do latim vulgar às Três Coroas do Trecento, de Pietro Bembo a Manzoni e à unificação televisiva — explica por que o italiano tem a forma que tem hoje.",
        "inventario": [
            "Placito Capuano (960 d.C.): certidão de nascimento do vulgar escrito na Itália",
            "Le Tre Corone del Trecento: Dante Alighieri, Francesco Petrarca, Giovanni Boccaccio",
            "Questione della lingua ('500): Pietro Bembo e a codificação do florentino literário",
            "Alessandro Manzoni ('800): I Promessi Sposi e 'sciacquare i panni in Arno'",
            "Século XX: rádio, cinema e televisão (1954) difundem o italiano falado a toda a população"
        ],
        "definicao": {
            "fenomeno": "Diferente da França ou da Espanha, a Itália permaneceu politicamente fragmentada até 1861, mas manteve durante séculos uma língua literária comum extraordinariamente estável.",
            "causa": "Por que um italiano de hoje consegue ler a *Divina Commedia* de Dante (século XIV) com muito mais facilidade do que um inglês lê os textos medievais da mesma época?",
            "conceito": "Porque o italiano padrão nasceu diretamente do **volgare fiorentino letterario del Trecento** (consagrado por Dante, Petrarca e Boccaccio) e foi preservado na escrita culta por gramáticos como **Pietro Bembo** (1525) e pela **Accademia della Crusca** (1583), sofrendo pouca erosão fonética até se tornar língua falada nacional nos séculos XIX e XX."
        },
        "tecnica": "**Marcos essenciais da História da Língua Italiana (Nível C2):**\n\n1. **Origens (Séculos IX–X):** Transição do *latino parlato (volgare)* para os primeiros documentos escritos, como o *Indovinello Veronese* e o **Placito Capuano (960 d.C.)** (*Sao ko kelle terre...*).\n2. **O Trecento e as Três Coroas:** **Dante** (*De vulgari eloquentia* e *Commedia*, pai do plurilinguismo), **Petrarca** (*Canzoniere*, modelo poético) e **Boccaccio** (*Decameron*, modelo da prosa).\n3. **O Cinquecento:** **Pietro Bembo** (*Prose della volgar lingua*, 1525) vence a *Questione della lingua* impondo o florentino literário do século XIV.\n4. **O Ottocento e o Novecento:** **Manzoni** aproxima a língua escrita do florentino vivo culto (*I Promessi Sposi*, 1840), e a escola, o rádio e a **TV (RAI, 1954)** completam a unificação linguística real da população.",
        "teoria": "### Storia della Lingua Italiana: Dalle Origini al Novecento\n\nA história linguística da Itália é única na Europa: uma língua unificada primeiro pela **literatura** e só séculos depois pelo **Estado**.\n\n| Época | Marco Histórico | Importância Linguística |\n|---|---|---|\n| **960 d.C.** | **Placito Capuano** | Primeiro documento oficial com fórmula deliberada em vulgar italiano |\n| **Séc. XIII** | **Scuola Siciliana** & **Dolce Stil Novo** | Primeiras escolas poéticas em vulgar na corte de Frederico II e na Toscana |\n| **Séc. XIV** | **Dante, Petrarca, Boccaccio** | As *Tre Corone* elevam o florentino a língua literária de prestígio europeu |\n| **1525 / 1612** | **Pietro Bembo** & **Vocabolario della Crusca** | Codificação gramatical e primeiro grande dicionário normativo da Europa |\n| **1840 / 1861** | **Manzoni** & **Unificação da Itália** | Adoção do florentino culto vivo; em 1861, apenas ~2,5% a 10% falavam italiano |\n| **Séc. XX** | **Escolarização, Rádio e TV (1954)** | Tullio De Mauro mostra como a mídia transformou o italiano em língua materna de todos |",
        "tabela_visual": make_tabela_visual("Linha do Tempo da Língua Italiana", [
            ("960 d.C. — Placito Capuano", "«Sao ko kelle terre...» — 1º registro oficial em vulgar"),
            ("1300 — Le Tre Corone", "Dante (Commedia), Petrarca (poesia), Boccaccio (prosa)"),
            ("1525 — Pietro Bembo", "Prose della volgar lingua: fixa o modelo florentino do '300"),
            ("1840 — Alessandro Manzoni", "I Promessi Sposi: renova a prosa no florentino vivo culto")
        ]),
        "observacao_cards": [
            {"italiano": "Il Placito Capuano (960 d.C.): «Sao ko kelle terre...»", "traducao": "O Plácito de Cápua (960 d.C.): «Sei que aquelas terras...»", "artigo": "960 d.C.", "genero": "origem", "motivo": "Considerado o ato de nascimento do vulgar italiano escrito, inserido como testemunho dentro de um documento jurídico em latim."},
            {"italiano": "Le Tre Corone fiorentine: Dante, Petrarca e Boccaccio.", "traducao": "As Três Coroas florentinas: Dante, Petrarca e Boccaccio.", "artigo": "Trecento", "genero": "prestígio literário", "motivo": "O prestígio imenso de suas obras fez com que o dialeto florentino se tornasse a base do italiano padrão."},
            {"italiano": "Manzoni andò a Firenze per «sciacquare i panni in Arno».", "traducao": "Manzoni foi a Florença para «enxaguar as roupas no rio Arno».", "artigo": "Ottocento", "genero": "unificação", "motivo": "Metáfora célebre de Manzoni para a revisão linguística de 'I Promessi Sposi' (1840), substituindo lombardismos e arcaísmos pelo florentino vivo culto."}
        ],
        "exemplos_prc": [
            {"oracao": "Nel 'De vulgari eloquentia', Dante cerca il 'volgare illustre'.", "pergunta": "Em que língua Dante escreveu o tratado 'De vulgari eloquentia' e por quê?", "resposta": "No 'De vulgari eloquentia', Dante busca o 'vulgar ilustre'.", "conclusao": "Dante escreveu o tratado em latim para convencer os doutos e eruditos da época sobre a dignidade literária da língua vulgar."},
            {"oracao": "Nel Cinquecento Pietro Bembo indicò Petrarca per la poesia e Boccaccio per la prosa.", "pergunta": "Qual foi a consequência da teoria de Bembo?", "resposta": "No século XVI, Pietro Bembo indicou Petrarca para a poesia e Boccaccio para a prosa.", "conclusao": "Garantiu a unidade escrita do italiano entre os intelectuais de toda a península, preservando as estruturas do século XIV."}
        ],
        "armadilhas": [
            {"errado": "L'italiano moderno deriva dal latino classico scritto da Cicerone.", "certo": "L'italiano moderno deriva dal latino volgare (parlato) attraverso il fiorentino del Trecento.", "motivo": "As línguas românicas evoluíram do latim falado cotidiano (latino volgare), não do latim literário clássico."},
            {"errado": "Nel 1861, al momento dell'Unità, tutti gli italiani parlavano già l'italiano standard.", "certo": "Nel 1861 la grande maggioranza della popolazione era dialettofona; l'italiano era lingua soprattutto scritta.", "motivo": "Na unificação política (1861), a comunicação oral cotidiana ocorria quase inteiramente nos dialetos locais."}
        ],
        "ponte": "**Paralelo histórico:** Enquanto o português foi unificado cedo pela corte real de Lisboa/Coimbra, o italiano foi unificado pelos seus escritores e poetas mais de quinhentos anos antes de existir o Estado italiano moderno.",
        "coda": "Resumo C2: **Latim Vulgar → Placito Capuano (960) → Dante/Petrarca/Boccaccio ('300) → Bembo ('500) → Manzoni ('800) → TV/De Mauro ('900)**.",
        "exemplos": [
            "L'Accademia della Crusca pubblicò nel 1612 il primo grande vocabolario storico della lingua italiana.",
            "Con l'avvento della televisione nel 1954, l'italiano divenne finalmente una lingua parlata da tutta la nazione.",
            "Il plurilinguismo dantesco si contrappone al monolinguismo selettivo di Petrarca."
        ]
    },
    "c2-ii": {
        "alerta": "As figuras de retórica (metafora, metonimia, sineddoche, chiasmo, ossimoro, litote, ipallage) são ferramentas essenciais para analisar literatura italiana e escrever com maestria estilística.",
        "inventario": [
            "Tropos de significado: metafora, similitudine, metonimia, sineddoche, sinestesia",
            "Figuras de pensamento e contraste: antitesi, ossimoro, litote, iperbole, ironia",
            "Figuras de sintaxe e ordem: chiasmo (ABBA), anafora, anastrofe, ipallage, zeugma",
            "Figuras de som: allitterazione, onomatopea, paronomasia"
        ],
        "definicao": {
            "fenomeno": "Na poesia, na retórica política e na crítica literária italiana, o sentido estético e persuasivo nasce do desvio intencional em relação à linguagem literal.",
            "causa": "Como distinguir com exatidão figuras próximas, como *Metafora vs Similitudine*, *Metonimia vs Sineddoche* ou *Antitesi vs Ossimoro*?",
            "conceito": "A **Similitudine** compara explicitamente com *come/sembra* (*forte come un leone*), enquanto a **Metafora** funde os conceitos diretamente (*sei un leone*). A **Metonimia** substitui por contiguidade lógica (autor pela obra: *leggere Dante*; continente pelo conteúdo: *bere un bicchiere*), enquanto a **Sineddoche** substitui por relação de quantidade parte/todo (*una vela all'orizzonte* = um barco). O **Ossimoro** une dois termos contraditórios num mesmo sintagma (*ghiaccio bollente*), enquanto a **Antitesi** contrapõe ideias em frases ou orações (*Pace non trovo, e non ho da far guerra*)."
        },
        "tecnica": "**Guia Rápido de Identificação de Figuras Retóricas (C2):**\n\n1. **Tem 'come' / 'pare'?** → **Similitudine**. Fala direta sem conectivo (*I tuoi occhi sono stelle*)? → **Metafora**.\n2. **Mistura dois sentidos sensoriais diferentes** (*urlo nero*, *dolce rumore*)? → **Sinestesia**.\n3. **Nega o oposto para afirmar de forma atenuada** (*Non è una cattiva idea* = é uma boa ideia; *Don Abbondio non era nato con un cuor di leone*)? → **Litote**.\n4. **Estrutura cruzada em espelho (A-B / B-A)** (*Le donne, i cavalier, l'arme, gli amori*)? → **Chiasmo**.",
        "teoria": "### Retorica e Stile Letterario: Le Figure del Linguaggio\n\nO estudo das **figure retoriche** divide-se em três grandes categorias: figuras de **significado (tropi)**, de **sintaxe (costruzione)** e de **pensamento**.\n\n| Figura Retórica | Definição Técnica | Exemplo Clássico Italiano |\n|---|---|---|\n| **Metafora** | Transferência de sentido sem conectivo comparativo | *«La vita è un sogno»* / *«Il fuoco della passione»* |\n| **Metonimia** | Substituição por causa/efeito, continente/conteúdo, autor/obra | *«Ascoltare Verdi»* / *«Bere un buon bicchiere»* |\n| **Sineddoche** | Substituição da parte pelo todo (ou singular pelo plural) | *«Tornare al tetto natio»* (= alla casa) |\n| **Sinestesia** | Associação de esferas sensoriais distintas | *«Parole calde»* / *«L'urlo nero della madre»* (Quasimodo) |\n| **Ossimoro** | União sintática de duas palavras de sentido oposto | *«Tacito tumulto»* (Pascoli) / *«Silenzio assordante»* |\n| **Antitesi** | Contraposição simétrica de conceitos opostos na frase | *«Pace non trovo, e non ho da far guerra»* (Petrarca) |\n| **Litote** | Afirmação obtida pela negação do seu contrário | *«Non era un genio»* (= era mediocre) |\n| **Chiasmo** | Disposição cruzada AB-BA de elementos sintáticos | *«Ovidio è il terzo, e l'ultimo Lucano»* (Dante) |",
        "tabela_visual": make_tabela_visual("Distinções Clássicas da Retórica C2", [
            ("Metafora vs Similitudine", "La vita è un sogno (Metafora) vs è come un sogno (Similitudine)"),
            ("Metonimia vs Sineddoche", "Leggere Dante (Autor/Obra) vs Quindici primavere (Parte/Todo)"),
            ("Ossimoro vs Antitesi", "Ghiaccio bollente (1 sintagma) vs Odi et amo (2 polos na frase)"),
            ("Litote vs Chiasmo", "Non mi dispiace (nega o oposto) vs A-B / B-A (espelhamento)")
        ]),
        "observacao_cards": [
            {"italiano": "«Pace non trovo, e non ho da far guerra» (Petrarca)", "traducao": "«Paz não encontro, e não tenho com que fazer guerra»", "artigo": "Antitesi", "genero": "contraste", "motivo": "Contrapõe os conceitos opostos 'pace' e 'guerra' em orações coordenadas."},
            {"italiano": "C'era un silenzio assordante nella sala.", "traducao": "Havia um silêncio ensurdecedor na sala.", "artigo": "Ossimoro", "genero": "paradoxo", "motivo": "Une diretamente um substantivo ('silenzio') a um adjetivo que o contradiz ('assordante')."},
            {"italiano": "Il risultato non è affatto male.", "traducao": "O resultado não é nada mau (= é muito bom).", "artigo": "Litote", "genero": "atenuação", "motivo": "Afirma-se uma qualidade positiva negando o seu oposto ('non è male')."}
        ],
        "exemplos_prc": [
            {"oracao": "Ho bevuto due bicchieri e ho letto tutto Manzoni.", "pergunta": "Qual figura retórica aparece em 'bere due bicchieri' e 'leggere Manzoni'?", "resposta": "Bebi dois copos e li todo o Manzoni.", "conclusao": "Trata-se de Metonímia: o continente pelo conteúdo ('bicchieri' pelo líquido) e o autor pela obra ('Manzoni' pelos seus livros)."},
            {"oracao": "«Le donne, i cavalier, l'arme, gli amori» (Ariosto, Orlando Furioso)", "pergunta": "Por que este verso famoso de Ariosto é um Chiasmo (ABBA)?", "resposta": "«As damas, os cavaleiros, as armas, os amores»", "conclusao": "'Le donne' (A) liga-se a 'gli amori' (A' nas extremidades), enquanto 'i cavalier' (B) liga-se a 'l'arme' (B' no centro), formando o cruzamento AB-B'A'."}
        ],
        "armadilhas": [
            {"errado": "«Sei furbo come una volpe» è una metafora.", "certo": "«Sei furbo come una volpe» è una similitudine; «Sei una volpe» è una metafora.", "motivo": "A presença do conectivo comparativo 'come' caracteriza a Similitudine, e não a Metafora."},
            {"errado": "«Un silenzio assordante» è un'antitesi.", "certo": "«Un silenzio assordante» è un ossimoro.", "motivo": "Quando os dois termos opostos formam um único sintagma (substantivo + adjetivo), a figura chama-se Ossimoro."}
        ],
        "ponte": "**Em português:** Os nomes e conceitos retóricos são praticamente idênticos (*metáfora, metonímia, sinédoque, quiasmo, oxímoro, lítotes, sinestesia*). Atenção à grafia italiana com consoantes duplas (*allitterazione, ossimoro, sineddoche*).",
        "coda": "Dica rápida: **Come** = Similitudine; **Sintagma contraditório** = Ossimoro; **Não + contrário** = Litote; **Cruzamento ABBA** = Chiasmo.",
        "exemplos": [
            "L'anafora consiste nella ripetizione di una parola all'inizio di versi successivi («Per me si va...»). ",
            "Nella sinestesia si associano sensazioni appartenenti a sfere sensoriali diverse («profumo dolce», «voce chiara»).",
            "L'iperbole esagera la realtà oltre il verosimile («Te l'ho detto mille volte!»)."
        ]
    },
    "c2-iii": {
        "alerta": "O italiano não é um bloco monolítico: varia conforme a região geográfica (diatopia), o grupo social (diastratia), a situação comunicativa (diafasia) e o meio físico (diamesia).",
        "inventario": [
            "Diatopia (espaço): dialetti primari vs italiano regionale vs geosinonimi (anguria/cocomero)",
            "Diastratia (camada social/escolaridade): italiano colto vs italiano popolare",
            "Diafasia (situação e contexto): registro aulico/formale vs familiare/colloquiale vs linguaggi settoriali",
            "Diamesia (canal): italiano scritto, parlato, trasmesso/digitale",
            "Italiano neo-standard (dell'uso medio): formas antes coloquiais hoje aceitas no padrão culto médio"
        ],
        "definicao": {
            "fenomeno": "Na sociolinguística italiana (sistematizada por Gaetano Berruto e Tullio De Mauro), qualquer enunciado se posiciona simultaneamente em quatro eixos de variação (*diatopico, diastratico, diafasico, diamesico*).",
            "causa": "Qual é a diferença entre um **dialetto italiano** (como o napolitano ou o vêneto) e o **italiano regionale**, e o que são **geosinonimi**?",
            "conceito": "Os **dialetti italiani** não são 'corrupções' do italiano, mas **línguas irmãs** nascidas diretamente do latim vulgar em cada região. O **italiano regionale** é o italiano padrão falado com sotaque, entonação e vocabulário locais. Já os **geosinonimi** são palavras do próprio italiano que mudam conforme a região para designar o mesmo objeto (*anguria* no Norte, *cocomero* no Centro, *mellone d'acqua* no Sul para 'melancia')."
        },
        "tecnica": "**Como classificar os eixos da variação sociolinguística (Exames C2):**\n\n1. **Diatopia (Lugar):** Mudança geográfica (*balocco* na Toscana vs *giocattolo*; *adesso* vs *mo'*).\n2. **Diastratia (Sociedade):** Variação ligada ao nível de escolaridade ou grupo social (*italiano popolare*: erros como *se avrei*, *ci ho detto* no lugar de *gli ho detto*).\n3. **Diafasia (Registro e Tema):** Adaptação consciente do mesmo falante à situação (conversa com amigos vs entrevista de emprego).\n4. **Diamesia (Meio):** Diferença entre o texto escrito planejado, a fala espontânea face a face e a comunicação mediada por telas (*italiano digitato*).",
        "teoria": "### Varietà dell'Italiano e Sociolinguistica\n\nA arquitetura do italiano contemporâneo estrutura-se em **quatro dimensões de variação** (com o prefixo grego *dia-* = através de):\n\n| Dimensão | Fator de Variação | Exemplos Práticos |\n|---|---|---|\n| **Variazione Diatopica** | Espaço geográfico | Dialetos, italiano regional e **geosinonimi** (*papà / babbo*, *anguria / cocomero*, *gruccia / stampella*) |\n| **Variazione Diastratica** | Estrato social e instrução | *Italiano colto* vs *italiano popolare* vs *gerghi giovanili* |\n| **Variazione Diafasica** | Situação, interlocutor e tema | Registro *solenne/formale* (*Le porgo distinti saluti*) vs *informale* (*Un caro saluto*) |\n| **Variazione Diamesica** | Meio/Canal físico | *Scritto* (sintaxe hipotática) vs *Parlato* (pausas, dêiticos) vs *Trasmesso* |\n\n#### O *Italiano dell'Uso Medio* (Neo-Standard)\nRefere-se ao italiano falado e escrito cotidiano pelas classes escolarizadas, onde traços antes restritos à oralidade passaram a ser normais: *lui/lei/loro* como sujeito, *gli* unificado para plural (*a loro*), *ci* com o verbo *avere* na fala (*c'ho fame*) e o presente pelo futuro (*Domani parto*).",
        "tabela_visual": make_tabela_visual("Os 4 Eixos da Sociolinguística Italiana", [
            ("Diatopia (Geografia)", "Dialetti, italiano regionale, geosinonimi (anguria / cocomero)"),
            ("Diastratia (Social)", "Italiano colto vs italiano popolare / gerghi"),
            ("Diafasia (Situação)", "Registri (formale / colloquiale) e linguaggi settoriali"),
            ("Diamesia (Canal)", "Scritto pianificato vs Parlato spontaneo vs Digitale")
        ]),
        "observacao_cards": [
            {"italiano": "Anguria (Nord), cocomero (Centro), mellone d'acqua (Sud).", "traducao": "Melancia (no Norte, no Centro e no Sul da Itália).", "artigo": "Diatopia", "genero": "geosinonimi", "motivo": "Geosinonimi são palavras diferentes usadas em regiões distintas da Itália para designar exatamente o mesmo referente."},
            {"italiano": "La variazione diafasica dipende dalla situazione comunicativa.", "traducao": "A variação diafásica depende da situação comunicativa.", "artigo": "Diafasia", "genero": "registro", "motivo": "Um mesmo falante culto muda seu registro conforme fala com um juiz em audiência ou com um amigo no bar."},
            {"italiano": "I dialetti italiani derivano direttamente dal latino volgare.", "traducao": "Os dialetos italianos derivam diretamente do latim vulgar.", "artigo": "Dialetti", "genero": "história linguística", "motivo": "Os dialetos primários (siciliano, vêneto, lombardo, napolitano) são sistemas linguísticos autônomos derivados do latim, e não variantes do toscano."}
        ],
        "exemplos_prc": [
            {"oracao": "In Toscana si dice 'babbo', nel resto d'Italia prevale 'papà'.", "pergunta": "A qual eixo de variação pertence a diferença entre 'babbo' e 'papà'?", "resposta": "Na Toscana diz-se 'babbo'; no resto da Itália prevalece 'papà'.", "conclusao": "Pertence à variação diatópica (geográfica) e constitui um par clássico de geossinônimos."},
            {"oracao": "«Lui mi ha detto che domani non viene» invece di «Egli mi disse che non sarebbe venuto».", "pergunta": "Como a linguística classifica a primeira frase?", "resposta": "«Ele me disse que amanhã não vem».", "conclusao": "É um exemplo típico do 'italiano neo-standard' (ou dell'uso medio), com 'lui' sujeito e presente com valor de futuro."}
        ],
        "armadilhas": [
            {"errado": "I dialetti italiani sono forme corrotte dell'italiano nazionale.", "certo": "I dialetti italiani sono lingue neolatine sorelle del fiorentino, nate dal latino volgare.", "motivo": "Do ponto de vista linguístico, o florentino era originalmente um dialeto entre os outros, que se tornou língua nacional por prestígio literário e histórico."},
            {"errado": "La differenza tra scritto e parlato si chiama variazione diastratica.", "certo": "La differenza tra scritto e parlato si chiama variazione diamesica (dal greco mesos = mezzo).", "motivo": "Diastratica refere-se ao estrato social; Diamesica refere-se ao meio/canal físico (voz vs papel vs tela)."}
        ],
        "ponte": "**Em português:** Assim como no Brasil temos geossinônimos (*mandioca / aipim / macaxeira*), a Itália tem uma riqueza imensa de geossinônimos (*cornetto / brioche*, *marinocche / bruciare la scuola / fare forca*). Os termos técnicos (*diatópico, diastrático, diafásico, diamésico*) são idênticos na linguística em português.",
        "coda": "Mnemônico rápido para os 4 eixos: **TOPos** = lugar (diatópica); **STRATo** = classe social (diastrática); **FASe/fala** = situação/registro (diafásica); **MEio** = canal escrito/falado (diamésica).",
        "exemplos": [
            "L'italiano neo-standard ha accolto nel parlato colto strutture come la frase scissa e la dislocazione.",
            "I linguaggi settoriali (medico, giuridico, informatico) rientrano nell'asse della variazione diafasica.",
            "Il bilinguismo italiano-dialetto con diglossia caratterizza ancora molte aree della penisola."
        ]
    },
    "c2-iv": {
        "alerta": "A era digital criou o 'italiano digitato' (ou e-italiano), marcado por anglismos híbridos (*chattare, loggarsi, spoilerare*), neologismos semânticos e uma nova relação entre escrita e oralidade.",
        "inventario": [
            "Verbos híbridos (inglês + -are): chattare, postare, taggare, bannare, spoilerare, ghostare",
            "Anglismos não adaptados (forestierismi crudi): smart working, lockdown, green pass, feedback, deadline",
            "Equivalentes italianos formais: lavoro agile (smart working), divieto d'accesso (ban), scadenza (deadline)",
            "Italiano digitato: escrita rápida, sincopada, dialógica, que simula a fala em tempo real"
        ],
        "definicao": {
            "fenomeno": "Com as redes sociais, o trabalho remoto e a tecnologia, o italiano contemporâneo absorve dezenas de empréstimos do inglês (*forestierismi*) e cria neologismos morfológicos todos os anos.",
            "causa": "Por que os verbos criados a partir do inglês entram sempre na 1ª conjugação (*-are*: *scaricare, cliccare, formattare, postare*) e como escolher o gênero de substantivos estrangeiros (*la mail vs il file*)?",
            "conceito": "Na morfologia italiana contemporânea, apenas a **1ª conjugação (-are)** e o sufixo incoativo *-izzare* são produtivos para novos verbos. Já o gênero dos empréstimos segue normalmente o **substantivo italiano equivalente subentendido**: *la mail* (porque *la posta elettronica* é feminina), *la chat* (*la conversazione*), *il file* (*il documento*), *il browser* (*il programma*)."
        },
        "tecnica": "**Como lidar com anglismos e neologismos no nível C2:**\n\n1. **Saiba alternar para o equivalente italiano em textos formais:** Em vez de *smart working*, prefira *lavoro agile* em documentos oficiais; em vez de *deadline*, use *scadenza*; em vez de *meeting*, use *riunione*.\n2. **Atenção aos falsos anglismos (pseudoanglicismi):** *Smart working* na Itália significa especificamente 'home office / teletrabalho', uma criação italiana que em inglês nativo seria *remote working*!\n3. **Gênero dos substantivos digitais:** *la mail, la password, la chat, la call, la app* (femininos); *il post, il link, il file, il cloud, il social* (masculinos).",
        "teoria": "### L'Italiano nell'Era Digitale: Neologismi e Anglismi\n\nO linguista Giuseppe Antonelli denomina **e-italiano** a variedade escrita digital que aproxima a escrita da conversa cotidiana, enquanto a **Accademia della Crusca** monitora os neologismos.\n\n#### 1. Tipologia dos Empréstimos (*Prestiti Linguistici*)\n| Tipo de Empréstimo | Mecanismo | Exemplos em Italiano |\n|---|---|---|\n| **Prestito non adattato** | Mantém a grafia original estrangeira | *il computer, il mouse, lo smartphone, il feedback* |\n| **Prestito adattato (Híbrido)** | Raiz estrangeira + morfologia italiana (*-are*) | *cliccare, chattare, postare, taggare, bannare, hackerare* |\n| **Calco semantico** | Palavra italiana ganha novo sentido digital | *navigare* (na web), *scaricare* (download), *salvare* (um arquivo), *profilo* |\n| **Pseudoanglicismo** | Expressão em inglês criada na Itália | *smart working* (trabalho remoto), *mister* (técnico de futebol) |\n\n#### 2. Equivalências para o Registro Culto / Institucional\n- *Deadline* → **la scadenza / il termine ultimo**\n- *Smart working* → **il lavoro agile / il telelavoro**\n- *Fake news* → **le notizie false / la disinformazione (le bufale)**\n- *Question time* → **le interrogazioni a risposta immediata**",
        "tabela_visual": make_tabela_visual("Fenômenos do Italiano Digital (C2)", [
            ("Verbos em -ARE", "Cliccare, postare, taggare, bannare, spoilerare"),
            ("Calcos Semânticos", "Salvare (save), scaricare (download), finestre (windows)"),
            ("Pseudoanglicismos", "Smart working (criação italiana para remote work)"),
            ("Gênero Gramatical", "La mail, la password, la call (f.) | Il file, il link, il post (m.)")
        ]),
        "observacao_cards": [
            {"italiano": "Ti mando una mail con il file in allegato.", "traducao": "Mando-te um e-mail com o arquivo em anexo.", "artigo": "La mail", "genero": "gênero digital", "motivo": "Em italiano diz-se 'la mail' (feminino, por 'la posta/lettera') e 'in allegato' (em anexo)."},
            {"italiano": "Tutti i nuovi verbi digitali entrano nella prima coniugazione (-are).", "traducao": "Todos os novos verbos digitais entram na primeira conjugação (-are).", "artigo": "-ARE", "genero": "morfologia", "motivo": "A 1ª conjugação é a única aberta e produtiva no italiano moderno: postare, linkare, loggarsi."},
            {"italiano": "Il termine «smart working» in Italia è uno pseudoanglicismo.", "traducao": "O termo «smart working» na Itália é um pseudoanglicismo.", "artigo": "Lavoro agile", "genero": "sociolinguística", "motivo": "Na lei italiana o termo oficial é 'lavoro agile', mas a mídia popularizou o pseudoanglicismo 'smart working'."}
        ],
        "exemplos_prc": [
            {"oracao": "Hai già scaricato l'applicazione e salvato la password?", "pergunta": "Por que 'scaricare' e 'salvare' são chamados de calcos semânticos?", "resposta": "Você já baixou o aplicativo e salvou a senha?", "conclusao": "Porque eram verbos italianos antigos ('descarregar carga' e 'salvar vidas') que absorveram os novos significados informáticos do inglês 'to download' e 'to save'."},
            {"oracao": "L'utente è stato bannato dagli amministratori del forum.", "pergunta": "Como se formou o verbo 'bannare'?", "resposta": "O usuário foi banido pelos administradores do fórum.", "conclusao": "É um empréstimo adaptado (híbrido) do inglês 'to ban' com geminação da consoante final e desinência italiana '-are'."}
        ],
        "armadilhas": [
            {"errado": "Ho ricevuto i files e le mails che mi hai mandato.", "certo": "Ho ricevuto i file e le mail che mi hai mandato.", "motivo": "Regra normativa da gramática italiana: substantivos estrangeiros não adaptados são INVARIÁVEIS no plural (i file, le mail, i computer, i film — sem -s!)."},
            {"errado": "Ti invio il mio nuovo password.", "certo": "Ti invio la mia nuova password.", "motivo": "'Password' em italiano é feminino (la password), pois subentende 'la parola chiave / la parola d'ordine'."}
        ],
        "ponte": "**Regra de ouro que difere do português:** Em português escrevemos *os e-mails, os links, os filmes*. Em italiano culto, **empréstimos estrangeiros terminados em consoante NÃO levam -s no plural**: escreve-se *i film, i computer, i link, i file, le mail, i social*!",
        "coda": "Nunca adicione **-s** no plural de palavras estrangeiras dentro de uma frase em italiano (*i film*, *i test*, *le mail*, *i leader*).",
        "exemplos": [
            "La normativa sul lavoro agile disciplina i diritti dei lavoratori da remoto.",
            "Molti linguisti criticano l'abuso dell'itanglese nella pubblica amministrazione.",
            "Prima di chiudere il documento, ricordati di salvare le modifiche nel cloud."
        ]
    },
    "c2-v": {
        "alerta": "O texto argumentativo de nível C2 exige estrutura retórica clássica (Tesi, Argomenti, Antitesi, Confutazione, Conclusione), impessoalidade e domínio absoluto dos articuladores discursivos.",
        "inventario": [
            "Estrutura: Introduzione / Tesi → Argomentazione → Antitesi → Confutazione → Conclusione",
            "Introdutores de tese: Si ritiene che, È opinione diffusa che, La tesi che si intende sostenere è che",
            "Concessão e Refutação: Sebbene alcuni sostengano che... va tuttavia rilevato che...",
            "Impessoalidade acadêmica: Si osserva come, Risulta evidente che, Appare opportuno sottolineare"
        ],
        "definicao": {
            "fenomeno": "Nos exames CELI 5 / CILS C2 e em ensaios universitários, não basta opinar com *Io penso che*: é necessário construir uma arquitetura dialética que apresente a tese, antecipe a objeção (*antitesi*) e a desmonte com dados e lógica (*confutazione*).",
            "causa": "Qual é a diferença estrutural entre uma redação escolar B2 e um ensaio argumentativo de nível C2?",
            "conceito": "O ensaio C2 utiliza **despersonalização sintática** (*si evidenzia, va sottolineato, non si può prescindere da*), **coesão por encapsuladores anafóricos** (*tale fenomeno, suddetta problematica, siffatta ipotesi*) e o movimento dialético **Concessão + Refutação** (*Pur riconoscendo la validità di..., non si può ignorare che...*)."
        },
        "tecnica": "**Roteiro infalível para redigir um Testo Argomentativo C2:**\n\n1. **Inquadramento del problema (Introdução):** Contextualize o tema de forma impessoal (*Negli ultimi decenni il dibattito intorno a... ha assunto una rilevanza centrale*).\n2. **Formulazione della Tesi e Argomenti:** Apresente sua posição sustentada por causas e evidências (*In primo luogo...; A ciò si aggiunga che...*).\n3. **Antitesi e Confutazione (O coração do C2):** Antecipe o argumento contrário no Congiuntivo (*Sebbene i detrattori sostengano che...*) e refute-o imediatamente (*...tale obiezione trascura tuttavia il fatto che...*).\n4. **Sintesi e Conclusione:** Feche retomando a tese sob uma perspectiva mais ampla (*Alla luce di quanto esposto, appare evidente come...*).",
        "teoria": "### Analisi e Produzione del Testo Argomentativo (C2)\n\nO **testo argomentativo** visa persuadir o leitor da validade de uma **tesi** por meio de raciocínio lógico, provas (*dati di fatto, esempi, citazioni d'autorità*) e refutação das posições contrárias.\n\n#### 1. Arquitetura Dialética do Ensaio\n| Etapa | Função Discursiva | Fórmulas de Nível C2 |\n|---|---|---|\n| **1. Introduzione** | Apresentar o tema e sua relevância | *Il tema relativo a... si colloca al centro del dibattito odierno.* |\n| **2. Tesi e Argomenti** | Defender a posição principal | *Si intende qui sostenere che... / In primo luogo, va rilevato come...* |\n| **3. Antitesi** | Dar voz à objeção adversária | *Da più parti si obietta che... / Non manca chi ritiene che (+ cong.)* |\n| **4. Confutazione** | Desconstruir a antítese | *Pur comprendendo tali timori, risulta tuttavia innegabile che...* |\n| **5. Conclusione** | Síntese final e abertura | *Alla luce delle considerazioni svolte, si può dunque concludere che...* |\n\n#### 2. Encapsuladores Anafóricos (*Incapsulatori Anaforici*)\nPara evitar repetir a mesma palavra, retome um parágrafo inteiro com sintagmas nominais demonstrativos: *tale fenomeno, questa dinamica, la suddetta questione, un simile scenario*.",
        "tabela_visual": make_tabela_visual("Arquitetura do Ensaio Argumentativo C2", [
            ("1. Tesi & Argomenti", "Si intende sostenere che... / In primo luogo va rilevato..."),
            ("2. Antitesi (Concessão)", "Non manca chi obietta che... / Sebbene si sostenga che..."),
            ("3. Confutazione", "Tale obiezione trascura tuttavia il fatto che..."),
            ("4. Conclusione", "Alla luce di quanto esposto, appare evidente come...")
        ]),
        "observacao_cards": [
            {"italiano": "Alla luce di quanto esposto, appare evidente la necessità di una riforma.", "traducao": "À luz do que foi exposto, mostra-se evidente a necessidade de uma reforma.", "artigo": "Conclusão", "genero": "fórmula C2", "motivo": "Fórmula clássica de fechamento argumentativo que retoma toda a demonstração anterior."},
            {"italiano": "Pur riconoscendo i costi del progetto, non si può ignorare il suo valore sociale.", "traducao": "Mesmo reconhecendo os custos do projeto, não se pode ignorar seu valor social.", "artigo": "Confutazione", "genero": "dialética", "motivo": "Une a concessão ('Pur riconoscendo' = antítese) à refutação ('non si può ignorare' = defesa da tese)."},
            {"italiano": "Tale fenomeno merita un'analisi approfondita.", "traducao": "Tal fenômeno merece uma análise aprofundada.", "artigo": "Incapsulatore", "genero": "coesão textual", "motivo": "'Tale fenomeno' funciona como encapsulador anafórico, resumindo toda a ideia explicada no período anterior."}
        ],
        "exemplos_prc": [
            {"oracao": "Sebbene alcuni critici ritengano che l'intelligenza artificiale riduca l'occupazione, va tuttavia sottolineato come essa crei nuove figure professionali.", "pergunta": "Como estão articuladas a Antítese e a Confutação neste período?", "resposta": "Embora alguns críticos considerem que a IA reduza o emprego, cabe contudo ressaltar como ela cria novos perfis profissionais.", "conclusao": "A oração concessiva ('Sebbene... ritengano') introduz a antítese no subjuntivo; a principal ('va tuttavia sottolineato') realiza a refutação com elegância impessoal."},
            {"oracao": "Non si può prescindere da una rigorosa verifica delle fonti.", "pergunta": "O que significa o verbo 'prescindere da'?", "resposta": "Não se pode prescindir de (abrir mão de) uma rigorosa verificação das fontes.", "conclusao": "'Non si può prescindere da' (= é indispensável considerar) é uma das estruturas impessoais mais valorizadas em textos acadêmicos C2."}
        ],
        "armadilhas": [
            {"errado": "Secondo me io penso che questo problema è molto grande.", "certo": "Si ritiene che tale problematica rivesta un'importanza cruciale.", "motivo": "Em primeiro lugar, 'secondo me io penso' é pleonasmo vicioso; além disso, 'penso che' exige Congiuntivo ('sia'), e no registro C2 prefere-se a forma impessoal."},
            {"errado": "In conclusione, per concludere finalmente, dico che...", "certo": "In definitiva, alla luce delle considerazioni svolte, si può affermare che...", "motivo": "Em italiano, 'finalmente' significa 'até que enfim!' (alívio), e não 'por fim / finalmente' para encerrar uma enumeração (use 'infine' ou 'in conclusione')."}
        ],
        "ponte": "**Atenção ao falso cognato clássico em redações:** Em português usamos *Finalmente* para introduzir o último argumento. Em italiano, *Finalmente!* significa *Até que enfim!*. Para enumerar o último ponto de um texto, use sempre **Infine**, **Da ultimo** ou **In conclusione**!",
        "coda": "Checklist C2: 1) Tese impessoal; 2) *Sebbene... tuttavia...* (antítese + refutação); 3) Encapsulador (*tale fenomeno*); 4) *Infine / Alla luce di quanto esposto* no fechamento.",
        "exemplos": [
            "Non si può prescindere dal contesto storico nell'analisi di un'opera letteraria.",
            "A sostegno di tale tesi, basti citare i dati pubblicati dall'ISTAT.",
            "In definitiva, i benefici a lungo termine superano ampiamente le criticità iniziali."
        ]
    }
}

# Correções dos 84 observacao_cards de a1-lez3 a a1-lez30:
# Mapeia cada frase italiana para (traducao_pt_real, artigo_badge, genero_label, motivo_explicativo_pt)
A1_CARDS_FIX = {
    "Il libro del professore è sulla scrivania.": (
        "O livro do professor está sobre a escrivaninha.",
        "del / sulla", "preposizione articolata",
        "di + il = del (posse: do professor) | su + la = sulla (localização: sobre a escrivaninha)."
    ),
    "Vengo dall'università alle tre.": (
        "Venho da universidade às três horas.",
        "dall' / alle", "preposizione articolata",
        "da + l' = dall' (origem antes de vogal) | a + le = alle (horário plural)."
    ),
    "Parlo con gli studenti del corso.": (
        "Falo com os estudantes do curso.",
        "con gli / del", "preposição",
        "'con' moderno não se contrai com 'gli' (con gli studenti), enquanto 'di + il' funde-se em 'del'."
    ),
    "Ieri ho mangiato la pasta e ho bevuto il vino.": (
        "Ontem comi a massa e bebi o vinho.",
        "avere + -ato/-uto", "passato prossimo",
        "Verbos transitivos (mangiare, bere) usam o auxiliar AVERE e o particípio permanece invariável em -o."
    ),
    "Maria è andata a Roma e è tornata stanotte.": (
        "Maria foi a Roma e voltou esta noite.",
        "essere + -a", "passato prossimo",
        "Verbos de movimento/direção (andare, tornare) usam ESSERE e o particípio concorda com o sujeito feminino (andata, tornata)."
    ),
    "I ragazzi sono partiti presto; le ragazze sono partite tardi.": (
        "Os rapazes partiram cedo; as moças partiram tarde.",
        "partiti / partite", "concordância",
        "Com o auxiliar ESSERE, o particípio concorda em gênero e número: masculino plural (-i) e feminino plural (-e)."
    ),
    "Sei mai stato a Venezia? — Sì, ci sono stato l'anno scorso.": (
        "Você já esteve em Veneza? — Sim, estive lá no ano passado.",
        "ci = lá", "particella ci",
        "A partícula locativa 'ci' substitui o lugar já mencionado ('a Venezia' = lá/ali) antes do verbo."
    ),
    "Ci vuole coraggio per parlare in pubblico.": (
        "É preciso coragem para falar em público.",
        "ci vuole", "expressão com ci",
        "'Ci vuole' (+ singular) e 'ci vogliono' (+ plural) significam 'é necessário / são necessários'."
    ),
    "Non ci credo! È impossibile.": (
        "Não acredito nisso! É impossível.",
        "ci = nisso", "ci pronominal",
        "Com verbos como credere, pensare e contare, 'ci' significa 'em tal coisa / nisso' (a ciò)."
    ),
    "Domani andrò a Roma e vedrò il Colosseo.": (
        "Amanhã irei a Roma e verei o Coliseu.",
        "andrò / vedrò", "futuro irregular",
        "Andare e vedere perdem a vogal temática no futuro: andr-ò e vedr-ò."
    ),
    "Quando arriverò, ti chiamerò subito.": (
        "Quando eu chegar, te ligarei imediatamente.",
        "quando + futuro", "regra italiana",
        "Diferente do português (que usa futuro do subjuntivo 'quando eu chegar'), o italiano usa dois futuros simples!"
    ),
    "Avrà almeno quarant'anni, quel signore.": (
        "Deve ter pelo menos quarenta anos, aquele senhor.",
        "futuro epistêmico", "suposição",
        "O futuro simples também expressa suposição ou probabilidade no presente ('deve ter / terá')."
    ),
    "Il mio zaino è rosso; la mia borsa è nera.": (
        "A minha mochila é vermelha; a minha bolsa é preta.",
        "il mio / la mia", "possessivos",
        "O possessivo italiano concorda com a coisa possuída (zaino masc. → il mio; borsa fem. → la mia) e leva artigo."
    ),
    "Mia sorella studia medicina; mio fratello lavora.": (
        "Minha irmã estuda medicina; meu irmão trabalha.",
        "sem artigo", "parentesco singular",
        "Com nomes de parentes próximos no singular (madre, padre, fratello, sorella), omite-se o artigo antes do possessivo."
    ),
    "I loro genitori vivono a Milano.": (
        "Os pais deles moram em Milão.",
        "i loro", "invariável",
        "O possessivo 'loro' (deles/delas) é invariável e exige SEMPRE o artigo, inclusive com parentes no singular (il loro padre)."
    ),
    "Conosci Marco? — Sì, lo conosco bene.": (
        "Você conhece o Marco? — Sim, eu o conheço bem.",
        "lo", "pronome direto",
        "'Lo' substitui o objeto direto masculino singular (Marco) e posiciona-se antes do verbo conjugado."
    ),
    "Hai comprato le mele? — Sì, le ho comprate.": (
        "Você comprou as maçãs? — Sim, eu as comprei.",
        "le ho comprate", "concordância",
        "Quando o pronome direto (lo, la, li, le) vem antes de 'avere', o particípio passado concorda com ele (le → comprate)."
    ),
    "Devo chiamare Maria. — Devo chiamarla.": (
        "Preciso ligar para a Maria. — Preciso ligar para ela.",
        "chiamarla", "ênclise no infinitivo",
        "Com verbos no infinitivo, o pronome pode juntar-se ao final do verbo, que perde o '-e' final (chiamare + la = chiamarla)."
    ),
    "Quando ero piccolo, andavo al mare ogni estate.": (
        "Quando eu era pequeno, ia ao mar todo verão.",
        "ero / andavo", "imperfetto",
        "O Imperfetto expressa estados contínuos no passado ('ero piccolo') e ações habituais repetidas ('andavo ogni estate')."
    ),
    "Dormivo quando il telefono ha squillato.": (
        "Eu estava dormindo quando o telefone tocou.",
        "imperf. + p.pross.", "ação interrompida",
        "A ação longa em andamento fica no Imperfetto (dormivo) e o evento pontual que a interrompe fica no Passato Prossimo (ha squillato)."
    ),
    "Era una bella giornata: il sole splendeva e la gente passeggiava.": (
        "Era um belo dia: o sol brilhava e as pessoas passeavam.",
        "descrição", "cenário passado",
        "Para descrever o pano de fundo, o clima e ações simultâneas no passado, usa-se sempre o Imperfetto."
    ),
    "Ho scritto a Maria. — Le ho scritto una lettera.": (
        "Escrevi para a Maria. — Escrevi-lhe uma carta.",
        "le (a ela)", "pronome indireto",
        "O pronome indireto feminino singular ('a lei') é 'le', e nunca faz concordância com o particípio passado."
    ),
    "Mi piace la pizza. Mi piacciono i dolci.": (
        "Eu gosto de pizza. Eu gosto de doces.",
        "piace / piacciono", "verbo piacere",
        "Em italiano, a coisa apreciada é o sujeito do verbo: singular → piace (la pizza); plural → piacciono (i dolci)."
    ),
    "Gli ho detto la verità, ma non mi ha risposto.": (
        "Eu disse a verdade a ele, mas ele não me respondeu.",
        "gli / mi", "indireto",
        "'Gli' significa 'a ele' (e no italiano moderno também 'a eles/elas'); 'mi' significa 'a mim'."
    ),
    "Puoi prestarmi il libro? — Te lo presto volentieri.": (
        "Pode me emprestar o livro? — Eu o empresto a você com prazer.",
        "te lo", "pronome combinado",
        "Antes de lo/la/li/le/ne, os pronomes indiretos mi, ti, ci, vi mudam o -i para -e: ti + lo = te lo."
    ),
    "Gli ho mandato la lettera. — Gliel'ho mandata.": (
        "Mandei a carta para ele. — Eu a mandei para ele.",
        "gliel'ho mandata", "gli + la",
        "'Gli' e 'le' fundem-se em 'glie-' antes do pronome direto: gli + la = gliela (gliel' antes de vogal), com concordância (mandata)."
    ),
    "Vuole spiegarci la regola? — Ce la spiega?": (
        "Quer nos explicar a regra? — Explica-a para nós?",
        "ce la", "ci + la",
        "O pronome indireto 'ci' (a nós) transforma-se em 'ce' antes do pronome direto 'la' (la regola): ce la."
    ),
    "Mi sono svegliato tardi e mi sono vestito in fretta.": (
        "Acordei tarde e me vesti depressa.",
        "mi sono + -o", "verbo reflexivo",
        "Todos os verbos reflexivos usam obrigatoriamente o auxiliar ESSERE nos tempos compostos, concordando com o sujeito."
    ),
    "Come ti chiami? — Mi chiamo Marco.": (
        "Como você se chama? — Eu me chamo Marco.",
        "ti / mi", "reflexivo presente",
        "No presente, os pronomes reflexivos (mi, ti, si, ci, vi, si) antecedem o verbo conjugado."
    ),
    "Marco e Maria si sono conosciuti a Roma.": (
        "Marco e Maria se conheceram em Roma.",
        "si recíproco", "ação mútua",
        "O reflexivo recíproco no plural ('si sono conosciuti') indica ação mútua ('um ao outro')."
    ),
    "Vorrei prenotare un tavolo per due persone.": (
        "Eu gostaria de reservar uma mesa para duas pessoas.",
        "vorrei", "condizionale cortês",
        "O Condizionale Presente de volere ('vorrei' = eu gostaria) é a forma essencial de cortesia para pedidos em italiano."
    ),
    "Se avessi più tempo, studierei l'italiano ogni giorno.": (
        "Se eu tivesse mais tempo, estudaria italiano todos os dias.",
        "studierei", "hipótese",
        "Na consequência de uma hipótese presente (Se + Congiuntivo Imperfetto), usa-se o Condizionale Semplice (studierei)."
    ),
    "Avrei dovuto studiare di più per l'esame.": (
        "Eu deveria ter estudado mais para o exame.",
        "avrei dovuto", "condizionale composto",
        "O Condizionale Composto expressa arrependimento no passado ou algo que deveria ter ocorrido mas não ocorreu."
    ),
    "La ragazza che ho incontrato ieri si chiama Sofia.": (
        "A garota que encontrei ontem se chama Sofia.",
        "che", "pronome relativo",
        "'Che' é invariável e funciona apenas como sujeito ou objeto direto (sem preposição antes dele)."
    ),
    "Il paese in cui sono nato è piccolo.": (
        "A cidadezinha em que nasci é pequena.",
        "in cui", "prep. + cui",
        "Quando o verbo pede preposição (nascere in, parlare di, contare su), usa-se obrigatoriamente 'preposição + cui'."
    ),
    "Chi non risica, non rosica.": (
        "Quem não arrisca, não petisca.",
        "chi", "relativo duplo",
        "'Chi' significa 'aquele que / quem' e leva sempre o verbo na 3ª pessoa do singular."
    ),
    "Roma è più grande di Firenze.": (
        "Roma é maior do que Florença.",
        "più... di", "comparativo com di",
        "Quando comparamos uma qualidade entre dois substantivos ou pronomes (Roma vs Firenze), usamos 'di'."
    ),
    "È più facile studiare che lavorare.": (
        "É mais fácil estudar do que trabalhar.",
        "più... che", "comparativo com che",
        "Quando comparamos dois verbos no infinitivo, dois adjetivos ou dois complementos com preposição, usamos 'che'."
    ),
    "Questo è il miglior ristorante della città.": (
        "Este é o melhor restaurante da cidade.",
        "il migliore", "superlativo irregular",
        "'Migliore' (melhor) e 'peggiore' (pior) são as formas comparativas/superlativas sintéticas de 'buono' e 'cattivo'."
    ),
    "Garibaldi nacque a Nizza nel 1807 e morì a Caprera nel 1882.": (
        "Garibaldi nasceu em Nice em 1807 e morreu em Caprera em 1882.",
        "nacque / morì", "passato remoto",
        "O Passato Remoto indica eventos históricos ou totalmente concluídos no passado distante, sem vínculo com o presente."
    ),
    "Dante scrisse la Divina Commedia tra il 1308 e il 1320.": (
        "Dante escreveu a Divina Comédia entre 1308 e 1320.",
        "scrisse", "raiz irregular",
        "Muitos verbos em -ere têm Passato Remoto irregular na 1ª, 3ª sg. e 3ª pl. (scrissi, scrivesti, scrisse, scrivemmo, scriveste, scrissero)."
    ),
    "Quando vidi Marco, capii subito che c'era un problema.": (
        "Quando vi o Marco, entendi logo que havia um problema.",
        "vidi / capii", "narrativa literária",
        "Na narrativa literária e histórica, o Passato Remoto marca a sequência de eventos pontuais (vidi, capii)."
    ),
    "Quando sono arrivato al cinema, il film era già iniziato.": (
        "Quando cheguei ao cinema, o filme já tinha começado.",
        "era già iniziato", "trapassato prossimo",
        "O Trapassato Prossimo (imperfetto do auxiliar + particípio) indica uma ação ocorrida ANTES de outra ação no passado."
    ),
    "Non avevo mai mangiato il sushi prima di quel giorno.": (
        "Eu nunca tinha comido sushi antes daquele dia.",
        "avevo mangiato", "anterioridade",
        "Marca uma experiência que nunca havia acontecido até aquele ponto específico do passado."
    ),
    "Siamo usciti dopo che aveva finito di piovere.": (
        "Saímos depois que tinha parado de chover.",
        "dopo che + trapass.", "sequência no passado",
        "A chuva parou primeiro (aveva finito) e nós saímos depois (siamo usciti)."
    ),
    "Abito a Firenze ma lavoro in Toscana.": (
        "Moro em Florença, mas trabalho na Toscana.",
        "a città / in regione", "preposições de lugar",
        "Regra fundamental geográfica: usa-se 'A' para cidades (a Firenze, a Roma) e 'IN' para regiões, países e continentes (in Toscana, in Italia)."
    ),
    "Studio l'italiano da tre anni.": (
        "Estudo italiano há três anos.",
        "da + tempo", "duração contínua",
        "Para uma ação que começou no passado e continua no presente, o italiano usa 'Presente + da' (há três anos)."
    ),
    "Ho comprato un regalo per mia madre.": (
        "Comprei um presente para a minha mãe.",
        "per", "destinatário / fim",
        "A preposição 'per' indica o beneficiário/destinatário ('para minha mãe') ou finalidade."
    ),
    "Credevo che tu fossi stanco. / Credo che tu sia stanco.": (
        "Eu achava que você estivesse cansado. / Acho que você está cansado.",
        "fossi / sia", "concordância dos tempos",
        "Verbo principal no presente (Credo) pede Congiuntivo Presente (sia); no passado (Credevo), pede Congiuntivo Imperfetto (fossi)."
    ),
    "Quando sarò a Roma, ti chiamerò.": (
        "Quando eu estiver em Roma, te ligarei.",
        "sarò → chiamerò", "duplo futuro",
        "Em orações temporais futuras com 'quando' ou 'appena', o italiano usa o Futuro Semplice em ambas as orações."
    ),
    "Dopo che aveva finito il lavoro, Marco è uscito.": (
        "Depois que tinha terminado o trabalho, Marco saiu.",
        "anterioridade", "consecutio temporum",
        "O Trapassato Prossimo ('aveva finito') marca com clareza a ação concluída antes da principal ('è uscito')."
    ),
    "Se hai fame, mangia qualcosa.": (
        "Se você está com fome, coma alguma coisa.",
        "Tipo 1 (Real)", "período hipotético",
        "Hipótese real/provável (Tipo 1): Se + Presente (ou Futuro) seguido de Presente, Futuro ou Imperativo."
    ),
    "Se avessi più soldi, viaggierei di più.": (
        "Se eu tivesse mais dinheiro, viajaria mais.",
        "Tipo 2 (Possível)", "hipótese presente",
        "Hipótese pouco provável ou irreal no presente (Tipo 2): Se + Congiuntivo Imperfetto (avessi) → Condizionale Semplice (viaggierei)."
    ),
    "Se avessi studiato di più, avrei superato l'esame.": (
        "Se eu tivesse estudado mais, teria passado no exame.",
        "Tipo 3 (Impossível)", "hipótese passada",
        "Hipótese irreal no passado (Tipo 3): Se + Congiuntivo Trapassato (avessi studiato) → Condizionale Composto (avrei superato)."
    ),
    "Studiando ogni giorno, ho imparato l'italiano in un anno.": (
        "Estudando todos os dias, aprendi italiano em um ano.",
        "gerúndio modal", "modo / meio",
        "O Gerundio Semplice ('studiando') indica o modo ou meio pelo qual a ação principal foi alcançada."
    ),
    "Stavo dormendo quando è suonato il telefono.": (
        "Eu estava dormindo quando o telefone tocou.",
        "stare + gerúndio", "forma progressiva",
        "'Stare + gerúndio' enfatiza uma ação exata em curso no momento em que outro evento acontece."
    ),
    "Avendo finito il lavoro, Marco è uscito.": (
        "Tendo terminado o trabalho, Marco saiu.",
        "gerúndio composto", "causa / tempo anterior",
        "O Gerundio Composto ('avendo finito') expressa uma ação concluída antes da oração principal."
    ),
    "La torta è stata mangiata dai bambini.": (
        "O bolo foi comido pelas crianças.",
        "è stata mangiata", "voz passiva",
        "A voz passiva forma-se com ESSERE (conjugado no tempo correspondente) + particípio concordado + DA (agente da passiva)."
    ),
    "In Italia si parla italiano.": (
        "Na Itália fala-se italiano.",
        "si passivante", "passiva impessoal",
        "'Si + verbo na 3ª pessoa' funciona como passiva impessoal (com objeto plural, o verbo vai ao plural: In Italia si mangiano gli spaghetti)."
    ),
    "La legge verrà approvata domani.": (
        "A lei será aprovada amanhã.",
        "venire + part.", "passiva dinâmica",
        "Nos tempos simples, o auxiliar 'venire' pode substituir 'essere' na passiva para destacar o processo da ação."
    ),
    "So parlare italiano ma non so suonare il pianoforte.": (
        "Sei falar italiano, mas não sei tocar piano.",
        "sapere + inf.", "habilidade aprendida",
        "Para habilidades adquiridas com estudo ou prática (nadar, dirigir, falar línguas), usa-se 'sapere + infinitivo', e não 'potere'."
    ),
    "Non sono potuto andare alla festa.": (
        "Não pude ir à festa.",
        "sono potuto andare", "auxiliar dos modais",
        "Nos tempos compostos, o verbo modal (potere, dovere, volere) adota o auxiliar do infinitivo que o segue (andare pede essere → sono potuto andare)."
    ),
    "Dovresti studiare di più.": (
        "Você deveria estudar mais.",
        "dovresti", "conselho com modal",
        "O verbo modal 'dovere' no Condizionale ('dovresti') suaviza a obrigação, transformando-a em conselho."
    ),
    "Hai dei fratelli? — Sì, ne ho due.": (
        "Você tem irmãos? — Sim, tenho dois (deles).",
        "ne partitivo", "quantidade",
        "Quando indicamos uma quantidade parcial (uno, due, molti, alcuni, nessuno) sem repetir o substantivo, 'ne' é obrigatório em italiano."
    ),
    "Ce ne sono ancora molti da leggere.": (
        "Ainda há muitos (deles) para ler.",
        "ce ne sono", "ci + ne",
        "Na expressão existencial 'ci sono' combinada com o partitivo 'ne', 'ci' transforma-se em 'ce': ce ne sono."
    ),
    "Gliene ho parlato ieri.": (
        "Falei com ele/ela sobre isso ontem.",
        "gliene", "gli/le + ne",
        "'Gli' ou 'le' combinados com 'ne' (sobre isso / disso) formam uma única palavra: gliene."
    ),
    "Luca ha detto: 'Parto domani.' → Luca ha detto che sarebbe partito il giorno dopo.": (
        "Luca disse: 'Parto amanhã.' → Luca disse que partiria no dia seguinte.",
        "sarebbe partito", "discurso indireto",
        "No discurso indireto no passado, a ação posterior expressa-se com o Condizionale Composto e 'domani' vira 'il giorno dopo'."
    ),
    "La prof ha chiesto: 'Avete studiato?' → ha chiesto se avevamo studiato.": (
        "A professora perguntou: 'Vocês estudaram?' → perguntou se tínhamos estudado.",
        "se + trapassato", "pergunta indireta",
        "Perguntas de sim/não no discurso indireto são introduzidas por 'se', e o Passato Prossimo recua para o Trapassato Prossimo."
    ),
    "Mi ha detto di aspettare.": (
        "Ele me disse para esperar.",
        "di + infinitivo", "imperativo indireto",
        "Um pedido ou ordem no imperativo ('Aspetta!') converte-se em 'di + infinitivo' no discurso indireto."
    ),
    "Sono le otto e un quarto di mattina.": (
        "São oito e quinze da manhã.",
        "sono le...", "horas",
        "Todas as horas usam 'sono le...' no plural, exceto uma hora/meio-dia/meia-noite (è l'una, è mezzogiorno, è mezzanotte)."
    ),
    "Il corso inizia il primo settembre e finisce il trenta giugno.": (
        "O curso começa em primeiro de setembro e termina em trinta de junho.",
        "il primo / il trenta", "datas do mês",
        "Nas datas em italiano, apenas o dia 1º usa numeral ordinal ('il primo'); todos os demais usam numeral cardinal ('il due', 'il trenta')."
    ),
    "Sono nato il ventitrè novembre millenovecentonovantadue.": (
        "Nasci em vinte e três de novembro de mil novecentos e noventa e dois.",
        "números compostos", "grafia contínua",
        "Em italiano, os números escrevem-se em uma única palavra contínua e 'tre' no fim leva acento agudo/grave (ventitré)."
    ),
    "Ho qualche domanda da fare.": (
        "Tenho algumas perguntas para fazer.",
        "qualche + singular", "indefinido",
        "Regra de ouro: 'qualche' tem sentido plural ('alguns/algumas'), mas é SEMPRE seguido por substantivo e verbo no SINGULAR!"
    ),
    "Non è venuto nessuno alla festa.": (
        "Não veio ninguém à festa.",
        "non... nessuno", "dupla negação",
        "Quando 'nessuno', 'niente' ou 'nulla' vêm DEPOIS do verbo, a partícula 'non' antes do verbo é obrigatória."
    ),
    "Tutti i giorni studio un'ora d'italiano.": (
        "Todos os dias estudo uma hora de italiano.",
        "tutti i / ogni", "totalidade",
        "'Tutti' exige o artigo plural ('tutti i giorni'), enquanto 'ogni' é invariável e seguido de singular sem artigo ('ogni giorno')."
    ),
    "Studio italiano perché voglio lavorare in Italia.": (
        "Estudo italiano porque quero trabalhar na Itália.",
        "perché + ind.", "causal",
        "Quando 'perché' significa 'porque / já que' (causa), usa-se o Indicativo; quando significa 'para que' (finalidade), usa-se o Congiuntivo."
    ),
    "Sebbene sia stanco, continuo a lavorare.": (
        "Embora eu esteja cansado, continuo trabalhando.",
        "sebbene + cong.", "concessiva",
        "As conjunções concessivas 'sebbene', 'benché', 'nonostante' e 'malgrado' exigem obrigatoriamente o Congiuntivo."
    ),
    "Appena arriverò a casa, ti chiamerò.": (
        "Assim que eu chegar em casa, te ligarei.",
        "appena + futuro", "temporal futura",
        "Conjunções temporais como 'appena' e 'quando' referindo-se ao futuro usam o Futuro Semplice em italiano."
    ),
    "Parla italiano perfettamente ma scrive lentamente.": (
        "Fala italiano perfeitamente, mas escreve lentamente.",
        "-mente", "advérbios de modo",
        "Os advérbios em '-mente' formam-se a partir do feminino singular do adjetivo (perfetta → perfettamente; lenta → lentamente)."
    ),
    "Non sono mai stato a Tokyo.": (
        "Eu nunca estive em Tóquio.",
        "non... mai", "advérbio de tempo",
        "Nos tempos compostos, advérbios curtos de tempo como 'mai', 'già', 'sempre' e 'ancora' ficam normalmente entre o auxiliar e o particípio."
    ),
    "Ho già mangiato, ma ho ancora fame.": (
        "Já comi, mas ainda estou com fome.",
        "già / ancora", "contraste temporal",
        "'Già' indica ação já realizada; 'ancora' indica continuidade de um estado ('ainda')."
    ),
    "Se avessi studiato di più, sarei riuscito nell'esame.": (
        "Se eu tivesse estudado mais, teria tido êxito no exame.",
        "revisão Tipo 3", "período hipotético",
        "Síntese do Período Hipotético do Tipo 3: Se + Congiuntivo Trapassato → Condizionale Composto."
    ),
    "Gliel'ho già mandata ieri.": (
        "Já a enviei para ele/ela ontem.",
        "gliel'ho mandata", "síntese pronominal",
        "Combina pronome indireto (gli/le → glie-) + pronome direto (la → l') + advérbio (già) + concordância do particípio (mandata)."
    ),
    "Stavo leggendo quando è arrivato Marco.": (
        "Eu estava lendo quando o Marco chegou.",
        "progressivo + passato", "síntese verbal",
        "Contrasta a ação em curso no passado (stavo leggendo) com o evento pontual que a interrompe (è arrivato)."
    )
}

def translate_it_explanation_to_pt(exp, ex, u_titulo):
    """Traduz explicações que estavam puramente em italiano para português didático, preservando os termos italianos em destaque."""
    if not exp or not exp.strip():
        correta = ex.get("resposta")
        if isinstance(correta, int) and ex.get("opcoes") and 0 <= correta < len(ex["opcoes"]):
            correta_str = ex["opcoes"][correta]
        else:
            correta_str = str(correta or "")
        return f"A resposta correta é «{correta_str}», conforme a regra estudada em {u_titulo}."

    # Substituições sistemáticas de termos metalinguísticos italianos para português didático
    subs = [
        ("L'aggettivo concorda con il sostantivo:", "O adjetivo concorda em gênero e número com o substantivo:"),
        ("L'aggettivo concorda:", "O adjetivo concorda em gênero e número:"),
        ("Accordo aggettivo:", "Concordância do adjetivo:"),
        ("Aggettivi in -e (triste, veloce, lente) sono invariabili nel genere.", "Adjetivos terminados em -e (triste, veloce) servem para masculino e feminino no singular (plural em -i)."),
        ("Aggettivi in -o/-a:", "Adjetivos de 4 formas (-o/-a/-i/-e):"),
        ("Terza persona plurale:", "Conjugação na 3ª pessoa do plural (loro):"),
        ("Si usa A per luogo.", "Usa-se a preposição 'a' para indicar destino ou permanência em casa/cidade."),
        ("Si usa CI per luogo.", "Usa-se a partícula 'ci' para indicar permanência em um lugar ('estar lá')."),
        ("Si usa CI per movimento verso luogo.", "Usa-se a partícula 'ci' para indicar movimento em direção a um lugar já mencionado ('ir para lá')."),
        ("Aggettivo possessivo con articolo:", "Adjetivo possessivo precedido de artigo definido:"),
        ("Pronomi diretti dopo verbi.", "Posição dos pronomes de objeto direto em relação ao verbo."),
        ("Pronomi indiretti atoni:", "Pronomes de objeto indireto átonos:"),
        ("Pronome formale Le (signorina/signor).", "Pronome indireto formal 'Le' (ao senhor / à senhora)."),
        ("a/da/su/di/in + articolo formano contrazioni.", "As preposições di, a, da, in, su fundem-se obrigatoriamente com o artigo definido (preposizioni articolate)."),
        ("Ricevere DA qualcuno. Mandare/dare A qualcuno.", "Receber DE (da) alguém; enviar/dar A (a) alguém."),
        ("Con: descrizione fisica. Di: materia/possesso. In: nazione/stagione/mezzo. A: città.", "Uso das preposições: CON (característica física), DI (matéria/posse), IN (país/estação/meio de transporte), A (cidade)."),
        ("Preposizioni chiave:", "Preposições-chave nesta frase:"),
        ("In estate/inverno/primavera/autunno (senza articolo).", "Com as estações do ano usa-se 'in' sem artigo (in estate, in inverno)."),
        ("In Spagna/Germania (nazioni senza articolo).", "Com nomes de países usa-se a preposição 'in' (in Spagna, in Germania)."),
        ("Per + infinito (scopo).", "Usa-se 'per + infinitivo' para expressar finalidade/objetivo."),
        ("Lettura del dialogo: pronomi indiretti, verbo piacere e lessico del negozio.", "Compreensão do diálogo: observe o uso dos pronomes indiretos, do verbo 'piacere' e do vocabulário de compras."),
        ("Verbi come piacere: il soggetto è la cosa, la persona è complemento indiretto.", "Com o verbo 'piacere', a coisa apreciada é o sujeito gramatical e a pessoa é o complemento indireto (mi, ti, gli, le)."),
        ("Quando si cerca qualcosa di ipotetico/non ancora trovato → congiuntivo PRESENTE:", "Quando se procura algo hipotético ou ainda não encontrado, usa-se o Congiuntivo Presente:"),
        ("Se fosse passato irreale → congiuntivo imperfetto.", "Se estivesse no passado ou fosse irreal, usaríamos o Congiuntivo Imperfetto."),
        ("Entrambe corrette!", "Ambas estão corretas!"),
        ("azione anteriore rispetto alla principale", "ação anterior em relação à oração principal"),
        ("azione simultanea alla principale presente", "ação simultânea à oração principal no presente"),
        ("azione simultanea alla principale passata", "ação simultânea à oração principal no passado"),
        ("Non si usa", "Não se usa"),
        ("per azioni passate remote", "para ações passadas anteriores"),
        ("Entrambi i tempi composti.", "Ambos os verbos ficam nos tempos compostos."),
        ("Apodosi del tipo 3 → condizionale composto:", "Consequência (apódose) do Período Hipotético Tipo 3 → Condizionale Composto:"),
        ("La protasi è già al trapassato", "A condição (prótase) já está no Congiuntivo Trapassato"),
        ("L'italiano standard deriva dal VOLGARE TOSCANO LETTERARIO del Trecento", "O italiano padrão deriva do vulgar toscano literário do século XIV (Trecento)"),
        ("Il loro modello linguistico divenne la base della lingua letteraria italiana.", "O modelo linguístico de Dante, Petrarca e Boccaccio tornou-se a base da língua literária italiana."),
        ("è il primo trattato teorico sul volgare:", "é o primeiro tratado teórico sobre a língua vulgar:"),
        ("analizza i dialetti italiani e propone un 'volgare illustre' come lingua comune letteraria.", "analisa os dialetos italianos e propõe um 'vulgar ilustre' como língua literária comum."),
        ("vide Pietro Bembo difendere il fiorentino trecentesco", "viu Pietro Bembo defender o florentino do século XIV"),
        ("contro chi preferiva una lingua cortigiana più moderna o varia.", "contra aqueles que preferiam uma língua cortesã mais moderna ou eclética."),
        ("accosta concetti OPPOSTI per creare effetto contrastivo:", "aproxima conceitos OPOSTOS para criar um efeito de contraste:"),
        ("Molto usata in retorica politica.", "Muito utilizada na retórica literária e política."),
        ("identificazione diretta tra due concetti", "identificação direta entre dois conceitos"),
        ("La similitudine usa 'come':", "A comparação (similitudine) usa o conectivo 'come':"),
        ("La metafora è più forte perché elimina il grado di comparazione.", "A metáfora é mais intensa porque funde os termos sem conectivo comparativo."),
        ("è una METAFORA LESSICALIZZATA (ormai convenzionale):", "é uma metáfora lexicalizada (consagrada pelo uso):"),
        ("insensibilità, durezza emotiva.", "insensibilidade e dureza emocional."),
        ("La connotazione ha sopraffatto la denotazione letterale.", "O sentido conotativo (figurado) prevalece sobre o sentido literal."),
        ("nella frase subordinata", "na oração subordinada"),
        ("rispetto alla principale", "em relação à oração principal"),
        ("si usa il", "usa-se o"),
        ("si usa la", "usa-se a"),
        ("si usa ", "usa-se "),
        ("Si usa ", "Usa-se "),
        ("richiede il congiuntivo", "exige o modo Congiuntivo"),
        ("richiede l'indicativo", "exige o modo Indicativo"),
        ("regge il congiuntivo", "rege o modo Congiuntivo"),
        ("regge l'indicativo", "rege o modo Indicativo"),
        ("è obbligatorio", "é obrigatório"),
        ("è invariabile", "é invariável"),
        ("al plurale", "no plural"),
        ("al singolare", "no singular"),
        ("nel parlato", "na língua falada"),
        ("nello scritto", "na língua escrita"),
        ("invece di", "em vez de"),
        ("significa", "significa"),
    ]
    out = exp
    for k, v in subs:
        out = out.replace(k, v)
    return out

def main():
    with open("data/grammar.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    fixed_cards_count = 0
    removed_bad_ex_count = 0
    updated_c1_c2_count = 0

    for mod in data["moduli"]:
        for u in mod["lezioni"]:
            uid = u["id"]

            # 1. Preencher C1 e C2 com todas as camadas didáticas
            if uid in C1_C2_CONTENT:
                patch = C1_C2_CONTENT[uid]
                for k, v in patch.items():
                    u[k] = v
                updated_c1_c2_count += 1

            # 2. Corrigir observacao_cards de a1-lez3 a a1-lez30
            if "observacao_cards" in u and isinstance(u["observacao_cards"], list):
                for card in u["observacao_cards"]:
                    it_phrase = card.get("italiano", "").strip()
                    if it_phrase in A1_CARDS_FIX:
                        trad_pt, art_badge, gen_label, mot_pt = A1_CARDS_FIX[it_phrase]
                        card["traducao"] = trad_pt
                        card["artigo"] = art_badge
                        card["genero"] = gen_label
                        card["motivo"] = mot_pt
                        fixed_cards_count += 1

            # 3. Limpar exercícios corrompidos ('EXERCÍCIOS EXTRAS' / '(Extra)' com respostas coladas de outra lição)
            if "exercicios" in u and isinstance(u["exercicios"], list):
                cleaned_exs = []
                for ex in u["exercicios"]:
                    perg = ex.get("pergunta", "")
                    exp = ex.get("explicacao", "")
                    if "EXERCÍCIOS EXTRAS" in perg or "(Extra)" in perg or "undefined" in exp:
                        removed_bad_ex_count += 1
                        continue
                    ex["explicacao"] = translate_it_explanation_to_pt(exp, ex, u.get("titulo", ""))
                    cleaned_exs.append(ex)
                u["exercicios"] = cleaned_exs

    with open("data/grammar.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Sucesso! Lições C1/C2 enriquecidas: {updated_c1_c2_count} | Cards A1 corrigidos: {fixed_cards_count} | Exercícios corrompidos removidos: {removed_bad_ex_count}")

if __name__ == "__main__":
    main()
