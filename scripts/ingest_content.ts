import fs from 'node:fs';
import path from 'node:path';
import {
  TemploSchema,
  StoriaItemSchema,
  DialogoItemSchema,
  CanzoneItemSchema
} from './schemas';

export interface IngestOptions {
  tipo: 'templo' | 'storia' | 'dialogo' | 'canzone';
  caminhoEntrada: string;
  dataDir?: string;
  dryRun?: boolean;
}

export interface IngestResult {
  sucesso: boolean;
  mensagem: string;
  arquivoGerado?: string;
  totalItens?: number;
  erros?: string[];
}

export function ingerirConteudo(options: IngestOptions): IngestResult {
  const dir = options.dataDir || path.resolve(process.cwd(), 'data');

  if (!fs.existsSync(options.caminhoEntrada)) {
    return {
      sucesso: false,
      mensagem: `Arquivo de entrada não encontrado: ${options.caminhoEntrada}`
    };
  }

  let conteudoRaw: string;
  let json: any;

  try {
    conteudoRaw = fs.readFileSync(options.caminhoEntrada, 'utf-8');
    json = JSON.parse(conteudoRaw);
  } catch (err: any) {
    return {
      sucesso: false,
      mensagem: `Falha ao parsear JSON de entrada: ${err.message}`
    };
  }

  if (options.tipo === 'templo') {
    // Normalização preventiva
    if (json.palavras && Array.isArray(json.palavras)) {
      json.palavras = json.palavras.map((p: any, idx: number) => ({
        ...p,
        id: p.id || `t${json.templo}_${String(idx + 1).padStart(3, '0')}`,
        genero: p.genero || null,
        plural: p.plural || null,
        dificuldade: p.dificuldade || 'medio',
        categoria: p.categoria || 'geral'
      }));
    }

    const validacao = TemploSchema.safeParse(json);
    if (!validacao.success) {
      return {
        sucesso: false,
        mensagem: 'Validação de schema do templo falhou',
        erros: validacao.error.issues.map((i) => `[${i.path.join('.')}] ${i.message}`)
      };
    }

    const destino = path.join(dir, `templo-${validacao.data.templo}.json`);

    if (!options.dryRun) {
      fs.writeFileSync(destino, JSON.stringify(validacao.data, null, 2), 'utf-8');
    }

    return {
      sucesso: true,
      mensagem: `Templo ${validacao.data.templo} (${validacao.data.cidade}) ingerido com sucesso!`,
      arquivoGerado: destino,
      totalItens: validacao.data.palavras.length
    };
  }

  if (options.tipo === 'storia') {
    const validacao = StoriaItemSchema.safeParse(json);
    if (!validacao.success) {
      return {
        sucesso: false,
        mensagem: 'Validação de schema de história falhou',
        erros: validacao.error.issues.map((i) => `[${i.path.join('.')}] ${i.message}`)
      };
    }

    const destino = path.join(dir, 'storie.json');
    if (!options.dryRun && fs.existsSync(destino)) {
      const db = JSON.parse(fs.readFileSync(destino, 'utf-8'));
      if (Array.isArray(db.storie)) {
        // Evita duplicata por id
        const idx = db.storie.findIndex((s: any) => s.id === validacao.data.id);
        if (idx >= 0) {
          db.storie[idx] = validacao.data;
        } else {
          db.storie.push(validacao.data);
        }
        fs.writeFileSync(destino, JSON.stringify(db, null, 2), 'utf-8');
      }
    }

    return {
      sucesso: true,
      mensagem: `História '${validacao.data.titulo}' ingerida com sucesso!`,
      arquivoGerado: destino,
      totalItens: validacao.data.testo.length
    };
  }

  return {
    sucesso: false,
    mensagem: `Tipo de conteúdo não suportado: ${options.tipo}`
  };
}

// Execução via CLI
const isMain = process.argv[1] && (
  process.argv[1].endsWith('ingest_content.ts') || 
  process.argv[1].endsWith('ingest_content.js')
);

if (isMain) {
  const args = process.argv.slice(2);
  const tipo = (args[0] || 'templo') as any;
  const arquivo = args[1];

  if (!arquivo) {
    console.error('Uso: npx vite-node scripts/ingest_content.ts <tipo: templo|storia> <caminho_arquivo.json>');
    process.exit(1);
  }

  const res = ingerirConteudo({ tipo, caminhoEntrada: arquivo });
  if (res.sucesso) {
    console.log(`✅ [Ingestão Concluída] ${res.mensagem}`);
    if (res.arquivoGerado) console.log(`📁 Destino: ${res.arquivoGerado}`);
    process.exit(0);
  } else {
    console.error(`❌ [Falha na Ingestão] ${res.mensagem}`);
    res.erros?.forEach((e) => console.error(`   - ${e}`));
    process.exit(1);
  }
}
