# v1.0.1 execution ledger

Plan: uninstall local portable copies, fix monitor recovery, make releases immutable and tag based, publish 1.0.1.

Ruling: workspace has no local Git metadata; keep the existing source workspace and publish an atomic remote commit using GitHub Git APIs, preserving the remote tree.
Ruling: deletion and publishing are already explicitly authorized by the user.
Task monitor recovery RED: three new monitor-list tests fail on the old implementation (unsupported actual-monitor input).
Uninstall: removed previous verification EXE/checksum and user settings. Workspace EXE deletion initially denied; verify and retry before completion.

Task uninstall complete: second deletion verified Test-Path False; no DesktopClock process found. Source preserved.
Task monitor recovery GREEN: all 13 unit tests passed after fix.
Ruling: connector has no tag-write or dispatch tool; a narrowly gated bootstrap workflow tags only the successful commit with exact release message and explicitly dispatches the tag workflow. Ordinary pushes still only build. No personal token is required.
Ruling: actual GUI integration runs on Windows CI because local Python Tcl installation is incomplete. Tests use temporary settings and package smoke never saves personal settings.

Final review: independent reviewer found withdrawn GUI coverage, unchecked drag drop and inline ref-name interpolation. Fixed by mapping GUI windows with visibility checks, recovering coordinates at drop (new test observed FAIL with x=2200 vs expected 1560), and reading runner environment variables.
Deferred minor: unused virtual_desktop_bounds helper retained to avoid unrelated cleanup.
