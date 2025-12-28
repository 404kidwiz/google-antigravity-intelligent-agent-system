# EXPERT MEMORY SYSTEM - Persistent Context Management

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import hashlib
import os
from pathlib import Path

class MemoryEntry:
    """Individual memory entry with metadata"""
    
    def __init__(self, id: str = "", timestamp: Optional[datetime] = None, expert_name: str = "", 
                 user_request: str = "", expert_response: str = "", 
                 user_feedback: Optional[float] = None, session_id: str = "",
                 context_tags: Optional[List[str]] = None, 
                 performance_metrics: Optional[Dict[str, float]] = None,
                 related_memories: Optional[List[str]] = None):
        self.id = id
        self.timestamp = timestamp or datetime.now()
        self.expert_name = expert_name
        self.user_request = user_request
        self.expert_response = expert_response
        self.user_feedback = user_feedback
        self.session_id = session_id
        self.context_tags = context_tags or []
        self.performance_metrics = performance_metrics or {}
        self.related_memories = related_memories or []
        self.relevance_score = 0.0

class ExpertMemorySystem:
    """Advanced memory system for persistent expert context management"""
    
    def __init__(self, storage_path: Optional[str] = None):
        if storage_path is None:
            storage_path = os.path.expanduser("~/.gemini/memory")
        
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize SQLite database for structured memories
        self.db_path = self.storage_path / "expert_memory.db"
        self._init_database()
        
        # Memory caches for fast access
        self.session_memory: Dict[str, Dict[str, Any]] = {}
        self.expert_knowledge: Dict[str, Dict[str, Any]] = {}
        self.context_index: Dict[str, List[str]] = {}
        
        # Load existing memories
        self._load_memories()
    
    def _init_database(self):
        """Initialize SQLite database for memory storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_entries (
                id TEXT PRIMARY KEY,
                timestamp DATETIME,
                expert_name TEXT,
                user_request TEXT,
                expert_response TEXT,
                user_feedback REAL,
                session_id TEXT,
                context_tags TEXT,
                performance_metrics TEXT,
                related_memories TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at DATETIME,
                last_interaction DATETIME,
                interaction_count INTEGER,
                user_preferences TEXT,
                expertise_cache TEXT,
                collaboration_patterns TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expert_learning (
                expert_name TEXT,
                learning_type TEXT,
                content TEXT,
                confidence_score REAL,
                created_at DATETIME,
                PRIMARY KEY (expert_name, learning_type, content)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_interaction(self, session_id: str, expert_name: str, 
                         user_request: str, expert_response: str,
                         performance_metrics: Optional[Dict[str, float]] = None,
                         context_tags: Optional[List[str]] = None,
                         user_feedback: Optional[float] = None) -> str:
        """Store an interaction in memory with full context"""
        
        # Generate unique memory ID
        memory_id = hashlib.md5(
            f"{session_id}{expert_name}{user_request}{datetime.now().isoformat()}".encode()
        ).hexdigest()
        
        # Create memory entry
        memory = MemoryEntry(
            id=memory_id,
            timestamp=datetime.now(),
            expert_name=expert_name,
            user_request=user_request,
            expert_response=expert_response,
            user_feedback=user_feedback,
            session_id=session_id,
            context_tags=context_tags or [],
            performance_metrics=performance_metrics or {},
            related_memories=[]
        )
        
        # Find related memories
        memory.related_memories = self._find_related_memories(memory)
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO memory_entries 
            (id, timestamp, expert_name, user_request, expert_response, 
             user_feedback, session_id, context_tags, performance_metrics, related_memories)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory.id,
            memory.timestamp,
            memory.expert_name,
            memory.user_request,
            memory.expert_response,
            memory.user_feedback,
            memory.session_id,
            json.dumps(memory.context_tags),
            json.dumps(memory.performance_metrics),
            json.dumps(memory.related_memories)
        ))
        
        conn.commit()
        conn.close()
        
        # Update caches
        self._update_session_memory(session_id, expert_name, memory)
        self._update_expert_knowledge(expert_name, memory)
        self._update_context_index(memory)
        
        return memory_id
    
    def get_session_context(self, session_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get comprehensive session context"""
        
        # Get recent memories for session
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM memory_entries 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (session_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Parse memories
        recent_memories = []
        for row in rows:
            memory = self._row_to_memory_entry(row)
            recent_memories.append(memory)
        
        # Get session data
        session_data = self._get_session_data(session_id)
        
        # Build context
        context = {
            "session_id": session_id,
            "recent_interactions": recent_memories,
            "user_preferences": session_data.get("user_preferences", {}),
            "expertise_cache": session_data.get("expertise_cache", {}),
            "collaboration_patterns": session_data.get("collaboration_patterns", {}),
            "interaction_count": session_data.get("interaction_count", 0),
            "session_duration": self._calculate_session_duration(session_id),
            "expert_usage_history": self._get_expert_usage_history(session_id),
            "context_summary": self._generate_context_summary(recent_memories),
            "predicted_needs": self._predict_user_needs(recent_memories)
        }
        
        return context
    
    def get_expert_memory(self, expert_name: str, limit: int = 50) -> Dict[str, Any]:
        """Get comprehensive expert memory and learning data"""
        
        # Get expert's memories
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM memory_entries 
            WHERE expert_name = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (expert_name, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Parse memories
        expert_memories = []
        for row in rows:
            memory = self._row_to_memory_entry(row)
            expert_memories.append(memory)
        
        # Get expert learning data
        learning_data = self._get_expert_learning(expert_name)
        
        # Build expert memory profile
        expert_memory = {
            "expert_name": expert_name,
            "recent_interactions": expert_memories,
            "learning_data": learning_data,
            "performance_trends": self._calculate_performance_trends(expert_memories),
            "specialization_areas": self._identify_specialization_areas(expert_memories),
            "collaboration_patterns": self._analyze_collaboration_patterns(expert_memories),
            "user_feedback_summary": self._summarize_user_feedback(expert_memories),
            "knowledge_gaps": self._identify_knowledge_gaps(expert_memories, learning_data),
            "adaptation_suggestions": self._generate_adaptation_suggestions(expert_memories)
        }
        
        return expert_memory
    
    def learn_from_interaction(self, expert_name: str, learning_type: str, 
                              content: str, confidence_score: float):
        """Store learning from expert interactions"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO expert_learning 
            (expert_name, learning_type, content, confidence_score, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (expert_name, learning_type, content, confidence_score, datetime.now()))
        
        conn.commit()
        conn.close()
        
        # Update expert knowledge cache
        if expert_name not in self.expert_knowledge:
            self.expert_knowledge[expert_name] = {}
        
        if learning_type not in self.expert_knowledge[expert_name]:
            self.expert_knowledge[expert_name][learning_type] = []
        
        self.expert_knowledge[expert_name][learning_type].append({
            "content": content,
            "confidence": confidence_score,
            "timestamp": datetime.now()
        })
    
    def find_similar_memories(self, query: str, expert_name: Optional[str] = None, 
                            limit: int = 10) -> List[MemoryEntry]:
        """Find memories similar to query using semantic search"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build SQL query
        sql = '''
            SELECT * FROM memory_entries 
            WHERE (user_request LIKE ? OR expert_response LIKE ?)
        '''
        params = [f"%{query}%", f"%{query}%"]
        
        if expert_name:
            sql += ' AND expert_name = ?'
            params.append(expert_name)
        
        sql += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(str(limit))
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        
        # Parse and rank memories
        memories = []
        for row in rows:
            memory = self._row_to_memory_entry(row)
            relevance_score = self._calculate_relevance_score(query, memory)
            memory.relevance_score = relevance_score
            memories.append(memory)
        
        # Sort by relevance
        memories.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return memories
    
    def _find_related_memories(self, memory: MemoryEntry) -> List[str]:
        """Find related memories based on content similarity"""
        
        related_ids = []
        
        # Search for similar expert responses
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find memories with similar requests
        cursor.execute('''
            SELECT id FROM memory_entries 
            WHERE expert_name = ? 
            AND user_request LIKE ? 
            AND id != ?
            LIMIT 3
        ''', (memory.expert_name, f"%{memory.user_request[:50]}%", memory.id))
        
        rows = cursor.fetchall()
        related_ids.extend([row[0] for row in rows])
        
        # Find memories with similar context tags
        if memory.context_tags:
            for tag in memory.context_tags:
                cursor.execute('''
                    SELECT id FROM memory_entries 
                    WHERE context_tags LIKE ? 
                    AND id != ?
                    LIMIT 2
                ''', (f"%{tag}%", memory.id))
                
                rows = cursor.fetchall()
                related_ids.extend([row[0] for row in rows])
        
        conn.close()
        
        return list(set(related_ids))[:5]  # Limit to 5 related memories
    
    def _update_session_memory(self, session_id: str, expert_name: str, memory: MemoryEntry):
        """Update session memory cache"""
        
        if session_id not in self.session_memory:
            self.session_memory[session_id] = {
                "experts_used": [],
                "interaction_count": 0,
                "last_interaction": memory.timestamp,
                "context_summary": {}
            }
        
        session = self.session_memory[session_id]
        session["interaction_count"] += 1
        session["last_interaction"] = memory.timestamp
        
        if expert_name not in session["experts_used"]:
            session["experts_used"].append(expert_name)
    
    def _update_expert_knowledge(self, expert_name: str, memory: MemoryEntry):
        """Update expert knowledge cache"""
        
        if expert_name not in self.expert_knowledge:
            self.expert_knowledge[expert_name] = {
                "total_interactions": 0,
                "avg_performance": 0.0,
                "specializations": {},
                "recent_successes": []
            }
        
        knowledge = self.expert_knowledge[expert_name]
        knowledge["total_interactions"] += 1
        
        # Update performance average
        if memory.performance_metrics:
            perf_score = sum(memory.performance_metrics.values()) / len(memory.performance_metrics)
            knowledge["avg_performance"] = (
                (knowledge["avg_performance"] * (knowledge["total_interactions"] - 1) + perf_score) /
                knowledge["total_interactions"]
            )
        
        # Track recent successes
        if memory.user_feedback and memory.user_feedback >= 4.0:
            knowledge["recent_successes"].append({
                "memory_id": memory.id,
                "feedback": memory.user_feedback,
                "timestamp": memory.timestamp.isoformat()
            })
            
            # Keep only last 10 successes
            knowledge["recent_successes"] = knowledge["recent_successes"][-10:]
    
    def _update_context_index(self, memory: MemoryEntry):
        """Update context index for fast retrieval"""
        
        for tag in memory.context_tags:
            if tag not in self.context_index:
                self.context_index[tag] = []
            
            if memory.id not in self.context_index[tag]:
                self.context_index[tag].append(memory.id)
    
    def _row_to_memory_entry(self, row) -> MemoryEntry:
        """Convert database row to MemoryEntry object"""
        return MemoryEntry(
            id=row[0],
            timestamp=datetime.fromisoformat(row[1]),
            expert_name=row[2],
            user_request=row[3],
            expert_response=row[4],
            user_feedback=row[5],
            session_id=row[6],
            context_tags=json.loads(row[7]) if row[7] else [],
            performance_metrics=json.loads(row[8]) if row[8] else {},
            related_memories=json.loads(row[9]) if row[9] else []
        )
    
    def _get_session_data(self, session_id: str) -> Dict[str, Any]:
        """Get session data from database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM sessions WHERE session_id = ?
        ''', (session_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "session_id": row[0],
                "created_at": row[1],
                "last_interaction": row[2],
                "interaction_count": row[3],
                "user_preferences": json.loads(row[4]) if row[4] else {},
                "expertise_cache": json.loads(row[5]) if row[5] else {},
                "collaboration_patterns": json.loads(row[6]) if row[6] else {}
            }
        
        return {}
    
    def _get_expert_learning(self, expert_name: str) -> Dict[str, Any]:
        """Get expert learning data"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT learning_type, content, confidence_score, created_at
            FROM expert_learning 
            WHERE expert_name = ?
            ORDER BY confidence_score DESC
        ''', (expert_name,))
        
        rows = cursor.fetchall()
        conn.close()
        
        learning_data = {}
        for row in rows:
            learning_type, content, confidence, created_at = row
            if learning_type not in learning_data:
                learning_data[learning_type] = []
            
            learning_data[learning_type].append({
                "content": content,
                "confidence": confidence,
                "created_at": created_at
            })
        
        return learning_data
    
    def _calculate_session_duration(self, session_id: str) -> str:
        """Calculate session duration"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT MIN(timestamp), MAX(timestamp) FROM memory_entries 
            WHERE session_id = ?
        ''', (session_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] and result[1]:
            start = datetime.fromisoformat(result[0])
            end = datetime.fromisoformat(result[1])
            duration = end - start
            
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            
            if hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
        
        return "0m"
    
    def _get_expert_usage_history(self, session_id: str) -> Dict[str, int]:
        """Get expert usage history for session"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT expert_name, COUNT(*) as usage_count
            FROM memory_entries 
            WHERE session_id = ?
            GROUP BY expert_name
            ORDER BY usage_count DESC
        ''', (session_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return {row[0]: row[1] for row in rows}
    
    def _generate_context_summary(self, memories: List[MemoryEntry]) -> str:
        """Generate summary of session context"""
        
        if not memories:
            return "No previous interactions"
        
        # Extract key themes
        all_requests = " ".join([memory.user_request for memory in memories])
        all_experts = list(set([memory.expert_name for memory in memories]))
        
        # Generate summary
        summary = f"Session with {len(memories)} interactions. "
        summary += f"Experts involved: {', '.join(all_experts)}. "
        
        # Try to identify main topic
        common_words = []
        for word in all_requests.lower().split():
            if len(word) > 4 and word.isalpha():
                common_words.append(word)
        
        if common_words:
            from collections import Counter
            word_counts = Counter(common_words)
            top_words = [word for word, count in word_counts.most_common(3)]
            summary += f"Main topics: {', '.join(top_words)}."
        
        return summary
    
    def _predict_user_needs(self, memories: List[MemoryEntry]) -> List[str]:
        """Predict what user might need next based on history"""
        
        if not memories:
            return []
        
        needs = []
        recent_experts = [memory.expert_name for memory in memories[:5]]
        
        # Common expert transitions
        transitions = {
            "react-expert": ["redux-expert", "testing-framework", "css-expert"],
            "backend-architect": ["database-expert", "docker-expert", "security-expert"],
            "python-expert": ["testing-framework", "database-expert", "deployment-expert"],
            "ui-designer": ["frontend-developer", "accessibility-expert"],
            "database-expert": ["migration-expert", "optimization-expert"]
        }
        
        # Predict based on transitions
        for expert in recent_experts:
            if expert in transitions:
                for next_expert in transitions[expert]:
                    if next_expert not in recent_experts:
                        needs.append(f"May need {next_expert} assistance")
        
        return needs[:3]  # Top 3 predictions
    
    def _calculate_performance_trends(self, memories: List[MemoryEntry]) -> Dict[str, Any]:
        """Calculate performance trends for expert"""
        
        if not memories:
            return {}
        
        # Group memories by time periods
        recent_memories = [m for m in memories if (datetime.now() - m.timestamp).days <= 7]
        older_memories = [m for m in memories if (datetime.now() - m.timestamp).days > 7]
        
        trends = {}
        
        if recent_memories and older_memories:
            recent_avg = sum(m.performance_metrics.get("quality", 4.0) for m in recent_memories) / len(recent_memories)
            older_avg = sum(m.performance_metrics.get("quality", 4.0) for m in older_memories) / len(older_memories)
            
            if recent_avg > older_avg:
                trends["performance_trend"] = "improving"
            elif recent_avg < older_avg:
                trends["performance_trend"] = "declining"
            else:
                trends["performance_trend"] = "stable"
        
        return trends
    
    def _identify_specialization_areas(self, memories: List[MemoryEntry]) -> List[str]:
        """Identify expert's specialization areas based on interactions"""
        
        if not memories:
            return []
        
        # Extract common themes from requests
        all_requests = " ".join([memory.user_request.lower() for memory in memories])
        
        # Common technical terms
        specializations = []
        tech_terms = {
            "react": ["react", "hooks", "components", "jsx"],
            "database": ["database", "sql", "query", "schema"],
            "api": ["api", "endpoint", "rest", "graphql"],
            "security": ["security", "authentication", "authorization", "encryption"],
            "performance": ["performance", "optimization", "speed", "efficiency"],
            "testing": ["test", "testing", "unit", "integration"],
            "deployment": ["deploy", "deployment", "production", "docker"]
        }
        
        for specialization, keywords in tech_terms.items():
            if sum(1 for keyword in keywords if keyword in all_requests) >= 3:
                specializations.append(specialization)
        
        return specializations
    
    def _analyze_collaboration_patterns(self, memories: List[MemoryEntry]) -> Dict[str, Any]:
        """Analyze collaboration patterns with other experts"""
        
        # This would analyze how this expert works with others
        # For now, return basic patterns
        return {
            "collaboration_frequency": "medium",
            "preferred_partners": [],
            "collaboration_style": "supportive"
        }
    
    def _summarize_user_feedback(self, memories: List[MemoryEntry]) -> Dict[str, float]:
        """Summarize user feedback for expert"""
        
        feedback_scores = [m.user_feedback for m in memories if m.user_feedback is not None]
        
        if not feedback_scores:
            return {}
        
        return {
            "average_feedback": sum(feedback_scores) / len(feedback_scores),
            "total_feedback_count": len(feedback_scores),
            "positive_feedback_rate": len([f for f in feedback_scores if f >= 4.0]) / len(feedback_scores)
        }
    
    def _identify_knowledge_gaps(self, memories: List[MemoryEntry], 
                                learning_data: Dict[str, Any]) -> List[str]:
        """Identify knowledge gaps based on interactions and learning"""
        
        gaps = []
        
        # Look for areas with low performance or no learning
        if memories:
            low_performance_areas = [m for m in memories 
                                  if m.performance_metrics.get("quality", 5.0) < 3.5]
            
            for memory in low_performance_areas:
                # Extract keywords from low-performance requests
                request_words = memory.user_request.lower().split()
                for word in request_words:
                    if len(word) > 5 and word.isalpha():
                        gaps.append(f"Improve knowledge in {word}")
        
        return list(set(gaps))[:5]  # Top 5 gaps
    
    def _generate_adaptation_suggestions(self, memories: List[MemoryEntry]) -> List[str]:
        """Generate suggestions for expert adaptation"""
        
        suggestions = []
        
        if not memories:
            return suggestions
        
        # Analyze recent performance
        recent_memories = memories[:10]
        avg_quality = sum(m.performance_metrics.get("quality", 4.0) for m in recent_memories) / len(recent_memories)
        
        if avg_quality < 4.0:
            suggestions.append("Focus on improving response quality")
        
        # Check for repetitive patterns
        requests = [m.user_request for m in recent_memories]
        if len(set(requests)) < len(requests) * 0.5:
            suggestions.append("Develop more diverse solution approaches")
        
        # Check feedback patterns
        low_feedback = [m for m in recent_memories if m.user_feedback and m.user_feedback < 3.0]
        if len(low_feedback) > len(recent_memories) * 0.3:
            suggestions.append("Review and improve user interaction patterns")
        
        return suggestions
    
    def _calculate_relevance_score(self, query: str, memory: MemoryEntry) -> float:
        """Calculate relevance score between query and memory"""
        
        query_words = set(query.lower().split())
        request_words = set(memory.user_request.lower().split())
        response_words = set(memory.expert_response.lower().split())
        
        # Calculate overlap
        request_overlap = len(query_words & request_words) / len(query_words | request_words) if query_words | request_words else 0
        response_overlap = len(query_words & response_words) / len(query_words | response_words) if query_words | response_words else 0
        
        # Time decay (newer memories more relevant)
        days_old = (datetime.now() - memory.timestamp).days
        time_factor = 1.0 / (1.0 + days_old * 0.1)
        
        # Combine factors
        relevance = (request_overlap * 0.6 + response_overlap * 0.4) * time_factor
        
        return relevance
    
    def _load_memories(self):
        """Load existing memories into cache"""
        
        # This would load recent memories into cache for faster access
        # For now, initialize empty caches
        pass

# Global memory system instance
expert_memory_system = ExpertMemorySystem()