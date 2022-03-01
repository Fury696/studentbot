# TABLE: users
# COLUMNS: id, member, joined_timestamp, active_suspicions, total_suspicions, appraises
# Available SQL queries:
#   INSERT_INTO_USERS (userID int, boolean, timestamp)
#   UPDATE_USERS_LEFT_TIMESTAMP (timestamp, userID int)
#   UPDATE_USERS_ACTIVE_SUSPICIONS (int, userID int)
#   UPDATE_USERS_TOTAL_SUSPICIONS (int, userID int)
#   UPDATE_USERS_APPRAISES (int, userID int)
#   SELECT_ACTIVE_SUSPICIONS_FROM_USERS (userID int)
#   SELECT_TOTAL_SUSPICIONS_FROM_USERS (userID int)
#   SELECT_APPRAISES_FROM_USERS (userID int)
#   SELECT_ID_FROM_USERS (userID int)
CREATE_TABLE_USERS = '''
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    member BOOLEAN,
    joined_timestamp TIMESTAMP,
    left_timestamp TIMESTAMP,
    active_suspicions SMALLINT DEFAULT 0,
    total_suspicions INT DEFAULT 0,
    appraises SMALLINT DEFAULT 0
);
CREATE INDEX IF NOT EXISTS index_user_id ON users (user_id);
'''
INSERT_INTO_USERS = '''
INSERT INTO users (
    id, member, joined_timestamp
) VALUES ( $1, $2, $3 );
'''
UPDATE_USERS_LEFT_TIMESTAMP = '''
UPDATE users SET left_timestamp = $1 WHERE id = $2;
'''
UPDATE_USERS_ACTIVE_SUSPICIONS = '''
UPDATE users SET active_suspicions = $1 WHERE id = $2;
'''
UPDATE_USERS_TOTAL_SUSPICIONS = '''
UPDATE users SET total_suspicions = $1 WHERE id = $2;
'''
UPDATE_USERS_APPRAISES = '''
UPDATE users SET appraises = $1 WHERE id = $1;
'''
SELECT_ACTIVE_SUSPICIONS_FROM_USERS = '''
SELECT active_suspicions FROM users WHERE id = $1;
'''
SELECT_TOTAL_SUSPICIONS_FROM_USERS = '''
SELECT total_suspicions FROM users WHERE id = $1;
'''
SELECT_APPRAISES_FROM_USERS = '''
SELECT appraises FROM users WHERE id = $1;
'''
SELECT_ID_FROM_USERS = '''
SELECT id FROM users WHERE user_id = $1;
'''


# TABLE: collections
# COLUMNS: user_id, messages, bad_words, last_message_timestamp
# Available SQL queries:
#   INSERT_INTO_COLLECTIONS (userID)
#   UPDATE_COLLECTIONS_MESSAGES (int, userID int)
#   UPDATE_COLLECTIONS_BAD_WORDS (int, userID int)
#   UPDATE_COLLECTIONS_LAS_MESSAGE_TIMESTAMP (timestamp. userID int)
#   SELECT_MESSAGES_FROM_COLLECTIONS (userID)
#   SELECT_BAD_WORDS_FROM_COLLECTIONS (userID)
#   SELECT_LAST_MESSAGE_TIMESTAMP_FROM_COLLECTIONS (userID)
CREATE_TABLE_COLLECTIONS = '''
CREATE TABLE IF NOT EXISTS collections (
    user_id BIGINT PRIMARY KEY,
    messages BIGINT DEFAULT 0,
    bad_words INT DEFAULT 0,
    last_message_timestamp TIMESTAMP
);
CREATE INDEX IF NOT EXISTS index_collection_user_id ON collections (user_id);
'''
INSERT_INTO_COLLECTIONS = '''
INSERT INTO collections (
    user_id
) VALUES ( $1 );
'''
UPDATE_COLLECTIONS_MESSAGES = '''
UPDATE collections SET messages = $1 WHERE user_id $2;
'''
UPDATE_COLLECTIONS_BAD_WORDS = '''
UPDATE collections SET bad_words = $1 WHERE user_id $2;
'''
UPDATE_COLLECTIONS_LAST_MESSAGE_TIMESTAMP = '''
UPDATE collections SET last_message_timestamp = $1 WHERE user_id = $2;
'''
SELECT_MESSAGES_FROM_COLLECTIONS = '''
SELECT messages FROM collections WHERE user_id = $1;
'''
SELECT_BAD_WORDS_FROM_COLLECTIONS = '''
SELECT bad_words FROM collections WHERE user_id = $1;
'''
SELECT_LAST_MESSAGE_TIMESTAMP_FROM_COLLECTIONS = '''
SELECT last_message_timestamp FROM collections WHERE user_id = $1;
'''


