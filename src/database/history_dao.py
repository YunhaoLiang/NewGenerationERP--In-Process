from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

class HistoryDAO:
    def __init__(self, session: Session):
        self.session = session

    def save_history(self, history_entry: Dict[str, Any]) -> None:
        """保存一条历史记录到数据库"""
        query = text('''
            INSERT INTO task_history (
                timestamp, task_id, task_type, input, output,
                status, agents_involved, execution_time
            ) VALUES (:timestamp, :task_id, :task_type, :input, :output, 
                     :status, :agents_involved, :execution_time)
        ''')
        
        self.session.execute(query, {
            'timestamp': history_entry['timestamp'],
            'task_id': history_entry['task_id'],
            'task_type': history_entry['task_type'],
            'input': history_entry['input'],
            'output': history_entry['output'],
            'status': history_entry['status'],
            'agents_involved': history_entry['agents_involved'],
            'execution_time': history_entry['execution_time']
        })
        self.session.commit()

    def get_history(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        task_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """查询历史记录"""
        query = ['SELECT * FROM task_history WHERE 1=1']
        params = {}
        
        if start_time:
            query.append('AND timestamp >= :start_time')
            params['start_time'] = start_time
            
        if end_time:
            query.append('AND timestamp <= :end_time')
            params['end_time'] = end_time
            
        if task_type:
            query.append('AND task_type = :task_type')
            params['task_type'] = task_type
            
        query.append('ORDER BY timestamp DESC')
        query.append('LIMIT :limit')
        params['limit'] = limit
        
        result = self.session.execute(text(' '.join(query)), params)
        return [dict(row) for row in result] 