// SYNTHETIC EXAMPLE — not taken from any lecturer's notes.
// The "lecturer note" page below is invented to show how the layers are typeset.
// Build from the repository root:
//   typst compile examples/numeric-branch/main.typ examples/numeric-branch/example.pdf --root .
#import "../../templates/textbook.typ": *

#let AC = "AI çözümü"
#let H = "hoca hesabı"
#let HS = "hoca sonucu"
#let kaynak = "C-001 · sentetik örnek"

#show: ders.with(ders-adi: "Sentetik örnek · Diferansiyel denklemler", surum: "örnek", paraf: "sample")

#bolum-baslangic(1, "Birinci mertebe lineer denklemler",
  ([$y' + p(x) y = q(x)$ biçimini tanımak], [İntegrasyon çarpanı ile çözmek], [Sonucu yerine koyarak denetlemek]),
  kaynak-sayfalar: "C-001", kaynak-dosya: "sentetik_not.pdf")

#tanim("I.1", "Lineer denklem")[
  $y' + p(x) y = q(x)$ biçiminde yazılabilen birinci mertebe denklem. İntegrasyon çarpanı $mu(x) = e^(integral p(x) thin d x)$.
]

// ---- 4-page cycle: only used when the lecturer's own solution is visible in the source ----

#hoca-notu("I.1", "Örnek I.1", "Sabit katsayılı lineer denklem",
  $ y' + 2 y = 4 $,
  [
    $ mu = e^(2x) $
    $ (y e^(2x))' = 4 e^(2x) $
    $ y e^(2x) = 2 e^(2x) + C $
    $ y = 2 + C e^(-2x) $
  ],
  kenar-notlari: (kenar("Aktarım", [Satırlar kaynak sayfadaki sırayla. Okunamayan sembol olsaydı `[?]` ya da Blocked yazılırdı.]),),
  kaynak: kaynak)

#ai-aciklama("I.1", "Neden çalışıyor?", "AI açıklaması · hoca notunun yeniden anlatımı",
  [
    Çarpan $e^(2x)$ ile çarpınca sol taraf tek bir çarpımın türevi olur:
    $ e^(2x) y' + 2 e^(2x) y = (y e^(2x))' $
    Böylece denklem doğrudan integrallenebilir hâle gelir.
  ],
  ek: [Sonucu denetle: $y = 2 + C e^(-2x)$ için $y' + 2y = -2C e^(-2x) + 4 + 2C e^(-2x) = 4$. Bu iddia `checks/checks_example.py` içinde SymPy ile de sınanır.],
  kaynak: kaynak)

#kendin-coz("I.1", $ y' + 2 y = 4 $, kaynak: kaynak)

#adim-cozum("I.1", (
  (baslik: "İntegrasyon çarpanı", tur: H, govde: $ mu = e^(integral 2 thin d x) = e^(2x) $),
  (baslik: "Çarp ve topla", tur: H, govde: $ (y e^(2x))' = 4 e^(2x) $),
  (baslik: "İntegralle", tur: H, govde: $ y e^(2x) = 2 e^(2x) + C $),
  (baslik: "Yerine koyarak denetle", tur: "AI tamamlaması", govde: $ y' + 2y = -2 C e^(-2x) + 2(2 + C e^(-2x)) = 4 $),
), $ y = 2 + C e^(-2x) $, kaynak: kaynak)

// ---- Question-only item: the source has no solution, so every step is labelled "AI çözümü" ----

#kendin-coz("I.2", $ y' = x y $, kaynak: kaynak)

#adim-cozum("I.2", (
  (baslik: "Değişkenleri ayır", tur: AC, govde: $ (d y) / y = x thin d x $),
  (baslik: "İntegralle", tur: AC, govde: $ ln abs(y) = x^2 / 2 + C_0 $),
  (baslik: "Yerine koyarak denetle", tur: AC, govde: $ y' = x C e^(x^2 \/ 2) = x y $),
), $ y = C e^(x^2 \/ 2) $, kaynak: kaynak)

#kendini-denetle((
  [İntegrasyon çarpanı neden $e^(integral p)$ biçimindedir?],
  [$y' - 3y = 0$ denkleminin genel çözümünü yazın ve yerine koyarak denetleyin.],
))
