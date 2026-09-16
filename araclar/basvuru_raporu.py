# -*- coding: utf-8 -*-
"""Bizimkent FEST basvurularini komisyonlara gore siniflandirip
tiklanabilir telefon / e-posta / link iceren PDF rapor uretir."""
import re, html, datetime
import openpyxl
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, CondPageBreak, PageBreak)

import argparse

_ap = argparse.ArgumentParser(
    description="Google Form basvuru tablosundan komisyon bazli PDF rapor uretir.")
_ap.add_argument("xlsx", help="Google Form yanitlarinin indirilmis .xlsx dosyasi")
_ap.add_argument("-o", "--cikti", default="Bizimkent_FEST_Basvuru_Raporu.pdf",
                 help="Uretilecek PDF dosyasinin adi")
_args = _ap.parse_args()
SRC, OUT = _args.xlsx, _args.cikti

import glob as _glob
import os as _os


def _font(*adaylar):
    """Turkce karakterleri destekleyen ilk uygun TTF dosyasini bulur."""
    for kalip in adaylar:
        for yol in sorted(_glob.glob(kalip, recursive=True)):
            if _os.path.isfile(yol):
                return yol
    raise SystemExit("Uygun yazi tipi bulunamadi: %s" % (adaylar,))


pdfmetrics.registerFont(TTFont("DJV", _font(
    "/usr/share/fonts/**/DejaVuSans.ttf", "/usr/share/fonts/**/LiberationSans-Regular.ttf",
    "/Library/Fonts/Arial Unicode.ttf", "C:/Windows/Fonts/arial.ttf")))
pdfmetrics.registerFont(TTFont("DJV-B", _font(
    "/usr/share/fonts/**/DejaVuSans-Bold.ttf", "/usr/share/fonts/**/LiberationSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf")))
pdfmetrics.registerFont(TTFont("DJV-I", _font(
    "/usr/share/fonts/**/LiberationSans-Italic.ttf", "/usr/share/fonts/**/DejaVuSans-Oblique.ttf",
    "/usr/share/fonts/**/DejaVuSans.ttf", "C:/Windows/Fonts/ariali.ttf")))
pdfmetrics.registerFontFamily("DJV", normal="DJV", bold="DJV-B", italic="DJV-I", boldItalic="DJV-B")

# ---------------------------------------------------------------- veri okuma
wb = openpyxl.load_workbook(SRC)
ws = wb.worksheets[0]
rows = list(ws.iter_rows(values_only=True))

C_TS, C_AD, C_ADRES, C_TEL, C_MAIL = 0, 2, 3, 4, 5
C_EKIP, C_SANATCI, C_SANATCI_LINK = 7, 8, 9
C_ATOLYE_FIKRI, C_VOLEYBOL, C_BASKET = 11, 12, 13
C_PAZAR, C_DEMO, C_COCUK_ATOLYE = 17, 18, 19
C_COCUK_AD, C_COCUK_YAS, C_VELI = 20, 21, 22
C_SPONSOR, C_SPONSOR_SEKIL, C_WORKSHOP = 23, 24, 25
C_YETISKIN_ATOLYE = 28
C_STAR, C_STAR_LINK, C_STAND_TUR, C_FUTBOL = 30, 31, 32, 33


