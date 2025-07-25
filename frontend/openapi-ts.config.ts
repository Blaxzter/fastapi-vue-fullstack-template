import { defineConfig } from '@hey-api/openapi-ts'

export default defineConfig({
  input: 'http://localhost:8002/api/v1/openapi.json', // './openapi.json',
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
