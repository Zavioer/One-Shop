import json
import hashlib
import hmac
from django.core.mail import send_mail, EmailMultiAlternatives
from fpdf import FPDF


class PDF(FPDF):
    def title(self, text):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(w=210.0, h=40.0, align='C', txt=text, border=0)

    def texts(self, text):
        self.set_xy(10.0,80.0)    
        self.set_text_color(76.0, 32.0, 250.0)
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)

def create_payment_chk(attributes: dict) -> str:
    dotpay_pin = b'5KxhBSFW7HJQ058ujZZHccUtJSuY2LSb' # TODO switch to env variable
    separator = ';'  # needed by dotpay doc
    keys = list(attributes.keys())
    keys.sort()
    
    paramsList = separator.join(keys)
    attributes.update({'paramsList': paramsList})

    sorted_attributes = dict(sorted(attributes.items()))
    json_attributes = json.dumps(sorted_attributes, separators=(',', ':'))
    encoded = hmac.new(key=dotpay_pin, msg=json_attributes.encode(), digestmod=hashlib.sha256).hexdigest()

    return encoded


def _create_bill_email_template(order_id: int, cost: float, status: str = 'ACCEPTED') -> str:
    # order id - card id
    # cost - amount 
    # status always accepted
    header = f'<h3>Your order {order_id} status</h3>'
    body = f'<p>Stasu of payment: <b>{status}</b>. Total cost: {cost}</p>'
    footer = f'<br><br><a href="">Rate out shop!</a>'

    return ''.join([header, body, footer])


def send_bill_email(email: str, order_id: int, cost: float) -> None:
    subject = 'SHOP - order status'
    email_body = _create_bill_email_template(order_id, cost)

    mail = EmailMultiAlternatives(
        subject,
        email_body,
        'shop-noreply@shop.com',
        [email]
    )

    pdf_bill = _generate_pdf_bill(email, order_id, cost)
    mail.attach_alternative(email_body, 'text/html')
    mail.attach(f'{order_id}.pdf', pdf_bill, 'application/pdf')

    mail.send()

def _generate_pdf_bill(email: str, order_id: int, cost: float, status: str = 'ACCEPTED')  -> bytearray:
    pdf = PDF()
    pdf.add_page()
    pdf.title(f'Your order {order_id} status')
    pdf.set_title(f'Your order {order_id} status: {status}')

    msg = f'Stasu of payment {status}. Total cost: {cost}\nThank You for Your shopping: *{email}*'

    pdf.texts(msg)

    return pdf.output(dest='S')