def s(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


kayitlar = []
for ri, r in enumerate(rows[2:], start=3):
    if all(v in (None, "") for v in r):
        continue
    kayitlar.append({"satir": ri, "r": r})

# ---------------------------------------------------------------- yardimcilar
URL_RE = re.compile(r"(https?://[^\s<>\"']+)")


def tel_temiz(raw):
    d = re.sub(r"\D", "", s(raw))
    if d.endswith("0") and s(raw).endswith(".0"):
        d = d[:-1]
    if len(d) > 10 and d.startswith("90"):
        d = d[2:]
    if len(d) == 11 and d.startswith("0"):
        d = d[1:]
    if len(d) == 10:
        return d
    return None


def tel_goster(raw):
    d = tel_temiz(raw)
    if not d:
        return html.escape(s(raw)) or "—"
    gosterim = "0%s %s %s %s" % (d[0:3], d[3:6], d[6:8], d[8:10])
    return '<link href="tel:+90%s" color="#1558b0"><u>%s</u></link>' % (d, gosterim)


def mail_goster(raw):
    v = s(raw).replace(" ", "")
    if "@" not in v or "." not in v.split("@")[-1]:
        return html.escape(s(raw)) or "—"
    return '<link href="mailto:%s" color="#1558b0"><u>%s</u></link>' % (
        html.escape(v), html.escape(v))


def linkle(metin):
    """Metin icindeki URL'leri tiklanabilir hale getirir."""
    metin = s(metin)
    if not metin:
        return ""
    parcalar = []
    for parca in URL_RE.split(metin):
        if URL_RE.fullmatch(parca):
            kisa = parca if len(parca) <= 58 else parca[:55] + "…"
            parcalar.append('<link href="%s" color="#1558b0"><u>%s</u></link>'
                            % (html.escape(parca, quote=True), html.escape(kisa)))
        else:
            parcalar.append(html.escape(parca).replace("\n", "<br/>"))
    return "".join(parcalar)


UZUN_METINLER = []   # (ad soyad, baslik, tam metin)
UZUN_SINIR = 330


def kisalt(k, metin, etiket):
    """Cok uzun serbest metinleri tabloda kisaltir, tam halini EK-2'ye tasir."""
    metin = s(metin)
    if len(metin) <= UZUN_SINIR:
        return linkle(metin)
    UZUN_METINLER.append((s(k["r"][C_AD]), etiket, metin))
    no = len(UZUN_METINLER)
    kesme = metin[:UZUN_SINIR].rsplit(" ", 1)[0]
    return (linkle(kesme) +
            ' …<br/><font color="#8a4b00"><b>[Tam metin: EK-2, kayıt %d]</b></font>' % no)


# ---------------------------------------------------------------- stiller
st_h1 = ParagraphStyle("h1", fontName="DJV-B", fontSize=22, leading=27,
                       textColor=colors.HexColor("#0b3d6b"), alignment=TA_CENTER)
st_h2 = ParagraphStyle("h2", fontName="DJV-B", fontSize=13, leading=17,
                       textColor=colors.white)
st_alt = ParagraphStyle("alt", fontName="DJV-I", fontSize=8.5, leading=11,
                        textColor=colors.HexColor("#8a4b00"))
st_p = ParagraphStyle("p", fontName="DJV", fontSize=10, leading=14)
st_pc = ParagraphStyle("pc", parent=st_p, alignment=TA_CENTER)
st_th = ParagraphStyle("th", fontName="DJV-B", fontSize=8.2, leading=10.5,
                       textColor=colors.white, alignment=TA_CENTER)
st_td = ParagraphStyle("td", fontName="DJV", fontSize=8.0, leading=10.5,
                       alignment=TA_LEFT)
st_tdc = ParagraphStyle("tdc", parent=st_td, alignment=TA_CENTER)
st_small = ParagraphStyle("small", fontName="DJV", fontSize=8.5, leading=12,
                          textColor=colors.HexColor("#444444"))

RENK = {
    "ekip": "#1b5e20", "sanatci": "#6a1b9a", "workshop": "#00695c",
    "pazar": "#b35c00", "cocuk": "#0277bd", "yetiskin": "#4527a0",
    "spor": "#c62828", "star": "#ad1457", "sponsor": "#37474f",
    "diger": "#546e7a",
}


def basvuran_hucreleri(k, no):
    r = k["r"]
    ts = r[C_TS]
    tarih = ts.strftime("%d.%m.%Y") if isinstance(ts, datetime.datetime) else "—"
    return [
        Paragraph(str(no), st_tdc),
        Paragraph(html.escape(s(r[C_AD])) or "—", st_td),
        Paragraph(html.escape(s(r[C_ADRES])) or "—", st_td),
        Paragraph(tel_goster(r[C_TEL]), st_td),
        Paragraph(mail_goster(r[C_MAIL]), st_td),
        Paragraph(tarih, st_tdc),
    ]


BASLIKLAR = ["#", "Ad Soyad", "Ada / Blok / Daire", "İletişim No", "E-posta", "Başvuru\nTarihi"]
GENIS = [20, 112, 118, 80, 140, 60]
TOPLAM_GENISLIK = 782
VARSAYILAN_DETAY = TOPLAM_GENISLIK - sum(GENIS)


def bolum(baslik, renk_anahtari, kayit_listesi, ek_baslik, ek_fn, aciklama=None,
          ek_genislik=None):
    """Tek bir komisyon bolumu (baslik + tablo) uretir.

    ek_genislik: detay sutununun genisligi; artan alan adres sutununa eklenir,
    boylece tum bolumler ayni toplam genislikte kalir."""
    renk = colors.HexColor(RENK[renk_anahtari])
    # bolum basliginin sayfa dibinde yalniz kalmamasi icin asgari alan talebi
    ogeler = [CondPageBreak(95)]
    bant = Table([[Paragraph("%s  (%d başvuru)" % (baslik, len(kayit_listesi)), st_h2)]],
                 colWidths=[TOPLAM_GENISLIK])
    bant.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), renk),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    ogeler.append(bant)
    if aciklama:
        ogeler.append(Spacer(1, 3))
        ogeler.append(Paragraph(aciklama, st_alt))
    ogeler.append(Spacer(1, 5))

    if not kayit_listesi:
        ogeler.append(Paragraph("Bu kategoride başvuru bulunmamaktadır.", st_small))
        ogeler.append(Spacer(1, 14))
        return ogeler

    detay_g = ek_genislik or VARSAYILAN_DETAY
    genis = list(GENIS)
    artan = VARSAYILAN_DETAY - detay_g
    genis[1] += round(artan * 0.30)          # Ad Soyad
    genis[4] += round(artan * 0.25)          # E-posta
    genis[2] += artan - round(artan * 0.30) - round(artan * 0.25)   # Adres
    genis.append(detay_g)
    veri = [[Paragraph(b.replace("\n", "<br/>"), st_th) for b in BASLIKLAR + [ek_baslik]]]
    for i, k in enumerate(kayit_listesi, 1):
        veri.append(basvuran_hucreleri(k, i) + [Paragraph(ek_fn(k) or "—", st_td)])

    t = Table(veri, colWidths=genis, repeatRows=1)
    stil = [
        ("BACKGROUND", (0, 0), (-1, 0), renk),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c8d0d8")),
        ("BOX", (0, 0), (-1, -1), 0.9, renk),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]
    for i in range(1, len(veri)):
        if i % 2 == 0:
            stil.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f4f7fa")))
    t.setStyle(TableStyle(stil))
    ogeler.append(t)
    ogeler.append(Spacer(1, 16))
    return ogeler


