#!/usr/bin/env python3
"""
CLI Interface for the Multi-Agent Collaboration System
"""

import asyncio
import click
import json
import os
from typing import Optional, Dict, Any

from multi_agent_cli.messages.base import Message, MessageType
from multi_agent_cli.core.state import SystemState
from multi_agent_cli.workflow.workflow import MultiAgentWorkflow
from multi_agent_cli.config import load_config, create_default_config_file
from multi_agent_cli.utils import LogManager


class CLIInterface:
    """CLI Interface to bridge command-line and multi-agent system"""

    def __init__(self):
        """Initialize the CLI interface with workflow system"""
        self.workflow = MultiAgentWorkflow()
        self.config = load_config()
        self.log_manager = LogManager()

    async def analyze_request(self, text: str, format: str = "json") -> Dict[str, Any]:
        """
        Analyze a text request using the multi-agent system
        
        Args:
            text: The text to analyze
            format: Output format (json, text, etc.)
            
        Returns:
            Analysis results from the multi-agent system
        """
        # Create initial message
        initial_message = Message(
            id="cli_request_1",
            sender_id="cli_user",
            receiver_id="analyst",
            message_type=MessageType.USER_REQUEST,
            payload={
                "request": text,
                "format": format
            }
        )
        
        # Run workflow with a session ID to satisfy the checkpointer requirement
        final_state = await self.workflow.run(initial_message, session_id="cli_session_1")
        
        # Return results
        return {
            "session_id": final_state.session_id,
            "final_results": final_state.final_results,
            "task_history": [task.__dict__ for task in final_state.task_history]
        }

    async def execute_plan(self, plan: str, parallel: bool = False) -> Dict[str, Any]:
        """
        Execute a task plan using the multi-agent system
        
        Args:
            plan: The plan to execute
            parallel: Whether to execute tasks in parallel
            
        Returns:
            Execution results from the multi-agent system
        """
        # Implementation would go here
        return {"status": "not_implemented", "plan": plan, "parallel": parallel}

    async def validate_result(self, result: str, criteria: str) -> Dict[str, Any]:
        """
        Validate execution results using the multi-agent system
        
        Args:
            result: The result to validate
            criteria: Validation criteria
            
        Returns:
            Validation results from the multi-agent system
        """
        # Implementation would go here
        return {"status": "not_implemented", "result": result, "criteria": criteria}

    async def get_status(self, session_id: str) -> Dict[str, Any]:
        """
        Get the status of a session
        
        Args:
            session_id: The session ID to check
            
        Returns:
            Status information for the session
        """
        # Implementation would go here
        return {"status": "not_implemented", "session_id": session_id}

    async def export_logs(self, session_id: str, format: str = "json") -> Dict[str, Any]:
        """
        Export execution logs for a session
        
        Args:
            session_id: The session ID to export logs for
            format: Export format (json, csv, etc.)
            
        Returns:
            Exported logs
        """
        # Get logs from log manager
        exported_logs = self.log_manager.export_logs(session_id, format)
        return {
            "status": "success",
            "session_id": session_id,
            "format": format,
            "logs": exported_logs
        }


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Multi-Agent CLI Tool for Complex Task Analysis, Execution, and Validation"""
    pass


@cli.command()
@click.option('--config-path', '-c', default='./config.yaml', help='Path to configuration file')
def init(config_path: str):
    """Initialize the multi-agent CLI tool with default configuration"""
    try:
        create_default_config_file(config_path)
        click.echo(f"Default configuration file created at {config_path}")
    except Exception as e:
        click.echo(f"Error creating configuration file: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.argument('text', type=str)
@click.option('--format', '-f', default='json', help='Output format (json, text)')
def analyze(text: str, format: str):
    """Analyze a text request using the multi-agent system"""
    cli_interface = CLIInterface()
    try:
        results = asyncio.run(cli_interface.analyze_request(text, format))
        if format == 'json':
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"Analysis Results: {results}")
    except Exception as e:
        click.echo(f"Error during analysis: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--plan', '-p', required=True, help='Path to task plan file')
@click.option('--parallel', '-P', is_flag=True, help='Execute tasks in parallel')
def execute(plan: str, parallel: bool):
    """Execute a task plan using the multi-agent system"""
    if not os.path.exists(plan):
        click.echo(f"Error: Plan file '{plan}' not found", err=True)
        raise click.Abort()
        
    cli_interface = CLIInterface()
    try:
        with open(plan, 'r') as f:
            plan_content = f.read()
        results = asyncio.run(cli_interface.execute_plan(plan_content, parallel))
        click.echo(json.dumps(results, indent=2))
    except Exception as e:
        click.echo(f"Error during execution: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--result', '-r', required=True, help='Path to result file')
@click.option('--criteria', '-c', required=True, help='Validation criteria')
def validate(result: str, criteria: str):
    """Validate execution results using the multi-agent system"""
    if not os.path.exists(result):
        click.echo(f"Error: Result file '{result}' not found", err=True)
        raise click.Abort()
        
    cli_interface = CLIInterface()
    try:
        with open(result, 'r') as f:
            result_content = f.read()
        results = asyncio.run(cli_interface.validate_result(result_content, criteria))
        click.echo(json.dumps(results, indent=2))
    except Exception as e:
        click.echo(f"Error during validation: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--session-id', '-s', required=True, help='Session ID to check')
def status(session_id: str):
    """Check the status of a session"""
    cli_interface = CLIInterface()
    try:
        results = asyncio.run(cli_interface.get_status(session_id))
        click.echo(json.dumps(results, indent=2))
    except Exception as e:
        click.echo(f"Error getting status: {str(e)}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--session-id', '-s', required=True, help='Session ID to export logs for')
@click.option('--format', '-f', default='json', help='Export format (json, csv)')
def export_logs(session_id: str, format: str):
    """Export execution logs for a session"""
    cli_interface = CLIInterface()
    try:
        results = asyncio.run(cli_interface.export_logs(session_id, format))
        click.echo(json.dumps(results, indent=2))
    except Exception as e:
        click.echo(f"Error exporting logs: {str(e)}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    cli()
