## 1. References

- [x] 1.1 Inventory: from the README text alone, list every standard, identity scheme, protocol, idea, and external artefact a sentence leans on; confirm the list against D1 and admit nothing the text does not use
- [x] 1.2 Add *References* after *Contributing* and before *License*, in the intentions form: bold group labels, middle-dot-separated entries, a link on each standard, prose for conceptual sources, every entry naming what it backs
- [x] 1.3 *Standards borrowed as grammars*: RFC 9562 UUID version 7 for ids; RFC 3339 timestamps; RFC 8785 JSON Canonicalization Scheme for the signed payload; RFC 8141 URN syntax for `urn:dkf:`; YAML 1.2 as the file format and the reason the typed-data-model rule exists; SHA-256 (FIPS 180-4) as the document hash writers write
- [x] 1.4 *Identity schemes admitted as author URIs*: ORCID; W3C Decentralized Identifiers, naming it also as the identity the reserved signature would bind; a GitHub profile URL; stated as examples, not requirements
- [x] 1.5 *Protocol*: the Model Context Protocol, against which the tool surface and *What the server tells the model* are defined
- [x] 1.6 *Conceptual sources*: Hegel on *Aufhebung* behind synthesis carrying its inputs; Fichte for the thesis–antithesis–synthesis triad as the README uses it; Chalybäus for attaching that triad to Hegel; Page and Brin, PageRank, behind citation weight — verify the Fichte and Chalybäus attributions against primary sources before landing and word the entry to claim no more than they support
- [x] 1.7 *Ecosystem*: particulars-cli as the reference implementation; particulars.fyi as the visual introduction; intentions as the format that composes with this one for the prospective layer
- [x] 1.8 Leave every inline citation as it is; References carries the links and the reasons, and the inline mentions carry the point of use

## 2. Timestamps

- [x] 2.1 In *Identifiers*, after the paragraph distinguishing the minting instant from the assertion `timestamp`, state the grammar: every timestamp field is an RFC 3339 `date-time`; writers write UTC with `Z` at seconds precision; readers accept any RFC 3339 form; comparison is as instants, with the `09:02:00Z` versus `10:00:00+02:00` example showing why string comparison is wrong; the month a timestamp falls in is its UTC month
- [x] 2.2 In *Sharding*, where a retraction's month is where its `timestamp` falls, add that the month is the UTC month of the instant, with `2026-09-01T00:30:00+02:00` as an August retraction
- [x] 2.3 In *Trust and Provenance*, give "the string this specification requires" its referent: the instant in UTC with `Z`, a fractional second only when non-zero and without trailing zeros, so an offset form and its UTC form sign identically
- [x] 2.4 Delta spec: the ADDED requirement in `canonical-serialisation` with scenarios for writing, reading an offset form, a month at a boundary, one payload from two forms, and ordering across forms

## 3. Close out

- [x] 3.1 Verify each scenario in the delta spec is answered by a normative sentence in README.md
- [x] 3.2 Confirm the ADDED block introduces no term the baseline `canonical-serialisation` spec does not already use, and that `workspace-layout` and `index-manifest` need no edit to inherit the UTC month rule — confirmed 2026-09-20: the block's only new vocabulary (`date-time`, instant, designator, fractional second) is RFC 3339's own, named in the sentence that uses it; `workspace-layout` and `index-manifest` say where a timestamp "falls" and inherit the UTC month without edit
- [x] 3.3 In particulars-cli, confirm that retraction month derivation and the payload builder both take the UTC instant from `ParseTime` and not the string as written; open an issue only if either does not — confirmed 2026-09-20: the CLI has not yet implemented sharding or the signed payload (no month-derivation or payload code exists); `Retracted.Timestamp` is a `time.Time` populated by `ParseTime`, which returns UTC, so any month derived from it will be the UTC month by construction; no issue opened
- [x] 3.4 Record in particulars-knowledge: the timestamp grammar was unstated from the first draft through v0.1 and past it, and was found by writing the References section; the pattern worth keeping is that the inventory of borrowings is a check on the spec, not decoration — recorded 2026-09-20 in particulars-knowledge#40 on branch knowledge/references-section as clm_01a0bbda-0265-71f7-809c-acfc3e06db63 (the gap and the requirement) and clm_01a0bbda-0294-77fa-859f-d5582c85064f (found by the inventory)
