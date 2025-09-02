# Multi-Agent CLI Tool Usage Examples

This document provides comprehensive usage examples for the Multi-Agent CLI Tool, demonstrating how to use each command and the complete workflow.

## Installation

First, install the tool in development mode:

```bash
cd multi-agent-cli-tool
pip install -e .
```

## Configuration

Initialize the tool with default configuration:

```bash
multi-agent-cli init
```

This creates a `config.yaml` file with default settings for all agents.

## Basic Commands

### 1. Analyze Command

Analyze a complex task request:

```bash
# Basic usage
multi-agent-cli analyze "Create a web application with user authentication and deploy it to the cloud"

# With JSON output
multi-agent-cli analyze "Build a REST API for a todo application" --format json
```

### 2. Status Command

Check the status of a session:

```bash
multi-agent-cli status --session-id session_20250902_160132
```

### 3. Export Logs Command

Export execution logs for analysis:

```bash
# Export in JSON format
multi-agent-cli export-logs --session-id session_20250902_160132 --format json

# Export in text format
multi-agent-cli export-logs --session-id session_20250902_160132 --format text
```

## Complete Workflow Example

Here's a complete example of using the multi-agent system:

1. Initialize the tool:
```bash
multi-agent-cli init
```

2. Analyze a complex request:
```bash
multi-agent-cli analyze "Create a web application with user authentication, REST API, and database integration" --format json
```

3. Check the session status:
```bash
multi-agent-cli status --session-id session_20250902_160132
```

4. Export logs for detailed analysis:
```bash
multi-agent-cli export-logs --session-id session_20250902_160132 --format json
```

## Configuration File

The `config.yaml` file allows you to customize agent settings:

```yaml
system:
  max_retry_attempts: 3
  timeout_seconds: 300
  log_level: INFO

agents:
  analyst:
    model: gpt-4
    temperature: 0.2
    max_tokens: 2000
    capabilities:
      - requirement_analysis
      - task_decomposition
      - strategy_planning

  executor:
    model: gpt-3.5-turbo
    temperature: 0.1
    max_tokens: 1500
    capabilities:
      - command_execution
      - file_operations
      - api_calls

  validator:
    model: gpt-4
    temperature: 0.0
    max_tokens: 1000
    capabilities:
      - result_validation
      - quality_assurance
      - compliance_check

message_bus:
  queue_size: 1000
  batch_size: 10
  retry_delay: 5
```

## System Architecture

The multi-agent system consists of three specialized agents:

1. **Analyst Agent**: Analyzes requests, decomposes tasks, and creates execution plans
2. **Executor Agent**: Executes tasks according to the plan
3. **Validator Agent**: Validates results and ensures quality

The agents communicate through a message bus and are coordinated by a LangGraph workflow engine.

## Message Types

The system uses various message types for communication:

- `USER_REQUEST`: User's initial request
- `TASK_PLAN`: Task execution plan from Analyst
- `EXECUTION_RESULT`: Results from Executor
- `VALIDATION_RESULT`: Validation results from Validator
- And more...

## Extending the System

You can extend the system by:

1. Adding new agent types
2. Creating custom message types
3. Implementing new capabilities
4. Modifying the workflow graph

All components are designed to be modular and extensible.