# ---------------------------------------------------------------- siniflandirma
def var(k, c):
    return s(k["r"][c]) != ""


ekip = [k for k in kayitlar if var(k, C_EKIP)]
sanatci = [k for k in kayitlar if var(k, C_SANATCI)]
workshop = [k for k in kayitlar if var(k, C_WORKSHOP) or var(k, C_ATOLYE_FIKRI)]
pazar = [k for k in kayitlar if var(k, C_PAZAR)]
pazar_ek = [k for k in kayitlar if not var(k, C_PAZAR) and var(k, C_STAND_TUR)]
cocuk = [k for k in kayitlar if var(k, C_COCUK_ATOLYE) or var(k, C_COCUK_AD)]
yetiskin = [k for k in kayitlar if var(k, C_YETISKIN_ATOLYE)]
voleybol = [k for k in kayitlar if var(k, C_VOLEYBOL)]
basketbol = [k for k in kayitlar if var(k, C_BASKET) or var(k, C_FUTBOL)]
star = [k for k in kayitlar if var(k, C_STAR) or var(k, C_STAR_LINK) or var(k, C_DEMO)]
sponsor = [k for k in kayitlar if var(k, C_SPONSOR)]

KATEGORI_SUTUNLARI = [C_EKIP, C_SANATCI, C_WORKSHOP, C_ATOLYE_FIKRI, C_PAZAR,
                      C_STAND_TUR, C_COCUK_ATOLYE, C_COCUK_AD, C_YETISKIN_ATOLYE,
                      C_VOLEYBOL, C_BASKET, C_FUTBOL, C_STAR, C_STAR_LINK,
                      C_DEMO, C_SPONSOR]
