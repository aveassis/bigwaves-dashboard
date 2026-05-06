# BigWaves PDF Rapport Generator
# Gebruikt fpdf2 met Unicode font voor emoji/UTF-8 support
from fpdf import FPDF
import json
import os
from datetime import datetime
from pathlib import Path
FONT_DIR = Path(__file__).parent / "fonts"
SYSTEM_FONTS = Path("/usr/share/fonts/truetype/dejavu")


class BigWavesPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self._register_fonts()

    def _register_fonts(self):
        """Registreer DejaVu Sans voor unicode support."""
        if not (FONT_DIR / "DejaVuSans.ttf").exists():
            _ensure_fonts()
        self.add_font("DejaVu", "", str(FONT_DIR / "DejaVuSans.ttf"), uni=True)
        self.add_font("DejaVu", "B", str(FONT_DIR / "DejaVuSans-Bold.ttf"), uni=True)

    def _font(self, style="", size=10):
        return ("DejaVu", style, size)

    def header(self):
        self.set_font(*self._font("B", 10))
        self.set_text_color(10, 77, 164)
        self.cell(0, 8, "BigWaves Performance Dashboard", align="L")
        self.cell(0, 8, datetime.now().strftime("%d-%m-%Y"), align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 180, 216)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font(*self._font("", 8))
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}  |  BigWaves  |  datagedreven, menselijk gecheckt", align="C")

    def section_title(self, title):
        self.set_font(*self._font("B", 13))
        self.set_text_color(10, 77, 164)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 180, 216)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def kpi_table(self, kpis):
        self.set_font(*self._font("B", 9))
        self.set_fill_color(10, 77, 164)
        self.set_text_color(255, 255, 255)
        self.cell(55, 8, "KPI", border=1, align="C", fill=True)
        self.cell(30, 8, "Waarde", border=1, align="C", fill=True)
        self.cell(30, 8, "Doel", border=1, align="C", fill=True)
        self.cell(20, 8, "Status", border=1, align="C", fill=True)
        self.cell(55, 8, "Trend", border=1, align="C", fill=True, new_x="LMARGIN", new_y="NEXT")

        self.set_text_color(30, 30, 30)
        self.set_font(*self._font("", 9))
        for kpi, info in kpis.items():
            status = info.get("status", "groen")
            waarde = info["waarde"]
            eenheid = info.get("eenheid", "")

            if eenheid == "euro":
                disp_waarde = f"EUR {waarde:,}" if isinstance(waarde, int) else f"EUR {waarde}"
            elif eenheid == "seconden":
                disp_waarde = f"{waarde}s"
            elif eenheid == "%":
                disp_waarde = f"{waarde}%"
            else:
                disp_waarde = str(waarde)

            doel = info["doel"]
            if eenheid == "seconden":
                disp_doel = f"{doel}s"
            elif eenheid == "euro":
                disp_doel = f"EUR {doel:,}" if isinstance(doel, int) else f"EUR {doel}"
            elif eenheid == "%":
                disp_doel = f">{doel}%" if kpi in ("Nauwkeurigheid", "Uptime") else f"<{doel}%"
            else:
                disp_doel = str(doel)

            status_sym = {"groen": "GOED", "oranje": "MATIG", "rood": "KRITISCH"}.get(status, "-")
            trend = info.get("trend", "")

            self.cell(55, 7, kpi, border=1)
            self.cell(30, 7, disp_waarde, border=1, align="C")
            self.cell(30, 7, disp_doel, border=1, align="C")
            self.cell(20, 7, status_sym, border=1, align="C")
            self.cell(55, 7, trend, border=1, align="C", new_x="LMARGIN", new_y="NEXT")

    def hitl_section(self, hitl, kpis):
        hitl_ratio = kpis.get("HITL-ratio", {}).get("waarde", "-")
        self.section_title("Human In The Loop (HITL)")

        self.set_font(*self._font("", 10))
        self.cell(0, 6, f"Totaal acties: {hitl.get('totaal_acties', 0):,}", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 6, f"Menselijke check: {hitl.get('menselijke_check', 0):,}  ({hitl_ratio}%)", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 6, f"Geautomatiseerd: {hitl.get('geautomatiseerd', 0):,}", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 6, f"Bespaarde uren: {hitl.get('bespaarde_uren', 0)}u", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

        cat = hitl.get("categorieen", {})
        if cat:
            self.set_font(*self._font("B", 9))
            self.set_fill_color(10, 77, 164)
            self.set_text_color(255, 255, 255)
            self.cell(50, 8, "Categorie", border=1, align="C", fill=True)
            self.cell(25, 8, "Totaal", border=1, align="C", fill=True)
            self.cell(25, 8, "HITL", border=1, align="C", fill=True)
            self.cell(25, 8, "Auto", border=1, align="C", fill=True)
            self.cell(25, 8, "HITL %", border=1, align="C", fill=True)
            self.cell(40, 8, "Advies", border=1, align="C", fill=True, new_x="LMARGIN", new_y="NEXT")

            self.set_text_color(30, 30, 30)
            self.set_font(*self._font("", 9))
            for c, info in cat.items():
                pct = info["percentage"]
                advies = "Goed" if pct <= 20 else "Optimaliseer" if pct <= 30 else "Actie nodig"
                self.cell(50, 7, c, border=1)
                self.cell(25, 7, str(info["totaal"]), border=1, align="C")
                self.cell(25, 7, str(info["hitl"]), border=1, align="C")
                self.cell(25, 7, str(info["totaal"] - info["hitl"]), border=1, align="C")
                self.cell(25, 7, f"{pct}%", border=1, align="C")
                self.cell(40, 7, advies, border=1, align="C", new_x="LMARGIN", new_y="NEXT")

    def bottleneck_section(self, bottleneck):
        if bottleneck and bottleneck.get("tekst"):
            self.section_title("Bottleneck-analyse")
            self.set_font(*self._font("", 10))
            prio = bottleneck.get("prioriteit", "laag").upper()
            self.set_text_color(200, 0, 0) if prio == "HOOG" else self.set_text_color(200, 100, 0)
            self.cell(0, 6, f"Prioriteit: {prio}", new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(30, 30, 30)
            self.multi_cell(0, 6, bottleneck["tekst"])
            self.ln(2)

    def kosten_section(self, kosten_besparing, vorige):
        self.section_title("Kostenbesparing")
        self.set_font(*self._font("", 10))
        self.cell(0, 6, f"Prognose deze maand: EUR {kosten_besparing:,}", new_x="LMARGIN", new_y="NEXT")
        delta = kosten_besparing - vorige
        teken = "+" if delta >= 0 else ""
        self.cell(0, 6, f"Verschil vs. vorige maand: {teken}EUR {delta:,}", new_x="LMARGIN", new_y="NEXT")


def genereer_pdf(data: dict) -> bytes:
    """Genereer een PDF rapport op basis van klantdata. Returnt bytes."""
    # Check if fonts exist, otherwise copy from system
    if not (FONT_DIR / "DejaVuSans.ttf").exists():
        _ensure_fonts()

    pdf = BigWavesPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # ─── Titel ────────────────────────────────────────
    pdf.set_font(*pdf._font("B", 20))
    pdf.set_text_color(10, 77, 164)
    pdf.cell(0, 12, f"BigWaves — {data['naam']}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(*pdf._font("", 11))
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, f"Periode: {data.get('periode', 'Huidige maand')}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Laatste update: {data.get('laatste_update', '-')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # ─── KPI Tabel ────────────────────────────────────
    kpis = data.get("kpis", {})
    if kpis:
        pdf.section_title("Kern-KPI's")
        pdf.kpi_table(kpis)
        pdf.ln(4)

    # ─── Bottleneck ───────────────────────────────────
    pdf.bottleneck_section(data.get("bottleneck", {}))

    # ─── HITL ─────────────────────────────────────────
    hitl = data.get("hitl_detail", None)
    if hitl:
        pdf.hitl_section(hitl, kpis)
        pdf.ln(2)

    # ─── Kosten ───────────────────────────────────────
    if data.get("kosten_besparing"):
        vorige = data.get("doelen_vorige_maand", {}).get("kosten_besparing", 0)
        pdf.kosten_section(data["kosten_besparing"], vorige)

    # ─── Closing ──────────────────────────────────────
    pdf.ln(5)
    pdf.set_font(*pdf._font("", 9))
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "BigWaves -- datagedreven, menselijk gecheckt", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Gegenereerd op: " + datetime.now().strftime("%d-%m-%Y %H:%M"), align="C")

    return pdf.output()


def _ensure_fonts():
    """Kopieer DejaVu Sans fonts van systeem naar lokale fonts/ map."""
    import shutil
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    for font in ["DejaVuSans.ttf", "DejaVuSans-Bold.ttf"]:
        src = SYSTEM_FONTS / font
        dst = FONT_DIR / font
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
            print(f"Copied {font}")

