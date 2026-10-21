import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  TemploSchema,
  StorieFileSchema,
  DialoghiFileSchema,
  CanzoniFileSchema
} from './schemas';

export interface RelatorioValidacao {
  sucesso: boolean;
  totalArquivos: number;
  totalPalavras: number;
  erros: { arquivo: string; mensagem: string }[];
  avisos: { arquivo: string; mensagem: string }[];
}

export function validarTodosConteudos(dataDir?: string): RelatorioValidacao {
  const dir = dataDir || path.resolve(process.cwd(), 'data');
  const relatorio: RelatorioValidacao = {
    sucesso: true,
    totalArquivos: 0,
    totalPalavras: 0,
    erros: [],
    avisos: []
  };

  const wordIdSet = new Set<string>();

  // 1. Validar Templos
  for (let i = 1; i <= 51; i++) {
    const filename = `templo-${i}.json`;
    const filepath = path.join(dir, filename);

    if (!fs.existsSync(filepath)) {
      relatorio.avisos.push({ arquivo: filename, mensagem: 'Arquivo não encontrado' });
      continue;
    }

    relatorio.totalArquivos++;
    try {
      const raw = fs.readFileSync(filepath, 'utf-8');
      const json = JSON.parse(raw);
      const parsed = TemploSchema.safeParse(json);

      if (!parsed.success) {
        relatorio.sucesso = false;
        parsed.error.issues.forEach((err) => {
          relatorio.erros.push({
            arquivo: filename,
            mensagem: `[${err.path.join('.')}] ${err.message}`
          });
        });
      } else {
        relatorio.totalPalavras += parsed.data.palavras.length;
        for (const p of parsed.data.palavras) {
          if (wordIdSet.has(p.id)) {
            relatorio.avisos.push({
              arquivo: filename,
              mensagem: `ID de palavra duplicado detectado: ${p.id}`
            });
          }
          wordIdSet.add(p.id);
        }
      }
    } catch (err: any) {
      relatorio.sucesso = false;
      relatorio.erros.push({ arquivo: filename, mensagem: `JSON malformado: ${err.message}` });
    }
  }

  // 2. Validar storie.json
  const storiePath = path.join(dir, 'storie.json');
  if (fs.existsSync(storiePath)) {
    relatorio.totalArquivos++;
    try {
      const raw = fs.readFileSync(storiePath, 'utf-8');
      const json = JSON.parse(raw);
      const parsed = StorieFileSchema.safeParse(json);
      if (!parsed.success) {
        relatorio.sucesso = false;
        parsed.error.issues.slice(0, 10).forEach((err) => {
          relatorio.erros.push({
            arquivo: 'storie.json',
            mensagem: `[${err.path.join('.')}] ${err.message}`
          });
        });
      }
    } catch (err: any) {
      relatorio.sucesso = false;
      relatorio.erros.push({ arquivo: 'storie.json', mensagem: `Erro de parsing: ${err.message}` });
    }
  }

  // 3. Validar dialogi.json
  const dialogiPath = path.join(dir, 'dialogi.json');
  if (fs.existsSync(dialogiPath)) {
    relatorio.totalArquivos++;
    try {
      const raw = fs.readFileSync(dialogiPath, 'utf-8');
      const json = JSON.parse(raw);
      const parsed = DialoghiFileSchema.safeParse(json);
      if (!parsed.success) {
        relatorio.sucesso = false;
        parsed.error.issues.slice(0, 10).forEach((err) => {
          relatorio.erros.push({
            arquivo: 'dialogi.json',
            mensagem: `[${err.path.join('.')}] ${err.message}`
          });
        });
      }
    } catch (err: any) {
      relatorio.sucesso = false;
      relatorio.erros.push({ arquivo: 'dialogi.json', mensagem: `Erro de parsing: ${err.message}` });
    }
  }

  // 4. Validar canzoni.json
  const canzoniPath = path.join(dir, 'canzoni.json');
  if (fs.existsSync(canzoniPath)) {
    relatorio.totalArquivos++;
    try {
      const raw = fs.readFileSync(canzoniPath, 'utf-8');
      const json = JSON.parse(raw);
      const parsed = CanzoniFileSchema.safeParse(json);
      if (!parsed.success) {
        relatorio.sucesso = false;
        parsed.error.issues.slice(0, 10).forEach((err) => {
          relatorio.erros.push({
            arquivo: 'canzoni.json',
            mensagem: `[${err.path.join('.')}] ${err.message}`
          });
        });
      }
    } catch (err: any) {
      relatorio.sucesso = false;
      relatorio.erros.push({ arquivo: 'canzoni.json', mensagem: `Erro de parsing: ${err.message}` });
    }
  }

  return relatorio;
}

// Execução via CLI direta
const isMain = process.argv[1] && (
  process.argv[1].endsWith('validate_content.ts') || 
  process.argv[1].endsWith('validate_content.js')
);

if (isMain) {
  console.log('🔍 [Content Pipeline] Iniciando validação dos dados mestres...');
  const relatorio = validarTodosConteudos();

  console.log(`📊 Arquivos analisados: ${relatorio.totalArquivos}`);
  console.log(`📖 Total de palavras indexadas em templos: ${relatorio.totalPalavras}`);

  if (relatorio.avisos.length > 0) {
    console.warn(`⚠️ Avisos (${relatorio.avisos.length}):`);
    relatorio.avisos.slice(0, 5).forEach((a) => console.warn(`   - [${a.arquivo}] ${a.mensagem}`));
  }

  if (relatorio.sucesso) {
    console.log('✅ [Content Pipeline] Todos os conteúdos foram aprovados com sucesso!');
    process.exit(0);
  } else {
    console.error(`❌ [Content Pipeline] Falha na validação (${relatorio.erros.length} erros encontrados):`);
    relatorio.erros.forEach((e) => console.error(`   - [${e.arquivo}] ${e.mensagem}`));
    process.exit(1);
  }
}
