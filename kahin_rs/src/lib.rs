// Kahin Rust tokenizer - PyO3 extension
//
// to_python(src): Kahin (Türkçe) kaynağı -> Python kaynağı.
//   - // -> # yorum
//   - string/yorum içeriği KORUNUR
//   - Türkçe keyword -> Python (kelime sınırı)
//   - 1..10 -> range(1, 10), 1..=10 -> range(1, 10 + 1)
//   - x |> f -> f(x) (satır bazlı, depth-0 zincir)
//
// Tek geçişlik elle yazılmış scanner. Regex motoru yok.

use pyo3::prelude::*;

// ── Türkçe → Python keyword haritası ───────────────────────────────
fn keyword(tr: &str) -> Option<&'static str> {
    Some(match tr {
        "ice_aktar" => "import", "tanimla" => "def", "eger" => "if",
        "degilse_eger" => "elif", "degilse" => "else", "dondu_boyunca" => "while",
        "her_biri_icin" => "for", "icinde" => "in", "dondur" => "return",
        "dur" => "break", "devam_et" => "continue", "gec" => "pass",
        "ile" => "with", "yukle" => "yield",
        "dene" => "try", "yakala" => "except", "sonunda" => "finally",
        "firlat" => "raise", "olumla" => "assert",
        "dogru" => "True", "yanlis" => "False", "hic" => "None",
        "sinif" => "class", "sil" => "del", "kuresel" => "global",
        "yerel_degil" => "nonlocal", "lambda" => "lambda",
        "eslestir" => "match", "desen" => "case",
        "yazdir" => "print", "girdi" => "input", "uzunluk" => "len",
        "aralik" => "range", "tam_sayi" => "int", "metin" => "str",
        "ondalik" => "float", "liste" => "list", "sozluk" => "dict",
        "kume" => "set", "demet" => "tuple", "tur" => "type",
        "yardim" => "help", "mutlak" => "abs", "sirala" => "sorted",
        "ac" => "open", "topla" => "sum", "en_buyuk" => "max",
        "en_kucuk" => "min", "bekle" => "input",
        "sistem" => "os", "istek" => "requests",
        "arayuz" => "sys",
        _ => return None,
    })
}

// Tüm tasarımın özü bu enum'da: kaynağı parçalara ayırırken hangi parçanın
// "kod" hangisinin "dokunulmaz metin" olduğunu tipiyle işaretliyoruz. Str ve
// Comment çevrilmeden aynen geçer; Word/Range/Pipe ise çevrime tabi. Bu ayrım
// olmadan `"1..10"` literali ile gerçek `1..10` aralığını ayırt edemezdik.
#[derive(Debug, Clone)]
enum Tok {
    // kod parçaları (keyword çevrilebilir, range/pipe burada)
    Word(String),    // tanımlayıcı / keyword adayı
    Number(String),
    Str(String),     // string literali (aynen, f"" dahil) — DOKUNMA
    Comment(String), // # ... (// zaten # yapıldı)
    Op(String),      // operatörler, noktalama, boşluk dahil ham parça
    Range(bool),     // .. (false)  ..= (true)
    Pipe,            // |>
    Newline,
}

struct Lexer {
    src: Vec<char>,
    pos: usize,
}

impl Lexer {
    fn new(s: &str) -> Self {
        Lexer { src: s.chars().collect(), pos: 0 }
    }
    fn peek(&self) -> Option<char> { self.src.get(self.pos).copied() }
    fn peek2(&self) -> Option<char> { self.src.get(self.pos + 1).copied() }
    fn bump(&mut self) -> Option<char> {
        let c = self.peek();
        if c.is_some() { self.pos += 1; }
        c
    }

