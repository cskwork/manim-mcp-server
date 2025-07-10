from manim import *

class TestScene(Scene):
    def construct(self):
        # 간단한 텍스트 생성
        text = Text("Hello, Manim!", color=BLUE)
        self.play(Write(text))
        self.wait(1)
        
        # 원 생성 및 애니메이션
        circle = Circle(radius=1, color=RED)
        self.play(Create(circle))
        self.wait(1)
        
        # 변환 애니메이션
        self.play(Transform(text, circle))
        self.wait(1)