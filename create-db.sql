CREATE TABLE post
(
    -- 为 NULL 代表是主串
    parent_id INTEGER NULL,

    id INTEGER NOT NULL,
    attachment_path TEXT NULL,
    created_at_since_epoch INTEGER NOT NULL,
    user_id TEXT NOT NULL,
    name TEXT NULL,
    email TEXT NULL,
    title TEXT NULL,
    content TEXT NULL,
    marked_sage INTEGER NOT NULL,
    marked_admin INTEGER NOT NULL,
    leftover_json TEXT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (parent_id) REFERENCES post(id)
);
CREATE INDEX idx_post_created_at_since_epoch ON post(created_at_since_epoch);
CREATE INDEX idx_post_parent_id ON post(parent_id);

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
    FOREIGN KEY (thread_id) REFERENCES post(id),
    UNIQUE(thread_id, from_page)
);