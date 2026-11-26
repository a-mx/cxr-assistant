# src/app/services/export.py
from html import escape
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class Export:
    def __init__(self, filetype: str, analysis=None):
        self.filetype = filetype
        self.analysis = analysis

    def export(self):
        if self.filetype == "pdf":
            return self.export_to_pdf()

        raise ValueError("Unknown filetype")

    def export_to_pdf(self):
        if self.analysis is None:
            raise ValueError("Analysis is required")

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=40,
            rightMargin=40,
            topMargin=40,
            bottomMargin=40,
        )

        styles = getSampleStyleSheet()
        title_style = styles["Heading1"]
        title_style.alignment = TA_LEFT

        patient = self.analysis.patient
        patient_name = (
            f"{patient.name} {patient.surname}"
            if patient
            else "Unknown patient"
        )

        report = escape(
            self.analysis.current_report
            or self.analysis.generated_report
            or ""
        ).replace("\n", "<br/>")

        elements = [
            Paragraph("Analysis report", title_style),
            Spacer(1, 16),
        ]

        patient_pesel = patient.pesel if patient else "-"

        details = [
            ["Patient", escape(patient_name)],
            ["PESEL", escape(patient_pesel)],
            [
                "Date",
                escape(
                    self.analysis.created_at.strftime("%Y-%m-%d %H:%M")
                ),
            ],
            ["Analysis ID", str(self.analysis.id)],
        ]

        details_table = Table(details, colWidths=[100, 380])
        details_table.setStyle(
            TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#000000")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#000000")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ])
        )

        elements.extend([
            details_table,
            Spacer(1, 20),
            Paragraph("Radiology report", styles["Heading2"]),
            Spacer(1, 8),
            Paragraph(report, styles["BodyText"]),
        ])

        document.build(elements)

        buffer.seek(0)
        return buffer
