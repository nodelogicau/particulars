## 1. The principle and the layout, in the README

- [x] 1.1 Add a short section before File Layout stating the bounded-working-set principle and the numbers behind it: the 105k-entry parse at 700 MB, the flat-directory git tree, the thousand-file listing; that history is unbounded by design and per-operation cost is not
- [x] 1.2 Replace the File Layout tree with the sharded shape (`claims/2026-09/clm_….yaml`, every type directory, `index/2026-08.yaml` beside `index.yaml`), and show the flat `dkf/0.1` tree beneath it as the legacy layout
- [x] 1.3 Add a `### Sharding` subsection: the path is derived from the id's minting month in UTC and nothing else; why the id and not `timestamp`; why month and not a hex prefix; what "sealed" means and the one exception (a `retracted` block appended); the clock-skew case reported by the drift check
- [x] 1.4 Change `format: dkf/0.1` to `dkf/0.2` in every example, and in the `dkf.yaml` section add that a reader refuses a version it does not implement and reads both layouts by the declared version; say plainly that a `dkf/0.1` reader written before this rule may misread, that one such reader exists and is updated, and that no workspace is obliged to migrate

## 2. The index, in the README

- [x] 2.1 Rewrite the `index.yaml` section: root with `segments`, `entries` for the current month, `retracted` tombstones; a segment per sealed month at `index/<YYYY-MM>.yaml`; the current month is the month of the newest id, so a rebuild is a function of the files
- [x] 2.2 Say why retraction moved from an entry flag to a list: it was the one mutable field, and moving it makes a sealed segment byte-immutable, which lets git leave it alone and a remote consumer cache it forever and poll only the root
- [x] 2.3 Update the drift-check paragraph: per document, tombstone list compared by id, missing or extra segment reported; the MAY-field tolerances unchanged
- [x] 2.4 Add a `### Migration` note: move each file to its derived path, regenerate the index, rewrite `format`; nothing any signature covers changes; git sees renames

## 3. Public discovery, in the README

- [x] 3.1 Update the fetch-path sentence: `<YYYY-MM>/<id>.yaml` for a `dkf/0.2` publisher, the format taken from the index; segment paths resolve against the index's URL; the manifest is unchanged

## 4. Close out

- [x] 4.1 Verify each scenario across the five delta specs is answered by a normative sentence in README.md, including the deterministic-rebuild, wrong-month-file, refused-version, and cached-segment scenarios
- [x] 4.2 Confirm every MODIFIED block copies its baseline requirement text in full with every pre-existing scenario retained; confirm the `workspace-layout` capability has at least one scenario per requirement
- [x] 4.3 Reread the canonical-serialisation and object-identifiers specs and confirm neither needs a delta: paths are not in the payload, and the minting-time rule already says what the shard relies on
- [x] 4.4 Filed as particulars-cli#11: read both layouts by declared format; refuse an unimplemented version by name; `init` writes `dkf/0.2`; a `migrate` verb; `index` and `index --check` per segment with the tombstone list; drop `retracted` from entry comparison; fetch-path derivation in any feed code
- [ ] 4.5 Migrate particulars-knowledge in one commit once a CLI reads `dkf/0.2`, and pin its CI to that version; record the change there and qualify the 2026-08-26 "derived cache" belief rather than reverse it
