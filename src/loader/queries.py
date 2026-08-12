UPSERT_MATCHES = """
    INSERT INTO raw.matches(
        match_id, season, matchday, utc_date, status,
        home_team_id, home_team_name, away_team_id, away_team_name,
        home_score, away_score, winner, raw_json, ingested_at
    ) VALUES %s
    ON CONFLICT(match_id) DO UPDATE SET
        utc_date = EXCLUDED.utc_date,
        status = EXCLUDED.status,
        home_score = EXCLUDED.home_score,
        away_score = EXCLUDED.away_score,
        winner = EXCLUDED.winner,
        raw_json = EXCLUDED.raw_json,
        ingested_at = EXCLUDED.ingested_at

"""

UPSERT_TEAMS = """
    INSERT INTO raw.teams(team_id, season, name, short_name, tla, raw_json, ingested_at) VALUES %s
    ON CONFLICT(team_id, season) DO UPDATE SET
        name = EXCLUDED.name,
        short_name = EXCLUDED.short_name,
        tla = EXCLUDED.tla,
        raw_json = EXCLUDED.raw_json,
        ingested_at = EXCLUDED.ingested_at
"""