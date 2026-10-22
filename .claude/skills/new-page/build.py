"""Page builder for fridgerepairblacktown.com.au (bundled with the new-page skill).

Run from the repo root. It reads freezer-repair-blacktown.html (header and
footer) and index.html (site-wide business schema node), writes <slug>.html,
and checks the FAQ schema against the visible FAQs.

  from build import *            # helpers: card, grid, table, steps, tags, intro, article, checks, white, grey
  build(slug, title, desc, h1, svc_name, svc_type, svc_desc, crumb, banner_p, intro_p,
        checklist, btn, sections, faqs, faq_h2, cta_h2, cta_p, related, end_line)
  wire(slug, label, dropdown=True, footer=True)   # .htaccess rule, sitemap-static.xml entry, menu and footer links

Rules (CLAUDE.md): title <= 60 chars, description 140-165, "from $69", "up to 12 months",
no em dashes, no phone number, no invented facts. Example sections: see the existing
brand pages (for example lg-fridge-repair.html) for the final result.
"""
import re,json,html as H,glob,xml.dom.minidom
SITE='https://fridgerepairblacktown.com.au'
LINK='style="color: var(--secondary); font-weight: 700;"'
def esc(t): return H.escape(t,quote=False)
def card(icon,t,p): return f'                <div class="frb-fault-card"><h3><i class="fa-solid fa-{icon}"></i> {t}</h3><p>{p}</p></div>\n'
def li(t): return f'                <li><i class="fa-solid fa-circle-check"></i> {t}</li>\n'
def tr(*c): return '                        <tr>'+''.join(f'<td>{x}</td>' for x in c)+'</tr>\n'
def table(heads,rows):
    return ('        <div class="frb-table-wrapper">\n            <table class="frb-compare-table">\n                <thead><tr>'+''.join(f'<th>{h}</th>' for h in heads)+'</tr></thead>\n                <tbody>\n'+''.join(tr(*r) for r in rows)+'                </tbody>\n            </table>\n        </div>\n')
def step(n,i,t,p,d): return f'''            <div class="frb-process-step frb-reveal"{f' style="transition-delay: {d}s;"' if d else ''}>
                <span class="frb-step-num">{n}</span>
                <i class="fa-solid fa-{i}"></i>
                <h3>{t}</h3>
                <p>{p}</p>
            </div>
'''
def steps(lst): return '        <div class="frb-process-grid">\n'+''.join(step(i+1,*x,[0,0.1,0.2][i%3]) for i,x in enumerate(lst))+'        </div>\n'
def tags(lst): return '            <div class="frb-tag-grid">\n'+''.join(f'                <div class="frb-tag-item">{x}</div>\n' for x in lst)+'            </div>\n'
def grid(cards): return '            <div class="frb-faults-grid">\n'+''.join(card(*c) for c in cards)+'            </div>\n'
def white(h2,inner): return f'''    <section class="frb-container frb-reveal">
        <h2 class="frb-section-title center frb-text-center">{h2}</h2>
{inner}    </section>
'''
def grey(h2,inner): return f'''    <section class="frb-bg-light">
        <div class="frb-container frb-reveal">
            <h2 class="frb-section-title center frb-text-center">{h2}</h2>
{inner}        </div>
    </section>
'''
def p_c(t): return f'        <p class="frb-text-center" style="max-width: 820px; margin: 0 auto 10px;">{t}</p>\n'
def intro(*ps): return '        <div class="frb-intro-block">\n'+''.join(f'            <p>{p}</p>\n' for p in ps)+'        </div>\n'
def article(blocks): return '        <div class="frb-article-block" style="margin-top: 30px;">\n'+''.join(f'            <h3>{h}</h3>\n            <p>{p}</p>\n' for h,p in blocks)+'        </div>\n'
def checks(items): return '            <ul class="frb-check-list left" style="max-width: 760px; margin: 30px auto 0;">\n'+''.join(li(i) for i in items)+'            </ul>\n'
def faqs_html(faqs): return '            <div style="max-width: 900px; margin: 40px auto 0;">\n'+''.join(f'                <div class="frb-faq-item frb-reveal"><h3 class="frb-faq-question">{esc(q)}</h3><div class="frb-faq-answer"><p>{esc(a)}</p></div></div>\n' for q,a in faqs)+'            </div>\n'

