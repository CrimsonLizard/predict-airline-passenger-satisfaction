 // Function to update the slider value
 function updateSliderValue(sliderId, valueElementId) {
  const slider = document.getElementById(sliderId);
  const valueElement = document.getElementById(valueElementId);
  const value = slider.value || 0;
  valueElement.textContent = value;

  const form = document.querySelector('form');
  const hiddenInput = form.querySelector(`input[name="${sliderId}"]`);
  if (hiddenInput) {
    hiddenInput.value = value || 0;
  } else {
    const newHiddenInput = document.createElement('input');
    newHiddenInput.type = 'hidden';
    newHiddenInput.name = sliderId;
    newHiddenInput.value = value || 0;
    form.appendChild(newHiddenInput);
  }
}

// Function to reset the slider value
function resetSliderValue(sliderId, valueElementId, defaultValue) {
  const slider = document.getElementById(sliderId);
  const valueElement = document.getElementById(valueElementId);
  // Retrieve the stored value from local storage
  const storedValue = localStorage.getItem(sliderId);
  // set the slider value to 0
  slider.value = 0;
  valueElement.textContent = slider.value;
}

// Get all the sliders on the page with class "slider"
const sliders = document.getElementsByClassName("slider");

// Loop through each slider and set up event listeners and reset values
for (let i = 0; i < sliders.length; i++) {
  const slider = sliders[i];
  const sliderId = slider.id;
  const valueElementId = sliderId + "Value";
  const defaultValue = slider.getAttribute("value");

  // Add event listener for slider input
  slider.addEventListener("input", function() {
    updateSliderValue(sliderId, valueElementId);
  });

  // Reset the slider value on page load
  resetSliderValue(sliderId, valueElementId, defaultValue);
  // Reset the age input value on page load
const ageInput = document.getElementById("age");
ageInput.value = 0;
}

function resetSelectValue(selectId, defaultValue) {
  const select = document.getElementById(selectId);
  // Set the select value to the default value
  select.value = defaultValue;
}

// Reset the select dropdowns to their default values
resetSelectValue("customer_type", "");
resetSelectValue("type_of_travel", "");
resetSelectValue("class_of_travel", "");

// Add event listeners for select dropdowns to update the default value
document.getElementById("customer_type").addEventListener("change", function() {
  localStorage.setItem("customer_type", this.value);
});

document.getElementById("type_of_travel").addEventListener("change", function() {
  localStorage.setItem("type_of_travel", this.value);
});

document.getElementById("class_of_travel").addEventListener("change", function() {
  localStorage.setItem("class_of_travel", this.value);
});