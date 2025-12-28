# PERFORMANCE ANALYTICS DASHBOARD - Real-time Expert Monitoring

import json
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import statistics
import threading
from collections import defaultdict, deque
import sqlite3
import os
from pathlib import Path

@dataclass
class ExpertMetrics:
    """Real-time expert performance metrics"""
    expert_name: str
    response_time: float
    success_rate: float
    user_rating: float
    collaboration_effectiveness: float
    knowledge_depth: float
    adaptability_score: float
    task_completion_time: float
    error_rate: float
    total_interactions: int
    last_updated: datetime

@dataclass
class SystemMetrics:
    """Overall system performance metrics"""
    total_experts: int
    active_sessions: int
    requests_per_minute: float
    average_response_time: float
    system_load: float
    memory_usage: float
    error_rate: float
    uptime_percentage: float
    timestamp: datetime

class PerformanceAnalyticsDashboard:
    """Real-time performance analytics and monitoring system"""
    
    def __init__(self, storage_path: Optional[str] = None):
        if storage_path is None:
            storage_path = os.path.expanduser("~/.gemini/analytics")
        
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self.db_path = self.storage_path / "performance_metrics.db"
        self._init_database()
        
        # Performance tracking
        self.expert_metrics: Dict[str, ExpertMetrics] = {}
        self.system_metrics_history: deque = deque(maxlen=1000)
        self.real_time_metrics: Dict[str, Any] = defaultdict(list)
        
        # Alert thresholds
        self.alert_thresholds = {
            "response_time": 3.0,
            "error_rate": 0.05,
            "memory_usage": 0.8,
            "system_load": 0.9,
            "user_rating": 3.0
        }
        
        # Background monitoring
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._background_monitoring, daemon=True)
        self.monitoring_thread.start()
        
        # Load existing metrics
        self._load_historical_metrics()
    
    def _init_database(self):
        """Initialize database for performance metrics storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expert_metrics (
                expert_name TEXT,
                timestamp DATETIME,
                response_time REAL,
                success_rate REAL,
                user_rating REAL,
                collaboration_effectiveness REAL,
                knowledge_depth REAL,
                adaptability_score REAL,
                task_completion_time REAL,
                error_rate REAL,
                total_interactions INTEGER,
                PRIMARY KEY (expert_name, timestamp)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                timestamp DATETIME PRIMARY KEY,
                total_experts INTEGER,
                active_sessions INTEGER,
                requests_per_minute REAL,
                average_response_time REAL,
                system_load REAL,
                memory_usage REAL,
                error_rate REAL,
                uptime_percentage REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT,
                expert_name TEXT,
                message TEXT,
                severity TEXT,
                timestamp DATETIME,
                resolved BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_expert_performance(self, expert_name: str, 
                                 response_time: float,
                                 success: bool,
                                 user_rating: Optional[float] = None,
                                 collaboration_score: Optional[float] = None,
                                 task_duration: Optional[float] = None,
                                 error_occurred: bool = False):
        """Record expert performance metrics"""
        
        # Get current metrics for expert
        if expert_name not in self.expert_metrics:
            self.expert_metrics[expert_name] = ExpertMetrics(
                expert_name=expert_name,
                response_time=response_time,
                success_rate=1.0 if success else 0.0,
                user_rating=user_rating or 4.0,
                collaboration_effectiveness=collaboration_score or 4.0,
                knowledge_depth=4.0,
                adaptability_score=4.0,
                task_completion_time=task_duration or response_time,
                error_rate=1.0 if error_occurred else 0.0,
                total_interactions=1,
                last_updated=datetime.now()
            )
        else:
            # Update existing metrics
            current = self.expert_metrics[expert_name]
            
            # Calculate running averages
            n = current.total_interactions
            new_n = n + 1
            
            # Update success rate
            success_rate = (current.success_rate * n + (1.0 if success else 0.0)) / new_n
            
            # Update error rate
            error_rate = (current.error_rate * n + (1.0 if error_occurred else 0.0)) / new_n
            
            # Update response time
            avg_response_time = (current.response_time * n + response_time) / new_n
            
            # Update user rating if provided
            avg_user_rating = current.user_rating
            if user_rating is not None:
                avg_user_rating = (current.user_rating * n + user_rating) / new_n
            
            # Update collaboration score if provided
            avg_collaboration = current.collaboration_effectiveness
            if collaboration_score is not None:
                avg_collaboration = (current.collaboration_effectiveness * n + collaboration_score) / new_n
            
            # Update task completion time if provided
            avg_task_time = current.task_completion_time
            if task_duration is not None:
                avg_task_time = (current.task_completion_time * n + task_duration) / new_n
            
            # Calculate derived metrics
            knowledge_depth = self._calculate_knowledge_depth(expert_name)
            adaptability_score = self._calculate_adaptability_score(expert_name)
            
            self.expert_metrics[expert_name] = ExpertMetrics(
                expert_name=expert_name,
                response_time=avg_response_time,
                success_rate=success_rate,
                user_rating=avg_user_rating,
                collaboration_effectiveness=avg_collaboration,
                knowledge_depth=knowledge_depth,
                adaptability_score=adaptability_score,
                task_completion_time=avg_task_time,
                error_rate=error_rate,
                total_interactions=new_n,
                last_updated=datetime.now()
            )
        
        # Store in database
        self._store_expert_metrics(self.expert_metrics[expert_name])
        
        # Check for alerts
        self._check_expert_alerts(expert_name)
    
    def record_system_metrics(self, active_sessions: int, 
                            requests_per_minute: float,
                            system_load: float,
                            memory_usage: float):
        """Record overall system performance metrics"""
        
        # Calculate system metrics
        total_experts = len(self.expert_metrics)
        avg_response_time = 0.0
        error_rate = 0.0
        
        if self.expert_metrics:
            response_times = [m.response_time for m in self.expert_metrics.values()]
            error_rates = [m.error_rate for m in self.expert_metrics.values()]
            avg_response_time = statistics.mean(response_times)
            error_rate = statistics.mean(error_rates)
        
        system_metrics = SystemMetrics(
            total_experts=total_experts,
            active_sessions=active_sessions,
            requests_per_minute=requests_per_minute,
            average_response_time=avg_response_time,
            system_load=system_load,
            memory_usage=memory_usage,
            error_rate=error_rate,
            uptime_percentage=99.9,  # Would calculate actual uptime
            timestamp=datetime.now()
        )
        
        self.system_metrics_history.append(system_metrics)
        self._store_system_metrics(system_metrics)
        
        # Check system alerts
        self._check_system_alerts(system_metrics)
    
    def get_performance_dashboard(self) -> Dict[str, Any]:
        """Generate comprehensive performance dashboard"""
        
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "expert_performance": self._get_expert_performance_summary(),
            "system_health": self._get_system_health_status(),
            "top_performers": self._get_top_performers(),
            "performance_trends": self._get_performance_trends(),
            "active_alerts": self._get_active_alerts(),
            "resource_utilization": self._get_resource_utilization(),
            "quality_metrics": self._get_quality_metrics()
        }
        
        return dashboard
    
    def get_expert_detailed_report(self, expert_name: str, 
                                 days: int = 30) -> Dict[str, Any]:
        """Get detailed performance report for specific expert"""
        
        if expert_name not in self.expert_metrics:
            return {"error": f"Expert {expert_name} not found"}
        
        # Get historical data
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since_date = datetime.now() - timedelta(days=days)
        cursor.execute('''
            SELECT * FROM expert_metrics 
            WHERE expert_name = ? AND timestamp >= ?
            ORDER BY timestamp DESC
        ''', (expert_name, since_date))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Parse historical data
        historical_data = []
        for row in rows:
            historical_data.append({
                "timestamp": row[1],
                "response_time": row[2],
                "success_rate": row[3],
                "user_rating": row[4],
                "collaboration_effectiveness": row[5],
                "knowledge_depth": row[6],
                "adaptability_score": row[7],
                "task_completion_time": row[8],
                "error_rate": row[9],
                "total_interactions": row[10]
            })
        
        current_metrics = self.expert_metrics[expert_name]
        
        # Generate report
        report = {
            "expert_name": expert_name,
            "current_metrics": asdict(current_metrics),
            "historical_data": historical_data,
            "performance_summary": self._generate_expert_summary(expert_name, historical_data),
            "recommendations": self._generate_expert_recommendations(expert_name, historical_data),
            "comparison": self._compare_expert_performance(expert_name),
            "trend_analysis": self._analyze_expert_trends(historical_data)
        }
        
        return report
    
    def _calculate_knowledge_depth(self, expert_name: str) -> float:
        """Calculate knowledge depth score based on interaction diversity"""
        
        # This would analyze the variety and complexity of interactions
        # For now, return a simulated score
        base_score = 4.0
        
        # Adjust based on total interactions
        if expert_name in self.expert_metrics:
            interactions = self.expert_metrics[expert_name].total_interactions
            if interactions > 100:
                base_score += 0.5
            elif interactions > 50:
                base_score += 0.3
        
        return min(base_score, 5.0)
    
    def _calculate_adaptability_score(self, expert_name: str) -> float:
        """Calculate adaptability score based on performance improvements"""
        
        if expert_name not in self.expert_metrics:
            return 4.0
        
        # Get recent performance trend
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get last 10 records
        cursor.execute('''
            SELECT response_time, success_rate FROM expert_metrics 
            WHERE expert_name = ? 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''', (expert_name,))
        
        rows = cursor.fetchall()
        conn.close()
        
        if len(rows) < 5:
            return 4.0
        
        # Calculate trend
        recent_half = rows[:len(rows)//2]
        older_half = rows[len(rows)//2:]
        
        recent_avg = statistics.mean([r[0] for r in recent_half])
        older_avg = statistics.mean([r[0] for r in older_half])
        
        # Better adaptability if response time is improving
        if recent_avg < older_avg:
            return min(5.0, 4.0 + (older_avg - recent_avg) * 0.5)
        else:
            return max(3.0, 4.0 - (recent_avg - older_avg) * 0.3)
    
    def _store_expert_metrics(self, metrics: ExpertMetrics):
        """Store expert metrics in database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO expert_metrics 
            (expert_name, timestamp, response_time, success_rate, user_rating,
             collaboration_effectiveness, knowledge_depth, adaptability_score,
             task_completion_time, error_rate, total_interactions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metrics.expert_name,
            metrics.last_updated,
            metrics.response_time,
            metrics.success_rate,
            metrics.user_rating,
            metrics.collaboration_effectiveness,
            metrics.knowledge_depth,
            metrics.adaptability_score,
            metrics.task_completion_time,
            metrics.error_rate,
            metrics.total_interactions
        ))
        
        conn.commit()
        conn.close()
    
    def _store_system_metrics(self, metrics: SystemMetrics):
        """Store system metrics in database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO system_metrics 
            (timestamp, total_experts, active_sessions, requests_per_minute,
             average_response_time, system_load, memory_usage, error_rate, uptime_percentage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metrics.timestamp,
            metrics.total_experts,
            metrics.active_sessions,
            metrics.requests_per_minute,
            metrics.average_response_time,
            metrics.system_load,
            metrics.memory_usage,
            metrics.error_rate,
            metrics.uptime_percentage
        ))
        
        conn.commit()
        conn.close()
    
    def _check_expert_alerts(self, expert_name: str):
        """Check for expert performance alerts"""
        
        if expert_name not in self.expert_metrics:
            return
        
        metrics = self.expert_metrics[expert_name]
        
        # Check response time
        if metrics.response_time > self.alert_thresholds["response_time"]:
            self._create_alert(
                alert_type="response_time",
                expert_name=expert_name,
                message=f"Response time {metrics.response_time:.2f}s exceeds threshold {self.alert_thresholds['response_time']}s",
                severity="warning"
            )
        
        # Check error rate
        if metrics.error_rate > self.alert_thresholds["error_rate"]:
            self._create_alert(
                alert_type="error_rate",
                expert_name=expert_name,
                message=f"Error rate {metrics.error_rate:.2%} exceeds threshold {self.alert_thresholds['error_rate']:.2%}",
                severity="critical"
            )
        
        # Check user rating
        if metrics.user_rating < self.alert_thresholds["user_rating"]:
            self._create_alert(
                alert_type="user_rating",
                expert_name=expert_name,
                message=f"User rating {metrics.user_rating:.1f} below threshold {self.alert_thresholds['user_rating']}",
                severity="warning"
            )
    
    def _check_system_alerts(self, metrics: SystemMetrics):
        """Check for system-level alerts"""
        
        # Check memory usage
        if metrics.memory_usage > self.alert_thresholds["memory_usage"]:
            self._create_alert(
                alert_type="memory_usage",
                expert_name="system",
                message=f"Memory usage {metrics.memory_usage:.1%} exceeds threshold {self.alert_thresholds['memory_usage']:.1%}",
                severity="critical"
            )
        
        # Check system load
        if metrics.system_load > self.alert_thresholds["system_load"]:
            self._create_alert(
                alert_type="system_load",
                expert_name="system",
                message=f"System load {metrics.system_load:.1%} exceeds threshold {self.alert_thresholds['system_load']:.1%}",
                severity="critical"
            )
        
        # Check average response time
        if metrics.average_response_time > self.alert_thresholds["response_time"]:
            self._create_alert(
                alert_type="avg_response_time",
                expert_name="system",
                message=f"Average response time {metrics.average_response_time:.2f}s exceeds threshold",
                severity="warning"
            )
    
    def _create_alert(self, alert_type: str, expert_name: str, 
                     message: str, severity: str):
        """Create performance alert"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO performance_alerts 
            (alert_type, expert_name, message, severity, timestamp, resolved)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (alert_type, expert_name, message, severity, datetime.now(), False))
        
        conn.commit()
        conn.close()
    
    def _get_expert_performance_summary(self) -> Dict[str, Any]:
        """Get summary of expert performance"""
        
        if not self.expert_metrics:
            return {}
        
        # Calculate aggregates
        response_times = [m.response_time for m in self.expert_metrics.values()]
        success_rates = [m.success_rate for m in self.expert_metrics.values()]
        user_ratings = [m.user_rating for m in self.expert_metrics.values()]
        error_rates = [m.error_rate for m in self.expert_metrics.values()]
        
        return {
            "total_experts": len(self.expert_metrics),
            "average_response_time": statistics.mean(response_times),
            "average_success_rate": statistics.mean(success_rates),
            "average_user_rating": statistics.mean(user_ratings),
            "average_error_rate": statistics.mean(error_rates),
            "best_performer": max(self.expert_metrics.items(), key=lambda x: x[1].user_rating)[0],
            "needs_improvement": min(self.expert_metrics.items(), key=lambda x: x[1].user_rating)[0]
        }
    
    def _get_system_health_status(self) -> Dict[str, Any]:
        """Get overall system health status"""
        
        if not self.system_metrics_history:
            return {"status": "unknown"}
        
        latest = self.system_metrics_history[-1]
        
        # Determine health status
        status = "healthy"
        issues = []
        
        if latest.error_rate > 0.1:
            status = "degraded"
            issues.append("High error rate")
        
        if latest.average_response_time > 3.0:
            status = "degraded"
            issues.append("Slow response times")
        
        if latest.memory_usage > 0.8:
            status = "critical"
            issues.append("High memory usage")
        
        if latest.system_load > 0.9:
            status = "critical"
            issues.append("High system load")
        
        return {
            "status": status,
            "issues": issues,
            "uptime": latest.uptime_percentage,
            "load": latest.system_load,
            "memory": latest.memory_usage
        }
    
    def _get_top_performers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performing experts"""
        
        sorted_experts = sorted(
            self.expert_metrics.items(),
            key=lambda x: x[1].user_rating,
            reverse=True
        )
        
        top_performers = []
        for expert_name, metrics in sorted_experts[:limit]:
            top_performers.append({
                "expert_name": expert_name,
                "user_rating": metrics.user_rating,
                "success_rate": metrics.success_rate,
                "response_time": metrics.response_time,
                "total_interactions": metrics.total_interactions
            })
        
        return top_performers
    
    def _get_performance_trends(self) -> Dict[str, Any]:
        """Get performance trends over time"""
        
        if len(self.system_metrics_history) < 10:
            return {"message": "Insufficient data for trends"}
        
        recent = list(self.system_metrics_history)[-10:]
        older = list(self.system_metrics_history)[-20:-10] if len(self.system_metrics_history) >= 20 else []
        
        if not older:
            return {"message": "Insufficient historical data"}
        
        # Calculate trends
        recent_avg_response = statistics.mean([m.average_response_time for m in recent])
        older_avg_response = statistics.mean([m.average_response_time for m in older])
        
        recent_error_rate = statistics.mean([m.error_rate for m in recent])
        older_error_rate = statistics.mean([m.error_rate for m in older])
        
        response_trend = "improving" if recent_avg_response < older_avg_response else "degrading"
        error_trend = "improving" if recent_error_rate < older_error_rate else "degrading"
        
        return {
            "response_time_trend": response_trend,
            "error_rate_trend": error_trend,
            "recent_avg_response": recent_avg_response,
            "older_avg_response": older_avg_response,
            "recent_error_rate": recent_error_rate,
            "older_error_rate": older_error_rate
        }
    
    def _get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get active (unresolved) alerts"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT alert_type, expert_name, message, severity, timestamp
            FROM performance_alerts 
            WHERE resolved = FALSE 
            ORDER BY timestamp DESC 
            LIMIT 20
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        alerts = []
        for row in rows:
            alerts.append({
                "alert_type": row[0],
                "expert_name": row[1],
                "message": row[2],
                "severity": row[3],
                "timestamp": row[4]
            })
        
        return alerts
    
    def _get_resource_utilization(self) -> Dict[str, Any]:
        """Get current resource utilization"""
        
        if not self.system_metrics_history:
            return {}
        
        latest = self.system_metrics_history[-1]
        
        return {
            "cpu_usage": latest.system_load,
            "memory_usage": latest.memory_usage,
            "active_sessions": latest.active_sessions,
            "requests_per_minute": latest.requests_per_minute,
            "total_experts": latest.total_experts
        }
    
    def _get_quality_metrics(self) -> Dict[str, Any]:
        """Get quality metrics across the system"""
        
        if not self.expert_metrics:
            return {}
        
        # Calculate quality metrics
        user_ratings = [m.user_rating for m in self.expert_metrics.values()]
        success_rates = [m.success_rate for m in self.expert_metrics.values()]
        response_times = [m.response_time for m in self.expert_metrics.values()]
        
        # Quality score calculation
        quality_score = (
            statistics.mean(user_ratings) * 0.4 +
            statistics.mean(success_rates) * 100 * 0.4 +
            (1.0 / min(statistics.mean(response_times), 5.0)) * 5.0 * 0.2
        )
        
        return {
            "overall_quality_score": min(quality_score, 5.0),
            "average_user_rating": statistics.mean(user_ratings),
            "average_success_rate": statistics.mean(success_rates),
            "average_response_time": statistics.mean(response_times),
            "experts_above_4_rating": len([r for r in user_ratings if r >= 4.0]),
            "total_experts": len(user_ratings)
        }
    
    def _generate_expert_summary(self, expert_name: str, historical_data: List[Dict]) -> Dict[str, Any]:
        """Generate performance summary for expert"""
        
        if not historical_data:
            return {}
        
        # Calculate statistics
        response_times = [d["response_time"] for d in historical_data]
        success_rates = [d["success_rate"] for d in historical_data]
        user_ratings = [d["user_rating"] for d in historical_data]
        
        return {
            "avg_response_time": statistics.mean(response_times),
            "avg_success_rate": statistics.mean(success_rates),
            "avg_user_rating": statistics.mean(user_ratings),
            "total_interactions": historical_data[0]["total_interactions"],
            "performance_consistency": 1.0 - (statistics.stdev(response_times) if len(response_times) > 1 else 0),
            "improvement_trend": self._calculate_improvement_trend(historical_data)
        }
    
    def _generate_expert_recommendations(self, expert_name: str, historical_data: List[Dict]) -> List[str]:
        """Generate improvement recommendations for expert"""
        
        recommendations = []
        
        if not historical_data:
            return recommendations
        
        latest = historical_data[0]
        
        # Response time recommendations
        if latest["response_time"] > 3.0:
            recommendations.append("Focus on reducing response time through optimization")
        
        # Success rate recommendations
        if latest["success_rate"] < 0.9:
            recommendations.append("Improve task completion accuracy through better understanding")
        
        # User rating recommendations
        if latest["user_rating"] < 4.0:
            recommendations.append("Enhance user experience with more personalized and helpful responses")
        
        # Error rate recommendations
        if latest["error_rate"] > 0.1:
            recommendations.append("Review and fix common error patterns in responses")
        
        # Collaboration recommendations
        if latest["collaboration_effectiveness"] < 4.0:
            recommendations.append("Improve collaboration with other experts for better teamwork")
        
        return recommendations
    
    def _compare_expert_performance(self, expert_name: str) -> Dict[str, Any]:
        """Compare expert performance with peers"""
        
        if expert_name not in self.expert_metrics:
            return {}
        
        expert_metrics = self.expert_metrics[expert_name]
        
        # Calculate peer averages
        all_ratings = [m.user_rating for m in self.expert_metrics.values()]
        all_response_times = [m.response_time for m in self.expert_metrics.values()]
        all_success_rates = [m.success_rate for m in self.expert_metrics.values()]
        
        peer_avg_rating = statistics.mean(all_ratings)
        peer_avg_response_time = statistics.mean(all_response_times)
        peer_avg_success_rate = statistics.mean(all_success_rates)
        
        # Calculate percentiles
        rating_percentile = len([r for r in all_ratings if r <= expert_metrics.user_rating]) / len(all_ratings) * 100
        response_time_percentile = len([r for r in all_response_times if r >= expert_metrics.response_time]) / len(all_response_times) * 100
        
        return {
            "rating_vs_average": expert_metrics.user_rating - peer_avg_rating,
            "response_time_vs_average": peer_avg_response_time - expert_metrics.response_time,
            "success_rate_vs_average": expert_metrics.success_rate - peer_avg_success_rate,
            "rating_percentile": rating_percentile,
            "response_time_percentile": response_time_percentile,
            "overall_rank": len([r for r in all_ratings if r > expert_metrics.user_rating]) + 1
        }
    
    def _analyze_expert_trends(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """Analyze performance trends for expert"""
        
        if len(historical_data) < 5:
            return {"message": "Insufficient data for trend analysis"}
        
        # Split data
        mid_point = len(historical_data) // 2
        recent = historical_data[:mid_point]
        older = historical_data[mid_point:]
        
        # Calculate averages
        recent_rating = statistics.mean([d["user_rating"] for d in recent])
        older_rating = statistics.mean([d["user_rating"] for d in older])
        
        recent_response = statistics.mean([d["response_time"] for d in recent])
        older_response = statistics.mean([d["response_time"] for d in older])
        
        recent_success = statistics.mean([d["success_rate"] for d in recent])
        older_success = statistics.mean([d["success_rate"] for d in older])
        
        # Determine trends
        rating_trend = "improving" if recent_rating > older_rating else "declining"
        response_trend = "improving" if recent_response < older_response else "declining"
        success_trend = "improving" if recent_success > older_success else "declining"
        
        return {
            "rating_trend": rating_trend,
            "response_trend": response_trend,
            "success_trend": success_trend,
            "rating_change": recent_rating - older_rating,
            "response_time_change": older_response - recent_response,
            "success_rate_change": recent_success - older_success
        }
    
    def _calculate_improvement_trend(self, historical_data: List[Dict]) -> str:
        """Calculate overall improvement trend"""
        
        if len(historical_data) < 10:
            return "insufficient_data"
        
        # Compare first and last 5 records
        first_five = historical_data[-5:]
        last_five = historical_data[:5]
        
        first_avg_rating = statistics.mean([d["user_rating"] for d in first_five])
        last_avg_rating = statistics.mean([d["user_rating"] for d in last_five])
        
        if last_avg_rating > first_avg_rating + 0.2:
            return "strong_improvement"
        elif last_avg_rating > first_avg_rating + 0.1:
            return "moderate_improvement"
        elif last_avg_rating < first_avg_rating - 0.2:
            return "strong_decline"
        elif last_avg_rating < first_avg_rating - 0.1:
            return "moderate_decline"
        else:
            return "stable"
    
    def _background_monitoring(self):
        """Background thread for continuous monitoring"""
        
        while self.monitoring_active:
            try:
                # Record system metrics periodically
                if self.system_metrics_history:
                    latest = self.system_metrics_history[-1]
                    self.record_system_metrics(
                        active_sessions=latest.active_sessions,
                        requests_per_minute=latest.requests_per_minute,
                        system_load=latest.system_load,
                        memory_usage=latest.memory_usage
                    )
                
                time.sleep(60)  # Monitor every minute
                
            except Exception as e:
                print(f"Background monitoring error: {e}")
                time.sleep(60)
    
    def _load_historical_metrics(self):
        """Load historical metrics from database"""
        
        # Load recent expert metrics
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get latest metrics for each expert
        cursor.execute('''
            SELECT expert_name, response_time, success_rate, user_rating,
                   collaboration_effectiveness, knowledge_depth, adaptability_score,
                   task_completion_time, error_rate, total_interactions, timestamp
            FROM expert_metrics 
            WHERE (expert_name, timestamp) IN (
                SELECT expert_name, MAX(timestamp) 
                FROM expert_metrics 
                GROUP BY expert_name
            )
        ''')
        
        rows = cursor.fetchall()
        for row in rows:
            expert_name = row[0]
            self.expert_metrics[expert_name] = ExpertMetrics(
                expert_name=expert_name,
                response_time=row[1],
                success_rate=row[2],
                user_rating=row[3],
                collaboration_effectiveness=row[4],
                knowledge_depth=row[5],
                adaptability_score=row[6],
                task_completion_time=row[7],
                error_rate=row[8],
                total_interactions=row[9],
                last_updated=datetime.fromisoformat(row[10])
            )
        
        # Load recent system metrics
        cursor.execute('''
            SELECT * FROM system_metrics 
            ORDER BY timestamp DESC 
            LIMIT 100
        ''')
        
        rows = cursor.fetchall()
        for row in rows:
            system_metrics = SystemMetrics(
                total_experts=row[1],
                active_sessions=row[2],
                requests_per_minute=row[3],
                average_response_time=row[4],
                system_load=row[5],
                memory_usage=row[6],
                error_rate=row[7],
                uptime_percentage=row[8],
                timestamp=datetime.fromisoformat(row[0])
            )
            self.system_metrics_history.append(system_metrics)
        
        conn.close()

# Global performance analytics instance
performance_analytics = PerformanceAnalyticsDashboard()