CREATE TABLE thread
(
    id INTEGER NOT NULL,
    created_at_utc INTEGER NOT NULL,
    user_id TEXT NOT NULL,
    raw TEXT NOT NULL,

    PRIMARY KEY(id)
);

CREATE TABLE post
(
    id INTEGER NOT NULL,
    thread_id INTEGER NOT NULL,
    created_at_utc INTEGER NOT NULL,
    user_id TEXT NOT NULL,
    raw TEXT NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (thread_id) REFERENCES thread(id)
);
CREATE INDEX idx_post_thread_id ON post(thread_id);

CREATE TABLE board_collected_datetime_range
(
    from_utc INTEGER,
    to_utc INTEGER
);
CREATE INDEX idx_board_collected_id_range_from_id ON board_collected_datetime_range(from_utc);
CREATE INDEX idx_board_collected_id_range_to_id ON board_collected_datetime_range(to_utc);

CREATE TABLE thread_collected_page_range
(
    thread_id INTEGER,

    from_page INTEGER,
    to_page INTEGER,
    to_page_max_post_id INTEGER,

    PRIMARY KEY (thread_id),
    FOREIGN KEY (thread_id) REFERENCES thread(id),
    UNIQUE(thread_id, from_page)
);