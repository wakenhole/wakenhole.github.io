document.addEventListener("DOMContentLoaded", function () {
  // 모든 <pre><code> 코드블록 탐색
  document.querySelectorAll("pre > code").forEach(function (codeBlock) {
    var button = document.createElement("button");
    button.className = "copy-code-button";
    button.type = "button";
    button.innerText = "Copy";
    button.style.position = "absolute";
    button.style.right = "0.5em";
    button.style.top = "0.5em";
    button.style.zIndex = "10";

    var pre = codeBlock.parentNode;
    pre.style.position = "relative";
    pre.appendChild(button);

    button.addEventListener("click", function () {
      navigator.clipboard.writeText(codeBlock.innerText).then(function () {
        button.innerText = "Copied!";
        setTimeout(function () { button.innerText = "Copy"; }, 1500);
      });
    });
  });
});