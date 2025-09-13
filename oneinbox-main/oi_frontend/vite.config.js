import path from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react'
import proxyOptions from './proxyOptions';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [react()],
	server: {
		host: "0.0.0.0",
		port: 8080,
		proxy: proxyOptions
	// 	proxy: {
    //   "/api": {
    //     target: "http://oneinbox.localhost:9002/", // Replace with your Frappe backend URL
    //     changeOrigin: true,
    //   },
	// }
	},
	resolve: {
		extensions: [".js", ".jsx", ".ts", ".tsx"],
		alias: {
			'@': path.resolve(__dirname, 'src')
		}
	},
	build: {
		outDir: '../oneinbox/public/oi_frontend',
		emptyOutDir: true,
		target: 'es2015',
	},
});