def build(slug,title,desc,h1,svc_name,svc_type,svc_desc,crumb,banner_p,intro_p,checklist,btn,sections,faqs,faq_h2,cta_h2,cta_p,related,end_line):
    URL=f'{SITE}/{slug}/'
    assert len(title)<=60,(len(title),title); assert 140<=len(desc)<=165,len(desc)
    tpl=open('freezer-repair-blacktown.html',encoding='utf-8',newline='').read()
    idx=open('index.html',encoding='utf-8',newline='').read()
    sj=json.loads(re.search(r'ld\+json">\s*(.*?)</script>',idx,re.S).group(1))
    org=[n for n in sj['@graph'] if n['@type']=='HVACBusiness'][0]
    graph=[
     {"@type":"WebPage","@id":URL+"#webpage","url":URL,"name":title,"description":desc,"isPartOf":{"@id":SITE+"/#website"},"about":{"@id":SITE+"/#organization"},"breadcrumb":{"@id":URL+"#breadcrumb"},"inLanguage":"en-AU"},
     org,
     {"@type":"Service","@id":URL+"#service","name":svc_name,"serviceType":svc_type,"provider":{"@id":SITE+"/#organization"},
      "areaServed":[{"@type":"City","name":"Blacktown NSW 2148"},{"@type":"AdministrativeArea","name":"Western Sydney NSW"}],
      "description":svc_desc,"url":URL,
      "offers":{"@type":"Offer","name":"Call-out fee covering the visit and diagnosis","priceCurrency":"AUD","price":"69","priceSpecification":{"@type":"PriceSpecification","price":"69","priceCurrency":"AUD"}}},
     {"@type":"BreadcrumbList","@id":URL+"#breadcrumb","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},{"@type":"ListItem","position":2,"name":crumb,"item":URL}]},
     {"@type":"FAQPage","@id":URL+"#faq","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]},
    ]
    ld=json.dumps({"@context":"https://schema.org","@graph":graph},indent=2,ensure_ascii=False)
    a=tpl.index('<!-- Favicon'); b=tpl.index('</header>')+len('</header>')
    chrome=tpl[a:b]; footer=tpl[tpl.index('    <!-- FOOTER -->'):]
    head=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{URL}">
<meta name="robots" content="index, follow, max-image-preview:large">

<script type="application/ld+json">
{ld}
</script>

'''
    rel=', '.join(f'<a href="{u}" style="color: #fff; text-decoration: underline;">{t}</a>' for u,t in related)
    body=f'''
    <!-- PAGE BANNER / H1 -->
    <section class="frb-page-banner">
        <div class="frb-container" style="padding: 0;">
            <div class="frb-reveal active">
                <h1>{h1}</h1>
                <p>{banner_p}</p>
            </div>
        </div>
    </section>

    <!-- INTRO / CTA -->
    <section class="frb-container frb-reveal" style="padding-bottom: 40px;">
        <div class="frb-intro-block">
            <p>{intro_p}</p>
            <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-top: 20px;">
                <a href="mailto:info@fridgerepairblacktown.com.au" class="frb-btn frb-btn-outline"><i class="fa-solid fa-envelope"></i> Email Us</a>
                <a href="/#contact-form" class="frb-btn"><i class="fa-solid fa-calendar-check"></i> {btn}</a>
            </div>
            <ul class="frb-check-list">
{''.join(li(c) for c in checklist)}            </ul>
        </div>
    </section>

{chr(10).join(sections)}
    <!-- FAQ -->
    <section class="frb-bg-light" id="faq-section">
        <div class="frb-container frb-reveal">
            <h2 class="frb-section-title frb-text-center center">{faq_h2}</h2>
{faqs_html(faqs)}        </div>
    </section>

    <!-- FINAL CTA -->
    <section class="frb-cta-section frb-reveal">
        <div class="frb-container" style="padding: 0;">
            <h2 class="frb-section-title center">{cta_h2}</h2>
            <p style="font-size: 1.1em; max-width: 700px; margin: 0 auto; line-height: 1.8;">{cta_p}</p>
            <div style="display: flex; gap: 20px; justify-content: center; margin-top: 40px; flex-wrap: wrap;">
                <a href="mailto:info@fridgerepairblacktown.com.au" class="frb-btn frb-btn-outline"><i class="fa-solid fa-envelope"></i> Email Us</a>
                <a href="/#contact-form" class="frb-btn"><i class="fa-solid fa-laptop"></i> {btn}</a>
            </div>
            <p style="margin-top: 30px; font-size: 0.95em; color: rgba(255,255,255,0.85);">{end_line}</p>
            <p style="margin-top: 10px; font-size: 0.95em; color: rgba(255,255,255,0.85);">Related: {rel}.</p>
        </div>
    </section>

'''
    out=head+chrome+'\n'+body+footer
    open(slug+'.html','w',encoding='utf-8',newline='').write(out)
    j=json.loads(re.search(r'ld\+json">\s*(.*?)</script>',out,re.S).group(1))
    vis=re.findall(r'frb-faq-question">(.*?)</h3><div class="frb-faq-answer"><p>(.*?)</p>',out)
    ok=all(f['name']==H.unescape(q) and f['acceptedAnswer']['text']==H.unescape(a) for f,(q,a) in zip(j['@graph'][4]['mainEntity'],vis))
    txt=re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>',' ',out,flags=re.S)
    print(slug,'title',len(title),'desc',len(desc),'faq',len(vis),ok,'emdash','—' in out)
    import os
    bad=[l for l in sorted(set(re.findall(r'href="(/[^"#?]*)',out))) if not (l=='/' or os.path.exists(l.strip('/')) or os.path.exists(l.strip('/')+'.html') or os.path.exists(l.strip('/')+'.php') or os.path.isdir(l.strip('/')))]
    print('missing links',bad)

def wire(slug,label,dropdown=True,footer=True):
    h=open('.htaccess',encoding='utf-8',newline='').read()
    rule=f'RewriteRule ^{slug}/?$ {slug}.html [L]'
    if rule not in h:
        a='RewriteRule ^fridge-regas/?$ fridge-regas.html [L]\r\n'
        assert a in h
        h=h.replace(a,a+f'\r\n# Allow the {label} landing page to work without .html extension\r\n{rule}\r\n')
        open('.htaccess','w',encoding='utf-8',newline='').write(h)
    sm=open('sitemap-static.xml',encoding='utf-8',newline='').read()
    loc=f'{SITE}/{slug}/'
    if loc not in sm:
        i=sm.index('    <url>\n        <loc>'+SITE+'/fridge-regas/</loc>'); j=sm.index('</url>',i)+len('</url>\n')
        sm=sm[:j]+f'    <url>\n        <loc>{loc}</loc>\n        <changefreq>monthly</changefreq>\n        <priority>0.8</priority>\n    </url>\n'+sm[j:]
        open('sitemap-static.xml','w',encoding='utf-8',newline='').write(sm)
    xml.dom.minidom.parse('sitemap-static.xml')
    new=f'<li><a href="/{slug}/">{label}</a></li>'
    n=0
    for f in glob.glob('*.html')+glob.glob('*.php'):
        if f==slug+'.html': continue
        s=open(f,encoding='utf-8',newline='').read()
        if new in s: continue
        nl='\r\n' if '\r\n' in s else '\n'
        t=s
        if dropdown:
            m=re.search(r'^([ \t]*)<li><a href="/freezer-repair-blacktown/">Freezer Repair</a></li>\r?$',t,re.M)
            if m: t=t[:m.start()]+m.group(1)+new+nl+t[m.start():]
        if footer:
            m=re.search(r'^([ \t]*)<li><a href="/fridge-regas/">Fridge Regassing</a></li>\r?$',t,re.M)
            if m:
                e=t.index('\n',m.start())+1
                t=t[:e]+m.group(1)+new+nl+t[e:]
        if t!=s: open(f,'w',encoding='utf-8',newline='').write(t); n+=1
    print('wired files',n)
