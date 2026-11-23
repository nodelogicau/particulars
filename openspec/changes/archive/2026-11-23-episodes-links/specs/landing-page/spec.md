## ADDED Requirements

### Requirement: Sibling formats are linked once, in the footer
The landing page SHALL link intentions.fyi, episodes.fyi and forgetting.fyi exactly once each, together in a single line in the footer, worded by what each covers (what a person means to do, what happened, and why the family models memory as several kinds). It SHALL NOT add a section for them, and the *Page narrative* order SHALL be unchanged. The page SHALL say nothing about intentions or episodes that the specification's README does not, and every sibling site it links SHALL be listed in the README's *Ecosystem*.

#### Scenario: Siblings linked once
- **WHEN** the landing page is searched for links to intentions.fyi, episodes.fyi and forgetting.fyi
- **THEN** each is found exactly once, all in the footer

#### Scenario: Narrative unchanged
- **WHEN** a visitor scrolls the page reading only headlines, diagrams and captions
- **THEN** the five narrative sections appear in the order *Page narrative* requires, with no section about the sibling formats

#### Scenario: Backed by the README
- **WHEN** the footer's family line is compared with the README
- **THEN** each site it links is listed in *Ecosystem*, and each thing it says about a sibling is stated in *Purpose* or *Ecosystem*