    fn run(&mut self) -> Vec<Tok> {
        let mut out = Vec::new();
        while let Some(c) = self.peek() {
            // newline
            if c == '\n' {
                self.bump();
                out.push(Tok::Newline);
                continue;
            }
            // yorum: # ... satır sonuna kadar  (// önceden # yapıldı)
            if c == '#' {
                let mut s = String::new();
                while let Some(ch) = self.peek() {
                    if ch == '\n' { break; }
                    s.push(ch);
                    self.bump();
                }
                out.push(Tok::Comment(s));
                continue;
            }
            // string: ' " ve f-prefix
            if c == '"' || c == '\'' {
                out.push(Tok::Str(self.scan_string(None)));
                continue;
            }
            if (c == 'f' || c == 'r' || c == 'b') &&
                matches!(self.peek2(), Some('"') | Some('\'')) {
                let prefix = c;
                self.bump();
                out.push(Tok::Str(self.scan_string(Some(prefix))));
                continue;
            }
            // sayı: ondalık + alt çizgi. 0x/0b/0o ve hex tek Word'e karışmasın diye basit tut.
            if c.is_ascii_digit() {
                let mut s = String::new();
                while let Some(ch) = self.peek() {
                    // Burası ince: `1..10` okurken nokta görünce durmalıyız,
                    // yoksa "1." diye ondalık sayı sanıp aralığı yiyebiliriz.
                    // İki nokta peş peşeyse bu bir aralık operatörü, sayı değil.
                    if ch == '.' && self.peek2() == Some('.') { break; }
                    if ch.is_ascii_digit() || ch == '.' || ch == '_' {
                        s.push(ch);
                        self.bump();
                    } else { break; }
                }
                out.push(Tok::Number(s));
                continue;
            }
            // tanımlayıcı / keyword: harf, _, unicode (Türkçe karakter)
            if c == '_' || c.is_alphabetic() {
                let mut s = String::new();
                while let Some(ch) = self.peek() {
                    if ch == '_' || ch.is_alphanumeric() {
                        s.push(ch);
                        self.bump();
                    } else { break; }
                }
                out.push(Tok::Word(s));
                continue;
            }
            // ..= ve ..
            if c == '.' && self.peek2() == Some('.') {
                self.bump(); self.bump();
                if self.peek() == Some('=') {
                    self.bump();
                    out.push(Tok::Range(true));
                } else {
                    out.push(Tok::Range(false));
                }
                continue;
            }
            // |>
            if c == '|' && self.peek2() == Some('>') {
                self.bump(); self.bump();
                out.push(Tok::Pipe);
                continue;
            }
            // diğer her şey: tek karakter op/boşluk
            self.bump();
            // ardışık op/boşlukları tek Op'ta toplama: basit tут tek tek
            out.push(Tok::Op(c.to_string()));
        }
        out
    }

    // string tara: açılış tırnağından kapanışa, escape farkında. Üçlü tırnak destekli.
    fn scan_string(&mut self, prefix: Option<char>) -> String {
        let mut s = String::new();
        if let Some(p) = prefix { s.push(p); }
        let quote = self.peek().unwrap();
        // üçlü mü
        let triple = self.peek2() == Some(quote)
            && self.src.get(self.pos + 2).copied() == Some(quote);
        if triple {
            for _ in 0..3 { s.push(self.bump().unwrap()); }
            // kapanışa kadar
            loop {
                match self.peek() {
                    None => break,
                    Some(ch) => {
                        if ch == quote
                            && self.peek2() == Some(quote)
                            && self.src.get(self.pos + 2).copied() == Some(quote) {
                            for _ in 0..3 { s.push(self.bump().unwrap()); }
                            break;
                        }
                        s.push(ch);
                        self.bump();
                    }
                }
            }
        } else {
            s.push(self.bump().unwrap()); // açılış tırnağı
            let mut esc = false;
            while let Some(ch) = self.peek() {
                s.push(ch);
                self.bump();
                if esc { esc = false; continue; }
                if ch == '\\' { esc = true; continue; }
                if ch == quote { break; }
                if ch == '\n' { break; } // tek satır string, kaçış güvenliği
            }
        }
        s
    }
}

