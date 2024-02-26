DROP TABLE IF EXISTS trpo_session;
DROP TABLE IF EXISTS trpo_showcase_has_tag;
DROP TABLE IF EXISTS trpo_user_has_favourite_showcase;
DROP TABLE IF EXISTS trpo_showcase_view_count;
DROP TABLE IF EXISTS trpo_showcase;
DROP TABLE IF EXISTS trpo_tag;
DROP TABLE IF EXISTS trpo_image;
DROP TABLE IF EXISTS trpo_user;


CREATE TABLE trpo_image(
    id SERIAL PRIMARY KEY,
    url VARCHAR(128)
);

CREATE TABLE trpo_user(
    id SERIAL PRIMARY KEY,
    email VARCHAR(128),
    username VARCHAR(30),
    password_hash VARCHAR(256),
    userpic_id INT,

    FOREIGN KEY(userpic_id) REFERENCES trpo_image(id)
);

CREATE TABLE trpo_showcase(
    id SERIAL PRIMARY KEY,
    title VARCHAR(30),
    description VARCHAR(250),
    src_img_id INT,
    sample_img_id INT,
    dst_img_id INT,
    author_id INT,
    is_published INT,

    FOREIGN KEY(src_img_id) REFERENCES trpo_image(id), 
    FOREIGN KEY(sample_img_id) REFERENCES trpo_image(id), 
    FOREIGN KEY(dst_img_id) REFERENCES trpo_image(id),
    FOREIGN KEY(author_id) REFERENCES trpo_user(id)
);

CREATE TABLE trpo_tag(
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) UNIQUE
);

CREATE TABLE trpo_showcase_has_tag(
    showcase_id INT NOT NULL,
    tag_id INT NOT NULL,

    FOREIGN KEY(showcase_id) REFERENCES trpo_showcase ON DELETE CASCADE,
    FOREIGN KEY(tag_id) REFERENCES trpo_tag ON DELETE CASCADE,
    UNIQUE(showcase_id, tag_id)
);

CREATE TABLE trpo_user_has_favourite_showcase(
    showcase_id INT NOT NULL,
    user_id INT NOT NULL,

    FOREIGN KEY(showcase_id) REFERENCES trpo_showcase ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES trpo_user ON DELETE CASCADE,
    UNIQUE(showcase_id, user_id)
);

CREATE TABLE trpo_showcase_view_count(
    showcase_id INT NOT NULL,
    view_count INT DEFAULT 0,
    FOREIGN KEY(showcase_id) REFERENCES trpo_showcase ON DELETE CASCADE
)

CREATE TABLE trpo_session(
    id SERIAL PRIMARY KEY,
    user_id INT,
    expires_date TIMESTAMP,
    key VARCHAR(256) UNIQUE,
    is_expired INT,

    FOREIGN KEY(user_id) REFERENCES trpo_user
);
