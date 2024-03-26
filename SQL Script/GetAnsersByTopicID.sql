CREATE PROCEDURE GetAnswersByTopicID(
    IN topic_id_param INT
    )
    BEGIN
    SELECT * FROM Answers WHERE topic_id = topic_id_param;
    END //
