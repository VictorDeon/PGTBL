function validInput(select) {
  let alternatives = document.querySelectorAll(".alternatives");
  let selectedIndex = select.selectedIndex;
  let selectedOption = select[selectedIndex].value
  const alternativeLength = alternatives.length;
  const optionsLength = select.length;

  for (let i = 0; i < alternativeLength; i++) {
    if (selectedOption != alternatives[i].selectedOptions[0].value) {
      console.log(alternatives[i].selectedOptions[0].value)
    }
  }

}