CREATE PROCEDURE DeleteTopicByID(
        IN topic_id_param INT,
        IN username_param VARCHAR(255)
    )
    BEGIN
        DECLARE user_exists INT;
         
        -- Check the username table
        SELECT COUNT(*) INTO user_exists FROM Users WHERE username = username_param;
        
        -- If the username exists, delete the topic with that username and topic_id
        IF user_exists > 0 THEN
            DELETE FROM Topics WHERE topic_id = topic_id_param AND username = username_param;
        ELSE
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User does not exist';
        END IF;
    END //
