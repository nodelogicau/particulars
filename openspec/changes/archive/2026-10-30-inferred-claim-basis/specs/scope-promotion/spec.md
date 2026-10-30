## ADDED Requirements

### Requirement: A basis is treated as inputs for disclosure
For the purposes of *Promotion does not cascade to inputs*, *Derived disclosure is warned, not forbidden*, and *Derived disclosure is evaluated from workspace state*, the members of an inferred claim's `basis` SHALL be treated as that claim's inputs. Promoting an inferred claim SHALL NOT promote its basis. Implementations SHOULD warn, and SHALL report `scope_wider_than_inputs`, when an inferred claim's effective scope is wider than the effective scope of any basis member, and SHALL NOT reject the claim on that basis. They SHALL evaluate the condition during validation, when such a claim is created, and when `knowledge_publish` promotes it.

#### Scenario: A shared rule from personal instances
- **WHEN** an inferred claim is asserted `organisation` with a basis of claims asserted `personal`
- **THEN** the implementation reports `scope_wider_than_inputs` naming the narrower basis members, and writes the claim

#### Scenario: Promoting a rule
- **WHEN** an inferred claim is promoted to `public` and its basis members are not
- **THEN** only the claim becomes eligible for a public feed, the condition is reported, and a public consumer receives basis ids it cannot resolve
