import matplotlib.pyplot as plt
import pygame


class Player():
    def __init__(self, agent, game):
        self.agent = agent
        self.game = game

    def _plot(self, scores, mean_scores):
        plt.clf()
        plt.title('Training...')
        plt.xlabel('Number of Games')
        plt.ylabel('Score')
        plt.plot(scores)
        plt.plot(mean_scores)
        plt.ylim(ymin=0)
        plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
        plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
        plt.show(block=False)
        plt.pause(.1)

    def play(self):
        if self.game.train:
            self._train()
        else:
            clock = pygame.time.Clock()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        break
                self.game.play_Step([])
                if self.game.GameOver:
                    self.game.initialize()
                self.game.draw()
                clock.tick(self.game.FPS)
                self.game.space.step(1 / self.game.FPS)

    def _train(self, plot_results=True):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0
        if self.agent.play_trained:
            self.agent.model.load()
        while True:
            state_old = self.agent.get_state(self.game)
            if not self.agent.play_trained:
                final_move = self.agent.get_action(state_old)
            else:
                final_move = self.agent.get_trained_action(state_old)
            reward, done, score = self.game.play_Step(final_move)
            if not self.agent.play_trained:
                state_new = self.agent.get_state(self.game)
                self.agent.train_short_memory(state_old, final_move, reward, state_new, done)
                self.agent.remember(state_old, final_move, reward, state_new, done)
            self.game.timeTicking()

            if done:
                self.game.initialize()
                self.agent.n_games += 1
                if self.agent.play_trained:
                    print('Game', self.agent.n_games, 'Score', score)
                else:
                    self.agent.train_long_memory()
                    if score > record:
                        record = score
                        self.agent.model.save()
                    print('Game', self.agent.n_games, 'Score', score, 'Record:', record)

                total_score += score
                mean_score = total_score / self.agent.n_games
                if plot_results:
                    plot_scores.append(score)
                    plot_mean_scores.append(mean_score)
                    self._plot(plot_scores, plot_mean_scores)
