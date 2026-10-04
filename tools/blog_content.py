"""Guides / blog articles (English + Arabic). Rendered by tools/build_blog.py.

Each article: slug, date, product (slug of the related product page), and per-language
title, description, keywords, intro and sections (heading, html).
Keep claims factual: describe what to look for; never claim certifications we haven't confirmed.
"""

ARTICLES = [
    {
        'slug': 'restaurant-pos-system-uae',
        'date': '2026-10-04',
        'product': 'sello',
        'en': {
            'title': 'How to Choose a Restaurant POS System in the UAE',
            'description': 'A practical checklist for restaurants and cafés in Abu Dhabi, Dubai and across the UAE: VAT invoices, offline billing, kitchen display, tables and inventory.',
            'keywords': 'restaurant POS UAE, POS system Abu Dhabi, POS system Dubai, cafe POS UAE, restaurant billing software, kitchen display system, VAT invoice POS',
            'intro': 'A restaurant POS does far more than print bills. In the UAE it has to produce VAT-ready invoices, keep the kitchen in sync with the floor, and keep working when the internet doesn&rsquo;t. Use this checklist before you choose one.',
            'sections': [
                ('1. VAT-ready invoices', '<p>UAE VAT is charged at 5%. Your POS should let you set the tax rate once, show tax clearly on every receipt, and print your business details on invoices. Check that you can choose whether menu prices include VAT or have it added at checkout, and that tax reports can be exported for your accountant.</p>'),
                ('2. It must keep billing when the internet drops', '<p>Cloud-only systems stop the moment the connection fails &mdash; usually during the lunch rush. Look for a POS that runs on your own shop network or stores sales on the device, then syncs or backs up afterwards. Ask the provider directly: <em>&ldquo;Can I take payment with no internet?&rdquo;</em></p>'),
                ('3. Tables, orders and the kitchen', '<p>For dine-in you need a floor plan with table status, orders taken in rounds, transfers and merges between tables, and bill splitting. A kitchen display (KDS) replaces paper tickets: orders move from <strong>New</strong> to <strong>Preparing</strong> to <strong>Ready</strong>, so nothing is lost between the floor and the kitchen.</p>'),
                ('4. Menu portions and modifiers', '<p>Many UAE menus sell the same dish in sizes &mdash; quarter, half, full &mdash; or with add-ons. Make sure each portion can have its own price and that modifiers print on the kitchen ticket.</p>'),
                ('5. Inventory and recipes', '<p>Recipe-based inventory deducts ingredients as dishes are sold, so you can see stock levels, wastage and real food cost. Purchase orders and supplier records help you reorder before you run out.</p>'),
                ('6. Payments the way guests pay', '<p>Cash, card, split payments and change calculation are the minimum. Shift and register reports make cash-up at closing quick and accurate.</p>'),
                ('7. Arabic, support and data ownership', '<p>If your staff or customers prefer Arabic, check the interface and receipts. Ask who stores your data, how backups work, and what local support is available in Abu Dhabi, Dubai and the other emirates.</p>'),
                ('Quick checklist', '<ul><li>5% VAT on receipts and tax reports</li><li>Works without internet</li><li>Tables, rounds and bill splitting</li><li>Kitchen display</li><li>Portions, modifiers and recipe inventory</li><li>Cash, card and split payments</li><li>Arabic, local support and your own backups</li></ul>'),
            ],
            'cta': 'SELLO covers this checklist for restaurants, cafés and retail stores across the UAE.',
        },
        'ar': {
            'title': 'كيف تختار نظام نقاط البيع (كاشير) لمطعمك في الإمارات',
            'description': 'قائمة عملية للمطاعم والمقاهي في أبوظبي ودبي وجميع الإمارات: فواتير ضريبة القيمة المضافة، والفوترة دون إنترنت، وشاشة المطبخ، والطاولات، والمخزون.',
            'keywords': 'نظام نقاط البيع للمطاعم الإمارات, برنامج كاشير للمطاعم, برنامج كاشير أبوظبي, برنامج كاشير دبي, شاشة المطبخ, فاتورة ضريبية, برنامج مطاعم',
            'intro': 'نظام الكاشير في المطعم يفعل أكثر بكثير من طباعة الفواتير. في الإمارات يجب أن يُصدر فواتير متوافقة مع ضريبة القيمة المضافة، وأن يربط المطبخ بالصالة، وأن يستمر في العمل عند انقطاع الإنترنت. استخدم هذه القائمة قبل أن تختار.',
            'sections': [
                ('1. فواتير جاهزة لضريبة القيمة المضافة', '<p>ضريبة القيمة المضافة في الإمارات 5%. يجب أن يتيح لك النظام ضبط نسبة الضريبة مرة واحدة، وإظهارها بوضوح على كل إيصال، وطباعة بيانات نشاطك على الفواتير. تأكد من إمكانية اختيار أن تكون الأسعار شاملة للضريبة أو تُضاف عند الدفع، ومن تصدير تقارير الضريبة لمحاسبك.</p>'),
                ('2. يجب أن تستمر الفوترة عند انقطاع الإنترنت', '<p>الأنظمة السحابية فقط تتوقف لحظة انقطاع الاتصال &mdash; وغالبًا في وقت الذروة. ابحث عن نظام يعمل على شبكة متجرك أو يحفظ المبيعات على الجهاز ثم يزامنها لاحقًا. اسأل المزوّد مباشرة: <em>&laquo;هل أستطيع استلام الدفع دون إنترنت؟&raquo;</em></p>'),
                ('3. الطاولات والطلبات والمطبخ', '<p>للجلوس داخل المطعم تحتاج مخططًا للصالة مع حالة كل طاولة، وطلبات على دفعات، ونقل ودمج الطاولات، وتقسيم الفاتورة. وتستبدل شاشة المطبخ التذاكر الورقية: تنتقل الطلبات من <strong>جديد</strong> إلى <strong>قيد التحضير</strong> إلى <strong>جاهز</strong>، فلا يضيع شيء بين الصالة والمطبخ.</p>'),
                ('4. أحجام الأطباق والإضافات', '<p>تبيع كثير من القوائم في الإمارات الطبق نفسه بأحجام &mdash; ربع ونصف وكامل &mdash; أو مع إضافات. تأكد أن لكل حجم سعره، وأن الإضافات تُطبع على تذكرة المطبخ.</p>'),
                ('5. المخزون والوصفات', '<p>المخزون القائم على الوصفات يخصم المكونات عند بيع الأطباق، فترى مستويات المخزون والهدر والتكلفة الحقيقية. وتساعدك أوامر الشراء وسجلات الموردين على إعادة الطلب قبل النفاد.</p>'),
                ('6. الدفع كما يفضّل الضيوف', '<p>النقد والبطاقة والدفع المجزّأ وحساب الباقي هي الحد الأدنى. وتقارير الورديات والصناديق تجعل إغلاق اليوم سريعًا ودقيقًا.</p>'),
                ('7. العربية والدعم وملكية البيانات', '<p>إذا كان موظفوك أو عملاؤك يفضّلون العربية، فتحقق من الواجهة والإيصالات. واسأل أين تُحفظ بياناتك، وكيف يتم النسخ الاحتياطي، وما الدعم المحلي المتوفر في أبوظبي ودبي وبقية الإمارات.</p>'),
                ('قائمة سريعة', '<ul><li>ضريبة 5% على الإيصالات وتقارير الضريبة</li><li>يعمل دون إنترنت</li><li>الطاولات والدفعات وتقسيم الفاتورة</li><li>شاشة المطبخ</li><li>الأحجام والإضافات ومخزون الوصفات</li><li>النقد والبطاقة والدفع المجزّأ</li><li>العربية والدعم المحلي ونسخك الاحتياطية</li></ul>'),
            ],
            'cta': 'يغطي SELLO هذه القائمة للمطاعم والمقاهي ومتاجر التجزئة في جميع أنحاء الإمارات.',
        },
    },
    {
        'slug': 'pos-software-saudi-arabia',
        'date': '2026-10-04',
        'product': 'sello',
        'en': {
            'title': 'POS Software in Saudi Arabia: VAT, E-Invoicing and What to Check',
            'description': 'Choosing a POS system for a shop or restaurant in Riyadh, Jeddah or Dammam? What to check on 15% VAT, ZATCA e-invoicing, Arabic, offline billing and support.',
            'keywords': 'POS system Saudi Arabia, POS software KSA, POS Riyadh, POS Jeddah, cashier software Saudi, VAT POS Saudi Arabia, e-invoicing POS, Arabic POS',
            'intro': 'Saudi Arabia has its own rules for shops and restaurants: 15% VAT, mandatory electronic invoicing, and customers who expect Arabic. Here is what to check before you sign up for a POS in Riyadh, Jeddah, Dammam or anywhere in the Kingdom.',
            'sections': [
                ('1. 15% VAT on every sale', '<p>VAT in Saudi Arabia is 15%. Your POS must apply the right rate, show it on receipts, handle tax-inclusive and tax-exclusive prices, and give you tax reports for your filings.</p>'),
                ('2. E-invoicing (ZATCA / Fatoora)', '<p>Electronic invoicing is mandatory in Saudi Arabia and is being rolled out to businesses in phases by ZATCA. Requirements depend on your business and its phase, so ask any POS provider <strong>in writing</strong> how their system supports e-invoicing for your business, and check the official ZATCA guidance. Don&rsquo;t rely on a sales claim alone.</p>'),
                ('3. Arabic first', '<p>Staff and customers often prefer Arabic. Check the screens, receipts and reports in Arabic, including right-to-left layout and correct Arabic numerals and dates.</p>'),
                ('4. Billing that never stops', '<p>Choose a system that keeps selling during internet outages &mdash; running on the shop&rsquo;s own network or storing sales on the device &mdash; so a connection problem never closes the till.</p>'),
                ('5. Retail and restaurant features', '<p>Retail needs barcode scanning, stock, purchasing and suppliers. Restaurants need tables, a kitchen display, portions, modifiers and bill splitting. If you run both, look for one system with both modes.</p>'),
                ('6. Support, backups and data', '<p>Ask where your data is stored, how backups work, and how support reaches you in your city. Clear licensing &mdash; without surprise per-seat fees &mdash; matters as much as features.</p>'),
                ('Checklist', '<ul><li>15% VAT on receipts and reports</li><li>E-invoicing support confirmed in writing for your phase</li><li>Arabic screens and receipts</li><li>Works without internet</li><li>Retail and/or restaurant features you need</li><li>Backups, local support and clear pricing</li></ul>'),
            ],
            'cta': 'Talk to us about SELLO and SELLO Lite for shops and restaurants in Saudi Arabia, and ask us about your e-invoicing requirements.',
        },
        'ar': {
            'title': 'برنامج كاشير في السعودية: ضريبة القيمة المضافة والفوترة الإلكترونية وما يجب التحقق منه',
            'description': 'تختار نظام نقاط بيع لمتجر أو مطعم في الرياض أو جدة أو الدمام؟ ما يجب التحقق منه في ضريبة 15% والفوترة الإلكترونية (فاتورة) والعربية والفوترة دون إنترنت والدعم.',
            'keywords': 'برنامج كاشير السعودية, نظام نقاط البيع السعودية, برنامج كاشير الرياض, برنامج كاشير جدة, الفوترة الإلكترونية, فاتورة هيئة الزكاة, ضريبة القيمة المضافة 15%',
            'intro': 'للمتاجر والمطاعم في السعودية متطلبات خاصة: ضريبة قيمة مضافة 15%، وفوترة إلكترونية إلزامية، وعملاء يتوقعون اللغة العربية. إليك ما يجب التحقق منه قبل الاشتراك في نظام كاشير في الرياض أو جدة أو الدمام أو أي مكان في المملكة.',
            'sections': [
                ('1. ضريبة 15% على كل عملية بيع', '<p>ضريبة القيمة المضافة في السعودية 15%. يجب أن يطبّق النظام النسبة الصحيحة، ويُظهرها على الإيصالات، ويتعامل مع الأسعار الشاملة وغير الشاملة للضريبة، ويوفّر تقارير الضريبة لإقراراتك.</p>'),
                ('2. الفوترة الإلكترونية (هيئة الزكاة والضريبة والجمارك / فاتورة)', '<p>الفوترة الإلكترونية إلزامية في السعودية، وتُطبّقها الهيئة على المنشآت على مراحل. تختلف المتطلبات حسب منشأتك ومرحلتها، لذا اطلب من أي مزوّد نظام كاشير أن يوضّح <strong>كتابيًا</strong> كيف يدعم نظامه الفوترة الإلكترونية لمنشأتك، وراجع الإرشادات الرسمية للهيئة. لا تعتمد على وعود المبيعات وحدها.</p>'),
                ('3. العربية أولًا', '<p>كثيرًا ما يفضّل الموظفون والعملاء العربية. تحقق من الشاشات والإيصالات والتقارير بالعربية، بما في ذلك الواجهة من اليمين إلى اليسار والأرقام والتواريخ.</p>'),
                ('4. فوترة لا تتوقف', '<p>اختر نظامًا يستمر في البيع أثناء انقطاع الإنترنت &mdash; يعمل على شبكة المتجر أو يحفظ المبيعات على الجهاز &mdash; حتى لا تُغلق مشكلة اتصال الصندوق.</p>'),
                ('5. مزايا التجزئة والمطاعم', '<p>تحتاج التجزئة إلى الباركود والمخزون والمشتريات والموردين. وتحتاج المطاعم إلى الطاولات وشاشة المطبخ والأحجام والإضافات وتقسيم الفاتورة. وإذا كنت تدير الاثنين فابحث عن نظام واحد يدعم الوضعين.</p>'),
                ('6. الدعم والنسخ الاحتياطي والبيانات', '<p>اسأل أين تُحفظ بياناتك، وكيف يتم النسخ الاحتياطي، وكيف يصلك الدعم في مدينتك. ووضوح الترخيص &mdash; دون رسوم مفاجئة لكل مستخدم &mdash; لا يقل أهمية عن المزايا.</p>'),
                ('قائمة التحقق', '<ul><li>ضريبة 15% على الإيصالات والتقارير</li><li>دعم الفوترة الإلكترونية مؤكد كتابيًا لمرحلتك</li><li>شاشات وإيصالات بالعربية</li><li>يعمل دون إنترنت</li><li>مزايا التجزئة و/أو المطاعم التي تحتاجها</li><li>نسخ احتياطي ودعم محلي وأسعار واضحة</li></ul>'),
            ],
            'cta': 'تحدّث معنا عن SELLO و SELLO Lite للمتاجر والمطاعم في السعودية، واسألنا عن متطلبات الفوترة الإلكترونية لمنشأتك.',
        },
    },
    {
        'slug': 'automatic-school-bell-system',
        'date': '2026-10-04',
        'product': 'automatic-bell',
        'en': {
            'title': 'Automatic School Bell Systems: A Practical Guide for Schools',
            'description': 'How automatic school bells work, what features matter (timetables, holidays, manual ring, offline timekeeping) and how to choose one for your school or factory.',
            'keywords': 'automatic school bell, school bell system, school bell timer, automatic bell for schools UAE, school bell Saudi Arabia, period bell system, bell scheduler',
            'intro': 'Ringing period bells by hand ties up staff and leads to missed or late bells. An automatic bell controller rings on a timetable, skips holidays and can still be rung manually. Here is how they work and what to look for.',
            'sections': [
                ('How an automatic bell works', '<p>A small controller is wired into the existing bell circuit through a relay. It keeps time with a real-time clock, checks the saved timetable every minute, and switches the bell on for a set number of seconds when a period starts.</p>'),
                ('Features that matter', '<ul><li><strong>Daily timetable</strong> with enough bells for every period and break</li><li><strong>Weekends and holidays</strong> skipped automatically, including exam days</li><li><strong>Manual ring</strong> for assemblies, drills and emergencies</li><li><strong>Accurate offline timekeeping</strong> so power or WiFi cuts don&rsquo;t shift the schedule</li><li><strong>Phone app control</strong> so staff can change times without an electrician</li></ul>'),
                ('Wired timers vs app-controlled bells', '<p>Mechanical or basic digital timers need someone at the control box to change them and can&rsquo;t skip holidays. App-controlled systems let an administrator update the timetable, holidays and ring length from a phone, and see the next bell at a glance.</p>'),
                ('Installation', '<p>Installation usually means mounting the controller near the existing bell, wiring it into the bell&rsquo;s power circuit, joining it to the school WiFi and entering the timetable. After that, all changes are made from the app.</p>'),
                ('Not just schools', '<p>Factories, workshops and training centres use the same systems for shift changes and breaks.</p>'),
            ],
            'cta': 'See how our Automatic Bell works, with real screens from the app.',
        },
        'ar': {
            'title': 'أنظمة جرس المدرسة الآلي: دليل عملي للمدارس',
            'description': 'كيف تعمل أجراس المدارس الآلية، وما المزايا المهمة (الجداول، العطل، الرنين اليدوي، الوقت دون إنترنت)، وكيف تختار النظام المناسب لمدرستك أو مصنعك.',
            'keywords': 'جرس مدرسة آلي, نظام جرس المدرسة, جرس الحصص الآلي, مؤقت جرس المدرسة, جرس مدرسي ذكي, جرس مدرسة الإمارات, جرس مدرسة السعودية',
            'intro': 'قرع أجراس الحصص يدويًا يشغل الموظفين ويؤدي إلى أجراس فائتة أو متأخرة. أما وحدة الجرس الآلي فترنّ حسب الجدول، وتتخطّى العطل، ويمكن تشغيلها يدويًا عند الحاجة. إليك كيف تعمل وما الذي تبحث عنه.',
            'sections': [
                ('كيف يعمل الجرس الآلي', '<p>تُوصَل وحدة تحكم صغيرة بدائرة الجرس الحالية عبر مرحّل. تحافظ على الوقت بساعة حقيقية، وتتحقق من الجدول المحفوظ كل دقيقة، وتشغّل الجرس لعدد محدد من الثواني عند بدء الحصة.</p>'),
                ('المزايا المهمة', '<ul><li><strong>جدول يومي</strong> بعدد كافٍ من الأجراس لكل حصة واستراحة</li><li><strong>تخطّي العطل الأسبوعية والرسمية</strong> تلقائيًا، بما في ذلك أيام الاختبارات</li><li><strong>رنين يدوي</strong> للطابور الصباحي والتمارين والطوارئ</li><li><strong>وقت دقيق دون إنترنت</strong> حتى لا يتغيّر الجدول عند انقطاع الكهرباء أو WiFi</li><li><strong>تحكم من تطبيق الجوال</strong> ليعدّل الموظفون الأوقات دون كهربائي</li></ul>'),
                ('المؤقتات التقليدية مقابل الأجراس بالتطبيق', '<p>المؤقتات الميكانيكية أو الرقمية البسيطة تحتاج من يذهب إلى صندوق التحكم لتعديلها ولا تتخطّى العطل. أما الأنظمة المتحكم بها من التطبيق فتتيح للإدارة تحديث الجدول والعطل ومدة الرنين من الجوال، ومعرفة الجرس التالي بنظرة.</p>'),
                ('التركيب', '<p>يشمل التركيب عادةً تثبيت وحدة التحكم قرب الجرس الحالي، وتوصيلها بدائرة تغذية الجرس، وربطها بشبكة WiFi المدرسة، وإدخال الجدول. بعد ذلك تتم كل التعديلات من التطبيق.</p>'),
                ('ليس للمدارس فقط', '<p>تستخدم المصانع والورش ومراكز التدريب الأنظمة نفسها لتبديل الورديات والاستراحات.</p>'),
            ],
            'cta': 'شاهد كيف يعمل الجرس الآلي لدينا، مع شاشات حقيقية من التطبيق.',
        },
    },
    {
        'slug': 'water-tank-level-monitoring',
        'date': '2026-10-04',
        'product': 'water-monitoring',
        'en': {
            'title': 'Water Tank Overflow and Low-Level Alarms: How Tank Monitoring Works',
            'description': 'How a water tank level sensor works, why live level on your phone beats checking the roof, and how low-level and overflow alerts prevent dry tanks and wasted water.',
            'keywords': 'water tank level monitoring, water level sensor, tank overflow alarm, low water alarm, water level indicator, rooftop tank monitoring UAE, smart water tank',
            'intro': 'Rooftop and underground tanks are out of sight &mdash; until they overflow or run dry. A level sensor with phone alerts tells you what is happening in the tank at any moment.',
            'sections': [
                ('How the level is measured', '<p>A sensor mounted on the tank lid measures the distance to the water surface and converts it into a fill percentage. Readings are taken continuously, so the level on your phone rises and falls as the tank fills and empties.</p>'),
                ('Why alerts matter', '<p>Two thresholds cover most problems:</p><ul><li><strong>Low level</strong> (for example below 15%): the tank is nearly empty &mdash; refill before taps run dry.</li><li><strong>High level</strong> (for example above 95%): the tank is about to overflow &mdash; stop the water before it is wasted.</li></ul><p>Messaging apps such as Telegram deliver these alerts instantly to one or several phones.</p>'),
                ('Where it helps most', '<ul><li>Villas and homes with rooftop tanks</li><li>Apartment buildings with shared tanks</li><li>Farms and commercial sites with large or remote tanks</li></ul>'),
                ('What to check before installing', '<ul><li>Tank type and size (overhead or sump)</li><li>A stable WiFi or network connection near the tank</li><li>Who should receive alerts, and on which phones</li><li>The low and high thresholds that suit your usage</li></ul>'),
            ],
            'cta': 'See our Water Monitoring system: live level on your phone and Telegram alerts below 15% and above 95%.',
        },
        'ar': {
            'title': 'إنذار فيضان الخزان وانخفاض المياه: كيف تعمل مراقبة الخزانات',
            'description': 'كيف يعمل حسّاس منسوب خزان المياه، ولماذا يغنيك عرض المنسوب على جوالك عن الصعود إلى السطح، وكيف تمنع تنبيهات الانخفاض والفيضان فراغ الخزان وهدر المياه.',
            'keywords': 'مراقبة منسوب خزان المياه, حساس منسوب المياه, إنذار فيضان الخزان, إنذار انخفاض المياه, مؤشر منسوب الماء, خزان مياه ذكي, مراقبة خزان المياه الإمارات',
            'intro': 'خزانات الأسطح والخزانات الأرضية بعيدة عن الأنظار &mdash; حتى تفيض أو تفرغ. يخبرك حسّاس المنسوب مع تنبيهات الجوال بما يحدث في الخزان في أي لحظة.',
            'sections': [
                ('كيف يُقاس المنسوب', '<p>حسّاس مثبّت على غطاء الخزان يقيس المسافة إلى سطح الماء ويحوّلها إلى نسبة امتلاء. تُؤخذ القراءات باستمرار، فيرتفع المنسوب على جوالك وينخفض مع امتلاء الخزان وتفريغه.</p>'),
                ('لماذا التنبيهات مهمة', '<p>حدّان يغطيان معظم المشكلات:</p><ul><li><strong>منسوب منخفض</strong> (مثلًا أقل من 15%): الخزان أوشك على الفراغ &mdash; اِملأه قبل أن تجف الصنابير.</li><li><strong>منسوب مرتفع</strong> (مثلًا أكثر من 95%): الخزان على وشك الفيضان &mdash; أوقف المياه قبل أن تُهدر.</li></ul><p>تطبيقات المراسلة مثل تيليجرام توصل هذه التنبيهات فورًا إلى جوال أو أكثر.</p>'),
                ('أين يفيد أكثر', '<ul><li>الفلل والمنازل ذات الخزانات العلوية</li><li>البنايات السكنية ذات الخزانات المشتركة</li><li>المزارع والمواقع التجارية ذات الخزانات الكبيرة أو البعيدة</li></ul>'),
                ('ما يجب التحقق منه قبل التركيب', '<ul><li>نوع الخزان وحجمه (علوي أو أرضي)</li><li>اتصال WiFi أو شبكة مستقر قرب الخزان</li><li>من يجب أن يستقبل التنبيهات وعلى أي جوالات</li><li>حدّا الانخفاض والارتفاع المناسبان لاستهلاكك</li></ul>'),
            ],
            'cta': 'تعرّف على نظام مراقبة خزانات المياه لدينا: المنسوب مباشرة على جوالك وتنبيهات تيليجرام عند أقل من 15% وأكثر من 95%.',
        },
    },
]
