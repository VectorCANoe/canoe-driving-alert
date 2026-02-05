# Changelog

All notable changes to the CANoe-IVI-OTA project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Multi-zone ambient lighting synchronization
- Advanced ADAS lighting patterns
- Predictive OTA update scheduling
- AI-based fault prediction

## [1.0.0] - 2026-02-05

### Added
- Initial project structure with ISO 26262 and ASPICE compliance
- Safety management framework
- Requirements management system
- Architecture documentation structure
- IVI module implementation framework
  - HVAC control structure
  - Window control structure
  - Seat control structure
- UX Lighting modules
  - Ambient lighting control (RGB, zones, scenes)
  - Dashboard lighting control (adaptive brightness)
  - ADAS integration lighting
  - Parking assist lighting
- Diagnostics modules
  - BDC fault injection framework
  - UDS diagnostic services structure
  - OTA update mechanism with vVIRTUALtarget
- Verification and validation framework
- Quality assurance structure
- Configuration management system
- CANoe simulation configurations
- Comprehensive documentation

### Features
- **Ambient Lighting**: 8-zone RGB control with 5 scene modes
- **Dashboard Lighting**: Adaptive brightness with 4 color themes
- **Fault Injection**: 50+ fault scenarios for diagnostic validation
- **OTA Updates**: Secure software updates with rollback capability
- **Safety Compliance**: ISO 26262 ASIL A/B support
- **Process Compliance**: ASPICE Level 2-3 structure

### Documentation
- Project README with complete overview
- Module-specific README files
- Safety management documentation
- Requirements engineering guides
- Architecture documentation templates
- Test plan templates
- Quality assurance procedures

## Version History

### Version Numbering Scheme
```
MAJOR.MINOR.PATCH

MAJOR: Incompatible API changes or major feature additions
MINOR: Backwards-compatible functionality additions
PATCH: Backwards-compatible bug fixes
```

### Component Versions

| Component | Version | Description |
|-----------|---------|-------------|
| BDC Core | 1.0.0 | Body Domain Controller base |
| IVI HVAC | 1.0.0 | Climate control module |
| IVI Window | 1.0.0 | Power window control |
| IVI Seat | 1.0.0 | Seat adjustment control |
| Ambient Lighting | 1.0.0 | RGB ambient lighting |
| Dashboard Lighting | 1.0.0 | Instrument cluster lighting |
| ADAS Lighting | 1.0.0 | ADAS event lighting |
| UDS Diagnostics | 1.0.0 | Diagnostic services |
| OTA Manager | 1.0.0 | Software update system |

## Migration Guides

### Migrating to 1.0.0
This is the initial release. No migration required.

## Breaking Changes

None (initial release)

## Deprecations

None (initial release)

## Security Updates

None (initial release)

## Known Issues

- None currently identified

## Contributors

- Hyundai Mobis Bootcamp Team
- Vector Korea Co., Ltd.

---

**Note**: This changelog is maintained as part of the configuration management process. All changes must be reviewed and approved before release.
