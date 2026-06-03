import json
import os

t24_add = [
    ('processore', 'processador', 'hardware', 'Un processore molto veloce.', 'Um processador muito rápido.', '/protʃesˈsore/', 'm', 'processori'),
    ('scheda madre', 'placa-mãe', 'hardware', 'La scheda madre del computer.', 'A placa-mãe do computador.', '/ˈskɛda ˈmadre/', 'f', 'schede madri'),
    ('videogioco', 'videogame', 'software', 'Gioca sempre a quel videogioco.', 'Ele sempre joga aquele videogame.', '/videoˈdʒɔko/', 'm', 'videogiochi'),
    ('cuffiette', 'fones (pequenos)', 'hardware', 'Le cuffiette senza fili.', 'Os fones de ouvido sem fio.', '/kufˈfjette/', 'f', 'cuffiette'),
    ('spina', 'plugue', 'hardware', 'Inserire la spina nella presa.', 'Inserir o plugue na tomada.', '/ˈspina/', 'f', 'spine'),
    ('presa', 'tomada', 'hardware', 'La presa di corrente.', 'A tomada elétrica.', '/ˈpreza/', 'f', 'prese'),
    ('dispositivo', 'dispositivo', 'hardware', 'Associare il dispositivo Bluetooth.', 'Parear o dispositivo Bluetooth.', '/dispoziˈtivo/', 'm', 'dispositivi'),
    ('penna USB', 'pendrive', 'hardware', 'Salva tutto sulla penna USB.', 'Salve tudo no pendrive.', '/ˈpenna uesseˈbi/', 'f', 'penne USB'),
    ('algoritmo', 'algoritmo', 'software', 'Un algoritmo complesso.', 'Um algoritmo complexo.', '/alɡoˈritmo/', 'm', 'algoritmi'),
    ('connesso', 'conectado', 'reti', 'Ora sei connesso alla rete.', 'Agora você está conectado à rede.', '/konˈnesso/', 'm', 'connessi'),
    ('disconnesso', 'desconectado', 'reti', 'Il server risulta disconnesso.', 'O servidor consta como desconectado.', '/diskonˈnesso/', 'm', 'disconnessi'),
    ('blocco', 'bloqueio/travamento', 'software', 'Il computer ha avuto un blocco.', 'O computador travou.', '/ˈblɔkko/', 'm', 'blocchi'),
    ('crash', 'falha geral', 'software', 'Il sistema ha subito un crash.', 'O sistema sofreu uma falha geral.', '/krɛʃ/', 'm', 'crash'),
    ('browser', 'navegador', 'software', 'Quale browser usi per navigare?', 'Qual navegador você usa?', '/ˈbrauzer/', 'm', 'browser'),
    ('homepage', 'página inicial', 'reti', 'Imposta la homepage su Google.', 'Defina a página inicial como Google.', '/homˈpeidʒ/', 'f', 'homepage'),
    ('app', 'app', 'software', 'Scarica l\'app dallo store.', 'Baixe o app da loja.', '/ap/', 'f', 'app'),
    ('notiziario', 'feed de notícias', 'social', 'Scorri il notiziario.', 'Role o feed de notícias.', '/notitˈtsjarjo/', 'm', 'notiziari'),
    ('cavo di rete', 'cabo de rede', 'hardware', 'Attacca il cavo di rete al pc.', 'Conecte o cabo de rede ao pc.', '/ˈkavo di ˈrete/', 'm', 'cavi di rete'),
    ('backup', 'backup', 'software', 'Fai sempre un backup dei dati.', 'Faça sempre um backup dos dados.', '/ˈbɛkap/', 'm', 'backup'),
    ('streaming', 'streaming', 'reti', 'Guardo film in streaming.', 'Assisto a filmes em streaming.', '/ˈstrimiŋ/', 'm', 'streaming')
]

