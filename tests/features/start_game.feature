Feature: Starting a new game

  Scenario: Start a new game
    Given a room code
    And a full valid input for start the game
    When I request to start a new game
    Then I should get a 201 http response code
    And an empty response body
    And I should not have a "selected_questions" node on the room

  Scenario: Start a new game without a valid room code
    Given a room with id "ZY11"
    And a full valid input for start the game
    When I request to start a new game
    Then I should get a 404 http response code
    And an error response body
    And an error message like "Room ID ZY11 not found"

  Scenario: Restart a new game after a question being requested
    Given a room code
    And a full valid input for start the game
    When I request to start a new game
    Then I should get a 201 http response code
    And an empty response body
    And I request a new question
    And I request to start a new game
    And I should have a "selected_questions" node on the room