// // -> # ama yalnızca satırın ilk anlamlı karakteri //' ise. Satır ortasındaki
// //'a dokunmuyorum bilerek: `x = a // b` Python'da tam bölme operatörü, onu
// yorum sanıp # yaparsam kodu öldürürüm. lstrip sonrası bakmak Python tarafıyla
// birebir aynı davranış.
fn yorum_cevir(src: &str) -> String {
    let mut out = String::with_capacity(src.len());
    for (i, line) in src.split('\n').enumerate() {
        if i > 0 { out.push('\n'); }
        let trimmed = line.trim_start();
        if let Some(rest) = trimmed.strip_prefix("//") {
            let indent_len = line.len() - trimmed.len();
            out.push_str(&line[..indent_len]);
            out.push('#');
            out.push_str(rest);
        } else {
            out.push_str(line);
        }
    }
    out
}

// Token akışını Python kaynağına yaz. Pipe dönüşümü tek bir satırın tamamını
// görmek zorunda (x |> f |> g hepsi aynı satırda), bu yüzden önce Newline'lara
// göre satırlara bölüp her satırı kendi içinde işliyorum.
fn emit(tokens: &[Tok]) -> String {
    // satırlara böl (Newline ayır)
    let mut lines: Vec<Vec<Tok>> = vec![Vec::new()];
    for t in tokens {
        if let Tok::Newline = t {
            lines.push(Vec::new());
        } else {
            lines.last_mut().unwrap().push(t.clone());
        }
    }
    let mut out = String::new();
    for (i, line) in lines.iter().enumerate() {
        if i > 0 { out.push('\n'); }
        out.push_str(&emit_line(line));
    }
    out
}

fn emit_line(line: &[Tok]) -> String {
    let has_pipe = line.iter().any(|t| matches!(t, Tok::Pipe));
    if !has_pipe {
        return lower_with_range(line).concat();
    }
    rewrite_pipe(line)
}

// `1..10` gibi bir aralığı `range(1, 10)`'a çevirmek için sadece range
// token'ına bakmak yetmiyor: solundaki ve sağındaki operand'ı da bilmem
// gerekiyor. Bu yüzden iş regex'le değil token dizisi üzerinde yapılıyor —
// komşulara ancak burada erişebiliyoruz.
fn lower_with_range(line: &[Tok]) -> Vec<String> {
    // önce her token'ı string'e indir (range hariç placeholder)
    let strs: Vec<String> = line.iter().map(|t| match t {
        Tok::Word(w) => keyword(w).map(|k| k.to_string()).unwrap_or_else(|| w.clone()),
        Tok::Number(n) => n.clone(),
        Tok::Str(s) => fstring_cevir(s),
        Tok::Comment(c) => c.clone(),
        Tok::Op(o) => o.clone(),
        Tok::Range(_) => "\x00R\x00".to_string(),
        Tok::Pipe => "|>".to_string(),
        Tok::Newline => String::new(),
    }).collect();

    // range çöz: anlamlı (boşluk olmayan) sol ve sağ komşuyu bul
    let mut out = strs.clone();
    for (idx, t) in line.iter().enumerate() {
        if let Tok::Range(inclusive) = t {
            // sol operand: idx'ten geri, boşluk-only Op atla
            let left = prev_operand(&line, &strs, idx);
            let right = next_operand(&line, &strs, idx);
            if let (Some((ls, le)), Some((rs, re))) = (left, right) {
                let left_txt: String = strs[ls..=le].concat();
                let right_txt: String = strs[rs..=re].concat();
                let upper = if *inclusive { format!("{} + 1", right_txt.trim()) } else { right_txt.trim().to_string() };
                let replacement = format!("range({}, {})", left_txt.trim(), upper);
                // sol..sağ aralığını temizle, range token konumuna replacement
                for k in ls..=re { out[k] = String::new(); }
                out[idx] = replacement;
            }
        }
    }
    out
}

// idx'ten sola doğru ilk operand parçasının (başlangıç,bitiş) index aralığı
fn prev_operand(line: &[Tok], _strs: &[String], idx: usize) -> Option<(usize, usize)> {
    let mut j = idx;
    // boşlukları atla
    while j > 0 {
        j -= 1;
        if is_ws(&line[j]) { continue; }
        // operand: Word/Number; ardışık Word/Number/Op('.')/() basit tut → tek token al
        return Some((j, j));
    }
    None
}

