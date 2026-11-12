from collections import Counter


COUNTER = {"R": "P", "P": "S", "S": "R"}


class Match:
    def __init__(self):
        self.our_moves = []
        self.opponent_moves = []
        self.transitions = Counter()
        self.predictions = {}
        self.scores = Counter()

    def next_move(self, previous_opponent_move):
        if previous_opponent_move:
            self.opponent_moves.append(previous_opponent_move)

            for strategy, prediction in self.predictions.items():
                if prediction == previous_opponent_move:
                    self.scores[strategy] += 1
                else:
                    self.scores[strategy] -= 1

        last_move = self.our_moves[-1] if self.our_moves else "R"

        if self.our_moves:
            earlier_move = self.our_moves[-2] if len(self.our_moves) > 1 else "R"
            self.transitions[earlier_move, last_move] += 1

        likely_next_move = max(
            "RPS",
            key=lambda move: self.transitions[last_move, move],
        )

        recent_moves = ([""] + self.our_moves)[-10:]
        most_used_move = max(set(recent_moves), key=recent_moves.count)

        self.predictions = {
            "transition_counter": COUNTER[likely_next_move],
            "last_move_counter": COUNTER[last_move],
            "frequency_counter": COUNTER[most_used_move or "S"],
        }

        if len(self.opponent_moves) >= 5:
            self.predictions["five_round_cycle"] = self.opponent_moves[-5]

        best_strategy = max(self.predictions, key=self.scores.__getitem__)
        move = COUNTER[self.predictions[best_strategy]]
        self.our_moves.append(move)
        return move


_match = Match()


def player(prev_play):
    global _match

    if prev_play == "":
        _match = Match()

    return _match.next_move(prev_play)