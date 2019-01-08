function validInput(number) {
  let alternatives = document.querySelectorAll(".alternatives");
  const length = alternatives.length;
  let values = [];
  let max = [];

  // Populate alternative values and max value of each alternative
  // and calculate sum of all alternatives.
  let sum = 0;
  for (let i = 0; i < length; i++) {
    sum += parseInt(alternatives[i].value);
    values.push(alternatives[i].value);
    max.push(alternatives[i].max);
  }

  // Populate max array with each alternative values
  for (let i = 0; i < length; i++) {
    max[i] = 4 - sum;
  }

  // Change max value of each alternative according input values
  for (let i = 0; i < length; i++) {
    alternatives[i].max = max[i] + values[i];
  }

  // Insert read only property in some inputs if sum is bigger than 4 or smaller than 0.
  if (sum >= 4 || sum < 0) {
    for (let i = 0; i < length; i++) {
      if (number.value != alternatives[i].value && alternatives[i].value == 0) {
        alternatives[i].readOnly = true;
      }
    }
  } else {
    for (let i = 0; i < length; i++) {
      alternatives[i].readOnly = false;
    }
  }
}