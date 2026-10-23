"""Builds the bilingual site: /, /guide/, /ja/, /ja/guide/. Usage (from the repo root): python3 tools/build.py ."""
import html, os, sys, urllib.parse

ROOT = sys.argv[1]
e = html.escape
FORM = "https://tally.so/r/PRdXZd"

def maps(q, pid):
    return "https://www.google.com/maps/search/?" + urllib.parse.urlencode({"api": "1", "query": q, "query_place_id": pid})

CSS = """
:root { --bg:#FBF6EC; --ink:#1B2238; --sub:#4A4E63; --muted:#5E6377; --navy:#1F2A4A; --gold:#F2C766; --rust:#A84A27; --line:#EADFCB; --card:#FFFFFF; }
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; background: var(--bg); color: var(--ink); font-family: 'Zen Maru Gothic', system-ui, sans-serif; font-size: 16px; line-height: 1.65; -webkit-text-size-adjust: 100%; }
a { color: var(--rust); }
.wrap { max-width: 680px; margin: 0 auto; padding: 0 16px; }
header.top { background: var(--navy); color: var(--bg); border-radius: 0 0 28px 28px; padding: 18px 0 28px; }
.bar { display: flex; justify-content: flex-end; margin-bottom: 14px; }
a.lang { display: inline-flex; align-items: center; min-height: 40px; padding: 0 14px; border: 1px solid #7A84A6; border-radius: 999px; color: var(--bg); text-decoration: none; font-size: 14px; font-weight: 700; }
.tagline { margin: 0 0 18px; font-family: 'Zen Old Mincho', serif; font-size: 20px; line-height: 1.4; font-weight: 700; color: var(--bg); }
.kicker { margin: 0; font-size: 13px; letter-spacing: 3px; font-weight: 700; color: var(--gold); }
h1 { margin: 4px 0 10px; font-family: 'Zen Old Mincho', serif; font-size: clamp(32px, 9vw, 40px); line-height: 1.2; color: var(--bg); }
.lede { margin: 0 0 10px; color: #D4D1C8; }
.fact { margin: 16px 0 0; padding-top: 12px; border-top: 1px solid #3A4568; font-size: 14px; font-weight: 700; color: var(--bg); }
a.btn { display: inline-flex; align-items: center; min-height: 48px; padding: 0 22px; border-radius: 999px; background: var(--gold); color: var(--navy); font-weight: 700; text-decoration: none; margin-top: 16px; }
nav.jump { position: sticky; top: 0; z-index: 5; background: var(--bg); border-bottom: 1px solid var(--line); }
nav.jump ul { list-style: none; margin: 0 auto; padding: 10px 16px; max-width: 680px; display: flex; gap: 8px; overflow-x: auto; }
nav.jump a { display: inline-flex; align-items: center; white-space: nowrap; text-decoration: none; color: var(--ink); background: var(--card); border: 1px solid var(--line); border-radius: 999px; padding: 0 14px; font-size: 15px; font-weight: 700; min-height: 40px; }
section.part { padding: 28px 0 6px; scroll-margin-top: 64px; }
.label { margin: 0 0 6px; font-size: 12px; letter-spacing: 3px; font-weight: 700; color: var(--rust); }
h2 { margin: 0 0 10px; font-family: 'Zen Old Mincho', serif; font-size: 26px; line-height: 1.3; }
p { margin: 0 0 12px; }
main p, main li { color: var(--sub); }
.sub { color: var(--sub); }
.small, .note, .foot { font-size: 14px; color: var(--muted); }
main .small, main .note, main .foot { color: var(--muted); }
h3 { margin: 22px 0 10px; font-size: 14px; letter-spacing: 3px; text-transform: uppercase; color: var(--rust); display: flex; align-items: center; gap: 8px; }
.dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; flex: none; }
ul.places { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 10px; }
li.place, .card, .plan { background: var(--card); border: 1px solid var(--line); border-radius: 16px; }
li.place { padding: 12px 16px 14px; }
a.pl { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 10px; text-decoration: none; color: var(--ink); min-height: 44px; }
.nm { font-size: 18px; font-weight: 700; }
.tag { font-size: 12px; font-weight: 700; color: var(--rust); border: 1px solid #C9A38F; border-radius: 999px; padding: 1px 8px; }
.go { margin-left: auto; font-size: 14px; font-weight: 700; color: var(--rust); }
.desc { margin: 2px 0 0; color: var(--sub); }
.info { margin: 4px 0 0; font-size: 14px; font-weight: 700; color: var(--muted); }
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 10px; }
.card { padding: 14px 16px; }
.w { margin: 0; display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 10px; }
.ro { font-family: 'Zen Old Mincho', serif; font-size: 21px; font-weight: 700; }
.ja { font-size: 16px; color: var(--muted); }
.me { margin: 4px 0 0; color: var(--sub); }
ul.small-list { background: var(--card); border: 1px solid var(--line); border-radius: 16px; margin: 0; padding: 14px 16px 14px 34px; display: flex; flex-direction: column; gap: 8px; color: var(--sub); }
.allergy { background: var(--card); border: 2px dashed #C9A38F; border-radius: 16px; padding: 16px; }
.allergy .head { margin: 0 0 4px; font-size: 22px; font-weight: 700; }
.allergy .head .en { display: block; font-size: 15px; font-weight: 400; color: var(--muted); }
.chks { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 4px 12px; margin: 12px 0 8px; }
label.chk { display: flex; align-items: center; gap: 10px; min-height: 44px; cursor: pointer; }
label.chk input { width: 24px; height: 24px; flex: none; accent-color: var(--navy); }
label.chk .jp { font-size: 19px; font-weight: 700; }
label.chk .en { font-size: 14px; color: var(--muted); }
.plan { padding: 18px; margin: 14px 0; }
.plan .meta { margin: 0 0 4px; font-size: 12px; letter-spacing: 2px; font-weight: 700; color: var(--muted); }
.plan h3 { margin: 0 0 8px; font-family: 'Zen Old Mincho', serif; font-size: 21px; letter-spacing: 0; text-transform: none; color: var(--ink); }
.price { margin: 10px 0 4px; font-size: 19px; font-weight: 700; color: var(--ink) !important; }
.price span { font-size: 15px; font-weight: 400; color: var(--muted); }
.two { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; margin-top: 12px; }
.opt { border-top: 1px solid var(--line); padding-top: 12px; }
.opt h4 { margin: 0 0 6px; font-family: 'Zen Old Mincho', serif; font-size: 18px; color: var(--ink); }
ul.list { margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 10px; color: var(--sub); }
.ph { display: none; margin: 12px 0; height: 200px; border: 2px dashed #C9A38F; border-radius: 16px; background: #F3EBDB; align-items: center; justify-content: center; text-align: center; padding: 12px; }
.ph span { font-size: 14px; font-weight: 700; letter-spacing: 1px; color: var(--rust); }
.draft .ph { display: flex; }
.book { background: var(--navy); color: var(--bg); border-radius: 20px; padding: 24px 20px; margin: 30px 0 0; }
.book h2 { color: var(--bg); }
.book p { color: #D4D1C8 !important; }
.book .small { color: #B8B5AC !important; margin-top: 14px; }
:lang(ja) h1, :lang(ja) h2, :lang(ja) .tagline, :lang(ja) .lede, :lang(ja) .fact { word-break: auto-phrase; }
footer { padding: 24px 0 40px; font-size: 14px; color: var(--muted); }
"""

