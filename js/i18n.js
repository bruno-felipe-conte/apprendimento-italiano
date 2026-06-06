// ============================================================
// i18n.js — Sistema de Localização (Imersão Total em Italiano)
// ============================================================

const I18n = {
  idioma: 'pt',
  
  dict: {
    // ── Abas de Navegação (Bottom / Mobile) ──
    'nav_inicio': { pt: 'Início', it: 'Inizio' },
    'nav_dialogos': { pt: 'Diálogos', it: 'Dialoghi' },
    'nav_canzoni': { pt: 'Canzoni', it: 'Canzoni' },
    'nav_imitacao': { pt: 'Imitação', it: 'Imitazione' },
    'nav_flashcard': { pt: 'Flashcard', it: 'Flashcard' },
    'nav_quiz': { pt: 'Quiz', it: 'Quiz' },
    'nav_vocab': { pt: 'Vocab', it: 'Vocabolario' },
    'nav_gramatica': { pt: 'Gramática', it: 'Grammatica' },
    'nav_storie':    { pt: 'Storie', it: 'Storie' },
    
    // ── Abas de Navegação (Top / Desktop) ──
    'top_nav_templi': { pt: 'Templi', it: 'Templi' },
    'top_nav_dialoghi': { pt: 'Dialoghi', it: 'Dialoghi' },
    'top_nav_canzoni': { pt: 'Canzoni', it: 'Canzoni' },
    'top_nav_imitazione': { pt: 'Imitazione', it: 'Imitazione' },
    'top_nav_flashcard': { pt: 'Flashcard', it: 'Flashcard' },
    'top_nav_quiz': { pt: 'Quiz', it: 'Quiz' },
    'top_nav_vocabolario': { pt: 'Vocabolario', it: 'Vocabolario' },
    'top_nav_grammatica': { pt: 'Gramática', it: 'Grammatica' },
    'top_nav_storie':     { pt: 'Storie',     it: 'Storie' },

    // ── Elementos Globais ──
    'meta_do_dia': { pt: 'Meta do dia', it: 'Obiettivo del giorno' },
    'config_perfil': { pt: 'Configurações & Perfil', it: 'Impostazioni & Profilo' },
    'btn_fechar': { pt: 'Fechar', it: 'Chiudi' },
    'btn_cancelar': { pt: 'Cancelar', it: 'Annulla' },
    'btn_salvar': { pt: 'Salvar', it: 'Salva' },

    // ── Modal de Configurações ──
    'cfg_titulo': { pt: 'Configurações', it: 'Impostazioni' },
    'cfg_idioma_app': { pt: 'Idioma do App', it: 'Lingua dell\'App' },
    'cfg_idioma_pt': { pt: 'Português (PT)', it: 'Portoghese (PT)' },
    'cfg_idioma_it': { pt: 'Italiano (IT) - Imersão', it: 'Italiano (IT) - Immersione' },
    'cfg_tema_claro': { pt: 'Modo Claro', it: 'Tema Chiaro' },
    'cfg_tema_escuro': { pt: 'Modo Escuro', it: 'Tema Scuro' },
    'cfg_sons_ligados': { pt: 'Sons: Ligados', it: 'Suoni: Attivi' },
    'cfg_sons_desligados': { pt: 'Sons: Desligados', it: 'Suoni: Disattivati' },
    
    // ── Modal Meta de XP (Configurações) ──
    'meta_diaria_xp': { pt: 'Meta Diária de XP', it: 'Obiettivo Quotidiano XP' },
    'quantos_xp': { pt: 'Quantos XP quer ganhar por dia?', it: 'Quanti XP vuoi guadagnare al giorno?' },

    // ── Modal Meta com Prazo ──
    'meta_minha': { pt: '🎯 Minha Meta', it: '🎯 Il Mio Obiettivo' },
    'meta_nivel': { pt: 'Quero atingir o nível:', it: 'Voglio raggiungere il livello:' },
    'meta_data': { pt: 'Até a data:', it: 'Entro il:' },
    'meta_definir': { pt: 'Definir Meta', it: 'Imposta Obiettivo' },
    'meta_remover': { pt: 'Remover meta atual', it: 'Rimuovi obiettivo attuale' },
    'nivel_5': { pt: 'Nível 5 — Principiante (A1)', it: 'Livello 5 — Principiante (A1)' },
    'nivel_10': { pt: 'Nível 10 — Intermediário (A2)', it: 'Livello 10 — Intermedio (A2)' },
    'nivel_15': { pt: 'Nível 15 — Avançado (B1)', it: 'Livello 15 — Avanzato (B1)' },
    'nivel_20': { pt: 'Nível 20 — Maestro (B2)', it: 'Livello 20 — Maestro (B2)' },
    
    // ── Perfil e Gestão de Dados ──
    'prof_gestao_dati': { pt: '⚙️ Gestão de Dados', it: '⚙️ Gestione Dati' },
    'prof_backup_desc': { pt: 'O Italiano Autentico guarda seu progresso localmente no seu dispositivo. Faça backup regularmente para não perder seus dados caso limpe o histórico do navegador.', it: 'Italiano Autentico salva i tuoi progressi localmente sul tuo dispositivo. Fai regolarmente un backup per non perdere i tuoi dati se cancelli la cronologia del browser.' },
    'prof_exp_backup': { pt: '⬇️ Exportar Backup', it: '⬇️ Esporta Backup' },
    'prof_imp_backup': { pt: '⬆️ Importar Backup', it: '⬆️ Importa Backup' },
    'prof_azzera': { pt: '⚠️ Apagar Tudo', it: '⚠️ Azzera Tutto' },
    'prof_conteudo_criado': { pt: 'Conteúdo Criado por Mim', it: 'Contenuto Creato da Me' },
    'prof_exp_conteudo': { pt: '⬇️ Exportar Músicas e Diálogos', it: '⬇️ Esporta Canzoni e Dialoghi' },
    'prof_imp_conteudo': { pt: '⬆️ Importar Conteúdo', it: '⬆️ Importa Contenuto' },
    
    // ── Seção Templos ──
    'templi_titulo': { pt: 'Sua Jornada', it: 'Il Tuo Viaggio' },
    'templi_sub': { pt: 'Explore os templos e domine o vocabulário.', it: 'Esplora i templi e padroneggia il vocabolario.' },
    'btn_continuar': { pt: 'Continuar de Onde Parou', it: 'Continua da Dove Eri Rimasto' },

    // ── Feedback e Notificações (Usados no JS) ──
    'notif_salvo': { pt: 'Salvo com sucesso!', it: 'Salvato con successo!' },
    'notif_erro': { pt: 'Ocorreu um erro.', it: 'Si è verificato un errore.' },
    'notif_bloqueado': { pt: 'Templo não desbloqueado.', it: 'Tempio non sbloccato.' },

    // ── Core / Templos ──
    'notif_templo_sbloccato': { pt: '🏛️ Templo {n} desbloqueado!', it: '🏛️ Tempio {n} sbloccato!' },
    'notif_templo_completato': { pt: '🏆 Templo {n} completado!', it: '🏆 Tempio {n} completato!' },
    'notif_codice_errato': { pt: 'Código incorreto.', it: 'Codice non corretto.' },
    'notif_tutti_sbloccati': { pt: 'Todos os templos desbloqueados! 🎉', it: 'Tutti i templi sbloccati! 🎉' },
    'notif_data_futura': { pt: 'A data limite deve ser no futuro.', it: 'La data limite deve essere nel futuro.' },
    'notif_meta_definida': { pt: 'Meta: {val} XP/dia', it: 'Obiettivo: {val} XP/giorno' },
    'meta_do_dia_label': { pt: '🎯 Meta do dia', it: '🎯 Obiettivo del giorno' },

    // ── Áudio ──
    'notif_sons_ativados': { pt: '🔔 Sons ativados', it: '🔔 Suoni attivati' },
    'notif_sons_desativados': { pt: '🔕 Sons desativados', it: '🔕 Suoni disattivati' },

    // ── Flashcards ──
    'notif_fc_bloqueado': { pt: 'Templo não desbloqueado ainda!', it: 'Tempio non ancora sbloccato!' },
    'notif_fc_vocab_nao_carregado': { pt: 'Vocabulário deste templo não carregado.', it: 'Vocabolario di questo tempio non caricato.' },
    'notif_fc_erro_resposta': { pt: 'Erro ao registrar resposta. Tente novamente.', it: 'Errore nel registrare la risposta. Riprova.' },
    'notif_fc_favorito_add': { pt: '❤️ Adicionado aos favoritos', it: '❤️ Aggiunto ai preferiti' },
    'notif_fc_favorito_rem': { pt: '🤍 Removido dos favoritos', it: '🤍 Rimosso dai preferiti' },
    'notif_fc_sem_favoritos': { pt: 'Nenhum favorito ainda. Adicione com o ❤️!', it: 'Nessun preferito ancora. Aggiungi con il ❤️!' },
    'notif_fc_favoritos_nao_enc': { pt: 'Palavras favoritas não encontradas nos dados.', it: 'Parole preferite non trovate nei dati.' },
    'notif_fc_favoritos_revisar': { pt: '❤️ {n} favoritos para revisar', it: '❤️ {n} preferiti da ripassare' },
    'notif_fc_sem_dificeis': { pt: 'Nenhuma palavra difícil encontrada! 🎉', it: 'Nessuna parola difficile trovata! 🎉' },
    'notif_fc_dificeis_revisar': { pt: '📚 {n} palavras difíceis para revisar', it: '📚 {n} parole difficili da ripassare' },
    'notif_fc_sem_voz': { pt: 'Seu browser não suporta reconhecimento de voz.', it: 'Il tuo browser non supporta il riconoscimento vocale.' },
    'notif_fc_nao_ouviu': { pt: 'Não consegui ouvir. Tente novamente.', it: 'Non ho sentito. Riprova.' },

    // ── Gramática ──
    'notif_gram_capitolo': { pt: '🏆 Capítulo completado! +{xp} XP', it: '🏆 Capitolo completato! +{xp} XP' },

    // ── Canzoni (custom) ──
    'notif_can_titulo_obr': { pt: 'O título é obrigatório.', it: 'Il titolo è obbligatorio.' },
    'notif_can_sem_verso': { pt: 'Adicione pelo menos um verso com lacuna.', it: 'Aggiungi almeno un verso con lacuna.' },
    'notif_can_excluida': { pt: 'Música excluída.', it: 'Canzone eliminata.' },

    // ── Dialoghi (custom) ──
    'notif_dial_titulo_obr': { pt: 'O título é obrigatório.', it: 'Il titolo è obbligatorio.' },
    'notif_dial_sem_turnos': { pt: 'Adicione pelo menos 2 turnos.', it: 'Aggiungi almeno 2 turni.' },
    'notif_dial_excluido': { pt: 'Diálogo excluído.', it: 'Dialogo eliminato.' },

    // ── Core — templates renderizados ──
    'cc_continuar_label': { pt: 'Continuar de onde parou', it: 'Continua da dove eri rimasto' },
    'cc_retomar': { pt: '→ Retomar', it: '→ Riprendi' },
    'cc_ultima_sessao': { pt: 'Última sessão:', it: 'Ultima sessione:' },
    'cc_agora_mesmo': { pt: 'agora mesmo', it: 'proprio adesso' },
    'cc_ha_minutos': { pt: 'há poucos minutos', it: 'pochi minuti fa' },
    'cc_ha_horas': { pt: 'há {n}h', it: '{n}h fa' },
    'cc_ha_dias': { pt: 'há {n} dia(s)', it: '{n} giorno/i fa' },
    'cc_secao_inicio': { pt: 'Início', it: 'Inizio' },
    'cc_secao_vocab': { pt: 'Vocabulário', it: 'Vocabolario' },
    'cc_secao_gram': { pt: 'Gramática', it: 'Grammatica' },
    'cc_secao_perfil': { pt: 'Perfil', it: 'Profilo' },
    'meta_definir_prazo': { pt: 'Definir uma meta com prazo', it: 'Imposta un obiettivo con scadenza' },
    'meta_dias_restantes': { pt: '{n} dias restantes', it: '{n} giorni rimanenti' },
    'meta_no_ritmo': { pt: 'No ritmo atual:', it: 'Al ritmo attuale:' },
    'meta_xp_necessarios': { pt: 'XP/dia necessários', it: 'XP/giorno necessari' },
    'templo_requer': { pt: 'Requer Livello {n} · Toque para inserir código', it: 'Richiede Livello {n} · Tocca per inserire il codice' },

    // ── Heatmap ──
    'hm_atividades': { pt: 'atividades em', it: 'attività in' },
    'hm_dias': { pt: 'dias', it: 'giorni' },
    'hm_sequencia': { pt: 'Sequência:', it: 'Sequenza:' },
    'hm_atividades_tooltip': { pt: 'atividades', it: 'attività' },

    // ── Progression ──
    'notif_meta_atingida': { pt: '🎯 Meta diária atingida! Ottimo!', it: '🎯 Obiettivo giornaliero raggiunto! Ottimo!' },
    'notif_meta_def_ok': { pt: '🎯 Meta definida! Boa sorte!', it: '🎯 Obiettivo impostato! Buona fortuna!' },

    // ── Quiz ──
    'notif_quiz_bloqueado': { pt: 'Tempio não desbloqueado!', it: 'Tempio non sbloccato!' },
    'notif_quiz_sem_perguntas': { pt: 'Nenhuma pergunta disponível para este tempio.', it: 'Nessuna domanda disponibile per questo tempio.' },
    'notif_quiz_sem_perguntas_todos': { pt: 'Nenhuma pergunta disponível para os templos desbloqueados.', it: 'Nessuna domanda disponibile per i templi sbloccati.' },
    'notif_quiz_morf_insuf': { pt: 'Dados de morfologia insuficientes para este tempio.', it: 'Dati morfologici insufficienti per questo tempio.' },
    'notif_quiz_conj_insuf': { pt: 'Dados de conjugação insuficientes.', it: 'Dati di coniugazione insufficienti.' },
    'notif_quiz_listen_insuf': { pt: 'Dados insuficientes para listening.', it: 'Dati insufficienti per il listening.' },
    'notif_quiz_gram_insuf': { pt: 'Dados insuficientes de gramática para este nível.', it: 'Dati grammaticali insufficienti per questo livello.' },

    // ── Profilo ──
    'notif_backup_exp': { pt: '✅ Backup exportado com sucesso!', it: '✅ Backup esportato con successo!' },
    'notif_backup_imp': { pt: '✅ Backup importado! Recarregando...', it: '✅ Backup importato! Ricaricamento...' },
    'notif_arquivo_inv': { pt: '❌ Arquivo inválido: ', it: '❌ File non valido: ' },
    'notif_prog_reset': { pt: 'Progresso resetado. Recarregando...', it: 'Progresso azzerato. Ricaricamento...' },
    'notif_conteudo_exp': { pt: '✅ Conteúdo exportado!', it: '✅ Contenuto esportato!' },

    // ── Conquistas — descrições ──
    'ach_primeiro_passo': { pt: 'Complete seu primeiro flashcard', it: 'Completa il tuo primo flashcard' },
    'ach_uma_semana': { pt: '7 dias consecutivos de estudo', it: '7 giorni consecutivi di studio' },
    'ach_studioso': { pt: 'Revisar 100 cartas nos flashcards', it: 'Ripassa 100 carte nei flashcard' },
    'ach_quiz_perfetto': { pt: '10/10 acertos em um quiz', it: '10/10 risposte corrette in un quiz' },
    'ach_primo_tempio': { pt: 'Completar o Tempio 1 nos flashcards', it: 'Completa il Tempio 1 nei flashcard' },
    'ach_vocabulario': { pt: 'Dominar 50 palavras (3+ revisões)', it: 'Padroneggia 50 parole (3+ revisioni)' },
    'ach_duro': { pt: 'Marcar "Esqueci" 50 vezes — a perseverança tem recompensa', it: 'Segna "Non ricordo" 50 volte — la perseveranza ha la sua ricompensa' },
    'ach_italiano_autentico': { pt: 'Atingir o Livello 10', it: 'Raggiungere il Livello 10' },
    'ach_um_mes': { pt: '30 dias consecutivos de estudo', it: '30 giorni consecutivi di studio' },
    'ach_maestro': { pt: 'Revisar 500 cartas nos flashcards', it: 'Ripassa 500 carte nei flashcard' },
    'ach_esploratore': { pt: 'Desbloquear 5 templos', it: 'Sblocca 5 templi' },
    'ach_grammatico': { pt: 'Completar 10 lições de gramática', it: 'Completa 10 lezioni di grammatica' },
    'ach_precisione': { pt: '5 quizzes seguidos com mais de 80% de acerto', it: '5 quiz consecutivi con più dell\'80% di risposte corrette' },
    'ach_notturno': { pt: 'Estudar após as 22h', it: 'Studiare dopo le 22:00' },
    'ach_mattiniero': { pt: 'Estudar antes das 7h da manhã', it: 'Studiare prima delle 7:00 del mattino' },

    // ── Flashcard — estado vazio ──
    'fc_todas_estudadas': { pt: 'Todas as cartas estudadas hoje.', it: 'Tutte le carte studiate oggi.' },

    // ── Flashcard — dicas no card ──
    'fc_dica_ouvir': { pt: 'Toque no card para ouvir novamente 🔊', it: 'Tocca la carta per ascoltare di nuovo 🔊' },
    'fc_dica_palavra_falta': { pt: 'Que palavra falta?', it: 'Quale parola manca?' },
    'fc_dica_revelar': { pt: 'Clique para revelar', it: 'Clicca per rivelare' },

    // ── Flashcard — resumo da sessão ──
    'fc_resumo_muito_bom': { pt: 'Muito bom!', it: 'Molto bene!' },
    'fc_resumo_continua': { pt: 'Continua a praticare!', it: 'Continua a praticare!' },
    'fc_resumo_sem_agendamento': { pt: 'Sem agendamento', it: 'Nessuna programmazione' },
    'fc_resumo_em_dias': { pt: 'em {n} dia', it: 'tra {n} giorno' },
    'fc_resumo_em_dias_plural': { pt: 'em {n} dias', it: 'tra {n} giorni' },
    'fc_resumo_em_horas': { pt: 'em {n}h', it: 'tra {n}h' },
    'fc_resumo_cartas': { pt: 'cartas', it: 'carte' },
    'fc_resumo_acertos': { pt: 'acertos', it: 'risposte corrette' },
    'fc_resumo_proxima': { pt: '⏰ Próxima revisão:', it: '⏰ Prossima revisione:' },
    'fc_resumo_novas': { pt: '🌱 {n} palavra nova aprendida!', it: '🌱 {n} parola nuova appresa!' },
    'fc_resumo_novas_plural': { pt: '🌱 {n} palavras novas aprendidas!', it: '🌱 {n} parole nuove apprese!' },
    'fc_resumo_praticar': { pt: '🔁 Praticar todas', it: '🔁 Pratica tutte' },
    'fc_gravar_parar': { pt: '⏹ Parar', it: '⏹ Ferma' },
    'fc_gravar_imitar': { pt: '🎤 Imitar', it: '🎤 Imita' },

    // ── Quiz — feedback e resultado ──
    'quiz_correto': { pt: '✅ Correto!', it: '✅ Corretto!' },
    'quiz_resposta_correta_era': { pt: '❌ A resposta correta era:', it: '❌ La risposta corretta era:' },
    'quiz_xp_ganhos': { pt: '+{n} XP ganhos', it: '+{n} XP guadagnati' },

    // ── Quiz — morfologia (gerado dinamicamente) ──
    'quiz_morf_genero_pergunta': { pt: 'Qual o gênero de "{w}"?', it: 'Qual è il genere di "{w}"?' },
    'quiz_morf_genero_masc': { pt: 'masculino', it: 'maschile' },
    'quiz_morf_genero_fem': { pt: 'feminino', it: 'femminile' },
    'quiz_morf_genero_exp': { pt: '"{w}" é {g}', it: '"{w}" è {g}' },
    'quiz_morf_plural_pergunta': { pt: 'Qual o plural de "{w}"?', it: 'Qual è il plurale di "{w}"?' },
    'quiz_morf_plural_exp': { pt: 'O plural de "{w}" é "{p}".', it: 'Il plurale di "{w}" è "{p}".' },

    // ── Imitazione ──
    'imit_erro_ouvir': { pt: 'Erro ao ouvir. Tente novamente.', it: 'Errore nell\'ascolto. Riprova.' },

    // ── Storie — leitura interativa ──
    'storie_titulo_secao':   { pt: 'Storie Italiane', it: 'Storie Italiane' },
    'storie_escolha':        { pt: 'Escolha uma história para começar a leitura', it: 'Scegli una storia per iniziare la lettura' },
    'storie_btn_traduzir':   { pt: '👁️ Ocultar tradução', it: '👁️ Nascondi traduzione' },
    'storie_btn_mostrar':    { pt: '👁️ Mostrar tradução', it: '👁️ Mostra traduzione' },
    'storie_btn_ouvir_tudo': { pt: '🔊 Ouvir tudo', it: '🔊 Ascolta tutto' },
    'storie_btn_concluir':   { pt: '✓ Concluí (+{xp} XP)', it: '✓ Ho finito (+{xp} XP)' },
    'storie_btn_relida':     { pt: '✓ Relida', it: '✓ Riletta' },
    'storie_btn_todas':      { pt: '‹ Todas as histórias', it: '‹ Tutte le storie' },
    'storie_notif_lida':     { pt: '📖 +{xp} XP por terminar a história!', it: '📖 +{xp} XP per aver finito la storia!' },
    'storie_notif_ja_lida':  { pt: 'Você já leu esta história.', it: 'Hai già letto questa storia.' },
    'storie_vocab_titulo':   { pt: '📚 Vocabulário ({n})', it: '📚 Vocabolario ({n})' },

    // ── index.html — onboarding e strings estáticas ──
    'ob_descricao': { pt: 'Este app foi desenhado para te levar do zero ao italiano falado de forma simples, natural e altamente eficaz. Cada sessão dura aproximadamente 10 minutos.', it: 'Questa app è stata progettata per portarti da zero all\'italiano parlato in modo semplice, naturale e altamente efficace. Ogni sessione dura circa 10 minuti.' },
    'ob_como_comecar': { pt: 'É muito fácil começar sua jornada:', it: 'È molto facile iniziare il tuo viaggio:' },

    // ── Flashcard — labels inline ──
    'fc_novas': { pt: 'novas', it: 'nuove' },
    'fc_revisao': { pt: 'revisão', it: 'da ripassare' },
    'fc_escolha_vocab': { pt: 'Escolha um conjunto de vocabulário para estudar', it: 'Scegli un insieme di vocabolario da studiare' },
    'fc_selecione_tempio': { pt: 'Selecione um Tempio', it: 'Seleziona un Tempio' },
    'fc_use_seletor': { pt: '↑ use o seletor acima', it: '↑ usa il selettore sopra' },
    'fc_volte_amanha': { pt: 'Volte amanhã para as próximas revisões.', it: 'Torna domani per le prossime revisioni.' },
    'fc_btn_pronunciar': { pt: '🔊 Pronunciar', it: '🔊 Pronuncia' },
    'fc_btn_imitar': { pt: '🎤 Imitar', it: '🎤 Imita' },
    'fc_btn_esqueci': { pt: '❌ Esqueci', it: '❌ Non ricordo' },
    'fc_btn_dificil': { pt: '⚡ Difícil', it: '⚡ Difficile' },
    'fc_btn_bom': { pt: '✅ Bom', it: '✅ Bene' },
    'fc_btn_facil': { pt: '⭐ Fácil', it: '⭐ Facile' },
    'fc_btn_favoritos': { pt: '❤️ Favoritos', it: '❤️ Preferiti' },
    'fc_btn_dificeis': { pt: '⚠️ Difíceis', it: '⚠️ Difficili' },
    'fc_btn_praticar_todas': { pt: '🔁 Praticar todas', it: '🔁 Pratica tutte' },

    // ── Quiz ──
    'quiz_morf_titulo': { pt: '🔤 Quiz de Morfologia (Gênero & Plural)', it: '🔤 Quiz di Morfologia (Genere & Plurale)' },
    'quiz_list_titulo': { pt: '🎧 Quiz de Listening (Ascolto)', it: '🎧 Quiz di Listening (Ascolto)' },
    'quiz_gram_titulo': { pt: '📚 Quiz de Gramática (Grammatica)', it: '📚 Quiz di Grammatica' },
    'quiz_gram_nao_carregado': { pt: 'Dados de gramática não carregados.', it: 'Dati grammaticali non caricati.' },
    'quiz_verbi_titulo': { pt: '🇮🇹 Quiz de Conjugação Verbal', it: '🇮🇹 Quiz di Coniugazione Verbale' },
    'quiz_verbi_nao_carregado': { pt: 'Dados de conjugação não carregados.', it: 'Dati di coniugazione non caricati.' },
    'quiz_pergunta_de': { pt: 'Pergunta {a} de {b}', it: 'Domanda {a} di {b}' },
    'quiz_ouvir': { pt: '🔊 Ouvir', it: '🔊 Ascolta' },
    'quiz_continuar': { pt: 'Continuar →', it: 'Continua →' },
    'quiz_voltar': { pt: '← Voltar aos Templi', it: '← Torna ai Templi' },

    // ── Vocab ──
    'vocab_dificeis': { pt: '⚠️ Difíceis', it: '⚠️ Difficili' },
    'vocab_favoritos': { pt: '❤️ Favoritos', it: '❤️ Preferiti' },
    'vocab_palavras_total': { pt: '{n} palavras no total', it: '{n} parole in totale' },
    'vocab_palavra_dificil': { pt: '{n} palavra difícil (3+ erros)', it: '{n} parola difficile (3+ errori)' },
    'vocab_palavras_dificeis': { pt: '{n} palavras difíceis (3+ erros)', it: '{n} parole difficili (3+ errori)' },
    'vocab_resultados': { pt: '{m} de {f} resultado(s) — {t} palavras totais', it: '{m} di {f} risultati — {t} parole totali' },
    'vocab_nenhuma': { pt: 'Nenhuma palavra encontrada.', it: 'Nessuna parola trovata.' },
    'vocab_ocultar_pt': { pt: '👁 Ocultar PT', it: '👁 Nascondi PT' },
    'vocab_ocultar_it': { pt: '👁 Ocultar IT', it: '👁 Nascondi IT' },

    // ── Core — streak ──
    'streak_dia': { pt: '🔥 {n} dia', it: '🔥 {n} giorno' },
    'streak_dias': { pt: '🔥 {n} dias', it: '🔥 {n} giorni' },

    // ── Grammar — feedback ──
    'gram_conteudo_indisponivel': { pt: 'Conteúdo não disponível.', it: 'Contenuto non disponibile.' },
    'gram_placeholder_resposta': { pt: 'Digite sua resposta...', it: 'Scrivi la tua risposta...' },
    'gram_por_que': { pt: 'Por que?', it: 'Perché?' },
    'gram_correto': { pt: 'Correto!', it: 'Corretto!' },
    'gram_errado': { pt: 'Errado.', it: 'Sbagliato.' },
    'gram_resposta_era': { pt: 'A resposta era:', it: 'La risposta era:' },
    'gram_por_que_importa': { pt: 'Por que isso importa?', it: 'Perché è importante?' },
    'gram_arm_errado': { pt: 'Errado', it: 'Sbagliato' },
    'gram_arm_certo': { pt: 'Certo', it: 'Corretto' },

    // ── Quiz — gramática ──
    'quiz_gram_nivel': { pt: '📚 Nível {n}', it: '📚 Livello {n}' },

    // ── Vocab — overflow ──
    'vocab_e_mais': { pt: '... e mais {n} palavras. Use os filtros para refinar.', it: '... e altre {n} parole. Usa i filtri per affinare.' },

    // ── Imitazione — resultados ──
    'imit_voce_disse': { pt: 'Você disse:', it: 'Hai detto:' },
    'imit_ouvimos': { pt: 'Ouvimos:', it: 'Abbiamo sentito:' },
    'imit_proxima_frase': { pt: 'Próxima Frase', it: 'Frase Successiva' },
    'imit_tentar_novamente': { pt: 'Tentar Novamente', it: 'Riprova' },
    'imit_pronunciar_melhor': { pt: 'Tente pronunciar mais claramente.', it: 'Prova a pronunciare più chiaramente.' },
    'imit_ouvir_exemplo': { pt: 'Ouça o exemplo e tente de novo.', it: 'Ascolta l\'esempio e riprova.' },

    // ── Canzoni — resultado ──
    'can_corretas': { pt: '{a}/{b} corretas', it: '{a}/{b} corrette' },
    'can_repetir': { pt: '🔄 Repetir', it: '🔄 Ripeti' },
    'can_outras_musicas': { pt: '‹ Outras músicas', it: '‹ Altre canzoni' },
    'can_salva': { pt: '🎵 "{t}" salva!', it: '🎵 "{t}" salvata!' },

    // ── Dialoghi — resultado ──
    'dial_concluido': { pt: 'Diálogo Concluído', it: 'Dialogo Completato' },
    'dial_acertos': { pt: 'Acertos: {a} / {b}', it: 'Risposte corrette: {a} / {b}' },
    'dial_vocab_chave': { pt: 'Vocabulário Chave:', it: 'Vocabolario Chiave:' },
    'dial_voltar': { pt: '‹ Voltar', it: '‹ Torna' },
    'dial_salvo': { pt: '💬 "{t}" salvo!', it: '💬 "{t}" salvato!' },

    // ── Onboarding slide 2 ──
    'ob_vocabulario': { pt: 'Vocabulário:', it: 'Vocabolario:' },
    'ob_gramatica': { pt: 'Gramática:', it: 'Grammatica:' },

    // ── Dialoghi ──
    'dial_praticar_novamente': { pt: 'Praticar Novamente 🔄', it: 'Pratica di nuovo 🔄' },
    'dial_excluir_confirm': { pt: 'Excluir "{t}"?', it: 'Eliminare "{t}"?' },

    // ── Canzoni ──
    'can_excluir_confirm': { pt: 'Excluir "{t}"?', it: 'Eliminare "{t}"?' },

    // ── Perfil — confirms destrutivos ──
    'prof_confirm_importar': { pt: 'Isso vai substituir todo o seu progresso atual. Confirmar?', it: 'Questo sostituirà tutti i tuoi progressi attuali. Confermi?' },
    'prof_confirm_apagar1': { pt: '⚠️ Isso apagará TODO o seu progresso — XP, flashcards, conquistas e streak. Tem certeza?', it: '⚠️ Questo cancellerà TUTTI i tuoi progressi — XP, flashcard, traguardi e sequenza. Sei sicuro?' },
    'prof_confirm_apagar2': { pt: 'Esta ação é IRREVERSÍVEL. Deseja mesmo começar do zero?', it: 'Questa azione è IRREVERSIBILE. Vuoi davvero ricominciare da zero?' },
    'prof_confirm_import_content': { pt: 'Importar {c} músicas e {d} diálogos? O conteúdo existente será mantido e mesclado.', it: 'Importare {c} canzoni e {d} dialoghi? Il contenuto esistente sarà mantenuto e unito.' },
    'prof_erro_formato': { pt: 'Formato inválido', it: 'Formato non valido' },

    // ── Quiz — initial label ──
    'quiz_pergunta_inicial': { pt: 'Pergunta 1 de 10', it: 'Domanda 1 di 10' },

    // ── index.html — section titles ──
    'sec_dialoghi': { pt: 'Modo Diálogo', it: 'Modo Dialogo' },

    // ── Grammar — NMA layer labels ──
    'gram_fase2_label': { pt: '🔎 Fase 2: Observe e Descubra', it: '🔎 Fase 2: Osserva e Scopri' },
    'gram_fase2_sub':   { pt: 'Clique nos cards abaixo para descobrir as regras e padrões de forma prática!', it: 'Clicca sulle schede per scoprire regole e schemi in modo pratico!' },
    'gram_fase3_label': { pt: '📋 Fase 3: Tabela de Referência Rápida', it: '📋 Fase 3: Tabella di Riferimento Rapido' },
    'gram_fase4_label': { pt: '🗣️ Fase 4: Analise os Exemplos', it: '🗣️ Fase 4: Analizza gli Esempi' },
    'gram_fase4_sub':   { pt: 'Clique nos exemplos abaixo para exercitar seu raciocínio antes de ver a resposta!', it: 'Clicca sugli esempi per esercitare il ragionamento prima di vedere la risposta!' },
    'gram_fase4_prc_pergunta': { pt: 'Pergunta', it: 'Domanda' },
    'gram_fase4_prc_resposta': { pt: 'Resposta', it: 'Risposta' },
    'gram_fase4_prc_conclusao': { pt: 'Conclusão', it: 'Conclusione' },
    'gram_fase4_ver_detalhes': { pt: 'Ver detalhes ▾', it: 'Vedi dettagli ▾' },
    'gram_fase5_label': { pt: '⚠️ Fase 5: Evite Armadilhas Comuns', it: '⚠️ Fase 5: Evita le Trappole Comuni' },
    'gram_fase5_sub':   { pt: 'Erros comuns cometidos por estudantes de português e como evitá-los:', it: 'Errori comuni commessi dagli studenti e come evitarli:' },
    'gram_fase5_porque': { pt: 'Porquê?', it: 'Perché?' },
    'gram_inventario_label': { pt: '✅ O que você vai aprender', it: '✅ Cosa imparerai' },
    'gram_definicao_label': { pt: '🔍 Observe e entenda', it: '🔍 Osserva e capisci' },
    'gram_def_veja':    { pt: 'Veja', it: 'Osserva' },
    'gram_def_pense':   { pt: 'Pense', it: 'Rifletti' },
    'gram_def_entenda': { pt: 'Entenda', it: 'Capisci' },
    'gram_tecnica_label': { pt: '📌 Como usar na prática', it: '📌 Come usarlo in pratica' },
    'gram_exemplos_prc_label': { pt: '🗣️ Veja os exemplos (clique 🔊 para ouvir)', it: '🗣️ Vedi gli esempi (clicca 🔊 per ascoltare)' },
    'gram_ponte_label': { pt: '🇧🇷 Em português é assim… em italiano é assim:', it: '🇧🇷 In portoghese è così… in italiano è così:' },

    // ── Tooltips — flashcard buttons ──
    'title_reverso':   { pt: 'Reverso: PT→IT', it: 'Inverso: PT→IT' },
    'title_contexto':  { pt: 'Contexto: frase com lacuna', it: 'Contesto: frase con lacuna' },
    'title_escuta':    { pt: 'Escuta: adivinhe pelo áudio', it: 'Ascolto: indovina dall\'audio' },
    'title_dica':      { pt: 'Ver dica (nível 1)', it: 'Mostra suggerimento (livello 1)' },
    'title_favorito':  { pt: 'Adicionar/remover favorito', it: 'Aggiungi/rimuovi dai preferiti' },
    'title_blur_pt':   { pt: 'Oculta a coluna em português para testar sua memória', it: 'Nasconde la colonna portoghese per testare la memoria' },
    'title_blur_it':   { pt: 'Oculta a coluna em italiano para testar sua memória', it: 'Nasconde la colonna italiana per testare la memoria' },

    // ── Onboarding slide 3 ──
    'ob_slide3_li1': { pt: 'Acesse a aba <strong>TEMPLOS</strong>', it: 'Vai alla scheda <strong>TEMPLI</strong>' },
    'ob_slide3_li2': { pt: 'Escolha o <strong>1º Templo (Roma - Le Fondamenta)</strong>', it: 'Scegli il <strong>1° Tempio (Roma - Le Fondamenta)</strong>' },
    'ob_slide3_li3': { pt: 'Estude usando os <strong>FLASHCARDS</strong>', it: 'Studia con i <strong>FLASHCARD</strong>' },
    'ob_slide3_li4': { pt: 'Pratique o que aprendeu respondendo aos <strong>QUIZZES</strong>!', it: 'Metti alla prova con i <strong>QUIZ</strong>!' },

    // ── Dialoghi / Canzoni — botões de criação ──
    'dial_btn_adicionar': { pt: '➕ Adicionar Diálogo', it: '➕ Aggiungi Dialogo' },
    'can_btn_adicionar':  { pt: '➕ Adicionar Música',  it: '➕ Aggiungi Canzone' },

    // ── Imitazione — botão ouvir ──
    'imit_btn_ouvir_exemplo': { pt: '🔊 Ouvir Exemplo', it: '🔊 Ascolta l\'Esempio' },

    // ── Tour ──
    'tour_templi_title': { pt: '🏛️ Templi (Sua Jornada)', it: '🏛️ Templi (Il Tuo Viaggio)' },
    'tour_templi_desc': { pt: 'Aqui é o coração do seu aprendizado. Desbloqueie novos templos e alcance sua meta diária de experiência.', it: 'Questo è il cuore del tuo apprendimento. Sblocca nuovi templi e raggiungi il tuo obiettivo quotidiano di esperienza.' },
    'tour_dialoghi_title': { pt: '💬 Dialoghi', it: '💬 Dialoghi' },
    'tour_dialoghi_desc': { pt: 'Leia e escute diálogos reais para pegar o ritmo, contexto e melhorar sua compreensão auditiva.', it: 'Leggi e ascolta dialoghi reali per cogliere il ritmo, il contesto e migliorare la tua comprensione auditiva.' },
    'tour_canzoni_title': { pt: '🎵 Canzoni', it: '🎵 Canzoni' },
    'tour_canzoni_desc': { pt: 'Aprenda vocabulário se divertindo com os clássicos da música italiana.', it: 'Impara il vocabolario divertendoti con i classici della musica italiana.' },
    'tour_imitazione_title': { pt: '🎙️ Imitazione', it: '🎙️ Imitazione' },
    'tour_imitazione_desc': { pt: 'Escute um nativo falando e grave sua própria voz. O segredo para uma dicção autêntica.', it: 'Ascolta un madrelingua e registra la tua voce. Il segreto per una dizione autentica.' },
    'tour_flashcard_title': { pt: '🧠 Flashcard', it: '🧠 Flashcard' },
    'tour_flashcard_desc': { pt: 'Revise o vocabulário no momento exato em que estiver prestes a esquecer, usando nosso algoritmo espaçado.', it: 'Ripassa il vocabolario nel momento esatto in cui stai per dimenticare, usando il nostro algoritmo di ripetizione spaziata.' },
    'tour_quiz_title': { pt: '📝 Quiz', it: '📝 Quiz' },
    'tour_quiz_desc': { pt: 'Teste seus conhecimentos em baterias de exercícios rápidos e conquiste moedas.', it: 'Metti alla prova le tue conoscenze con batterie di esercizi rapidi e conquista monete.' },
    'tour_grammatica_title': { pt: '📚 Grammatica', it: '📚 Grammatica' },
    'tour_grammatica_desc': { pt: 'Dúvidas estruturais? Consulte rapidamente todas as regras de gramática aqui.', it: 'Dubbi strutturali? Consulta rapidamente tutte le regole grammaticali qui.' },
    'tour_vocabolario_title': { pt: '📖 Vocabolario', it: '📖 Vocabolario' },
    'tour_vocabolario_desc': { pt: 'Seu glossário mestre. Pesquise por qualquer palavra aprendida até o momento.', it: 'Il tuo glossario principale. Cerca qualsiasi parola appresa finora.' },
    'tour_config_title': { pt: '⚙️ Configurações & Perfil', it: '⚙️ Impostazioni & Profilo' },
    'tour_config_desc': { pt: 'Mude para o modo escuro, silencie os sons e acesse as opções de Perfil no topo da tela.', it: 'Passa alla modalità scura, silenzia i suoni e accedi alle opzioni del Profilo in cima allo schermo.' }
  },

  inicializar() {
    this.idioma = localStorage.getItem('it_idioma') || 'pt';
    this.traduzirDOM();
  },

  mudarIdioma(lang) {
    if (lang !== 'pt' && lang !== 'it') return;
    document.body.classList.add('lang-switching');       // fade out
    setTimeout(() => {
      this.idioma = lang;
      localStorage.setItem('it_idioma', lang);
      this.traduzirDOM();
      document.dispatchEvent(new CustomEvent('i18n:changed', { detail: { lang } }));
      // Força recarregamento dos dados de gramática na próxima visita à aba
      if (typeof Grammatica !== 'undefined') Grammatica.dados = null;
      document.body.classList.remove('lang-switching'); // fade in
      if (typeof App !== 'undefined') {
        if (lang === 'it') {
          const primeiraVez = !localStorage.getItem('it_imersao_usada');
          if (primeiraVez) {
            localStorage.setItem('it_imersao_usada', '1');
            App.notificar('Benvenuto! Ora sei in modalità Immersione 🇮🇹', 'alerta');
          } else {
            App.notificar('Lingua cambiata in Italiano!', 'sucesso');
          }
        } else {
          App.notificar('Idioma alterado para Português!', 'sucesso');
        }
      }
    }, 180);
  },

  toggleIdioma() {
    this.mudarIdioma(this.idioma === 'pt' ? 'it' : 'pt');
  },

  // Retorna a string traduzida baseada na chave
  t(chave) {
    if (!this.dict[chave]) return chave; // Retorna a chave se não existir tradução
    return this.dict[chave][this.idioma] || this.dict[chave]['pt'];
  },

  // Busca todos os elementos com data-i18n e substitui o innerText (ou HTML mantendo ícones)
  traduzirDOM() {
    // Traduz textContent / value
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const chave = el.getAttribute('data-i18n');
      if (!this.dict[chave]) return;
      const texto = this.dict[chave][this.idioma] || this.dict[chave]['pt'];
      if (el.tagName.toLowerCase() === 'input' && el.type === 'button') {
        el.value = texto;
      } else if (el.tagName.toLowerCase() === 'button' && el.querySelector('span')) {
        el.querySelector('span').textContent = texto;
      } else {
        el.textContent = texto;
      }
    });

    // Traduz atributo title (data-i18n-title)
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const chave = el.getAttribute('data-i18n-title');
      if (this.dict[chave]) el.title = this.dict[chave][this.idioma] || this.dict[chave]['pt'];
    });

    // Onboarding slide 3 — contém HTML (negrito), usa innerHTML
    ['onb-li1','onb-li2','onb-li3','onb-li4'].forEach((id, i) => {
      const el = document.getElementById(id);
      const key = `ob_slide3_li${i+1}`;
      if (el && this.dict[key]) el.innerHTML = this.dict[key][this.idioma] || this.dict[key]['pt'];
    });

    const langBtn = document.getElementById('lang-toggle');
    if (langBtn) {
      const ptSeg = document.getElementById('lang-pill-pt');
      const itSeg = document.getElementById('lang-pill-it');
      if (ptSeg) ptSeg.classList.toggle('ativo', this.idioma === 'pt');
      if (itSeg) itSeg.classList.toggle('ativo', this.idioma === 'it');
      langBtn.title = this.idioma === 'pt' ? 'Mudar para Italiano' : 'Cambia in Portoghese';
    }
  }
};
