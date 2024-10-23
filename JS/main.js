document.addEventListener("DOMContentLoaded", () => {
  const testForm = document.getElementById("testForm");
  const criteriaForm = document.getElementById("criteriaForm");
  const resultsSection = document.getElementById("results");
  const perfumeResult = document.getElementById("perfumeResult");
  const criteriaSection = document.getElementById("criteria");
  const testSection = document.getElementById("test");
  const criteriaBtn = document.getElementById("criteriaBtn");
  const testBtn = document.getElementById("testBtn");
  const optionsSection = document.getElementById("options");
  const retakeTestBtn = document.getElementById("retakeTestBtn");

  if (retakeTestBtn) {
    retakeTestBtn.remove();
  }

  const retakeButton = document.createElement("button");
  retakeButton.id = "retakeTestBtn";
  retakeButton.className = "hidden";
  retakeButton.innerText = "Pick another fragrance";
  resultsSection.appendChild(retakeButton);

  criteriaBtn.addEventListener("click", () => {
    optionsSection.classList.add("hidden");
    criteriaSection.classList.remove("hidden");
    resultsSection.classList.add("hidden");
  });

  testBtn.addEventListener("click", () => {
    optionsSection.classList.add("hidden");
    testSection.classList.remove("hidden");
    resultsSection.classList.add("hidden");
    showQuestion(1);
  });

  async function fetchPerfumes() {
    const response = await fetch("updated_all_perfumes.json");
    const perfumes = await response.json();
    return perfumes;
  }

  function combineCriteria(selectedValues) {
    const combinedCriteria = {
      floral: ["floral", "green", "herbal"],
      woody: ["woody", "earthy", "smoky", "animalic"],
      freshScent: ["fresh", "citrus", "marine", "aquatic"],
      relaxed: ["relaxed", "calm"],
      cheerful: ["cheerful", "playful", "carefree"],
      mysterious: ["mysterious", "meditative", "melancholic", "exotic"],
      sophisticated: ["sophisticated", "cozy", "comforting"],
      intenseMood: ["intenseMood", "bold", "exotic"],
      friendly: ["friendly", "easygoing"],
      confident: ["confident", "assertive", "fearless"],
      imaginative: ["imaginative", "independent"],
      fruitJuice: ["fruitJuice", "apple juice", "fruit punch"],
      special: ["special", "formal", "night out", "evening"],
      outdoor: ["outdoor", "casual", "daytime"],
      indoor: ["indoor", "casual", "evening"],
      everyday: ["everyday", "casual"],
    };

    let combinedValues = [];
    selectedValues.forEach((value) => {
      if (combinedCriteria[value]) {
        combinedValues = combinedValues.concat(combinedCriteria[value]);
      } else {
        combinedValues.push(value);
      }
    });

    return [...new Set(combinedValues)];
  }

  function getCriteriaWeight(value) {
    const criteriaWeights = {
      // Тип аромата
      floral: 5,
      green: 5,
      herbal: 5,
      woody: 5,
      earthy: 5,
      smoky: 5,
      fresh: 5,
      citrus: 5,
      marine: 5,
      aquatic: 5,

      // Интенсивность
      intenseMood: 4,
      bold: 4,
      exotic: 4,

      // Стиль одежды
      sophisticated: 3,
      cozy: 3,
      comforting: 3,

      // Событие
      special: 3,
      formal: 3,
      night_out: 3,
      evening: 3,
      outdoor: 2,
      casual: 2,
      daytime: 2,
      indoor: 2,
      evening: 2,
      everyday: 2,

      // Настроение
      relaxed: 2,
      calm: 2,
      cheerful: 2,
      playful: 2,
      carefree: 2,
      mysterious: 2,
      meditative: 2,
      melancholic: 2,

      // Характер
      friendly: 1,
      easygoing: 1,
      confident: 1,
      assertive: 1,
      imaginative: 1,
      independent: 1,

      // Напиток
      fruitJuice: 1,
      apple_juice: 1,
      fruit_punch: 1,
    };

    return criteriaWeights[value] || 1;
  }

  function findBestMatch(perfumes, selectedValues) {
    let bestMatch = null;
    let highestMatchScore = 0;

    perfumes.forEach((perfume) => {
      let matchScore = 0;
      const criteria = Object.values(perfume.criteria).flat();

      selectedValues.forEach((value) => {
        if (criteria.includes(value)) {
          matchScore += getCriteriaWeight(value);
        }
      });

      if (matchScore > highestMatchScore) {
        highestMatchScore = matchScore;
        bestMatch = perfume;
      }
    });

    return bestMatch;
  }

  function showQuestion(questionNumber) {
    const questions = testForm.querySelectorAll(".question");
    questions.forEach((question) => {
      question.classList.add("hidden");
    });
    const currentQuestionEl = testForm.querySelector(
      `[data-question="${questionNumber}"]`
    );
    if (currentQuestionEl) {
      currentQuestionEl.classList.remove("hidden");
    } else {
      console.error(
        `Question element with data-question="${questionNumber}" not found`
      );
    }
  }

  function goToNextQuestion() {
    const currentQuestionEl = testForm.querySelector(".question:not(.hidden)");
    if (!currentQuestionEl) return;

    const currentQuestionNumber = parseInt(currentQuestionEl.dataset.question);
    const nextQuestionNumber = currentQuestionNumber + 1;

    showQuestion(nextQuestionNumber);
  }

  async function submitForm(form) {
    const formData = new FormData(form);
    let selectedValues = [];

    for (let value of formData.values()) {
      selectedValues.push(value);
    }

    selectedValues = combineCriteria(selectedValues);

    const perfumes = await fetchPerfumes();
    const bestMatch = findBestMatch(perfumes, selectedValues);

    resultsSection.classList.remove("hidden");
    perfumeResult.innerHTML = `
      <h3><a href="${bestMatch.url}" target="_blank">${bestMatch.title}</a></h3>
      <div class="result-container">
        <div class="result-image">
          <img src="${bestMatch.thumbnail_url}" alt="${bestMatch.title}">
        </div>
        <div class="result-description">
          <p>${bestMatch.description}</p>
        </div>
      </div>
    `;

    if (form === testForm) {
      testSection.classList.add("hidden");
    } else if (form === criteriaForm) {
      criteriaSection.classList.add("hidden");
    }

    retakeButton.classList.remove("hidden");
  }

  testForm.addEventListener("click", (e) => {
    if (e.target.classList.contains("next-btn")) {
      const currentQuestionEl = testForm.querySelector(
        ".question:not(.hidden)"
      );
      const currentQuestionNumber = parseInt(
        currentQuestionEl.dataset.question
      );
      if (currentQuestionNumber === 9) {
        submitForm(testForm);
      } else {
        goToNextQuestion();
      }
    }
  });

  criteriaForm.addEventListener("submit", (event) => {
    event.preventDefault();
    submitForm(criteriaForm);
  });

  retakeButton.addEventListener("click", () => {
    location.reload();
  });

  const questions = testForm.querySelectorAll(".question");
  questions.forEach((question) => {
    const radioButtons = question.querySelectorAll('input[type="radio"]');
    const nextButton = question.querySelector(".next-btn");

    radioButtons.forEach((radioButton) => {
      radioButton.addEventListener("change", () => {
        if (question.querySelector('input[type="radio"]:checked')) {
          nextButton.disabled = false;
        }
      });
    });

    nextButton.disabled = true;
  });
});