fn next_operand(line: &[Tok], _strs: &[String], idx: usize) -> Option<(usize, usize)> {
    let mut j = idx + 1;
    while j < line.len() {
        if is_ws(&line[j]) { j += 1; continue; }
        return Some((j, j));
    }
    None
}

fn is_ws(t: &Tok) -> bool {
    matches!(t, Tok::Op(o) if o.chars().all(|c| c == ' ' || c == '\t'))
}

// pipe satırı yeniden yaz: x |> f |> g  ->  g(f(x))
fn rewrite_pipe(line: &[Tok]) -> String {
    // Range'i pipe'tan önce çözüyorum ki `1..10 |> topla` gibi bir satırda
    // aralık zaten range(...) olmuş halde gelsin; aksi halde |> böldükten
    // sonra komşu bilgisi dağılır ve range'i çözemezdim.
    let lowered = lower_with_range(line);
    // Segmentlere ayırırken parantez derinliğini sayıyorum: yalnızca depth==0
    // konumdaki |> gerçek pipe. f(a |> b) içindeki bir |> olsa (ki şu an yok)
    // bölme noktası sayılmamalı — bu yüzden depth kontrolü.
    let mut segs: Vec<String> = Vec::new();
    let mut cur = String::new();
    let mut depth: i32 = 0;
    for s in &lowered {
        if s == "|>" && depth == 0 {
            segs.push(cur.clone());
            cur.clear();
            continue;
        }
        for ch in s.chars() {
            match ch {
                '(' | '[' | '{' => depth += 1,
                ')' | ']' | '}' => depth -= 1,
                _ => {}
            }
        }
        cur.push_str(s);
    }
    segs.push(cur);

    if segs.len() < 2 {
        return lowered.concat();
    }

    // İlk segmentteki "x = " veya "return " önekini gövdeden ayırıyorum.
    // Çünkü zincir `f(g(x))` haline gelirken bu önek en dışta kalmalı:
    // `sonuc = veri |> temizle` → `sonuc = temizle(veri)`, `temizle(sonuc = veri)`
    // değil. Önek ayrılmazsa atama yanlış yere gömülürdü.
    let first = segs[0].clone();
    let (prefix, mut expr) = split_prefix(&first);
    expr = expr.trim().to_string();
    for seg in &segs[1..] {
        let seg = seg.trim();
        if seg.ends_with(')') && seg.contains('(') {
            let ac = seg.find('(').unwrap();
            let fn_ = &seg[..ac];
            let args = seg[ac + 1..seg.len() - 1].trim();
            if args.is_empty() {
                expr = format!("{}({})", fn_, expr);
            } else {
                expr = format!("{}({}, {})", fn_, expr, args);
            }
        } else {
            expr = format!("{}({})", seg, expr);
        }
    }
    format!("{}{}", prefix, expr)
}

// "  sonuc = X" -> ("  sonuc = ", "X");  "  return X" -> ("  return ", "X")
fn split_prefix(s: &str) -> (String, String) {
    // indent
    let indent_len = s.len() - s.trim_start().len();
    let (indent, rest) = s.split_at(indent_len);
    // İlk top-level '=' atama işareti. Ama ==, <=, >=, != karşılaştırma —
    // onları atama sanmamak için bir önceki/sonraki karaktere bakıyorum.
    // Parantez içindeyken (depth>0) görülen '=' de keyword argümanı olabilir,
    // o yüzden sadece depth==0'da atama kabul ediyorum.
    let bytes: Vec<char> = rest.chars().collect();
    let mut depth = 0;
    for i in 0..bytes.len() {
        match bytes[i] {
            '(' | '[' | '{' => depth += 1,
            ')' | ']' | '}' => depth -= 1,
            '=' if depth == 0 => {
                let prev = if i > 0 { bytes[i-1] } else { ' ' };
                let next = bytes.get(i+1).copied().unwrap_or(' ');
                if prev != '=' && prev != '!' && prev != '<' && prev != '>' && next != '=' {
                    let pre: String = bytes[..=i].iter().collect();
                    let post: String = bytes[i+1..].iter().collect();
                    // '=' sonrası tek boşluk garanti (expr trim edileceği için)
                    return (format!("{}{} ", indent, pre.trim_end()), post);
                }
            }
            _ => {}
        }
    }
    // return / dondur(zaten return'e çevrildi) / yield
    for kw in ["return ", "yield "] {
        if let Some(r) = rest.strip_prefix(kw) {
            return (format!("{}{}", indent, kw), r.to_string());
        }
    }
    (indent.to_string(), rest.to_string())
}

