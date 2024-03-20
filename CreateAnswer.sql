-- stored procedure for creating answers
DELIMITER //

CREATE PROCEDURE CreateAnswer(
    IN p_user_id INT,
    IN p_topic_id INT,
    IN p_content TEXT
)
BEGIN
    INSERT INTO answers (user_id, topic_id, content) VALUES (p_user_id, p_topic_id, p_content);
END //

DELIMITER ;

/* 
--- table for answers ---
CREATE TABLE answers (
    answer_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    topic_id INT,
    content TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
);
*/
