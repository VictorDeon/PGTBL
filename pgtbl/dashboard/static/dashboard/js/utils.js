function parser(string) {
  var array = []
  var array1 = string.split("],")
  for (i in array1) {
    array1[i] = array1[i].replace(/\s/g, '')
    array1[i] = array1[i].replace(/'/g, '')
    array1[i] = array1[i].replace("[", '')
    array1[i] = array1[i].replace("[", '')
    array1[i] = array1[i].replace("]", '')
    array1[i] = array1[i].replace("]", '')
    var array2 = array1[i].split(",")
    for (j = 1; j < array2.length; j++) {
        array2[j] = parseInt(array2[j])
    }
    array.push(array2)
  }
  return array
}

function parserOptions(string) {
    var array = []
    var array1 = string.split(",")
    for (i in array1) {
      var array2 = array1[i].split(": ")
      array2.shift() // remove the first element
      array2[0] = array2[0].replace(/'/g, '')
      array2[0] = array2[0].replace("}", '')
      array.push(array2[0])
    }
    return array
}