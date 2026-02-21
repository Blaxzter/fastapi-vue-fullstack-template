import { defineConfig } from '@hey-api/openapi-ts'

export default defineConfig({
  input: './openapi.json',
  output: 'src/client',
  plugins: [
    '@hey-api/client-axios',
    {
      name: 'zod',
      metadata: true,
      definitions: true,
      responses: true,
      requests: true,
    },
  ],
})
