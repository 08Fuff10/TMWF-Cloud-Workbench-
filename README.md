# TMWF Cloud Workbench

AI-assisted cloud development environment for Arma Reforger, using the original Enfusion Workbench, automated script validation and optional MCP integration.

**Status: v0.1.0 bootstrap (experimental).** Eight local Python unit tests passed using synthetic logs. Native Workbench compilation, Windows cloud deployment and MCP integration have not yet been validated. No cloud resources have been provisioned.

## Quick start

1. Prepare a Windows x64 host (CPU-only with experimental WARP fallback, or a GPU VM). Initial sizing estimate: 8 vCPU, 32 GB RAM, 100–150 GB SSD.
2. Install Steam, Arma Reforger and Arma Reforger Tools in matching version lines. Use your own licensed account and comply with the host's and Steam's terms. Never give account credentials to an agent.
3. Install Python 3.10+ and Git. Install Node.js 20+ if using the optional MCP integration.
4. Start Steam and Workbench interactively once; resolve project dependencies and locate the Workbench executable. Keep an isolated copy of the mod project.
5. Run the wrapper from the repository directory (adjust paths):

```powershell
py -3 cloud_compile.py --exe "C:\Program Files (x86)\Steam\steamapps\common\Arma Reforger Tools\ArmaReforgerWorkbenchSteamDiag.exe" --game "C:\Program Files (x86)\Steam\steamapps\common\Arma Reforger" --project "C:\TMWF\addons\TMWF\TMWF.gproj" --warp
```

Use `--dry-run` to print the command without launching the compiler. `--warp` enables the documented software-rendering fallback; CPU-only compatibility is unverified. Omit it on a GPU host if appropriate. Use `--timeout 1200` for slow hosts and `--config PC` when appropriate (default: ALL).

Each run writes a JSON report and available logs to a unique folder under `runs/`. Isolated profiles may need additional dependency setup. Logs written outside the isolated profile must be collected separately. An exit code of zero alone does not establish a successful compilation; success-text matching is heuristic until verified against actual Workbench output.

## Local tests

```bash
python -m unittest -v
```

These tests do not require Workbench and do not compile Enforce Script.

## Optional MCP integration

The sample `mcp.example.json` targets the third-party [Enfusion Workbench MCP](https://github.com/Goldwep/enfusion-workbench-mcp), not an official Bohemia or ChatGPT connector. Review dependencies and pin a reviewed commit before installation. Build the project according to its own instructions, adapt the example paths and register it with a compatible local MCP client. Keep its Workbench network API on loopback; use an authenticated remote desktop or VPN rather than exposing ports publicly. Restrict tools, operate on a working copy and review diffs. Remove temporary Workbench handlers before publishing.

## Acceptance and roadmap

- [x] Compiler invocation and report wrapper
- [x] Local unit tests
- [x] Example MCP configuration
- [ ] Provision an authorized Windows test host
- [ ] Validate an unchanged vanilla project and a known-good addon
- [ ] Insert a deliberate syntax error in a disposable addon, confirm failure, revert and retest
- [ ] Calibrate log detection and profile/dependency handling
- [ ] Compare CPU/WARP and GPU cost, performance and reliability
- [ ] Validate MCP connectivity and pin versions
- [ ] Implement a bounded AI repair loop and review workflow
- [ ] Validate TMWF Framework compilation and runtime behavior

## Agent safety

The proposed agent may read project files, make small patches in an isolated working copy and run up to three repair iterations. Stop on dependency conflicts, ambiguous tool results or unconfirmed validation. Return diffs, logs and reports for review. No automatic publishing, credential changes or cloud purchases. These are design requirements, not an implemented autonomous agent.

## References

- [Official Workbench startup parameters](https://community.bistudio.com/wiki/Arma_Reforger:Startup_Parameters)
- [Workbench validation discussion](https://feedback.bistudio.com/T181951)
- [Third-party MCP implementation](https://github.com/Goldwep/enfusion-workbench-mcp)

No third-party game binaries are included. Project license has not yet been selected.
