## ADDED Requirements

### Requirement: A workspace may carry a conventions document for agents
A workspace MAY carry a conventions document: prose addressed to agents that write into the workspace, stating what only the workspace can — its topic vocabulary, retired tags, ingestion policy, scope practice. The document SHALL be `dkf.md` at the workspace root, or the file named by `workspace.conventions` in `dkf.yaml`, which SHALL be a relative path inside the workspace. The specification SHALL NOT constrain the document's content. No reader or validator SHALL derive behaviour from it, and it SHALL NOT relax any requirement of this specification. The specification SHALL note that what the format models structurally — authors as particulars, topics on the index — belongs there rather than in the document.

#### Scenario: Default document
- **WHEN** `dkf.md` exists at the workspace root and `dkf.yaml` has no `workspace.conventions`
- **THEN** `dkf.md` is the workspace's conventions document

#### Scenario: Configured document
- **WHEN** `dkf.yaml` has `workspace.conventions: TOPICS.md`
- **THEN** `TOPICS.md` is the workspace's conventions document, and a `dkf.md` at the root, if present, is not

#### Scenario: No document
- **WHEN** `dkf.yaml` has no `workspace.conventions` and no `dkf.md` exists
- **THEN** the workspace has no conventions document, and that is not a warning

#### Scenario: The document does not change how a file is read
- **WHEN** a conventions document says that held claims in this workspace carry a confidence
- **THEN** a validator still rejects a `held` claim carrying `confidence`, and a claim file is interpreted exactly as it would be without the document

### Requirement: An MCP server delivers the conventions document
An MCP server bound to a workspace that carries a conventions document SHOULD include the document's content in its `initialize` instructions, after its generic guidance, under a heading naming the file. A prompt the server offers carrying its discipline SHOULD carry the same text. The server MAY additionally expose the document as a resource. A configured document that cannot be read SHALL be reported as a warning and omitted; it SHALL NOT fail startup.

#### Scenario: Delivered with the instructions
- **WHEN** the workspace root holds `dkf.md` and a client initialises
- **THEN** `instructions` contains a heading naming `dkf.md` followed by the file's content, after the server's generic guidance

#### Scenario: Delivered under the configured name
- **WHEN** `dkf.yaml` has `workspace.conventions: TOPICS.md` and a client initialises
- **THEN** the heading names `TOPICS.md`

#### Scenario: Prompt carries the same text
- **WHEN** a client gets the server's discipline prompt
- **THEN** its text contains the conventions section that the instructions contain

#### Scenario: Configured but unreadable
- **WHEN** `workspace.conventions` names a file that does not exist
- **THEN** the server starts, warns naming the file, and its instructions contain no conventions section

### Requirement: Truncation has a floor and is announced
An implementation that limits how much of the document it delivers SHALL deliver at least the first 16 KiB of its UTF-8 encoding, SHALL truncate only on a character boundary, and SHALL append a note stating that the text was truncated and naming the file.

#### Scenario: Within the floor
- **WHEN** the document is 12 KiB
- **THEN** it is delivered in full

#### Scenario: Over the floor
- **WHEN** the document is 40 KiB
- **THEN** at least its first 16 KiB are delivered, the cut falls between characters, and a note names the file as truncated

#### Scenario: A larger budget is conformant
- **WHEN** an implementation delivers documents up to 64 KiB before truncating
- **THEN** it conforms

### Requirement: The tool surface teaches the register
The descriptions of `claim_assert` and `particular_define` SHALL state that the subject of a claim is the thing in the world the fact is about, never the document or feed it was read in, and that what was read belongs in `source.document`. `particular_define`'s examples of global URIs SHALL be identities — a person, a project — and SHALL NOT be reading matter. The requirement pins the presence of the register, not its wording.

#### Scenario: Assert-time register present
- **WHEN** a client lists tools
- **THEN** `claim_assert`'s description states that the subject is the thing in the world and that what was read belongs in `source.document`

#### Scenario: Define does not invite document particulars
- **WHEN** a client reads `particular_define`'s description
- **THEN** its URI examples name identities, not articles or feeds
