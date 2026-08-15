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

UPSERT_CSV_MATCHES = """
    INSERT INTO raw.csv_matches (
        season_code, match_date, home_team, away_team,
        full_time_home_goals, full_time_away_goals, full_time_result,
        raw_json, ingested_at
    ) VALUES %s
    ON CONFLICT (season_code, match_date, home_team, away_team) DO UPDATE SET
        full_time_home_goals = EXCLUDED.full_time_home_goals,
        full_time_away_goals = EXCLUDED.full_time_away_goals,
        full_time_result = EXCLUDED.full_time_result,
        raw_json = EXCLUDED.raw_json,
        ingested_at = EXCLUDED.ingested_at;
"""