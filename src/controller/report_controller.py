import os
import sqlite3
import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from datetime import datetime
from openpyxl import Workbook

def create_connection():
    return sqlite3.connect("cash_flow.db")

def get_transazioni_per_periodo(start_date, end_date):    
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Formato data non valido. Usa 'YYYY-MM-DD'.")
    
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id_transazione, t.data_ora, t.id_turno, tu.des_turno, t.id_operatore, (op.nome || ', ' || op.cognome) as des_operatore, t.id_articolo, a.des_articolo, t.quantita, t.valore_unitario, t.sconto, t.tot_transazione, t.des_transazione, t.id_pagamento, p.des_pagamento, t.id_categoria, c.des_categoria
        FROM Transazioni as t
        LEFT JOIN turni as tu ON t.id_turno = tu.id_turno
        LEFT JOIN operatori as op ON t.id_operatore = op.id_operatore
        LEFT JOIN articoli as a ON t.id_articolo = a.id_articolo
        LEFT JOIN pagamenti as p ON t.id_pagamento = p.id_pagamento
        LEFT JOIN categorie as c ON t.id_categoria = c.id_categoria
        WHERE DATE(t.data_ora) BETWEEN ? AND ?
        ORDER BY t.data_ora, t.id_transazione
    """, (start_date, end_date))
    transazioni = cursor.fetchall()
    conn.close()
    return transazioni

def generate_pdf(transazioni, filename, start_date, end_date):
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)
    c.setFont("Helvetica", 20)
    
    start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    
    # Controllo se ci sono dati
    if not data:
        # Messaggio specifico quando non ci sono dati
        c.drawString(100, 700, f"Report Transazioni dal {data_inizio} al {data_fine}")
        c.drawString(100, 680, "Nessuna transazione disponibile per il periodo specificato.")
        c.save()
        return
    
    title =  f"Report Transazioni dal {start_date} al {end_date}"
    c.drawString(100, height - 40, title)
    c.setFont("Helvetica", 12)
    y = height - 80
    headers = ["ID", "Data Ora", "Turno", "Operatore", "Articolo", "Q.tà", "Val.", "%", "Totale", "Descrizione", "Pagamento", "Categoria"]
    x_positions = [10, 30, 100, 165, 260, 330, 380, 430, 480, 530, 650, 750]

    # Stampa delle intestazioni
    for i, header in enumerate(headers):
        c.drawString(x_positions[i], y, header)
    y -= 20

    # Stampa delle transazioni
    xpos = -1
    for trans in transazioni:
        for i, value in enumerate(trans):
            if i in [0, 1, 3, 5, 7, 8, 9, 10, 11, 12, 14, 16]:
                xpos = xpos + 1
                c.drawString(x_positions[xpos], y, str(value))
        xpos = -1
        y -= 20

    # Calcolo dei totali per tipo di pagamento
    summary = {}
    for trans in transazioni:
        id_pagamento = trans[13]
        des_pagamento = trans[14]
        quantita = trans[8]
        tot_transazione = trans[11]
        if id_pagamento not in summary:
            summary[id_pagamento] = {"des_pagamento": des_pagamento, "quantita": 0, "tot_transazione": 0}
        summary[id_pagamento]["quantita"] += quantita
        summary[id_pagamento]["tot_transazione"] += tot_transazione

    # Stampa dei totali per tipo di pagamento
    y -= 20
    for id_pagamento, data in summary.items():
        c.drawString(100, y, f"Pagamento: {data['des_pagamento']}")
        c.drawString(300, y, f"Quantità Tot.: {data['quantita']}")
        c.drawString(500, y, f"Tot. pagamento: {data['tot_transazione']}")
        y -= 30

    # Calcolo dei totali complessivi
    total_quantita = sum(data["quantita"] for data in summary.values())
    total_tot_transazione = sum(data["tot_transazione"] for data in summary.values())
    
    c.setFont("Helvetica", 15)
    
    # Aggiunta dei totali complessivi in fondo al PDF
    c.drawString(100, y - 20, f"Quantità totale del periodo: {total_quantita}")
    c.drawString(100, y - 40, f"Totale transato del periodo: {total_tot_transazione}")

    c.save()
    
def generate_xlsx(transazioni, filename, start_date, end_date):
    try:
        wb = Workbook()
        wb.properties.title = "Report Transazioni"
        wb.properties.subject = "Report Transazioni"    
        wb.properties.creator = "CashFlow"
        wb.properties.created = datetime.now()
        wb.properties.modified = datetime.now()
        wb.properties.lastModifiedBy = "CashFlow"
        wb.properties.description = "Report delle transazioni effettuate"
        wb.properties.keywords = "transazioni, report, cashflow"
        wb.properties.category = "Report"
        wb.properties.language = "it-IT"
        wb.properties.contentStatus = "Final"
        wb.properties.version = "1.0"
    
        ws = wb.active
        ws.title = "Transazioni dal {} al {}".format(start_date, end_date)  
        
        # Aggiungi l'intestazione
        headers = ["ID", "Data", "ID Operatore", "Operatore", "ID Categoria", "Categoria", "ID Articolo", "Articolo", "Quantità", "Valore Unitario", "Sconto", "Totale", "Descrizione","ID Pagamento", "Pagamento", "ID Categoria", "Categoria"]
        ws.append(headers)

        # Aggiungi i dati delle transazioni
        for trans in transazioni:
            ws.append([
                trans[0],
                trans[1],
                trans[2],
                trans[3],
                trans[4],
                trans[5],
                trans[6],
                trans[7],
                int(trans[8]),
                float(trans[9]),
                float(trans[10]),
                float(trans[11]),
                trans[12],
                trans[13],
                trans[14],
                trans[15],
                trans[16]
            ])
        # Salva il workbook
        wb.save(filename)
        wb.close()

    except Exception as e:
        messagebox.showerror("Errore", f"Errore nell'export delle transazioni: {e}")
            
def send_email(filename, sender, recipient, provider):
    subject = "Report Giornaliero Museo generato il " + datetime.now().strftime("%Y-%m-%d")
    body = "Ecco il report giornaliero delle transazioni."

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    
    # Corpo dell'email
    body = "In allegato troverai il report delle transazioni."
    msg.attach(MIMEText(body, 'plain'))

    # Allegato PDF
    pdf_attachment = open(f"{filename}.pdf", "rb")
    pdf_part = MIMEApplication(pdf_attachment.read(), _subtype="pdf")
    pdf_part.add_header('Content-Disposition', 'attachment', filename=f"{filename}.pdf")
    msg.attach(pdf_part)
    pdf_attachment.close()

    # Allegato XLSX
    xlsx_attachment = open(f"{filename}.xlsx", "rb")
    xlsx_part = MIMEApplication(xlsx_attachment.read(), _subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    xlsx_part.add_header('Content-Disposition', 'attachment', filename=f"{filename}.xlsx")
    msg.attach(xlsx_part)
    xlsx_attachment.close()
    
    # Configura il server SMTP in base al provider selezionato
    if provider == "Gmail":
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
    elif provider == "Yahoo":
        smtp_server = 'smtp.mail.yahoo.com'
        smtp_port = 587
    elif provider == "Outlook":
        smtp_server = 'smtp.office365.com'
        smtp_port = 587
    else:
        raise ValueError("Provider SMTP non supportato")

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender, "lavoro")  # Inserisci la password reale
    text = msg.as_string()
    server.sendmail(sender, recipient, text)
    server.quit()

def generate_report(start_date, end_date, sender, recipient):
    transazioni = get_transazioni_per_periodo(start_date, end_date)
    if not os.path.exists("reports"):
        os.makedirs("reports")
    filename = os.path.join("reports", f"report_transazioni_{start_date}_to_{end_date}.pdf")
    generate_pdf(transazioni, filename, start_date, end_date)
    send_email(filename, sender, recipient)