# TABLE: reports
# COLUMNS: case, user_id, issuer_id, issue_timestamp, reason
# Available SQL queries:
#   INSERT_INTO_REPORTS (userID int, issuerID int, timestamp, reason str)
#   SELECT_ALL_FROM_REPORTS_WHERE_USER_ID (userID int)
#   SELECT_ALL_FROM_REPORTS_WHERE_CASE (case int)
CREATE_TABLE_REPORTS = '''
CREATE TABLE IF NOT EXISTS reports (
    case SERIAL PRIMARY KEY,
    user_id BIGINT,
    issuer_id BIGINT,
    issue_timestamp TIMESTAMP,
    reason MEDIUMTEXT
);
CREATE INDEX IF NOT EXISTS index_report_user_id ON reports (user_id);
CREATE INDEX IF NOT EXISTS index_report_issuer_id ON reports (issuer_id);
CREATE INDEX IF NOT EXISTS index_report_case ON reports (case);
'''
INSERT_INTO_REPORTS = '''
INSERT INTO reports (
    user_id,
    issuer_id,
    issue_timestamp,
    reason
) VALUES(
    $1, $2, $3, $4
) RETURNING case;
'''
SELECT_ALL_FROM_REPORTS_WHERE_USER_ID = '''
SELECT * FROM reports WHERE user_id = $1;
'''
SELECT_ALL_FROM_REPORTS_WHERE_CASE = '''
SELECT * FROM reports WHERE case = $1;
'''


# INFRACTIONS
CREATE_TABLE_INFRACTIONS = '''
CREATE TABLE IF NOT EXISTS infractions (
    case SERIAL PRIMARY KEY,
    user_id BIGINT,
    issuer_id BIGINT,
    issue_timestamp TIMESTAMP,
    expiry_timestamp TIMESTAMP,
    active BOOLEAN,
    action TINYTEXT,
    reason TEXT
);
CREATE INDEX IF NOT EXISTS index_infraction_user_id ON infractions (user_id);
CREATE INDEX IF NOT EXISTS index_infraction_case ON infractions (case);
CREATE INDEX IF NOT EXISTS index_infraction_action ON infractions (action);
'''
INSERT_INTO_INFRACTIONS = '''
INSERT INTO infractions (
    user_id,
    issuer_id,
    issue_timestamp,
    expiry_timestamp,
    active,
    action,
    reason
) VALUES (
    $1, $2, $3, $4, $5, $6, $7
) RETURNING case;
'''
UPDATE_INFRACTIONS_ACTIVE = '''
UPDATE infractions SET active = $1 WHERE case = $2;
'''
SELECT_ALL_FROM_INFRACTIONS_WHERE_CASE = '''
SELECT * FROM infractions WHERE case = $1;
'''
SELECT_ALL_FROM_INFRACTIONS_WHERE_USER_ID_AND_ACTION = '''
SELECT * FROM infractions WHERE user_id = $1 AND action = $2;
'''
SELECT_ALL_FROM_INFRACTIONS_WHERE_USER_ID = '''
SELECT * FROM infractions WHERE user_id = $1;
'''
DELETE_ALL_FROM_INFRACTIONS_WHERE_CASE = '''
DELETE FROM infractions WHERE case = $1;
'''
DELETE_ALL_FROM_INFRACTIONS_WHERE_USER_ID_AND_ACTION = '''
DELETE FROM infractions WHERE user_id = $1 AND action = $2
'''
DELETE_ALL_FROM_INFRACTIONS_WHERE_USER_ID = '''
DELETE FROM infractions WHERE user_id = $1;
'''
DELETE_ALL_FROM_INFRACTIONS = '''
DELETE FROM infractions;
'''


# WARNING: DANGEROUS QUERY
DELETE_ALL_FROM_INFRACTIONS = '''
DELETE FROM infractions;
DELETE FROM users;
DELETE FROM collections;
DELETE FROM reports;
'''
