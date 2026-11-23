## MODIFIED Requirements

### Requirement: The specification states what is outside its scope
The *Purpose* section SHALL state that episodic memory and procedural memory are outside the format: that an event may be a particular with claims made about it while a log of episodes is not the format's job, and that know-how, the habits and practised skills a person exercises rather than recalls, is not the format's job either. It SHALL name the episodes format as where a log of what happened lives, and SHALL state that a claim may cite an episode as its source document, with the episode's id as `document.ref` and the episode's standpoint as `document.author`. It SHALL state that the coupling runs one way: episodes cites nothing in DKF, and no DKF validator resolves an episode reference. It SHALL describe procedural memory as a person's know-how and SHALL NOT define it as how an agent does things. It SHALL state that a harness's own know-how lives in skill files and prompts, and that the conventions document addresses an agent without constraining anything. It SHALL leave open that procedural memory may be addressed by a separate specification. It SHALL point to the Forgetting whitepaper for why the family models memory as several kinds, and the *References* section SHALL list the whitepaper and the episodes format.

#### Scenario: An event recorded as knowledge
- **WHEN** a reader wants to record that a certificate was renewed on a given day
- **THEN** *Purpose* tells them the event may be a particular with a claim about it, that DKF is not a log of episodes, and that such a log lives in the episodes format

#### Scenario: A claim citing an episode
- **WHEN** a reader wants a claim to rest on something said in a recorded conversation
- **THEN** *Purpose* tells them the claim may cite the episode as its source document, with the episode id as `document.ref` and its standpoint as `document.author`

#### Scenario: The coupling runs one way
- **WHEN** a reader reads how DKF relates to episodes
- **THEN** nothing in it implies that episodes cites DKF, or that a DKF validator resolves an episode reference

#### Scenario: Procedural memory described for the person
- **WHEN** a reader reads how *Purpose* describes procedural memory
- **THEN** it is described as a person's know-how, habits and practised skills, and not as how an agent does things

#### Scenario: A procedure for an agent
- **WHEN** a reader asks whether DKF stores how an agent should perform a task
- **THEN** *Purpose* tells them that is a harness's own know-how, held in skill files and prompts outside the format

#### Scenario: Future specifications not foreclosed
- **WHEN** a reader reads the scope statement
- **THEN** it does not say procedural memory will never be specified

#### Scenario: The fuller argument
- **WHEN** a reader wants to know why the family models memory as several kinds
- **THEN** *Purpose* links the Forgetting whitepaper, and *References* lists it
