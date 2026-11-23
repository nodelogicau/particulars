## Why

[episodes.fyi](https://episodes.fyi) is live: the landing page for the [Episodes Format](https://github.com/nodelogicau/episodes), the family's draft format for what happened. episodes.fyi, intentions.fyi and forgetting.fyi all link particulars.fyi, but particulars.fyi links none of them. The README the page is checked against doesn't name episodes either. *Purpose* says a log of what happened is not DKF's job without saying where that log lives, and *Ecosystem* lists intentions and Forgetting but not episodes. Raised as #69.

## What Changes

- **README, *Purpose*:** name episodes as where a log of what happened lives, and say a claim may cite an episode as its source document (`document.ref` is the episode id, `document.author` the episode's standpoint), so *reported from* works across formats. The coupling runs one way: episodes cites nothing in DKF, and DKF validates no episode reference. Episodic memory now has a format, so the "could get a specification of its own" sentence narrows to procedural memory.
- **README, *Ecosystem*:** add episodes and episodes.fyi, and add intentions.fyi and forgetting.fyi beside the repositories already listed, so every sibling link on the page is backed by the README.
- **The page:** one family line in the footer linking intentions.fyi, episodes.fyi and forgetting.fyi, each worded by what it covers rather than by a product pitch. No new section, and the five-part narrative is unchanged.
- **No format version.** No file is read differently and no file stops validating.

## Capabilities

### New Capabilities

_None._

### Modified Capabilities
- `format-purpose`: *The specification states what is outside its scope* names episodes as where episodic memory lives and states the one-way citation. Procedural memory alone is left open for a separate specification.
- `landing-page`: a new requirement, *Sibling formats are linked once, in the footer*.

## Impact

- `README.md`: *Purpose* (the out-of-scope paragraph) and *Ecosystem* in References.
- `docs/index.html`: the footer.
- `openspec/specs/format-purpose`: one requirement modified. `openspec/specs/landing-page`: one requirement added.
- Implementations: none.
