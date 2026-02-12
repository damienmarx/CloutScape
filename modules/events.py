"""
CloutScape AIO - Event Management System
Handles giveaways, tournaments, raffles, and rewards
"""

import json
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class EventType(Enum):
    """Event types"""
    GIVEAWAY = "giveaway"
    TOURNAMENT = "tournament"
    RAFFLE = "raffle"
    CONTEST = "contest"

class EventStatus(Enum):
    """Event status"""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class EventSystem:
    """Advanced event management system"""
    
    def __init__(self, config_file: str = 'events_config.json'):
        self.config_file = config_file
        self.events: Dict[str, Dict] = {}
        self.load_config()
    
    def load_config(self):
        """Load event configuration"""
        try:
            with open(self.config_file, 'r') as f:
                self.events = json.load(f)
        except FileNotFoundError:
            self.events = {}
            self.save_config()
    
    def save_config(self):
        """Save event configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.events, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving events config: {e}")
    
    def create_event(self, event_id: str, event_type: str, title: str,
                    description: str, creator_id: str, creator_name: str,
                    prizes: List[Dict], duration_hours: int = 24,
                    entry_requirement: Optional[Dict] = None) -> Dict:
        """
        Create a new event
        
        Args:
            event_id: Unique event ID
            event_type: Type of event (giveaway, tournament, etc.)
            title: Event title
            description: Event description
            creator_id: Discord ID of creator
            creator_name: Name of creator
            prizes: List of prizes
            duration_hours: Duration in hours
            entry_requirement: Entry requirements (min level, etc.)
        
        Returns:
            Created event
        """
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=duration_hours)
        
        event = {
            'id': event_id,
            'type': event_type,
            'title': title,
            'description': description,
            'creator_id': creator_id,
            'creator_name': creator_name,
            'status': EventStatus.PENDING.value,
            'prizes': prizes,
            'total_prize_value': sum(p.get('value', 0) for p in prizes),
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_hours': duration_hours,
            'entry_requirement': entry_requirement or {},
            'participants': [],
            'winners': [],
            'created_at': start_time.isoformat()
        }
        
        self.events[event_id] = event
        self.save_config()
        
        logger.info(f"Created event: {title} (ID: {event_id})")
        return event
    
    def add_participant(self, event_id: str, player_id: str, player_name: str) -> bool:
        """Add participant to event"""
        if event_id not in self.events:
            return False
        
        event = self.events[event_id]
        
        # Check if already participating
        if any(p['id'] == player_id for p in event['participants']):
            return False
        
        event['participants'].append({
            'id': player_id,
            'name': player_name,
            'joined_at': datetime.now().isoformat()
        })
        
        self.save_config()
        return True
    
    def select_winners(self, event_id: str, num_winners: int = 1) -> List[Dict]:
        """
        Select random winners from participants
        
        Args:
            event_id: Event ID
            num_winners: Number of winners to select
        
        Returns:
            List of winners
        """
        if event_id not in self.events:
            return []
        
        event = self.events[event_id]
        
        if len(event['participants']) < num_winners:
            num_winners = len(event['participants'])
        
        winners = random.sample(event['participants'], num_winners)
        
        event['winners'] = winners
        event['status'] = EventStatus.COMPLETED.value
        
        self.save_config()
        
        logger.info(f"Selected {num_winners} winners for event: {event_id}")
        return winners
    
    def award_prizes(self, event_id: str) -> Dict:
        """
        Award prizes to winners
        
        Returns:
            Award summary
        """
        if event_id not in self.events:
            return {}
        
        event = self.events[event_id]
        awards = []
        
        for i, winner in enumerate(event['winners']):
            if i < len(event['prizes']):
                prize = event['prizes'][i]
                awards.append({
                    'winner_id': winner['id'],
                    'winner_name': winner['name'],
                    'prize': prize,
                    'awarded_at': datetime.now().isoformat()
                })
        
        event['awards'] = awards
        self.save_config()
        
        return {
            'event_id': event_id,
            'total_awards': len(awards),
            'awards': awards
        }
    
    def get_event(self, event_id: str) -> Optional[Dict]:
        """Get event details"""
        return self.events.get(event_id)
    
    def get_active_events(self) -> List[Dict]:
        """Get all active events"""
        active = []
        now = datetime.now()
        
        for event in self.events.values():
            end_time = datetime.fromisoformat(event['end_time'])
            if end_time > now and event['status'] in [EventStatus.PENDING.value, EventStatus.ACTIVE.value]:
                active.append(event)
        
        return sorted(active, key=lambda x: x['end_time'])
    
    def get_completed_events(self, limit: int = 10) -> List[Dict]:
        """Get completed events"""
        completed = [e for e in self.events.values() if e['status'] == EventStatus.COMPLETED.value]
        return sorted(completed, key=lambda x: x['created_at'], reverse=True)[:limit]
    
    def get_event_stats(self) -> Dict:
        """Get event statistics"""
        total_events = len(self.events)
        active_events = len(self.get_active_events())
        completed_events = len([e for e in self.events.values() if e['status'] == EventStatus.COMPLETED.value])
        
        total_prize_value = sum(e.get('total_prize_value', 0) for e in self.events.values())
        total_participants = sum(len(e.get('participants', [])) for e in self.events.values())
        
        return {
            'total_events': total_events,
            'active_events': active_events,
            'completed_events': completed_events,
            'total_prize_value': total_prize_value,
            'total_participants': total_participants,
            'average_participants': total_participants / max(1, total_events)
        }
    
    def cancel_event(self, event_id: str, reason: str = "") -> bool:
        """Cancel an event"""
        if event_id not in self.events:
            return False
        
        event = self.events[event_id]
        event['status'] = EventStatus.CANCELLED.value
        event['cancellation_reason'] = reason
        event['cancelled_at'] = datetime.now().isoformat()
        
        self.save_config()
        logger.info(f"Cancelled event: {event_id} - Reason: {reason}")
        return True
    
    def extend_event(self, event_id: str, additional_hours: int) -> bool:
        """Extend event duration"""
        if event_id not in self.events:
            return False
        
        event = self.events[event_id]
        end_time = datetime.fromisoformat(event['end_time'])
        new_end_time = end_time + timedelta(hours=additional_hours)
        
        event['end_time'] = new_end_time.isoformat()
        event['duration_hours'] += additional_hours
        
        self.save_config()
        logger.info(f"Extended event: {event_id} by {additional_hours} hours")
        return True
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get event participation leaderboard"""
        participants = {}
        
        for event in self.events.values():
            for participant in event.get('participants', []):
                p_id = participant['id']
                if p_id not in participants:
                    participants[p_id] = {
                        'id': p_id,
                        'name': participant['name'],
                        'events_participated': 0,
                        'events_won': 0,
                        'prizes_won': 0
                    }
                
                participants[p_id]['events_participated'] += 1
                
                if participant in event.get('winners', []):
                    participants[p_id]['events_won'] += 1
                    participants[p_id]['prizes_won'] += len(event.get('awards', []))
        
        sorted_participants = sorted(
            participants.values(),
            key=lambda x: x['events_won'],
            reverse=True
        )
        
        return sorted_participants[:limit]
