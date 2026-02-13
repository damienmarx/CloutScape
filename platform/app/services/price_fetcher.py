"""
Price Intelligence Engine - Updated for Fixed Elite Rates ($0.17 Sell / $0.16 Buy)
"""
import asyncio
import json
import os
from datetime import datetime, timedelta
from app import db, redis_client
from app.models import PriceSnapshot
from decimal import Decimal

# Elite fixed rates as specified by the user
SELL_PRICE = Decimal('0.17')
BUY_PRICE = Decimal('0.16')

def calculate_our_price(competitor_prices=None):
    """Returns the fixed elite sell price"""
    return float(SELL_PRICE)

def update_prices():
    """Main function to update prices with fixed elite rates"""
    try:
        our_price = float(SELL_PRICE)
        buy_price = float(BUY_PRICE)
        
        # We still store a snapshot for history
        current_prices = {
            'our_price': our_price,
            'buy_price': buy_price,
            'competitor_prices': {}, # Competitor tracking disabled for fixed elite rates
            'average_competitor': 0.25, # Example average for savings calculation
            'savings_percent': 32.0, # Fixed savings display
            'updated_at': datetime.utcnow().isoformat(),
            'note': 'Bulk GP specialists'
        }
        
        redis_client.setex('current_prices', 3600, json.dumps(current_prices))
        redis_client.setex('our_price', 3600, str(our_price))
        
        # Save to database for history
        snapshot = PriceSnapshot(
            competitor='CloutScape Elite',
            price_per_m=our_price,
            our_price_per_m=our_price
        )
        db.session.add(snapshot)
        db.session.commit()
        
        return current_prices
        
    except Exception as e:
        print(f"Error updating prices: {e}")
        return None

def get_current_prices():
    """Get current prices from Redis cache"""
    cached = redis_client.get('current_prices')
    if cached:
        return json.loads(cached)
    
    return update_prices()

def get_price_history(days=7):
    """Get historical price data"""
    since = datetime.utcnow() - timedelta(days=days)
    snapshots = PriceSnapshot.query.filter(
        PriceSnapshot.created_at >= since
    ).order_by(PriceSnapshot.created_at.asc()).all()
    
    history = {}
    for snapshot in snapshots:
        timestamp = snapshot.created_at.isoformat()
        if timestamp not in history:
            history[timestamp] = {
                'our_price': float(snapshot.our_price_per_m),
                'competitors': {}
            }
    
    return history