kategorisiz = [k for k in kayitlar if not any(var(k, c) for c in KATEGORI_SUTUNLARI)]

# mukerrer kayit tespiti (ayni telefon veya ayni e-posta)
from collections import defaultdict
tel_map, mail_map = defaultdict(list), defaultdict(list)
for k in kayitlar:
    t = tel_temiz(k["r"][C_TEL])
    m = s(k["r"][C_MAIL]).lower().replace(" ", "")
    if t:
        tel_map[t].append(k)
    if "@" in m:
        mail_map[m].append(k)
mukerrer = []
gorulen = set()
for anahtar, grup in list(tel_map.items()) + list(mail_map.items()):
    if len(grup) < 2:
        continue
    imza = tuple(sorted(g["satir"] for g in grup))
    if imza in gorulen:
        continue
    gorulen.add(imza)
    mukerrer.append((anahtar, grup))
mukerrer.sort(key=lambda x: x[1][0]["satir"])

# ---------------------------------------------------------------- belge
def sayfa_dekoru(canvas, doc):
    canvas.saveState()
    g, y = landscape(A4)
    canvas.setFillColor(colors.HexColor("#0b3d6b"))
    canvas.rect(0, y - 16 * mm, g, 16 * mm, stroke=0, fill=1)
    canvas.setFont("DJV-B", 11)
    canvas.setFillColor(colors.white)
    canvas.drawString(14 * mm, y - 10.5 * mm, "BİZİMKENT FEST — Başvuru Değerlendirme Raporu")
    canvas.setFont("DJV", 8.5)
    canvas.drawRightString(g - 14 * mm, y - 10.5 * mm, "Komisyon Dağılım Listesi")
    canvas.setStrokeColor(colors.HexColor("#c8d0d8"))
    canvas.setLineWidth(0.5)
    canvas.line(14 * mm, 12 * mm, g - 14 * mm, 12 * mm)
    canvas.setFont("DJV", 8)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(14 * mm, 7.5 * mm,
                      "Telefon, e-posta ve bağlantılar tıklanabilir. Kişisel veriler KVKK kapsamında yalnızca komisyon çalışmaları için kullanılmalıdır.")
    canvas.drawRightString(g - 14 * mm, 7.5 * mm, "Sayfa %d" % doc.page)
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=landscape(A4),
                      leftMargin=14 * mm, rightMargin=14 * mm,
                      topMargin=21 * mm, bottomMargin=15 * mm,
                      title="Bizimkent FEST Başvuru Raporu",
                      author="Bizimkent FEST Düzenleme Kurulu",
                      subject="Google Form başvurularının komisyon bazlı sınıflandırması")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="ana")
doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=sayfa_dekoru)])

F = []

# --- kapak / ozet
F.append(Spacer(1, 12))
F.append(Paragraph("BİZİMKENT FEST", st_h1))
F.append(Paragraph("Başvuru Değerlendirme ve Komisyon Dağılım Raporu",
                   ParagraphStyle("sub", parent=st_h1, fontSize=13, leading=18,
                                  textColor=colors.HexColor("#444444"))))
F.append(Spacer(1, 10))
ilk = min(k["r"][C_TS] for k in kayitlar if isinstance(k["r"][C_TS], datetime.datetime))
son = max(k["r"][C_TS] for k in kayitlar if isinstance(k["r"][C_TS], datetime.datetime))
F.append(Paragraph(
    "Kaynak: Google Form – <b>Bizimkent FEST Başvuruları</b> &nbsp;|&nbsp; "
    "Toplam <b>%d</b> başvuru &nbsp;|&nbsp; Kayıt aralığı: <b>%s – %s</b> &nbsp;|&nbsp; "
    "Rapor tarihi: <b>%s</b>" % (len(kayitlar), ilk.strftime("%d.%m.%Y"),
                                 son.strftime("%d.%m.%Y"),
                                 datetime.date.today().strftime("%d.%m.%Y")),
    ParagraphStyle("meta", parent=st_pc, fontSize=9.5)))
F.append(Spacer(1, 16))

