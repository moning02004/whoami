function initLightbox() {
    if (document.getElementById("lightbox-overlay")) return;

    const overlay = document.createElement("div");
    overlay.id = "lightbox-overlay";
    Object.assign(overlay.style, {
        display: "none",
        position: "fixed",
        inset: "0",
        backgroundColor: "rgba(0,0,0,0.85)",
        zIndex: "9999",
        alignItems: "center",
        justifyContent: "center",
        padding: "16px",
        boxSizing: "border-box",
    });

    const img = document.createElement("img");
    img.id = "lightbox-img";
    Object.assign(img.style, {
        maxWidth: "100%",
        maxHeight: "100%",
        width: "auto",
        height: "auto",
        objectFit: "contain",
        borderRadius: "8px",
        boxShadow: "0 8px 40px rgba(0,0,0,0.6)",
    });

    // 닫기 버튼 (모바일에서 탭 영역 확보)
    const closeBtn = document.createElement("button");
    closeBtn.textContent = "✕";
    Object.assign(closeBtn.style, {
        position: "absolute",
        top: "12px",
        right: "16px",
        background: "rgba(255,255,255,0.15)",
        border: "none",
        borderRadius: "50%",
        color: "#fff",
        fontSize: "18px",
        width: "36px",
        height: "36px",
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        lineHeight: "1",
        WebkitTapHighlightColor: "transparent",
    });
    closeBtn.addEventListener("click", closeLightbox);

    overlay.appendChild(img);
    overlay.appendChild(closeBtn);
    document.body.appendChild(overlay);

    // 이미지 바깥 클릭 시 닫기
    overlay.addEventListener("click", (e) => {
        if (e.target === overlay) closeLightbox();
    });

    // ESC 키로도 닫기
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") closeLightbox();
    });
}

function openLightbox(src) {
    initLightbox();

    const isMobile = window.innerWidth <= 768;
    console.log(isMobile)
    const overlay = document.getElementById("lightbox-overlay");
    const img = document.getElementById("lightbox-img");

    img.src = src;

    // 모바일: 거의 꽉 차게 / 데스크톱: 70% 제한
    if (isMobile) {
        overlay.style.padding = "48px 16px 16px"; // 상단 닫기 버튼 공간
        img.style.maxWidth = "90vw";
        img.style.maxHeight = "90vh";
    } else {
        overlay.style.padding = "16px";
        img.style.maxWidth = "70vw";
        img.style.maxHeight = "70vh";
    }

    overlay.style.display = "flex";

    // 스크롤 방지
    document.body.style.overflow = "hidden";
}

function closeLightbox() {
    const overlay = document.getElementById("lightbox-overlay");
    if (overlay) overlay.style.display = "none";
    document.body.style.overflow = "";
}