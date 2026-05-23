#!/usr/bin/env python3
"""
VikkAI Doctor — Prescription PDF Generator
Generates a prescription PDF in the style of Indian clinic prescriptions.
Usage: python3 generate_prescription.py --help
"""

import argparse
import json
import sys
from datetime import datetime

def generate_prescription(args):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            HRFlowable
        )
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
    except ImportError:
        print("Installing reportlab...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "reportlab", "--break-system-packages", "-q"])
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            HRFlowable
        )
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

    # Colors matching the sample prescription
    PINK = colors.HexColor('#E91E8C')
    BLACK = colors.black
    LIGHT_GRAY = colors.HexColor('#F5F5F5')
    BORDER_GRAY = colors.HexColor('#CCCCCC')

    # Page setup
    doc = SimpleDocTemplate(
        args.output,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=10*mm,
        bottomMargin=15*mm
    )

    width, height = A4
    usable_width = width - 30*mm

    # Styles
    def style(name, **kwargs):
        defaults = dict(fontName='Helvetica', fontSize=9, textColor=BLACK, leading=12)
        defaults.update(kwargs)
        return ParagraphStyle(name, **defaults)

    clinic_name_style = style('ClinicName', fontSize=16, fontName='Helvetica-Bold', textColor=PINK, alignment=TA_CENTER, leading=20)
    doctor_name_style = style('DoctorName', fontSize=11, fontName='Helvetica-Bold', textColor=PINK, alignment=TA_CENTER)
    doctor_sub_style = style('DoctorSub', fontSize=9, textColor=PINK, alignment=TA_CENTER, leading=12)
    date_style = style('DateStyle', fontSize=9, alignment=TA_RIGHT)
    patient_label_style = style('PatLabel', fontSize=9, fontName='Helvetica-Bold')
    patient_value_style = style('PatValue', fontSize=9)
    section_header_style = style('SecHeader', fontSize=10, fontName='Helvetica-Bold', leading=14)
    normal_style = style('Normal', fontSize=9, leading=12)
    notes_style = style('Notes', fontSize=9, leading=13)
    footer_pink_style = style('FooterPink', fontSize=8, textColor=PINK, alignment=TA_CENTER, leading=11)
    footer_disclaimer_style = style('FooterDisc', fontSize=7.5, textColor=PINK, alignment=TA_CENTER, leading=10)

    story = []

    # ── Header: Clinic Name + Date side by side ──
    header_data = [
        [
            Paragraph('Claude Verma\'s Clinic', clinic_name_style),
            Paragraph(f'Consultation date: {args.date}', date_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[usable_width * 0.65, usable_width * 0.35])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(header_table)

    # Doctor info centered
    story.append(Paragraph('VikkAI', doctor_name_style))
    story.append(Paragraph('MBBS, MD', doctor_sub_style))
    story.append(Spacer(1, 2*mm))

    # Top horizontal line
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER_GRAY))
    story.append(Spacer(1, 3*mm))

    # ── Patient Info Row ──
    # Name | Age/Gender | ID
    pat_id = f"PAT{datetime.now().strftime('%Y%m%d%H%M')}"
    
    weight_str = ""
    if args.weight and args.weight.lower() not in ('na', 'n/a', 'none', ''):
        weight_str = f" | Weight: {args.weight}"

    patient_info_data = [
        [
            Paragraph(f'<b>Name</b>   {args.patient_name}', normal_style),
            Paragraph(f'<b>Age / Gender</b>   {args.age}, {args.gender}{weight_str}', normal_style),
            Paragraph(f'<b>ID</b>   {pat_id}', normal_style),
        ]
    ]
    patient_table = Table(
        patient_info_data,
        colWidths=[usable_width * 0.3, usable_width * 0.45, usable_width * 0.25]
    )
    patient_table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 2*mm))

    # Temperature row (blank placeholder like the sample)
    temp_data = [
        [
            Paragraph('<b>Temperature</b>', normal_style),
            Paragraph('_____ °F', normal_style),
            Paragraph('<b>Parity Index</b>', normal_style),
            Paragraph('', normal_style),
        ]
    ]
    temp_table = Table(temp_data, colWidths=[usable_width*0.2, usable_width*0.2, usable_width*0.25, usable_width*0.35])
    temp_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(temp_table)
    story.append(Spacer(1, 4*mm))

    # ── Medical History / Diagnosis ──
    story.append(Paragraph('Medical History', section_header_style))
    story.append(Paragraph('<b>Diagnosis</b>', normal_style))
    story.append(Paragraph(args.diagnosis, normal_style))
    story.append(Spacer(1, 4*mm))

    # ── Medicines Table ──
    story.append(Paragraph('Medicines', section_header_style))
    story.append(Spacer(1, 1*mm))

    medicines = json.loads(args.medicines)

    # Table header
    med_header = [
        Paragraph('<b>Name</b>', normal_style),
        Paragraph('<b>Dose</b>', normal_style),
        Paragraph('<b>Timing</b>', normal_style),
        Paragraph('<b>Duration</b>', normal_style),
        Paragraph('<b>Route</b>', normal_style),
        Paragraph('<b>Notes</b>', normal_style),
    ]
    med_rows = [med_header]

    for m in medicines:
        name_text = m.get('name', '')
        generic = m.get('generic', '')
        if generic:
            name_cell = Paragraph(f'{name_text}<br/><i>{generic}</i>', normal_style)
        else:
            name_cell = Paragraph(name_text, normal_style)

        row = [
            name_cell,
            Paragraph(m.get('dose', ''), normal_style),
            Paragraph(m.get('timing', ''), normal_style),
            Paragraph(m.get('duration', ''), normal_style),
            Paragraph(m.get('route', 'Oral'), normal_style),
            Paragraph(m.get('notes', ''), normal_style),
        ]
        med_rows.append(row)

    col_widths = [
        usable_width * 0.28,
        usable_width * 0.10,
        usable_width * 0.22,
        usable_width * 0.12,
        usable_width * 0.10,
        usable_width * 0.18,
    ]

    med_table = Table(med_rows, colWidths=col_widths, repeatRows=1)
    med_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_GRAY),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(med_table)
    story.append(Spacer(1, 4*mm))

    # ── Notes / Advice ──
    if args.notes:
        story.append(Paragraph('Notes', section_header_style))
        note_lines = args.notes.split('|')
        for line in note_lines:
            line = line.strip()
            if line:
                story.append(Paragraph(f'• {line}', notes_style))
        story.append(Spacer(1, 6*mm))

    # ── Doctor signature block (right-aligned) ──
    sig_data = [[
        '',
        Paragraph(
            f'<font color="#E91E8C"><b>VikkAI</b><br/>MBBS, MD<br/>Claude Verma\'s Clinic</font>',
            style('Sig', fontSize=9, textColor=PINK, alignment=TA_RIGHT, leading=13)
        )
    ]]
    sig_table = Table(sig_data, colWidths=[usable_width * 0.6, usable_width * 0.4])
    sig_table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
    ]))
    story.append(sig_table)

    # ── Footer ──
    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=PINK))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        'This is an AI-generated consultation prescription. '
        'For emergencies, please visit your nearest hospital or call 112.',
        footer_disclaimer_style
    ))

    # Build PDF
    doc.build(story)
    print(f"Prescription saved: {args.output}")


def main():
    parser = argparse.ArgumentParser(description='Generate VikkAI prescription PDF')
    parser.add_argument('--patient-name', required=True)
    parser.add_argument('--age', required=True)
    parser.add_argument('--gender', required=True)
    parser.add_argument('--weight', default='NA')
    parser.add_argument('--date', default=datetime.now().strftime('%d-%m-%Y %H:%M'))
    parser.add_argument('--diagnosis', required=True)
    parser.add_argument('--medicines', required=True, help='JSON array of medicine objects')
    parser.add_argument('--notes', default='', help='Advice lines separated by |')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    generate_prescription(args)


if __name__ == '__main__':
    main()
