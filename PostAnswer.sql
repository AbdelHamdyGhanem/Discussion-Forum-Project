-- Allows a user to create a new question
DELIMITER //

CREATE PROCEDURE CreateTopic(
    IN p_user_id INT,
    IN p_title VARCHAR(255),
    IN p_content TEXT
)
BEGIN
    INSERT INTO questions (user_id, title, content)
    VALUES (p_user_id, p_title, p_content);
END //

DELIMITER ;