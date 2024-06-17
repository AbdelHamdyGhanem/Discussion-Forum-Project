CREATE PROCEDURE GetTopicByID(
        IN topic_id_param INT
    )
    BEGIN
        SELECT * FROM Topics WHERE topic_id = topic_id_param;
    END //