ozet_satirlar = [
    ("Festival Ekip Gönüllüleri", ekip, "ekip"),
    ("Gönüllü Sanatçılar", sanatci, "sanatci"),
    ("Gönüllü Workshop / Atölye Verenler", workshop, "workshop"),
    ("Bizim Pazar – Stand Başvuruları", pazar, "pazar"),
    ("Çocuk Atölyeleri Ön Kayıt", cocuk, "cocuk"),
    ("Yetişkin Atölye Katılımcıları", yetiskin, "yetiskin"),
    ("Voleybol Turnuvası", voleybol, "spor"),
    ("Basketbol / Futbol Turnuvası", basketbol, "spor"),
    ("Bizim Star Ses Yarışması", star, "star"),
    ("Sponsorluk Başvuruları", sponsor, "sponsor"),
    ("Kategori Seçmemiş Başvurular", kategorisiz, "diger"),
]
ozet = [[Paragraph("KOMİSYON / KATEGORİ", st_th), Paragraph("BAŞVURU SAYISI", st_th),
         Paragraph("KOMİSYON / KATEGORİ", st_th), Paragraph("BAŞVURU SAYISI", st_th)]]
yarim = (len(ozet_satirlar) + 1) // 2
sol, sag = ozet_satirlar[:yarim], ozet_satirlar[yarim:]
while len(sag) < len(sol):
    sag.append(None)
for a, b in zip(sol, sag):
    satir = [Paragraph("<b>%s</b>" % a[0], st_td), Paragraph("<b>%d</b>" % len(a[1]), st_tdc)]
    if b:
        satir += [Paragraph("<b>%s</b>" % b[0], st_td), Paragraph("<b>%d</b>" % len(b[1]), st_tdc)]
    else:
        satir += [Paragraph("", st_td), Paragraph("", st_tdc)]
    ozet.append(satir)
to = Table(ozet, colWidths=[230, 90, 230, 90], hAlign="CENTER")
to.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b3d6b")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c8d0d8")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f7fa")]),
]))
F.append(to)
F.append(Spacer(1, 12))
F.append(Paragraph(
    "<b>Not:</b> Bir başvuru sahibi birden fazla kategoriye başvurabildiği için "
    "kategori toplamları genel başvuru sayısından fazladır. Her komisyon yalnızca "
    "kendi bölümündeki listeden sorumludur.", st_small))
F.append(PageBreak())

# --- bolumler
F += bolum("1. FESTİVAL EKİP GÖNÜLLÜLERİ KOMİSYONU", "ekip", ekip,
           "Ek Başvuruları / Notlar",
           lambda k: " • ".join(filter(None, [
               "Gönüllü sanatçı" if var(k, C_SANATCI) else "",
               "Workshop veriyor" if var(k, C_WORKSHOP) else "",
               "Voleybol" if var(k, C_VOLEYBOL) else "",
               "Basketbol" if (var(k, C_BASKET) or var(k, C_FUTBOL)) else "",
               "Bizim Pazar standı" if var(k, C_PAZAR) else "",
               "Çocuk atölyesi kaydı" if var(k, C_COCUK_AD) else "",
               "Yetişkin atölye: " + s(k["r"][C_YETISKIN_ATOLYE]) if var(k, C_YETISKIN_ATOLYE) else "",
               "Bizim Star" if var(k, C_STAR) else "",
           ])) or "Yalnızca ekip gönüllülüğü")

F += bolum("2. GÖNÜLLÜ SANATÇI KOMİSYONU", "sanatci", sanatci,
           "Eser / Portfolyo Bağlantısı",
           lambda k: linkle(k["r"][C_SANATCI_LINK]))

F += bolum("3. ATÖLYE / WORKSHOP KOMİSYONU  –  Gönüllü Eğitmenler", "workshop", workshop,
           "Atölye Fikri / İçerik",
           lambda k: kisalt(k, k["r"][C_ATOLYE_FIKRI], "Atölye fikri / içerik")
           or "<i>Detay belirtilmemiş</i>")

F += bolum("4. BİZİM PAZAR KOMİSYONU  –  Stand Başvuruları", "pazar", pazar,
           "Stand Türü",
           lambda k: "<b>%s</b>" % html.escape(s(k["r"][C_STAND_TUR]))
           if var(k, C_STAND_TUR) else "<i>Stand türü belirtilmemiş</i>",
           ek_genislik=140)

