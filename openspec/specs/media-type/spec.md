# Media Type Specification

## Purpose

Defines the `application/dkf+yaml` media type for every DKF document — objects, records, index documents and the discovery manifest — with no parameters, UTF-8 encoding, consumer tolerance of generic YAML and text labels, and the RFC 6838 registration template it is prepared for.

## Requirements

### Requirement: DKF documents have one media type
The specification SHALL define the media type `application/dkf+yaml`, under the `+yaml` structured suffix of RFC 9512, for every document it defines: object and record files, index documents (root, sealed segments and `index/legacy.yaml`), and the public discovery manifest. The media type SHALL have no required and no optional parameters. A document's layout version SHALL continue to be read from the `format` the document or its index declares, never from a media type or header.

#### Scenario: Serving a claim file
- **WHEN** a publisher that controls its response headers serves `/knowledge/claims/2026-09/<id>.yaml`
- **THEN** it SHOULD serve it as `application/dkf+yaml`

#### Scenario: A parameter is not a format declaration
- **WHEN** a response carries `Content-Type: application/dkf+yaml; format=dkf/0.3` for an index whose `format` is `dkf/0.2`
- **THEN** the consumer reads the index as `dkf/0.2` and ignores the parameter

### Requirement: DKF documents are UTF-8
A document served as `application/dkf+yaml` SHALL be encoded in UTF-8, without a byte order mark. A `charset` parameter, if present, SHALL be ignored.

#### Scenario: A charset parameter
- **WHEN** a response carries `Content-Type: application/dkf+yaml; charset=utf-8`
- **THEN** the consumer reads the body as UTF-8, as it would without the parameter

### Requirement: Consumers do not reject documents on Content-Type
A consumer SHALL NOT reject a document fetched from a path that a manifest or index names solely because it was served as `application/yaml`, `text/yaml`, `application/x-yaml`, `text/plain` or `application/octet-stream`, or with no `Content-Type` at all. A document served under any other type SHALL be parsed as it would be otherwise, and reported only if it fails to parse as a DKF document. The path a document was fetched from, not its header, makes it a DKF document.

#### Scenario: A static host's generic label
- **WHEN** a GitHub Pages site serves `/.well-known/dkf.yaml` as `application/yaml`
- **THEN** the consumer reads it as a manifest

#### Scenario: An error page
- **WHEN** a host answers a segment path with a `text/html` error page and status 200
- **THEN** the consumer reports that the segment did not parse as a DKF document, not that it carried the wrong type

### Requirement: The media type is prepared for registration
The specification SHALL carry an RFC 6838 §5.6 registration template for `application/dkf+yaml`:
- **type name:** `application`; **subtype name:** `dkf+yaml`
- **required and optional parameters:** none
- **encoding considerations:** 8bit, UTF-8
- **security considerations:** documents MUST NOT contain YAML anchors or aliases, because alias expansion is a resource-exhaustion vector; a consumer resolves no tag outside the YAML 1.2 core schema; and documents contain no active content. Object files may quote source text verbatim, so their effective scope governs exposure
- **interoperability considerations:** consumers accept generic YAML labels
- **published specification:** this specification
- **fragment identifier considerations:** as for the `+yaml` suffix, with none added
- **file extension:** `.yaml`; **intended usage:** COMMON; **change controller:** the specification's maintainers

The specification SHALL state that the type is used unregistered until registration, and that registration changes no document.

#### Scenario: An implementer checks the registry
- **WHEN** an implementer looks up `application/dkf+yaml` before it is registered
- **THEN** the specification says it is not yet registered, carries the template, and says registration changes no document

#### Scenario: A document with an alias
- **WHEN** a document served as `application/dkf+yaml` contains a YAML alias
- **THEN** the consumer may refuse to expand it, and a validator rejects the file, as the existing file-format safety rule requires
