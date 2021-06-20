Feature: Managing a game room

  Scenario: Create a new game room
    Given a full valid input for new room
    When I request to create a new room
    Then I should get a 201 http response code
    And I should get a new room code

  Scenario: Checks whether room exists
    Given a room code
    When I request to check the existence of this room code
    Then I should get a 200 http response code
    And I should get the the exists response as "True"

  Scenario: Checks whether room exists, with invalid room id
    Given a room with id "ZY10"
    When I request to check the existence of this room code
    Then I should get a 200 http response code
    And I should get the the exists response as "False"