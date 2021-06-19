Feature: Managing a game room

  Scenario: Create a new game room
    Given a full valid input for new room
    When I request to crate a new room
    Then I should get a 201 http response code
    And I should get a new room code