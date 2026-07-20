import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://visitbulharsko.cz',
  integrations: [tailwind()],
  output: 'static',
  trailingSlash: 'always',
});
