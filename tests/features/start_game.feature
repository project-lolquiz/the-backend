Feature: Starting a new game

  Scenario: Start a new game
    Given a room code
    And a full valid input for start the game
    When I request to start a new game
    Then I should get a 201 http response code
    And an empty response body