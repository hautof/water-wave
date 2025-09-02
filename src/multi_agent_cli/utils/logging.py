from dataclasses import dataclass, field
from typing import Any, Optional, List
from datetime import datetime
import uuid


@dataclass
class ExecutionLog:
    """Execution log entry"""
    log_id: str
    session_id: str
    agent_id: str
    action: str
    input_data: Any
    output_data: Any
    execution_time: float
    timestamp: datetime
    status: str
    error_info: Optional[str] = None


class LogManager:
    """Log manager for agent execution logs"""
    
    def __init__(self):
        self.logs = {}
    
    def log_agent_action(self, session_id: str, agent_id: str, action: str, 
                        input_data: Any, output_data: Any, 
                        execution_time: float, status: str, error_info: Optional[str] = None):
        """Log an agent action"""
        log_entry = ExecutionLog(
            log_id=f"log_{uuid.uuid4().hex[:8]}",
            session_id=session_id,
            agent_id=agent_id,
            action=action,
            input_data=input_data,
            output_data=output_data,
            execution_time=execution_time,
            timestamp=datetime.now(),
            status=status,
            error_info=error_info
        )
        
        if session_id not in self.logs:
            self.logs[session_id] = []
        
        self.logs[session_id].append(log_entry)
    
    def get_execution_history(self, session_id: str) -> List[ExecutionLog]:
        """Get execution history for a session"""
        return self.logs.get(session_id, [])
    
    def export_logs(self, session_id: str, format: str = "json") -> str:
        """Export logs in specified format"""
        logs = self.get_execution_history(session_id)
        
        if format.lower() == "json":
            import json
            return json.dumps([{
                "log_id": log.log_id,
                "session_id": log.session_id,
                "agent_id": log.agent_id,
                "action": log.action,
                "input_data": str(log.input_data),
                "output_data": str(log.output_data),
                "execution_time": log.execution_time,
                "timestamp": log.timestamp.isoformat(),
                "status": log.status,
                "error_info": log.error_info
            } for log in logs], indent=2)
        
        # Default to plain text format
        result = f"Execution Logs for Session {session_id}\n"
        result += "=" * 50 + "\n"
        for log in logs:
            result += f"Agent: {log.agent_id}\n"
            result += f"Action: {log.action}\n"
            result += f"Status: {log.status}\n"
            result += f"Timestamp: {log.timestamp}\n"
            result += f"Execution Time: {log.execution_time}s\n"
            if log.error_info:
                result += f"Error: {log.error_info}\n"
            result += "-" * 30 + "\n"
        
        return result
