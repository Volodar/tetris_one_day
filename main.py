from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
from numpy import *
from time import *
from datetime import datetime
import random


class Engine():

    def __init__(self, state):
        glutInit([])
        glutInitDisplayMode(GLUT_DEPTH | GLUT_RGB | GLUT_DOUBLE)
        glutInitWindowSize(600, 600)
        glutCreateWindow("Tetris")
        glutReshapeFunc(self.change_size)
        glutDisplayFunc(self.draw)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glShadeModel(GL_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

        self.axrange = 600.0
        self.time = time()
        gluLookAt(-10.0, -10.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 10.0)

        self.states = []
        self.push_state(state)

    def push_state(self, state):
        self.states.append(state(self))
        self._set_state(self.states[-1])

    def _set_state(self, state):
        glutMouseFunc(state.mouse)
        glutKeyboardFunc(state.keyboard)
        glutSpecialFunc(state.keyboard)

    def pop_state(self):
        self.states = self.states[:-1]
        if len(self.states):
            self._set_state(self.states[-1])
        else:
            sys.exit()

    def run(self):
        glutMainLoop()

    def plot_axises(self):
        S = self.axrange / 2
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glVertex3f(-S, -S, 0.0)
        glVertex3f(S, -S, 0.0)
        glVertex3f(-S, S, 0.0)
        glVertex3f(S, S, 0.0)
        glVertex3f(S, -S, 0.0)
        glVertex3f(S, S, 0.0)
        glVertex3f(-S, -S, 0.0)
        glVertex3f(-S, S, 0.0)
        glEnd()

    def draw_rect(self,
                  center_x=0.0, center_y=0.0,
                  width=1.0, height=1.0,
                  line_width=1.0, color=None, color4=(1.0, 1.0, 1.0, 1.0)
                  ):
        if color:
            glColor3f(*color)
        elif color4:
            glColor4f(*color4)
        glLineWidth(line_width)
        glBegin(GL_LINE_STRIP)
        center_x -= self.axrange / 2.0
        center_y -= self.axrange / 2.0
        glVertex3f(center_x - width / 2.0, center_y - height / 2.0, 0)
        glVertex3f(center_x - width / 2.0, center_y + height / 2.0, 0)
        glVertex3f(center_x + width / 2.0, center_y + height / 2.0, 0)
        glVertex3f(center_x + width / 2.0, center_y - height / 2.0, 0)
        glVertex3f(center_x - width / 2.0, center_y - height / 2.0, 0)
        glEnd()

    def draw_solid_rect(self,
                        center_x=0.0, center_y=0.0,
                        width=1.0, height=1.0,
                        line_width=1.0, color=None, color4=(1.0, 1.0, 1.0, 1.0)
                        ):
        if color:
            glColor3f(*color)
        elif color4:
            glColor4f(*color4)
        glLineWidth(line_width)
        glBegin(GL_QUADS)
        center_x -= self.axrange / 2.0
        center_y -= self.axrange / 2.0
        glVertex3f(center_x - width / 2.0, center_y + height / 2.0, 0)
        glVertex3f(center_x + width / 2.0, center_y + height / 2.0, 0)
        glVertex3f(center_x + width / 2.0, center_y - height / 2.0, 0)
        glVertex3f(center_x - width / 2.0, center_y - height / 2.0, 0)
        glEnd()

    def draw_line(self, x0, y0, x1, y1, line_width=1.0, color=None, color4=(1.0, 1.0, 1.0, 1.0)):
        if color:
            glColor3f(*color)
        elif color4:
            glColor4f(*color4)
        glLineWidth(line_width)
        glBegin(GL_LINES)
        glVertex3f(x0 - self.axrange / 2.0, y0 - self.axrange / 2.0, 0.0)
        glVertex3f(x1 - self.axrange / 2.0, y1 - self.axrange / 2.0, 0.0)
        glEnd()

    def draw_text(self, x, y, string, fontsize=100, weight=1, color=None, color4=(1.0, 1.0, 1.0, 1.0)):
        if color:
            glColor3f(*color)
        elif color4:
            glColor4f(*color4)
        glPushMatrix()
        glLineWidth(weight)
        glTranslate(-self.axrange / 2 + x, -self.axrange / 2 + y, 0.0)
        glScalef(fontsize / 100.0, fontsize / 100.0, fontsize / 100.0)
        glRotate(0.0, 0.0, 0.0, 1.0)

        for ch in string:
            glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(ch))
        glPopMatrix()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)
        glDisable(GL_DEPTH_TEST)
        glPushMatrix()

        self.plot_axises()

        curr = time()
        dt = curr - self.time
        self.states[-1].update(dt)
        self.states[-1].draw()
        self.time = curr

        glFlush()
        glPopMatrix()
        glutSwapBuffers()
        glutPostRedisplay()

    def change_size(self, w, h):
        if h == 0:
            h = 1
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.axrange /= 2
        if w < h:
            glOrtho(-self.axrange, self.axrange,
                    -self.axrange * h / w, self.axrange * h / w,
                    -self.axrange * 1.0, self.axrange * 1.0)
        else:
            glOrtho(-self.axrange * w / h, self.axrange * w / h,
                    -self.axrange, self.axrange,
                    -self.axrange * 1.0, self.axrange * 1.0)
        self.axrange *= 2
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


