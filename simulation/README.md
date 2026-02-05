# Simulation Configurations

This directory contains CANoe simulation configurations, CAN databases, and test cases.

## Directory Structure

### configurations/
CANoe project configuration files (.cfg)
- Network configurations
- Node configurations
- Environment variable settings

### databases/
CAN database files (.dbc)
- Message definitions
- Signal mappings
- Network protocol specifications

### test-cases/
Simulation test scenarios
- Unit test configurations
- Integration test scenarios
- Validation test suites

## Usage

1. **Load Configuration**: Open CANoe and load the appropriate .cfg file from `configurations/`
2. **Import Database**: Ensure the correct .dbc file is loaded from `databases/`
3. **Run Tests**: Execute test cases from `test-cases/` directory
4. **Monitor Results**: Check trace window and analysis blocks for validation

## Best Practices

- Keep configurations modular and reusable
- Document all custom environment variables
- Maintain version control for database files
- Create separate test configurations for different scenarios
- Use descriptive naming conventions for all files

## File Naming Convention

- Configurations: `[Module]_[Feature]_config.cfg`
- Databases: `[Vehicle]_[Network]_vX.X.dbc`
- Test Cases: `[Module]_[TestType]_test.cfg`
