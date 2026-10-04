# Anqah Tech: SEO launch kit (off-site steps)

These steps need your own Google and Microsoft accounts, so only you can do them. Do them in this order after the site is live at https://www.anqah.com.

## 1. Google Search Console (most important)
1. Go to https://search.google.com/search-console and click **Add property**.
2. Choose **URL prefix** and enter `https://www.anqah.com/`.
3. Verify ownership with **HTML tag**. Send the `<meta name="google-site-verification" ...>` line to Claude, and it will be added to both home pages.
4. Open **Sitemaps** and submit `sitemap.xml`. It lists 20 pages: English and Arabic home, 4 products and 5 guides each.
5. Open **URL inspection**, paste each main URL and click **Request indexing**: home, `/ar/`, the 4 product pages and `/blog/`.

## 2. Google Business Profile (the map pack for "POS system Abu Dhabi")
Create it at https://business.google.com. Use **exactly** the same name, phone and address everywhere (NAP consistency):

| Field | Value |
|---|---|
| Business name | Anqah Tech |
| Category (primary) | Software company |
| Categories (additional) | Computer support and services · Point of sale equipment supplier · Website designer · Security system installer |
| Phone | +971 50 239 3703 |
| Website | https://www.anqah.com/ |
| Hours | Mon–Sat 09:00–19:00 |
| Service areas | Abu Dhabi, Dubai, Sharjah, Al Ain, Riyadh, Jeddah, Dammam |

**Description (English, under 750 chars):**
> Anqah Tech is an Abu Dhabi technology company building POS software and smart IoT systems for businesses, schools and homes. Our products include SELLO, a POS system for restaurants, cafés and retail stores; SELLO Lite, an offline mobile POS app; an Automatic School Bell controlled from your phone; and Water Tank Monitoring with live levels and Telegram alerts. We also provide web development, mobile apps, CCTV, home automation and IT infrastructure across the UAE, Saudi Arabia and India.

**الوصف (العربية):**
> Anqah Tech شركة تقنية في أبوظبي تطوّر برامج نقاط البيع وأنظمة إنترنت الأشياء الذكية للشركات والمدارس والمنازل. من منتجاتنا SELLO نظام كاشير للمطاعم والمقاهي ومتاجر التجزئة، و SELLO Lite تطبيق كاشير للجوال يعمل دون إنترنت، والجرس المدرسي الآلي المتحكم به من الجوال، ونظام مراقبة خزانات المياه مع المنسوب المباشر وتنبيهات تيليجرام. كما نقدّم تطوير المواقع وتطبيقات الجوال وكاميرات المراقبة وأتمتة المنازل والبنية التحتية لتقنية المعلومات في الإمارات والسعودية والهند.

Then:
- Add **products** in the profile (SELLO, SELLO Lite, Automatic Bell, Water Monitoring), each linking to its product page.
- Upload **real photos**: the office, installations, the team and screenshots.
- Each time a guide is published, add a **Post** that links to it.

## 3. Reviews
Reviews are the strongest map-pack signal. After every installation, send the customer the review link from your Business Profile (**Ask for reviews**), for example on WhatsApp. Reply to every review. Never buy reviews; Google removes them and can suspend the profile.

## 4. Bing Webmaster Tools (also feeds ChatGPT search and DuckDuckGo)
Go to https://www.bing.com/webmasters, choose **Import from Google Search Console**, and confirm that `sitemap.xml` is listed.

## 5. Directory listings (same name, phone and address on every one)
- **UAE:** Yellow Pages UAE (yellowpages.ae), Connect.ae, Dubizzle Services
- **Saudi Arabia:** Yellow Pages KSA (yellowpages-sa.com), Daleeli
- **India:** Justdial, IndiaMART, Sulekha
- **Software / B2B:** Clutch, GoodFirms, Capterra and G2 (list SELLO as a product), LinkedIn company page
- **SELLO Lite:** link the Google Play listing to https://www.anqah.com/products/sello-lite.html

## 6. Keep publishing
Add one guide a month in `tools/blog_content.py`, then run:
```
python tools/build_blog.py
python tools/build_sitemap.py
python tools/audit_seo.py
```
Topic ideas: POS for supermarkets in Sharjah · POS software for restaurants in India (GST) · Barcode scanner and printer setup · Restaurant kitchen display explained · Smart home automation in Abu Dhabi villas · CCTV for small shops in UAE.

## Before going live: please check
- **Arabic text:** have a native speaker proofread `ar/` and the Arabic in `tools/blog_content.py`.
- **Saudi e-invoicing:** the guide deliberately does not claim SELLO is ZATCA-certified. If it is, tell Claude and the claim will be added.
- **SELLO Lite screenshots** show ₹ prices. That's fine for India, but UAE and KSA visitors may want AED/SAR screenshots.
- **Bell images** are AI-generated. Replace them with real installation photos when you have them; real photos also help image search.
