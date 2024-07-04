import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// export default defineConfig({
//   plugins: [vue()],
//   server: {
//     proxy: {
//       "/upload": {
//         target: "http://localhost:8000",
//         changeOrigin: true,
//         rewrite: (path) => path.replace(/^\/upload/, ""),
//       },
//     },
//   },
// });

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      "/upload": {
        target: "http://localhost:8080",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/upload/, ""),
      },
      "/signup": {
        target: "http://localhost:8080",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/signup/, ""),
      },
      "/register": {
        target: "http://localhost:8080",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/register/, ""),
      },
      "/login": {
        target: "http://localhost:8080",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/login/, ""),
      },
    },
  },
});
