# Examples

## Example 1

Input:
- v1.8.0: Added CSV export for trial summary
- v1.8.0: Fixed crash when channel list is empty
- v1.8.0: Changed default sampling preview from 30s to 10s

Output:
- Summary: v1.8.0 improves export capability and stability while reducing preview latency.
- Added: CSV export for trial summary.
- Changed: default sampling preview reduced from 30s to 10s.
- Fixed: crash on empty channel list.
- Risks: users expecting 30s preview may need retraining.
- Action items:
  1. Update user guide screenshots.
  2. Announce preview default change to lab operators.

## Example 2

Input:
- v2.0.0: Deprecated legacy GDF converter path
- v2.0.0: Added compatibility check for external converter
- v2.0.0: Security hardening for path handling

Output:
- Summary: v2.0.0 improves conversion safety and prepares migration away from legacy conversion flow.
- Added: compatibility check for external converter.
- Deprecated: legacy GDF converter path.
- Security: hardened path handling.
- Risks: existing scripts relying on legacy converter may fail.
- Action items:
  1. Validate converter command in environment setup.
  2. Publish migration note.
