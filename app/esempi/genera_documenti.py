from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

F = "/usr/share/fonts/truetype/dejavu/"
def f(name, size): return ImageFont.truetype(F + name, size)
R, B, S = "DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "DejaVuSerif.ttf"
INK = (30, 30, 34); GREY = (90, 90, 96); LINE = (180, 180, 186)

def photo_finish(img, angle):
    # leggero effetto "foto col telefono": rotazione, ombra, rumore
    bg = Image.new("RGB", (img.width + 120, img.height + 120), (196, 190, 178))
    bg.paste(img, (60, 60))
    bg = bg.rotate(angle, resample=Image.BICUBIC, fillcolor=(196, 190, 178))
    px = bg.load()
    random.seed(7)
    for _ in range(9000):
        x, y = random.randrange(bg.width), random.randrange(bg.height)
        r, g, b = px[x, y]; d = random.randint(-10, 10)
        px[x, y] = (max(0, min(255, r + d)),) * 1 + (max(0, min(255, g + d)), max(0, min(255, b + d)))
    return bg.filter(ImageFilter.GaussianBlur(0.6))

def fattura():
    W, H = 1100, 1500
    im = Image.new("RGB", (W, H), (252, 252, 250)); d = ImageDraw.Draw(im)
    d.text((70, 70), "Centro Oculistico San Marco s.r.l.", font=f(B, 34), fill=INK)
    for i, t in enumerate(["Via Roma 18 - 40121 Bologna", "P.IVA 01234567890 - Tel. 051 000 1234",
                           "Struttura sanitaria privata autorizzata"]):
        d.text((70, 120 + i * 30), t, font=f(R, 20), fill=GREY)
    d.text((70, 250), "FATTURA N. 2026/1847", font=f(B, 30), fill=INK)
    d.text((70, 292), "Data documento: 12/09/2026", font=f(R, 22), fill=INK)
    d.rectangle((620, 240, 1030, 380), outline=LINE, width=2)
    d.text((640, 252), "Intestata a", font=f(R, 18), fill=GREY)
    d.text((640, 280), "Roberto Ferri", font=f(B, 24), fill=INK)
    d.text((640, 314), "Via dei Mille 7, 40129 Bologna", font=f(R, 18), fill=INK)
    d.text((640, 340), "C.F. FRRRRT63A12A944K", font=f(R, 18), fill=INK)
    y = 450
    d.line((70, y, 1030, y), fill=INK, width=2)
    d.text((80, y + 12), "Descrizione", font=f(B, 20), fill=INK)
    d.text((780, y + 12), "Qtà", font=f(B, 20), fill=INK)
    d.text((900, y + 12), "Importo", font=f(B, 20), fill=INK)
    d.line((70, y + 48, 1030, y + 48), fill=LINE, width=1)
    d.text((80, y + 70), "Visita oculistica specialistica con", font=f(R, 22), fill=INK)
    d.text((80, y + 100), "esame del fondo oculare", font=f(R, 22), fill=INK)
    d.text((80, y + 132), "Medico: Dott.ssa Laura Bettini", font=f(R, 18), fill=GREY)
    d.text((795, y + 70), "1", font=f(R, 22), fill=INK)
    d.text((880, y + 70), "€ 120,00", font=f(R, 22), fill=INK)
    d.text((80, y + 190), "Imposta di bollo assolta in modo virtuale", font=f(R, 20), fill=INK)
    d.text((895, y + 190), "€ 2,00", font=f(R, 22), fill=INK)
    d.line((70, y + 250, 1030, y + 250), fill=LINE, width=1)
    d.text((80, y + 275), "Imponibile esente IVA", font=f(R, 20), fill=GREY)
    d.text((880, y + 275), "€ 120,00", font=f(R, 20), fill=GREY)
    d.text((80, y + 310), "IVA: operazione esente art. 10 n. 18 DPR 633/72", font=f(R, 18), fill=GREY)
    d.rectangle((560, y + 360, 1030, y + 430), outline=INK, width=2)
    d.text((580, y + 378), "TOTALE DOCUMENTO", font=f(B, 22), fill=INK)
    d.text((870, y + 376), "€ 122,00", font=f(B, 26), fill=INK)
    d.text((80, y + 480), "Pagamento: carta di debito - QUIETANZATA il 12/09/2026", font=f(R, 20), fill=INK)
    d.text((80, y + 515), "Documento valido ai fini della detrazione fiscale.", font=f(R, 18), fill=GREY)
    d.text((80, y + 545), "Conservare l'originale.", font=f(R, 18), fill=GREY)
    # timbro "pagato"
    st = Image.new("RGBA", (300, 110), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.rounded_rectangle((4, 4, 296, 106), 14, outline=(170, 40, 50, 210), width=5)
    sd.text((48, 26), "PAGATO", font=f(B, 46), fill=(170, 40, 50, 210))
    st = st.rotate(14, expand=True)
    im.paste(st, (140, 1120), st)
    d.text((70, 1420), "Pagina 1 di 1", font=f(R, 16), fill=GREY)
    return photo_finish(im, -2.2)

def prescrizione():
    W, H = 1100, 1250
    im = Image.new("RGB", (W, H), (250, 251, 255)); d = ImageDraw.Draw(im)
    d.text((70, 70), "Dott. Mario Gentile", font=f(B, 34), fill=INK)
    d.text((70, 118), "Medico di Medicina Generale", font=f(R, 22), fill=GREY)
    d.text((70, 150), "Ambulatorio: Via Libia 42, Bologna - Tel. 051 000 9876", font=f(R, 20), fill=GREY)
    d.line((70, 200, 1030, 200), fill=INK, width=2)
    d.text((70, 240), "Bologna, 28/08/2026", font=f(R, 24), fill=INK)
    d.text((70, 310), "Sig. Roberto Ferri", font=f(B, 26), fill=INK)
    d.text((70, 350), "nato il 12/01/1963", font=f(R, 22), fill=INK)
    d.text((70, 440), "Si prescrive:", font=f(B, 26), fill=INK)
    d.text((110, 495), "visita oculistica specialistica", font=f(S, 30), fill=(20, 40, 110))
    d.text((110, 545), "con esame del fondo oculare", font=f(S, 30), fill=(20, 40, 110))
    d.text((70, 640), "Quesito diagnostico:", font=f(B, 22), fill=INK)
    d.text((70, 680), "controllo periodico in paziente con retinopatia diabetica", font=f(R, 22), fill=INK)
    d.text((70, 770), "Ricetta bianca - prestazione in regime privato", font=f(R, 20), fill=GREY)
    d.text((640, 960), "Timbro e firma", font=f(R, 18), fill=GREY)
    d.ellipse((650, 990, 860, 1120), outline=(40, 70, 160), width=4)
    d.text((690, 1035), "Dr. M. GENTILE", font=f(B, 18), fill=(40, 70, 160))
    d.line((860, 1080, 1010, 1020), fill=(20, 40, 110), width=3)
    d.line((880, 1060, 990, 1075), fill=(20, 40, 110), width=2)
    return photo_finish(im, 1.6)

for name, fn in (("fattura_esempio", fattura), ("prescrizione_esempio", prescrizione)):
    img = fn().convert("RGB")
    img.thumbnail((1000, 1400))
    img.save(f"{name}.jpg", quality=72)
    print(name, img.size)
