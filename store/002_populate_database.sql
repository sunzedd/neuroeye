/* INSERT INTO trpo_user(email, username, password) VALUES 
    ('user1@mail.ru', 'username1', 'username1password'),
    ('user2@mail.ru', 'username2', 'username2password'),
    ('user3@mail.ru', 'username3', 'username3password'),
    ('user4@mail.ru', 'username4', 'username4password'); */

INSERT INTO trpo_filter(url) VALUES
    ('filter/test1.f'),
    ('filter/test2.f'),
    ('filter/test3.f'),
    ('filter/test4.f');

INSERT INTO trpo_meta_image(url) VALUES
    ('img/user_img/src_1.jpeg'),
    ('img/user_img/dst_1.jpeg');

INSERT INTO trpo_filter_showcase(title, filter_id, src_img_id, dst_img_id) VALUES
    ('showcase1', 1, 1, 2);
