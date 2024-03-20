-- stored procedure for deleting a topic
DELIMITER //

CREATE PROCEDURE DeleteTopic(
    IN p_topic_id INT
)
BEGIN
    DELETE FROM topics WHERE topic_id = p_topic_id;
END //

DELIMITER ;
