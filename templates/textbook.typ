// Textbook template (numeric branch) — black-and-white academic layout.
// The books this pipeline produces are in Turkish, so component names and labels are Turkish.
// See docs/architecture.md for an English glossary of the components.
//
// Usage:  #import "textbook.typ": *
//         #show: ders.with(ders-adi: "...", surum: "...", paraf: "...")
//
// Layer labels are ALWAYS printed as text; there are no background colours.
// Layers are distinguished by label + thin rule, so the book survives grayscale printing.

#let renk = (
  metin: rgb("#20252a"), baslik: rgb("#243747"), vurgu: rgb("#243747"), gri: rgb("#606a71"),
  // Zemin tonları bilerek beyaz: çağıran kod "ton:" verse de baskıda renk çıkmaz.
  hoca: white, ai: white, ek: white, cozum: white,
  cizgi: rgb("#d1d9db"),
)

// upper() is not Turkish-aware (i -> I instead of İ); fix strings before upper-casing.
#let tr-upper(s) = if type(s) == str { upper(s.replace("i", "İ")) } else { upper(s) }

// paraf: optional faint mark printed bottom-centre on every page (and used as PDF author).
// The QA step counts it to prove that every page went through the same build.
#let ders(ders-adi: "", surum: "", paraf: none, body) = {
  set document(title: ders-adi, author: if paraf == none { () } else { paraf })
  set text(lang: "tr", font: ("New Computer Modern", "Libertinus Serif"), size: 11.2pt, fill: renk.metin)
  // Ölçüler onaylı referans tasarımla aynı: 11.2 pt, satır adımı ~14.6 pt, 22 mm kenar.
  // Ferahlık satır aralığıyla değil, bloklar arası boşluk + kenar notu sütunu + büyük (display) kesirlerle sağlanır.
  set par(leading: 0.62em, spacing: 1.1em, justify: true)
  set list(spacing: 0.7em, indent: 2mm)
  set enum(spacing: 0.7em, indent: 2mm)
  show math.equation.where(block: true): set block(above: 0.9em, below: 0.9em)
  show heading.where(level: 1): set block(below: 0.9em)
  set page(
    paper: "a4",
    margin: (left: 22mm, right: 17mm, top: 22mm, bottom: 22mm),
    header: text(size: 8pt, fill: renk.gri, font: "Arial")[#tr-upper(ders-adi) #h(1fr) #surum],
    footer: context {
      line(length: 100%, stroke: 0.4pt + renk.cizgi)
      v(-1mm)
      // Paraf: her sayfada orta altta silik işaret; dikkat çekmeyecek açıklıkta
      grid(columns: (1fr, auto, 1fr), align: (left, center, right),
        [],
        text(size: 6.5pt, fill: rgb("#c3c9cc"), font: "Arial", tracking: 0.04em)[#if paraf != none { paraf }],
        text(size: 8pt, fill: renk.gri, font: "Arial")[#counter(page).display()])
    },
  )
  show heading.where(level: 1): set text(size: 22pt, weight: "bold", fill: renk.baslik, font: "New Computer Modern")
  show heading.where(level: 2): set text(size: 13pt, weight: "bold", fill: renk.vurgu)
  body
}

// Etiket satırı: katman adı her zaman yazılı (zeminsiz, küçük kalın büyük harf)
#let etiket(metin, ton: none) = block(
  width: 100%, above: 0pt,
  text(size: 8pt, weight: "bold", tracking: 0.06em, font: "Arial", fill: renk.baslik)[#tr-upper(metin)],
)

// Sağ kenar notu: gövdeyle AYNI bakışta (satır içi yan sütun)
#let kenar(baslik, metin) = box(width: 100%)[
  #set par(justify: false, leading: 0.7em)
  #text(size: 8pt, weight: "bold", font: "Arial")[#baslik] \
  #text(size: 8pt, fill: renk.gri, font: "Arial")[#metin]
]

// Gövde + kenar notu sütunu yan yana
#let yan(govde, ..notlar) = grid(
  columns: (3fr, 1fr), column-gutter: 8mm,
  govde,
  stack(spacing: 6mm, ..notlar.pos()),
)

#let adim(no, baslik, etiket-turu: none, body) = {
  v(4mm)
  // sticky: adım başlığı sayfa sonunda gövdesinden ayrı kalmasın (25 Eki)
  // below 3 mm: gövdenin ilk satırındaki büyük (display) kesir başlığa binmesin
  block(sticky: true, below: 3mm,text(weight: "bold", size: 10.5pt, font: "Arial")[#no #h(1mm) #baslik #if etiket-turu != none [· #text(fill: renk.vurgu)[#etiket-turu]]])
  body
}

#let sonuc-kutusu(baslik, body) = {
  v(3mm)
  text(weight: "bold", size: 10pt, font: "Arial")[#baslik]
  v(2mm)
  block(stroke: 0.8pt + renk.baslik, inset: 10pt, width: 100%, align(center, body))
}

// Ek blok: zeminsiz; üstte ince çizgi + kalın başlık (referanstaki "3 AI eklemesi" bölümü gibi)
#let ek-kutu(baslik, body, ton: none) = block(stroke: (top: 0.5pt + renk.cizgi), inset: (top: 9pt, bottom: 3pt), above: 6mm, below: 6mm, width: 100%, breakable: false)[
  #text(weight: "bold", size: 10pt, font: "Arial", fill: renk.baslik)[#baslik] \
  #body
]

#let altbilgi(metin) = place(bottom + left, dy: 12mm, text(size: 8pt, fill: renk.gri, font: "Arial")[#metin])

// Sayfa başlığı: 1. düzey başlıkla aynı görünüm, ama heading değil. Yer imi olmayan heading'ler
// PDF yer imi ağacını her soruda sıfırlıyordu (25 Eki 2026); ağaç yalnız yer-imi() başlıklarından kurulur.
#let sayfa-basligi(metin) = block(above: 0pt, below: 0.9em, sticky: true,
  text(size: 22pt, weight: "bold", fill: renk.baslik, font: "New Computer Modern", metin))

