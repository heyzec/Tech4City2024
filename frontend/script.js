const SERVER_URL = `http://localhost:8000`;

// ================================================================================
// API
// ================================================================================

class API {
  async get_photos() {
    try {
      const response = await fetch(`${SERVER_URL}/results`);
      if (!response.ok) {
        throw new Error("Failed to fetch photos");
      }
      return await response.json();
    } catch (error) {
      console.error("Error fetching photos:", error.message);
      throw error;
    }
  }

  async upload_photo(file) {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${SERVER_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload photo");
      }

      return await response.json();
    } catch (error) {
      console.error("Error uploading photo:", error.message);
      throw error;
    }
  }
}

const api = new API();

// ================================================================================
// Helpers
// ================================================================================

// ================================================================================
// Event handlers
// ================================================================================

// // Tutorial Modal
// document.addEventListener("DOMContentLoaded", function () {
//   if (localStorage.getItem("visited") === "true") {
//     return;
//   }

//   var modal = document.getElementById("tutorialModal");
//   modal.style.display = "block";

//   var closeBtn = modal.querySelector(".close");
//   closeBtn.addEventListener("click", function () {
//     modal.style.display = "none";
//     localStorage.setItem("visited", "true");
//   });

//   var nextBtn = modal.querySelector(".nextBtn");
//   var tutorialText = [
//     "Upload an image by either drag & drop or click on 'Upload Image'.",
//     "Click 'Submit' to upload.",
//     "The image will be sent to analyse and you will be able to view the final results.",
//   ];
//   var step = 0;

//   function updateTutorialText() {
//     document.getElementById("tutorialStep").textContent = "Step " + (step + 1);
//     document.getElementById("tutorialText").textContent = tutorialText[step];
//   }

//   updateTutorialText();

//   nextBtn.addEventListener("click", function () {
//     step++;
//     if (step < tutorialText.length) {
//       updateTutorialText();
//     } else {
//       modal.style.display = "none";
//       localStorage.setItem("visited", "true");
//     }
//   });
// });

// document.addEventListener("DOMContentLoaded", async () => {
//   const r = await fetch(`${SERVER_URL}/results`);
//   const data = await r.json();
//   document.getElementById(
//     "placeholder"
//   ).innerHTML = `Number of elements: ${data.length}`;
// });

// document.getElementById("uploadForm").onsubmit = function (event) {
//   // Stop page from reloading
//   console.log("onsubmit");
//   event.preventDefault();

//   handleUpload();
// };

document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("imageUpload");
  const placeholderText = document.querySelector(".result-header p");

  fileInput.addEventListener("change", function (event) {
    const file = event.target.files[0];

    if (file) {
      const imageUrl = URL.createObjectURL(file);
      document.getElementById("uploadedImage").src = imageUrl;
      document.getElementById("uploadedImage").style.display = "block";
      placeholderText.textContent = "Uploaded Image";
    } else {
      document.getElementById("uploadedImage").src = "";
      document.getElementById("uploadedImage").style.display = "none";
    }
  });

  const uploadForm = document.getElementById("uploadForm");
  const resultsContainer = document.getElementById("results-container");

  uploadForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const file = fileInput.files[0];

    if (file) {
      api
        .upload_photo(file)
        .then((response) => {
          if (currentInputImage.src && currentResultImage.src) {
            const cardResult = document.createElement("div");
            cardResult.classList.add("card-result");

            const resultHeader = document.createElement("div");
            resultHeader.classList.add("result-header");

            const inputText = document.createElement("p");
            inputText.textContent = "Input";

            const inputImage = document.createElement("img");
            inputImage.src = currentInputImage.src;
            inputImage.alt = "Input Image";
            inputImage.classList.add("result-image");

            const resultBody = document.createElement("div");
            resultBody.classList.add("result-body");

            const outputText = document.createElement("p");
            outputText.textContent = "Output";

            const outputImage = document.createElement("img");
            outputImage.src = currentResultImage.src;
            outputImage.alt = "Output Image";
            outputImage.classList.add("result-image");

            resultHeader.appendChild(inputText);
            resultHeader.appendChild(inputImage);
            resultBody.appendChild(outputText);
            resultBody.appendChild(outputImage);
            cardResult.appendChild(resultHeader);
            cardResult.appendChild(resultBody);
            resultsContainer.appendChild(cardResult);
          }

          currentInputImage.src = response.input;
          currentResultImage.src = response.output;
          currentInputImage.style.display = "block";
          currentResultImage.style.display = "block";
        })
        .catch((error) => {
          console.error("Failed to upload photo:", error);
        });
    }
  });
});

document.addEventListener("DOMContentLoaded", async function () {
  const resultsContainer = document.getElementById("results-container");

  try {
    const response = await fetch(`${SERVER_URL}/results`);
    const photos = await response.json();

    photos.forEach((photo) => {
      const cardResult = document.createElement("div");
      cardResult.classList.add("card-result");

      const resultHeader = document.createElement("div");
      resultHeader.classList.add("result-header");

      const inputText = document.createElement("p");
      inputText.textContent = "Input";

      const inputImage = document.createElement("img");
      inputImage.src = photo.input;
      inputImage.alt = "Input Image";
      inputImage.classList.add("result-image");

      const resultBody = document.createElement("div");
      resultBody.classList.add("result-body");

      const outputText = document.createElement("p");
      outputText.textContent = "Output";

      const outputImage = document.createElement("img");
      outputImage.src = photo.output;
      outputImage.alt = "Output Image";
      outputImage.classList.add("result-image");

      resultHeader.appendChild(inputText);
      resultHeader.appendChild(inputImage);
      resultBody.appendChild(outputText);
      resultBody.appendChild(outputImage);
      cardResult.appendChild(resultHeader);
      cardResult.appendChild(resultBody);
      resultsContainer.appendChild(cardResult);
    });
  } catch (error) {
    console.error("Failed to fetch and display images:", error);
  }
});

async function deleteAllPhotos() {
  try {
    const response = await fetch(`${SERVER_URL}/delete`, {
      method: "DELETE",
    });
    if (!response.ok) {
      throw new Error("Failed to delete entries");
    }
    const data = await response.json();
    console.log(data.message);
    location.reload();
  } catch (error) {
    console.error("Error deleting entries:", error);
  }
}
