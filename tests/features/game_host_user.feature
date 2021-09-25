Feature: Changing a host user

  Scenario: Change a host user with empty selected users list
    Given I request to create a new room with
      | game_type | game_mode | host_user_uid                        | host_user_nickname | total_rounds |
      | 2         | 1         | 48f51f68-9337-4d91-abdb-4bd5feebf1ac | Handsome Guy       | 3            |
    And I request to start a new game with users
      | uid                                  | nickname |
      | a362d801-908a-4d67-b82c-078068269654 | User 1   |
      | d3dce936-66a6-4653-ad36-335110249c86 | User 2   |
    And there is a selected users list
    When I request to set the new host user as
      | uid                                  | nickname |
      | a362d801-908a-4d67-b82c-078068269654 | User 1   |
    Then I should get a 204 http response code
    And there will be only 2 users in the game
    And there will be only 0 users in the selected users list
    And the host user is not
      | uid                                  | nickname     |
      | 48f51f68-9337-4d91-abdb-4bd5feebf1ac | Handsome Guy |

  Scenario: Change a host user with a valid selected users list
    Given I request to create a new room with
      | game_type | game_mode | host_user_uid                        | host_user_nickname | total_rounds |
      | 2         | 1         | 48f51f68-9337-4d91-abdb-4bd5feebf1ac | Handsome Guy       | 3            |
    And I request to start a new game with users
      | uid                                  | nickname |
      | a362d801-908a-4d67-b82c-078068269654 | User 1   |
      | d3dce936-66a6-4653-ad36-335110249c86 | User 2   |
    And there is a selected users list with
      | uid                                  |
      | 48f51f68-9337-4d91-abdb-4bd5feebf1ac |
      | a362d801-908a-4d67-b82c-078068269654 |
      | d3dce936-66a6-4653-ad36-335110249c86 |
    When I request to set the new host user as
      | uid                                  | nickname |
      | a362d801-908a-4d67-b82c-078068269654 | User 1   |
    Then I should get a 204 http response code
    And there will be only 2 users in the game
    And there will be only 2 users in the selected users list
    And the host user is not
      | uid                                  | nickname     |
      | 48f51f68-9337-4d91-abdb-4bd5feebf1ac | Handsome Guy |

  Scenario: Change a host user without a selected users list
    Given I request to create a new room with
      | game_type | game_mode | host_user_uid                        | host_user_nickname | total_rounds |
      | 2         | 1         | 48f51f68-9337-4d91-abdb-4bd5feebf1ac | Handsome Guy       | 3            |
    And I request to start a new game with users
      | uid                                  | nickname |
      | a362d801-908a-4d67-b82c-078068269654 | User 1   |
      | d3dce936-66a6-4653-ad36-335110249c86 | User 2   |
    When I request to set the new host user as
      | uid                                  | nickname |
      | a362d801-908a-4d67-b82c-078068269654 | User 1   |
    Then I should get a 204 http response code
    And there will be only 2 users in the game
    And there will have no selected users list
    And the host user is not
      | uid                                  | nickname     |
      | 48f51f68-9337-4d91-abdb-4bd5feebf1ac | Handsome Guy |