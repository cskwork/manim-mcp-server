from manim import *

class MathTexTest(Scene):
    def construct(self):
        # 기본 수학 공식 테스트
        basic_formula = MathTex(r"E = mc^2")
        basic_formula.scale(1.5)
        self.play(Write(basic_formula))
        self.wait(2)
        
        # 분수 표현식
        fraction = MathTex(r"\frac{a}{b} + \frac{c}{d} = \frac{ad + bc}{bd}")
        fraction.scale(1.2)
        self.play(Transform(basic_formula, fraction))
        self.wait(2)
        
        # 복잡한 수학 표현식
        complex_formula = MathTex(
            r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}"
        )
        complex_formula.scale(1.3)
        self.play(Transform(basic_formula, complex_formula))
        self.wait(2)
        
        # 이차방정식 해공식
        quadratic = MathTex(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}"
        )
        quadratic.scale(1.2)
        self.play(Transform(basic_formula, quadratic))
        self.wait(2)
        
        # 삼각함수 표현식
        trig = MathTex(
            r"\sin^2(x) + \cos^2(x) = 1"
        )
        trig.scale(1.4)
        self.play(Transform(basic_formula, trig))
        self.wait(2)
        
        # 행렬 표현식
        matrix = MathTex(
            r"\begin{pmatrix} a & b \\ c & d \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} ax + by \\ cx + dy \end{pmatrix}"
        )
        matrix.scale(0.8)
        self.play(Transform(basic_formula, matrix))
        self.wait(3)
        
        # 페이드 아웃
        self.play(FadeOut(basic_formula))
        self.wait(1)

class ColoredMathTexTest(Scene):
    def construct(self):
        # 색상이 있는 수학 공식
        colored_formula = MathTex(
            r"f(x) = ax^2 + bx + c",
            substrings_to_isolate=["a", "b", "c", "x"]
        )
        colored_formula.set_color_by_tex("a", RED)
        colored_formula.set_color_by_tex("b", BLUE)
        colored_formula.set_color_by_tex("c", GREEN)
        colored_formula.set_color_by_tex("x", YELLOW)
        colored_formula.scale(1.5)
        
        self.play(Write(colored_formula))
        self.wait(3)
        
        # 애니메이션으로 색상 변경
        self.play(
            colored_formula.animate.set_color(PURPLE)
        )
        self.wait(2)
        
        self.play(FadeOut(colored_formula))
        self.wait(1)

class MathTexAlignment(Scene):
    def construct(self):
        # 수식 정렬 테스트
        equations = MathTex(
            r"x^2 + y^2 &= r^2 \\",
            r"x &= r\cos\theta \\",
            r"y &= r\sin\theta"
        )
        equations.scale(1.2)
        
        self.play(Write(equations))
        self.wait(3)
        
        # 개별 라인 강조
        for i, line in enumerate(equations):
            self.play(line.animate.set_color(YELLOW))
            self.wait(0.5)
            self.play(line.animate.set_color(WHITE))
            self.wait(0.5)
        
        self.play(FadeOut(equations))
        self.wait(1)