// f-string özel durum: stringin gövdesine dokunulmaz ama `{...}` içi gerçek
// kod, oradaki Türkçe keyword'ler de çevrilmeli. Yani f"{eger}" değil ama
// f"sonuc: {topla(a, b)}" içindeki ifadeyi çevirmem lazım. {{ ve }} ise
// kaçış — onları ayraç sanıp içine girersem string'i bozarım, o yüzden
// çift süslüyü atlıyorum.
fn fstring_cevir(s: &str) -> String {
    let is_f = s.starts_with("f\"") || s.starts_with("f'")
        || s.starts_with("rf") || s.starts_with("fr")
        || s.starts_with("F\"") || s.starts_with("F'");
    if !is_f || !s.contains('{') {
        return s.to_string();
    }
    let chars: Vec<char> = s.chars().collect();
    let mut out = String::with_capacity(s.len());
    let mut i = 0;
    while i < chars.len() {
        let c = chars[i];
        if c == '{' {
            if chars.get(i + 1) == Some(&'{') {
                out.push_str("{{");
                i += 2;
                continue;
            }
            // blok içeriğini topla (iç içe {} basitçe say)
            let mut depth = 1;
            let mut blok = String::new();
            i += 1;
            while i < chars.len() && depth > 0 {
                let ch = chars[i];
                if ch == '{' { depth += 1; }
                else if ch == '}' { depth -= 1; if depth == 0 { break; } }
                blok.push(ch);
                i += 1;
            }
            out.push('{');
            out.push_str(&kelime_cevir_segment(&blok));
            out.push('}');
            i += 1; // kapanan }
        } else if c == '}' && chars.get(i + 1) == Some(&'}') {
            out.push_str("}}");
            i += 2;
        } else {
            out.push(c);
            i += 1;
        }
    }
    out
}

// Düz kod segmentinde (string olmadan) kelime sınırlı keyword çevirisi.
fn kelime_cevir_segment(seg: &str) -> String {
    let chars: Vec<char> = seg.chars().collect();
    let mut out = String::new();
    let mut i = 0;
    while i < chars.len() {
        let c = chars[i];
        if c == '_' || c.is_alphabetic() {
            let mut w = String::new();
            while i < chars.len() && (chars[i] == '_' || chars[i].is_alphanumeric()) {
                w.push(chars[i]);
                i += 1;
            }
            out.push_str(keyword(&w).unwrap_or(&w));
        } else {
            out.push(c);
            i += 1;
        }
    }
    out
}

/// Kahin kaynağını Python kaynağına çevir.
#[pyfunction]
fn to_python(src: &str) -> String {
    let pre = yorum_cevir(src);
    let mut lx = Lexer::new(&pre);
    let toks = lx.run();
    emit(&toks)
}

/// Debug: token tiplerini string listesi olarak döndür.
#[pyfunction]
fn tokenize_debug(src: &str) -> Vec<String> {
    let pre = yorum_cevir(src);
    let mut lx = Lexer::new(&pre);
    lx.run().iter().map(|t| format!("{:?}", t)).collect()
}

#[pymodule]
fn kahin_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(to_python, m)?)?;
    m.add_function(wrap_pyfunction!(tokenize_debug, m)?)?;
    Ok(())
}
