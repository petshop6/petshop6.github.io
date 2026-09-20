import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// petshop6.com is in the shop's Instagram bio but does not resolve today;
// point the build at whatever host is live with SITE_URL until the domain is set up.
const SITE_URL = process.env.SITE_URL || 'https://petshop6.github.io';

export default defineConfig({
  site: SITE_URL,
  output: 'static',
  trailingSlash: 'never',
  build: { format: 'file' },
  compressHTML: true,
  server: { port: 4328 },
  integrations: [sitemap()],
});
