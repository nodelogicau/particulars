## MODIFIED Requirements

### Requirement: The specification states what is outside its scope
The *Purpose* section SHALL state that episodic memory and procedural memory are outside the format: that an event may be a particular with claims made about it while a log of episodes is not the format's job, and that know-how, the habits and practised skills a person exercises rather than recalls, is not the format's job either. It SHALL describe procedural memory as a person's know-how and SHALL NOT define it as how an agent does things. It SHALL state that a harness's own know-how lives in skill files and prompts, and that the conventions document addresses an agent without constraining anything. It SHALL leave open that either memory may be addressed by a separate specification. It SHALL point to the Forgetting whitepaper for why the family models memory as several kinds, and the *References* section SHALL list the whitepaper.

#### Scenario: An event recorded as knowledge
- **WHEN** a reader wants to record that a certificate was renewed on a given day
- **THEN** *Purpose* tells them the event may be a particular with a claim about it, and that DKF is not a log of episodes

#### Scenario: Procedural memory described for the person
- **WHEN** a reader reads how *Purpose* describes procedural memory
- **THEN** it is described as a person's know-how, habits and practised skills, and not as how an agent does things

#### Scenario: A procedure for an agent
- **WHEN** a reader asks whether DKF stores how an agent should perform a task
- **THEN** *Purpose* tells them that is a harness's own know-how, held in skill files and prompts outside the format

#### Scenario: Future specifications not foreclosed
- **WHEN** a reader reads the scope statement
- **THEN** it does not say episodic or procedural memory will never be specified

#### Scenario: The fuller argument
- **WHEN** a reader wants to know why the family models memory as several kinds
- **THEN** *Purpose* links the Forgetting whitepaper, and *References* lists it