def head(lang, title, desc):
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{title}</title>
<meta name="description" content="{desc}">
<script>try{{if(new URLSearchParams(location.search).has('draft'))document.documentElement.classList.add('draft')}}catch(_){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;700&amp;family=Zen+Old+Mincho:wght@700&amp;display=swap">
<style>{CSS}</style>
</head>
<body>
"""

def langbtn(href, lang):
    label = "日本語" if lang == "en" else "English"
    hl = "ja" if lang == "en" else "en"
    return f'<div class="bar"><a class="lang" href="{href}" hreflang="{hl}" lang="{hl}">{label}</a></div>'

def ph(label):
    return f'<figure class="ph" aria-hidden="true"><span>{e(label)}</span></figure>'

def ul(items, cls="list"):
    return f'<ul class="{cls}">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"

FOOT = '<footer class="wrap"><p>Ikitsuke · Kai &amp; Maya · Kichijoji, Tokyo</p></footer>\n</body>\n</html>\n'

# ---------------------------------------------------------------- top page
TOP = {
 "en": dict(
  title="Ikitsuke · A night at our regular places in Kichijoji",
  brand="Ikitsuke", tagline="A night at our regular places in Kichijoji",
  desc="Kai &amp; Maya take small groups to their regular bars and restaurants in Kichijoji and Mitaka, Tokyo.",
  kicker="KICHIJOJI &amp; MITAKA · WITH LOCALS",
  h1="A night at the places we call our own.",
  ledes=["Not a tour. More like a friend taking you to their regular places.",
         "For your first trip to Tokyo, or your tenth. Small bars and restaurants that are hard to walk into on your own, with one or both of us, locals who are regulars there."],
  fact="For 2–4 adults (20+) · from ¥30,000 per person, all in",
  cta="Tell us about your night",
  ph=["PHOTO · a toast at the counter", "PHOTO · Kai & Maya", "PHOTO · izakaya, then a small bar", "PHOTO · our favorite izakaya", "PHOTO · sushi counter (after the shop's OK)", "PHOTO · charcoal-grill French (after the shop's OK)"],
  hosts_label="YOUR HOSTS",
  hosts="We are a married couple who have lived in Kichijoji for 15 years. One izakaya changes its menu every day, so we are there about three nights a week. A friend from the Netherlands once made time on a Tokyo business trip just to come back to it. At a family-run Chinese restaurant nearby, Maya chats with the family in Chinese. We sit at the counter when there is room, introduce you to the owners, and help you talk with them.",
  hosts_sub="Why you won't find them on your own: phone-only reservations, Japanese-only menus, doors that are easy to miss.",
  ways_label="WAYS TO SPEND THE EVENING",
  ways_h="Private, unhurried, and all taken care of.",
  ways="Just your group of 2 to 4, all 20 or older, at small places, many of which take phone bookings only. Food and two to three drinks at every place, booking, and your hosts all evening are in the price. No booking fees, no tips. We can't offer vegetarian, vegan, halal or allergy-safe meals.",
  casual=("2 STOPS · 3 HRS · 2–3 GUESTS", "Casual Night", "For example, dinner at a neighborhood izakaya, then a small bar to finish the night. We order for you, introduce the owners, and help you talk with them whenever you like.", "¥30,000 per person", "about US$190", "All in: food and drinks at both places, booking, and your hosts all evening"),
  usual=("3 STOPS · 4 HRS · 2–4 GUESTS", "Our Usual Night", "For example, Japanese craft gin at a cozy local pub, small home-style dishes, then sake and seasonal food at our favorite izakaya.", "¥35,000 per person", "about US$220", "All in: food and drinks at all three places, booking, and your hosts all evening"),
  combos="Many other combinations are possible, such as a pub with plenty of whisky, craft beer, or a bistro with good wine; we pick the stops to match what you like, within the evenings and prices above. Wine lovers: we can build an evening around wine, though not every stop will be a wine bar. Rum lovers can make their last stop a bar with over 500 rums, opened in 1997 by the founder of the Japan Rum Association.",
  long=("ONE PLACE · 3 HRS · 2 OR 4 GUESTS · LUNCH TOO", "One Long Dinner", "Both counters are run by couples who love to talk. You watch them cook right in front of you, often after they show you the ingredients, and we stay with you to translate whenever they have a moment to chat. Come as two and you sit among the regulars; come as four and the counter is all yours. On weekends, lunch works too."),
  sushi=("SUSHI", "A cozy counter in Mitaka, with fresh and aged fish from Toyosu. Plates like hairy crab and shirako tempura, served to suit each of you, then sushi you each pick piece by piece, off the menu we arrange with the chef.", "¥40,000 per person", "about US$255", "Includes: about 13 small plates and sushi each, a beer and about 360 ml of sake each"),
  french=("FRENCH", "A charcoal grill in Kichijoji, known for seasonal game. A course might bring Nagano-made cured ham, a starter, soup, a main you choose, then dessert or, like us, cheese and more Burgundy.", "¥50,000 per person", "about US$320", "Includes: the course and wine pairing"),
  long_foot="All in, both: booking and your hosts all evening (we pay for our own meal). Anything extra? Pay the difference at the shop.",
  inc_label="INCLUDED", book_label="WHEN YOU BOOK", notes_label="GOOD TO KNOW",
  included=["At each place, a first drink together: we help you order and tell you about the shop and its owners. Your food and drinks stay covered all evening; after that first drink, we pay for our own",
   "Your hosts close by all evening",
   "Dinner and drinks at every stop, about two to three drinks per place: beer, highballs, sake, cocktails and more from the regular menu",
   "Photos of your night, where the shop allows and with the OK of anyone in them",
   "We settle the bill at each stop",
   "A pocket booklet of bar words and manners to take home"],
  booking=["Book at least 7 days ahead. Pay by card in advance, but only after we've talked it through with you by email or messages and your date is set; then we send a payment link. Free cancellation until two days before; the day before or on the day, the full price is charged. These small shops turn other guests away to hold your seats",
   "If we have to cancel, you get a full refund. If a shop has to cancel, we suggest another; if that doesn't suit you, we refund in full",
   "Photos of your group are welcome. Please don't film or post the shops or owners for content, reviews or collaborations; these are regulars' places. There are no free or discounted spots"],
  notes=["At each place, the first drink is at your table. After that, on Casual and Usual Nights, it's your choice, depending on seating: we stay at your table, or sit close by so you can enjoy your own evening. Wave us over anytime, for example to talk with the owner.",
   "On Casual and Usual Nights, we meet you at Kichijoji Station around 6 pm, walk between places, and finish by 9 or 10 pm. For One Long Dinner, we wait for you outside the shop; beforehand we send a card with its name and address in Japanese to show a taxi driver. Kichijoji is about 15 minutes from Shinjuku on the JR Chuo Line; getting there is not included. Either One Long Dinner can also be a weekend lunch",
   "Order what you like, or let the shop choose. Beyond about two to three drinks per place, or for a pricier drink, you pay the difference at the shop; they'll tell you before pouring. As a guide, a drink is about ¥700–1,500 at izakaya and ¥1,500–2,500 at bars; rare whiskies or rums can cost more",
   "Not drinking? The price is the same; the shop makes it up with extra food or soft drinks. Everyone in your group must still be 20 or older, Japan's drinking age",
   "Casual and Usual Nights mean walking between places, and some are up a flight of stairs. If walking or stairs are hard for you, One Long Dinner is the easier choice: one place, no stairs, and you can take a taxi to the door. Tell us either way",
   "Our shops have small, shared kitchens, so we can't offer vegetarian, vegan, halal or allergy-safe meals, even partly. Simple dislikes, like sea urchin or raw oysters? Tell us, and we'll order around them"],
  book_h="Interested? Tell us about your night.",
  book_p="A short form: dates, group size, which evening, foods you avoid, what you're in the mood for, and how you'd like us to reach you (email, LINE or Instagram). We usually reply within two days. Just have a question? Use the same form.",
  book_btn="Open the form",
  book_small="Or ask the friend who shared this with you. Hosted in English.",
 ),
 "ja": dict(
  title="Ikitsuke（行きつけ）· 吉祥寺の、私たちの行きつけで過ごす夜",
  brand="Ikitsuke（行きつけ）", tagline="吉祥寺の、私たちの行きつけで過ごす夜",
  desc="吉祥寺・三鷹で、KaiとMayaが少人数のグループを行きつけのバーや飲食店へご案内します。",
  kicker="吉祥寺・三鷹　地元の常連と",
  h1="私たちの行きつけで過ごす夜。",
  ledes=["友人に行きつけの店へ連れていってもらうような夜です。観光ツアーとは違います。",
         "初めての東京にも、10回目の東京にも。一人では入りにくい小さなバーや飲食店へ、そこの常連である私たち（一人か二人）がご案内します。"],
  fact="2〜4人・全員20歳以上・1人30,000円から、すべて込み",
  cta="希望を伝える",
  ph=["写真：カウンターで乾杯", "写真：KaiとMaya", "写真：居酒屋と小さなバー", "写真：お気に入りの居酒屋", "写真：鮨のカウンター（お店の了承後）", "写真：炭火焼きフレンチ（お店の了承後）"],
  hosts_label="案内する二人",
  hosts="吉祥寺に住んで15年の夫婦です。ある居酒屋はメニューが毎日変わるので、週に3回ほど通っています。オランダに住む友人は、東京出張の合間に時間を作って、わざわざこの店に戻ってきました。近所の家族経営の中華料理店では、Mayaがお店の家族と中国語で話します。空いていればカウンターに座り、お客さんを店主に紹介して、会話を手伝います。",
  hosts_sub="旅行者だけでは見つけにくいお店です。予約は電話だけ、メニューは日本語だけ、入口も見落としやすいからです。",
  ways_label="夜の過ごし方",
  ways_h="自分たちだけのグループで、急がず、すべてお任せで。",
  ways="2〜4人、全員20歳以上のお客さんのグループだけで、電話予約が中心の小さな店へ。各店の料理と2〜3杯のお酒、予約、ひと晩じゅうの案内まで料金に含まれます。予約料とチップはかかりません。ベジタリアン、ヴィーガン、ハラール、アレルギー対応の食事はできません。",
  casual=("2軒・3時間・2〜3人", "気軽な夜", "例えば、近所の居酒屋で夕食をとり、締めは小さなバーで。注文は私たちが代わりにして、店主を紹介します。店主と話したいときは、いつでも通訳します。", "1人30,000円", "約190米ドル", "すべて込み：2軒分の料理とお酒、予約、ひと晩の案内"),
  usual=("3軒・4時間・2〜4人", "いつもの夜", "例えば、落ち着いた地元のパブで国産クラフトジン、小皿の家庭料理、最後はお気に入りの居酒屋で日本酒と季節の料理を楽しみます。", "1人35,000円", "約220米ドル", "すべて込み：3軒分の料理とお酒、予約、ひと晩の案内"),
  combos="ウイスキーの多いパブ、クラフトビール、ワインのおいしいビストロなど、ほかにも多くの組み合わせがあります。上の料金とプランの範囲で、お客さんの好みに合わせて店を選びます。ワインが好きなら、ワインを中心にした夜も組めます（すべての店がワインバーとはいきません）。ラムが好きなら、締めの1軒を、日本ラム協会を設立した人が1997年に開いた、500種類以上のラムがそろうバーにできます。",
  long=("1軒・3時間・2人、または4人で貸切・昼も可", "一軒でじっくり", "どちらも、話好きのご夫婦が営むカウンターです。目の前で料理をつくるところが見られ、つくる前に素材を見せてくれることもあります。私たちも最後まで同席し、店主夫婦と話せるときは通訳します。2人なら常連さんと並んで、4人ならカウンターを貸切にして楽しめます。土日は昼も可能です。"),
  sushi=("鮨", "三鷹のアットホームな鮨カウンター。豊洲の新鮮なネタと熟成ネタで、毛ガニや白子の天ぷらなどのつまみを1人ずつ食べやすく。鮨は一貫ずつ好きなネタで。メニューにない頼み方を、私たちが大将にお願いします。", "1人40,000円", "約255米ドル", "内容：1人あたりつまみと鮨あわせて13品ほど、ビール1杯と日本酒2合ほど"),
  french=("フレンチ", "吉祥寺の気軽な炭火焼きフレンチ。季節のジビエが看板です。コースの一例は、長野の生ハム「掬月」、季節の前菜、スープ、選べるメイン、デザート。私たちのように、デザートをチーズに替えてブルゴーニュ中心のワインを飲み続けることもできます。", "1人50,000円", "約320米ドル", "内容：コースとワインペアリング"),
  long_foot="すべて込み（共通）：予約、ひと晩の案内（私たちの食事代は自分たちで払います）。追加の分は、差額をお店に直接お支払いください。",
  inc_label="料金に含まれるもの", book_label="予約のとき", notes_label="知っておいてほしいこと",
  included=["各店で、最初の一杯は一緒に。注文を手伝い、お店と店主を紹介します。お客さんの飲食は最後まで料金に含まれます。私たちの分は、最初の一杯のあとは自分たちで払います",
   "ひと晩、案内役がすぐそばにいます",
   "どの店でも食事と飲み物。1軒あたり2〜3杯ほどで、ビール、ハイボール、日本酒、カクテルなど、いつものメニューから選べます",
   "その夜の写真。お店が許す範囲で、写る人の了承をもらって撮ります",
   "各店の会計は私たちが済ませます",
   "持ち帰り用の、お酒の席の言葉とマナーの小冊子"],
  booking=["7日以上先の日程でお申し込みください。カードで前払いです。メールやメッセージでやり取りして日程が決まってから、支払い用のリンクをお送りします。2日前までのキャンセルは無料、前日と当日は全額をいただきます。小さな店なので、ほかのお客さんを断って席を空けてもらっているためです",
   "私たちの都合で中止するときは、全額を返金します。お店の都合のときは別の店をご提案し、合わなければ全額を返金します",
   "皆さん同士の写真は歓迎です。お店や店主を、発信・口コミ・コラボ用に撮影・投稿するのはご遠慮ください。常連の店だからです。無料・割引の枠はありません"],
  notes=["各店で、最初の一杯は同じ席で。そのあとは、気軽な夜といつもの夜なら選べます（席の空き具合によります）。同じ席にいることも、皆さんだけの時間を楽しめるよう、すぐ近くの席に移ることもできます。店主と話したいときなど、いつでも呼んでください",
   "気軽な夜といつもの夜は、18時ごろに吉祥寺駅で待ち合わせ、歩いて店を回って、21〜22時に解散します。一軒でじっくりは、店の前でお待ちしています。前もって店名と住所を日本語で書いたカードをお送りするので、タクシーの運転手に見せてください。吉祥寺は新宿からJR中央線で約15分です（ここまでの交通費は含みません）。一軒でじっくりは、土日なら昼も可能です",
   "お酒は、好きなものを頼むか、お店に選んでもらえます。1軒2〜3杯を超える分や、高いお酒の差額は、お店で直接お支払いください。超えるときは、注ぐ前にお店が教えてくれます。目安は1杯、居酒屋で700〜1,500円、バーで1,500〜2,500円ほどです。希少なウイスキーやラムは、もっと高いこともあります",
   "お酒を飲まない方も料金は同じです。そのぶん、料理やソフトドリンクでお店が調整します。ただし、飲まない方も含めて参加は20歳以上に限ります（日本の飲酒年齢です）",
   "気軽な夜といつもの夜は店から店へ歩き、階段を上がる店もあります。歩くのや階段がつらい方には、一軒でじっくりが向いています。1軒だけで階段がなく、店の前までタクシーで行けます。気になることがあれば教えてください",
   "どの店も調理場が小さく共通なので、ベジタリアン、ヴィーガン、ハラール、アレルギー対応の食事は、一部でも用意できません。ウニや生ガキが苦手、といった好き嫌いなら、教えてもらえれば避けて注文します"],
  book_h="興味があれば、希望を教えてください。",
  book_p="下のボタンから、短いフォームに入力してください。希望日、人数、プラン、食べられないもの、その日の気分、連絡方法（メール、LINE、Instagram）を伺います。たいてい2日以内に、私たちから連絡します。質問だけの場合も、同じフォームからどうぞ。",
  book_btn="フォームを開く（英語）",
  book_small="これを送ってくれた友人に聞いても構いません。案内は英語です。",
 ),
}

def plan_block(p, phl):
    meta, h, desc, price, usd, small = p
    return (f'<div class="plan"><p class="meta">{e(meta)}</p><h3>{e(h)}</h3>{ph(phl)}<p class="sub">{e(desc)}</p>'
            f'<p class="price">{e(price)} <span>· {e(usd)}</span></p><p class="small">{e(small)}</p></div>')

def opt_block(o, phl):
    h, desc, price, usd, small = o
    return (f'<div class="opt"><h4>{e(h)}</h4>{ph(phl)}<p class="sub">{e(desc)}</p>'
            f'<p class="price">{e(price)} <span>· {e(usd)}</span></p><p class="small">{e(small)}</p></div>')

def top_page(lang, other):
    T = TOP[lang]; P = T["ph"]
    ledes = "".join(f'<p class="lede">{e(l)}</p>' for l in T["ledes"])
    meta, h, desc = T["long"]
    return head(lang, T["title"], T["desc"]) + f"""<header class="top">
<div class="wrap">
{langbtn(other, lang)}
<h1>{e(T["brand"])}</h1>
<p class="tagline">{e(T["tagline"])}</p>
{ledes}
<p class="fact">{e(T["fact"])}</p>
<a class="btn" href="#book">{e(T["cta"])}</a>
</div>
</header>
<main class="wrap">
{ph(P[0])}
<section class="part">
<p class="label">{e(T["hosts_label"])}</p>
<h2>Kai &amp; Maya</h2>
{ph(P[1])}
<p>{e(T["hosts"])}</p>
<p class="sub">{e(T["hosts_sub"])}</p>
</section>
<section class="part">
<p class="label">{e(T["ways_label"])}</p>
<h2>{e(T["ways_h"])}</h2>
<p class="sub">{e(T["ways"])}</p>
{plan_block(T["casual"], P[2])}
{plan_block(T["usual"], P[3])}
<p class="small">{e(T["combos"])}</p>
<div class="plan"><p class="meta">{e(meta)}</p><h3>{e(h)}</h3><p class="sub">{e(desc)}</p>
<div class="two">{opt_block(T["sushi"], P[4])}{opt_block(T["french"], P[5])}</div>
<p class="small">{e(T["long_foot"])}</p></div>
</section>
<section class="part"><p class="label">{e(T["inc_label"])}</p>{ul(T["included"])}</section>
<section class="part"><p class="label">{e(T["book_label"])}</p>{ul(T["booking"])}</section>
<section class="part"><p class="label">{e(T["notes_label"])}</p>{ul(T["notes"])}</section>
<section class="book" id="book">
<h2>{e(T["book_h"])}</h2>
<p>{e(T["book_p"])}</p>
<a class="btn" href="{FORM}" target="_blank" rel="noopener">{e(T["book_btn"])}</a>
<p class="small">{e(T["book_small"])}</p>
</section>
</main>
""" + FOOT

# ---------------------------------------------------------------- guide page
COLORS = {"dinner": "#C25A2E", "beer": "#3E8EC4", "tachi": "#B07A1E", "bars": "#23305C", "ramen": "#8E4C78", "udon": "#2B7A78", "cafe": "#7A5230", "walk": "#3E7046"}
CATNAME = {
 "en": {"dinner": "Dinner", "beer": "Pubs", "tachi": "Tachinomi &amp; casual", "bars": "Bars", "ramen": "Ramen", "udon": "Udon", "cafe": "Cafes", "walk": "Walk around"},
 "ja": {"dinner": "食事", "beer": "パブ", "tachi": "立ち飲み・気軽な店", "bars": "バー", "ramen": "ラーメン", "udon": "うどん", "cafe": "カフェ・喫茶店", "walk": "散歩"},
}
BARFOOT = {"en": "All three are in the Kichijoji Bar Map, if you want to keep going.", "ja": "3軒とも吉祥寺バーマップに載っています。"}

# key, place_id, en(name, desc, tag, info), ja(name, desc, tag, info)
PLACES = [
 ("dinner", "ChIJ10Pt_0fuGGARuToFYjbttz0", ("Hanamichi", "A sake-focused izakaya run by a couple; the menu changes daily.", "", "¥¥¥ · From 18:30 · Closed Sun, Mon · Cash only · 2F"), ("花道", "日本酒が中心の、夫婦で営む居酒屋。メニューは毎日変わります。", "", "¥¥¥・18:30から・日・月休み・現金のみ・2階")),
 ("dinner", "ChIJEcqBWLPvGGAR3CuPMquh1Kk", ("Yoin", "Obanzai (small home-style dishes) from a couple, in wigtown's building.", "", "¥¥ · From 17:00 (Sat, Sun 15:00) · Closed Mon · Card OK"), ("よいん", "夫婦で営むおばんざいの店。wigtownと同じビルにあります。", "", "¥¥・17:00から（土日は15:00）・月曜休み・カード可")),
 ("dinner", "ChIJf6VSBUnuGGARfj6BNB4xdNg", ("Kujirayama", "A small izakaya with every kind of drink. Welcome even on your own.", "", "¥¥ · From 17:00 · Closed Sun · Card OK · 2F"), ("くじら山", "お酒の種類がそろった小さな居酒屋。お客さんだけで行っても歓迎してくれます。", "", "¥¥・17:00から・日曜休み・カード可・2階")),
 ("dinner", "ChIJ6fGsvDjuGGARTdf4Vw_gpeU", ("Andu", "A bistro strong on Burgundy wine. Welcome even on your own.", "", "¥¥¥ · From 18:00 · Closed Sun · Card OK"), ("アンドゥー", "ブルゴーニュワインに強いビストロ。お客さんだけで行っても歓迎してくれます。", "", "¥¥¥・18:00から・日曜休み・カード可")),
 ("dinner", "ChIJH6MaBUjuGGARSUsV5CIdHe0", ("Kissho Saikan", "Homestyle Chinese, run by a family.", "", "¥¥ · From 11:00 · Open daily · Card OK · 3F"), ("吉祥菜館", "家族で営む、家庭的な中華料理。", "", "¥¥・11:00から・毎日営業・カード可・3階")),
 ("dinner", "ChIJR7bDwJ7vGGARxRuSkxG2EmA", ("Pétillant", "A charcoal-grill French counter with a strong wine list, for a special night.", "", "¥¥¥ · Lunch 11:30, dinner 17:00 · Irregular days off"), ("ペティヤン", "炭火焼きが中心のカウンターフレンチ。ワインも豊富で、特別な夜に。", "", "¥¥¥・昼11:30、夜17:00から・不定休")),
 ("dinner", "ChIJXxyoCrDvGGARGxQYtLLL0hI", ("Sushi Shigeno", "A small sushi counter in Mitaka, one stop west. Sushi and small dishes, with about ten sakes.", "", "¥¥¥ · From 17:00 · Closed Thu · Phone booking only"), ("鮨繁乃", "三鷹の小さな鮨店（吉祥寺から1駅）。鮨とつまみを自由に頼めて、日本酒は約10種類。", "", "¥¥¥・17:00から・木曜休み・予約は電話のみ")),
 ("beer", "ChIJjaAMOjnuGGAR25JBaJGSS0w", ("wigtown", "A British pub with Japanese craft gin, whisky and Scottish beer. No smoking inside.", "Easy in English", "¥¥ · From 17:00 (Sat, Sun 14:00) · Closed Thu · Card OK"), ("wigtown", "国産クラフトジン、ウイスキー、スコットランドのビールがある英国風パブ。店内禁煙です。", "英語で話しやすい", "¥¥・17:00から（土日は14:00）・木曜休み・カード可")),
 ("tachi", "ChIJheMTbZvvGGARZXsCFA8ABf8", ("Craft Beer TOCA", "Craft beer at the edge of Inokashira Park, plus a little sake.", "", "¥¥ · From 16:30 (Mon, Tue 18:00) · Open daily · Card OK"), ("Craft Beer TOCA", "井の頭公園のそばのクラフトビール。日本酒も少しあります。", "", "¥¥・16:30から（月・火は18:00）・毎日営業・カード可")),
 ("bars", "ChIJ4eaW13PvGGARlWTlOiYZ8o8", ("HARD SHAKE BAR130", "A cocktail bar on the third floor above Harmonica Yokocho, away from the noise.", "", "¥¥ · From 17:00 (Sat, Sun 16:00) · Closed Thu · 3F"), ("HARD SHAKE BAR130", "ハモニカ横丁の3階にある、喧騒から離れたカクテルバー。", "", "¥¥・17:00から（土日は16:00）・木曜休み・3階")),
 ("bars", "ChIJU4WEQh7vGGARmYKvSzlEiD4", ("BUILD BAR130", "The sister bar of HARD SHAKE BAR130, focused on craft gin and mezcal.", "", "¥¥ · From 20:00 · Closed Sun · 2F"), ("BUILD BAR130", "HARD SHAKE BAR130の姉妹店。クラフトジンとメスカルが中心です。", "", "¥¥・20:00から・日曜休み・2階")),
 ("bars", "ChIJYUDrDkfuGGARfveMJGIk5xI", ("SCREW DRIVER", "A rum bar with more than 500 rums, open since 1997.", "", "¥¥ · From 19:00 (Sat 17:00) · Closed Sun · 4F"), ("SCREW DRIVER", "500種類以上のラムがそろうバー。1997年に開店しました。", "", "¥¥・19:00から（土は17:00）・日曜休み・4階")),
 ("ramen", "ChIJDTPucdPvGGARUyUK4yYl8QE", ("Ramen Sawada", "Light, clear chicken broth.", "", "¥ · From 11:00 · Open daily"), ("らぁ麺 さわ田", "鶏清湯の淡麗系。", "", "¥・11:00から・毎日営業")),
 ("ramen", "ChIJVUlwv0fuGGAREfKscLN6LZg", ("Hope-ken", "The original back-fat pork-soy.", "", "¥ · From 11:00 · Closed Tue, Wed"), ("ホープ軒", "背脂チャッチャ系の元祖。", "", "¥・11:00から・火・水休み")),
 ("ramen", "ChIJZ1L290fuGGARHN_FQIq56HI", ("Tsukemen Enji", "Pioneer of vegepota tsukemen: rich pork-and-seafood broth blended with vegetable purée.", "", "¥ · From 11:00 · Open daily"), ("つけ麺 えん寺", "濃厚な豚骨魚介に野菜ペーストを合わせた、ベジポタつけ麺の先駆け。", "", "¥・11:00から・毎日営業")),
 ("ramen", "ChIJm8EJaTjuGGARE-2uonEBzeQ", ("Dokutsuya", "Iekei: Yokohama-style pork-soy.", "", "¥ · From 11:00 · Closed Mon"), ("洞くつ家", "家系。", "", "¥・11:00から・月曜休み")),
 ("udon", "ChIJizSBRkjuGGARV0tn49N9AaU", ("Ibuki Udon", "Udon. Order at the ticket machine (it has English). Mostly standing.", "", "¥ · From 11:00 · Open daily"), ("いぶきうどん", "うどん。券売機で注文します（英語表示もあり）。ほとんど立ち食いです。", "", "¥・11:00から・毎日営業")),
 ("cafe", "ChIJG-aoZEjuGGARDr4v62ZwbXo", ("Kugutsuso", "A retro coffee house, known for its curry.", "", "¥ · From 10:00 · Open daily · B1"), ("くぐつ草", "レトロな喫茶店。カレーが人気です。", "", "¥・10:00から・毎日営業・地下1階")),
 ("cafe", "ChIJe-TeakzuGGAR7ZrlpUdY69g", ("LIGHT UP COFFEE", "Third-wave coffee; you can buy their beans too. A bit far from the station, so usually less crowded.", "", "¥ · From 9:00 · Open daily · Card OK"), ("LIGHT UP COFFEE", "サードウェーブ系のコーヒー店。オリジナルの豆も買えます。駅から少し遠いぶん、比較的すいています。", "", "¥・9:00から・毎日営業・カード可")),
 ("walk", "ChIJLWaVdDXuGGART_Pg1R3CZ4A", ("Inokashira Park", "A big park with a pond and swan boats, a few minutes south of the station.", "", ""), ("井の頭恩賜公園", "池とスワンボートのある大きな公園。駅から南へ数分です。", "", "")),
 ("walk", "ChIJZXco9RXvGGARYzRNqY-U-o8", ("Harmonica Yokocho", "Narrow lanes of tiny bars and eateries, right by the station's north exit.", "", ""), ("ハモニカ横丁", "小さな飲み屋や食堂が並ぶ細い路地。駅の北口のすぐそばです。", "", "")),
]

# (title_en, title_ja, [(romaji, kanji, en, ja)])
WORDS = [
 ("This night", "今夜のこと", [
  ("Ikitsuke", "行きつけ", "Your regular place, where the owner knows your name.", "店主が名前を覚えている、いつもの店。"),
  ("Joren", "常連", "A regular. Tonight, that's us, and maybe one day, you.", "常連のこと。今夜は私たち。いつかは、あなたの番です。"),
  ("Hashigo", "はしご", "Hopping from one small place to the next, like climbing a ladder.", "小さな店を一軒ずつ回ること。はしごを上るように。"),
  ("Tachinomi", "立ち飲み", "A standing bar for a quick, casual drink. Some have a few seats, but most people stand.", "立って気軽に一杯飲める店。席が少しある店もあります。")]),
 ("Walking in", "お店に入ったら", [
  ("Irasshaimase", "いらっしゃいませ", "\"Welcome!\" No need to answer. A smile and a nod is enough.", "「ようこそ」の意味です。返事はいりません。笑顔でうなずけば十分です。"),
  ("Oshibori", "おしぼり", "A hot or cold towel to wipe your hands before you eat.", "食べる前に手をふく、温かいか冷たいタオル。"),
  ("Otoshi", "お通し", "A small dish that arrives without ordering. It is charged like a small seat charge. That is normal, so no need to send it back.", "頼まなくても出てくる小皿。小さな席料のようにお会計に入ります。よくあることなので、断らなくて大丈夫です。")]),
 ("Ordering", "注文するとき", [
  ("Osusume", "おすすめ", "\"What do you recommend?\" Ask the owner, then let them choose.", "「おすすめは？」と店主に聞いて、選んでもらいましょう。"),
  ("Omakase", "おまかせ", "\"I'll leave it to you.\" The owner picks for you.", "「お任せします」。店主が選んでくれます。"),
  ("Okawari", "おかわり", "\"Another one, please.\" A refill of the same drink.", "「もう一杯」。同じ飲み物をもう一杯。"),
  ("Chaser", "チェイサー", "A glass of water on the side. Just ask for one.", "お酒と一緒に飲む水。頼めば出してくれます。")]),
 ("Drinks", "飲み物", [
  ("Nama", "生", "Draft beer. \"Nama, kudasai\" gets you one.", "生ビール。「生、ください」で出てきます。"),
  ("Highball", "ハイボール", "Whisky and soda. A favorite in bars across Japan.", "ウイスキーのソーダ割り。日本中のバーで人気です。"),
  ("Hiya / Atsukan", "冷や・熱燗", "Sake at room temperature, or served warm.", "常温の日本酒と、温めた日本酒。"),
  ("Shochu", "焼酎", "A spirit made from sweet potato, barley, or rice. Try it with water or soda.", "芋や麦、米から造る蒸留酒。水割りやソーダ割りで。"),
  ("Umeshu", "梅酒", "Sweet plum liqueur, often on the rocks.", "甘い梅のお酒。ロックで飲むことが多いです。")]),
 ("Food", "料理", [
  ("Tsumami", "つまみ", "Small dishes to go with your drinks.", "お酒に合わせる小皿料理。"),
  ("Obanzai", "おばんざい", "Kyoto-style home cooking, served in small bowls.", "小鉢で出てくる、京都風の家庭料理。"),
  ("Shime", "締め", "The last dish of the night, often noodles or rice.", "その夜の最後の一品。麺やご飯が多いです。")]),
 ("The regulars' way", "常連のやり方", [
  ("Kanpai", "乾杯", "Cheers. Wait until everyone has a glass before the first sip.", "全員のグラスがそろってから、最初の一口を。"),
  ("Okaikei", "お会計", "\"The bill, please.\"", "「お会計をお願いします」。"),
  ("Gochisosama", "ごちそうさま", "Said as you leave. Thanks for the food and drink.", "帰るときに言うことば。料理とお酒へのお礼です。")]),
 ("Streets & alleys", "通りと路地", [
  ("Dori", "通り", "Street. Inokashira-dori is Inokashira Street.", "通りのこと。Inokashira-doriは井の頭通りです。"),
  ("Kaido", "街道", "An old road between towns, now a main road. Like Itsukaichi-kaido.", "町と町を結んだ古い道で、今は幹線道路です。五日市街道がその例です。"),
  ("Yokocho", "横丁", "A narrow alley packed with tiny bars and eateries, like Harmonica Yokocho.", "小さな飲み屋や食堂がぎっしり並ぶ路地。ハモニカ横丁のような場所です。"),
  ("Shotengai", "商店街", "A local shopping street, often under a roof. Sunroad is one.", "地元の商店街。屋根付きのものも多く、サンロードもそのひとつです。"),
  ("Ura", "裏", "\"Behind.\" Locals call the bar-filled lanes behind a big store by its name, like Yodobashi-ura.", "「裏手」のこと。大きな店の裏の、飲み屋が多い路地を、地元の人は「ヨドバシ裏」のように呼びます。"),
  ("Koen-guchi", "公園口", "The park-side (south) exit of a station. Many izakaya gather around it.", "駅の公園側の出口（南口）。この出口のまわりにも居酒屋が集まっています。")]),
 ("Who's behind the counter", "カウンターの向こうの人", [
  ("Masuta", "マスター", "What regulars call the owner or head bartender of a bar.", "常連がバーの店主やヘッドバーテンダーを呼ぶときのことば。"),
  ("Taisho", "大将", "What regulars call the chef-owner at a sushi counter or izakaya.", "常連が寿司屋や居酒屋の主人を呼ぶときのことば。")]),
]
MANNERS = [
 ("About tipping", "チップについて", [
  ("No tips, please", "チップは不要", "Japan has no tipping. Foreign cash can't be used in the shop and is hard to exchange, so a kind tip can leave the owner with a problem.", "日本にチップの習慣はありません。外国のお金はお店で使えず、両替も手間なので、好意のチップがかえって店主を困らせることがあります。"),
  ("\"Masuta mo ippai dozo\"", "マスターも一杯どうぞ", "Want to say thank you? Buy the owner a drink. It goes on your bill like any other.", "お礼をしたいときは、店主に一杯ごちそうしましょう。ほかの注文と同じように、お会計に入ります。"),
  ("\"Oishikatta\"", "おいしかった", "\"That was delicious.\" Owners remember the guests who say it.", "「おいしかった」。こう言ってくれたお客さんを、店主は覚えています。")]),
 ("At the counter", "カウンターで", [
  ("Drinks first", "まず飲み物", "Order a drink first, then a few dishes at a time. More can always follow.", "まず飲み物を頼み、料理は数品ずつ。あとからいつでも追加できます。"),
  ("Ask before photos", "写真は一声かけて", "Food is usually fine. Ask before photographing the owner or other guests: \"Shashin, ii desu ka?\"", "料理はたいてい大丈夫です。店主やほかのお客さんを撮るときは「写真、いいですか？」と聞きましょう。"),
  ("Shared space", "カウンターは共有", "Counter seats are close together. Keep voices easy and bags under your chair.", "カウンターの席は近いので、声は控えめに。荷物はいすの下へ。"),
  ("Smoking", "たばこ", "Rules differ by place, and many are smoke-free inside. Ask before you light up.", "ルールは店ごとに違い、店内禁煙の店も多いです。火をつける前に聞きましょう。"),
  ("Paying", "お支払い", "Many places take cards. A little yen in your pocket still helps.", "カードが使える店は多いですが、少し現金があると安心です。")]),
 ("Sharing the table", "みんなで食べるとき", [
  ("Torizara", "取り皿", "Small plates for sharing. Dishes are meant for the table: \"Torizara, kudasai.\"", "取り分け用の小皿。料理はみんなで分けるものです。「取り皿、ください」。"),
  ("Oshaku", "お酌", "Pour for your friends, and they pour for you. Nobody fills their own glass first.", "友人のグラスに注ぎ、自分のぶんは注いでもらいます。自分で先に注ぐ人はいません。"),
  ("Chopsticks", "お箸", "Never pass food from chopsticks to chopsticks, or stand them up in rice.", "箸から箸へ料理を渡したり、ご飯に箸を立てたりしないように。"),
  ("Last order", "ラストオーダー", "The last call for food and drinks, often 30 minutes before closing.", "料理と飲み物の最後の注文。閉店の30分前のことが多いです。")]),
]
SMALL = {
 "en": ("Small shops, small teams", [
  "Many of our shops are run by just one or two people. When it's busy, food can take a while. That's part of a small shop, not bad service.",
  "Order a few dishes at once, rather than one at a time.",
  "If someone is busy cooking, ask the person serving instead. If the owner is doing both, wait for a quiet moment."]),
 "ja": ("小さな店、少ない人数", [
  "私たちの行きつけの多くは、1〜2人で切り盛りしている店です。混んでいるときは、料理を待つ時間が長くなる日もあります。それも小さな店らしさのひとつです。",
  "料理は、何品かまとめて頼みましょう。",
  "注文や質問は、接客している人にお願いしましょう。店主が一人で料理と接客をしている店では、手が空くのを待ちましょう。"]),
}
ALLERGY = [("肉", "meat"), ("豚肉（豚骨スープも）", "pork, incl. broth"), ("魚（だし・かつお節も）", "fish, incl. dashi"), ("甲殻類・貝・イカ・タコ", "shellfish, squid, octopus"), ("卵", "egg"), ("乳製品", "dairy"), ("小麦", "wheat"), ("そば", "buckwheat"), ("落花生・ナッツ", "peanuts, tree nuts"), ("アルコール（料理酒・みりんも）", "alcohol, incl. in cooking")]

G = {
 "en": dict(title="Our Kichijoji · Ikitsuke", desc="Kai &amp; Maya's own list of places in Kichijoji, with words and manners for the counter.",
  kicker="KICHIJOJI · TOKYO", h1="Our Kichijoji",
  lede="Some of the places we actually go, and the words that help at the counter. From Kai &amp; Maya, who have lived in Kichijoji for 15 years.",
  nav=["Places", "Words", "Manners", "Allergies", "Book a night"],
  places_h="Places", places_intro="Most are within a 10-minute walk of the station. Tap a name to open it in Google Maps.",
  places_note="Per person with drinks: ¥ up to ¥3,000 · ¥¥ ¥3,000–6,000 · ¥¥¥ over ¥6,000. 2F = one floor up; B1 = basement. Times are weekday opening times. Hours and days off can change, so check before you go.",
  go="Map ›", words_h="Words from the bar counter", words_intro="Point at the Japanese, or say it out loud. The owners will smile either way.",
  manners_h="Good manners at the counter", manners_intro="What regulars do.",
  allergy_h="Food allergies", allergy_intro="Tick what you can't eat, then show this screen to the staff.",
  allergy_note="For going on your own; our hosted evenings can't cater for allergies. Small kitchens may not be able to avoid these completely.",
  book_h="Spend an evening with us", book_p="We walk you to our regular places and help with ordering, so you can just enjoy the night.", book_btn="Ask about a date"),
 "ja": dict(title="私たちの吉祥寺 · Ikitsuke", desc="KaiとMayaが実際に通う吉祥寺の店と、カウンターで役立つことばとマナー。",
  kicker="吉祥寺・東京", h1="私たちの吉祥寺",
  lede="私たちが実際に通っている店と、カウンターで役立つことば。吉祥寺に住んで15年の、KaiとMayaより。",
  nav=["お店", "ことば", "マナー", "アレルギー", "申し込み"],
  places_h="お店", places_intro="ほとんどが駅から歩いて10分以内です。店名を押すとGoogleマップが開きます。",
  places_note="価格は1人あたり、お酒込みの目安です。¥は3,000円まで。¥¥は3,000〜6,000円。¥¥¥は6,000円以上です。時刻は平日の開店時間です。営業時間や定休日は変わることがあるので、行く前に確かめてください。",
  go="地図 ›", words_h="カウンターで使うことば", words_intro="日本語を指さすか、声に出して言ってみてください。どちらでも、店主はきっと笑顔になります。",
  manners_h="カウンターでのマナー", manners_intro="常連がしていること。",
  allergy_h="食物アレルギー", allergy_intro="食べられないものに印を付けて、この画面を店の人に見せてください。",
  allergy_note="ご自分で回るとき用です。案内の夜はアレルギーに対応できません。小さな店では、避けきれない場合があります。",
  book_h="私たちと過ごす夜", book_p="行きつけの店へ歩いて案内し、注文もお手伝いします。気楽に夜を楽しんでください。", book_btn="日程を相談する（英語のフォーム）"),
}

def cards(groups, lang):
    out = []
    for ten, tja, items in groups:
        t = ten if lang == "en" else tja
        cs = "".join(
            f'<div class="card"><p class="w"><span class="ro">{e(ro)}</span><span class="ja" lang="ja">{e(kj)}</span></p><p class="me">{e(en if lang == "en" else ja)}</p></div>'
            for ro, kj, en, ja in items)
        out.append(f'<section class="grp"><h3>{e(t)}</h3><div class="cards">{cs}</div></section>')
    return "\n".join(out)

def guide_page(lang, other):
    T = G[lang]; idx = 2 if lang == "en" else 3
    secs = []
    for key in ["dinner", "beer", "tachi", "bars", "ramen", "udon", "cafe", "walk"]:
        rows = []
        for k, pid, en, ja in PLACES:
            if k != key: continue
            name, desc, tag, info = en if lang == "en" else ja
            q = en[0] + " Kichijoji"
            tag_html = f' <span class="tag">{e(tag)}</span>' if tag else ""
            info_html = f'<p class="info">{e(info)}</p>' if info else ""
            rows.append(f'<li class="place"><a class="pl" href="{e(maps(q, pid))}" target="_blank" rel="noopener"><span class="nm">{e(name)}</span>{tag_html}<span class="go" aria-hidden="true">{e(T["go"])}</span></a><p class="desc">{e(desc)}</p>{info_html}</li>')
        foot = f'<p class="foot">{e(BARFOOT[lang])}</p>' if key == "bars" else ""
        secs.append(f'<section class="cat"><h3><span class="dot" style="background:{COLORS[key]}"></span>{CATNAME[lang][key]}</h3><ul class="places">{"".join(rows)}</ul>{foot}</section>')
    nav = "".join(f'<li><a href="#{a}">{e(l)}</a></li>' for a, l in zip(["places", "words", "manners", "allergy", "book"], T["nav"]))
    st, sl = SMALL[lang]
    chks = "".join(f'<label class="chk"><input type="checkbox"><span><span class="jp" lang="ja">{e(j)}</span> <span class="en" lang="en">{e(en)}</span></span></label>' for j, en in ALLERGY)
    return head(lang, T["title"], T["desc"]) + f"""<header class="top">
<div class="wrap">
{langbtn(other, lang)}
<p class="kicker">{e(T["kicker"])}</p>
<h1>{e(T["h1"])}</h1>
<p class="lede">{T["lede"]}</p>
</div>
</header>
<nav class="jump" aria-label="Sections"><ul>{nav}</ul></nav>
<main class="wrap">
<section class="part" id="places">
<h2>{e(T["places_h"])}</h2>
<p class="sub">{e(T["places_intro"])}</p>
<p class="note">{e(T["places_note"])}</p>
{"".join(secs)}
</section>
<section class="part" id="words">
<h2>{e(T["words_h"])}</h2>
<p class="sub">{e(T["words_intro"])}</p>
{cards(WORDS, lang)}
</section>
<section class="part" id="manners">
<h2>{e(T["manners_h"])}</h2>
<p class="sub">{e(T["manners_intro"])}</p>
{cards(MANNERS, lang)}
<section class="grp"><h3>{e(st)}</h3>{ul(sl, "small-list")}</section>
</section>
<section class="part" id="allergy">
<h2>{e(T["allergy_h"])}</h2>
<p class="sub">{e(T["allergy_intro"])}</p>
<div class="allergy">
<p class="head" lang="ja">アレルギーがあります。少量でも食べられません。<span class="en" lang="en">I have an allergy. Even a small amount is a problem.</span></p>
<div class="chks">{chks}</div>
<p class="note">{e(T["allergy_note"])}</p>
</div>
</section>
<section class="book" id="book">
<h2>{e(T["book_h"])}</h2>
<p>{e(T["book_p"])}</p>
<a class="btn" href="{FORM}" target="_blank" rel="noopener">{e(T["book_btn"])}</a>
</section>
</main>
""" + FOOT

def write(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)
    print("wrote", rel, len(text))

write("index.html", top_page("en", "ja/"))
write("ja/index.html", top_page("ja", "../"))
write("guide/index.html", guide_page("en", "../ja/guide/"))
write("ja/guide/index.html", guide_page("ja", "../../guide/"))