F += bolum("4b. BİZİM PAZAR — Stand türü seçmiş, başvuru kutusunu işaretlememiş kayıtlar",
           "pazar", pazar_ek, "Stand Türü / Doğrulama Notu",
           lambda k: "<b>%s</b> — <i>teyit edilmeli</i>" % html.escape(s(k["r"][C_STAND_TUR])),
           ek_genislik=180,
           aciklama="Bu kişiler formda stand türünü seçmiş ancak “Bizim Pazar için stand başvurusu yapmak istiyorum” "
                    "kutusunu işaretlememiştir. Komisyonun telefonla teyit etmesi önerilir.")

def cocuk_detay(k):
    r = k["r"]
    p = []
    if var(k, C_COCUK_ATOLYE):
        p.append("<b>Atölye:</b> " + html.escape(s(r[C_COCUK_ATOLYE])))
    else:
        p.append("<b>Atölye:</b> <i>seçilmemiş</i>")
    if var(k, C_COCUK_AD):
        p.append("<b>Çocuk:</b> " + html.escape(s(r[C_COCUK_AD])))
    if var(k, C_COCUK_YAS):
        p.append("<b>Yaş:</b> " + html.escape(s(r[C_COCUK_YAS])))
    p.append("<b>Veli onayı:</b> " + ("✓ var" if var(k, C_VELI) else "✗ YOK"))
    return " &nbsp;|&nbsp; ".join(p)


F += bolum("5. ÇOCUK ATÖLYELERİ KOMİSYONU  –  Ön Kayıtlar", "cocuk", cocuk,
           "Çocuk Bilgileri / Atölye", cocuk_detay)

F += bolum("6. YETİŞKİN ATÖLYELERİ KOMİSYONU  –  Katılımcılar", "yetiskin", yetiskin,
           "Seçilen Atölye",
           lambda k: "<b>%s</b>" % html.escape(s(k["r"][C_YETISKIN_ATOLYE])),
           ek_genislik=140)

F += bolum("7. SPOR KOMİSYONU  –  Voleybol Turnuvası", "spor", voleybol,
           "Diğer Spor Başvuruları",
           lambda k: " • ".join(filter(None, [
               "Basketbol" if (var(k, C_BASKET) or var(k, C_FUTBOL)) else "",
           ])) or "Yalnızca voleybol", ek_genislik=170)

F += bolum("8. SPOR KOMİSYONU  –  Basketbol / Futbol Turnuvası (3'er kişilik takım)",
           "spor", basketbol, "Başvurunun Geldiği Form Alanı",
           lambda k: " • ".join(filter(None, [
               "Basketbol Turnuvası alanı" if var(k, C_BASKET) else "",
               "“Futbol Turnuvası” alanı (metin basketbol olarak gelmiştir)" if var(k, C_FUTBOL) else "",
           ])),
           aciklama="Formdaki “Futbol Turnuvası Başvurusu” sütunundaki seçenek metni basketbol turnuvasını "
                    "tarif etmektedir. Bu nedenle iki sütun tek listede birleştirilmiş, kaynak alan ayrıca belirtilmiştir.")

def star_detay(k):
    r = k["r"]
    p = []
    if var(k, C_STAR_LINK):
        p.append("<b>Referans:</b> " + linkle(r[C_STAR_LINK]))
    if var(k, C_DEMO):
        p.append("<b>Demo dosyası:</b> " + linkle(r[C_DEMO]))
    return " <br/> ".join(p) or "<i>Demo / bağlantı paylaşılmamış — talep edilmeli</i>"


F += bolum("9. BİZİM STAR SES YARIŞMASI KOMİSYONU", "star", star,
           "Demo / Referans Bağlantıları", star_detay)

F += bolum("10. SPONSORLUK KOMİSYONU", "sponsor", sponsor,
           "Sponsorluk Şekli / Notlar",
           lambda k: "<b>%s</b>%s" % (
               html.escape(s(k["r"][C_SPONSOR_SEKIL])) or "Belirtilmemiş",
               " &nbsp;|&nbsp; Ayrıca Bizim Pazar stand başvurusu var" if var(k, C_PAZAR) else ""))

