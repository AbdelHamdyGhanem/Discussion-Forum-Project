DELIMITER //

CREATE PROCEDURE GetAnswersForTopic(
    IN p_topic_id INT
)
BEGIN
    SELECT * FROM answers WHERE topic_id = p_topic_id;
END //

DELIMITER ;
