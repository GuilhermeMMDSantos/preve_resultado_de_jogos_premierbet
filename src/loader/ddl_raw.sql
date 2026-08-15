CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.matches (
    match_id        BIGINT PRIMARY KEY,
    season          INT NOT NULL,
    matchday        INT,
    utc_date        TIMESTAMPTZ,
    status          TEXT,
    home_team_id    INT,
    home_team_name  TEXT,
    away_team_id    INT,
    away_team_name  TEXT,
    home_score      INT,
    away_score      INT,
    winner          TEXT,
    raw_json        JSONB,
    ingested_at     DATE
);
 
CREATE TABLE IF NOT EXISTS raw.teams (
    team_id     INT NOT NULL,
    season      INT NOT NULL,
    name        TEXT,
    short_name  TEXT,
    tla         TEXT,
    raw_json    JSONB,
    ingested_at DATE,
    PRIMARY KEY (team_id, season)
);

CREATE TABLE IF NOT EXISTS raw.csv_matches (
    season_code           TEXT NOT NULL,
    match_date             DATE NOT NULL,
    home_team              TEXT NOT NULL,
    away_team              TEXT NOT NULL,
    full_time_home_goals   INT,
    full_time_away_goals   INT,
    full_time_result       TEXT,
    raw_json                JSONB,
    ingested_at             DATE,
    PRIMARY KEY (season_code, match_date, home_team, away_team)
);