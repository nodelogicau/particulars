## 1. Signing basis

- [ ] 1.1 Rewrite the signing paragraph in Trust and Provenance: payload is the data model minus `retracted` and `signature`, canonicalised per RFC 8785; suites remain reserved
- [ ] 1.2 State the mapping rules (textual fields are strings, `confidence` a number, no anchors/aliases/non-string keys)
- [ ] 1.3 Remove the order-mandatory-when-signed sentence, and the "prerequisite for signing" clause from Field order, keeping the diff rationale

## 2. Discovery

- [ ] 2.1 Make the Public Discovery section normative: required/optional manifest keys, site-root path resolution, unknown keys ignored
- [ ] 2.2 State fetchability at feed path + id, index-as-enumeration-may-lag, and the public-effective-scope rule with the promotions-feed verification note
- [ ] 2.3 State that crawler behaviour is out of scope, deliberately

## 3. urn:dkf:

- [ ] 3.1 Replace the "registration is deferred" sentence with the deliberate-unregistered statement and the collision argument

## 4. Status

- [ ] 4.1 Rewrite Status: nothing open before v0.1; declaring it is the maintainer's act

## 5. Review and close out

- [ ] 5.1 Post the proposal on a particulars-cli issue for review before applying
- [ ] 5.2 After review, apply; verify each scenario against README; confirm MODIFIED headers match baselines
- [ ] 5.3 Archive; capture in the knowledge workspace that the blockers are cleared