t25_add = [
    ('profumeria', 'perfumaria', 'luoghi', 'Andiamo in profumeria a comprare un regalo.', 'Vamos à perfumaria comprar um presente.', '/profumeˈria/', 'f', 'profumerie'),
    ('gioielleria', 'joalheria', 'luoghi', 'Ha comprato l\'anello in gioielleria.', 'Comprou o anel na joalheria.', '/dʒojelleˈria/', 'f', 'gioiellerie'),
    ('edicola', 'banca de jornal', 'luoghi', 'Compro il giornale in edicola.', 'Compro o jornal na banca.', '/eˈdikola/', 'f', 'edicole'),
    ('tabaccheria', 'tabacaria/banca', 'luoghi', 'Comprare i biglietti in tabaccheria.', 'Comprar as passagens na tabacaria.', '/tabakkeˈria/', 'f', 'tabaccherie'),
    ('pasticceria', 'confeitaria', 'luoghi', 'Prendiamo dei dolci in pasticceria.', 'Vamos pegar uns doces na confeitaria.', '/pastittʃeˈria/', 'f', 'pasticcerie'),
    ('gelateria', 'sorveteria', 'luoghi', 'Una buona gelateria artigianale.', 'Uma boa sorveteria artesanal.', '/dʒelateˈria/', 'f', 'gelaterie'),
    ('cartoleria', 'papelaria', 'luoghi', 'Quaderni e penne in cartoleria.', 'Cadernos e canetas na papelaria.', '/kartoleˈria/', 'f', 'cartolerie'),
    ('ferramenta', 'loja de ferragens', 'luoghi', 'Comprare i chiodi in ferramenta.', 'Comprar pregos na loja de ferragens.', '/ferraˈmenta/', 'f', 'ferramenta'),
    ('spesa online', 'compras on-line', 'oggetti', 'Oggi facciamo la spesa online.', 'Hoje fazemos compras on-line.', '/ˈspeza onˈlain/', 'f', 'spese online'),
    ('spedizione', 'frete/envio', 'oggetti', 'La spedizione è gratuita.', 'O frete é grátis.', '/speditˈtsjone/', 'f', 'spedizioni'),
    ('corriere', 'entregador', 'persone', 'Il corriere ha suonato.', 'O entregador tocou a campainha.', '/korˈrjɛre/', 'm', 'corrieri'),
    ('pacco', 'pacote', 'oggetti', 'Ho ricevuto un grosso pacco.', 'Recebi um pacote grande.', '/ˈpakko/', 'm', 'pacchi'),
    ('imballaggio', 'embalagem', 'oggetti', 'Un imballaggio molto resistente.', 'Uma embalagem muito resistente.', '/imbalˈladdʒo/', 'm', 'imballaggi'),
    ('consegna', 'entrega', 'oggetti', 'Pagamento alla consegna.', 'Pagamento na entrega.', '/konˈseɲɲa/', 'f', 'consegne'),
    ('reso', 'devolução', 'oggetti', 'Devo fare un reso per la maglia.', 'Preciso fazer uma devolução da blusa.', '/ˈrezo/', 'm', 'resi'),
    ('ricevuta', 'recibo', 'denaro', 'Ecco la sua ricevuta.', 'Aqui está o seu recibo.', "/ritʃeˈvuta/", 'f', 'ricevute'),
    ('titolare', 'dono (da loja)', 'persone', 'Voglio parlare con il titolare.', 'Quero falar com o dono.', '/titoˈlare/', 'm/f', 'titolari'),
    ('budget', 'orçamento (budget)', 'denaro', 'Non rientra nel mio budget.', 'Não cabe no meu orçamento.', '/ˈbadʒɛt/', 'm', 'budget')
]

def w(tid, it, pt, cat, ex_it, ex_pt, ipa='', gen=None, pl=None):
    return {
        'id': tid, 'italiano': it, 'portugues': pt, 'genero': gen, 'plural': pl,
        'exemplo': ex_it, 'exemplo_pt': ex_pt, 'categoria': cat, 'dificuldade': 'medio', 'audio_ipa': ipa
    }

for temp_num, words_to_add in [(24, t24_add), (25, t25_add)]:
    path = f'c:/Users/bruno/Documents/italian-learning-app-pro/data/templo-{temp_num}.json'
    with open(path, 'r', encoding='utf-8') as f:
        obj = json.load(f)

    current_count = len(obj['palavras'])
    for i, (it, pt, cat, ex_it, ex_pt, ipa, gen, pl) in enumerate(words_to_add, current_count + 1):
        tid = f't{temp_num}_{i:03d}'
        obj['palavras'].append(w(tid, it, pt, cat, ex_it, ex_pt, ipa, gen, pl))

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

    print(f'T{temp_num} now has {len(obj["palavras"])} parole')
