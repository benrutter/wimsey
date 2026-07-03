document$.subscribe(() => {
  document.querySelectorAll("img.dither:not([data-dithered])").forEach((img) => {
    const apply = () => {
      img.dataset.dithered = "true";
      const span = document.createElement("span");
      span.className = "dither-mask";
      span.style.setProperty("--dither-src", `url("${img.currentSrc || img.src}")`);
      span.style.aspectRatio = `${img.naturalWidth} / ${img.naturalHeight}`;
      img.replaceWith(span);
    };
    img.complete ? apply() : img.addEventListener("load", apply, { once: true });
  });
});
