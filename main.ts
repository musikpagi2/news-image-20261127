// news-image-20261127 — the entry program (Node 22, standard library only).
// The front page lives in the repository as entry.png: a newspaper page
// summing up the world news of Friday 27 November 2026. This program reads
// those bytes and writes them unchanged to /output/entry.png, so the judge
// sees exactly the image the repository holds. The gate accepts a whole PNG
// or JPEG of at most 1 MiB and 1024 by 1024 pixels.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(here, "entry.png");
const target = join(outDir, "entry.png");

const bytes = readFileSync(source);
mkdirSync(outDir, { recursive: true });
writeFileSync(target, bytes);
console.log(`wrote entry.png (${bytes.length} bytes)`);
