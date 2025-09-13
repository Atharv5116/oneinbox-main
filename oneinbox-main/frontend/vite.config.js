import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import path from 'path'
import frappeui from 'frappe-ui/vite'
// import { VitePWA } from 'vite-plugin-pwa'

// import { getProxyOptions } from 'frappe-ui/src/utils/vite-dev-server'
// import { webserver_port } from '../../../sites/common_site_config.json'
import proxyOptions from './proxyOptions.js';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    frappeui(),
    vue({
      script: {
        propsDestructure: true,
      },
    }),
    vueJsx(),
    {
      name: 'transform-index.html',
      transformIndexHtml(html, context) {
        if (!context.server) {
          return html.replace(
            /<\/body>/,
            `
            <script>
                {% for key in boot %}
                window["{{ key }}"] = {{ boot[key] | tojson }};
                {% endfor %}
            </script>
            </body>
            `
          )
        }
        return html
      },
    },
  ],
  server: {
    host: "0.0.0.0",
    port: 8080,
    proxy: proxyOptions,
    ignored: ['**/node_modules/**', '**/.git/**', '**/public/**'],
    usePolling: true
        // proxy: getProxyOptions({ port: webserver_port }),
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  build: {
    outDir: '../oneinbox/public/frontend',
    emptyOutDir: true,
    commonjsOptions: {
      include: [/tailwind.config.js/, /node_modules/],
    },
    sourcemap: true,
  },
  // build: {
  //   outDir: `../${path.basename(path.resolve('..'))}/public/frontend`,
  //   emptyOutDir: true,
  //   target: 'es2015',
  // },
  optimizeDeps: {
    include: ['frappe-ui > feather-icons', 'showdown', 'tailwind.config.js', 'engine.io-client', 'prosemirror-state'],
  },
})
