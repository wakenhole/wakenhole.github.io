document.addEventListener("DOMContentLoaded", function () {

  // 코드 블록 선택
  const codeBlocks = document.querySelectorAll("div.highlighter-rouge, figure.highlight");

  codeBlocks.forEach((block, index) => {
    // 광고 HTML 문자열
    const adHTML = `
      <div class="adsense-block" style="margin: 1.5rem 0;">
        <ins class="adsbygoogle"
            style="display:block"
            data-ad-client="ca-pub-4802170714228040"
            data-ad-slot="7087125516"
            data-ad-format="auto"
            data-full-width-responsive="true"></ins>
      </div>
    `;

    // 📌 앞에 삽입
    block.insertAdjacentHTML("beforebegin", adHTML);

    // 📌 뒤에 삽입
    // block.insertAdjacentHTML("afterend", adHTML);

    // 렌더링 trigger
    try {
      (adsbygoogle = window.adsbygoogle || []).push({});
    } catch (e) {
      console.warn("Adsense render error", e);
    }
  });
});