# CloutScape AIO - Advanced Features Documentation

## 🎰 Gambling System

### Supported Games

#### 1. **Dice Rolls**
- Players roll 1-100
- Highest roll wins
- 2x payout on win
- Real-time statistics tracking

#### 2. **Flower Poker**
- 5-card hand evaluation
- Hand strength ranking (1-10)
- Multiplier-based payouts
- Win rate tracking

#### 3. **Blackjack**
- Player vs Dealer
- Bust detection
- Blackjack bonus (2.5x)
- Score calculation

#### 4. **Slot Machine**
- 3-reel spinner
- Symbol matching
- Jackpot detection (10x)
- Two-match bonus (3x)

#### 5. **Roulette**
- Number betting (36x payout)
- Color betting (2x payout)
- Odd/Even betting (2x payout)
- Realistic wheel simulation

### Gambling Statistics

- **Player Stats**: Total bets, winnings, profit, win rate
- **Game-Specific Stats**: Performance by game type
- **Leaderboards**: Top gamblers by profit, winnings, or win rate
- **Recent Games**: Last 10 games with full details
- **Overall Stats**: Total players, games, bets, winnings

### API Endpoints

```
GET /api/gambling/stats              - Overall gambling statistics
GET /api/gambling/leaderboard        - Top gamblers
GET /api/gambling/recent             - Recent games
GET /api/gambling/player/<id>        - Player statistics
```

---

## ⚔️ PvP Tracking System

### Features

#### Kill Logging
- Killer and victim tracking
- Location recording
- Weapon used
- Loot drops with values
- Timestamp recording

#### Player Statistics
- Total kills and deaths
- K/D ratio calculation
- Total loot earned
- Average loot per kill
- Kill streak tracking
- Best kill streak

#### Leaderboards
- Top killers
- Highest K/D ratios
- Biggest loot earners
- Kill hotspots

### Kill Hotspots

Identifies most dangerous locations:
- Number of kills at location
- Total loot value
- Average loot per kill

### API Endpoints

```
GET /api/pvp/stats                   - Overall PvP statistics
GET /api/pvp/leaderboard             - Top killers
GET /api/pvp/recent                  - Recent kills
GET /api/pvp/hotspots                - Kill hotspots
GET /api/pvp/player/<id>             - Player PvP stats
```

---

## 🎯 Event Management System

### Event Types

#### 1. **Giveaways**
- Prize pools
- Random winner selection
- Automatic notifications
- Participation tracking

#### 2. **Tournaments**
- Bracket management
- Round tracking
- Winner advancement
- Prize distribution

#### 3. **Raffles**
- Ticket-based entry
- Random drawing
- Prize assignment
- Winner notification

#### 4. **Contests**
- Submission tracking
- Voting system
- Scoring
- Leaderboard

### Event Features

- **Creation**: Set title, description, prizes, duration
- **Participation**: Track participants and entries
- **Winner Selection**: Automatic random selection
- **Prize Distribution**: Automatic reward assignment
- **Notifications**: Discord webhook alerts
- **Extension**: Extend event duration
- **Cancellation**: Cancel with reason

### Event Statistics

- Total events created
- Active events count
- Completed events
- Total prize pool value
- Participant count
- Average participants per event

### API Endpoints

```
GET /api/events/stats                - Event statistics
GET /api/events/active               - Active events
GET /api/events/completed            - Completed events
GET /api/events/leaderboard          - Participation leaderboard
GET /api/events/<id>                 - Event details
```

---

## 💰 Rewards & Economy System

### Currency Management

#### GP (Gold Points)
- Add GP to player balance
- Remove GP from balance
- Transfer between players
- Balance tracking

#### Items
- Add items to inventory
- Remove items
- Quantity tracking
- Rarity classification
- Value calculation

### Transactions

#### Transaction Types
- **Reward**: Admin rewards
- **Gamble Win**: Gambling winnings
- **Gamble Loss**: Gambling losses
- **Event Prize**: Event rewards
- **Purchase**: Item purchases
- **Transfer**: Player-to-player transfers
- **Admin**: Admin actions

#### Transaction History
- Per-player history
- All transactions view
- Timestamp tracking
- Balance snapshots

### Leaderboards

#### Wealth Leaderboard
- GP balance
- Inventory value
- Total wealth (GP + inventory)

#### Spending Leaderboard
- Total spent on gambling
- Total spent on purchases
- Average spending

### Economy Statistics

- Total players
- Total GP in circulation
- Total items in game
- Total inventory value
- Average player balance
- Total transactions

### API Endpoints

```
GET /api/rewards/stats               - Economy statistics
GET /api/rewards/leaderboard/wealth  - Wealth leaderboard
GET /api/rewards/leaderboard/spending - Spending leaderboard
GET /api/rewards/player/<id>         - Player summary
GET /api/rewards/transactions        - Transaction history
```

---

## 🔔 Webhook Notifications

### Notification Types

#### Gambling Notifications
- **Win Alert**: Player won with amount
- **Loss Alert**: Player lost with amount
- **Jackpot Alert**: Major win notification

#### PvP Notifications
- **Kill Alert**: Kill with loot value
- **Kill Streak**: Player on streak
- **Milestone**: Achievement reached

#### Event Notifications
- **Event Created**: New event announcement
- **Event Started**: Event begins
- **Event Ended**: Event completion
- **Winner Announced**: Winner notification

