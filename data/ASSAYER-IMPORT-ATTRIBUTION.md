# Assayer registry import: attribution and eligibility

ChemIsFree includes a normalized subset of public catalogue metadata from [Assayer](https://github.com/yboulaamane/assayer), specifically its [catalogue JSON](https://github.com/yboulaamane/assayer/blob/main/web/catalog.json). The Assayer repository declares the MIT License and identifies copyright © 2026 Yassir Boulaamane.

The supplemental file `assayer_free_registry.json` contains records whose Assayer licence/access field explicitly indicates a recognised open-source licence, an open content/data licence (CC-BY-4.0, CC-BY-SA-4.0 or CC0-1.0), or no-cost access (`free-web`, `free of charge`, or `freeware`). Entries labelled commercial, proprietary, academic-only, not licensed, missing/unclear, `noassertion`, `other`, or `free of charge (with restrictions)` are not imported.

Fourteen overlapping records were excluded because they already exist in the hand-maintained ChemIsFree catalogue. The imported records retain upstream names, descriptions, URLs, stage/tags, licence/access signals, and source identifiers where available. Each imported item identifies Assayer as its catalogue source and links to the official resource.

**Important limitations:** these are registry imports, not a claim that ChemIsFree has individually tested every tool or independently verified current availability, terms, platform support, or maintenance status. A `free-web` / `free of charge` label establishes only the upstream no-cost access claim; it does not itself establish permission to redistribute software or data. Check the resource's official terms before use, redistribution, or commercial work. Named software/content licences remain the responsibility of the upstream project. Imported items are marked `registry-listed` and their status is `unknown` until reviewed.

## Assayer MIT License notice

MIT License

Copyright (c) 2026 Yassir Boulaamane

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