// ---- Gezinme (kullanıcı, 25 Eki 2026: "içindekilerden tıklanarak gidilmiyor") ----
// Görünmez başlıklar PDF yer imi ağacını kurar (Bölüm → Bölüm X soruları → soru); etiketler tıklanabilir bağlantıların hedefidir.
#let romen = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX")
#let _imli-sorular = state("imli-sorular", ())
#let _son-soru-bolumu = state("son-soru-bolumu", "")

#let yer-imi(seviye, metin, etiket: none) = {
  let h = heading(level: seviye, outlined: true, bookmarked: true, metin)
  place(hide(if etiket == none { h } else { [#h#label(etiket)] }))
}

// Sorunun ilk sayfasına (hoca notu ya da kendin çöz) bir kez yer imi + "soru-<id>" etiketi koyar
#let soru-imi(id) = {
  let id = id.replace("ÖRNEK ", "").trim()
  let on = id.split(".").first()
  context {
    if id not in _imli-sorular.get() {
      if on in romen and _son-soru-bolumu.get() != on { yer-imi(2, "Bölüm " + on + " soruları") }
      yer-imi(if on in romen { 3 } else { 2 }, "Soru " + id, etiket: "soru-" + id)
    }
  }
  _imli-sorular.update(a => if id in a { a } else { a + (id,) })
  _son-soru-bolumu.update(on)
}

// Etiketli yere tıklanabilir bağlantı (etiket yoksa düz metin; derleme kırılmaz)
#let git(etiket, metin) = context {
  let q = query(label(etiket))
  if q.len() == 0 { metin } else { link(q.first().location(), metin) }
}

// İçindekiler satırı: metin ..... sayfa (tamamı tıklanabilir)
#let ic-satir(etiket, metin) = block(width: 100%, above: 0.5em, below: 0.5em, context {
  let q = query(label(etiket))
  if q.len() == 0 { metin } else {
    let loc = q.first().location()
    link(loc)[#metin #box(width: 1fr, repeat[#h(2pt).#h(2pt)]) #counter(page).at(loc).first()]
  }
})

