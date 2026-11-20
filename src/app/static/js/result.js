document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("toggle-boxes");
    const imageViewers = document.querySelectorAll(".image-viewer");

    if (toggleButton && imageViewers.length) {
        toggleButton.addEventListener("click", () => {
            const visible =
                toggleButton.getAttribute("aria-pressed") !== "true";

            imageViewers.forEach((imageViewer) => {
                imageViewer.classList.toggle("show-boxes", visible);
            });

            toggleButton.setAttribute("aria-pressed", String(visible));
            toggleButton.textContent = visible
                ? "Hide bounding boxes"
                : "Show bounding boxes";
        });
    }

    const imageTabs = document.querySelectorAll(".image-tab");
    const imageLayout = document.querySelector(".image-layout");

    if (!imageLayout) {
        return;
    }

    imageTabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            const layout = tab.dataset.layout;

            imageLayout.dataset.layout = layout;

            imageTabs.forEach((item) => {
                item.classList.toggle("active", item === tab);
            });
        });
    });
});