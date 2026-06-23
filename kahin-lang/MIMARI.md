# Kahin nasıl çalışıyor

Bu dosya, Kahin'in iç işleyişini ve özellikle Rust hızlandırıcının pipeline'ın
neresine oturduğunu anlatmak için. Kodu ilk kez açan birinin "şu dosya ne işe
yarıyor, veri nereden nereye akıyor" sorusuna cevap versin diye yazdım.

## Kısa özet

Kahin kendi sanal makinesi olan bir dil değil. Türkçe yazılmış kaynağı Python'a
çeviren bir transpiler — çeviriden sonra işi CPython yapıyor. Yani Kahin'in tek
işi şu: `eger`'i `if` yap, `1..10`'u `range(1, 10)` yap, gerisini Python'a bırak.

Bu kararın iyi tarafı, dilin "bedava" olması. Python'da ne varsa (sınıflar,
generatorlar, f-string, match/case, comprehension) Kahin'de de var, çünkü altta
zaten Python çalışıyor. Kötü tarafı da şu: Kahin kodu Python gramerine uymak
zorunda. Python'un olmayan bir şeyi Kahin'e ekleyemiyoruz, sadece isim
değiştiriyoruz veya çeviriden önce metni düzenliyoruz.

## Veri akışı

Bir `.kahin` dosyası çalıştırıldığında sırayla şunlar oluyor:

1. **Ön-işleme.** Kaynaktaki Kahin'e özel şeyler saf Python'a çevriliyor:
   `//` yorumları `#` oluyor, `1..10` → `range(...)`, `x |> f` → `f(x)`,
   f-string içindeki Türkçe kelimeler düzeltiliyor. Bu adım ya Rust'ta
   (varsa `kahin_rs.so`) ya da Python regex'iyle yapılıyor. İkisi de aynı
   çıktıyı veriyor.

2. **Tokenize.** Çıkan metin artık neredeyse Python — sadece anahtar kelimeler
   hâlâ Türkçe (`eger`, `tanimla`...). Python'un kendi `tokenize` modülüne
   veriliyor. Bu modül C'de yazıldığı için hızlı ve girinti/string/parantez
   gibi zor işleri doğru hallediyor; tekrar yazmaya değmez.

3. **Keyword değişimi.** Token akışında her NAME token'ı kontrol ediliyor.
   `eger` görürse `if` yazıyor. Bu, `kahin_lexer.py` içindeki `KEYWORD_MAP`
   sözlüğüyle yapılıyor. Önemli nokta: token'ın konumu (satır/sütun) aynı
   kalıyor, sadece metin değişiyor. Sayesinde hata mesajlarındaki satır
   numaraları `.kahin` dosyasını doğru gösteriyor.

4. **Geri yazma (untokenize).** Token'lar tekrar metne çevriliyor. Artık
   elimizde %100 geçerli Python kaynağı var.

5. **Parse + optimize.** `ast.parse` ile ağaç çıkarılıyor, sonra
   `KahinASTTransformer` üstünden geçiyor. Bu transformer sabit hesapları
   önceden yapıyor (`2 + 3` → `5`), ölü kodu atıyor (`eger yanlis:` bloğu
   siliniyor) gibi küçük optimizasyonlar.

6. **Compile + exec.** Ağaç bytecode'a derleniyor ve çalıştırılıyor. Bu
   noktadan sonra olan biten tamamen normal Python.

Yani Kahin'in kendine ait kısmı 1-3 arası. 4'ten sonrası CPython'un işi.

## Rust hızlandırıcı tam olarak ne yapıyor

En çok karıştırılan yer burası, o yüzden ayrıca açayım.

Rust **sadece 1. adımı** (ön-işleme) yapıyor. AST, optimizasyon, derleme,
çalıştırma — hiçbirine dokunmuyor. Rust'ın görevi şu: ham Kahin metnini al,
Python gramerine uyan bir metin döndür. O kadar.

