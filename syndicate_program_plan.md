# The Syndicate Program: Detailed Referral System Plan

## 1. Program Overview

**The Syndicate Program** is CloutScape's exclusive referral system designed to reward loyal players for expanding our elite community. By inviting new members to the platform, Syndicate members earn a percentage of the house edge from their referrals' gambling activity, fostering a mutually beneficial ecosystem. This program transforms active players into valued partners, driving growth and engagement through a tiered reward structure.

## 2. Syndicate Tiers and Commission Structure

The program operates on a progressive tier system, where higher tiers unlock greater commission rates and exclusive benefits. Advancement through tiers is based on the **Total Referred Wager (TRW)**, which is the cumulative amount of GP wagered by all directly referred players.

| Tier       | Total Referred Wager (TRW) Requirement | Commission Rate (on House Edge) | Exclusive Benefits                                                                                                                               |
| :--------- | :------------------------------------- | :------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------- |
| **Recruit**    | 0 GP                                   | 5%                              | - Unique Referral Code<br>- Basic Dashboard Access                                                                                      |
| **Agent**      | 100M GP                                | 7.5%                            | - Recruit Benefits<br>- Priority Support<br>- Exclusive Discord Role (`@Agent`)                                                         |
| **Enforcer**   | 500M GP                                | 10%                             | - Agent Benefits<br>- Monthly GP Bonus (based on performance)<br>- Early Access to New Games/Features<br>- Exclusive Discord Role (`@Enforcer`) |
| **Kingpin**    | 2B GP                                  | 12.5%                           | - Enforcer Benefits<br>- Dedicated Account Manager<br>- Custom In-Game Title<br>- Exclusive Discord Role (`@Kingpin`)                    |
| **Overlord**   | 10B GP                                 | 15%                             | - Kingpin Benefits<br>- Invitation to Private Alpha Tests<br>- Annual Real-World Merchandise Package<br>- Exclusive Discord Role (`@Overlord`) |

*   **House Edge**: The commission is calculated as a percentage of the house edge generated from referred players' bets, not their total wager. For example, if a game has a 2% house edge, a 5% commission means the referrer earns 5% of that 2%.
*   **Payout Frequency**: Commissions will be calculated and distributed weekly, directly to the Syndicate member's CloutScape GP balance.
*   **Active Referrals**: To maintain tier status and receive commissions, Syndicate members must have at least one active referred player (a player who has wagered GP within the last 30 days).

## 3. Referral Tracking and Attribution

Referrals are tracked using unique, permanent referral codes. When a new player registers on CloutScape.org using a Syndicate member's code, they are permanently linked to that referrer. This ensures that all future wagering activity from the referred player contributes to the referrer's TRW and commission earnings.

*   **Code Usage**: New players must enter the referral code during the registration process. Post-registration attribution will not be supported to maintain system integrity.
*   **First-Touch Attribution**: The system will operate on a first-touch attribution model; if a player uses multiple codes, only the first one entered will be valid.

## 4. Technical Implementation & Database Schema

To support The Syndicate Program, the following modifications and additions to the existing backend and database schema are required:

### Database Schema Additions (to `player_accounts.json` or a dedicated `referrals` table):

| Field Name           | Data Type | Description                                                                                               |
| :------------------- | :-------- | :-------------------------------------------------------------------------------------------------------- |
| `referral_code`      | String    | Unique code assigned to each Syndicate member (e.g., `CS-XYZ123`).                                         |
| `referred_by_code`   | String    | The `referral_code` of the player who referred this account. Null if not referred.                        |
| `total_referred_wager` | Integer   | Cumulative GP wagered by all direct referrals of this player. Used for tier advancement.                  |
| `syndicate_tier`     | String    | Current Syndicate tier of the player (e.g., "Recruit", "Agent").                                        |
| `last_commission_payout` | Datetime  | Timestamp of the last commission payout for this player.                                                  |
| `earned_commissions` | Integer   | Total commissions earned by this player (cumulative).                                                     |

### Backend Logic (Modifications to `app.py` and `rsps_integration.py`):

1.  **Registration Flow**: Modify the `/api/auth/register` endpoint to accept an optional `referred_by_code` parameter. Upon successful registration, update the `referred_by_code` for the new player and initialize their `syndicate_tier` to "Recruit" if they were referred.
2.  **Wager Tracking**: Enhance the `/api/games/bet` endpoint. After a bet is processed, identify the referrer of the player who placed the bet. Calculate the house edge from that bet and add the corresponding commission amount to the referrer's `total_referred_wager`.
3.  **Commission Calculation & Payout**: Implement a scheduled task (e.g., a cron job) that runs weekly:
    *   Iterate through all Syndicate members.
    *   Calculate their commission based on the `total_referred_wager` accumulated since the `last_commission_payout` and their current `syndicate_tier`'s rate.
    *   Add the calculated GP to the Syndicate member's `gp_balance` using `rsps.add_gp()`.
    *   Update `last_commission_payout` and `earned_commissions` fields.
    *   Check `total_referred_wager` against tier requirements and promote players to higher tiers if eligible.
4.  **Syndicate Dashboard API**: Create new API endpoints (e.g., `/api/syndicate/dashboard`, `/api/syndicate/referrals`) to allow Syndicate members to view their:
    *   Current tier and progress to the next tier.
    *   List of referred players and their activity.
    *   Total commissions earned and pending payouts.
    *   Unique referral code.

### Frontend Integration (Modifications to `index.html` and `games.js`):

1.  **Registration Form**: Add an optional input field for the `referral_code` in the `auth-modal`.
2.  **Syndicate Dashboard Tab**: Create a new tab in the main UI (similar to Deposit/Withdraw) that displays the Syndicate member's dashboard, showing their tier, earnings, and referral code.
3.  **Dynamic UI Updates**: Update the Syndicate dashboard dynamically via the new API endpoints.

## 5. Marketing Hooks & Recruitment Materials

### Messaging: "Join the Elite. Build Your Empire."

*   **Headline**: "Don't Just Play. Profit. Join The CloutScape Syndicate."
*   **Benefit-Driven**: "Turn your network into net worth. Earn passive GP from every bet your referrals make."
*   **Exclusivity**: "Only the most ambitious players are invited to build their Syndicate. Are you ready to lead?"

### Recruitment Channels:

*   **In-Game Announcements**: Regular broadcasts encouraging players to join the Syndicate.
*   **Discord**: Dedicated #syndicate-lounge channel for members, with automated messages for tier promotions and payout notifications.
*   **Social Media (X, TikTok)**: Short, punchy videos showcasing Syndicate members' earnings and the ease of referral.
*   **Dedicated Landing Page**: A simple page explaining the program benefits and how to join, linked from the main site.

### Visual Assets:

*   **Banners**: High-contrast, neon-themed banners for the website and social media, featuring phrases like "Earn Passive GP" and "Your Network, Your Net Worth."
*   **Infographics**: Simple, clear infographics explaining the tiered commission structure and how to get started.
*   **Video Snippets**: Short, dynamic video ads for TikTok/Reels demonstrating the earning potential.

## 6. Anti-Fraud Measures

*   **Self-Referral Prevention**: Implement checks to prevent users from referring themselves.
*   **IP/Device Tracking**: Monitor for suspicious activity (e.g., multiple accounts from the same IP address using referral codes).
*   **Manual Review**: Flag and manually review accounts with unusually high referral activity or suspicious wagering patterns.

This detailed plan provides a robust framework for implementing and promoting The Syndicate Program, transforming CloutScape into a community-driven growth engine. By rewarding players for their loyalty and outreach, we will significantly expand our user base and enhance platform engagement.
