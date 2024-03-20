-- stored procedure for topic
DELIMITER //

CREATE PROCEDURE CreateTopic(
    IN p_user_id INT,
    IN p_topic_title VARCHAR(255),
    IN p_content TEXT
)
BEGIN
    INSERT INTO topics (user_id, topic_title, content) VALUES (p_user_id, p_topic_title, p_content);
END //

DELIMITER ;

/*
-- table for topic
CREATE TABLE topics (
    topic_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    topic_title VARCHAR(255),
    content TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
*/
