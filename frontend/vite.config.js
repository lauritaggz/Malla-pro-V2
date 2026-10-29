import process from "node:process";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  // Base URL — cambiar a "/nombre-repo/" si se despliega en GitHub Pages en subcarpeta
  base: "/",

  build: {
    outDir: "dist",
    // Dividir chunks para mejor caché
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          motion: ["framer-motion"],
          icons: ["lucide-react"],
          pdf: ["pdfjs-dist"],
        },
      },
    },
    // Tamaño de advertencia de chunk
    chunkSizeWarningLimit: 600,
  },

  preview: {
    port: 4173,
    host: true,
  },

  server: {
    port: 5174,
    // Falla en vez de cambiar de puerto: el CORS del backend y los orígenes de Firebase
    // dependen de que sea siempre el 5174.
    strictPort: true,
    host: true,
    // En Docker con la carpeta montada desde Windows/macOS no llegan eventos de archivos:
    // docker-compose.yml activa el sondeo con VITE_USE_POLLING.
    watch: process.env.VITE_USE_POLLING === "true" ? { usePolling: true, interval: 300 } : undefined,
  },

  test: {
    globals: true,
    environment: "node",
    include: ["src/**/*.{test,spec}.{js,jsx}"],
  },
});
