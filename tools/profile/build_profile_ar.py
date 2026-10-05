"""Builds tools/profile/profile-ar.html (Arabic, right-to-left) from the English profile.html.
Each English string is swapped for its Arabic translation; if the English text changes, the matching pair below
must be updated too (the script stops and names the missing string).
    python tools/profile/build_profile_ar.py   then   node tools/profile/build_profile.mjs
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent

HEAD = [
    ('<html lang="en">', '<html lang="ar" dir="rtl">'),
    ('<title>Anqah Tech - Company Profile</title>', '<title>Anqah Tech - الملف التعريفي</title>'),
    ('&family=JetBrains+Mono', '&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Noto+Kufi+Arabic:wght@600;700;800&family=JetBrains+Mono'),
]

# Right-to-left overrides: Arabic fonts, no capitals/letter-spacing (they break Arabic joining), mirrored edges.
RTL_CSS = '''
/* ---------- Arabic / RTL ---------- */
:root { --display: 'Noto Kufi Arabic', 'Chakra Petch', sans-serif; --body: 'IBM Plex Sans Arabic', 'IBM Plex Sans', sans-serif; }
body { font-family: var(--body); }
h1, h2, h3, .kicker, .cover .brand span, .inds span, .incl li, .prod li, .stats span, .cgrid small, .foot,
.pos-grid figcaption b, .cover .hero div::after, .prod .img::after, .band div::after, .stack span, .cover .web, .cover .status {
    text-transform: none; letter-spacing: 0;
}
.kicker, .prod li, .stats span, .cgrid small, .foot, .cover .web, .cover .status, .cover .hero div::after,
.prod .img::after, .band div::after { font-family: var(--body); }
h1, h2 { line-height: 1.3; }
h2 { font-size: 30pt; }
.cover h1 { font-size: 40pt; }
h3 { line-height: 1.45; }
p { line-height: 1.8; }
.cover .brand { left: auto; right: 18mm; }
.cover .brand span { font-family: 'Chakra Petch', sans-serif; text-transform: uppercase; }
.cover .status { right: auto; left: 18mm; text-align: left; }
.cover .hero div::after, .band div::after { left: auto; right: 3mm; }
.prod .img::after { left: auto; right: 3mm; }
.stats div { border-left: 0; border-right: 0.8mm solid var(--lime); padding-left: 0; padding-right: 3mm; }
.why div::before { left: auto; right: 0; }
.inds span { border-left: 0; border-right: 1mm solid var(--navy); }
.pos-grid figcaption { border-left: 0; border-right: 0.8mm solid var(--lime); padding-left: 0; padding-right: 2.5mm; }
.svc h3 { font-size: 11pt; }
.ltr { direction: ltr; unicode-bidi: isolate; display: inline-block; }
</style>'''

TEXT = [
    # cover
    ('<div class="status"><i></i>SYS.ONLINE<br>ABU DHABI &middot; UAE</div>', '<div class="status"><i></i>SYS.ONLINE<br>أبوظبي &middot; الإمارات</div>'),
    ('<div class="kicker">Company Profile</div>', '<div class="kicker">الملف التعريفي للشركة</div>'),
    ('<h1>Intelligent POS, IoT<span>&amp; IT systems</span></h1>', '<h1>أنظمة ذكية لنقاط البيع<span>وإنترنت الأشياء والتقنية</span></h1>'),
    ('<p>Software, smart devices and IT infrastructure for businesses, schools and homes across the UAE, Saudi Arabia and India.</p>',
     '<p>برمجيات وأجهزة ذكية وبنية تحتية لتقنية المعلومات للشركات والمدارس والمنازل في الإمارات والسعودية والهند.</p>'),
    ('data-label="AUTOMATIC BELL"></div>\n        <div style="background-image:url(\'../../images/profile/stage-water-monitoring.jpg\')" data-label="WATER MONITORING">',
     'data-label="الجرس الآلي"></div>\n        <div style="background-image:url(\'../../images/profile/stage-water-monitoring.jpg\')" data-label="مراقبة خزانات المياه">'),
    ('<span>POS &middot; IoT &middot; IT SOLUTIONS</span>', '<span>نقاط البيع &middot; إنترنت الأشياء &middot; حلول تقنية</span>'),
    # footers
    ('<span><b>ANQAH TECH</b> &middot; COMPANY PROFILE</span>', '<span><b>ANQAH TECH</b> &middot; الملف التعريفي</span>'),
    # about
    ('01 &middot; Who we are', '01 &middot; من نحن'),
    ('<h2>About <em>us</em></h2>', '<h2>نبذة <em>عنّا</em></h2>'),
    ('<p class="lead">Anqah Tech is a software, IoT and IT solutions company based in Abu Dhabi, United Arab Emirates. We design and build our own products &mdash; the <b>SELLO</b> point-of-sale system, the <b>SELLO Lite</b> mobile POS app, the <b>Automatic Bell</b> and <b>Water Monitoring</b> &mdash; supply complete POS systems with hardware, and deliver web, mobile, CCTV, networking, automation and IT infrastructure for businesses, schools and homes.</p>',
     '<p class="lead">Anqah Tech شركة برمجيات وإنترنت أشياء وحلول تقنية مقرّها أبوظبي، الإمارات العربية المتحدة. نصمّم ونطوّر منتجاتنا الخاصة &mdash; نظام نقاط البيع <b>SELLO</b>، وتطبيق الكاشير للجوال <b>SELLO Lite</b>، و<b>الجرس الآلي</b>، و<b>مراقبة خزانات المياه</b> &mdash; ونوفّر أنظمة نقاط بيع متكاملة مع الأجهزة، ونقدّم تطوير المواقع وتطبيقات الجوال وكاميرات المراقبة والشبكات والأتمتة والبنية التحتية لتقنية المعلومات للشركات والمدارس والمنازل.</p>'),
    ('<div><h3>Vision</h3><p>To be the region&rsquo;s most dependable technology partner &mdash; where every shop, school and home runs on systems that are simple, smart and always on.</p></div>',
     '<div><h3>رؤيتنا</h3><p>أن نكون الشريك التقني الأكثر موثوقية في المنطقة &mdash; حيث يعمل كل متجر ومدرسة ومنزل بأنظمة بسيطة وذكية وتعمل دائمًا.</p></div>'),
    ('<div><h3>Mission</h3><p>To engineer practical software and connected devices that remove everyday friction, delivered end-to-end with honest pricing and local support.</p></div>',
     '<div><h3>رسالتنا</h3><p>تطوير برمجيات عملية وأجهزة متصلة تزيل متاعب العمل اليومي، وتسليمها من البداية للنهاية بأسعار صادقة ودعم محلي.</p></div>'),
    ('<div><h3>Our promise</h3><p>You work directly with the engineers who build your system. We design for how you actually work, keep it running with support and AMC, and stand behind every installation.</p></div>',
     '<div><h3>وعدنا</h3><p>تتعامل مباشرة مع المهندسين الذين يبنون نظامك. نصمّم وفق طريقة عملك الفعلية، ونحافظ على تشغيله بالدعم وعقود الصيانة، ونقف خلف كل تركيب.</p></div>'),
    ('<span>In-house products</span>', '<span>منتجات من تطويرنا</span>'),
    ('<span>Service lines</span>', '<span>خدمة تقنية</span>'),
    ('<span>Countries served</span>', '<span>دول نخدمها</span>'),
    ('<span>Languages: EN &middot; AR</span>', '<span>لغتان: العربية والإنجليزية</span>'),
    # products
    ('02 &middot; Built by us', '02 &middot; من تطويرنا'),
    ('<h2 style="margin-left:26mm">Our <em>products</em></h2>', '<h2 style="margin-left:26mm"><em>منتجاتنا</em></h2>'),
    ('data-tag="POS All-in-One Solution"', 'data-tag="حل نقاط بيع متكامل"'),
    ('<p>Complete point-of-sale and shop management for retail stores, restaurants and caf&eacute;s &mdash; billing, inventory, kitchen display and reports, running on your own shop network.</p>',
     '<p>نظام متكامل لنقاط البيع وإدارة المتاجر والمطاعم والمقاهي &mdash; فوترة ومخزون وشاشة مطبخ وتقارير، يعمل على شبكة متجرك الخاصة.</p>'),
    ('<ul><li>Retail &amp; restaurant</li><li>Kitchen display</li><li>Inventory</li><li>VAT / GST</li></ul>',
     '<ul><li>تجزئة ومطاعم</li><li>شاشة المطبخ</li><li>المخزون</li><li>ضريبة القيمة المضافة</li></ul>'),
    ('data-tag="Mobile POS"', 'data-tag="كاشير على الجوال"'),
    ('<p>An offline point-of-sale app for Android phones and tablets. Sell, print receipts and see reports with no internet and no cloud subscription.</p>',
     '<p>تطبيق كاشير يعمل دون إنترنت على هواتف وأجهزة أندرويد اللوحية. بِع واطبع الإيصالات واطّلع على التقارير دون إنترنت ودون اشتراك سحابي.</p>'),
    ('<ul><li>Works offline</li><li>Portions</li><li>Reports</li><li>Arabic</li></ul>',
     '<ul><li>يعمل دون إنترنت</li><li>أحجام الأطباق</li><li>التقارير</li><li>العربية</li></ul>'),
    ('data-tag="IoT &middot; Automation"', 'data-tag="إنترنت الأشياء &middot; أتمتة"'),
    ('<h3>Automatic Bell</h3><p>A WiFi bell controller that rings on schedule, skips weekends and holidays, and is managed from a mobile app.</p>',
     '<h3>الجرس الآلي</h3><p>وحدة تحكم بالجرس عبر WiFi ترنّ حسب الجدول، وتتخطّى العطل الأسبوعية والرسمية، وتُدار من تطبيق الجوال.</p>'),
    ('<ul><li>Schools</li><li>Colleges</li><li>Hostels</li><li>Factories</li></ul>',
     '<ul><li>المدارس</li><li>الكليات</li><li>السكن الطلابي</li><li>المصانع</li></ul>'),
    ('data-tag="IoT &middot; Smart Home"', 'data-tag="إنترنت الأشياء &middot; منزل ذكي"'),
    ('<h3>Water Monitoring</h3><p>Live tank level on your phone, with Telegram alerts below 15% (tank empty) and above 95% (overflow).</p>',
     '<h3>مراقبة خزانات المياه</h3><p>منسوب الخزان مباشرة على جوالك، مع تنبيهات تيليجرام عند أقل من 15% (الخزان فارغ) وأكثر من 95% (فيضان).</p>'),
    ('<ul><li>Live level</li><li>Telegram alerts</li><li>Villas</li><li>Buildings</li></ul>',
     '<ul><li>المنسوب مباشرة</li><li>تنبيهات تيليجرام</li><li>الفلل</li><li>البنايات</li></ul>'),
    # SELLO in action
    ('03 &middot; POS systems', '03 &middot; أنظمة نقاط البيع'),
    ('<h2>SELLO <em>in action</em></h2>', '<h2>SELLO <em>أثناء العمل</em></h2>'),
    ('<p class="lead" style="margin-bottom:6mm">One POS all-in-one solution for the counter, the dining floor and the kitchen &mdash; running on touch POS terminals, tablets and PCs on your own shop network.</p>',
     '<p class="lead" style="margin-bottom:6mm">حل نقاط بيع متكامل واحد للكاونتر وصالة الطعام والمطبخ &mdash; يعمل على أجهزة كاشير باللمس وأجهزة لوحية وحواسيب على شبكة متجرك الخاصة.</p>'),
    ('<b>Point of sale</b>Fast touch billing with categories, barcode search and a live cart with VAT.', '<b>نقطة البيع</b>فوترة سريعة باللمس مع الفئات والبحث بالباركود وسلة مباشرة مع ضريبة القيمة المضافة.'),
    ('<b>Checkout</b>Cash, card or split payments, with change calculated automatically.', '<b>الدفع</b>نقدًا أو بالبطاقة أو دفع مجزّأ، مع حساب الباقي تلقائيًا.'),
    ('<b>Restaurant tables</b>See every table at a glance, seat guests and manage orders in rounds.', '<b>طاولات المطعم</b>اطّلع على كل الطاولات بنظرة، واستقبل الضيوف، وأدِر الطلبات على دفعات.'),
    ('<b>Kitchen display</b>Tickets flow from New to Accepted, Preparing and Ready at the kitchen pass.', '<b>شاشة المطبخ</b>تنتقل الطلبات من جديد إلى مقبول ثم قيد التحضير ثم جاهز.'),
    ('<b>Sales history</b>Every invoice with payment method, items and one-click returns or exchanges.', '<b>سجل المبيعات</b>كل فاتورة مع طريقة الدفع والأصناف والمرتجعات أو الاستبدال بنقرة واحدة.'),
    ('<b>Dashboard</b>One home screen for POS, inventory, purchasing, kitchen, reports and settings.', '<b>لوحة التحكم</b>شاشة رئيسية واحدة للبيع والمخزون والمشتريات والمطبخ والتقارير والإعدادات.'),
    # POS hardware
    ('03 &middot; POS hardware', '03 &middot; أجهزة نقاط البيع'),
    ('<h2 style="margin-left:26mm">We sell <em>complete POS systems</em></h2>', '<h2 style="margin-left:26mm">نبيع <em>أنظمة نقاط بيع متكاملة</em></h2>'),
    ('<p class="lead" style="margin-bottom:5mm">Hardware and software from one supplier. We supply the POS machines, install SELLO, set up your products and taxes, and train your staff &mdash; ready to sell from day one.</p>',
     '<p class="lead" style="margin-bottom:5mm">الأجهزة والبرنامج من مورّد واحد. نوفّر أجهزة الكاشير، ونثبّت SELLO، ونُعدّ منتجاتك وضرائبك، وندرّب موظفيك &mdash; جاهز للبيع من اليوم الأول.</p>'),
    ('<b>Dual-screen POS terminal</b>All-in-one touch terminal with a customer-facing display.', '<b>جهاز كاشير بشاشتين</b>جهاز لمس متكامل مع شاشة عرض للعميل.'),
    ('<b>Receipt printer</b>Fast thermal printing for receipts and kitchen tickets.', '<b>طابعة الإيصالات</b>طباعة حرارية سريعة للإيصالات وتذاكر المطبخ.'),
    ('<b>Tablet POS</b>Compact counter or table-side billing on a secure stand.', '<b>كاشير على جهاز لوحي</b>فوترة مدمجة على الكاونتر أو عند الطاولة على حامل آمن.'),
    ('<b>Kitchen display</b>A screen at the kitchen pass, so orders never get lost.', '<b>شاشة المطبخ</b>شاشة عند نقطة استلام الطلبات في المطبخ حتى لا يضيع أي طلب.'),
    ('<b>Cash drawer</b>Opens automatically on cash sales and keeps takings secure.', '<b>درج النقود</b>يُفتح تلقائيًا عند البيع النقدي ويحفظ النقود بأمان.'),
    ('<b>Touch-screen POS monitor</b>Large touch screen for busy counters and the back office.', '<b>شاشة كاشير تعمل باللمس</b>شاشة لمس كبيرة للكاونترات المزدحمة والمكتب الخلفي.'),
    ('<span class="kicker">Every POS package includes</span>', '<span class="kicker">تشمل كل باقة نقاط بيع</span>'),
    ('<ul><li>POS hardware</li><li>SELLO software</li><li>Installation &amp; setup</li><li>Product &amp; VAT/GST setup</li><li>Staff training</li><li>Support &amp; AMC</li></ul>',
     '<ul><li>أجهزة نقاط البيع</li><li>برنامج SELLO</li><li>التركيب والإعداد</li><li>إعداد المنتجات والضريبة</li><li>تدريب الموظفين</li><li>الدعم وعقود الصيانة</li></ul>'),
    # services
    ('04 &middot; Services', '04 &middot; الخدمات'),
    ('<h2>What <em>we do?</em></h2>', '<h2>ماذا <em>نقدّم؟</em></h2>'),
    ('<p class="lead" style="margin-bottom:5mm">Comprehensive technology solutions for modern businesses and homes &mdash; designed, installed and supported by one team.</p>',
     '<p class="lead" style="margin-bottom:5mm">حلول تقنية شاملة للشركات والمنازل الحديثة &mdash; يصمّمها ويركّبها ويدعمها فريق واحد.</p>'),
    ('<h3>Web Design &amp; Development</h3><p>Responsive websites and web applications, optimised for performance and SEO.</p>', '<h3>تصميم وتطوير المواقع</h3><p>مواقع وتطبيقات ويب متجاوبة، مُحسّنة للأداء ومحركات البحث.</p>'),
    ('<h3>Mobile App Development</h3><p>Native and cross-platform apps for iOS and Android.</p>', '<h3>تطوير تطبيقات الجوال</h3><p>تطبيقات أصلية ومتعددة المنصات لأجهزة iOS وأندرويد.</p>'),
    ('<h3>Digital Marketing &amp; Branding</h3><p>SEO, social media, PPC and brand identity design.</p>', '<h3>التسويق الرقمي والهوية</h3><p>تحسين محركات البحث، ووسائل التواصل، والإعلانات المدفوعة، وتصميم الهوية.</p>'),
    ('<h3>POS Systems &amp; Hardware</h3><p>Complete POS machines with SELLO software, printers, cash drawers and ERP.</p>', '<h3>أنظمة وأجهزة نقاط البيع</h3><p>أجهزة كاشير متكاملة مع برنامج SELLO والطابعات وأدراج النقود وأنظمة ERP.</p>'),
    ('<h3>IT Solutions &amp; Infrastructure</h3><p>IT setup, server management, networking and cloud.</p>', '<h3>حلول وبنية تحتية تقنية</h3><p>تجهيز الأنظمة وإدارة الخوادم والشبكات والحلول السحابية.</p>'),
    ('<h3>CCTV Installation &amp; Service</h3><p>HD/4K and IP camera systems &mdash; supply, install and maintain.</p>', '<h3>تركيب وصيانة كاميرات المراقبة</h3><p>أنظمة كاميرات HD/4K و IP &mdash; توريد وتركيب وصيانة.</p>'),
    ('<h3>Access Control &amp; Attendance</h3><p>Biometric and card access, time attendance and intercom.</p>', '<h3>التحكم بالدخول والحضور</h3><p>دخول بالبصمة والبطاقة، وتسجيل الحضور، والإنتركم.</p>'),
    ('<h3>WiFi, GSM &amp; Networks</h3><p>Enterprise WiFi, GSM signal solutions and structured cabling.</p>', '<h3>الواي فاي والشبكات وتقوية الإشارة</h3><p>شبكات WiFi للمؤسسات، وحلول تقوية إشارة الجوال، والتمديدات المنظمة.</p>'),
    ('<h3>Home, Gate &amp; AC Automation</h3><p>Smart home, automated gates, AC control and IoT living.</p>', '<h3>أتمتة المنازل والبوابات والتكييف</h3><p>منزل ذكي، وبوابات آلية، والتحكم بالتكييف، وحياة متصلة.</p>'),
    ('<h3>Automobile Solutions</h3><p>GPS tracking, dash cameras and fleet technology.</p>', '<h3>حلول المركبات</h3><p>تتبّع GPS، وكاميرات السيارات، وتقنيات إدارة الأساطيل.</p>'),
    ('<h3>Electrical Services</h3><p>Wiring, sensor installation and automated electrical systems.</p>', '<h3>الخدمات الكهربائية</h3><p>التمديدات، وتركيب الحساسات، والأنظمة الكهربائية الآلية.</p>'),
    ('<h3>Annual Maintenance (AMC)</h3><p>Preventive, on-site support for IT, CCTV, networks and automation.</p>', '<h3>عقود الصيانة السنوية</h3><p>دعم وقائي في الموقع للأنظمة والكاميرات والشبكات والأتمتة.</p>'),
    # why
    ('05 &middot; Our edge', '05 &middot; ما يميّزنا'),
    ('<h2 style="margin-left:26mm">Why choose <em>Anqah Tech?</em></h2>', '<h2 style="margin-left:26mm">لماذا تختار <em>Anqah Tech؟</em></h2>'),
    ('<p class="lead" style="margin-bottom:6mm">We don&rsquo;t just deliver technology &mdash; we deliver confidence.</p>', '<p class="lead" style="margin-bottom:6mm">لا نقدّم التقنية فقط &mdash; بل نقدّم الثقة.</p>'),
    ('<h3>Own products</h3><p>You deal directly with the engineers who built SELLO, the Automatic Bell and Water Monitoring.</p>', '<h3>منتجاتنا الخاصة</h3><p>تتعامل مباشرة مع المهندسين الذين طوّروا SELLO والجرس الآلي ومراقبة خزانات المياه.</p>'),
    ('<h3>End-to-end</h3><p>Design, supply, installation, training and maintenance &mdash; one partner, one point of contact.</p>', '<h3>من البداية للنهاية</h3><p>التصميم والتوريد والتركيب والتدريب والصيانة &mdash; شريك واحد وجهة تواصل واحدة.</p>'),
    ('<h3>Reliable &amp; secure</h3><p>Systems that keep working offline and are built with security in every deployment.</p>', '<h3>موثوق وآمن</h3><p>أنظمة تستمر في العمل دون إنترنت، مع مراعاة الأمان في كل تركيب.</p>'),
    ('<h3>Fast turnaround</h3><p>Quick delivery without compromising on quality or detail.</p>', '<h3>تنفيذ سريع</h3><p>تسليم سريع دون التنازل عن الجودة أو التفاصيل.</p>'),
    ('<h3>Local expertise</h3><p>Deep knowledge of the local market, including VAT and GST tax setup.</p>', '<h3>خبرة محلية</h3><p>معرفة عميقة بالسوق المحلي، بما في ذلك إعداد ضريبة القيمة المضافة.</p>'),
    ('<h3>Fair pricing</h3><p>Premium solutions at transparent, competitive prices &mdash; no surprise fees.</p>', '<h3>أسعار عادلة</h3><p>حلول متميزة بأسعار شفافة وتنافسية &mdash; دون رسوم مفاجئة.</p>'),
    ('<h3>Innovative</h3><p>IoT, mobile and modern web technology applied to everyday problems.</p>', '<h3>الابتكار</h3><p>إنترنت الأشياء وتطبيقات الجوال وتقنيات الويب الحديثة لحل المشكلات اليومية.</p>'),
    ('<h3>Full support</h3><p>Technical support and AMC packages for complete peace of mind.</p>', '<h3>دعم كامل</h3><p>دعم فني وباقات صيانة سنوية لراحة بال تامة.</p>'),
    ('<h3 class="sub">Areas we serve</h3>', '<h3 class="sub">المناطق التي نخدمها</h3>'),
    ('<span class="kicker">Headquarters</span><h3>United Arab Emirates</h3><p>Abu Dhabi &middot; Dubai &middot; Sharjah &middot; Al Ain &middot; Ajman</p>',
     '<span class="kicker">المقر الرئيسي</span><h3>الإمارات العربية المتحدة</h3><p>أبوظبي &middot; دبي &middot; الشارقة &middot; العين &middot; عجمان</p>'),
    ('<span class="kicker">KSA</span><h3>Saudi Arabia</h3><p>Riyadh &middot; Jeddah &middot; Dammam &middot; Makkah &middot; Madinah</p>',
     '<span class="kicker">المملكة</span><h3>المملكة العربية السعودية</h3><p>الرياض &middot; جدة &middot; الدمام &middot; مكة المكرمة &middot; المدينة المنورة</p>'),
    ('<span class="kicker">India</span><h3>India</h3><p>Kerala &middot; Bengaluru &middot; Chennai &middot; Mumbai &middot; Hyderabad</p>',
     '<span class="kicker">الهند</span><h3>الهند</h3><p>كيرالا &middot; بنغالور &middot; تشيناي &middot; مومباي &middot; حيدر أباد</p>'),
    # how we work
    ('06 &middot; Process', '06 &middot; آلية العمل'),
    ('<h2>How <em>we work?</em></h2>', '<h2>كيف <em>نعمل؟</em></h2>'),
    ('<p class="lead" style="margin-bottom:6mm">A clear four-step process, from the first conversation to long-term support.</p>', '<p class="lead" style="margin-bottom:6mm">عملية واضحة من أربع خطوات، من أول محادثة حتى الدعم طويل الأمد.</p>'),
    ('<h3>Discover</h3><p>We understand your workflow, site and budget.</p>', '<h3>الاستكشاف</h3><p>نفهم سير عملك وموقعك وميزانيتك.</p>'),
    ('<h3>Design</h3><p>We plan the system, the hardware and the experience.</p>', '<h3>التصميم</h3><p>نخطّط للنظام والأجهزة وتجربة الاستخدام.</p>'),
    ('<h3>Build &amp; install</h3><p>We develop, configure and install on site.</p>', '<h3>التطوير والتركيب</h3><p>نطوّر ونُعدّ ونركّب في الموقع.</p>'),
    ('<h3>Support</h3><p>Training, updates and AMC so it keeps running.</p>', '<h3>الدعم</h3><p>التدريب والتحديثات وعقود الصيانة ليستمر العمل.</p>'),
    ('<h3 class="sub">Who we serve</h3>', '<h3 class="sub">من نخدم</h3>'),
    ('<span>Retail stores</span><span>Restaurants &amp; caf&eacute;s</span><span>Supermarkets</span><span>Schools</span>',
     '<span>متاجر التجزئة</span><span>المطاعم والمقاهي</span><span>السوبرماركت</span><span>المدارس</span>'),
    ('<span>Colleges</span><span>Hostels</span><span>Offices</span><span>Factories</span>', '<span>الكليات</span><span>السكن الطلابي</span><span>المكاتب</span><span>المصانع</span>'),
    ('<span>Villas &amp; homes</span><span>Buildings</span><span>Farms</span><span>Fleets</span>', '<span>الفلل والمنازل</span><span>البنايات</span><span>المزارع</span><span>الأساطيل</span>'),
    ('<h3 class="sub">Technology we work with</h3>', '<h3 class="sub">التقنيات التي نعمل بها</h3>'),
    ('<span>IP CCTV</span><span>Structured cabling</span>', '<span>IP CCTV</span><span>التمديدات المنظمة</span>'),
    ('data-label="SELLO &middot; TABLES"', 'data-label="SELLO &middot; الطاولات"'),
    ('data-label="SELLO &middot; KITCHEN"', 'data-label="SELLO &middot; المطبخ"'),
    ('<div style="background-image:url(\'img/bell-system-white.jpg\')" data-label="AUTOMATIC BELL">', '<div style="background-image:url(\'img/bell-system-white.jpg\')" data-label="الجرس الآلي">'),
    # contact
    ('07 &middot; Get in touch', '07 &middot; تواصل معنا'),
    ('<h2>Contact us</h2>', '<h2>تواصل معنا</h2>'),
    ('<p class="lead" style="color:#aab3bc">Tell us what you need &mdash; our team replies within 24 hours.</p>', '<p class="lead" style="color:#aab3bc">أخبرنا بما تحتاجه &mdash; يردّ فريقنا خلال 24 ساعة.</p>'),
    ('<div><small>Phone (UAE)</small><b>+971 50 239 3703</b></div>', '<div><small>الهاتف (الإمارات)</small><b class="ltr">+971 50 239 3703</b></div>'),
    ('<div><small>Phone (India)</small><b>+91 95670 40754</b></div>', '<div><small>الهاتف (الهند)</small><b class="ltr">+91 95670 40754</b></div>'),
    ('<div><small>WhatsApp</small><b>+971 50 576 2100</b></div>', '<div><small>واتساب</small><b class="ltr">+971 50 576 2100</b></div>'),
    ('<div><small>Email</small><b>anqahgroups@gmail.com</b></div>', '<div><small>البريد الإلكتروني</small><b class="ltr">anqahgroups@gmail.com</b></div>'),
    ('<div><small>Address</small><b>Abu Dhabi, UAE</b></div>', '<div><small>العنوان</small><b>أبوظبي، الإمارات</b></div>'),
    ('<div><small>Hours</small><b>Mon &ndash; Sat, 9 AM &ndash; 7 PM</b></div>', '<div><small>ساعات العمل</small><b>الاثنين &ndash; السبت، 9 ص &ndash; 7 م</b></div>'),
    ('<h3>Let&rsquo;s build something great</h3>', '<h3>لنبنِ معًا شيئًا رائعًا</h3>'),
]


def main():
    s = (HERE / 'profile.html').read_text(encoding='utf-8')
    for old, new in HEAD + TEXT:
        if old not in s:
            raise SystemExit(f'English text changed - update the translation for:\n  {old[:120]}')
        s = s.replace(old, new)
    # mirror the corner shapes (and the heading indent that keeps clear of them) for right-to-left pages
    for a, b in (('geo tr-', 'geo @TL-'), ('geo tl-', 'geo tr-'), ('geo @TL-', 'geo tl-'),
                 ('geo br-', 'geo @BL-'), ('geo bl-', 'geo br-'), ('geo @BL-', 'geo bl-'),
                 ('style="margin-left:26mm"', 'style="margin-right:26mm"')):
        s = s.replace(a, b)
    s = s.replace('</style>', RTL_CSS, 1)
    s = s.replace('<!-- Anqah Tech company profile (A4).', '<!-- GENERATED by build_profile_ar.py from profile.html - edit those, not this file. Arabic company profile (A4).')
    (HERE / 'profile-ar.html').write_text(s, encoding='utf-8')
    print('wrote tools/profile/profile-ar.html')


if __name__ == '__main__':
    main()
