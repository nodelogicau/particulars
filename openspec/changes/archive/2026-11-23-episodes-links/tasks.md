## 1. Spec

- [x] 1.1 Modify *The specification states what is outside its scope* in `format-purpose`: episodes is where a log of what happened lives, a claim may cite an episode through `source.document`, the coupling runs one way, and only procedural memory is left open for a separate specification
- [x] 1.2 Add *Sibling formats are linked once, in the footer* to `landing-page`

## 2. README

- [x] 2.1 In *Purpose*, name episodes, state how a claim cites an episode and that the coupling runs one way
- [x] 2.2 In *Ecosystem*, add episodes and episodes.fyi, and add intentions.fyi and forgetting.fyi

## 3. Page

- [x] 3.1 Add the family line to the footer of `docs/index.html`, linking intentions.fyi, episodes.fyi and forgetting.fyi
- [x] 3.2 Check the page still makes no request other than itself, and the narrative sections are unchanged

## 4. Verify

- [x] 4.1 Run `openspec validate episodes-links --strict` and fix any findings
