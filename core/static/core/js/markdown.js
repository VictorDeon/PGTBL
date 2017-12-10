$(document).ready(function(){
  // For each item in .content-markdown - not using
  // $(".content-markdown").each(function() {
  //   // Get the text content from .content-markdown class
  //   var content = $(this).text()

  //   // Transform the markdown text content in html content
  //   var markedContent = marked(content)
  //   $(this).html(markedContent)
  // })

  // Use image responsive on markdown - using
  $(".img-responsive-markdown img").each(function() {
    $(this).addClass("img-responsive");
  })

  // Get the item from wmd-input class
  var contentItem = $(".wmd-input")

  // Create a generic function to get the value of input
  // and transform the markdown value in html
  function setMarkdownToHTML(value) {
    // Transform the markdown value in html
    var markdownContent = marked(value)
    // Render the html into markdown-preview class
    $(".markdown-preview").html(markdownContent)
    // Insert img-responsive into img tag
    $(".markdown-preview img").each(function() {
      $(this).addClass("img-responsive");
    })
  }
  setMarkdownToHTML(contentItem.val())

  // Transform the preview dynamically by form
  contentItem.keyup(function(){
    var newContent = $(this).val()
    setMarkdownToHTML(newContent)
  })

})
