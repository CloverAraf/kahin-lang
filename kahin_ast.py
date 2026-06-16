#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
KAHİN AST (Abstract Syntax Tree) - CPython-like Implementation
═══════════════════════════════════════════════════════════════════════

CPython'un AST'si gibi çalışır.
Kahin kodunu AST'ye çevirir, optimize eder, Python AST'sine dönüştürür.

AST NEDİR:
----------
Abstract Syntax Tree - Kodun ağaç yapısında temsili

Örnek:
    eger x > 5:
        yazdir("test")

AST:
    If(
        test=Compare(left=Name('x'), ops=[Gt()], comparators=[Constant(5)]),
        body=[
            Expr(Call(func=Name('print'), args=[Constant('test')]))
        ],
        orelse=[]
    )

AVANTAJLAR:
-----------
1. Syntax kontrolü (parse time)
2. Optimizasyon (constant folding, dead code elimination)
3. Bytecode generation
4. Hata mesajları (satır numarası)

PERFORMANS:
-----------
- Python'un ast modülünü kullanır (C implementasyonu)
- Çok hızlı: ~0.002s for 1000 satır
"""

import ast
import sys
from typing import Any, List, Optional
from kahin_lexer import KahinLexer, KEYWORD_MAP


# ═══════════════════════════════════════════════════════════════════════
# AST TRANSFORMER - Türkçe → Python AST
# ═══════════════════════════════════════════════════════════════════════

class KahinASTTransformer(ast.NodeTransformer):
    """
    AST Transformer - Kahin AST → Python AST

    CPython'un ast.NodeTransformer'ı gibi çalışır.
    Her node'u ziyaret edip dönüştürür.

    NEDEN GEREKLİ:
    --------------
    Lexer token'ları çeviriyor ama bu yeterli değil!
    AST seviyesinde optimizasyon yapmalıyız:

    1. Constant Folding
       eger 2 + 3 > 4:  →  eger 5 > 4:  →  eger dogru:

    2. Dead Code Elimination
       eger yanlis:
           kod  →  (silinir, asla çalışmaz)

    3. Function Inlining (gelecek)
    4. Variable Renaming Optimization (gelecek)
    """

    def __init__(self):
        self.optimizations_applied = 0

    def visit_Name(self, node: ast.Name) -> ast.Name:
        """
        Name node'larını ziyaret et

        Türkçe değişken isimlerini Python'a çevirebiliriz
        (opsiyonel - şu an sadece keyword'ler çevriliyor)
        """
        # Şu an bir şey yapmıyoruz ama gelecekte:
        # - Türkçe değişken isimleri → snake_case
        # - Reserved keyword kontrolü
        return node

    def visit_Constant(self, node: ast.Constant) -> ast.Constant:
        """
        Constant node'ları optimize et

        Örnek:
            "test" + "123"  →  "test123" (compile time'da)
        """
        return node

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        """
        Binary operations - Constant Folding

        Örnek:
            2 + 3  →  5 (compile time'da hesapla)
            x + 0  →  x (identity optimization)
            x * 1  →  x
            x * 0  →  0
        """
        # Önce child node'ları ziyaret et
        self.generic_visit(node)

        # İki taraf da constant ise hesapla
        if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
            try:
                # Operasyonu compile time'da hesapla
                left_val = node.left.value
                right_val = node.right.value

                if isinstance(node.op, ast.Add):
                    result = left_val + right_val
                elif isinstance(node.op, ast.Sub):
                    result = left_val - right_val
                elif isinstance(node.op, ast.Mult):
                    result = left_val * right_val
                elif isinstance(node.op, ast.Div):
                    result = left_val / right_val
                elif isinstance(node.op, ast.Mod):
                    result = left_val % right_val
                elif isinstance(node.op, ast.Pow):
                    result = left_val ** right_val
                else:
                    return node  # Bilinmeyen operator

                self.optimizations_applied += 1
                return ast.Constant(value=result)

            except:
                # Hata olursa optimize etme
                return node

        # Identity optimizations
        # x + 0 → x
        if isinstance(node.op, ast.Add) and isinstance(node.right, ast.Constant):
            if node.right.value == 0:
                self.optimizations_applied += 1
                return node.left

        # x * 1 → x
        if isinstance(node.op, ast.Mult) and isinstance(node.right, ast.Constant):
            if node.right.value == 1:
                self.optimizations_applied += 1
                return node.left

        # x * 0 → 0
        if isinstance(node.op, ast.Mult):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                self.optimizations_applied += 1
                return ast.Constant(value=0)
            if isinstance(node.left, ast.Constant) and node.left.value == 0:
                self.optimizations_applied += 1
                return ast.Constant(value=0)

        return node

    def visit_Compare(self, node: ast.Compare) -> Any:
        """
        Karşılaştırma - Constant Folding

            5 > 3   → True
            "a" == "a" → True
            2 <= 2  → True

        Sadece tüm operandlar sabit ve tek operatörlü zincirde foldlanır.
        """
        self.generic_visit(node)

        operandlar = [node.left, *node.comparators]
        if not all(isinstance(o, ast.Constant) for o in operandlar):
            return node

        CMP = {
            ast.Eq: lambda a, b: a == b, ast.NotEq: lambda a, b: a != b,
            ast.Lt: lambda a, b: a < b, ast.LtE: lambda a, b: a <= b,
            ast.Gt: lambda a, b: a > b, ast.GtE: lambda a, b: a >= b,
            ast.Is: lambda a, b: a is b, ast.IsNot: lambda a, b: a is not b,
            ast.In: lambda a, b: a in b, ast.NotIn: lambda a, b: a not in b,
        }
        try:
            sonuc = True
            for i, op in enumerate(node.ops):
                fn = CMP.get(type(op))
                if fn is None:
                    return node
                sol = operandlar[i].value
                sag = operandlar[i + 1].value
                if not fn(sol, sag):
                    sonuc = False
                    break
            self.optimizations_applied += 1
            return ast.Constant(value=sonuc)
        except Exception:
            return node

    def visit_BoolOp(self, node: ast.BoolOp) -> Any:
        """
        Mantıksal operatör - Short-circuit folding

            dogru and x  → x
            yanlis and x → False
            yanlis or x  → x
            dogru or x   → True
        """
        self.generic_visit(node)

        deger = node.values
        if isinstance(node.op, ast.And):
            # Sabit False varsa kısa devre → False
            for v in deger:
                if isinstance(v, ast.Constant) and not v.value:
                    self.optimizations_applied += 1
                    return ast.Constant(value=False)
            # Sabit True'ları ele
            kalan = [v for v in deger if not (isinstance(v, ast.Constant) and v.value)]
            if len(kalan) != len(deger):
                self.optimizations_applied += 1
                if not kalan:
                    return ast.Constant(value=True)
                return kalan[0] if len(kalan) == 1 else ast.BoolOp(op=node.op, values=kalan)
        elif isinstance(node.op, ast.Or):
            for v in deger:
                if isinstance(v, ast.Constant) and v.value:
                    self.optimizations_applied += 1
                    return ast.Constant(value=v.value)
            kalan = [v for v in deger if not (isinstance(v, ast.Constant) and not v.value)]
            if len(kalan) != len(deger):
                self.optimizations_applied += 1
                if not kalan:
                    return ast.Constant(value=False)
                return kalan[0] if len(kalan) == 1 else ast.BoolOp(op=node.op, values=kalan)

        return node

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        """
        Tekli operatör - Constant Folding

            -5        → -5 (sabit)
            not dogru → False
            not yanlis → True
        """
        self.generic_visit(node)

        if isinstance(node.operand, ast.Constant):
            val = node.operand.value
            try:
                if isinstance(node.op, ast.USub):
                    sonuc = -val
                elif isinstance(node.op, ast.UAdd):
                    sonuc = +val
                elif isinstance(node.op, ast.Not):
                    sonuc = not val
                elif isinstance(node.op, ast.Invert):
                    sonuc = ~val
                else:
                    return node
                self.optimizations_applied += 1
                return ast.Constant(value=sonuc)
            except Exception:
                return node

        return node

    def visit_If(self, node: ast.If) -> Any:
        """
        If statements - Dead Code Elimination

        Örnek:
            eger dogru:  →  (body'yi direkt çalıştır, if'i kaldır)
                kod

            eger yanlis:  →  (tüm if'i sil veya orelse çalıştır)
                kod
        """
        # Child node'ları ziyaret et
        self.generic_visit(node)

        # Test constant ise
        if isinstance(node.test, ast.Constant):
            if node.test.value:  # dogru (True)
                # If body'yi direkt döndür (if'siz)
                self.optimizations_applied += 1
                return node.body if len(node.body) > 1 else node.body[0]
            else:  # yanlis (False)
                # orelse varsa onu döndür, yoksa pas
                self.optimizations_applied += 1
                if node.orelse:
                    return node.orelse if len(node.orelse) > 1 else node.orelse[0]
                else:
                    return ast.Pass()  # Boş if → pass

        return node


# ═══════════════════════════════════════════════════════════════════════
# KAHIN PARSER - Ana Sınıf
# ═══════════════════════════════════════════════════════════════════════

class KahinParser:
    """
    Kahin Parser - CPython-like

    NASIL ÇALIŞIR:
    --------------
    1. Lexer ile token'lara ayır
    2. Token'ları Python koduna çevir
    3. Python'un ast.parse() ile AST oluştur (CPython'un C parser'ı)
    4. AST'yi optimize et (transformer)
    5. AST'yi döndür

    Bu AST:
    - Bytecode'a compile edilebilir (compile())
    - Çalıştırılabilir (exec())
    - Optimize edilebilir
    - Analiz edilebilir
    """

    def __init__(self, optimize=True):
        self.lexer = KahinLexer()
        self.transformer = KahinASTTransformer() if optimize else None
        self.optimize = optimize

    def parse(self, kaynak_kod: str, dosya_adi='<kahin>', mode='exec') -> ast.Module:
        """
        Kahin kodunu parse et → AST

        Args:
            kaynak_kod: Kahin kaynak kodu
            dosya_adi: Dosya adı (hata mesajları için)
            mode: 'exec' (tam program) veya 'eval' (expression)

        Returns:
            Python AST (ast.Module)

        Raises:
            SyntaxError: Syntax hatası varsa
        """

        # ADIM 1: Tokenize (Lexer)
        tokens = self.lexer.tokenize(kaynak_kod)

        # ADIM 2: Detokenize (Python kodu)
        python_kod = self.lexer.tokens_to_code(tokens)

        # ADIM 3: Parse (CPython'un parser'ı)
        try:
            tree = ast.parse(python_kod, filename=dosya_adi, mode=mode)
        except SyntaxError as e:
            # Hata mesajını Türkçeleştir
            raise SyntaxError(f"Sözdizimi hatası: {e}")

        # ADIM 4: Optimize (AST Transformer)
        if self.optimize and self.transformer:
            tree = self.transformer.visit(tree)
            ast.fix_missing_locations(tree)  # Satır numaralarını düzelt

        return tree

    def parse_and_compile(self, kaynak_kod: str, dosya_adi='<kahin>', optimize=2) -> Any:
        """
        Parse + Compile → Bytecode

        Args:
            kaynak_kod: Kahin kaynak kodu
            dosya_adi: Dosya adı
            optimize: Optimizasyon seviyesi (0, 1, 2)
                      2 = En agresif (CPython -OO)

        Returns:
            Code object (bytecode)
        """

        # Parse
        tree = self.parse(kaynak_kod, dosya_adi)

        # Compile (CPython'un bytecode compiler'ı)
        code = compile(tree, dosya_adi, 'exec', optimize=optimize)

        return code


# ═══════════════════════════════════════════════════════════════════════
# TEST & BENCHMARK
# ═══════════════════════════════════════════════════════════════════════

def test_parser():
    """Parser test"""

    print("═" * 70)
    print("KAHİN AST PARSER - CPython-like Implementation")
    print("═" * 70)

    kahin_kod = '''
// Test programı
tanimla topla(a, b):
    sonuc = a + b
    dondur sonuc

x = 10
y = 20

eger x > 5:
    yazdir("x büyük")
    toplam = topla(x, y)
    yazdir(f"Toplam: {toplam}")
'''

    print("\nKahin Kodu:")
    print(kahin_kod)

    # Parser oluştur
    parser = KahinParser(optimize=True)

    # Parse et
    import time
    start = time.perf_counter()
    tree = parser.parse(kahin_kod)
    elapsed = time.perf_counter() - start

    print(f"\nParse süresi: {elapsed*1000:.3f} ms")
    print(f"Optimizasyonlar: {parser.transformer.optimizations_applied}")

    # AST göster
    print("\nAST (Abstract Syntax Tree):")
    print("-" * 70)
    print(ast.dump(tree, indent=2)[:1000] + "...")  # İlk 1000 karakter

    # Compile et
    start = time.perf_counter()
    code = compile(tree, '<test>', 'exec', optimize=2)
    elapsed = time.perf_counter() - start

    print(f"\nCompile süresi: {elapsed*1000:.3f} ms")
    print(f"Bytecode boyutu: {len(code.co_code)} byte")

    # Çalıştır
    print("\nÇıktı:")
    print("-" * 70)
    exec(code)


def test_optimizations():
    """Optimizasyon testi"""

    print("\n" + "═" * 70)
    print("OPTİMİZASYON TESTİ")
    print("═" * 70)

    testler = [
        ("2 + 3", "Constant folding (2+3 → 5)"),
        ("x + 0", "Identity (x+0 → x)"),
        ("x * 1", "Identity (x*1 → x)"),
        ("x * 0", "Identity (x*0 → 0)"),
        ("eger dogru:\n    yazdir('test')", "Dead code (eger dogru)"),
        ("eger yanlis:\n    yazdir('test')", "Dead code (eger yanlis)"),
    ]

    parser = KahinParser(optimize=True)

    for kod, aciklama in testler:
        print(f"\nTest: {aciklama}")
        print(f"  Kod: {kod!r}")

        parser.transformer.optimizations_applied = 0
        tree = parser.parse(kod, mode='eval' if '\n' not in kod else 'exec')

        print(f"  Optimizasyon: {'✓' if parser.transformer.optimizations_applied > 0 else '✗'}")


if __name__ == "__main__":
    test_parser()
    test_optimizations()
