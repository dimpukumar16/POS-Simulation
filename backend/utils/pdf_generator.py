import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors


class PDFGenerator:
    """Utility class for generating PDF receipts and reports"""
    
    # Store configuration
    STORE_INFO = {
        'name': 'POS Simulator Store',
        'address': '123 Commerce Street',
        'city': 'Tech City, TC 12345',
        'phone': '+1 (555) 123-4567',
        'email': 'support@possimulator.com',
        'tax_id': 'TAX-123456789'
    }
    
    @staticmethod
    def generate_receipt(transaction, output_dir='receipts'):
        """
        Generate a PDF receipt for a transaction
        
        Args:
            transaction: Transaction object
            output_dir: Directory to save the receipt
        
        Returns:
            str: Path to the generated PDF file
        """
        # Create receipts directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        filename = f"receipt_{transaction.transaction_number}.pdf"
        filepath = os.path.join(output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        header_style = ParagraphStyle(
            'Header',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        # Store header
        elements.append(Paragraph(PDFGenerator.STORE_INFO['name'], title_style))
        elements.append(Paragraph(PDFGenerator.STORE_INFO['address'], header_style))
        elements.append(Paragraph(f"{PDFGenerator.STORE_INFO['city']}", header_style))
        elements.append(Paragraph(f"Phone: {PDFGenerator.STORE_INFO['phone']}", header_style))
        elements.append(Paragraph(f"Tax ID: {PDFGenerator.STORE_INFO['tax_id']}", header_style))
        
        elements.append(Spacer(1, 0.3 * inch))
        
        # Transaction details
        elements.append(Paragraph("="*60, header_style))
        elements.append(Paragraph(f"<b>Receipt #{transaction.transaction_number}</b>", header_style))
        elements.append(Paragraph("="*60, header_style))
        
        elements.append(Spacer(1, 0.2 * inch))
        
        # Transaction info
        trans_info = [
            f"Date: {transaction.created_at.strftime('%Y-%m-%d %H:%M:%S') if transaction.created_at else 'N/A'}",
            f"Cashier: {transaction.user.full_name if transaction.user else 'N/A'}",
            f"Transaction Type: {transaction.transaction_type.upper()}"
        ]
        
        for info in trans_info:
            elements.append(Paragraph(info, styles['Normal']))
        
        elements.append(Spacer(1, 0.3 * inch))
        
        # Items table
        items_data = [['Item', 'Qty', 'Price', 'Disc.', 'Tax', 'Total']]
        
        for item in transaction.items:
            items_data.append([
                Paragraph(item.product.name if item.product else 'N/A', styles['Normal']),
                str(item.quantity),
                f"${item.unit_price:.2f}",
                f"${item.discount_amount:.2f}",
                f"${item.tax_amount:.2f}",
                f"${item.line_total:.2f}"
            ])
        
        # Create table
        items_table = Table(items_data, colWidths=[3*inch, 0.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.9*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ECF0F1'), colors.white])
        ]))
        
        elements.append(items_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Totals
        totals_data = [
            ['Subtotal:', f"${transaction.subtotal:.2f}"],
            ['Discount:', f"-${transaction.discount_amount:.2f}"],
            ['Tax:', f"${transaction.tax_amount:.2f}"],
            ['<b>TOTAL:</b>', f"<b>${transaction.total_amount:.2f}</b>"]
        ]
        
        if transaction.payment_method:
            totals_data.append(['Payment Method:', transaction.payment_method.upper()])
            totals_data.append(['Amount Paid:', f"${transaction.amount_paid:.2f}"])
            if transaction.change_given > 0:
                totals_data.append(['Change:', f"${transaction.change_given:.2f}"])
        
        totals_table = Table(totals_data, colWidths=[5*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
            ('TOPPADDING', (0, -1), (-1, -1), 10)
        ]))
        
        elements.append(totals_table)
        elements.append(Spacer(1, 0.5 * inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#7F8C8D')
        )
        
        elements.append(Paragraph("="*60, footer_style))
        elements.append(Paragraph("Thank you for your business!", footer_style))
        elements.append(Paragraph("Please keep this receipt for your records", footer_style))
        elements.append(Paragraph(f"For support: {PDFGenerator.STORE_INFO['email']}", footer_style))
        
        # Build PDF
        doc.build(elements)
        
        return filepath
    
    @staticmethod
    def generate_sales_report(transactions, start_date, end_date, output_dir='receipts'):
        """
        Generate a sales report PDF
        
        Args:
            transactions: List of Transaction objects
            start_date: Report start date
            end_date: Report end date
            output_dir: Directory to save the report
        
        Returns:
            str: Path to the generated PDF file
        """
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        elements.append(Paragraph("Sales Report", title_style))
        elements.append(Paragraph(f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}", styles['Normal']))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Summary statistics
        total_sales = sum(t.total_amount for t in transactions if t.transaction_type == 'sale')
        total_refunds = sum(t.total_amount for t in transactions if t.transaction_type == 'refund')
        net_sales = total_sales - total_refunds
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Transactions', str(len(transactions))],
            ['Total Sales', f"${total_sales:.2f}"],
            ['Total Refunds', f"${total_refunds:.2f}"],
            ['Net Sales', f"${net_sales:.2f}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ECF0F1'), colors.white])
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Transaction details
        trans_data = [['Trans #', 'Date', 'Type', 'Cashier', 'Amount']]
        
        for t in transactions[:50]:  # Limit to 50 transactions
            trans_data.append([
                t.transaction_number,
                t.created_at.strftime('%Y-%m-%d %H:%M') if t.created_at else 'N/A',
                t.transaction_type,
                t.user.username if t.user else 'N/A',
                f"${t.total_amount:.2f}"
            ])
        
        trans_table = Table(trans_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 1.2*inch, 1*inch])
        trans_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(Paragraph("<b>Transaction Details</b>", styles['Heading2']))
        elements.append(trans_table)
        
        # Build PDF
        doc.build(elements)
        
        return filepath
