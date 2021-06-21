Feature: Starting a new game

  Scenario: Start a new game
    Given a room code
    And a full valid input for start the game
    When I request to start a new game
    Then I should get a 201 http response code
    And an empty response body

  Scenario: Start a new game without a valid room code
    Given a room with id "ZY11"
    And a full valid input for start the game
    When I request to start a new game
    Then I should get a 404 http response code
    And an error response body
    And an error message like "Room ID ZY11 not found"