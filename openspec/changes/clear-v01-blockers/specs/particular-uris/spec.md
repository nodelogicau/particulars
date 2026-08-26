## ADDED Requirements

### Requirement: The urn:dkf: namespace is deliberately unregistered at v0.1
The specification SHALL state that `urn:dkf:` is used as an unregistered URN namespace: its NID syntax conforms to RFC 8141, every minted URN embeds the workspace UUID so collision with any other use of the NID requires a UUID collision, and formal registration — which would change no identifier — MAY be pursued after v0.1. `base-uri` remains the recommended form for publishers.

#### Scenario: An implementer checks the namespace status
- **WHEN** an implementer looks up whether `urn:dkf:` is IANA-registered
- **THEN** the specification says it is not, that this is deliberate, and why it is safe

#### Scenario: Registration changes nothing
- **WHEN** the namespace is later registered
- **THEN** every existing URN remains valid unchanged
