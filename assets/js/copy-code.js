document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("pre > code").forEach(function (codeBlock) {
    // 복사 버튼 생성
    var button = document.createElement("button");
    button.className = "copy-code-button";
    button.type = "button";
    button.innerText = "복사";
    button.style = "position: absolute; right: 0.5em; top: 0.5em;";

    // pre 태그에 상대 위치 지정
    var pre = codeBlock.parentNode;
    pre.style.position = "relative";
    pre.appendChild(button);

    button.addEventListener("click", function () {
      navigator.clipboard.writeText(codeBlock.innerText).then(function () {
        button.innerText = "복사됨!";
        setTimeout(function () { button.innerText = "복사"; }, 1500);
      });
    });
  });
});