F += bolum("11. KATEGORİ SEÇMEMİŞ / TAKİP EDİLECEK BAŞVURULAR", "diger", kategorisiz,
           "Yapılacak İşlem",
           lambda k: "Hangi kategoriye başvurduğu telefonla teyit edilecek",
           ek_genislik=210,
           aciklama="Bu kişiler formu doldurmuş ancak hiçbir kategori kutusunu işaretlememiştir. "
                    "Düzenleme kurulunun geri dönüş yapması önerilir.")

# --- mukerrer kayitlar
F.append(PageBreak())
bant = Table([[Paragraph("EK-1: MÜKERRER / EŞLEŞEN KAYIT UYARILARI  (%d grup)" % len(mukerrer), st_h2)]],
             colWidths=[TOPLAM_GENISLIK])
bant.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#8a4b00")),
                          ("LEFTPADDING", (0, 0), (-1, -1), 8),
                          ("TOPPADDING", (0, 0), (-1, -1), 6),
                          ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
F.append(bant)
F.append(Spacer(1, 3))
F.append(Paragraph("Aynı telefon numarası veya e-posta adresiyle birden fazla kayıt girilmiştir. "
                   "Bazıları gerçek mükerrer kayıt, bazıları ise aynı hane içinden farklı kişilerin "
                   "başvurusu olabilir; komisyonların teyit etmesi gerekir.", st_alt))
F.append(Spacer(1, 6))
mv = [[Paragraph(b, st_th) for b in
       ["#", "Eşleşen Bilgi", "Kayıtlar (satır — ad soyad)", "İletişim", "E-posta"]]]
for i, (anahtar, grup) in enumerate(mukerrer, 1):
    ad_liste = "<br/>".join("satır %d — %s" % (g["satir"], html.escape(s(g["r"][C_AD])))
                            for g in grup)
    mv.append([
        Paragraph(str(i), st_tdc),
        Paragraph("telefon" if anahtar.isdigit() else "e-posta", st_tdc),
        Paragraph(ad_liste, st_td),
        Paragraph(tel_goster(grup[0]["r"][C_TEL]), st_td),
        Paragraph(mail_goster(grup[0]["r"][C_MAIL]), st_td),
    ])
tm = Table(mv, colWidths=[22, 70, 300, 100, 180], repeatRows=1)
tm.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#8a4b00")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c8d0d8")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fdf6ec")]),
    ("TOPPADDING", (0, 0), (-1, -1), 3.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
]))
F.append(tm)

# --- EK-2: uzun serbest metinler
if UZUN_METINLER:
    F.append(PageBreak())
    bant2 = Table([[Paragraph("EK-2: BAŞVURU SAHİPLERİNİN UZUN AÇIKLAMA METİNLERİ (%d kayıt)"
                              % len(UZUN_METINLER), st_h2)]], colWidths=[TOPLAM_GENISLIK])
    bant2.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#00695c")),
                               ("LEFTPADDING", (0, 0), (-1, -1), 8),
                               ("TOPPADDING", (0, 0), (-1, -1), 6),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    F.append(bant2)
    F.append(Spacer(1, 3))
    F.append(Paragraph("İlgili bölümlerdeki tablolarda yer darlığı nedeniyle kısaltılan "
                       "açıklamaların tam metinleri aşağıdadır.", st_alt))
    F.append(Spacer(1, 8))
    for i, (ad, etiket, metin) in enumerate(UZUN_METINLER, 1):
        F.append(Paragraph("<b>Kayıt %d — %s</b> &nbsp;|&nbsp; <i>%s</i>"
                           % (i, html.escape(ad), html.escape(etiket)),
                           ParagraphStyle("ek2b", parent=st_p, fontSize=10,
                                          textColor=colors.HexColor("#00695c"))))
        F.append(Spacer(1, 3))
        F.append(Paragraph(linkle(metin), st_small))
        F.append(Spacer(1, 12))

doc.build(F)
print("PDF üretildi:", OUT)
for ad, lst, _ in ozet_satirlar:
    print("  %-42s %3d" % (ad, len(lst)))
print("  %-42s %3d" % ("Bizim Pazar (kutusuz, teyit edilecek)", len(pazar_ek)))
print("  %-42s %3d" % ("Mükerrer kayıt grubu", len(mukerrer)))
