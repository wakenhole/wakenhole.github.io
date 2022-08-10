var store = [{
        "title": "Layout: Post with Nested Table of Contents via Helper",
        "excerpt":"Tests table of contents with multiple levels to verify indentation is readible via helper include (deprecated). {% include toc %} On This Page Enim laboris id ea elit elit deserunt 2 Sit adipisicing tempor duis velit cupidatat occaecat do amet 2.1 Ex et quis exercitation fugiat excepteur eiusmod mollit consequat...","categories": [],
        "tags": ["table of contents"],
        "url": "/layout-table-of-contents-include-post/",
        "teaser": "/assets/images/teaser.jpg"
      },{
        "title": "Layout: Post with Nested Table of Contents",
        "excerpt":"Tests table of contents with multiple levels to verify indentation is readible. Enim laboris id ea elit elit deserunt Magna incididunt elit id enim nisi quis excepteur reprehenderit Lorem dolore dolore ad enim. Labore esse elit excepteur et elit dolor. Elit ut consectetur labore velit elit esse voluptate id commodo....","categories": [],
        "tags": ["table of contents"],
        "url": "/layout-table-of-contents-indent-post/",
        "teaser": "/assets/images/teaser.jpg"
      },{
        "title": "Layout: Post with Table of Contents",
        "excerpt":"Enable table of contents on post or page by adding toc: true to its YAML Front Matter. The title and icon can also be changed with: --- toc: true toc_label: \"Unique Title\" toc_icon: \"heart\" # corresponding Font Awesome icon name (without fa prefix) --- HTML Elements Below is just about...","categories": [],
        "tags": ["table of contents"],
        "url": "/layout-table-of-contents-post/",
        "teaser": "/assets/images/teaser.jpg"
      },{
        "title": "Layout: Post with Sticky Table of Contents",
        "excerpt":"“Stick” table of contents to the top of a page by adding toc_sticky: true to its YAML Front Matter. --- toc: true toc_sticky: true --- HTML Elements Below is just about everything you’ll need to style in the theme. Check the source code to see the many embedded elements within...","categories": [],
        "tags": ["table of contents"],
        "url": "/layout-table-of-contents-sticky/",
        "teaser": "/assets/images/teaser.jpg"
      },{
        "title": "Layout: Sidebar Custom",
        "excerpt":"This post has a custom sidebar set in the post’s YAML Front Matter.   An example of how that YAML could look is:   sidebar:   - title: \"Title\"     image: http://placehold.it/350x250     image_alt: \"image\"     text: \"Some text here.\"   - title: \"Another Title\"     text: \"More text here.\"  ","categories": [],
        "tags": [],
        "url": "/layout-sidebar-custom/",
        "teaser": "/assets/images/teaser.jpg"
      },{
        "title": "Layout: Sidebar with Navigation List",
        "excerpt":"This post has a custom navigation list set in the post’s YAML Front Matter. sidebar: title: \"Sample Title\" nav: sidebar-sample Along with navigation elements set in _data/navigation.yml. sidebar-sample: - title: \"Parent Page A\" children: - title: \"Child Page A1\" url: / - title: \"Child Page A2\" url: / - title:...","categories": [],
        "tags": [],
        "url": "/layout-sidebar-nav-list/",
        "teaser": "/assets/images/teaser.jpg"
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
    "excerpt":"","url": "http://localhost:4000/page2/"
  },{
    "title": null,
    "excerpt":"{% if page.xsl %} {% endif %} {% assign collections = site.collections | where_exp:'collection','collection.output != false' %}{% for collection in collections %}{% assign docs = collection.docs | where_exp:'doc','doc.sitemap != false' %}{% for doc in docs %} {{ doc.url | replace:'/index.html','/' | absolute_url | xml_escape }} {% if doc.last_modified_at or doc.date...","url": "http://localhost:4000/sitemap.xml"
  },{
    "title": null,
    "excerpt":"Sitemap: {{ \"sitemap.xml\" | absolute_url }} ","url": "http://localhost:4000/robots.txt"
  }]