Neden bu adım ayrı bir hızlandırıcıya değer? Çünkü Python tarafındaki karşılığı
regex'le çalışıyor ve birden çok geçiş yapıyor — önce yorumları çevir, sonra
metni baştan tara aralıkları bul, sonra bir daha tara pipe'ları bul. Her geçiş
tüm dosyayı dolaşıyor. Rust versiyonu ise tek geçişte, elle yazılmış bir
tarayıcıyla (`lib.rs` içindeki `Lexer`) hepsini bir arada hallediyor. Regex
motoru bile yok, karakter karakter ilerliyor.

İşin püf noktası string koruması. Düşün: `1..10` bir aralık, çevrilmeli. Ama
`"1..10"` bir metin literali, dokunulmamalı — kullanıcı öyle yazmış. Aynı şey
`x |> f` ile `"x |> f"` için de geçerli. Tarayıcının asıl zorluğu kodu metinden
ayırt etmek. Rust bunu token tipleriyle çözüyor: string'ler `Tok::Str` olarak
işaretleniyor ve çevrim aşamasında es geçiliyor, sadece kod parçaları
(`Tok::Word`, `Tok::Range`, `Tok::Pipe`) işleniyor.

f-string biraz daha çetrefilli, çünkü `f"sonuc: {eger ? ...}"` gibi bir şeyde
tırnağın içi metin ama `{...}` bloğunun içi kod. Rust f-string'i ayrıca tarayıp
sadece süslü parantez içindeki Türkçe kelimeleri çeviriyor, geri kalan metne
dokunmuyor (`fstring_cevir`).

### Araya nasıl giriyor

`kahin_lexer.py` açılırken `import kahin_rs` deniyor. `.so` dosyası yanındaysa
yükleniyor ve ön-işleme Rust'a gidiyor. Yoksa `_kahin_rs = None` kalıyor ve
Python regex hattına düşülüyor. Kullanıcı farkı görmüyor — çıktı birebir aynı,
sadece biri ötekinden hızlı. Yani Rust isteğe bağlı bir turbo; olmasa da dil
çalışır.

Bu fallback önemli, çünkü `.so` sadece Linux x86-64 + aynı Python ABI'sinde
yükleniyor. Başka platformda Rust devre dışı kalıyor ama Python yedeği devraldığı
için dil yine çalışmaya devam ediyor.

## Dosyalar

- `kahin_cli.py` — giriş noktası. Argümanları okur, dosya mı REPL mi karar
  verir, cache'e bakar, çeviriyi tetikler, sonucu çalıştırır. Hata olursa
  Türkçeleştirip basar.
- `kahin_lexer.py` — tokenize + keyword değişimi + ön-işleme (Python yedeği
  burada). Rust varsa ön-işlemeyi ona devreder.
- `kahin_ast.py` — `ast.parse` sarmalayıcısı ve optimize eden transformer.
- `kahin_cache.py` — derlenmiş bytecode'u `~/.kahin_cache/` altına yazıp tekrar
  okuyor, böylece değişmeyen dosya ikinci çalıştırmada baştan derlenmiyor.
- `kahin_hata.py` — Python exception'larını Türkçe mesaja çeviriyor.
- `kahin_repl.py` — interaktif kabuk.
- `kahin_lib/` — Türkçe standart kütüphane (`dosya`, `veri`, `zaman`).
- `kahin_rs/` — Rust ön-işleme kaynağı; derlenince `kahin_rs.so` çıkıyor.

## Tek dosya binary

`build_nuitka.py`, Nuitka ile her şeyi (Python motoru dahil) tek bir çalıştırılabilir
dosyaya gömüyor. Çıktı `dist/kahin` — hedef makinede Python kurulu olmasa bile
çalışıyor, çünkü gömülü bir Python taşıyor. `ldd dist/kahin` çıktısında libpython
görünmüyor, sadece libc var; yani gerçekten standalone.

Dikkat edilecek iki şey:

- `kahin_lib` modülleri runtime'da `ice_aktar dosya` gibi dinamik import
  ediliyor. Nuitka statik analizle bunları göremediği için build script'te
  `--include-module` ile elle ekleniyor. Atlanırsa binary derlenir ama kullanıcı
  `ice_aktar dosya` yazınca patlar.
- Binary sadece kendi platformuna (Linux x86-64) taşınabilir. Windows için
  Windows'ta derlemek gerekiyor.
