import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/** Rehber: short pet-care pieces, text from the shop's own Instagram posts. */
const rehber = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/rehber' }),
  schema: ({ image }) =>
    z.object({
      baslik: z.string(),
      ozet: z.string(),
      tarih: z.coerce.date(),
      kaynak: z.string().url(),
      kaynakNot: z.string().optional(),
      gorsel: image(),
      gorselAlt: z.string(),
      etiket: z.enum(['kedi', 'kopek', 'sokak']),
    }),
});

export const collections = { rehber };
