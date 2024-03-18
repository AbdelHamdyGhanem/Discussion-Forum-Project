-- Retrieves all topics/questions posted by a specific user
DELIMITER //

CREATE PROCEDURE GetUserTopics(
    IN p_user_id INT
)
BEGIN
    SELECT * FROM questions WHERE user_id = p_user_id;
END //

DELIMITER ;