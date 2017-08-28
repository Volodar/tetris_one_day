from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
from numpy import *
from time import *
import random


class Engine():

    def __init__(self):
        glutInit([])
        glutInitDisplayMode(GLUT_DEPTH | GLUT_RGB | GLUT_DOUBLE)
        glutInitWindowSize(600, 600)
        glutCreateWindow("Tetris")
        glutReshapeFunc(self.change_size)
        glutDisplayFunc(self.draw)
        glutMouseFunc(self.mouse)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.keyboard)

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glShadeModel(GL_SMOOTH)

        self.axrange = 600.0
        self.time = time()
        gluLookAt(-10.0, -10.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 10.0)

    def run(self):
        glutMainLoop()

    def loop(self):
        pass

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

    def mouse(self, button, state, x, y):
        print 'mouse'
        # if button == GLUT_LEFT_BUTTON:
        #     if state == GLUT_DOWN:
        #         glutIdleFunc(self.spin_func)
        # if button == GLUT_RIGHT_BUTTON:
        #     if state == GLUT_DOWN:
        #         glutIdleFunc(None)
        pass

    def draw_text(self, x, y, string, fontsize=100, weight=1):
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
        # self.lighting()
        glColor3f(1.0, 1.0, 1.0)
        glDisable(GL_DEPTH_TEST)
        glPushMatrix()

        self.plot_axises()

        curr = time()
        dt = curr - self.time
        self.update(dt)
        self.time = curr

        glFlush()
        glPopMatrix()
        glutSwapBuffers()

    def update(self, dt):
        pass

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


class Game(Engine):

    class Figure:
        Left = 1
        Right = -1
        F = []
        F.append([
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]])
        F.append([
            [0, 1, 0],
            [0, 1, 1],
            [0, 0, 1]])
        F.append([
            [0, 1, 0],
            [1, 1, 0],
            [1, 0, 0]])
        F.append([
            [1, 1, 1],
            [1, 0, 0],
            [0, 0, 0]])
        F.append([
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]])
        F.append([
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 0]])
        F.append([
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
            self.parts = Game.Figure.F[random.randint(0, len(Game.Figure.F) - 1)]
            rotate = random.randint(0, 3)
            for i in xrange(rotate):
                self.rotate(Game.Figure.Left)

        def rotate(self, direction):
            if direction == Game.Figure.Right:
                self.parts = zip(*self.parts[::-1])
            elif direction == Game.Figure.Left:
                self.parts = zip(*self.parts)[::-1]

    def __init__(self):
        Engine.__init__(self)

        self.width = 10
        self.height = 20
        self.figure_current = None
        self.figure_next = None
        self.score = 0
        self.board = None
        self.timer = 0
        self.frequence = 0.25
        self.start()
        self.finish = False

    def start(self):
        self.score = 0
        self.board = []
        for i in xrange(self.height):
            self.board.append([])
            for j in xrange(self.width):
                self.board[i].append(None)

        print self.board

        self.board[0][0] = (
            random.randint(128, 255) / 255.0,
            random.randint(128, 255) / 255.0,
            random.randint(128, 255) / 255.0
        )
        self.figure_next = Game.Figure(self)
        self.figure_current = Game.Figure(self)

    def update(self, dt):
        Engine.update(self, dt)

        if not self.finish:
            self.logic(dt)
        self.draw_scene()
        glutPostRedisplay()

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

    def draw_scene(self):
        size = 25
        # draw grid:
        for i in xrange(self.width + 1):
            self.draw_line(
                20 + i * size, 20,
                20 + i * size, 20 + size * self.height, color=(0.1, 0.1, 0.15))
        for i in xrange(self.height + 1):
            self.draw_line(
                20, 20 + i * size,
                20 + size * self.width, 20 + i * size, color=(0.1, 0.1, 0.15))
        self.draw_rect(center_x=20 + size * self.width / 2.0, center_y=20 + size * self.height / 2.0,
                       width=size * self.width + 10, height=size * self.height + 10,
                       line_width=5, color=(0.5, 0.5, 0.5))
        # draw board:

        border = 4

        def draw_squad(x, y, color):
            self.draw_rect(20 + (x + 0.5) * size, 20 + (y + 0.5) * size,
                           size - border, size - border, color=color, line_width=border)
            self.draw_rect(20 + (x + 0.5) * size, 20 + (y + 0.5) * size,
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
                else:
                    draw_squad(x + 12, self.height - y - 2, (0.1, 0.1, 0.1))
        self.draw_rect(370, 458, size * 4 + 10, size * 3 + 10)
        # draw scores
        self.draw_text(290, 350, 'Score:', 15, weight=2)
        self.draw_text(290, 320, str(self.score), 15, weight=2)

    def keyboard(self, key, x, y):
        if self.finish:
            return
        if key == chr(27) or key == 'q' or key == 'Q':
            sys.exit()
        if key == GLUT_KEY_UP:
            self.figure_current.rotate(Game.Figure.Left)
            if self.detect_collision():
                self.figure_current.rotate(Game.Figure.Right)

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
                print 'collision'
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
        self.figure_next = Game.Figure(self)
        if self.detect_collision():
            self.finish_with_fail()

    def finish_with_win(self):
        pass

    def finish_with_fail(self):
        pass


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()


# draw scene:
    # draw gameboard with grid
    # draw score
    # draw next figure place
    # draw menu
# draw board:
    # draw old figures
    # draw current figure