#### Reward Notifications
- **GP Received**: Currency reward
- **Item Received**: Item reward
- **Achievement Unlocked**: Achievement notification

#### System Notifications
- **System Message**: General announcements
- **Error Alert**: System errors
- **Maintenance**: Maintenance alerts

### Webhook Setup

```python
webhook_manager.set_webhook('gambling', 'https://discord.com/api/webhooks/...')
webhook_manager.set_webhook('pvp', 'https://discord.com/api/webhooks/...')
webhook_manager.set_webhook('event', 'https://discord.com/api/webhooks/...')
webhook_manager.set_webhook('reward', 'https://discord.com/api/webhooks/...')
webhook_manager.set_webhook('system', 'https://discord.com/api/webhooks/...')
```

---

## 📊 Dashboard Features

### Admin Dashboard

#### Gambling Dashboard
- Real-time betting activity
- Player statistics
- Game distribution
- Profit/loss tracking
- Leaderboards

#### PvP Dashboard
- Recent kills
- Kill hotspots
- Player rankings
- K/D ratios
- Loot tracking

#### Events Dashboard
- Active events
- Upcoming events
- Event statistics
- Participation tracking
- Prize pools

#### Economy Dashboard
- Wealth distribution
- Transaction history
- Player balances
- Inventory values
- Spending patterns

### Web Interface

- **Real-time Updates**: Live statistics
- **Responsive Design**: Mobile-friendly
- **Dark Theme**: Gaming aesthetic
- **Data Export**: JSON export capability
- **Admin Controls**: Full management interface

---

## 🔧 Configuration

### Environment Variables

```env
DISCORD_TOKEN=your_bot_token
ADMIN_ID=your_admin_id
FLASK_PORT=5000
FLASK_ENV=production
SECRET_KEY=your_secret_key
```

### System Configuration Files

- `gambling_config.json` - Gambling statistics
- `pvp_config.json` - PvP statistics
- `events_config.json` - Event data
- `rewards_config.json` - Economy data
- `bot_settings.json` - Bot configuration
- `server_config.json` - Server setup data

---

## 📈 Statistics & Analytics

### Gambling Analytics
- Win rates by game
- Average bet amounts
- Profit/loss trends
- Player retention
- Game popularity

### PvP Analytics
- Kill distribution
- Loot value trends
- Player activity
- Hotspot analysis
- Skill rankings

### Event Analytics
- Participation rates
- Prize pool distribution
- Event success metrics
- Participant engagement
- Reward distribution

### Economy Analytics
- Wealth distribution
- Transaction volume
- Player spending
- Item circulation
- Market trends

---

## 🚀 Advanced Features

### Automated Systems

- **Auto Winner Selection**: Random winner picking
- **Auto Rewards**: Automatic GP/item distribution
- **Auto Notifications**: Discord webhook alerts
- **Auto Leaderboards**: Real-time ranking updates
- **Auto Statistics**: Continuous data aggregation

### Customization

- **Custom Games**: Add new gambling games
- **Custom Events**: Create event types
- **Custom Rewards**: Define reward types
- **Custom Notifications**: Customize webhook messages
- **Custom Leaderboards**: Create custom rankings

### Integration

- **Discord Bot**: Full bot integration
- **Webhooks**: Real-time notifications
- **REST API**: Full API access
- **Database**: JSON-based storage
- **Web Dashboard**: Complete management UI

---

## 📝 Usage Examples

### Gambling

```python
from modules.gambling import GamblingSystem

gambling = GamblingSystem()

# Roll dice
result = gambling.roll_dice(
    player_id='123456',
    player_name='PlayerName',
    bet_amount=1000,
    player_roll=75,
    opponent_roll=45
)

# Get leaderboard
leaderboard = gambling.get_leaderboard(limit=10, sort_by='total_profit')
```

### PvP

```python
from modules.pvp import PvPSystem

pvp = PvPSystem()

# Log a kill
kill = pvp.log_kill(
    killer_id='123456',
    killer_name='Killer',
    victim_id='789012',
    victim_name='Victim',
    location='Duel Arena',
    loot=[{'name': 'Sword', 'value': 50000}],
    weapon='Sword'
)

# Get hotspots
hotspots = pvp.get_kill_hotspots(limit=5)
```

### Events

```python
from modules.events import EventSystem

events = EventSystem()

# Create event
event = events.create_event(
    event_id='event_001',
    event_type='giveaway',
    title='Weekly Giveaway',
    description='Win awesome prizes!',
    creator_id='123456',
    creator_name='Admin',
    prizes=[{'name': 'Gold', 'value': 100000}],
    duration_hours=24
)

# Select winners
winners = events.select_winners('event_001', num_winners=1)
```

### Rewards

```python
from modules.rewards import RewardSystem

rewards = RewardSystem()

# Add GP
transaction = rewards.add_gp(
    player_id='123456',
    player_name='Player',
    amount=50000,
    reason='Event Prize',
    source_id='event_001'
)

# Get wealth leaderboard
leaderboard = rewards.get_wealth_leaderboard(limit=10)
```

---

## 🔐 Security

- Admin authentication required
- Webhook URL validation
- Rate limiting
- Error handling
- Logging and auditing
- Data validation
- Input sanitization

---

## 📞 Support

For issues or feature requests, please refer to the main README.md or contact support.

---

**Version**: 1.0.0
**Last Updated**: February 2026
**Status**: Production Ready
