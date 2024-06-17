CREATE PROCEDURE InsertTopic(
        IN title_param VARCHAR(255),
        IN description_param TEXT,
        IN username_param VARCHAR(255)
    )
    BEGIN
        DECLARE user_exists INT;
        
        -- Check if the user table for username
        SELECT COUNT(*) INTO user_exists FROM Users WHERE username = username_param;
        
        -- If the username exists, insert the topic
        IF user_exists > 0 THEN
            INSERT INTO Topics (title, description, username) VALUES (title_param, description_param, username_param);
        ELSE
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User does not exist';
        END IF;
    END //
