# Audit logging

import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
import aiofiles
import os
from models import AuditLog

class AuditService:
    def __init__(self):
        self.audit_file = "audit_logs.json"
        self._ensure_audit_file()
        
    def _ensure_audit_file(self):
        """Create audit file if it doesn't exist"""
        if not os.path.exists(self.audit_file):
            with open(self.audit_file, 'w') as f:
                json.dump([], f)
    
    async def log(self, audit_entry: AuditLog) -> str:
        """Log an audit entry"""
        async with aiofiles.open(self.audit_file, 'r') as f:
            content = await f.read()
            logs = json.loads(content) if content else []
        
        entry_dict = audit_entry.dict()
        logs.append(entry_dict)
        
        async with aiofiles.open(self.audit_file, 'w') as f:
            await f.write(json.dumps(logs, indent=2, default=str))
        
        return audit_entry.id
    
    async def log_error(self, session_id: str, error_message: str):
        """Log an error"""
        error_log = {
            "session_id": session_id,
            "timestamp": datetime.now(),
            "error": error_message,
            "type": "error"
        }
        
        async with aiofiles.open("error_logs.json", 'a') as f:
            await f.write(json.dumps(error_log, default=str) + "\n")
    
    async def get_log(self, session_id: str) -> Optional[Dict]:
        """Retrieve a specific audit log"""
        async with aiofiles.open(self.audit_file, 'r') as f:
            content = await f.read()
            logs = json.loads(content) if content else []
        
        for log in logs:
            if log.get("session_id") == session_id:
                return log
        return None