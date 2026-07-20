import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

const site = process.env.SITE_URL || 'https://visitbulharsko.cz';
const base = process.env.BASE_PATH || '/';

export default defineConfig({
  site,
  base,
  integrations: [tailwind()],
  output: 'static',
  trailingSlash: 'always',
});
