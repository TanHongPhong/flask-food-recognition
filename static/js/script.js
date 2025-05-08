// script.js
document.addEventListener("DOMContentLoaded", () => {
  console.log("Trang đã tải xong!");

  const fileInput = document.querySelector('input[type="file"]');
  fileInput.addEventListener("change", (e) => {
    const fileName = e.target.files[0]?.name;
    if (fileName) {
      alert(`Bạn đã chọn ảnh: ${fileName}`);
    }
  });
});