// Soru dizini hücresi: kimlik (tıklanabilir) + sayfa
#let soru-git(id) = context {
  let q = query(label("soru-" + id))
  if q.len() == 0 { id } else {
    let loc = q.first().location()
    link(loc)[#text(fill: renk.vurgu, weight: "bold")[#id] #text(size: 8pt, fill: renk.gri)[s. #counter(page).at(loc).first()]]
  }
}

// İçindekiler: romen numaralı, tıklanabilir bölüm satırları ("bolum-N" etiketlerine)
#let ic-bolumler(..maddeler) = grid(columns: (14mm, 1fr), row-gutter: 0.6em,
  ..maddeler.pos().enumerate().map(((i, m)) => (numbering("I.", i + 1), ic-satir("bolum-" + str(i + 1), m))).flatten())

// ---- 4 sayfalık örnek döngüsü ----
// 1) Hoca notu
#let hoca-notu(id, baslik, alt, soru, govde, komut: [Verilen diferansiyel denklemin genel çözümünü bulunuz.], kenar-notlari: (), kaynak: "") = {
  pagebreak(weak: true)
  soru-imi(id)
  etiket("HOCA NOTU · " + id)
  v(4mm)
  sayfa-basligi(baslik)
  text(fill: renk.gri, size: 10pt)[#alt]
  v(3mm)
  komut
  align(center, soru)
  line(length: 100%, stroke: 0.5pt + renk.cizgi)
  text(size: 9pt, fill: renk.gri)[İşlemler kaynaktan aktarılmıştır. Adım başlıkları editoryaldir.]
  yan(govde, ..kenar-notlari)
  v(1fr)
  text(size: 8pt, fill: renk.gri, font: "Arial")[Kaynak: #kaynak]
}

// 2) AI açıklaması
#let ai-aciklama(id, baslik, alt, govde, ek: none, kenar-notlari: (), kaynak: "") = {
  pagebreak(weak: true)
  etiket("AI AÇIKLAMASI · " + id, ton: renk.ai)
  v(4mm)
  sayfa-basligi(baslik)
  text(fill: renk.gri, size: 10pt)[#alt]
  v(3mm)
  yan(govde, ..kenar-notlari)
  if ek != none { v(3mm); ek-kutu("AI eklemesi — hocanın notunda yok", ek) }
  v(1fr)
  text(size: 8pt, fill: renk.gri, font: "Arial")[Kaynak: #kaynak]
}

// 3) Kendin çöz (çözüm görünmez)
#let kendin-coz(id, soru, komut: [Verilen diferansiyel denklemin genel çözümünü bulunuz.], kaynak: "") = {
  pagebreak(weak: true)
  soru-imi(id)
  etiket("ÇALIŞMA KİTAPÇIĞI · " + id)
  v(4mm)
  sayfa-basligi("Kendin çöz")
  komut
  align(center, soru)
  text(size: 9pt, font: "Arial", fill: renk.gri)[Tarih: #box(width: 40mm, repeat[.]) #h(1fr) Deneme: #box(width: 15mm, repeat[.])]
  v(4mm)
  text(weight: "bold", size: 9pt, font: "Arial")[ÇÖZÜM ALANI]
  for _ in range(10) { v(11mm); line(length: 100%, stroke: 0.4pt + renk.cizgi) }
  v(4mm)
  text(size: 9pt, font: "Arial", fill: renk.gri)[Takıldığım adım / tekrar notum:]
  v(8mm)
  line(length: 100%, stroke: 0.4pt + renk.cizgi)
  v(1fr)
  text(size: 8pt, fill: renk.gri, font: "Arial")[Kaynak: #kaynak]
}

// 4) Adım adım çözüm — matematik önde, yazı az (kullanıcı, 25 Eki 2026: "yazıdan çok rakamla anlarız").
// Yan not sütunu YOK (sıkışık buldu); katman etiketi adım başlığında yazılı. Kesirler büyük (display) boyda.
#let adim-cozum(id, adimlar, sonuc, kaynak: "") = {
  pagebreak(weak: true)
  etiket("ÇÖZÜM KİTAPÇIĞI · " + id, ton: renk.cozum)
  v(4mm)
  sayfa-basligi("Adım adım çözüm")
  // Denetim (25 Eki 2026): hocanın çözmediği sorularda da görünüyordu; koşullu yazıldı.
  text(fill: renk.gri, size: 10pt)[Kaynakta çözüm varsa hoca yöntemi esas alınır. Her adımın kime ait olduğu (hoca / AI) adım başlığında yazılıdır.]
  v(2mm)
  {
    show math.frac: it => math.display(it)
    for (i, a) in adimlar.enumerate() {
      adim(str(i + 1), a.baslik, etiket-turu: a.tur, a.govde)
    }
    // Sonuç kutusu da büyük kesirle (denetim 25 Eki: kutudaki kesirler küçük basılıyordu)
    v(4mm)
    sonuc-kutusu("Çözüm bütünü", sonuc)
  }
  v(1fr)
  text(size: 8pt, fill: renk.gri, font: "Arial")[Kaynak: #kaynak]
}

// ---- Uluslararası ders kitabı bileşenleri (Zill, Boyce–DiPrima, Lebl tarzı) ----
// Numaralar elle verilir ve sabit kalır (Lebl: bölüm/alıştırma numaraları sürümler arası değişmez).

// Bölüm açılışı: "Bu bölümde" hedefleri + sayfa izlenebilirlik notu (Zill: bölüm başı; study-coach: kaynak sayfa notu)
#let bolum-baslangic(no, baslik, hedefler, kaynak-sayfalar: "", kaynak-dosya: "") = {
  pagebreak(weak: true)
  yer-imi(1, [Bölüm #numbering("I", no) · #baslik], etiket: "bolum-" + str(no))
  etiket("BÖLÜM " + numbering("I", no))
  v(4mm)
  sayfa-basligi(baslik)
  text(size: 9pt, style: "italic", fill: renk.gri)[Bu konu, «#kaynak-dosya» isimli özgün dokümanın #kaynak-sayfalar sayfalarındadır.]
  v(3mm)
  ek-kutu("Bu bölümde", list(..hedefler), ton: renk.hoca)
}

// Tanım / Teorem: çerçeveli, sabit numaralı (Boyce–DiPrima, Zill)
#let tanim(no, ad, body) = block(stroke: (left: 2pt + renk.vurgu), inset: (left: 11pt, y: 6pt), above: 5mm, below: 5mm, width: 100%, breakable: false)[
  #text(weight: "bold", font: "Arial", size: 10pt)[Tanım #no] #if ad != none [(#ad)] \
  #body
]
#let teorem(no, ad, body) = block(stroke: 0.6pt + renk.baslik, inset: 12pt, above: 5mm, below: 5mm, width: 100%, breakable: false)[
  #text(weight: "bold", font: "Arial", size: 10pt)[Teorem #no] #if ad != none [(#ad)] \
  #body
]

// Not (Zill "Remarks"): ana akışı bölmeyen yorum
#let not-kutu(body, baslik: "Not") = block(stroke: 0.5pt + renk.cizgi, inset: 11pt, above: 5mm, below: 5mm, width: 100%, breakable: false)[
  #text(weight: "bold", size: 9pt, font: "Arial")[#baslik.] #text(size: 10pt)[#body]
]

// Bölüm sonu: özet (Zill "Chapter in Review") + kendini denetle (Dunlosky: practice testing)
#let ozet-kutu(maddeler) = ek-kutu("Bölüm özeti", list(..maddeler), ton: renk.hoca)
#let kendini-denetle(sorular) = ek-kutu("Kendini denetle · AI çalışma soruları", enum(..sorular), ton: renk.ai)

// Ek okuma: yalnız AI katmanı, otoriter açık kaynak
#let ek-okuma(ad, url) = text(size: 9pt, fill: renk.gri)[Ek okuma (AI eklemesi): #link(url)[#ad]. Hoca notunun yerine geçmez.]
