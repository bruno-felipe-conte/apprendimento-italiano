import { defineConfig } from 'vite';
import fs from 'node:fs';
import path from 'node:path';

function copyLegacyAssets() {
  return {
    name: 'copy-legacy-assets',
    closeBundle() {
      const distDir = path.resolve(process.cwd(), 'dist');
      if (!fs.existsSync(distDir)) return;

      const toCopyDirs = ['data', 'js', 'wasm', 'icons'];
      for (const dir of toCopyDirs) {
        const srcDir = path.resolve(process.cwd(), dir);
        const targetDir = path.resolve(distDir, dir);
        if (fs.existsSync(srcDir)) {
          fs.cpSync(srcDir, targetDir, { recursive: true, force: true });
        }
      }

      const toCopyFiles = ['sw.js', 'favicon.ico', 'manifest.webmanifest'];
      for (const file of toCopyFiles) {
        const srcFile = path.resolve(process.cwd(), file);
        const targetFile = path.resolve(distDir, file);
        if (fs.existsSync(srcFile)) {
          fs.copyFileSync(srcFile, targetFile);
        }
      }
    }
  };
}

export default defineConfig({
  plugins: [copyLegacyAssets()],
  base: './',
  server: {
    port: 5173,
    open: false,
    cors: true
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: true,
    target: 'es2022',
    rollupOptions: {
      input: {
        main: './index.html'
      }
    }
  }
});
