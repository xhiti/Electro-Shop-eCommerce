from django.http import FileResponse
from django.http import HttpResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageTemplate, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus.flowables import Image, Spacer
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
from datetime import date
import os
from io import StringIO


class InvoicePrinter:

    @staticmethod
    def printInvoice(order_details, order_details_items, sub_total):
        file_name = 'Invoice ' + str(order_details.order_number) + '.pdf'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        elements = []

        doc = BaseDocTemplate(filename=response, pagesize=A4, title='Invoice')

        # ============================= #
        #           STYLES              #
        # ============================= #
        styles = getSampleStyleSheet()

        left_light = ParagraphStyle(
            'table_head',
            fontName='Times-Roman',
            fontSize=10,
            parent=styles['BodyText'],
            alignment=0,
        )

        center_light = ParagraphStyle(
            'table_head',
            fontName='Times-Roman',
            fontSize=10,
            parent=styles['BodyText'],
            alignment=1,
        )

        right_light = ParagraphStyle(
            'table_head',
            fontName='Times-Roman',
            fontSize=10,
            parent=styles['BodyText'],
            alignment=2,
        )

        total = ParagraphStyle(
            'table_head',
            color=colors.darkred,
            fontName='Times-Roman',
            fontSize=12,
            parent=styles['BodyText'],
            alignment=2,
        )

        table_head = ParagraphStyle(
            'table_head',
            fontName='Times-Roman',
            fontSize=10,
            parent=styles['BodyText'],
            alignment=1,
        )

        order_details_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), '#e5f0ff'),
            ('GRID', (0, 0), (-1, -1), .25, '#e5f0ff'),
            ('FONT', (0, 0), (-1, -1), 'Times-Roman', 12,),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'CENTER')
        ])

        order_items_table_style = TableStyle([
            ('BACKGROUND', (0, 0), (7, 0), '#e5f0ff'),
            ('GRID', (0, 0), (-1, -1), .25, '#e5f0ff'),
            ('FONT', (0, 0), (-1, -1), 'Times-Roman', 10,),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'CENTER')
        ])

        statistics_table_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), .25, '#e5f0ff'),
            ('FONT', (0, 0), (-1, -1), 'Times-Roman', 10,),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'CENTER')
        ])

        # ============================= #
        #          CONSTANTS            #
        # ============================= #
        # Spaces
        DEAFULT_SPACE_WIDTH = 0.1 * inch
        DEAFULT_SPACE_HEIGHT = 0.1 * inch
        SPACE_WIDTH_FOOTER = 0.5 * inch
        SPACE_HEIGHT_FOOTER = 0.5 * inch

        # ELEMENTS POSITIONS
        # Frame position
        FRAME_X = doc.leftMargin / 2
        FRAME_Y = doc.bottomMargin / 2
        FRAME_WIDTH = doc.width + doc.leftMargin
        FRAME_HEIGHT = doc.height + doc.bottomMargin - 20

        # Header line position
        HEADER_LINE_X1 = doc.leftMargin / 2
        HEADER_LINE_Y1 = doc.height + doc.topMargin + 25
        HEADER_LINE_X2 = doc.width + 1.5 * doc.leftMargin
        HEADER_LINE_Y2 = HEADER_LINE_Y1

        # Footer line position
        FOOTER_LINE_X1 = HEADER_LINE_X1
        FOOTER_LINE_Y1 = doc.bottomMargin / 2 + 5
        FOOTER_LINE_X2 = HEADER_LINE_X2
        FOOTER_LINE_Y2 = FOOTER_LINE_Y1

        # Serial Number position
        SERIAL_NUMBER_X = HEADER_LINE_X1 + doc.width + doc.rightMargin
        SERIAL_NUMBER_Y = HEADER_LINE_Y1 + 5

        # Institution position
        INSTITUTION_X = HEADER_LINE_X1
        INSTITUTION_Y = HEADER_LINE_Y1 + 5

        # Page Number position
        PAGE_NUMBER_X = FOOTER_LINE_X1 + doc.width + doc.rightMargin
        PAGE_NUMBER_Y = FOOTER_LINE_Y1 - 10

        # Printed Date position
        PRINTED_DATE_X = FOOTER_LINE_X1
        PRINTED_DATE_Y = FOOTER_LINE_Y1 - 10

        # PDF Header (same for all pages)
        def header(canvas, doc):
            canvas.line(HEADER_LINE_X1, HEADER_LINE_Y1, HEADER_LINE_X2, HEADER_LINE_Y2)
            canvas.setFont('Times-Roman', 9)
            text_serial = "Order number: " + order_details.order_number
            canvas.drawRightString(SERIAL_NUMBER_X, SERIAL_NUMBER_Y, text_serial)
            canvas.drawString(INSTITUTION_X, INSTITUTION_Y, "ElectroShop")

        # PDF Footer (same for all pages)
        def footer(canvas, doc):
            canvas.line(FOOTER_LINE_X1, FOOTER_LINE_Y1, FOOTER_LINE_X2, FOOTER_LINE_Y2)
            canvas.setFont('Times-Roman', 9)
            current_date = datetime.now()
            day = str(current_date.day)
            month = str(current_date.month)
            year = str(current_date.year)
            text_printed_date = "Created at: " + str(day + "/" + month + "/" + year)
            canvas.drawString(PRINTED_DATE_X, PRINTED_DATE_Y, text_printed_date)
            text_page_number = "Page: " + str(doc.page)
            canvas.drawRightString(PAGE_NUMBER_X, PAGE_NUMBER_Y, text_page_number)

        # FRAME
        full_page_frame = Frame(
            FRAME_X,
            FRAME_Y,
            FRAME_WIDTH,
            FRAME_HEIGHT,
            id='normal',
            showBoundary=0
        )

        # TABLE DATAS
        if order_details.payment.payment_id is not None:
            order_details_data = [
                [
                    Paragraph("<b>Full Name:</b> " + str(order_details.first_name) + " " + str(order_details.last_name), left_light),
                    Paragraph("<b>Invoice #" + str(order_details.order_number) + "</b>", right_light)
                ],
                [
                    Paragraph("<b>Full Address:</b> " + str(order_details.address_line_1) + ", " + str(order_details.address_line_1), left_light),
                    Paragraph(str(order_details.created_at), right_light)
                ],
                [
                    Paragraph("<b>" + str(order_details.city) + "</b>", left_light),
                    Paragraph("<b>Payment:</b> " + str(order_details.payment.payment_id), right_light)
                ]
            ]
        else:
            order_details_data = [
                [
                    Paragraph("<b>Full Name:</b> " + str(order_details.first_name) + " " + str(order_details.last_name),
                              left_light),
                    Paragraph("<b>Invoice #" + str(order_details.order_number) + "</b>", right_light)
                ],
                [
                    Paragraph("<b>Full Address:</b> " + str(order_details.address_line_1) + ", " + str(
                        order_details.address_line_1), left_light),
                    Paragraph(str(order_details.created_at), right_light)
                ],
                [
                    Paragraph("<b>" + str(order_details.city) + "</b>", left_light),
                    Paragraph("<b>Payment:</b> ", right_light)
                ]
            ]

        order_items_data = [
            [
                Paragraph(str("<b>Items</b>"), table_head),
                Paragraph(str("<b>Product ID</b>"), table_head),
                Paragraph(str("<b>Quantity</b>"), table_head),
                Paragraph(str("<b>Amount (Net)</b>"), table_head)
            ]
        ]

        for item in order_details_items:
            order_items_data.append(
                [
                    Paragraph(str(item.product.product_name), left_light),
                    Paragraph(str(item.product.product_description), center_light),
                    Paragraph("x" + str(item.quantity), center_light),
                    Paragraph("$" + str(item.product_price), right_light)
                ]
            )

        statistics_data = [
            [
                Paragraph(str("<b>Subtotal</b>"), right_light),
                Paragraph("<b>$" + str(sub_total) + "</b>", right_light),
            ],
            [
                Paragraph(str("<b>Tax</b>"), right_light),
                Paragraph("<b>$" + str(order_details.tax) + "</b>", right_light),
            ]
        ]

        total = [
            [
                Paragraph(str("<b>Total</b>"), total),
                Paragraph("<b>$" + str(order_details.order_total) + "</b>", total),
            ]
        ]

        # ============================= #
        #          ELEMENTS             #
        # ============================= #
        elements.append(Spacer(DEAFULT_SPACE_WIDTH, DEAFULT_SPACE_HEIGHT))
        elements.append(Spacer(SPACE_WIDTH_FOOTER, SPACE_HEIGHT_FOOTER))
        elements.append(
            Table(
                order_details_data,
                style=order_details_table_style,
                colWidths=[3.6 * inch, 3.6 * inch],
            )
        )
        elements.append(Spacer(DEAFULT_SPACE_WIDTH, DEAFULT_SPACE_HEIGHT))
        elements.append(Spacer(SPACE_WIDTH_FOOTER, SPACE_HEIGHT_FOOTER))
        elements.append(
            Table(
                order_items_data,
                repeatRows=1,
                style=order_items_table_style,
                colWidths=[3 * inch, 1.5 * inch, 1.5 * inch, 1.2 * inch],
            )
        )
        elements.append(
            Table(
                statistics_data,
                style=statistics_table_style,
                colWidths=[6 * inch, 1.2 * inch],
            )
        )
        elements.append(
            Table(
                total,
                style=statistics_table_style,
                colWidths=[6 * inch, 1.2 * inch],
            )
        )
        elements.append(Spacer(SPACE_WIDTH_FOOTER, SPACE_HEIGHT_FOOTER))
        doc.addPageTemplates([
            PageTemplate(id='InvoiceReport', frames=full_page_frame, onPage=header, onPageEnd=footer)
        ])
        doc.build(elements)
        # os.system(pdf_name)
        # os.startfile(pdf_name)
        return response
