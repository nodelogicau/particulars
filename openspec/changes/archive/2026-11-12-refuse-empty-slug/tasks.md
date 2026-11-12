## 1. Spec

- [x] 1.1 Modify *URI minting convention* in `particular-uris`: an empty slug is refused, nothing written, explicit `uri` required; scenarios for `#`, `東京` with and without a `uri`, and `C 東京`

## 2. README

- [x] 2.1 In *Minting URIs*, state the refusal and why an id fallback and an IRI slug were rejected
- [x] 2.2 Update the `particular_define` row in *MCP Server Tools*
- [x] 2.3 Add a Status entry: a clarification, no format version, existing particulars unaffected (#63)

## 3. Verify and follow up

- [x] 3.1 Run `openspec validate refuse-empty-slug --strict` and fix any findings
- [ ] 3.2 Comment on nodelogicau/particulars-cli#32 that the empty-slug refusal is part of the same CLI work
