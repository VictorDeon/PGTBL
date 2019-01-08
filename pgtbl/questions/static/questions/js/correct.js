(function() {
  // Verify if is update a question
  let question = document.getElementById("question");

  // If in question update, change the not checked input to disabled
  for (let i = 0; i <= 3; i++) {
    let checkbox = document.getElementById("id_alternatives-" + i + "-is_correct");

    if (question) {
      if (!checkbox.checked && checkbox.disabled) {
        checkbox.disabled = false;
      } else if (!checkbox.checked && !checkbox.disabled) {
        checkbox.disabled = true;
      }
    }
  }
}())

/*
  Function to disable not checked input when teacher
  click on it.
*/
function disableCheckboxs(currentCheckbox) {
  for (let i = 0; i <= 3; i++) {
    let checkbox = document.getElementById("id_alternatives-" + i + "-is_correct");

    if (checkbox.id != currentCheckbox.id) {
      if (!checkbox.checked && checkbox.disabled) {
        checkbox.disabled = false;
      } else if (!checkbox.checked && !checkbox.disabled) {
        checkbox.disabled = true;
      }
    }
  }
}