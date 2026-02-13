"""
API endpoints for CloutScape Platform - Enhanced with Wagering & Bonuses
"""
from flask import Blueprint, jsonify, request, session, abort
from app import db, limiter
from app.models import Order, User, GamblingLog
from app.services.price_fetcher import get_current_prices
from app.utils.security import login_required
from app.services.telegram_bot import send_notification as send_telegram_notification
from app.services.discord_bot import send_discord_notification
import uuid
import os
import asyncio
from decimal import Decimal

api_bp = Blueprint('api', __name__)

# Constants for the new pricing and bonus logic
SELL_PRICE = Decimal('0.17')
BUY_PRICE = Decimal('0.16')
CHALLENGE_WAGER_TARGET = Decimal('50.00')
CHALLENGE_REWARD = Decimal('5.00')


@api_bp.route('/prices/live', methods=['GET'])
@limiter.limit("60 per minute")
def get_live_prices():
    """Get current live prices (Updated with fixed rates)"""
    return jsonify({
        'our_price': float(SELL_PRICE),
        'buy_price': float(BUY_PRICE),
        'currency': 'USD',
        'unit': '1M GP',
        'note': 'Bulk GP specialists'
    }), 200


@api_bp.route('/user/challenge', methods=['GET'])
@login_required
def get_challenge_status():
    """Get the current user's wagering challenge status"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    return jsonify({
        'active': user.challenge_active,
        'target': float(user.challenge_wager_target),
        'current_progress': float(user.total_wagered_usd),
        'reward_claimed': user.challenge_reward_claimed,
        'percent_complete': float((user.total_wagered_usd / user.challenge_wager_target) * 100) if user.challenge_wager_target > 0 else 0
    }), 200


@api_bp.route('/stake/log', methods=['POST'])
@login_required
def log_stake():
    """Log a stake and update wagering progress"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    data = request.get_json()
    
    if not data or 'amount_gp' not in data:
        return jsonify({'error': 'Missing amount_gp'}), 400
        
    amount_gp = Decimal(str(data['amount_gp']))
    usd_value = (amount_gp / Decimal('1000000')) * SELL_PRICE
    
    # Create log
    log = GamblingLog(
        user_id=user.id,
        game_type=data.get('game_type', 'discord_game'),
        amount_won=data.get('amount_won', 0),
        amount_lost=data.get('amount_lost', 0),
        wager_value_usd=usd_value,
        approved=True # Auto-approve for demo/discord games
    )
    
    # Update user wagering
    user.total_wagered_usd += usd_value
    
    # Check if challenge completed
    challenge_completed = False
    if not user.challenge_reward_claimed and user.total_wagered_usd >= user.challenge_wager_target:
        user.balance_usd += CHALLENGE_REWARD
        user.challenge_reward_claimed = True
        challenge_completed = True
        
    db.session.add(log)
    db.session.commit()
    
    if challenge_completed:
        msg = f"🎉 **Challenge Completed!** {user.username} has wagered ${user.total_wagered_usd:.2f} and claimed their $5 reward!"
        asyncio.run(send_discord_notification(msg))
        
    return jsonify({
        'status': 'success',
        'wager_usd': float(usd_value),
        'total_wagered': float(user.total_wagered_usd),
        'challenge_completed': challenge_completed
    }), 200


@api_bp.route('/orders', methods=['POST'])
@login_required
def create_order():
    """Create a new gold order with 50% sign-up bonus logic"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    data = request.get_json()
    
    if not data or 'amount_gp' not in data:
        return jsonify({'error': 'Missing amount_gp'}), 400
        
    amount_gp = Decimal(str(data['amount_gp']))
    total_usd = (amount_gp / Decimal('1000000')) * SELL_PRICE
    
    # Check for first deposit bonus (50%)
    is_first_order = Order.query.filter_by(user_id=user.id).count() == 0
    bonus_amount = Decimal('0.00')
    if is_first_order:
        bonus_amount = total_usd * Decimal('0.50')
        user.bonus_balance_usd += bonus_amount
    
    order = Order(
        id=str(uuid.uuid4()),
        user_id=user.id,
        amount_gp=int(amount_gp),
        price_usd=total_usd,
        status='pending',
        in_game_rsn=data.get('in_game_rsn')
    )
    
    db.session.add(order)
    db.session.commit()
    
    message = f"🛒 **New Order**\nUser: {user.username}\nAmount: {amount_gp:,} GP\nTotal: ${total_usd:.2f}"
    if is_first_order:
        message += f"\n🎁 **50% First Deposit Bonus Applied:** +${bonus_amount:.2f} to bonus balance!"
        
    asyncio.run(send_discord_notification(message))
    
    return jsonify({
        'order_id': order.id,
        'total_usd': float(total_usd),
        'bonus_applied': float(bonus_amount) if is_first_order else 0,
        'status': order.status
    }), 201
