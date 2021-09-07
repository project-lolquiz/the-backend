Feature: Game question

  Scenario: Get a new question
    Given I request to create a new room with
      | game_type | game_mode | host_user_uid                        | host_user_nickname | total_rounds |
      | 2         | 1         | 48f51f68-9337-4d91-abdb-4bd5feebf1ac | Handsome Guy       | 3            |
    And I request to start a new game with users
      | uid                                  | nickname |
      | a362d801-908a-4d67-b82c-078068269654 | User 1   |
      | d3dce936-66a6-4653-ad36-335110249c86 | User 2   |
    When I request a new question
    Then I should get a 200 http response code
    And I should get a valid question