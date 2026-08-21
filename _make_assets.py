"""Generate OG card, project stills, and updated resume.pdf."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.colors import HexColor, white, black

ROOT = Path(r"D:\portfolio")
ASSETS = ROOT / "assets"
PROJ = ASSETS / "projects"
ASSETS.mkdir(exist_ok=True)
PROJ.mkdir(exist_ok=True)

def font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def rounded(draw, box, r, fill):
    draw.rounded_rectangle(box, radius=r, fill=fill)

# --- OG 1200x630 ---
og = Image.new("RGB", (1200, 630), "#0a0a0a")
d = ImageDraw.Draw(og)
# faint rings
for rx, ry, w in ((520, 220, 2), (400, 280, 1), (580, 160, 1)):
    d.ellipse([600 - rx, 315 - ry, 600 + rx, 315 + ry], outline="#2a2a2a", width=w)
d.rounded_rectangle([80, 80, 1120, 550], radius=28, outline="#333333", width=2)
# JR mark
d.rounded_rectangle([140, 220, 280, 360], radius=28, fill="#ffffff")
d.text((210, 290), "JR", font=font(52, True), fill="#0a0a0a", anchor="mm")
d.text((320, 250), "JAIMIN RANA", font=font(48, True), fill="#ffffff", anchor="lm")
d.text((320, 318), "QA Engineer  ·  Python Developer", font=font(24), fill="#a3a3a3", anchor="lm")
d.text((320, 370), "optimusbot.dev", font=font(22), fill="#737373", anchor="lm")
d.line([(320, 400), (980, 400)], fill="#262626", width=1)
d.text((320, 440), "Product QA  ·  Security  ·  Flask", font=font(18), fill="#737373", anchor="lm")
og.save(ASSETS / "og.png", "PNG", optimize=True)

def ui_chrome(draw, w, h, title):
    d = draw
    d.rectangle([0, 0, w, h], fill="#111111")
    d.rounded_rectangle([24, 24, w - 24, h - 24], radius=18, fill="#0a0a0a", outline="#2a2a2a", width=2)
    d.rounded_rectangle([24, 24, w - 24, 78], radius=18, fill="#141414")
    d.rectangle([24, 60, w - 24, 78], fill="#141414")
    for i, c in enumerate(("#3a3a3a", "#2e2e2e", "#262626")):
        d.ellipse([44 + i * 18, 42, 54 + i * 18, 52], fill=c)
    d.text((120, 51), title, font=font(16, True), fill="#e5e5e5", anchor="lm")

# CyberSuite still
cs = Image.new("RGB", (960, 540), "#111111")
d = ImageDraw.Draw(cs)
ui_chrome(d, 960, 540, "cybersuite.in  ·  security suite")
# sidebar
d.rounded_rectangle([44, 96, 250, 500], radius=12, fill="#121212", outline="#262626")
tools = ["Dashboard", "CryptoGuard", "Hash Lab", "File Locker", "Secure Paste"]
for i, t in enumerate(tools):
    y = 120 + i * 48
    if i == 0:
        d.rounded_rectangle([56, y - 10, 238, y + 26], radius=8, fill="#1f1f1f")
    d.text((72, y + 8), t, font=font(15, i == 0), fill="#fafafa" if i == 0 else "#8a8a8a", anchor="lm")
# main tiles
tiles = [("AES", "Encrypt"), ("HMAC", "Sign"), ("OTP", "Generate"), ("Scan", "Headers")]
for i, (a, b) in enumerate(tiles):
    x = 274 + (i % 2) * 320
    y = 108 + (i // 2) * 190
    d.rounded_rectangle([x, y, x + 300, y + 170], radius=14, fill="#141414", outline="#2a2a2a")
    d.rounded_rectangle([x + 18, y + 22, x + 62, y + 66], radius=10, fill="#ffffff")
    d.text((x + 40, y + 44), a[0], font=font(16, True), fill="#111111", anchor="mm")
    d.text((x + 78, y + 38), a, font=font(18, True), fill="#ffffff", anchor="lm")
    d.text((x + 78, y + 64), b, font=font(14), fill="#888888", anchor="lm")
    d.rounded_rectangle([x + 18, y + 118, x + 282, y + 148], radius=8, fill="#1c1c1c")
    d.text((x + 150, y + 133), "Ready", font=font(13), fill="#a3a3a3", anchor="mm")
cs.save(PROJ / "cybersuite.png", "PNG", optimize=True)

# SubGuard still
sg = Image.new("RGB", (960, 540), "#111111")
d = ImageDraw.Draw(sg)
ui_chrome(d, 960, 540, "subguard  ·  local-first subscriptions")
# stats
stats = [("12", "Active"), ("$86", "This month"), ("3", "Due soon")]
for i, (n, lab) in enumerate(stats):
    x = 48 + i * 300
    d.rounded_rectangle([x, 100, x + 280, 200], radius=14, fill="#141414", outline="#2a2a2a")
    d.text((x + 24, 132), n, font=font(28, True), fill="#ffffff", anchor="lm")
    d.text((x + 24, 172), lab, font=font(14), fill="#888888", anchor="lm")
# list
rows = [("Netflix", "$15.49", "8 days"), ("iCloud+", "$2.99", "12 days"), ("Figma", "$12.00", "21 days")]
d.rounded_rectangle([48, 220, 912, 500], radius=14, fill="#121212", outline="#2a2a2a")
for i, (name, price, due) in enumerate(rows):
    y = 250 + i * 78
    d.text((72, y), name, font=font(18, True), fill="#f5f5f5", anchor="lm")
    d.text((72, y + 26), due, font=font(13), fill="#737373", anchor="lm")
    d.text((860, y + 8), price, font=font(18, True), fill="#ffffff", anchor="rm")
    if i < 2:
        d.line([(72, y + 52), (888, y + 52)], fill="#262626", width=1)
sg.save(PROJ / "subguard.png", "PNG", optimize=True)

# Expense Tracker still
ex = Image.new("RGB", (960, 540), "#111111")
d = ImageDraw.Draw(ex)
ui_chrome(d, 960, 540, "expense tracker  ·  budgets & charts")
stats = [("$2,480", "Spent"), ("$720", "Left"), ("6", "Categories")]
for i, (n, lab) in enumerate(stats):
    x = 48 + i * 300
    d.rounded_rectangle([x, 100, x + 280, 196], radius=14, fill="#141414", outline="#2a2a2a")
    d.text((x + 24, 128), n, font=font(26, True), fill="#ffffff", anchor="lm")
    d.text((x + 24, 168), lab, font=font(14), fill="#888888", anchor="lm")
d.rounded_rectangle([48, 216, 560, 500], radius=14, fill="#121212", outline="#2a2a2a")
d.text((72, 246), "This month", font=font(15, True), fill="#f5f5f5", anchor="lm")
bars = [("Groceries", 0.78), ("Rent", 0.92), ("Transport", 0.46), ("Utilities", 0.58)]
for i, (name, pct) in enumerate(bars):
    y = 286 + i * 50
    d.text((72, y), name, font=font(14), fill="#a3a3a3", anchor="lm")
    d.rounded_rectangle([220, y - 6, 532, y + 10], radius=5, fill="#1c1c1c")
    d.rounded_rectangle([220, y - 6, 220 + int(312 * pct), y + 10], radius=5, fill="#e5e5e5")
d.rounded_rectangle([580, 216, 912, 500], radius=14, fill="#121212", outline="#2a2a2a")
tx = [("Market", "-$64.20"), ("Salary", "+$2,400"), ("Fuel", "-$28.00"), ("Power", "-$41.50")]
d.text((604, 246), "Recent", font=font(15, True), fill="#f5f5f5", anchor="lm")
for i, (name, amt) in enumerate(tx):
    y = 292 + i * 48
    d.text((604, y), name, font=font(14), fill="#d4d4d4", anchor="lm")
    d.text((888, y), amt, font=font(14, True), fill="#fafafa", anchor="rm")
    if i < 3:
        d.line([(604, y + 22), (888, y + 22)], fill="#262626", width=1)
ex.save(PROJ / "expense.png", "PNG", optimize=True)

# --- Resume PDF ---
out = ROOT / "resume.pdf"
c = pdfcanvas.Canvas(str(out), pagesize=letter)
W, H = letter
ink = HexColor("#111111")
mute = HexColor("#444444")
rule_color = HexColor("#222222")
left = 0.7 * inch
right = W - 0.7 * inch
y = H - 0.62 * inch

def rule(yy):
    c.setStrokeColor(rule_color)
    c.setLineWidth(0.8)
    c.line(left, yy, right, yy)

def h1(text, yy):
    c.setFillColor(ink)
    c.setFont("Times-Bold", 22)
    c.drawCentredString(W / 2, yy, text)

def section(title, yy):
    c.setFillColor(ink)
    c.setFont("Times-Bold", 11)
    c.drawString(left, yy, title)
    rule(yy - 4)
    return yy - 18

c.setFillColor(ink)
c.setFont("Times-Bold", 22)
c.drawCentredString(W / 2, y, "JAIMIN RANA")
y -= 16
c.setFont("Times-Roman", 10)
c.setFillColor(mute)
c.drawCentredString(W / 2, y, "Surat, India  |  https://optimusbot.dev  |  https://www.cybersuite.in")
y -= 14
c.setFillColor(ink)
c.setFont("Times-Roman", 9.5)
contact = "7600222251   ·   techhunter333@proton.me   ·   linkedin.com/in/jaimin-r-cyber   ·   github.com/techhunter333"
c.drawCentredString(W / 2, y, contact)
y -= 22

y = section("SUMMARY", y)
c.setFont("Times-Roman", 9.6)
c.setFillColor(ink)
summary = (
    "Detail-oriented Quality Assurance Engineer with product QA experience at SpaceXAI on Grok "
    "mobile and web. Strong in functional, regression, compatibility, exploratory, and localization QA, "
    "plus clear defect tracking. Python developer shipping secure Flask products (CyberSuite, SubGuard) "
    "with Google Professional cybersecurity credentials."
)
# simple wrap
from reportlab.pdfbase.pdfmetrics import stringWidth
def draw_wrap(text, yy, leading=13, size=9.6):
    words = text.split()
    line = ""
    c.setFont("Times-Roman", size)
    for w in words:
        trial = (line + " " + w).strip()
        if stringWidth(trial, "Times-Roman", size) > (right - left):
            c.drawString(left, yy, line)
            yy -= leading
            line = w
        else:
            line = trial
    if line:
        c.drawString(left, yy, line)
        yy -= leading
    return yy

y = draw_wrap(summary, y) - 6

y = section("EXPERIENCE", y)
c.setFont("Times-Bold", 10)
c.drawString(left, y, "SpaceXAI")
c.setFont("Times-Italic", 9.5)
c.drawRightString(right, y, "Dec 2025 – Present  |  Remote")
y -= 13
c.setFont("Times-Bold", 10)
c.drawString(left, y, "Product QA")
y -= 13
c.setFont("Times-Roman", 9.5)
y = draw_wrap(
    "QA for the Grok Android application: feature validation across form factors, screen sizes, "
    "and OS versions; exploratory and regression testing; detailed defect tracking.",
    y, 12, 9.5
) - 4
c.setFont("Times-Bold", 10)
c.drawString(left, y, "Multilingual Localization Specialist")
c.setFont("Times-Italic", 9.5)
c.drawRightString(right, y, "Nov 2025 – Present")
y -= 13
c.setFont("Times-Roman", 9.5)
y = draw_wrap(
    "Localizing X/Grok interface strings into Gujarati and checking linguistic accuracy and UI rendering across locales.",
    y, 12, 9.5
) - 8

c.setFont("Times-Bold", 10)
c.drawString(left, y, "Independent practice")
c.setFont("Times-Italic", 9.5)
c.drawRightString(right, y, "Jan 2021 – Apr 2026")
y -= 13
c.setFont("Times-Bold", 10)
c.drawString(left, y, "Python Developer & Security QA Analyst")
y -= 13
c.setFont("Times-Roman", 9.5)
y = draw_wrap(
    "Built and shipped Flask/Django apps with functional testing; OWASP-oriented security QA; "
    "Python security tooling; homelab for Linux hardening.",
    y, 12, 9.5
) - 8

y = section("PROJECTS", y)
for title, body in [
    ("CyberSuite  |  cybersuite.in",
     "Production cybersecurity platform: modular Flask tools for crypto, hashing, secure paste, file locker, OTP."),
    ("SubGuard  |  local-first subscriptions",
     "Renewals, budgets, analytics, import/export, command palette; security-hardened Flask + SQLite."),
    ("Expense Tracker",
     "Personal finance app with budgets, charts, and monochrome dark/light UI."),
]:
    c.setFont("Times-Bold", 10)
    c.drawString(left, y, title)
    y -= 12
    c.setFont("Times-Roman", 9.5)
    y = draw_wrap(body, y, 12, 9.5) - 4

y = section("TECHNICAL SKILLS", y)
c.setFont("Times-Roman", 9.4)
skills = [
    ("QA & Testing:", "Functional · Regression · Mobile (Android) · Localization · Exploratory · Compatibility · Defect tracking · Penetration testing · OWASP Top 10"),
    ("Development:", "Python · Flask · Django · FastAPI · JavaScript · Git / GitHub"),
    ("Security:", "Burp Suite · Wireshark · Nmap · Kali Linux · AES / hashing · Secure coding"),
    ("Data & Ops:", "PostgreSQL · MySQL · SQLite · Linux · Google Cloud IAM"),
]
for lab, rest in skills:
    c.setFont("Times-Bold", 9.4)
    lw = stringWidth(lab + " ", "Times-Bold", 9.4)
    c.drawString(left, y, lab)
    c.setFont("Times-Roman", 9.4)
    # wrap rest after label
    words = rest.split()
    buf = ""
    first = True
    x0 = left + lw
    for w in words:
        trial = (buf + " " + w).strip()
        start = x0 if first else left
        if stringWidth(trial, "Times-Roman", 9.4) > (right - start):
            c.drawString(start, y, buf)
            y -= 12
            buf = w
            first = False
            x0 = left
        else:
            buf = trial
    if buf:
        c.drawString(x0 if first else left, y, buf)
        y -= 14

y -= 2
y = section("EDUCATION", y)
c.setFont("Times-Bold", 10)
c.drawString(left, y, "PP Savani University")
c.setFont("Times-Italic", 9.5)
c.drawRightString(right, y, "2024 – 2026")
y -= 12
c.setFont("Times-Roman", 9.5)
c.drawString(left, y, "Master of Computer Applications (MCA)")
y -= 16
c.setFont("Times-Bold", 10)
c.drawString(left, y, "Veer Narmad South Gujarat University")
c.setFont("Times-Italic", 9.5)
c.drawRightString(right, y, "2021 – 2024")
y -= 12
c.setFont("Times-Roman", 9.5)
c.drawString(left, y, "Bachelor of Computer Applications (BCA)")
y -= 18

y = section("CERTIFICATIONS", y)
certs = [
    "Google Cybersecurity Professional Certificate",
    "Google Cloud Cybersecurity Professional Certificate",
    "Google IT Support Professional Certificate",
    "Gemini Certified Educator · Gemini Certified University Student",
    "Google DeepMind  |  Build Your Own Small Language Model",
    "Forage: Deloitte Cyber · Mastercard Cybersecurity · Tata Cybersecurity Analyst",
]
c.setFont("Times-Roman", 9.5)
for item in certs:
    c.drawString(left, y, "•  " + item)
    y -= 13

c.save()
print("wrote", ASSETS / "og.png", PROJ / "cybersuite.png", PROJ / "subguard.png", PROJ / "expense.png", out)
