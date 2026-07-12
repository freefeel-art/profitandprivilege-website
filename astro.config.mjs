// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import cloudflare from '@astrojs/cloudflare';

// https://astro.build/config
export default defineConfig({
  site: 'https://olsp.profitandprivilege.com',
  integrations: [
    sitemap(),
  ],
  adapter: cloudflare({ prerenderEnvironment: "node" }),
});
