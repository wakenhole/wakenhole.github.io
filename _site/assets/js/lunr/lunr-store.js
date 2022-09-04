var store = [{
        "title": "건축 가능한 토지 지목 종류 이해하기",
        "excerpt":"Reference 토지 지목에 따른 활용 방법 지목의 종류 지목은 토지의 주된 사용 목적에 따라서 토지의 종류를 구분하는 명칭이다. 총 28개의 많은 종류가 있지만 알아야 하는 건축 지목은 전, 답, 임야, 대 크게 4가지 종류이다. 전: 밭으로 식물을 재배를 위한 토지 답: 논으로 물을 상시 이용이 필요한 토지 임야: 산림, 자갈...","categories": ["부동산"],
        "tags": ["지목","토지"],
        "url": "/%EB%B6%80%EB%8F%99%EC%82%B0/%EA%B1%B4%EC%B6%95-%EA%B0%80%EB%8A%A5%ED%95%9C-%ED%86%A0%EC%A7%80-%EC%A7%80%EB%AA%A9-%EC%A2%85%EB%A5%98-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0/",
        "teaser": "https://t1.daumcdn.net/thumb/R720x0/?fname=http://t1.daumcdn.net/brunch/service/user/3xR/image/kAumR8L62A5Va7-63budXTKMkpc.JPG"
      },{
        "title": "용도 지역 이해하기",
        "excerpt":"1. 용도 지역 용도 지역은 아래와 같이 도시, 관리, 농림 자연환경 보전 지역으로 분류 할 수 있다. 용도 지역에 따라서 건축물의 용도 및 크기를 제한 한다. 2. 투자 투지를 위해 적합한 지역은 아래와 같이 분류 할수 있다. 단기 투자 도시지역 / 주거지역 도시지역 / 상업지역 도시지역 / 공업지역 장기 투자...","categories": ["부동산"],
        "tags": ["용도지역","자연녹지지역","계획관리지역","건폐율","용적율"],
        "url": "/%EB%B6%80%EB%8F%99%EC%82%B0/%EC%9A%A9%EB%8F%84-%EC%A7%80%EC%97%AD/",
        "teaser": "https://t1.daumcdn.net/cfile/tistory/990D9B415BF3C6BD07"
      },{
        "title": "다주택자 종합부동산세 중과세",
        "excerpt":"지목의 종류 종합부동산세(종부세)는 매년 6월 1일 기준 부동산 보유자가 그 해 12월에 납부 한다. 종부세를 계산함에 있어서 중요한 것은 아래와 같다. \\[\\sum_{}^{} \\{공시가격 × (1-감면율)\\} × 공정시장가액비율\\] 주 택 분 : $[{전국합산 공시가격× (1 - 감면율)} - 6억 원(11억 원]× 95%$ 법 인 : [전국합산 {공시가격× (1 - 감면율)}]× 95%...","categories": ["부동산"],
        "tags": ["세금","종합부동산세"],
        "url": "/%EB%B6%80%EB%8F%99%EC%82%B0/%EC%A2%85%ED%95%A9%EB%B6%80%EB%8F%99%EC%82%B0%EC%84%B8-%EC%A4%91%EA%B3%BC%EC%84%B8/",
        "teaser": "https://t1.daumcdn.net/thumb/R720x0/?fname=http://t1.daumcdn.net/brunch/service/user/3xR/image/kAumR8L62A5Va7-63budXTKMkpc.JPG"
      },{
    "title": "Page Not Found",
    "excerpt":"Sorry, but the page you were trying to view does not exist.  ","url": "http://localhost:4000/404.html"
  },{
    "title": "About",
    "excerpt":"Who I am?  ","url": "http://localhost:4000/about/"
  },{
    "title": "Posts by Category (grid view)",
    "excerpt":" ","url": "http://localhost:4000/categories-grid/"
  },{
    "title": "Posts by Category",
    "excerpt":" ","url": "http://localhost:4000/categories/"
  },{
    "title": null,
    "excerpt":"","url": "http://localhost:4000/"
  },{
    "title": null,
    "excerpt":"var idx = lunr(function () { this.field('title') this.field('excerpt') this.field('categories') this.field('tags') this.ref('id') this.pipeline.remove(lunr.trimmer) for (var item in store) { this.add({ title: store[item].title, excerpt: store[item].excerpt, categories: store[item].categories, tags: store[item].tags, id: item }) } }); $(document).ready(function() { $('input#search').on('keyup', function () { var resultdiv = $('#results'); var query = $(this).val().toLowerCase(); var result = idx.query(function...","url": "http://localhost:4000/assets/js/lunr/lunr-en.js"
  },{
    "title": null,
    "excerpt":"step1list = new Array(); step1list[\"ΦΑΓΙΑ\"] = \"ΦΑ\"; step1list[\"ΦΑΓΙΟΥ\"] = \"ΦΑ\"; step1list[\"ΦΑΓΙΩΝ\"] = \"ΦΑ\"; step1list[\"ΣΚΑΓΙΑ\"] = \"ΣΚΑ\"; step1list[\"ΣΚΑΓΙΟΥ\"] = \"ΣΚΑ\"; step1list[\"ΣΚΑΓΙΩΝ\"] = \"ΣΚΑ\"; step1list[\"ΟΛΟΓΙΟΥ\"] = \"ΟΛΟ\"; step1list[\"ΟΛΟΓΙΑ\"] = \"ΟΛΟ\"; step1list[\"ΟΛΟΓΙΩΝ\"] = \"ΟΛΟ\"; step1list[\"ΣΟΓΙΟΥ\"] = \"ΣΟ\"; step1list[\"ΣΟΓΙΑ\"] = \"ΣΟ\"; step1list[\"ΣΟΓΙΩΝ\"] = \"ΣΟ\"; step1list[\"ΤΑΤΟΓΙΑ\"] = \"ΤΑΤΟ\"; step1list[\"ΤΑΤΟΓΙΟΥ\"] = \"ΤΑΤΟ\"; step1list[\"ΤΑΤΟΓΙΩΝ\"] = \"ΤΑΤΟ\"; step1list[\"ΚΡΕΑΣ\"]...","url": "http://localhost:4000/assets/js/lunr/lunr-gr.js"
  },{
    "title": null,
    "excerpt":"var store = [ {%- for c in site.collections -%} {%- if forloop.last -%} {%- assign l = true -%} {%- endif -%} {%- assign docs = c.docs | where_exp:'doc','doc.search != false' -%} {%- for doc in docs -%} {%- if doc.header.teaser -%} {%- capture teaser -%}{{ doc.header.teaser }}{%- endcapture...","url": "http://localhost:4000/assets/js/lunr/lunr-store.js"
  },{
    "title": "Markup",
    "excerpt":"Sample post listing for the tag `markup`. ","url": "http://localhost:4000/tags/markup/"
  },{
    "title": "Portfolio",
    "excerpt":"Sample document listing for the collection `_portfolio`. ","url": "http://localhost:4000/portfolio/"
  },{
    "title": "Search",
    "excerpt":"","url": "http://localhost:4000/search/"
  },{
    "title": "Sitemap",
    "excerpt":"A list of all the posts and pages found on the site. For you robots out there is an [XML version]({{ '/sitemap.xml' | relative_url }}) available for digesting as well. Pages {% for post in site.pages %} {% include archive-single.html %} {% endfor %} Posts {% for post in site.posts...","url": "http://localhost:4000/sitemap/"
  },{
    "title": "Posts by Tag (grid view)",
    "excerpt":"","url": "http://localhost:4000/tags-grid/"
  },{
    "title": "Posts by Tag",
    "excerpt":"","url": "http://localhost:4000/tags/"
  },{
    "title": "Posts by Year (grid view)",
    "excerpt":"","url": "http://localhost:4000/year-archive-grid/"
  },{
    "title": "Posts by Year",
    "excerpt":"","url": "http://localhost:4000/year-archive/"
  },{
    "title": null,
    "excerpt":"{% if page.xsl %}{% endif %}Jekyll{{ site.time | date_to_xmlschema }}{{ page.url | absolute_url | xml_escape }}{% assign title = site.title | default: site.name %}{% if page.collection != \"posts\" %}{% assign collection = page.collection | capitalize %}{% assign title = title | append: \" | \" | append: collection %}{% endif...","url": "http://localhost:4000/feed.xml"
  },{
    "title": null,
    "excerpt":"{% if page.xsl %} {% endif %} {% assign collections = site.collections | where_exp:'collection','collection.output != false' %}{% for collection in collections %}{% assign docs = collection.docs | where_exp:'doc','doc.sitemap != false' %}{% for doc in docs %} {{ doc.url | replace:'/index.html','/' | absolute_url | xml_escape }} {% if doc.last_modified_at or doc.date...","url": "http://localhost:4000/sitemap.xml"
  },{
    "title": null,
    "excerpt":"Sitemap: {{ \"sitemap.xml\" | absolute_url }} ","url": "http://localhost:4000/robots.txt"
  }]
