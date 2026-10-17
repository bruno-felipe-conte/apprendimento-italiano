import json,re
P='data/grammar.json'
d=json.load(open(P,encoding='utf-8'))
strip=lambda s:re.sub(r'\*+','',s or '').strip()
def cut(s,n=260):
    s=strip(s).replace('\n',' ')
    return s if len(s)<=n else s[:n].rsplit(' ',1)[0]+'…'
ABR=["Antes de qualquer regra, vamos entrar numa cena. {a} Escute como quem está na mesa ao lado, sem tentar entender cada palavra: o ouvido percebe o padrão antes da cabeça.",
"Esqueça o caderno por um instante. {a} Imagine-se na Itália, ouvindo esta cena acontecer ao seu redor.",
"Toda regra nasce de uma conversa de verdade. {a} Então comece pela conversa, e deixe a gramática aparecer sozinha.",
"Vamos começar pela vida e deixar a teoria para depois. {a} Leia, ouça e sinta o ritmo da cena."]
DES=["Reparou em «{it}»? ({pt}) {m} Foi isso que a cena acabou de mostrar sem avisar.",
"Volte à cena e olhe para «{it}» ({pt}). {m} Esse pequeno detalhe é a lição de hoje.",
"Perceba a frase «{it}», que significa «{pt}». {m} Quando você enxerga isso na fala dos outros, a regra deixa de ser decoreba."]
FIM=["Agora você já ouviu, já viu e já entendeu o porquê. {c}",
"Com a cena na cabeça, a regra tem rosto e voz. {c}",
"Guarde isto como quem guarda um segredo de italiano nativo. {c}"]
n=0
for m in d['moduli']:
  for i,l in enumerate(m['lezioni']):
    t=l.get('teoria','') or ''
    cards=l.get('observacao_cards') or []
    cena=None
    if t.startswith('## '):
        parts=re.split(r'\n(?=## )',t,maxsplit=1)
        head=parts[0]; title,_,body=head.partition('\n')
        cena={'titulo':title[3:].strip(),'texto':body.strip(),'origem':'parla_e_scrivi'}
        l['teoria']=parts[1] if len(parts)>1 else ''
    elif cards:
        linhas=['**%s**\n_%s_'%(strip(c['italiano']),strip(c.get('traducao'))) for c in cards[:4]]
        cena={'titulo':'Frases ouvidas por aí','texto':'\n\n'.join(linhas),'origem':'cards'}
    l['cena']=cena
    a=strip(l.get('alerta')) or 'Esta lição aparece em quase toda conversa italiana.'
    c0=cards[0] if cards else {}
    df=l.get('definicao') or {}
    mot=cut(c0.get('motivo') or df.get('conceito') or df.get('causa') or '')
    k=n
    l['fio']={
      'abertura':ABR[k%4].format(a=a),
      'descoberta':(DES[k%3].format(it=strip(c0.get('italiano')),pt=strip(c0.get('traducao')),m=mot) if c0 else ''),
      'fecho':FIM[k%3].format(c=strip(l.get('coda')))
    }
    n+=1
json.dump(d,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print(n)
