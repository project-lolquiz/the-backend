Feature: Game answer

  Scenario: Set right answer for only one user
    Given I request to create a new room with
      | game_type | game_mode | host_user_uid                         | host_user_nickname | total_rounds |
      | 2         | 1         | 4b64074bb-3f11-4235-ae52-81b65a2df1cf | Handsome Guy       | 3            |
    And I request to start a new game with users
      | uid                                  | nickname |
      | 413e5edd-a297-4edd-9fd5-8f73a3a9a3e2 | User 1   |
      | 79829961-5483-4d58-a0d1-4332629355dd | User 2   |
    And I request a new question
    When I request to send the following answers
      | uid                                   | chosen_answer                         |
      | 413e5edd-a297-4edd-9fd5-8f73a3a9a3e2  | 413e5edd-a297-4edd-9fd5-8f73a3a9a3e1  |
      | 4b64074bb-3f11-4235-ae52-81b65a2df1cf | 4b64074bb-3f11-4235-ae52-81b65a2df2cf |
      | 79829961-5483-4d58-a0d1-4332629355dd  | 79829961-5483-4d58-a0d1-4332629354dd  |
    Then I should get a 201 http response code
    And I should get a valid answer response
    And Only one user should answered right

  Scenario: Set right answer for all users
    Given I request to create a new room with
      | game_type | game_mode | host_user_uid                        | host_user_nickname | total_rounds |
      | 2         | 1         | 94074753-b02f-425a-a9cd-529cfbc6bc84 | Handsome Guy       | 3            |
    And I request to start a new game with users
      | uid                                  | nickname |
      | e75e98c5-a3dd-4c17-9348-4f6b8992fad8 | User 1   |
      | b6c198f8-d288-4c7b-a195-02b9a1dd734d | User 2   |
    And I request a new question
    When I request to send all the answers with the right choice
      | uid                                  |
      | e75e98c5-a3dd-4c17-9348-4f6b8992fad8 |
      | b6c198f8-d288-4c7b-a195-02b9a1dd734d |
      | 94074753-b02f-425a-a9cd-529cfbc6bc84 |
    Then I should get a 201 http response code
    And I should get a valid answer response
    And All users should answered right
      | uid                                  |
      | e75e98c5-a3dd-4c17-9348-4f6b8992fad8 |
      | b6c198f8-d288-4c7b-a195-02b9a1dd734d |
      | 94074753-b02f-425a-a9cd-529cfbc6bc84 |