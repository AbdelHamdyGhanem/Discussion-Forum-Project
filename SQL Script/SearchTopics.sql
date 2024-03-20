DELIMITER //

CREATE PROCEDURE SearchTopics(
    IN p_search_query VARCHAR(255)
)
BEGIN
    SELECT * FROM topics WHERE topic_title LIKE CONCAT('%', p_search_query, '%');
END //

DELIMITER ;
