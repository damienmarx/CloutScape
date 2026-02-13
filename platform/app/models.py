"""
Database models for CloutScape Platform
"""
import uuid
from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    discord_id = db.Column(db.String(100), unique=True, nullable=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)
    clout_points = db.Column(db.Integer, default=0)
    referral_code = db.Column(db.String(20), unique=True, nullable=True)
    referred_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    # New fields for bonuses and wagering
    balance_usd = db.Column(db.Numeric(10, 2), default=0.00)
    bonus_balance_usd = db.Column(db.Numeric(10, 2), default=0.00)
    total_wagered_usd = db.Column(db.Numeric(10, 2), default=0.00)
    challenge_active = db.Column(db.Boolean, default=False)
    challenge_wager_target = db.Column(db.Numeric(10, 2), default=50.00)
    challenge_reward_claimed = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True)
    gambling_logs = db.relationship('GamblingLog', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    amount_gp = db.Column(db.BigInteger, nullable=False)
    price_usd = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(
        db.Enum('pending', 'paid', 'processing', 'completed', 'refunded', name='order_status'),
        default='pending'
    )
    payment_method = db.Column(db.String(50), nullable=True)
    payment_tx = db.Column(db.String(255), nullable=True)
    in_game_rsn = db.Column(db.String(100), nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Order {self.id} - {self.status}>'


class PriceSnapshot(db.Model):
    __tablename__ = 'price_snapshots'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    competitor = db.Column(db.String(100), nullable=False)
    price_per_m = db.Column(db.Numeric(10, 2), nullable=False)
    our_price_per_m = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PriceSnapshot {self.competitor} - ${self.price_per_m}>'


class GamblingLog(db.Model):
    __tablename__ = 'gambling_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    game_type = db.Column(db.String(50), nullable=True)  # 'duel', 'staking', 'flower'
    amount_won = db.Column(db.BigInteger, default=0)
    amount_lost = db.Column(db.BigInteger, default=0)
    wager_value_usd = db.Column(db.Numeric(10, 2), default=0.00) # USD value of the wager
    screenshot_url = db.Column(db.String(500), nullable=True)
    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GamblingLog {self.user_id} - {self.game_type}>'
