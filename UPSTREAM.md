# Upstream foundation and attribution

Brownie-Language currently begins from the Nim compiler source tree and is being adapted into the Brownie language implementation.

This document is kept separate from Brownie's product-facing identity so the project can use Brownie branding without obscuring the origin of inherited code.

## What this means

- Brownie is the target language and project identity.
- The current compiler source is derived from Nim; it is not accurate to describe the current tree as wholly original Brownie code.
- Existing copyright notices, license files, and attribution requirements must be preserved for inherited files.
- Technical identifiers and build configuration that still refer to Nim must only be renamed when the relevant compiler, bootstrap, tests, tooling, and build pipeline have been updated and verified.
- As files are substantially rewritten or replaced, their provenance should be tracked so upstream notices are handled correctly.

## License

Do not remove or rewrite `copying.txt` or inherited license/copyright notices as part of visual rebranding. Review the exact applicable license terms before changing notices in any file.

## Rebranding policy

Product-facing material (repository README, project descriptions, documentation landing pages, and Brownie-owned visual assets) should present Brownie as the project.

References that identify inherited Nim code, upstream history, required attribution, or still-active Nim build internals must remain accurate until the underlying code has genuinely been replaced.
