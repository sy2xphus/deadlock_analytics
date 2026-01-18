# Deadlock API Reference

**Base URL**: `https://api.deadlock-api.com`

## Authentication
Most "Analytics" and "Info" endpoints allow access via IP-based rate limiting (typically 100 req/s).
Some specialized endpoints (like creating custom matches) require an API Key.
For our ETL pipeline, we will likely rely on the public IP quotas initially.

## Key Endpoints

### Matches
- **List Active Matches**: `GET /v1/matches/active`
  - Returns currently active matches (top 200).
- **Match Metadata**: `GET /v1/matches/{match_id}/metadata`
  -  Detailed stats for a specific match.
- **Player Match History**: `GET /v1/players/{account_id}/match-history`
  - Lists past matches for a player.

### Analytics & Stats
- **Hero Stats**: `GET /v1/analytics/hero-stats`
- **Item Stats**: `GET /v1/analytics/item-stats`
- **Leaderboard**: `GET /v1/leaderboard/{region}` (Regions: Europe, Asia, NAmerica, SAmerica, Oceania)

### Players
- **Player Card**: `GET /v1/players/card/{account_id}` (Deduced from standard patterns, verifying...)
- **MMR History**: `GET /v1/players/{account_id}/mmr-history`

## Data Structures
- **Account IDs**: SteamID3 format.
- **Match IDs**: Integer (int64).