class State:

    def __init__(self, engine):
        self.engine = engine
        self.buttons = []

    def mouse(self, button, state, x, y):
        if state == GLUT_UP:
            for button in self.buttons:
                if button.test_point(x, y):
                    button.callback()
                    break

    def keyboard(self, key, x, y):
        pass

    def update(self, dt):
        pass

    def draw(self):
        for button in self.buttons:
            button.draw(self.engine)

    def add_button(self, button):
        self.buttons.append(button)


class Button:

    def __init__(self, center_x, center_y, width, height, text, text_pos=0):
        self.draw_info = (center_x, center_y, width, height)
        self.text = text
        self.text_pos = text_pos
        self.font_size = 20
        self.origin_x = center_x - width / 2
        self.origin_y = center_y - height / 2
        self.right_x = center_x + width / 2
        self.right_y = center_y + height / 2
        self.callback = None

    def draw(self, engine):
        engine.draw_rect(*self.draw_info, line_width=3)
        engine.draw_text(self.origin_x + self.text_pos, (self.origin_y + self.right_y) / 2 - self.font_size / 2, self.text, self.font_size)

    def test_point(self, x, y):
        y = 600 - y
        return x >= self.origin_x and x <= self.right_x and y >= self.origin_y and y <= self.right_y


class Direction:
    Left = 1
    Right = -1


class Figure:
    Template = []
    Template.append([
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]])
    Template.append([
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 1]])
    Template.append([
        [0, 1, 0],
        [1, 1, 0],
        [1, 0, 0]])
    Template.append([
        [1, 1, 1],
        [1, 0, 0],
        [0, 0, 0]])
    Template.append([
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0]])
    Template.append([
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 0]])
    Template.append([
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]])

    def __init__(self, game):
        self.game = game
        self.parts = None
        self.color = (1, 0, 0)
        self.generate()
        self.x = (game.width - len(self.parts)) / 2
        self.y = game.height - 1

    def generate(self):
        self.color = (
            random.randint(128, 255) / 255.0,
            random.randint(128, 255) / 255.0,
            random.randint(128, 255) / 255.0
        )
        self.parts = Figure.Template[random.randint(0, len(Figure.Template) - 1)]
        rotate = random.randint(0, 3)
        for i in xrange(rotate):
            self.rotate(Direction.Left)

    def rotate(self, direction):
        if direction == Direction.Right:
            self.parts = zip(*self.parts[::-1])
        elif direction == Direction.Left:
            self.parts = zip(*self.parts)[::-1]


