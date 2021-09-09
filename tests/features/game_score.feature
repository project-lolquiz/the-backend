Feature: Game scores

  Scenario: End game with a winner
    Given I request to create a new room with
      | game_type | game_mode | host_user_uid                        | host_user_nickname | total_rounds |
      | 2         | 1         | 42a36eff-6686-419d-a86e-a411e346040e | Handsome Guy       | 3            |
    And I request to start a new game with users
      | uid                                  | nickname |
      | 2c561241-fc88-458d-885a-35b53eb2472f | User 1   |
      | c00af165-ea20-4a2a-a14c-ecce7a74d91d | User 2   |
    When I request to send the following question x answer combinations for the 3 rounds
      | round | uid                                  | chosen_answer                        |
      | 1     | 42a36eff-6686-419d-a86e-a411e346040e | c00af165-ea20-4a2a-a14c-ecce7a74d91d |
      | 1     | 2c561241-fc88-458d-885a-35b53eb2472f | c00af165-ea20-4a2a-a14c-ecce7a74d91d |
      | 1     | c00af165-ea20-4a2a-a14c-ecce7a74d91d | 42a36eff-6686-419d-a86e-a411e346040e |
      | 2     | 42a36eff-6686-419d-a86e-a411e346040e | c00af165-ea20-4a2a-a14c-ecce7a74d91d |
      | 2     | 2c561241-fc88-458d-885a-35b53eb2472f | c00af165-ea20-4a2a-a14c-ecce7a74d91d |
      | 2     | c00af165-ea20-4a2a-a14c-ecce7a74d91d | 42a36eff-6686-419d-a86e-a411e346040e |
      | 3     | 42a36eff-6686-419d-a86e-a411e346040e | 2c561241-fc88-458d-885a-35b53eb2472f |
      | 3     | 2c561241-fc88-458d-885a-35b53eb2472f | 2c561241-fc88-458d-885a-35b53eb2472f |
      | 3     | c00af165-ea20-4a2a-a14c-ecce7a74d91d | 2c561241-fc88-458d-885a-35b53eb2472f |
    Then I should get a 201 http response code
    And I should get a valid answer response
    And The game is ended
    And I should get a game result score
    And I should get a winner