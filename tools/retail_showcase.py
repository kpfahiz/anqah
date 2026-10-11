"""3D SELLO Retail "live checkout" (home card + product hero).

A supermarket checkout in Three.js (initRetail() in three-scenes.js): groceries ride a conveyor, a gooseneck barcode
scanner reads each one, the bill builds on the POS screen (SELLO Retail's billing layout, prices include GST), the
customer pays by UPI, then the WhatsApp bill and the owner's email summary pop up as HTML toasts over the canvas.
Items and screen texts are passed to the scene in data-retail.  Styles: "SELLO Retail live checkout" in style.css.

    from retail_showcase import showcase
    html = showcase(root='../', lang='en')
"""
import json


# (name EN, name AR, qty, unit price, colour, barcode) - same items and totals as the real SELLO Retail screenshots
ITEMS = [
    ('Basmati Rice 1 kg', 'أرز بسمتي 1 كجم', 2, 110.50, '#e9b44c', '8901058000127'),
    ('Sunflower Oil 1 L', 'زيت دوار الشمس 1 لتر', 1, 165.00, '#f2d16b', '8906007280014'),
    ('Tomato 1 kg', 'طماطم 1 كجم', 1, 31.50, '#e4572e', '2000000315006'),
    ('Tea Powder 250 g', 'شاي 250 جم', 1, 140.00, '#3fb68b', '8901030754123'),
]
TEXT = {
    'en': {'billing': 'Billing', 'counter': 'Counter 1', 'search': 'Scan barcode or type name / SKU, then Enter',
           'customer': 'Walk-in customer', 'subtotal': 'Subtotal', 'cgst': 'CGST', 'sgst': 'SGST', 'round': 'Round off',
           'pcs': 'pcs', 'aria': '3D model: SELLO Retail supermarket checkout with barcode scanner and POS screen', 'total': 'Total', 'pay': 'Pay (F12)', 'paid': 'Paid', 'scan': 'Scanning barcode',
           'wa_t': 'WhatsApp', 'wa': 'Bill C1/0002 &middot; ₹558.00 sent to customer',
           'mail_t': 'Email', 'mail': 'Daily summary sent to owner &middot; 9:00 PM', 'upi': 'UPI', 'cash': 'Cash', 'card': 'Card'},
    'ar': {'billing': 'الفوترة', 'counter': 'الكاونتر 1', 'search': 'امسح الباركود أو اكتب الاسم / الرمز ثم Enter',
           'customer': 'عميل نقدي', 'subtotal': 'المجموع الفرعي', 'cgst': 'CGST', 'sgst': 'SGST', 'round': 'تقريب',
           'pcs': 'قطعة', 'aria': 'نموذج ثلاثي الأبعاد: نقطة دفع SELLO Retail مع ماسح باركود وشاشة نقاط البيع', 'total': 'الإجمالي', 'pay': 'ادفع (F12)', 'paid': 'تم الدفع', 'scan': 'جارٍ مسح الباركود',
           'wa_t': 'واتساب', 'wa': 'أُرسلت الفاتورة C1/0002 &middot; ₹558.00 إلى العميل',
           'mail_t': 'البريد', 'mail': 'أُرسل الملخص اليومي إلى المالك &middot; 9:00 م', 'upi': 'UPI', 'cash': 'نقد', 'card': 'بطاقة'},
}
KINDS = ['bag', 'bottle', 'tray', 'box']   # 3D model for each item
WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1-1.6-.5-3.4-1.6-4.7-3.1-1-1.1-1.6-2.3-1.7-3.3 0-.9.5-1.6.8-1.9.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.8 1.9c.1.2.1.4 0 .5l-.4.6-.3.4c-.1.1-.2.3-.1.5.4.7 1 1.4 1.6 1.9.7.6 1.4 1 2 1.2.2.1.4 0 .5-.1l.7-.8c.2-.2.3-.2.6-.1l1.8.9c.2.1.4.2.4.3.1.2.1.7-.1 1.3z"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" d="M3 5h18v14H3z M3 6l9 7 9-7"/></svg>'



def showcase(root, lang='en', cls=''):
    t = TEXT[lang]
    data = {
        'items': [{'name': ar if lang == 'ar' else en, 'qty': q, 'price': p, 'colour': c, 'code': code, 'kind': kind}
                  for (en, ar, q, p, c, code), kind in zip(ITEMS, KINDS)],
        'text': {k: t[k] for k in ('billing', 'counter', 'search', 'customer', 'subtotal', 'cgst', 'sgst', 'round', 'pcs',
                                   'total', 'pay', 'paid', 'cash', 'card', 'upi')},
    }
    blob = json.dumps(data, ensure_ascii=False).replace("'", '&#39;')
    return f'''<div class="rc {cls}" dir="ltr" data-retail='{blob}'>
                        <div class="rc-bg"></div>
                        <canvas data-scene="selloRetail" aria-label="{t['aria']}"></canvas>
                        <div class="rc-toast rc-wa" aria-hidden="true"><span class="rc-ico">{WA}</span><span><b>{t['wa_t']}</b>{t['wa']}</span></div>
                        <div class="rc-toast rc-mail" aria-hidden="true"><span class="rc-ico">{MAIL}</span><span><b>{t['mail_t']}</b>{t['mail']}</span></div>
                        <div class="rc-os" aria-hidden="true"><span>Windows</span><span>Android</span><span>iOS</span></div>
                    </div>'''