class StateGame(State):

    def __init__(self, engine):
        State.__init__(self, engine)
        self.width = 10
        self.height = 20
        self.figure_current = None
        self.figure_next = None
        self.score = 0
        self.board = None
        self.timer = 0
        self.frequence = 0.25
        self.time_of_game = 0
        self.start()
        self.finish_result = None

    def start(self):
        self.score = 0
        self.board = []
        for i in xrange(self.height):
            self.board.append([])
            for j in xrange(self.width):
                self.board[i].append(None)

        self.board[0][0] = (
            random.randint(128, 255) / 255.0,
            random.randint(128, 255) / 255.0,
            random.randint(128, 255) / 255.0
        )
        self.figure_next = Figure(self)
        self.figure_current = Figure(self)

    def update(self, dt):
        if self.finish_result is None:
            self.time_of_game += dt
            self.logic(dt)

    def logic(self, dt):
        self.timer += dt
        if self.timer >= self.frequence:
            self.timer -= self.frequence
            self.figure_current.y -= 1
            if self.detect_collision():
                self.figure_current.y += 1
                self.apply_figure()
                self.find_matches()
                self.next_figure()

    def draw(self):
        size = 25
        # draw grid:
        for i in xrange(self.width + 1):
            self.engine.draw_line(
                20 + i * size, 20,
                20 + i * size, 20 + size * self.height, color=(0.1, 0.1, 0.15))
        for i in xrange(self.height + 1):
            self.engine.draw_line(
                20, 20 + i * size,
                20 + size * self.width, 20 + i * size, color=(0.1, 0.1, 0.15))
        self.engine.draw_rect(center_x=20 + size * self.width / 2.0, center_y=20 + size * self.height / 2.0,
                              width=size * self.width + 10, height=size * self.height + 10,
                              line_width=5, color=(0.5, 0.5, 0.5))
        # draw board:

        border = 4

        def draw_squad(x, y, color):
            self.engine.draw_rect(20 + (x + 0.5) * size, 20 + (y + 0.5) * size,
                                  size - border - 1, size - border - 1, color=color, line_width=border)
            self.engine.draw_rect(20 + (x + 0.5) * size, 20 + (y + 0.5) * size,
                                  size / 2 - border, size / 2 - border, color=color, line_width=border)

        for y, line in enumerate(self.board):
            for x, cell in enumerate(line):
                if cell is None:
                    continue
                draw_squad(x, y, cell)
        # draw figure
        for y, line in enumerate(self.figure_current.parts):
            for x, cell in enumerate(line):
                if cell:
                    draw_squad(x + self.figure_current.x, self.figure_current.y - y, self.figure_current.color)
        # draw next figure
        for y, line in enumerate(self.figure_next.parts):
            for x, cell in enumerate(line):
                if cell:
                    draw_squad(x + 12, self.height - y - 2, self.figure_next.color)
        self.engine.draw_rect(370, 446, size * 4 + 10, size * 4 + 10)
        # draw scores
        self.engine.draw_text(315, 350, 'Score:', 15, weight=2)
        self.engine.draw_text(315, 320, str(self.score), 15, weight=2)

        self.engine.draw_text(315, 250, 'Time:', 15, weight=2)
        self.engine.draw_text(315, 220, datetime.fromtimestamp(int(self.time_of_game)).strftime('%M:%S'), 15, weight=2)

        if self.finish_result is not None:
            self.draw_finish_window()
        State.draw(self)

    def draw_finish_window(self):
        self.engine.draw_solid_rect(300, 300, 300, 400, color=(0.7, 0.7, 0.7))
        self.engine.draw_text(180, 450, 'Victory!' if self.finish_result else 'Defeat :(', 28, weight=4, color=(0.7, 0.5, 0.5))
        self.engine.draw_text(190, 300, 'Score: ' + str(self.score), 20, weight=4, color=(0.0, 0.5, 0.9))
        self.engine.draw_text(190, 250, 'Time: ' + datetime.fromtimestamp(int(self.time_of_game)).strftime('%M:%S'), 20, weight=4, color=(0.0, 0.5, 0.9))
        pass

    def keyboard(self, key, x, y):
        State.keyboard(self, key, x, y)
        if key == chr(27) or key == 'q' or key == 'Q':
            self.engine.pop_state()
        if self.finish_result is not None:
            return

        if key == GLUT_KEY_UP:
            self.figure_current.rotate(Direction.Left)
            if self.detect_collision():
                self.figure_current.rotate(Direction.Right)

        else:
            x = self.figure_current.x
            y = self.figure_current.y
            if key == GLUT_KEY_LEFT:
                self.figure_current.x -= 1
            if key == GLUT_KEY_RIGHT:
                self.figure_current.x += 1
            if key == GLUT_KEY_DOWN:
                self.figure_current.y -= 1

            if self.detect_collision():
                self.figure_current.x = x
                self.figure_current.y = y

    def detect_collision(self):
        for y, line in enumerate(self.figure_current.parts):
            for x, cell in enumerate(line):
                if cell:
                    X = x + self.figure_current.x
                    Y = self.figure_current.y - y
                    if X < 0 or X > self.width - 1:
                        return True
                    if Y < 0 or Y > self.height - 1:
                        return True
                    if self.board[Y][X] is not None:
                        return True
        return False

    def apply_figure(self):
        for y, line in enumerate(self.figure_current.parts):
            for x, cell in enumerate(line):
                if cell:
                    X = x + self.figure_current.x
                    Y = self.figure_current.y - y
                    if X >= 0 or X < self.width and Y >= 0 or Y < self.height:
                        self.board[Y][X] = self.figure_current.color

    def find_matches(self):
        repeat = True
        lines = 0
        while repeat:
            repeat = False
            for i, line in enumerate(self.board):
                match = True
                for cell in line:
                    if cell is None:
                        match = False
                if match:
                    lines += 1
                    for j in xrange(i, self.height - 1):
                        self.board[j] = self.board[j + 1]
                    repeat = True
        scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
        self.score += scores[lines]

        pass

    def next_figure(self):
        self.figure_current = self.figure_next
        self.figure_next = Figure(self)
        if self.detect_collision():
            self.finish_with_result(False)

    def finish_with_result(self, result):
        self.finish_result = result
        start = Button(300, 160, 200, 70, "Exit", 50)
        start.callback = self.exit
        self.add_button(start)

    def exit(self):
        self.engine.pop_state()


class StateTitle(State):

    def __init__(self, engine):
        State.__init__(self, engine)

        start = Button(300, 250, 200, 70, "Start", 50)
        start.callback = self.start
        self.add_button(start)

    def mouse(self, button, state, x, y):
        State.mouse(self, button, state, x, y)

    def keyboard(self, key, x, y):
        State.keyboard(self, key, x, y)

    def update(self, dt):
        State.update(self, dt)

    def draw(self):
        State.draw(self)
        self.engine.draw_text(40, 500, "Tetris One Day", fontsize=35)
        self.engine.draw_text(55, 20, "Author: Vladimir Tolmachev", fontsize=18)

    def start(self):
        self.engine.push_state(StateGame)


def main():
    engine = Engine(StateTitle)
    engine.run()

if __name__ == "__main__":
    main()
